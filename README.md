# HIPAA Compliance MasterScan

Skill name: `hipaa-compliance-masterscan`. A Claude skill that acts as a **pre-release compliance gate for US digital health
software**. It is built to catch what a HIPAA-only review misses.

## Why

A HIPAA checklist answers "do we have the required safeguards?". It does not answer:

- Does HIPAA even apply to this product, or is it under the FTC and state law instead?
- Is there a tracking pixel on the patient portal?
- Does the mobile app put a diagnosis in a push notification?
- Are prompts containing patient data going to a model provider without a contract?
- Is the triage feature a medical device?

This skill asks those questions first, then runs component-specific checklists against
**evidence**, and ends with a release decision.

## The two-axis model

**Axis 1 - Legal scope.** Covered Entity / Business Associate / neither; specially
protected data categories; third-party data flows; FDA device status; ONC information
blocking; user states. Output: the list of regimes that apply.

**Axis 2 - Technical component.** Backend/API, web frontend, mobile app,
infrastructure/DevOps, AI/LLM, integrations. Only components that touch health data get
a checklist; the rest get a one-line exclusion.

## Layout

```
hipaa-compliance-masterscan/
├── .claude-plugin/
│   ├── plugin.json                  plugin manifest
│   └── marketplace.json             lets Claude Code install straight from this repo
├── skills/hipaa-compliance-masterscan/
│   ├── SKILL.md                     entry point: model, workflow, ratings, output format
│   ├── references/
│   │   ├── axis1-legal-scope.md     the six scoping questions
│   │   ├── beyond-hipaa.md          FTC, 42 CFR Part 2, state laws, ONC, FDA, AI laws, certifications
│   │   ├── hipaa-core-summary.md    compact HIPAA reference so the skill stands alone
│   │   ├── component-backend-api.md
│   │   ├── component-web-frontend.md
│   │   ├── component-mobile-app.md
│   │   ├── component-infrastructure.md
│   │   ├── component-ai-llm.md
│   │   └── component-integrations.md
│   ├── templates/
│   │   ├── project-profile.md       Axis 1 intake form
│   │   └── release-review-report.md report with release decision
│   └── scripts/
│       └── scan.py                  heuristic lead finder (trackers, LLM SDKs, storage, secrets)
├── install.sh                       copies the skill into ~/.claude/skills
└── package-skill.sh                 builds a .skill file for claude.ai / Claude Desktop
```

## Install

### Option 1 - Claude Code plugin (one command)

Inside Claude Code:

```
/plugin install hipaa-compliance-masterscan --marketplace mikenguyendev/hipaa-compliance-masterscan
```

Or from a shell:

```bash
claude plugin marketplace add mikenguyendev/hipaa-compliance-masterscan
```

```bash
claude plugin install hipaa-compliance-masterscan@mikenguyendev
```

### Option 2 - Copy the skill folder

```bash
curl -fsSL https://raw.githubusercontent.com/mikenguyendev/hipaa-compliance-masterscan/main/install.sh | sh
```

Installs to `~/.claude/skills/hipaa-compliance-masterscan/`. Run with `--project` from a
cloned copy to install into the current repo's `.claude/skills/` instead.

### Option 3 - claude.ai and Claude Desktop (.skill file)

Download `hipaa-compliance-masterscan.skill` from the latest
[release](https://github.com/mikenguyendev/hipaa-compliance-masterscan/releases), then
upload it under Settings > Capabilities > Skills. To build it yourself:

```bash
sh package-skill.sh
```

### Then

Ask, for example: "Run a HIPAA Compliance MasterScan on this repo" or
"Profile the regulatory scope of this product".

## Using the scanner

```bash
python3 -I skills/hipaa-compliance-masterscan/scripts/scan.py /path/to/repo
python3 -I skills/hipaa-compliance-masterscan/scripts/scan.py /path/to/repo --json > leads.json
```

It reports leads by category with a pointer to the checklist that governs them. It does
not clear anything.

## Ratings

| Rating | Release effect |
|---|---|
| Block | Do not release until fixed and re-verified |
| Fix before release | Fix, or written risk acceptance from the compliance owner |
| Track | Ticket with owner and date |
| Unverified | Treated as Fix before release until evidence is produced |
| Needs human sign-off | A named person must sign (legal role, device status, state reach, breach assessment) |

## Companion skills

Works alongside a core HIPAA reference skill (for example Anthropic's
`hipaa-compliance`) for 45 CFR detail, and a code security review skill for
vulnerability-level findings. Neither is required.

## Limits

- This is not legal advice. The final determination belongs to a qualified attorney or
  compliance officer.
- Content reflects US law and agency guidance as of mid-2026. Several rules cited here
  have been challenged or amended; verify against primary sources before relying on them.
- The scanner is pattern-based and will produce false positives and miss things.
- US only. GDPR and other non-US regimes are out of scope.

## Contributing

Corrections to legal references are especially welcome. Please cite the primary source
(CFR section, statute, agency guidance document, or court decision) in the pull request.

## License

MIT. See [LICENSE](LICENSE).
