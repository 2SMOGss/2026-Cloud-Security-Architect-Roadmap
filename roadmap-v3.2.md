# 🚀 2026 AI-First Cloud Security Architect Roadmap (V3.2)
*The Ephemeral Path to SAA-C03, HIPAA Compliance, and Agentic Orchestration*

**This file is the single source of truth for the roadmap.** `README.md` and `MINDMAP.md` mirror this table — if they ever drift, this one wins.

## 🗺️ The Architecture Blocks (CABs)

Each CAB is scoped to one SAA-C03 exam domain so the roadmap tracks exam coverage directly, not just topic interest.

| Block | Phase | Weeks | Focus | Exam Domain | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CAB-01** | Foundations | 1-3 | **VPC Plumbing & CLI** — Build VitalStream 3-tier VPC by hand (no console). | Domain 1: Secure Architectures | ✅ Complete |
| **CAB-02** | Security | 4-6 | **IAM & Zero-Trust** — Permission boundary, ABAC-gated role, Zero-Trust bucket policy, IAM Access Analyzer. | Domain 1: Secure Architectures | 🟡 Built, pending live AWS verification |
| **CAB-03** | Data | 7-9 | **KMS & PHI Protection** — Encryption at rest, HIPAA/NIST auditing, immutable audit logs. | Domain 1: Secure Architectures | ✅ Complete |
| **CAB-04** | AI | 10-12 | **Bedrock & Guardrails** — Zero-exfiltration AI assistant via PrivateLink + PII/PHI redaction. | Domain 1: Secure Architectures | ✅ Complete |
| **CAB-05** | Resilience | 13-15 | **High Availability** — Multi-AZ RDS, ASG self-healing, Zero-Downtime chaos audit. | Domain 2: Resilient Architectures | ✅ Complete |
| **CAB-06** | Cost | 16-18 | **S3 Lifecycle & Cost Optimization** — Storage classes, lifecycle policies, Intelligent-Tiering, AWS Budgets. | Domain 4: Cost-Optimized Architectures | 🟡 Built, pending live AWS verification |
| **CAB-07** | Performance | 19-21 | **Serverless Decoupling** — SQS+DLQ, Lambda reserved concurrency, EventBridge pub/sub, CloudFront+OAC caching. | Domain 3: High-Performing Architectures | 🟡 Built, pending live AWS verification |
| **CAB-08** | Final Blitz | 22-24 | **Cert & Portfolio** — Full question-bank review, timed practice exam, portfolio launch. | All domains | 🔲 Not started |

## 🎁 Phase 6: Portfolio Extensions (Optional, Post-Cert)

These are differentiators, not SAA-C03 exam content — pick them up **after** CAB-08 and the exam, not instead of the domain gaps above:

* **CI/CD Automation** — GitHub Actions pipeline to deploy/destroy CDK stacks automatically (ties into the "ephemeral lab" rule below).
* **Data Ingestion** — Kinesis telemetry ingestion + AWS Glue ETL.
* **SageMaker/ML Isolation** — PrivateLink and EMR network isolation for a data-science workload.

## 🛡️ Core Operational Rules

1. **Agent-Led Auditing:** Every infrastructure change must be reviewed by the **Ulta Agent** (Architecture) and challenged by the **EPT Agent** (Security).
2. **The "Serverless-First" Filter:** Before deploying EC2, evaluate if **Lambda** or **Fargate** can achieve the goal to reduce the attack surface.
3. **Cost-Aware Engineering:** Never run a Bedrock or SageMaker script without the **Token Watchdog** active. Monthly budget alerts must be set via CLI.
4. **The "Publicist" Protocol:** Every "Critical" bug found and fixed must trigger the **Portfolio Publicist** to create a GitHub `README.md` or LinkedIn draft.
5. **Drive Sync:** End every session by updating the **"Roadmap" Google Doc** to ensure persistent tracking across all AI Gems.

## 🛠️ Technical Stack (V3.2)

* **Cloud:** AWS (VPC, IAM, S3, RDS, Lambda, SQS, Kinesis, Bedrock, KMS).
* **Languages:** Bash (Primary for Infra), Python (Automation/AI), TypeScript (VoltAgent Framework).
* **Tools:** Everything Claude Code (ECC), Gemini Gems, **micro** (Terminal Editor), WSL.
* **Compliance:** HIPAA, NIST-800-53, Well-Architected Framework.

## 🏁 Phase 5: Market Launch (The "Paramedic-to-Cloud" Transition)

* **The Narrative:** Frame 20 years of emergency medical experience as "Critical Infrastructure Management."
* **The Proof:** A public GitHub repository featuring the **VitalStream** architecture, featuring "Security Audit" reports and "Cost Optimization" whitepapers.
* **The Badge:** AWS Certified Solutions Architect – Associate (SAA-C03).
