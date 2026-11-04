# Axis 1 - Legal Scope

The first job of a release review is deciding **which laws apply**. Get this wrong and
every later checklist is aimed at the wrong target. Work through the five questions below,
record the answer and the reasoning in the project profile, and mark anything uncertain
as **Needs human sign-off**.

---

## Q1. What is the product's legal role?

| Role | Typical examples | What applies |
|---|---|---|
| **Covered Entity (CE)** | Provider that bills electronically, health plan, clearinghouse | Full HIPAA Privacy, Security, and Breach rules |
| **Business Associate (BA)** | EHR vendor, telehealth platform serving providers, billing SaaS, cloud host holding PHI, analytics vendor processing PHI for a CE | HIPAA Security Rule directly; Privacy Rule obligations via BAA; breach notification to the CE |
| **Subcontractor of a BA** | Sub-processor, hosting provider for a BA, offshore dev shop with prod access | Same as BA; BAA with the upstream BA |
| **Neither (direct-to-consumer)** | Wellness app, period tracker, symptom checker sold to individuals, fitness wearable, consumer genetic test | **Not HIPAA.** FTC Act §5, FTC Health Breach Notification Rule, state consumer health data laws, app store policies |
| **Hybrid** | DTC app that also sells a B2B version to clinics; provider-facing tool that also stores consumer self-reported data | Both sets. Review the strictest path for each data flow |

### Decision rules

- HIPAA attaches to **entities and relationships**, not to the sensitivity of the data.
  A symptom checker holding diagnoses is not under HIPAA if no CE or BA relationship exists.
- A product becomes a BA the moment it creates, receives, maintains, or transmits PHI
  **on behalf of** a CE. "We only store it" still counts. "We only see it in transit and
  it is encrypted end-to-end" may qualify for the conduit exception, which is narrow
  (telecoms, ISPs, couriers). Flag any conduit claim for human sign-off.
- A product that receives PHI from a CE under a patient's HIPAA authorization (not on
  the CE's behalf) is generally not a BA, but the data stays sensitive under FTC and
  state law.
- When the role is unclear, review against **both** HIPAA and the FTC/state set.

### Evidence to collect

- Customer contracts: are customers providers, plans, or individuals?
- Any executed BAAs (upstream and downstream).
- Marketing copy: does it claim "HIPAA compliant"? That claim itself is reviewable under
  FTC §5 if unsupported.

---

## Q2. Which categories of specially protected data are present?

| Category | Extra regime | Practical effect |
|---|---|---|
| **Substance use disorder treatment records** from a Part 2 program | 42 CFR Part 2 | Consent requirements stricter than HIPAA; redisclosure limits; segmentation or tagging of Part 2 data; breach rules aligned to HIPAA since the 2024 final rule (compliance date February 16, 2026) |
| **Mental health / psychotherapy notes** | HIPAA psychotherapy-notes rule, state law | Separate authorization for psychotherapy notes; many states restrict disclosure further |
| **Reproductive health** | HIPAA reproductive-health privacy rule (2024) - **vacated by a federal district court in 2025; verify current status**; state laws | Attestation requirements for certain disclosures may or may not be in force; several states have shield laws |
| **HIV / STI status** | State law | Many states require specific consent for disclosure |
| **Genetic information** | GINA, state genetic privacy laws | Restrictions on use for insurance/employment; some states require consent for genetic data sale |
| **Minors (under 13 / under 18)** | COPPA (under 13), state minor-consent laws, parental access rules | Verifiable parental consent; conflicts between parent access and minor confidentiality for sensitive services |
| **Biometrics** | Illinois BIPA, Texas CUBI, Washington HB 1493, others | Written consent, retention schedule, no sale; BIPA has a private right of action |

### Evidence to collect

- Data model / schema: which tables or fields hold these categories?
- Can the system **tag or segment** specially protected records? If not, the strictest
  rule applies to everything mixed with them.

---

## Q3. Which third parties receive data, and under what?

Build a **data-flow inventory**. For each third party record: what data, why, under what
contract, and whether the user is told.

| Third-party type | HIPAA path (CE/BA) | Non-HIPAA path (DTC) |
|---|---|---|
| Cloud host (AWS, Azure, GCP, others) | BAA required; configure only HIPAA-eligible services | Contract with security terms; still a breach vector |
| Analytics / product telemetry | BAA or no PHI sent; **no ad-tech on authenticated pages** | Must be disclosed; health data to ad-tech has drawn FTC enforcement |
| Advertising / attribution SDKs (pixels, mobile attribution) | Almost never permissible with PHI | Disclose; many state laws require opt-in consent for sharing consumer health data |
| LLM / AI API provider | BAA required; zero data retention or equivalent; no training on inputs | Disclose; same retention and training concerns |
| SMS / email / push providers | BAA required if message content is PHI | TCPA and CAN-SPAM consent; content minimization |
| Payment processor | Usually not a BA for card data alone; PCI DSS applies | PCI DSS |
| EHR / HIE / lab / pharmacy connectors | BAA or treatment-relationship basis; information blocking rules | n/a or state law |
| Customer support tooling (ticketing, session replay, chat) | BAA if PHI can land in tickets or recordings | Disclose; session replay on health pages is high risk |
| Error tracking / logging SaaS | BAA, or strip PHI before sending | Strip PHI |
| Offshore or contractor developers with production access | BAA / subcontractor agreement | Contract with security terms |

Anything on this list with **no contract on file** is a Block or Fix-before-release
finding, depending on whether PHI is involved.

---

## Q4. Is any part of the product a medical device?

Software is a device under the Federal Food, Drug, and Cosmetic Act if it is intended
for diagnosis, cure, mitigation, treatment, or prevention of disease. Key carve-outs
and traps:

- **Clinical decision support (CDS)** is excluded under section 520(o)(1)(E) **only**
  if it meets all four criteria (not analyzing medical images or signals; displays or
  analyzes medical information; supports but does not replace clinician judgment; lets
  the clinician independently review the basis). FDA's 2022 CDS guidance interprets these
  narrowly. Time-critical recommendations and single-output recommendations often fail.
- **General wellness** products (low risk, lifestyle claims only) are generally outside
  enforcement. "Helps manage your diabetes" is not general wellness.
- **AI/ML diagnostic or triage features** aimed at patients or clinicians are very likely
  devices.
- **Device cybersecurity**: for "cyber devices" (software, network-connected), section
  524B of the FD&C Act requires an SBOM, a vulnerability management plan, and
  postmarket cybersecurity processes in premarket submissions.
- Quality system: the Quality Management System Regulation (21 CFR Part 820, aligned
  with ISO 13485) took effect in February 2026.

Any "possibly a device" answer is **Needs human sign-off** from regulatory counsel.
This skill does not perform device classification.

---

## Q5. Does ONC information blocking apply?

Applies to **health IT developers of certified health IT**, **health information
networks/exchanges**, and **health care providers**. If the product holds certified
health IT or sits in the exchange path, practices that interfere with access, exchange,
or use of electronic health information (EHI) are prohibited unless an exception
(45 CFR Part 171) applies. Civil money penalties apply to developers and networks;
provider disincentives are set through CMS programs.

Common engineering-level issues:
- Export of EHI deliberately degraded or delayed.
- API access gated on fees or terms not permitted by the exceptions.
- Patient access via third-party apps blocked beyond what the Privacy or Security
  exceptions allow.

---

## Q6. Where are the users?

State law applies by **resident**, not by where the company sits. Record the states
with meaningful user populations and load the state section of `beyond-hipaa.md`.
At minimum consider Washington, Nevada, Connecticut, California, Texas, New York,
Illinois, and Colorado, plus any state with a comprehensive privacy law that treats
health data as sensitive.

---

## Output of Axis 1

A completed `templates/project-profile.md` with:
1. Legal role and reasoning (flagged for sign-off if not certain).
2. Specially protected data categories present and whether they are segmentable.
3. Third-party data-flow inventory with contract status.
4. Device determination status.
5. Information blocking applicability.
6. State coverage.
7. The resulting list of applicable regimes, feeding Step 2 of the workflow.
