# Component - Backend / API / Database

Applies when the component stores, processes, or serves health data. Each item needs
**evidence** (file:line, config path, query output, screenshot) to be marked ✅.

Ratings in brackets are the default severity when the item fails and PHI is involved.
Downgrade one level for non-HIPAA consumer health data unless a state law makes the
control mandatory.

## Authentication and access control
- [ ] **Unique user identity for every actor** including service accounts; no shared logins. (§164.312(a)(2)(i)) [Block]
- [ ] **Role-based or attribute-based authorization enforced server-side** on every PHI endpoint; object-level checks (user A cannot fetch patient B by changing an ID). [Block]
- [ ] **MFA** for workforce and admin access to PHI; strongly recommended for patients. [Fix]
- [ ] **Session management**: server-side expiry, idle timeout appropriate to the setting, revocation on password change and logout. (§164.312(a)(2)(iii)) [Fix]
- [ ] **Emergency access procedure** documented for clinical products. (§164.312(a)(2)(ii)) [Fix]
- [ ] **Break-glass access** logged and alerted. [Fix]
- [ ] Password storage with a modern adaptive hash; rate limiting and lockout on auth endpoints. [Fix]

## Audit logging (§164.312(b))
- [ ] Every **read, create, update, delete, export, and print** of PHI logs: actor, subject (patient/record), action, timestamp, source (IP / device / service). [Block]
- [ ] Logs are **immutable** or append-only, access-restricted, and retained **6 years**. [Fix]
- [ ] Logs **never contain PHI values** (names, DOB, MRN, free text). Log identifiers, not content. [Fix]
- [ ] Log review process exists: alerts on bulk export, off-hours access, access to VIP or own-record flags. (§164.308(a)(1)(ii)(D)) [Fix]
- [ ] Audit log can produce an **accounting of disclosures** for a given patient. (§164.528) [Track]

## Encryption and key management
- [ ] **Encryption at rest** for every datastore holding PHI: primary DB, replicas, backups, snapshots, search indexes, caches, queues, object storage, analytics warehouses. [Block]
- [ ] **TLS 1.2+** on every hop including service-to-service inside the VPC; no plaintext internal HTTP carrying PHI. [Block]
- [ ] Keys in a managed KMS; rotation; separation of key admin from data admin. [Fix]
- [ ] Field-level encryption or tokenization for the most sensitive fields where feasible (SSN, Part 2 flags). [Track]

## Data handling
- [ ] **No PHI in URLs, query strings, or path parameters** (they land in access logs, proxies, browser history, referrers). [Fix]
- [ ] **No PHI in error responses, stack traces, or exception-tracking payloads.** [Fix]
- [ ] **Minimum necessary** in API responses: endpoints return the fields the caller needs, not whole records. (§164.502(b)) [Fix]
- [ ] Bulk export endpoints are authorized, rate-limited, logged, and justified. [Fix]
- [ ] **Data retention and deletion** implemented per policy, including backups and derived data; patient deletion requests honored where applicable (state law) while medical-record retention rules are respected. [Track]
- [ ] Search indexes and caches holding PHI inherit access control and encryption. [Fix]
- [ ] Specially protected data (Part 2, psychotherapy notes) is **tagged** so disclosure logic can treat it differently. [Fix if present]

## Patient rights support (CE/BA products)
- [ ] Right of access: export of a designated record set in a readable electronic format within 30 days. (§164.524) [Fix]
- [ ] Amendment workflow or at least a documented manual process. (§164.526) [Track]
- [ ] Restriction flags honored by disclosure logic (for example self-pay restriction). (§164.522) [Track]

## Integrity and availability
- [ ] Integrity controls on stored PHI (checksums, versioning, signed records where clinical). (§164.312(c)) [Track]
- [ ] Tested backups with encryption and access control; restore tested within the last year. (§164.308(a)(7)) [Fix]
- [ ] Input validation and injection protection on every PHI path. [Block if an injection is demonstrable]

## Multi-tenancy (B2B products)
- [ ] Tenant isolation enforced at the data layer (row-level security, per-tenant keys, or separate schemas) and tested with cross-tenant access attempts. [Block]
- [ ] Tenant admins cannot escalate to platform admin. [Fix]

## Evidence to request
- Schema or data dictionary with PHI columns marked.
- Authorization middleware and at least two endpoint implementations.
- Logging configuration and a sample redacted log line.
- Datastore encryption settings and backup configuration.
- Results of the most recent penetration test or DAST run.
