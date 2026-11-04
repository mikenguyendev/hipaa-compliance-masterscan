# Beyond HIPAA - The Other US Regimes

Load this after Axis 1. Mark each regime **Applies / Does not apply / Unclear** with a
reason. Content reflects mid-2026; verify before relying on any item.

---

## 1. FTC Act §5 and the FTC Health Breach Notification Rule

**Who:** Essentially every health-adjacent company. §5 bars unfair or deceptive
practices. The Health Breach Notification Rule (16 CFR Part 318, amended 2024) covers
**vendors of personal health records**, PHR-related entities, and their service
providers that are **not** HIPAA covered entities or business associates. The 2024
amendment made explicit that most health apps and connected devices that draw
information from multiple sources are covered.

**What it requires:**
- A "breach of security" includes **unauthorized disclosure**, not just hacking. Sharing
  health data with an ad network without authorization has been treated as a breach.
- Notify affected individuals without unreasonable delay, no later than **60 calendar
  days** after discovery; notify the FTC within **10 business days** if 500+ people are
  affected (otherwise within 60 days of the end of the calendar year); notify media for
  500+ residents of a state.
- Electronic notice is permitted when the individual has chosen it.

**§5 patterns the FTC has enforced against (2023 onward):**
- Sharing health data with advertising platforms contrary to privacy promises.
- Using health data for retargeting after promising confidentiality.
- Representing a service as "HIPAA compliant" when it was not.
- Dark patterns in consent flows for health data.
Settlements have included bans on sharing health data for advertising and multi-year
compliance programs.

**Review checks:**
- [ ] Privacy policy claims match actual data flows (compare policy to the third-party inventory).
- [ ] No health data to ad-tech or attribution SDKs without a documented, affirmative, specific consent.
- [ ] "HIPAA compliant" marketing claims are substantiated or removed.
- [ ] A breach response plan covers the FTC timelines, not just HIPAA's.

---

## 2. 42 CFR Part 2 - Substance Use Disorder Records

**Who:** Federally assisted **Part 2 programs** and anyone receiving Part 2 records
from them (lawful holders). Applies in addition to HIPAA.

**What changed (2024 final rule, compliance date February 16, 2026):**
- A single patient consent can cover all future uses and disclosures for treatment,
  payment, and operations, aligned with HIPAA.
- Breach notification requirements aligned with HIPAA.
- Patients may request accounting of disclosures and restrictions.
- Redisclosure limits remain tighter than HIPAA; Part 2 records still cannot be used in
  legal proceedings against the patient without consent or a court order.
- Civil and criminal penalties aligned with HIPAA.

**Review checks:**
- [ ] Part 2 records are identifiable and segregable in the data model.
- [ ] Consent capture meets Part 2 content requirements.
- [ ] Redisclosure notice accompanies disclosures.
- [ ] Any mixing of Part 2 data with general records is intentional and documented.

---

## 3. State consumer health data laws

Apply by **resident**, regardless of HIPAA status, and generally exempt HIPAA-covered PHI
while covering everything else. Three with the broadest reach:

| Law | Key points |
|---|---|
| **Washington My Health My Data Act** (RCW 19.373, effective 2024) | Broad "consumer health data" definition including inferences; separate consumer health data privacy policy; **opt-in consent to collect and to share**, separate from each other; **signed authorization to sell**; geofencing ban around health facilities; **private right of action** via the state Consumer Protection Act. No revenue threshold for applicability. |
| **Nevada SB 370** (effective 2024) | Similar structure to Washington; no private right of action. |
| **Connecticut** (SB 3 amendments to CTDPA) | Consumer health data as a sensitive category; opt-in consent; geofencing ban. |

Other overlays:
- **California**: CMIA (Civil Code §56) covers providers and also businesses offering
  software to maintain medical information; CCPA/CPRA treats health data as sensitive
  personal information with a right to limit use; CCPA regulations on risk assessments
  and automated decision-making.
- **Texas**: Texas Medical Records Privacy Act (HB 300) applies to **any** person who
  handles PHI in Texas, with training and breach requirements beyond HIPAA; Texas Data
  Privacy and Security Act treats health data as sensitive.
- **New York**: SHIELD Act data security requirements; the Health Information Privacy
  Act was passed by the legislature in 2025 - verify whether signed and in force.
- **Illinois**: BIPA for biometrics (private right of action, statutory damages).
- **Comprehensive state privacy laws** (Virginia, Colorado, Utah, Oregon, Montana, Texas,
  and others) treat health data as sensitive, requiring opt-in consent and data
  protection assessments.

**Review checks:**
- [ ] State inventory in the project profile is complete.
- [ ] Consent flows separate collection from sharing where Washington-style laws apply.
- [ ] A consumer health data privacy policy exists where required.
- [ ] No geofencing within the statutory radius of health facilities.
- [ ] Data protection / risk assessments are documented where required.

---

## 4. ONC information blocking (45 CFR Part 171)

**Who:** Health care providers, health IT developers of certified health IT, health
information networks and exchanges. **What:** practices likely to interfere with
access, exchange, or use of EHI are prohibited unless one of the enumerated exceptions
(preventing harm, privacy, security, infeasibility, health IT performance, manner,
fees, licensing, TEFCA) applies and its conditions are documented.

Related: certified health IT must expose standardized FHIR APIs (USCDI, SMART on FHIR);
the HTI-1 rule adds transparency requirements for **decision support interventions**
built into certified health IT.

**Review checks:**
- [ ] Patient-facing API access uses standards and does not require unnecessary friction.
- [ ] Any blocking or delay of EHI maps to a named exception with documented conditions.
- [ ] Export and portability functions are complete and timely.

---

## 5. FDA - software, CDS, AI, and device cybersecurity

See Axis 1 Q4 for classification. Once something is a device:
- Premarket pathway (510(k), De Novo, PMA) and labeling.
- Quality Management System Regulation (21 CFR Part 820, effective February 2026).
- **Section 524B cybersecurity** for cyber devices: SBOM, vulnerability disclosure,
  postmarket patching plan; FDA's premarket cybersecurity guidance (2023, updated 2025).
- **AI-enabled devices**: Predetermined Change Control Plan guidance (final December
  2024) for models that update after clearance; AI lifecycle guidance (draft 2025).
- Adverse event reporting (21 CFR Part 803) and corrections/removals (Part 806).

**Review checks:**
- [ ] Device determination documented by regulatory counsel.
- [ ] If a device: SBOM generated and maintained; vulnerability handling process; change control for AI models.
- [ ] If relying on the CDS exclusion: all four criteria documented against the feature as built.

---

## 6. AI-specific rules that reach health software

- **ACA Section 1557 (45 CFR §92.210)**: covered health programs must make reasonable
  efforts to identify and mitigate discrimination risk from **patient care decision
  support tools**, including AI. In force since 2025. Requires knowing which tools use
  protected characteristics as inputs.
- **ONC HTI-1 decision support transparency** for certified health IT.
- **Colorado AI Act** (SB 24-205): developer and deployer duties for high-risk AI making
  consequential decisions including health care; effective date delayed to **June 30,
  2026** - verify current status and any amendments.
- **Utah AI Policy Act**: disclosure when generative AI is used in regulated occupations
  including health care.
- **State chatbot and mental-health AI laws**: several states (for example Illinois,
  Nevada, Utah) enacted limits on AI providing therapy or requiring disclosure that the
  user is talking to AI; verify per state.
- **FTC §5** applies to unsubstantiated AI accuracy claims.

Detail for engineering checks: `component-ai-llm.md`.

---

## 7. Other regimes that commonly appear

| Regime | Trigger | Check |
|---|---|---|
| **COPPA** (16 CFR Part 312, amended 2025) | Users under 13 | Verifiable parental consent; data minimization; retention limits |
| **TCPA** | SMS or automated calls | Prior express consent; health-care exemption is narrow |
| **CAN-SPAM** | Marketing email | Opt-out, identification |
| **PCI DSS 4.0** | Card payments | Scope minimization; usually offload to a processor |
| **GINA** | Genetic information | No use for employment or insurance decisions |
| **Section 508 / ADA** | Government or public accommodation | Accessibility; not privacy but a release gate for many customers |
| **EU GDPR / UK GDPR** | Any EU/UK users | Out of scope for this skill, but flag it |

---

## 8. Certifications customers ask for

Not laws, but frequently release gates in enterprise health sales:
- **SOC 2 Type II** (Trust Services Criteria) - the common baseline.
- **HITRUST** (e1, i1, r2) - frequently required by large health systems and payers.
- **HHS 405(d) HICP** - recognized security practices; demonstrated adoption can
  mitigate HIPAA penalties under the 2021 HITECH amendment.
- **NIST CSF 2.0 / NIST SP 800-66r2** - the HIPAA Security Rule crosswalk.

Record which the customer base requires and whether evidence exists; absence is a
Track item unless a contract makes it a Block.
