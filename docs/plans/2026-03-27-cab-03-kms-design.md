# 🔒 VitalStream Encryption Core (CAB-03) - Design Document
**Topic:** Data & PHI Protection (HIPAA/NIST Compliance)
**Phase:** CAB-03 (Weeks 7-9)
**Author:** Antigravity AI (Lead Cloud Security Architect)
**Status:** Approved by User

## 🎯 Purpose
To implement a "Zero-Trust" data protection layer for the VitalStream medical architecture, ensuring all Patient Health Information (PHI) is encrypted at-rest and actionably audited according to HIPAA/NIST-800-53 standards.

## 🏗️ Architecture: KMS Hierarchy
To minimize the blast radius and ensure separation of duties, we implement four distinct **Customer Managed Keys (CMKs)** in AWS KMS:

| Key Name | Purpose | Target Services | Key Policy Focus |
| :--- | :--- | :--- | :--- |
| `VitalStream-S3-PHI-Key` | Medical Imagery/Records | S3 | App-Tier IAM Role Access only. |
| `VitalStream-RDS-Data-Key` | Structured PHI Data | RDS | RDS Service Role + DB Admin Group. |
| `VitalStream-EBS-Tier-Key` | Instance Disk Encryption | EBS | Private App Subnet EC2 instances. |
| `VitalStream-Audit-Key` | Audit Log Integrity | S3-Audit, CloudTrail | CloudTrail Service + Security Auditor. |

## 🛠️ Implementation Strategy (CDK & Python)
*   **Provider**: AWS KMS (CMKs).
*   **Rotation**: `enable_key_rotation=True` for all keys (Automated 1-year rotation).
*   **Deletion Window**: `pending_window=30 days` (Maximum safety window).
*   **S3 Integration**: SSE-KMS for the PHI bucket and the Audit bucket.

## 🛡️ Auditing & Integrity (The "Audit Core")
To ensure architectural durability, we will build a dedicated **HIPAA Audit Core**:
1.  **VitalStream-Audit-S3-Bucket**:
    - **Encryption**: Encrypted with `VitalStream-Audit-Key`.
    - **S3 Object Lock**: Enabled (Compliance mode) for 7 years to ensure logs are immutable.
    - **MFA Delete**: Enabled to prevent manual deletion of compliance logs.
2.  **CloudTrail Integration**: Capturing **Data Events** for the S3-PHI bucket and **Management Events** for all KMS Keys.

## ✅ Verification & Success Criteria
1.  **KMS Policy Enforcement**: Verify that an EC2 instance without the `kms:Decrypt` permission receives an `AccessDenied` error.
2.  **Audit Trail Verification**: Confirm that KMS Key usage (Encryption/Decryption) is successfully logged in the `VitalStream-Audit-S3-Bucket`.
3.  **CDK Synth Validation**: Ensure the CloudFormation output contains the correct KMS properties and S3 Object Lock configurations.

## 🎓 SAA-C03 Exam Relevance
*   **Domain 1 (Secure Architectures)**: "Design data encryption at rest and in transit."
*   **KMS Key Policy vs. IAM Policy**: Understanding that KMS access requires *both* to be correctly configured.
*   **S3 Object Lock**: The standard answer for "Immutable Audit Log" compliance questions.
