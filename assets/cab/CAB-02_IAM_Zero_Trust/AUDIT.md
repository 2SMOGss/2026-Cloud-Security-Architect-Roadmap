# 🛡️ IAM & Zero-Trust Security Audit

**Project**: VitalStream Medical Cloud
**Compliance Focus**: HIPAA Section 164.312(a) (Access Control), Least Privilege
**Status**: 🔲 Code scaffolded and locally verified. **Live AWS deployment/verification pending** — this file gets updated with real proof once the stack is actually deployed and tested (per the Manual Terminal Execution policy in `CONTEXT.md`, deployment commands are run by the user, not the agent).

## 🎯 Objective
Demonstrate least-privilege identity design and a Zero-Trust posture for the VitalStream App Tier: a role that can never exceed a fixed permission boundary, an ABAC-gated trust policy, a deny-by-default resource policy on a sensitive bucket, and continuous auditing via IAM Access Analyzer.

## 🏗️ Architecture Design (SAA-C03 Domain 1)
- **Permission Boundary**: `VitalStream-AppTier-Boundary` — hard ceiling on the App-Tier role; explicitly denies `iam:*`, `organizations:*`, `account:*` regardless of what the role's own policies say.
- **Identity-Based Policy**: `VitalStream-App-Tier-Role` — scoped to `s3:GetObject`/`s3:PutObject`/`secretsmanager:GetSecretValue`, conditioned on `aws:ResourceTag/Project`.
- **ABAC Trust Policy**: the role's assume-role policy denies `sts:AssumeRole` unless the calling principal carries `aws:PrincipalTag/Project = VitalStream-Medical-Cloud`.
- **Resource-Based Policy**: `VitalStream-ZeroTrust-Bucket` denies all `s3:*` to any principal without the matching project tag — independent of whatever identity-based policy that principal holds.
- **Continuous Audit**: `VitalStream-ZeroTrust-Analyzer` (IAM Access Analyzer, account-level) flags any resource policy here or elsewhere in the account that grants access outside the zone of trust.

## ✅ Local Verification (Completed)
- `python app.py` synthesizes without error (validated in a clean venv with `aws-cdk-lib>=2.0.0`).
- `pytest` — 5/5 tests passing:
  - Permission boundary is attached to the App-Tier role.
  - Boundary explicitly denies IAM/Organizations escalation.
  - Bucket blocks all public access.
  - Bucket policy denies untagged principals (ABAC deny-by-default).
  - IAM Access Analyzer resource is created.

## ⏳ Pending Live Verification (do this next)
Follow `LAB_GUIDE.md` to deploy, then replace this section with real output:
1. `cdk deploy` succeeds and the three `CfnOutput` values (role ARN, bucket ARN, analyzer name) resolve.
2. Attempt `s3:GetObject` against the Zero-Trust bucket from a role **without** the `Project` tag — confirm `AccessDenied`.
3. Attempt `sts:AssumeRole` on the App-Tier role from a principal **without** the `Project` tag — confirm `AccessDenied`.
4. Check the IAM Access Analyzer console/CLI for findings after ~30 minutes.
5. `cdk destroy` to keep the lab ephemeral, and paste the exit code here.
