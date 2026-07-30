# 🏥 AWS Journey 2026: VitalStream Medical Infrastructure
*From Paramedic to Cloud Security Architect*

Welcome to my 24-week simplified roadmap to the **AWS Solutions Architect Associate (SAA-C03)**. This repository documents my journey building secure, HIPAA-compliant cloud infrastructure pattern by pattern.

## 🗂️ Courseware & Weekly Labs

Canonical source: [`roadmap-v3.2.md`](./roadmap-v3.2.md). Each CAB maps to one SAA-C03 exam domain.

| Week | Block | Phase | Focus | Exam Domain | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **01-03** | **CAB-01** | Foundations | **VPC Plumbing & CLI** — 3-tier VPC via Bash (No Console). | Domain 1 | ✅ Complete |
| **04-06** | **CAB-02** | Security | **IAM & Zero-Trust** — Least privilege, EPT & Ulta Agents. | Domain 1 | 🔲 Up next |
| **07-09** | **CAB-03** | Data | **KMS & PHI Protection** — HIPAA/NIST Auditing. | Domain 1 | ✅ Complete |
| **10-12** | **CAB-04** | AI | **Bedrock & Guardrails** — Zero-exfiltration AI assistant. | Domain 1 | ✅ Complete |
| **13-15** | **CAB-05** | Resilience | **High Availability** — Zero-Downtime Architecture. | Domain 2 | ✅ Complete |
| **16-18** | **CAB-06** | Cost | **S3 Lifecycle & Cost Optimization** | Domain 4 | 🔲 Not started |
| **19-21** | **CAB-07** | Performance | **Serverless Decoupling** — Lambda, SQS, EventBridge. | Domain 3 | 🔲 Not started |
| **22-24** | **CAB-08** | Final Blitz | **Cert & Portfolio** — SAA-C03 exam prep & launch. | All | 🔲 Not started |

CI/CD automation, Kinesis/Glue data ingestion, and SageMaker isolation moved to an optional **Phase 6: Portfolio Extensions** (post-cert) — see `roadmap-v3.2.md`.

## 🗺️ Master Plan
See the interactive roadmap below (click nodes to navigate):
- [Mermaid Roadmap Diagram](./MINDMAP.md)
- [Master Plan & Progress Tracker](./TODO.md)
- [Full Roadmap Detail](./roadmap-v3.2.md)


As part of my 24-week roadmap to the **AWS Solutions Architect Associate (SAA-C03)**, I have architected and deployed a professional-grade Virtual Private Cloud (VPC). This infrastructure is designed for **VitalStream Medical**, a hypothetical medical equipment distributor requiring strict HIPAA-compliant data isolation.

## 🏗️ Architecture Design
The network is segmented into three distinct tiers across multiple Availability Zones to ensure high availability and security:
1. **Public Edge Tier:** For load balancers and entry points.
2. **Private App Tier:** For internal inventory management logic.
3. **Isolated PHI Tier:** A strictly isolated environment for Protected Health Information (PHI), with no direct internet access.


## 🛠️ Skills & Technologies Demonstrated
* **Shell Scripting:** Transitioned manual processes into a repeatable `bash` automation script using the `aws-cli`.
* **Infrastructure Auditing:** Developed a verification script to audit CIDR blocks and verify resource tags.
* **Network Security:** Applied **Least Privilege** principles to subnet routing and gateway configurations.
* **Compliance Mindset:** Integrated security checks for **VPC Flow Logs** to support future HIPAA auditing.

## 🚀 How to Run
1. **Provision Infrastructure:** Refer to archived scripts in `archive/Week_01_Medical_VPC`.
2. **Deploy Capstone:** Run `bash archive/Week_06_Capstone_Web_Platform/deploy_portal.sh` to launch the inventory portal.
3. **Verify:** Use the auditing logic in `assets/cab/`.

---
**About Me:** I am a former Paramedic with 20 years of emergency response experience, currently transitioning into Cloud Security Engineering. I hold a **Google Cybersecurity Certificate** and am actively documenting my journey to the **AWS SAA-C03**.

Connect with me on X: @[2sm0gSS]