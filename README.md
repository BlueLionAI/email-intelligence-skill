# Email Intelligence Skill

A Claude skill for strategic email archive analysis. Turns Gmail, Outlook, or exported email archives into actionable revenue intelligence through a structured three-part framework.

## What it does

Runs a complete analytical workflow on any business email archive:

- **Part I — Service & Communication Analysis.** Tracks how offerings and messaging evolve over time. Detects shifts between technical and value-based framing. Identifies friction patterns in client communication.
- **Part II — Sales Performance & Conversion Analysis.** Win/loss metrics, root-cause analysis on lost deals, ghosted-lead detection, and open-to-sign cycle-time distribution.
- **Part III — Sales Strategy Optimization.** Email length vs. effectiveness correlation, gap identification, optimized templates per sales stage, and KPI definition.

Designed to work with Gmail (via MCP connector), Outlook, MBOX, EML, or CSV exports.

## Installation

### As a Claude skill (claude.ai)

1. Download the `email-intelligence/` folder
2. Zip it: `zip -r email-intelligence.zip email-intelligence/`
3. Upload through claude.ai → Settings → Capabilities → Skills

### As a project resource

Drop `email-intelligence/SKILL.md` into your Claude Project files. Claude will reference the framework when relevant queries are made.

### As a reference framework

The `SKILL.md` file is a complete prompt-engineered analytical framework. You can use it directly as a system prompt or instruction set with any capable LLM.

## Repository structure

```
email-intelligence-skill/
├── email-intelligence/
│   ├── SKILL.md                              # Main skill definition
│   ├── scripts/
│   │   └── cycle_time_analysis.py            # Reference Python implementation
│   ├── templates/
│   │   └── reengagement_email_template.md    # Ghosted-lead recovery patterns
│   └── references/
│       └── methodology_notes.md              # Analytical methodology guide
├── LICENSE
├── README.md
└── .gitignore
```

## Quick start

Once installed, invoke the skill with natural language:

```
Analyze my Gmail inbox for sales performance over the last 12 months.
Run a win/loss analysis. Find any ghosted leads.
Audit how my proposal messaging has evolved.
Run the gmailinsights framework on my exported MBOX file.
```

Claude will confirm scope, run a pilot scan first, then proceed to full analysis with intermediate validation checkpoints.

## What you get

- Executive summary with 6 to 8 prioritized insights
- Full analytical report covering all three parts
- Source dataset (CSV) with proposal IDs, dates, clients, statuses, and confidence scores
- Email template library — short, medium, and long variants per sales stage
- Refined value proposition in three lengths
- 30 / 60 / 90-day prioritized action plan

## Requirements

- A Claude account with skills capability enabled (claude.ai Pro or Team)
- Email archive in a supported format (Gmail / Outlook connector, or MBOX / EML / CSV export)
- Optional: CRM export (Pipedrive, HubSpot, Salesforce, Prospero) to enrich with deal-stage data

## Privacy

The skill treats all email content as confidential by default. Personal data is anonymized in shared outputs unless explicitly opted out. See `references/methodology_notes.md` for full data-handling guidance.

## Contributing

Issues and pull requests welcome. Suggested improvement areas:

- Additional pre-built email templates for new sales stages
- Connector recipes for Outlook, ProtonMail, FastMail
- Visualization templates for common output formats
- Localized template variants (currently English; templates can be translated)

## License

MIT — see `LICENSE`.

## Background

This skill was developed from a real-world implementation analyzing 50+ proposal events across a B2B services pipeline. The cycle-time analysis methodology in particular surfaced a counterintuitive finding: in the source data, **52% of deals signed in under 1 hour and zero deals signed between days 7 and 30** — meaning the entire sales motion needed to be redesigned around a fast-close window rather than a long-nurture cadence.

The framework is designed to surface that kind of structural insight in any email archive, regardless of industry or scale.
