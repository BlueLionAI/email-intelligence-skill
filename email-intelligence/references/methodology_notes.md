# Methodology Notes — Email Intelligence Framework

This document explains the analytical decisions, sampling strategies, and confidence-scoring approach used by the email-intelligence skill. Use it as a reference when running large analyses or explaining results to stakeholders.

## Sampling strategy

### Pilot scan size

The recommended pilot size is **300 to 500 emails** drawn from across the full archive period. This is large enough to surface dominant patterns and rare-but-important signals, while small enough to validate the classification framework before committing to a full run.

For archives under 5,000 emails, skip the pilot and run full analysis directly.

For archives over 100,000 emails, run pilots in two passes — one stratified random sample for breadth, one targeted scan on high-signal threads (proposals, signed contracts, lost deals) for depth.

### Stratification

When sampling, stratify across:

- **Time** — equal coverage across years/quarters to catch evolution
- **Outcome** — sample from won, lost, and ghosted cohorts proportionally
- **Volume** — include both high-frequency clients and one-off prospects
- **Channel** — inbound, outbound, referral, vendor

Avoid sampling only "interesting" or "recent" emails — that biases toward survivorship.

---

## Classification framework

### Service / offering detection

Use a hybrid approach:

1. **Seed list** — start with the user's known service catalog (extracted from their website, marketing materials, or stated by the user)
2. **NER expansion** — run named-entity recognition on a sample to surface offerings the user didn't mention
3. **User validation** — confirm the final list with the user before tagging at scale

Common pitfalls: synonyms that look unrelated (e.g., "TQA" and "quality assurance" and "QA review"), legacy offering names that no longer appear, and offerings that are described differently per segment.

### Value framing classification

Two-class supervised classification:

- **Technical / feature framing** — describes *what* the offering is. Tools, formats, file types, workflow steps, delivery mechanisms.
- **Value-based framing** — describes *why* it matters. Risk reduction, ROI, speed advantages, quality outcomes, strategic positioning.

Train a small classifier (a few hundred labeled examples is usually enough) or use zero-shot prompting with a clear definition. Validate the classifier on a held-out set before scaling.

A single email can contain both — count framing per *paragraph* or *claim*, not per email, for cleaner statistics.

### Outcome labeling

Outcomes are not always explicit. Build a hierarchy:

1. **Signed event** — proposal-tracker confirmation, contract attachment, payment receipt → confirmed Won
2. **Explicit decline** — "we've decided to go another direction", "not at this time" → confirmed Lost
3. **Stalled / ghosted** — proposal opened or sent, no follow-up signal within 60 days → inferred Lost
4. **In progress** — recent activity within 14 days → Pending

The 60-day cutoff for ghost detection is a default. Adjust based on the user's typical sales cycle (validate against the cycle-time analysis output).

---

## Cycle-time analysis

### Why match opens to signs

Most CRMs report a single "deal closed" date. That hides the actual decision moment. Matching the proposal-opened event to the proposal-signed event reveals the *real* close window — usually much shorter than reported sales cycles.

### Match window

Default match window is **60 days** between open and sign. This catches both fast-closes and slow-burn deals while filtering out noise from old proposal re-opens.

If the user has multiple proposal versions for the same client, match to the *most recent* prior open within the window. Don't match across version boundaries unless versioning data isn't available.

### Buckets

The standard buckets — `< 1h`, `1-24h`, `1-7d`, `7-30d`, `> 30d` — are designed to surface the typical B2B pattern where deals either close fast or not at all. The shape of this distribution is itself a finding: a flat distribution suggests a complex sales process; a heavily front-loaded distribution suggests low-friction, high-intent buyers.

---

## Confidence scoring

Every claim in the final report should carry a confidence label:

| Level | Definition | Example |
|---|---|---|
| **High** | Direct evidence in 5+ examples, no contradicting evidence | "Win rate dropped 30% in November 2025" (counted from full data) |
| **Medium** | Pattern visible but limited evidence or some ambiguity | "Legal vertical responds better to precision framing than urgency" |
| **Low** | Plausible inference but limited support | "The November dip was caused by vendor capacity issues" |

Never present Low-confidence inferences as conclusions. Frame them as *hypotheses to validate*, ideally with a suggested next step.

---

## Privacy and data handling

### Default posture

Treat all email content as confidential by default. In any output that may be shared:

- Anonymize personal names, email addresses, phone numbers
- Aggregate rather than quote where possible
- Strip or redact attachments and links

### When to opt out of anonymization

Only when the user explicitly requests it AND the output is for internal-only use AND the user owns the data. Document the decision in the report metadata.

### Vendor and third-party data

Treat vendor data with the same care as client data. Don't include vendor pricing, contract terms, or capacity information in shared deliverables without explicit permission.

---

## Common analytical pitfalls

### Survivorship bias

If you only analyze emails from active clients, you miss the patterns of *what made other prospects walk away*. Always include the lost and ghosted cohorts in qualitative analysis, even if they're smaller.

### Confounding the proposal with the sales motion

A high win rate at the proposal stage doesn't mean the proposal is good — it might mean qualification before the proposal is excellent. Always look upstream (lead source, discovery quality, scoping conversations) before attributing wins to the proposal itself.

### Assuming silence means "no"

In some segments (legal, finance, government), long silences are normal and don't necessarily indicate a lost deal. Validate ghost-detection thresholds against the user's historical patterns per segment, not as a single global rule.

### Over-interpreting small samples

A 5-deal vertical with a 60% win rate is not the same data point as a 50-deal vertical with a 60% win rate. Always report sample sizes alongside percentages, and flag insights drawn from samples below ~15 events as exploratory rather than conclusive.

---

## Suggested tooling

- **Data wrangling:** pandas, polars
- **Classification:** scikit-learn for traditional ML, transformers (HuggingFace) for zero-shot or fine-tuned classification
- **Topic modeling:** BERTopic for modern semantic clustering, classic LDA for keyword-driven analysis
- **NER:** spaCy or transformers-based pipelines
- **Visualization:** matplotlib for static, plotly for interactive dashboards
- **Email parsing:** mailbox (stdlib) for MBOX, eml-parser for EML, direct API access for Gmail / Outlook

Provide the user a reproducible pipeline (script or notebook) so they can re-run the analysis themselves on future data.
