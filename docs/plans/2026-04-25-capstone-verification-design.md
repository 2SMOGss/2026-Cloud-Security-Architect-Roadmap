# Design: CAB-06 Capstone "Dean's Audit" Script

**Date:** 2026-04-25
**Topic:** Automated Verification & Chaos Audit
**Status:** APPROVED

## 🎯 Objectives
Automate the verification of the VitalStream HIPAA-aligned architecture and perform a live Chaos Audit to satisfy the "Dean's Audit" requirements of the CAB-06 Capstone.

## 🏗️ Architecture
The script `verify_capstone.py` will use Python 3 and Boto3 to interface with AWS.

### 1. Verification Modules
| Module | AWS Service | Check Logic |
| :--- | :--- | :--- |
| **Guardrails** | Budgets | Ensure "VitalStream-Budget" exists and is <= $30. |
| **Storage** | S3 / CF | Verify S3 Public Access Blocked; Verify CF OAC is used. |
| **Data** | RDS | Verify Multi-AZ deployment and Storage Encryption. |
| **Compute** | ELB / ASG | Verify ALB health and ASG min/max/desired settings. |

### 2. Chaos Audit Logic
1. **Identify Target:** Find an instance in the `VitalStream-ASG` currently in a "Healthy" state.
2. **Connectivity Baseline:** Start pinging the CloudFront endpoint.
3. **Trigger Chaos:** Terminate the instance via `ec2.terminate_instances()`.
4. **Monitor Recovery:**
    - Track HTTP 200 OK success rate.
    - Measure time until ASG brings a new instance into the ALB Target Group.
    - Calculate total "Downtime" or packet loss.

### 3. Performance Benchmark
- Fetch `logo.png` (or index.html) 10 times from S3 directly and 10 times from CloudFront.
- Output Average, Min, and Max latencies.

## 📊 Output Format
The script will print a Markdown-formatted table to stdout, designed for the `Week06_Capstone_Final.md` report.

## 🛡️ Security & Compliance
- Script will run locally using the user's AWS CLI credentials.
- No hardcoded keys.
- Strictly "Read-Only" except for the Chaos Audit `terminate` command.
