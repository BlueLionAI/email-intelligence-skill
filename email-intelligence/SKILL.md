---
name: email-intelligence
description: "Strategic email analysis framework for any business or professional inbox. Analyzes email archives to extract revenue, sales, and communication insights through a three-part workflow: (1) Service & Value Analysis - tracking how offerings and messaging evolve over time, including the shift between technical and value-based framing; (2) Conversion Deep Dive - root-cause analysis of lost deals and identification of ghosted or stalled opportunities through win/loss metrics; (3) Sales Optimization - correlating email structure with response and win rates, and generating high-conversion templates. Use when a user wants to analyze their Gmail, Outlook, or exported email archive for sales performance, client patterns, communication style, missed opportunities, or proposal effectiveness."
license: MIT
---

# Email Intelligence — Strategic Email Analysis Framework

## Overview

This skill turns any business email archive into actionable revenue intelligence. It runs a structured three-part analysis covering communication evolution, conversion deep-dive, and sales optimization — producing evidence-based insights, ghosted-deal detection, cycle-time benchmarks, and ready-to-use email templates.

The framework is designed to work with Gmail or Outlook (via connector), or with exported archives in MBOX, EML, or CSV format.

## When to use this skill

Trigger this skill when the user asks to:

- Analyze their email inbox for sales performance, win rates, or proposal effectiveness
- Find ghosted leads or stalled deals
- Understand patterns in client communication
- Identify which messaging drives conversions
- Audit how their service offerings or value proposition has evolved
- Generate data-driven sales templates

Do not trigger for general email management, single-email drafting, or non-analytical email tasks.

## Workflow

### Phase 1 — Confirm scope before starting

Before running analysis, confirm with the user:

- [ ] Direct inbox access or exported data only?
- [ ] Anonymization required?
- [ ] Known list of lost deals for cross-reference?
- [ ] Priority clients, vendors, segments, or offerings?
- [ ] Time range to cover?
- [ ] Preferred deliverable format (report, dashboard, slides, spreadsheet)?

### Phase 2 — Pilot scan (300–500 emails)

Run a sample scan to:

- Detect data patterns and event types
- Build the classification framework
- Identify key clients, vendors, and offerings
- Flag the first wave of sales threads, proposals, and outcomes

Deliver pilot findings with confidence levels before proceeding to full analysis.

### Phase 3 — Full three-part analysis

Run all three parts described below. Each part produces independent deliverables that combine into the full analytical report.

### Phase 4 — Validation

Review representative email excerpts with the user. Confirm evidence-backed conclusions before final reporting.

### Phase 5 — Final reporting

Deliver intermediate outputs (CSV samples, early dashboards) and final deliverables in the user's preferred format.

---

## Part I — Service & Communication Analysis
*Focus: Strategic framing and value perception*

### 1.1 Offering evolution

Identify all products, services, or value propositions mentioned over time. Build a timeline showing the introduction of new offerings, shifts in the mix, and changes in messaging emphasis. Report frequency of mentions and inflection points by year, quarter, or month.

### 1.2 Value framing analysis

Classify core messaging into:

- **Technical / feature framing** — tools, formats, workflows, specifications
- **Value-based framing** — risk reduction, ROI, speed, quality, strategic outcomes

Provide yearly or quarterly percentages of each. Identify when communication shifted toward value-based messaging and correlate with conversion rate, response rate, or client engagement.

### 1.3 Communication style and friction

Analyze tone (formal, friendly, defensive, assertive), clarity, structure, assertiveness. Identify recurring objections, disputes, delays, and client/vendor friction. Evaluate whether communication maintains authority without creating conflict.

**Suggested methods:** keyword extraction, topic modeling (LDA / BERTopic), NER for offering detection, time-series trend analysis, sentiment / tone analysis, semi-supervised classification.

---

## Part II — Sales Performance & Conversion Analysis
*Focus: Conversion deep dive*

### 2.1 Lost deals — root cause analysis

For each lost opportunity, document the stated reason, infer root causes from email evidence (pricing, responsiveness, scope mismatch, operational gaps), and assign probability scores. Support with email excerpts and timing patterns.

### 2.2 Win / loss metrics

Calculate total proposals sent, deals won, deals lost. Break down win rate and win/loss ratio by year, offering type, client segment, and acquisition channel. Provide a clean source table: proposal ID, date sent, client, status (Won / Lost / Pending), deal value where available.

### 2.3 Unclosed opportunities — the "Unclosed Loop"

Pinpoint proposals with no clear outcome. Analyze follow-up frequency, time gaps between interactions, messaging quality, and client response patterns. Detect failure points: missing closing question, lack of pricing clarity, weak business context, no urgency framing, no clear next step.

Provide trigger-based follow-up frameworks and re-engagement templates.

**Suggested methods:** proposal-to-email matching, response rate / time analysis, dialogue classification, event-driven root cause modeling.

### 2.4 Cycle-time analysis (recommended addition)

Cross-reference proposal-opened events with proposal-signed events to calculate open-to-sign cycle time per deal. Bucket by time window (< 1h, 1–24h, 1–7d, 7–30d, > 30d) to identify the natural close window. The shape of this distribution reveals whether the user has a fast-close or slow-nurture pipeline — a critical input for follow-up cadence design.

---

## Part III — Sales Strategy Optimization

### 3.1 Email length vs. effectiveness

Correlate email length (words, sentences) with sales stage (discovery, proposal, follow-up, closing) and response / win rates. Provide optimal length benchmarks per stage and short vs. long sample formats.

### 3.2 Critical gaps in closing deals

Identify strategic gaps: missing closing moments, weak ROI articulation, lack of urgency or risk framing, vague pricing. Quantify impact on deal outcomes with real-world examples.

### 3.3 Optimization recommendations

**Messaging rewrite** — three variants per offering (Short / Medium / Long) in plain, non-technical language.

**Template delivery** — ready-to-use templates for:

1. Discovery / first contact
2. Initial proposal
3. Follow-up (unanswered proposal)
4. Closing email
5. Re-engagement (ghosted lead)

**KPI definition** — average response time, follow-up effectiveness rate, percentage of proposals with clear pricing, time-from-open-to-sign.

---

## Required Deliverables

1. **Executive summary (1 page)** — 6 to 8 key insights and immediate action items
2. **Full analytical report** — structured by Sections I–III with tables, charts, timelines
3. **Source dataset (CSV / Excel)** — per project / proposal: ID, date, client, offering, status, loss reason, links, confidence scores
4. **Email template library** — short, medium, and long variants per sales stage
5. **Refined value proposition** — three versions: one-liner, paragraph, full sales statement
6. **Prioritized action plan** — 30 / 60 / 90-day roadmap with measurable milestones
7. **Lessons learned and strategic risks** — summary of insights and pitfalls

---

## Execution Principles

- **Evidence-based conclusions.** Every claim assigns a confidence level (High / Medium / Low) and a methodological justification.
- **No speculation.** Where uncertainty exists, present ranked, data-backed hypotheses rather than guesses.
- **Privacy by default.** Treat email content as confidential. Anonymize personal data in shared outputs unless the user explicitly opts out.
- **Auditability.** Deliver raw data alongside insights so all findings can be traced.
- **Structured workflow.** Follow the phases in order. Surface intermediate outputs at each phase rather than dumping a single final report.

---

## Technical Specs

**Supported inputs:** Gmail (via MCP connector), Outlook, MBOX, EML, CSV exports.

**Required fields:** date, sender, recipients (To / CC), subject, body (plain or HTML), attachments (names / types), thread identifiers (message ID, references).

**CRM integration:** Pull in CRM exports where available (Pipedrive, HubSpot, Salesforce, Prospero, etc.) to enrich email data with deal stage, value, and outcome.

**Reproducibility:** When code is used, provide a pipeline outline (Python or R) and list libraries (e.g., pandas, scikit-learn, transformers, BERTopic). Reference scripts are in `scripts/`.

---

## Bundled Resources

- `scripts/cycle_time_analysis.py` — reference implementation for Part II cycle-time analysis
- `templates/reengagement_email_template.md` — proven re-engagement framework for ghosted leads
- `references/methodology_notes.md` — detailed guidance on classification, sampling, and confidence scoring
