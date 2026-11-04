# Component - AI / LLM / ML Features

Applies to any feature that sends health data to a model, trains or fine-tunes on
health data, generates clinical or patient-facing content, or makes or supports
decisions about individuals. This is the area where a HIPAA-only review is weakest.

## Classify the feature first
| Type | Examples | Extra regimes |
|---|---|---|
| **Administrative** | Note summarization for staff, coding suggestions, scheduling | HIPAA (if CE/BA), vendor contracts |
| **Patient-facing conversational** | Symptom intake bot, medication Q&A, mental-health companion | State AI-chatbot and mental-health AI laws, FTC §5, possibly FDA |
| **Clinical decision support** | Risk scores, differential suggestions, alerts | FDA CDS criteria, Section 1557 bias duty, ONC HTI-1 if in certified health IT |
| **Diagnostic / triage** | Image reads, triage levels, condition prediction | Very likely FDA device; Section 1557 |
| **Population / analytics** | Model training, research, cohort discovery | De-identification or authorization; IRB where research |

Record the type in the project profile. "Possibly a device" and "possibly research" are
**Needs human sign-off**.

## Data flow to the model provider
- [ ] **Contract**: if PHI reaches a hosted model API, a **BAA** with the provider is executed and the specific API/tier is covered by it (many providers cover only certain endpoints or enterprise tiers). [Block if PHI sent without BAA where HIPAA applies]
- [ ] **Zero data retention or defined retention** confirmed in writing; **no training on inputs or outputs**; abuse-monitoring retention understood and acceptable under the risk analysis. [Fix]
- [ ] Non-HIPAA products: privacy policy discloses that health data is processed by a named category of AI provider; state consumer health data consent covers this sharing. [Fix]
- [ ] **Minimum necessary** applied to prompts: strip identifiers not needed for the task (name, DOB, MRN, address) before the call; pass a session-scoped pseudonym where the model does not need identity. [Fix]
- [ ] **Retrieval (RAG) sources** are access-controlled per user: a query from user A can never retrieve patient B's documents. Test with cross-patient queries. [Block]
- [ ] Vector stores and embeddings holding PHI are treated as PHI datastores (encryption, access control, logging, retention). Embeddings of clinical text are not de-identified. [Fix]
- [ ] Prompt, completion, and tool-call **logs** are a PHI datastore: encrypted, access-controlled, retention-limited, not shipped to observability SaaS without a BAA. [Block if sent to non-BAA SaaS]
- [ ] Self-hosted models: the same infrastructure checklist applies; GPU hosts and model caches hold PHI. [Fix]

## Agentic and tool-using features
- [ ] Tools the model can call are **allow-listed** and each tool enforces authorization independently of what the model asks for. [Block if the model can reach data the user cannot]
- [ ] Prompt injection from patient-supplied or document content cannot cause exfiltration (for example a document instructing the model to email records). Tested. [Fix]
- [ ] Any action with external effect (send message, order, schedule, modify record) requires explicit user confirmation or is logged with the triggering input. [Fix]
- [ ] Every model-initiated PHI access appears in the audit log attributed to the end user and the feature. [Fix]

## Output safety and clinical use
- [ ] Clinical outputs are **labeled** as AI-generated, with the basis visible to the clinician (CDS exclusion requires independent review). [Fix]
- [ ] Patient-facing bots disclose they are AI at the start of the interaction and on request (several state laws); escalation path to a human for crisis or emergency signals. [Fix; Block for mental-health contexts without crisis handling]
- [ ] Medication, dosing, and diagnostic outputs are either excluded from scope or validated against a documented process. [Needs human sign-off]
- [ ] Hallucination and accuracy evaluation exists for the deployed use with a documented threshold; marketing claims match it (FTC §5). [Fix]
- [ ] Human review required before AI-generated content enters the legal medical record, or the entry is marked as AI-drafted with the approving user. [Fix]

## Bias and nondiscrimination
- [ ] Inventory of model inputs; any use of race, ethnicity, sex, age, disability, language, or proxies is identified. (Section 1557 patient care decision support duty) [Fix for covered entities]
- [ ] Performance evaluated across relevant subgroups where feasible; mitigation or documented rationale. [Fix for covered entities; Track otherwise]
- [ ] Colorado AI Act readiness where applicable: impact assessment, notices, and developer documentation. [Track; verify effective date]

## Training, fine-tuning, and evaluation data
- [ ] Training on PHI requires authorization, a research exception with IRB/privacy board, or de-identification (Safe Harbor or Expert Determination) documented **before** training. [Block if PHI used for training without a lawful basis]
- [ ] Evaluation datasets and prompt test sets do not contain real PHI, or are governed as PHI. [Fix]
- [ ] Model artifacts trained on PHI are treated as potentially containing PHI (access control, no public release). [Fix]
- [ ] Non-HIPAA products: state laws may require consent before using consumer health data for training; privacy policy says so. [Fix]

## Vendor and model lifecycle
- [ ] Model and provider versions pinned and recorded per release; a change in model is a change-control event for clinical features (and FDA PCCP territory for devices). [Track; Fix for CDS/devices]
- [ ] Provider's subprocessors reviewed; data residency confirmed for the covered tier. [Track]
- [ ] Kill switch: the feature can be disabled without a deploy. [Track]

## Evidence to request
- Provider contract and the retention/training terms for the exact endpoint in use.
- Prompt construction code showing identifier stripping.
- RAG authorization test results.
- Logging configuration for prompts/completions and where it ships.
- Evaluation report and subgroup analysis where applicable.
- Regulatory determination memo for CDS/device status.
