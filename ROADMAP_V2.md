# 🚀 2026 AI-First Cloud Security Architect Roadmap (V2)
*The Ephemeral Path to SAA-C03 and AWS AI Credentials*

## 🗺️ The Architecture Blocks (CABs)

| Block | Phase | Weeks | Focus | Goal |
| :--- | :--- | :--- | :--- | :--- |
| **CAB-01** | Foundations | 1-2 | **CDK & IAM Zero-Trust** | Rebuild Medical VPC with CDK. Implement Org-level SCPs. |
| **CAB-02** | Security | 3-4 | **Network Hardening** | ALBs, WAF, and VPC Endpoints for PHI isolation. |
| **CAB-03** | Data | 5-6 | **KMS & PHI Protection** | Automatic encryption of patient records at rest/transit. |
| **CAB-04** | AI | 7-8 | **Bedrock Compliance** | Use Bedrock to audit infrastructure logs for HIPAA compliance. |
| **CAB-05** | Resilience | 9-10 | **High Availability** | Global Accelerator and Multi-Region DR strategies. |
| **CAB-06** | DevOps | 11-12 | **CI/CD Architecture** | Automate the spin-up/tear-down labs via GitHub Actions. |
| **CAB-07** | Intelligence | 13-14 | **SageMaker Security** | Private link and EMR security for medical data science. |
| **CAB-08** | Final Blitz | 15-16 | **Certification & Portfolio** | SAA-C03 Blitz + AI Specialty preparation. |

## 🛡️ Core Rules
1. **Never leave resources running.** Use `cdk destroy` at the end of every study session.
2. **Every lesson is a BiP (Build in Public) post.** If you didn't document it, you didn't learn it.
3. **AI is the endgame.** Every block should ask: "How could Bedrock or SageMaker improve this security posture?"
