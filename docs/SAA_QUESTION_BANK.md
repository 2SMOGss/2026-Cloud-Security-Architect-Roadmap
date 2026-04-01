# 📚 SAA-C03 Question Bank: 2026 Architect Roadmap
*Refining conceptual understanding from hands-on labs (VitalStream Medical).*

## 🏷️ Domain 1: Design Secure Architectures (HIPAA Focused)

| Week | Concept | Question | Answer |
| :--- | :--- | :--- | :--- |
| **01** | VPC Isolation | How do you isolate PHI data in a 3-tier VPC? | Use a separate subnet tier (Isolated PHI Tier) with NO direct internet access and NACLs restricting inbound/outbound traffic to the App Tier. |
| cab04-1 | Design VitalStream AI Sentinel | completed | Bedrock + Guardrails + PrivateLink |
| cab04-2 | Provision Bedrock Interface VPC Endpoint | completed | SAA-C03: Bypasses Public Internet |
| cab04-3 | Provision Bedrock Guardrails (PII Masking) | completed | HIPAA Compliance Logic |
| cab04-4 | Configure IAM Zero-Exfiltration Policies | completed | Perimeter Gatekeeping |
| cab04-5 | Develop Sentinel Assistant Script (Boto3) | completed | Python integration with Guardrails |
| cab04-6 | SAA-C03 SITREP & WOW Document | completed | Audit Readiness |
| **03-04** | NACLs vs SGs | Which one is "stateless" and operates at the Subnet level? | Network ACLs (NACLs) are stateless and subnet-level. Security Groups (SGs) are stateful and instance-level. |
| **05** | VPC Flow Logs | Where should Flow Logs be published for HIPAA auditing? | To an encrypted S3 bucket or CloudWatch Logs with restricted IAM access for compliance teams. |
| **05** | Incident Response | A high-priority "Port 22" alert is triggered. What is the first response? | Use an automated script (or agent) to temporarily modify the Security Group of the affected instance to block port 22. |
| **06** | IAM Policies | What is the difference between an Identity-based and a Resource-based policy? | Identity-based policies are attached to users/groups/roles. Resource-based policies are attached directly to the resource (e.g., S3 Bucket Policy). |
| **06** | IAM Zero-Trust | In a Zero-Trust Medical VPC, can we trust internal traffic? | No. Every request must be verified regardless of origin, meaning internal ALB to App Tier traffic must also be encrypted. |
| **CAB-01** | CDK Automation | Why use CDK over manual console for HIPAA systems? | Ensures "Architectural Repeatability," allows version control (git), and enables automated security auditing (EPT Agent). |
| **CAB-01** | VPC Peering | Is VPC Peering transitive? | No. If VPC A is peered with VPC B, and B with C, A is not peered with C by default. |
| **CAB-03** | S3 Object Lock | How to ensure audit logs are immutable even for the root user for 5+ years? | Use **S3 Object Lock - Compliance Mode** with a default retention period. |
| **CAB-03** | KMS Keys | Why use Customer Managed Keys (CMKs) over AWS Managed Keys for HIPAA? | To enable "Separation of Duties" and have granular control over rotation and Key Policies. |
| **CAB-03** | VPC Flow Logs | Where should Flow Logs be sent if a Customer Managed Key (CMK) is required for auditing? | To an **S3 bucket** encrypted with a CMK (KMS Key). |
| **CAB-04** | PrivateLink | Why use an Interface Endpoint for Bedrock? | To keep AI invocation traffic within the private network, bypassing the public internet for HIPAA compliance. |
| **CAB-04** | Guardrails | How do Bedrock Guardrails protect data at-rest and in-transit? | By redacting PII/PHI on both input prompts and output responses automatically. |
| **CAB-04** | Zero-Trust | Can an Admin use a VPC Endpoint if the Endpoint Policy omits their role? | No. Endpoint Policies act as a perimeter gate; if a principal is not explicitly allowed (or is denied), access is blocked regardless of IAM permissions. |

---
## 🏁 Status Check:
- **Questions Stored:** 16
- **Priority Domain:** Domain 1 (Secure Architectures)
