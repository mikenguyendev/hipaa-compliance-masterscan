# Component - Infrastructure / DevOps / Cloud

Applies to hosting, networking, CI/CD, secrets, backups, and operations for any
component touching health data.

## Contracts and service scope
- [ ] **BAA executed** with each cloud provider and each SaaS that can touch PHI (hosting, logging, monitoring, error tracking, email, SMS, support, backups, data warehouse, LLM API). [Block for missing BAA where PHI flows and HIPAA applies]
- [ ] Only **HIPAA-eligible services** of the provider are used for PHI workloads; the eligible-services list is checked when new services are introduced. [Fix]
- [ ] Vendor inventory kept with data categories, contract type, and review date. (§164.308(b)) [Fix]

## Identity and access
- [ ] Cloud console and infrastructure access behind SSO with **MFA enforced**; no long-lived root or owner keys in use. [Block for root keys active without MFA]
- [ ] Least-privilege IAM; human and machine identities separated; access reviewed at least quarterly and on offboarding. (§164.308(a)(3), (a)(4)) [Fix]
- [ ] Production database access is brokered (bastion, just-in-time, or query proxy) and **logged with identity**. [Fix]
- [ ] Offshore or contractor access to production documented, contracted, and scoped. [Fix]

## Network
- [ ] PHI datastores have **no public endpoints**; private subnets, security groups deny-by-default. [Block if a PHI datastore is internet-reachable]
- [ ] Segmentation between production, non-production, and corporate networks. [Fix]
- [ ] WAF or equivalent in front of public PHI-handling applications; DDoS protections. [Track]
- [ ] Egress controls or at least egress logging so data exfiltration is detectable. [Track]

## Encryption and keys
- [ ] Encryption at rest enabled on **every** storage layer (volumes, managed DBs, object storage, snapshots, backups, log archives, message queues, caches). [Block]
- [ ] KMS with customer-managed keys for the most sensitive stores; key rotation; key access logged. [Fix]
- [ ] TLS termination and re-encryption documented; no plaintext hop between load balancer and service when PHI is in transit. [Fix]

## Logging, monitoring, detection
- [ ] Cloud audit logging enabled (control-plane actions, data-plane access where available), shipped to immutable storage, retained 6 years for HIPAA-relevant logs. (§164.312(b), §164.316(b)) [Fix]
- [ ] Alerting on: IAM changes, security-group changes, public-bucket events, mass data access, failed-login bursts, new regions or services. [Fix]
- [ ] Log pipeline **strips PHI** before it reaches third-party logging/monitoring SaaS without a BAA. [Block if PHI reaches a non-BAA log SaaS]
- [ ] Vulnerability scanning of hosts and containers; patch SLA defined. [Fix]

## Backup, DR, and contingency (§164.308(a)(7))
- [ ] Encrypted, access-controlled backups; retention documented; **restore tested** within the last 12 months with the result recorded. [Fix]
- [ ] Disaster recovery plan with RTO/RPO; emergency-mode operations plan for clinical products. [Fix]
- [ ] Backups are isolated from the primary account/blast radius (ransomware resilience). [Track]

## CI/CD and environments
- [ ] **No real PHI in development, test, staging, CI, or developer laptops.** Synthetic or de-identified data only; de-identification method documented. [Block if production PHI is copied to non-production]
- [ ] Secrets in a secrets manager; **no credentials in source, images, or CI logs**; secret scanning in the pipeline. [Block if live credentials in source]
- [ ] SAST, dependency scanning, and container scanning in the pipeline; results triaged. [Fix]
- [ ] Infrastructure as code reviewed; drift detection or periodic config audit against the security baseline. [Track]
- [ ] Deployment access limited; changes traceable to a person and a review. [Fix]
- [ ] SBOM generated for releases (required for FDA cyber devices; good practice otherwise). [Track, Fix if device]

## Operations and governance
- [ ] **Risk analysis** covering this infrastructure is documented and current (within a year or since the last major change). (§164.308(a)(1)(ii)(A)) [Block if none exists for a CE/BA]
- [ ] Incident response plan with HIPAA, FTC, and state breach timelines; tabletop exercised. (§164.308(a)(6)) [Fix]
- [ ] Media and device disposal procedures (cloud: volume and snapshot deletion verified; hardware: certificates of destruction). (§164.310(d)) [Track]
- [ ] Workforce security training recorded; sanction policy exists. (§164.308(a)(5), (a)(1)(ii)(C)) [Fix]

## Evidence to request
- List of executed BAAs with dates.
- IAM policy export or screenshots; MFA enforcement setting.
- Network diagram and security-group / firewall rules for PHI tiers.
- Storage encryption settings per datastore.
- Last backup-restore test record.
- Risk analysis document and date.
- Pipeline configuration showing scanning steps.
