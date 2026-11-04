# Health Release Review: [PRODUCT / COMPONENT]

**Release decision:** BLOCK / FIX BEFORE RELEASE / RELEASE WITH TRACKED ITEMS
**Review date:** [DATE] · **Reviewer:** [NAME] · **Compliance owner:** [NAME]
**Version under review:** [commit / build]
**Reviewed components:** [list] · **Not reviewed:** [list and why]
**Evidence basis:** [code at commit X / infrastructure config / vendor contracts / screenshots / interviews only]

> This review is for informational purposes only and does not constitute legal advice.
> A qualified attorney or compliance officer must make the final compliance determination.

## 1. Summary

[Three to five sentences: what the product is, its legal role, the decision, and the
one or two issues that drive the decision.]

## 2. Axis 1 - Legal scope

| Regime | Status | Reason |
|---|---|---|
| HIPAA | Applies / Does not apply / Unclear | |
| FTC Act §5 + Health Breach Notification Rule | | |
| 42 CFR Part 2 | | |
| State consumer health data laws | | |
| ONC information blocking | | |
| FDA | | |
| Section 1557 / state AI laws | | |
| Other | | |

## 3. Findings

Sorted by rating, then component. Every row has evidence.

| # | Rating | Component | Finding | Rule / reference | Evidence | Fix |
|---|---|---|---|---|---|---|
| 1 | Block | | | | file:line / config path | |
| 2 | Fix before release | | | | | |
| 3 | Track | | | | | |
| 4 | Unverified | | | | what was asked for and not produced | |

## 4. Items requiring human sign-off

| Determination | Why it cannot be made here | Who signs |
|---|---|---|
| Legal role (CE / BA / neither) | | |
| FDA device status | | |
| State law reach | | |
| Breach risk assessment for [incident] | | |

## 5. What was verified as implemented

[Short list of controls with evidence, so the reader knows what is covered. Keep it
honest: controls seen in code or config, not described in conversation.]

## 6. Out of scope and not verified

- [component or control] - [reason]

## 7. Re-review conditions

The decision above is valid for the version named. Re-review is required when:
- a new third party receives health data,
- an AI/LLM provider or model version changes for a clinical feature,
- a new component touches health data,
- user base expands into a new state with a consumer health data law,
- a Block or Fix item is remediated (verify the fix, do not accept a description).
