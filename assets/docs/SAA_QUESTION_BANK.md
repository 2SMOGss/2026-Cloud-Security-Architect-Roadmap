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
| **CAB-05** | RDS Resilience | What is the standard for synchronous failover in RDS? | **Multi-AZ Deployment**. (Read Replicas are for performance, Multi-AZ is for resilience). |
| **CAB-05** | Launch Templates | Why migrate from Launch Configurations to Launch Templates? | Launch Configurations are being phased out (legacy); Templates support versioning, T2/T3 instances, and modern features like IMDSv2. |
| **CAB-05** | Cyclic Dependency | How do you break a Security Group cycle between RDS and ASG? | Use **Subnet CIDR blocks** in the RDS ingress rules instead of referencing the ASG Security Group ID directly. |
| **CAB-05** | Self-Healing | What happens if an instance fails an ALB health check in an ASG? | The ASG **terminates** the unhealthy instance and **provisions** a new one in a healthy AZ to maintain desired capacity. |
| **CAB-05** | Secrets Manager | How to securely retrieve RDS credentials without hardcoding? | Use **AWS Secrets Manager** with an IAM Role (Instance Profile) that has `GetSecretValue` permissions. |
| **CAB-05** | Read Performance | A Multi-AZ RDS is hitting 90% CPU on reads. Best fix? | Deploy **RDS Read Replicas** and offload the read traffic from the primary instance. |
| **CAB-05** | Billing Alarms | Where are AWS Billing metrics stored? | Only in the **us-east-1** (N. Virginia) region. Alarms must be created there. |
| **CAB-05** | Instance Refresh | Benefit of ASG Instance Refresh over manual termination? | Performs a **controlled rolling update**, maintaining `MinHealthyPercentage` while deploying new Launch Template versions. |
| **CAB-05** | Private Updates | How do instances in isolated subnets download OS patches securely? | Via a **NAT Gateway** in a Public Subnet (or VPC Endpoints for specific AWS services). |
| **CAB-05** | 502 Bad Gateway | #1 cause of ALB returning 502 with healthy EC2 instances? | **Security Group mismatch**: The EC2 SG does not allow ingress from the ALB's SG on the application port. |
| **CAB-02** | Permission Boundaries | What does an IAM Permissions Boundary actually control? | It sets the **maximum** permissions a role/user can have — the role's own identity-based policies can only narrow access further, never exceed the boundary. |
| **CAB-02** | ABAC | What is Attribute-Based Access Control (ABAC), and why use it over per-resource roles? | Access decisions are based on **tags** (e.g., `aws:PrincipalTag`, `aws:ResourceTag`) instead of hardcoding a role per resource — it scales least privilege without policy sprawl. |
| **CAB-02** | Resource vs Identity Policy Precedence | If an identity-based policy allows an action but a resource-based (bucket) policy explicitly denies it, what wins? | An explicit **Deny** always wins, regardless of which policy type it's on. |
| **CAB-02** | IAM Access Analyzer | What does IAM Access Analyzer detect that a manual policy review might miss? | Resource-based policies (S3 bucket policies, KMS key policies, IAM role trust policies, etc.) that grant access to a principal **outside** the account or organization — i.e., unintended external access. |
| **CAB-02** | Zero-Trust Bucket Policy | Why enforce `aws:PrincipalTag` conditions on a bucket policy instead of relying only on IAM role permissions? | Zero-Trust assumes internal identity alone isn't enough proof of authorization — a resource-based deny-by-default policy blocks access even if a caller's identity-based policy would otherwise allow it. |

## 🏷️ Domain 4: Design Cost-Optimized Architectures

| Week | Concept | Question | Answer |
| :--- | :--- | :--- | :--- |
| **CAB-06** | S3 Storage Classes | For medical imaging accessed daily for a month, then rarely, then almost never after a year — what's the cost-optimal tiering? | Standard → Standard-IA (after ~30 days) → Glacier (after ~90 days) → Glacier Deep Archive (after ~180 days), via an S3 Lifecycle Rule. |
| **CAB-06** | Lifecycle vs Intelligent-Tiering | When should you use S3 Intelligent-Tiering instead of manual lifecycle rules? | When the access pattern is **unpredictable** — Intelligent-Tiering has no retrieval fee (unlike Glacier) and moves objects automatically, at the cost of a small per-object monitoring fee. |
| **CAB-06** | Encryption Cost Tradeoff | Why choose SSE-S3 over SSE-KMS for a large archival bucket with no key-rotation requirement? | SSE-KMS bills per API call (`kms:GenerateDataKey`, etc.) at scale; SSE-S3 is free. Reserve CMKs (SSE-KMS) for data that specifically needs key-level audit and rotation control. |
| **CAB-06** | Hidden Cost Leak | A bucket's storage cost is higher than expected even though visible objects are small. What's a common cause? | **Incomplete multipart uploads** that were never aborted — they still consume storage and bill indefinitely unless a lifecycle rule aborts them after N days. |
| **CAB-06** | Budgets vs Cost Explorer vs Trusted Advisor | What's the difference between these three cost tools? | **AWS Budgets** alerts on actual/forecasted spend against a threshold you set. **Cost Explorer** visualizes and analyzes historical spend trends. **Trusted Advisor** flags specific optimization opportunities (idle EC2, low-utilization RDS, unattached EBS, etc.) as a support-plan feature. |

## 🏷️ Domain 3: Design High-Performing Architectures

| Week | Concept | Question | Answer |
| :--- | :--- | :--- | :--- |
| **CAB-07** | SQS Visibility Timeout | Why size an SQS queue's visibility timeout off the consumer's function timeout instead of leaving the 30-second default? | If the consumer is still processing when the timeout expires, SQS makes the message visible again and a second worker can pick it up — a common cause of duplicate processing. AWS recommends at least 6x the consumer's timeout. |
| **CAB-07** | Reserved Concurrency | An SQS-triggered Lambda writes to an RDS instance that can only handle a handful of connections at once. A traffic spike floods the queue. What protects the database? | Set **Reserved Concurrent Executions** on the Lambda — it caps how many invocations can run in parallel regardless of how deep the queue gets. |
| **CAB-07** | SQS vs EventBridge | You need to decouple a producer from exactly one consumer that must process every message in order it arrives (per group). Later, you need to decouple a domain event from an unknown, growing number of subscribers. Which service for which? | **SQS** for point-to-point buffering to one consumer type (use FIFO if ordering matters). **EventBridge** for pub/sub fan-out where the publisher shouldn't need to know who's listening. |
| **CAB-07** | CloudFront Origin Access | Why use Origin Access Control (OAC) instead of making the S3 origin bucket public when it's already sitting behind CloudFront? | A public bucket can be reached directly, bypassing CloudFront (and any caching, WAF, or geo-restriction it provides). OAC lets only the specific CloudFront distribution read the bucket. |
| **CAB-07** | Dead Letter Queues | What's the purpose of a DLQ and what happens without one? | A DLQ catches messages that fail processing repeatedly (`maxReceiveCount` exceeded) for later inspection. Without one, poison messages either loop forever, consuming consumer capacity, or silently vanish at the queue's retention limit. |

---
## 🏁 Status Check:
- **Questions Stored:** 41
- **Coverage Gap:** None — all four SAA-C03 domains now have question-bank coverage.
- **Next Step:** All of CAB-02, CAB-06, and CAB-07 are code-complete but pending live AWS deployment/verification. CAB-08 (Final Blitz: timed practice exam + portfolio launch) is the last open block.
