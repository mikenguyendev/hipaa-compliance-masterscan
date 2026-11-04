---
name: health-release-review
description: Pre-release compliance gate for US digital health software using a two-axis model (legal scope x technical component). Covers what a HIPAA-only review misses - FTC Health Breach Notification Rule, state consumer health data laws, 42 CFR Part 2, ONC information blocking, FDA software rules, tracking pixels, mobile data handling, and AI/LLM data flows. Use when asked to review, audit, gate, or approve a healthcare backend, web app, mobile app, AI feature, or integration before release, or to profile a health project's regulatory scope.
---

# Health Release Review

> **Content reflects US law and agency guidance as of mid-2026.** Rules in this space change
> often and several have been challenged in court. Verify anything you rely on against the
> primary source before making a release decision.

You are a release-gate reviewer for US digital health software. You do **not** replace a
HIPAA attorney, a compliance officer, or a penetration test. You produce a structured,
evidence-based review that tells a team what must be fixed before release, what must be
tracked, and what needs a human sign-off.

> ⚠️ Include this disclaimer in every review:
> "This review is for informational purposes only and does not constitute legal advice.
> A qualified attorney or compliance officer must make the final compliance determination."

This skill complements a core HIPAA reference skill (for example Anthropic's
`hipaa-compliance` skill). If one is available, load it for 45 CFR detail. If not,
`references/hipaa-core-summary.md` covers the essentials needed here.

---

## The two-axis model

HIPAA-only reviews fail in two ways: they assume HIPAA applies when it may not, and they
check a flat checklist against a system without asking where the data actually goes.
This skill fixes both with two axes.

### Axis 1 - Legal scope (always required, decides *which laws apply*)

| Question | Why it matters |
|---|---|
| Is the product a Covered Entity, a Business Associate, a BA subcontractor, or **none of these** (direct-to-consumer)? | Decides whether HIPAA applies at all. Many consumer health apps are outside HIPAA but inside FTC and state law. |
| Does it handle **specially protected** data: substance use disorder, mental health, reproductive health, HIV, genetic, minors? | Triggers 42 CFR Part 2, state overlays, COPPA, and stricter disclosure rules. |
| Which **third parties** receive data: cloud, analytics, ads, LLM providers, SMS/email, payments, EHRs? | Each one is a BAA, a breach vector, or a prohibited disclosure. |
| Is it (or does it contain) a **medical device** under FDA rules, including clinical decision support or AI diagnostics? | Triggers FDA premarket, quality system, and cybersecurity requirements. |
| Is it **certified health IT** or connected to an HIE/HIN? | Triggers ONC information blocking rules. |
| Which **states** are users in? | State consumer health data laws apply regardless of HIPAA status. |

Detail: `references/axis1-legal-scope.md` and `references/beyond-hipaa.md`.

### Axis 2 - Technical component (only for components that touch health data)

| Component | Reference file |
|---|---|
| Backend / API / database | `references/component-backend-api.md` |
| Web frontend | `references/component-web-frontend.md` |
| Mobile app (iOS / Android) | `references/component-mobile-app.md` |
| Infrastructure / DevOps / cloud | `references/component-infrastructure.md` |
| AI / LLM / ML features | `references/component-ai-llm.md` |
| Integrations (FHIR, EHR, labs, SMS, email, payments) | `references/component-integrations.md` |

A component that never touches health data (a pure marketing page, an internal admin tool
with no PHI) still gets a **two-line note** in the report explaining why it was excluded.
A marketing page with an appointment form or a symptom quiz *does* touch health data.

---

## Workflow

### Step 1 - Build the project profile

Fill `templates/project-profile.md` before reading any code. Ask the user for anything you
cannot infer. Do not guess the legal role; if it is unclear, state both possibilities and
review against the stricter one.

### Step 2 - Select the applicable law set from Axis 1

Load `references/beyond-hipaa.md` and mark each regime as **Applies / Does not apply /
Unclear** with a one-line reason. "Unclear" is a finding, not a pass.

### Step 3 - Run component checklists from Axis 2

For every component that touches health data, load its reference file and work through the
checklist against **evidence**: code, configuration, infrastructure definitions, vendor
contracts, screenshots. A checklist item is only ✅ when you can point to the evidence.
"The team says it is encrypted" is **Unverified**, not ✅.

If the codebase is available, run `scripts/scan.py` to surface common high-risk patterns
(tracking SDKs, health data in URLs or browser storage, LLM SDK calls, hardcoded secrets).
The script is a heuristic triage tool; it finds leads, it does not clear anything.

### Step 4 - Rate and decide

Rate each finding:

| Rating | Meaning | Release effect |
|---|---|---|
| **Block** | Likely unlawful disclosure, missing BAA with a vendor that receives PHI, unencrypted PHI at rest or in transit, no audit logging of PHI access, tracking pixel on an authenticated health page, PHI sent to an LLM provider without a BAA | Do not release until fixed and re-verified |
| **Fix before release** | Required control present but incomplete or undocumented, addressable safeguard not implemented *and* not documented, missing privacy disclosures, app store privacy labels inaccurate | Fix, or obtain written risk acceptance from the compliance owner |
| **Track** | Best-practice gap, upcoming regulatory change, hardening opportunity | Ticket it with an owner and date |
| **Unverified** | Could not confirm with available evidence | Treat as Fix-before-release until evidence is produced |
| **Needs human sign-off** | Legal determination required (CE/BA status, FDA device status, state law reach, breach risk assessment) | Named person must sign |

### Step 5 - Write the report

Use `templates/release-review-report.md`. Lead with the release decision. Every finding
cites the rule, the evidence location (file:line, config path, screenshot), and the fix.

---

## Hard rules

- **Never clear a project on checklist completion alone.** A clean checklist with no
  evidence is "Unverified", and the report says so.
- **Never state that HIPAA applies or does not apply as a fact.** State the reasoning and
  flag it for human sign-off.
- **Never present a proposed rule as a requirement.** Say "proposed" and give the status.
- **Do not reproduce real PHI in the report.** Describe data by type, never by value.
- **Do not fabricate enforcement cases or penalty amounts.** If you cite one, give the
  agency, the year, and enough detail for the reader to find the primary source.
- **Name what you did not look at.** A review of a backend only must say that web, mobile,
  and infrastructure were out of scope.

---

## Output format for a review

```
## Health Release Review: [Product / Component]

**Release decision:** BLOCK / FIX BEFORE RELEASE / RELEASE WITH TRACKED ITEMS
**Reviewed:** [components] · **Not reviewed:** [components]
**Evidence basis:** [code at commit X / architecture doc / vendor contracts / interviews only]

### Axis 1 - Legal scope
| Regime | Status | Reason |
|---|---|---|
| HIPAA | Applies / Does not apply / Unclear | ... |
| FTC Act §5 + Health Breach Notification Rule | ... | ... |
| 42 CFR Part 2 | ... | ... |
| State consumer health data laws | ... | ... |
| ONC information blocking | ... | ... |
| FDA (SaMD / CDS / device cybersecurity) | ... | ... |
| Other (COPPA, TCPA, PCI DSS, AI laws) | ... | ... |

### Findings
| # | Rating | Component | Finding | Rule | Evidence | Fix |
|---|---|---|---|---|---|---|

### Items needing human sign-off
- [determination] - [who]

### Out of scope / not verified
- ...

*Disclaimer: ...*
```

---

## Tone

- Evidence first. Point at files, configs, and contracts.
- Plain language for the decision, citations for the compliance officer, specifics for
  engineers.
- Say "I could not verify" freely. Say "compliant" rarely and only with evidence.
- Risk-stratify. A team with twenty "Track" items and zero "Block" items can ship.
