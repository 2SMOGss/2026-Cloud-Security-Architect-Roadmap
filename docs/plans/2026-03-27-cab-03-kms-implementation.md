# 🔒 VitalStream Encryption Core (CAB-03) Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Implement a tiered KMS encryption strategy and an immutable S3 audit core for HIPAA compliance.

**Architecture:** Four Customer Managed Keys (CMKs) protecting PHI tiers and Audit logs, with S3 Object Lock (Compliance Mode) for log integrity.

**Tech Stack:** AWS CDK (Python), Pytest, Boto3.

---

### Task 1: Environment Scaffolding
**Files:**
- Create: `CAB-03_KMS_PHI_Protection/app.py`
- Create: `CAB-03_KMS_PHI_Protection/cdk.json`
- Create: `CAB-03_KMS_PHI_Protection/requirements.txt`

**Step 1: Create the directory and basic CDK app**
Write a minimal `app.py` that initializes the `VitalStreamDataStack`.

**Step 2: Commit**
`git add CAB-03_KMS_PHI_Protection/ && git commit -m "feat(cab03): project scaffolding"`

---

### Task 2: Multi-Tier KMS CMKs
**Files:**
- Modify: `CAB-03_KMS_PHI_Protection/app.py`
- Test: `CAB-03_KMS_PHI_Protection/test_kms_stack.py`

**Step 1: Write failing test for Key Rotation**
Verify that all four keys (S3, RDS, EBS, Audit) have rotation enabled.

**Step 2: Implement CMKs in CDK**
Use `aws_kms.Key` with `enable_key_rotation=True`.

**Step 3: Verify and Commit**
`pytest CAB-03_KMS_PHI_Protection/test_kms_stack.py`

---

### Task 3: Immutable Audit S3 Bucket
**Files:**
- Modify: `CAB-03_KMS_PHI_Protection/app.py`
- Test: `CAB-03_KMS_PHI_Protection/test_audit_integrity.py`

**Step 1: Write test for Object Lock & Encryption**
Ensure the bucket has `object_lock_enabled=True` and is encrypted with the `Audit-Key`.

**Step 2: Implement S3 Bucket in CDK**
Configure `BlockPublicAccess.BLOCK_ALL` and `ObjectLockMode.COMPLIANCE`.

**Step 3: Commit**
`git commit -m "feat(cab03): immutable audit core"`

---

### Task 4: PHI S3 Bucket with SSE-KMS
**Files:**
- Modify: `CAB-03_KMS_PHI_Protection/app.py`

**Step 1: Implement PHI S3 Bucket**
Link the `VitalStream-S3-PHI-Key` to the bucket using `encryption=s3.BucketEncryption.KMS`.

**Step 2: Verification**
Run `cdk synth` to ensure the CloudFormation template matches the design.

---

### Task 5: SAA-C03 Session Summary & Portfolio Moment
**Files:**
- Modify: `SAA_QUESTION_BANK.md`
- Create: `docs/portfolio/cab-03-encryption-audit.md`

**Step 1: Trigger @[/saa-summary]**
Recap the session and add 5-10 scenario-based questions to the bank.

**Step 2: Document "The WOW"**
Create a brief markdown file describing the "Immutable Audit" architecture for your portfolio.
