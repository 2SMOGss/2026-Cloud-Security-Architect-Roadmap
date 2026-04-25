# 🛡️ Capstone Design: Frugal High-Performance Portal (Week 06)
**Architect:** Robert Chich
**Objective:** Deploy a HIPAA-compliant medical portal that balances "Zero-Downtime" resilience with "Free-Tier" performance.

## 1. Architecture Components (Domain 1 & 2)
*   **Edge Layer:** Amazon CloudFront Distribution.
    *   **Origin A (Static):** S3 Bucket (Private) storing branding, CSS, and profile images.
    *   **Origin B (Dynamic):** Application Load Balancer (ALB) routing to ASG.
*   **Compute Tier:** Auto Scaling Group (min: 2, max: 4) using `t3.micro`.
*   **Data Tier:** Multi-AZ RDS PostgreSQL (Synchronous replication).

## 2. Cost Optimization Strategy (Domain 4)
*   **Primary Guardrail:** Monthly AWS Budget set to **$30.00**.
*   **Alerting:** CloudWatch Alarm at **$1.00** (80% threshold) and **$25.00** (Critical threshold).
*   **Efficiency:** Use CloudFront caching to minimize ALB/EC2 compute time.

## 3. Dean's Audit: Comprehension Gates (Verified by Mentor)
Before we finalize this Capstone, the Dean will require proof of understanding for:
*   **Statefulness:** Why Security Groups are stateful but NACLs are not.
*   **Caching vs. Replication:** The difference between CloudFront (performance) and Multi-AZ (resilience).
*   **IAM Least Privilege:** How the EC2 Instance Profile retrieves secrets without hardcoded credentials.
*   **Edge Locations:** How CloudFront reduces latency for remote sales teams (Domain 2).
