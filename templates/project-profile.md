# Project Profile (Axis 1)

Complete before reviewing any code. Every "Unclear" is a finding.

**Product:** [NAME]
**Version / commit under review:** [REF]
**Review date:** [DATE]
**Reviewer:** [NAME]
**Compliance owner (signs off):** [NAME, ROLE]

## 1. Legal role

| Question | Answer | Evidence / reasoning |
|---|---|---|
| Who are the customers? (providers / plans / individuals / employers / other) | | |
| Does the product create, receive, maintain, or transmit PHI on behalf of a covered entity? | Yes / No / Unclear | |
| Resulting role | CE / BA / BA subcontractor / Neither / Hybrid | |
| BAAs executed upstream (with customers)? | Yes / No / N/A | |
| Does marketing claim "HIPAA compliant"? | Yes / No | |
| **Sign-off required on role?** | Yes / No | |

## 2. Specially protected data

| Category | Present? | Segmentable in data model? | Notes |
|---|---|---|---|
| Substance use disorder (Part 2 program records) | | | |
| Mental health / psychotherapy notes | | | |
| Reproductive health | | | |
| HIV / STI | | | |
| Genetic | | | |
| Minors (<13 / <18) | | | |
| Biometrics | | | |

## 3. Third-party data-flow inventory

| Third party | Purpose | Data categories sent | Contract (BAA / DUA / terms / none) | Disclosed to users? | Status |
|---|---|---|---|---|---|
| | | | | | |

## 4. Medical device determination

| Question | Answer |
|---|---|
| Any feature intended to diagnose, treat, mitigate, or prevent disease? | |
| Any clinical decision support? If so, do all four 520(o)(1)(E) criteria hold? | |
| Any AI/ML diagnostic, triage, or risk-scoring output? | |
| Determination on file from regulatory counsel? | Yes / No / Date |
| **Sign-off required?** | |

## 5. ONC information blocking

| Question | Answer |
|---|---|
| Certified health IT, HIE/HIN, or provider actor? | |
| Any practice that limits access, exchange, or use of EHI? Mapped exception? | |

## 6. User geography

| State | Meaningful user population? | Applicable state regime |
|---|---|---|
| Washington | | My Health My Data Act |
| Nevada | | SB 370 |
| Connecticut | | CTDPA health amendments |
| California | | CMIA, CCPA/CPRA |
| Texas | | HB 300, TDPSA |
| New York | | SHIELD, verify Health Information Privacy Act |
| Illinois | | BIPA (biometrics) |
| Colorado | | CPA, Colorado AI Act |
| Other | | |

## 7. Components in scope (Axis 2)

| Component | Touches health data? | In this review? | Reference checklist |
|---|---|---|---|
| Backend / API / DB | | | component-backend-api.md |
| Web frontend | | | component-web-frontend.md |
| Mobile app | | | component-mobile-app.md |
| Infrastructure / DevOps | | | component-infrastructure.md |
| AI / LLM | | | component-ai-llm.md |
| Integrations | | | component-integrations.md |

Components excluded: [name each and give the one-line reason]

## 8. Resulting applicable regimes

| Regime | Applies / Does not apply / Unclear | Reason |
|---|---|---|
| HIPAA Privacy / Security / Breach | | |
| FTC Act §5 | | |
| FTC Health Breach Notification Rule | | |
| 42 CFR Part 2 | | |
| State consumer health data laws | | |
| ONC information blocking | | |
| FDA (SaMD / CDS / 524B) | | |
| Section 1557 decision support duty | | |
| COPPA / TCPA / CAN-SPAM / PCI DSS | | |
| State AI laws | | |
| Customer certification requirements (SOC 2, HITRUST) | | |
