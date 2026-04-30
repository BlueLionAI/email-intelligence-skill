#!/usr/bin/env python3
"""
Cycle-time analysis for proposal open-to-sign tracking.

Cross-references proposal-opened events with proposal-signed events to compute
per-deal cycle time. Outputs distribution buckets, ghosted-lead detection, and
top-client win counts.

Inputs:
    - opened_events: list of (client_name, ISO8601_timestamp) tuples
    - signed_events: list of (client_name, ISO8601_timestamp) tuples

Outputs:
    - Cycle-time distribution (< 1h, 1-24h, 1-7d, 7-30d, > 30d)
    - Median, mean, min, max cycle times
    - Ghosted leads (opened but not signed within 60 days)
    - Top clients by win count

Usage:
    Adapt the OPENED and SIGNED lists below to your data source.
    Output is plain text suitable for piping or capture.
"""
from datetime import datetime, timezone
from collections import defaultdict
import statistics


def parse_timestamp(ts: str) -> datetime:
    """Parse ISO 8601 timestamp, handling Z suffix."""
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def normalize_client_name(name: str) -> str:
    """
    Normalize client names to handle variations.

    Customize this function with your own client-name aliases. The default
    implementation lowercases and strips common business-entity suffixes.
    """
    n = name.lower().strip()
    # Strip common entity suffixes
    for suffix in [" ltd", " llc", " inc", " gmbh", " bv", " sa", " ag"]:
        if n.endswith(suffix):
            n = n[: -len(suffix)].strip()
    return n


def analyze_cycles(
    opened: list[tuple[str, str]],
    signed: list[tuple[str, str]],
    match_window_days: int = 60,
    ghost_threshold_days: int = 14,
    reference_date: datetime | None = None,
) -> dict:
    """
    Run the full cycle-time analysis.

    Args:
        opened: list of (client_name, iso_timestamp) for proposal-opened events
        signed: list of (client_name, iso_timestamp) for proposal-signed events
        match_window_days: max days between open and sign to consider them paired
        ghost_threshold_days: opens older than this with no sign are ghosted
        reference_date: "now" for ghost detection. Defaults to current UTC time.

    Returns:
        dict with cycles, stats, buckets, ghosted, win_counts
    """
    if reference_date is None:
        reference_date = datetime.now(timezone.utc)

    # Group by normalized client name
    opens_by_client: dict[str, list[datetime]] = defaultdict(list)
    signs_by_client: dict[str, list[datetime]] = defaultdict(list)
    display_name: dict[str, str] = {}

    for c, t in opened:
        k = normalize_client_name(c)
        opens_by_client[k].append(parse_timestamp(t))
        display_name.setdefault(k, c)

    for c, t in signed:
        k = normalize_client_name(c)
        signs_by_client[k].append(parse_timestamp(t))
        display_name[k] = c  # signed events take naming priority

    # Match each sign to the most recent prior open within the match window
    cycles = []
    for k, signs in signs_by_client.items():
        opens = sorted(opens_by_client.get(k, []))
        for s in signs:
            priors = [
                o for o in opens
                if o <= s and (s - o).days <= match_window_days
            ]
            if priors:
                o = max(priors)
                hours = (s - o).total_seconds() / 3600
                cycles.append({
                    "client": display_name[k],
                    "opened_at": o,
                    "signed_at": s,
                    "cycle_hours": hours,
                })

    cycles.sort(key=lambda c: c["cycle_hours"])

    # Distribution buckets
    buckets = {"<1h": 0, "1-24h": 0, "1-7d": 0, "7-30d": 0, ">30d": 0}
    hours_list = [c["cycle_hours"] for c in cycles]
    for h in hours_list:
        if h < 1:
            buckets["<1h"] += 1
        elif h < 24:
            buckets["1-24h"] += 1
        elif h < 168:
            buckets["1-7d"] += 1
        elif h < 720:
            buckets["7-30d"] += 1
        else:
            buckets[">30d"] += 1

    # Ghosted: opens with no matching sign within match window, and old enough
    ghosted = []
    for k, opens in opens_by_client.items():
        signs = sorted(signs_by_client.get(k, []))
        for o in opens:
            future_signs = [
                s for s in signs
                if s >= o and (s - o).days <= match_window_days
            ]
            age_days = (reference_date - o).days
            if not future_signs and age_days >= ghost_threshold_days:
                ghosted.append({
                    "client": display_name[k],
                    "opened_at": o,
                    "days_since_open": age_days,
                })
    ghosted.sort(key=lambda g: g["opened_at"], reverse=True)

    # Top clients by win count
    win_counts = sorted(
        [(display_name[k], len(s)) for k, s in signs_by_client.items()],
        key=lambda x: -x[1],
    )

    stats = {}
    if hours_list:
        stats = {
            "matched_cycles": len(cycles),
            "total_signs": len(signed),
            "median_hours": statistics.median(hours_list),
            "mean_hours": statistics.mean(hours_list),
            "min_hours": min(hours_list),
            "max_hours": max(hours_list),
        }

    return {
        "cycles": cycles,
        "stats": stats,
        "buckets": buckets,
        "ghosted": ghosted,
        "win_counts": win_counts,
    }


def format_report(result: dict) -> str:
    """Pretty-print the analysis output."""
    lines = []
    s = result["stats"]
    if s:
        lines.append(f"=== STATS ===")
        lines.append(f"Matched cycles: {s['matched_cycles']} of {s['total_signs']}")
        lines.append(f"Median cycle:   {s['median_hours']:.1f}h ({s['median_hours']/24:.1f}d)")
        lines.append(f"Mean cycle:     {s['mean_hours']:.1f}h ({s['mean_hours']/24:.1f}d)")
        lines.append(f"Range:          {s['min_hours']:.1f}h to {s['max_hours']:.1f}h")
        lines.append("")

    total = sum(result["buckets"].values())
    if total:
        lines.append("=== DISTRIBUTION ===")
        for bucket, count in result["buckets"].items():
            pct = count / total * 100
            lines.append(f"  {bucket:>8}: {count:>3} ({pct:.0f}%)")
        lines.append("")

    if result["ghosted"]:
        lines.append(f"=== GHOSTED ({len(result['ghosted'])} opens, no sign within window) ===")
        for g in result["ghosted"][:20]:
            lines.append(f"  {g['days_since_open']:>4}d ago  {g['client'][:50]}")
        lines.append("")

    if result["win_counts"]:
        lines.append("=== TOP CLIENTS BY WIN COUNT ===")
        for name, count in result["win_counts"][:10]:
            lines.append(f"  {count}x  {name[:50]}")

    return "\n".join(lines)


# === EXAMPLE USAGE ===
if __name__ == "__main__":
    # Replace these with data extracted from your CRM, email export, or webhook log
    OPENED = [
        ("Acme Corp", "2026-01-15T09:00:00Z"),
        ("Globex", "2026-01-20T14:30:00Z"),
        ("Initech", "2026-02-01T10:00:00Z"),
    ]
    SIGNED = [
        ("Acme Corp", "2026-01-15T09:45:00Z"),  # 45min cycle
        ("Globex", "2026-01-23T16:00:00Z"),     # 3-day cycle
        # Initech opened but never signed -> ghosted
    ]

    result = analyze_cycles(OPENED, SIGNED)
    print(format_report(result))
