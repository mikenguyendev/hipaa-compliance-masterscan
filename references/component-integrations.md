# Component - Integrations

Applies to every connection that moves health data across an organizational boundary:
EHR and FHIR APIs, HL7 v2 feeds, labs, pharmacies, imaging, HIEs, payers, messaging
(SMS, email, push, fax), payments, e-signature, and data partners.

## For every integration, record
| Field | Why |
|---|---|
| Counterparty and their role (CE, BA, neither) | Decides contract type |
| Direction and data categories | Minimum necessary; specially protected data |
| Legal basis (treatment, payment, operations, authorization, public health, DUA) | Required for disclosures |
| Contract on file (BAA, DUA, data-sharing agreement, vendor terms) | Missing contract is a finding |
| Transport and auth mechanism | Security Rule transmission security |
| Logging on both ends | Accounting of disclosures |

## FHIR / SMART on FHIR / EHR APIs
- [ ] **SMART on FHIR** with OAuth 2.0 and OpenID Connect; scopes limited to the resources needed; no wildcard `*.read` where narrower scopes work. [Fix]
- [ ] Patient-facing apps: token lifetimes short, refresh tokens bound, PKCE used, consent screen accurate about data accessed. [Fix]
- [ ] Backend services: client credentials with asymmetric keys (SMART Backend Services), key rotation, scoped to the integration's purpose. [Fix]
- [ ] Bulk Data (`$export`) jobs authorized, logged, and output stored as PHI with retention. [Fix]
- [ ] Information blocking: the integration does not impose fees, delays, or restrictions outside a documented Part 171 exception. [Fix if the organization is an actor under Part 171]
- [ ] Data mapping does not silently drop or mislabel specially protected categories (Part 2 segments, confidentiality codes). [Fix if present]

## HL7 v2 / file-based / SFTP feeds
- [ ] Transport encrypted (TLS, VPN, or SFTP); no plaintext MLLP across untrusted networks. [Block]
- [ ] Files at rest on both sides encrypted and purged after processing; SFTP landing zones not world-readable. [Fix]
- [ ] Message validation prevents malformed data from creating wrong-patient records. [Fix]
- [ ] Interface engine logs retained and PHI-free in alerting channels. [Fix]

## Messaging to patients
- [ ] **SMS**: TCPA prior express consent recorded; health-care exemption understood as narrow; content minimized (no diagnosis, medication, or test result in the message body unless the patient opted in to that explicitly); STOP handling works; provider under BAA where content is PHI. [Fix; Block if PHI sent via a non-BAA provider where HIPAA applies]
- [ ] **Email**: TLS enforced; PHI in email body only with documented patient preference or via a secure-message link; provider under BAA; CAN-SPAM for anything marketing. [Fix]
- [ ] **Push**: see mobile checklist; payloads free of PHI. [Fix]
- [ ] **Fax**: still PHI; misdirected-fax procedure exists; e-fax vendor under BAA. [Fix]
- [ ] **Marketing communications** involving PHI require authorization unless within the treatment or operations exceptions; no use of health data for third-party ad targeting. (§164.508(a)(3)) [Block if PHI used for targeting without authorization]

## Payments
- [ ] Card data handled by a PCI DSS-validated processor; the application never stores PAN. [Fix]
- [ ] Payment descriptors and receipts do not reveal condition or service type beyond what is necessary. [Track]
- [ ] Processor's access to health context minimized (line items generic where possible). [Track]

## E-signature, document, and support vendors
- [ ] Consent forms, intake PDFs, and signed authorizations stored under BAA or on controlled infrastructure. [Fix]
- [ ] Support ticketing and CRM: PHI landing there is either prevented (templates, redaction) or the vendor is under BAA. [Fix]

## Data partners, research, and analytics vendors
- [ ] Disclosures for research have IRB/privacy-board approval, authorization, or use a **limited data set under a DUA** or de-identified data with the method documented. [Block if identifiable PHI disclosed for research with none of these]
- [ ] "Sale of PHI" analysis done for any data-for-value arrangement; authorization required if it is a sale. (§164.502(a)(5)(ii)) [Block]
- [ ] Non-HIPAA products: sale of consumer health data requires signed authorization under Washington-style laws; opt-out or opt-in under others. [Fix]

## Operational
- [ ] Every integration has an owner, a monitoring alert for failure, and a documented off-boarding step that revokes credentials and purges data. [Track]
- [ ] Counterparty breach notification clauses align with the organization's own timelines. [Track]
- [ ] Accounting-of-disclosures capability covers disclosures made through integrations. [Track]

## Evidence to request
- Integration inventory with the fields above.
- OAuth client configuration and scope list for each EHR connection.
- Sample (redacted) outbound SMS/email templates.
- Contracts for each counterparty.
- Interface engine or API gateway log sample showing attribution.
