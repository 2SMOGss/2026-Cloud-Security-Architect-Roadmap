# 🔒 VitalStream: Zero-Trust PHI Protection with S3 Object Lock
**Date:** 2026-03-27
**Architecture Block:** CAB-03 (Data & PHI Protection)

## 🏗️ The Challenge
As part of the **VitalStream Medical architecture**, I needed to implement an immutable auditing layer that survives even a "Root User compromise." HIPAA requires that patient data logs are not only encrypted but also protected from deletion or modification.

## 🛡️ The Solution: Three-Tiered Immutable Architecture
1.  **Multi-Tier KMS Root-of-Trust**: Instead of using default AWS Managed Keys, I implemented four distinct **Customer Managed Keys (CMKs)** with automated rotation to enforce "Separation of Duties."
2.  **S3 Object Lock (Compliance Mode)**: I deployed a dedicated Audit Core S3 bucket with a 7-year compliance lock. This ensures logs are write-once, read-many (WORM) and cannot be deleted by any user, including the root account.
3.  **TDD Infrastructure**: Developed using **AWS CDK (Python)** with a Test-Driven Development approach using `pytest` to guarantee encryption policies are active upon deployment.

## 🎓 SAA-C03 Real-World Application
This lab directly demonstrates mastery over **HIPAA/NIST compliance patterns** in AWS, specifically targeting Domain 1 (Secure Architectures). It proves the ability to implement advanced S3 Object Lock strategies and KMS Key Policies for high-security medical workloads.
