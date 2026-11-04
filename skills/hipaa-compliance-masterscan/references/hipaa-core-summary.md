# HIPAA Core Summary

A compressed reference so this skill works without a separate HIPAA skill. For full
treatment load a dedicated HIPAA reference. Citations are to 45 CFR.

## Who must comply
- **Covered Entities**: health plans, health care clearinghouses, providers that
  transmit health information electronically for standard transactions (§160.103).
- **Business Associates**: anyone who creates, receives, maintains, or transmits PHI on
  behalf of a CE, and their subcontractors. Directly liable under the Security Rule and
  parts of the Privacy Rule since the 2013 Omnibus Rule.

## What is PHI
Individually identifiable health information held or transmitted by a CE or BA in any
form. The 18 Safe Harbor identifiers (§164.514(b)): names; geographic subdivisions
smaller than a state; all date elements except year (and ages over 89); phone; fax;
email; SSN; medical record number; health plan beneficiary number; account number;
certificate/license number; vehicle identifiers; device identifiers; URLs; IP
addresses; biometric identifiers; full-face photos; any other unique identifier.

De-identification: Safe Harbor (remove all 18 and have no actual knowledge of
re-identifiability) or Expert Determination.

## Privacy Rule (Subpart E) essentials
- Uses and disclosures permitted without authorization: treatment, payment, health care
  operations (§164.506); the §164.512 public-interest categories; to the individual.
- **Minimum necessary** (§164.502(b)) for everything except treatment disclosures,
  disclosures to the individual, and authorized disclosures.
- **Authorization** (§164.508) required for marketing, sale of PHI, psychotherapy notes,
  and most other uses. Must be specific and revocable.
- **Patient rights**: access within 30 days (§164.524) - the most enforced provision;
  amendment (§164.526); accounting of disclosures (§164.528); restrictions (§164.522(a));
  confidential communications (§164.522(b)); Notice of Privacy Practices (§164.520).
- **Business Associate Agreement** content requirements (§164.504(e)).

## Security Rule (Subpart C) essentials
Applies to **ePHI**. Three safeguard families, each with Required and Addressable
specifications. Addressable means implement it, or document why not and what you did
instead. It never means optional.

- **Administrative (§164.308)**: risk analysis and risk management (the most cited
  failure in enforcement), sanction policy, information system activity review, security
  official, workforce security, access management, training, incident procedures,
  contingency plan (backup, disaster recovery, emergency mode), evaluation, BA contracts.
- **Physical (§164.310)**: facility access, workstation use and security, device and
  media controls (disposal, re-use, accountability, backup).
- **Technical (§164.312)**: access control (unique user ID - R; emergency access - R;
  automatic logoff - A; encryption/decryption - A); audit controls - R; integrity - A;
  person or entity authentication - R; transmission security (integrity controls - A;
  encryption - A).
- **Documentation (§164.316)**: written policies, retained 6 years from creation or last
  effective date, reviewed and updated.

**Proposed Security Rule overhaul (NPRM, January 2025)** would make MFA, encryption,
asset inventories, network segmentation, and annual testing mandatory and remove the
addressable category. As of mid-2026 it is not final. Build to current rule, design
toward the proposal, and never cite it as a requirement.

## Breach Notification Rule (Subpart D) essentials
- A breach is an impermissible acquisition, access, use, or disclosure of unsecured PHI,
  presumed reportable unless a four-factor risk assessment (§164.402) shows a low
  probability of compromise.
- **Encryption safe harbor**: PHI encrypted per HHS guidance (NIST-consistent) is not
  "unsecured"; loss of an encrypted device with the key not compromised is not a breach.
- Individuals: without unreasonable delay, no later than **60 calendar days** from
  discovery (§164.404). HHS: within 60 days of discovery for 500+ affected; annual log
  for smaller breaches (§164.408). Media: 500+ residents of a state (§164.406).
- BA to CE: without unreasonable delay, no later than 60 days; the BAA often shortens
  this (§164.410).
- Discovery = known or should reasonably have been known.

## Enforcement patterns worth designing against
- Missing or inadequate **risk analysis** is the leading finding in settlements.
- **Right of access** delays are a standing enforcement initiative.
- **Ransomware** settlements emphasize risk analysis, access controls, and audit logs.
- OCR's guidance on **online tracking technologies** (2022, updated 2024) treats
  identifiers sent to ad-tech from authenticated pages as PHI disclosures; a federal
  court in 2024 vacated the part extending this to IP addresses on unauthenticated
  pages. Verify current status, and treat authenticated-page tracking as a Block.
