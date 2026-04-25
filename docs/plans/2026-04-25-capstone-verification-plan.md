# CAB-06 Capstone Verification Script Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Build a Boto3-based audit script to verify HIPAA compliance and perform a live Chaos Audit for the VitalStream Capstone.

**Architecture:** A modular Python script where each audit category is a separate function. Uses a background thread for pinging during the Chaos Audit.

**Tech Stack:** Python 3, Boto3, Requests.

---

### Task 1: Scaffolding and Guardrails Audit
**Files:**
- Create: `scripts/verify_capstone.py`
- Test: `scripts/test_verify_capstone.py`

**Step 1: Write failing test for budget check**
```python
import pytest
from verify_capstone import audit_guardrails

def test_audit_guardrails_fails_if_budget_missing(mocker):
    mocker.patch('boto3.client')
    # Mock budget not found
    mock_client = mocker.Mock()
    mock_client.get_budgets.return_value = {'Budgets': []}
    
    with pytest.raises(Exception, match="VitalStream-Budget not found"):
        audit_guardrails(mock_client)
```

**Step 2: Run test to verify it fails**
Run: `pytest scripts/test_verify_capstone.py`

**Step 3: Implement minimal budget check**
```python
import boto3

def audit_guardrails(client):
    response = client.get_budgets(AccountId='123456789012') # Placeholder
    budgets = response.get('Budgets', [])
    for b in budgets:
        if b['BudgetName'] == 'VitalStream-Budget':
            return True
    raise Exception("VitalStream-Budget not found")
```

**Step 4: Run test to verify it passes**
Run: `pytest scripts/test_verify_capstone.py`

**Step 5: Commit**
```bash
git add scripts/verify_capstone.py scripts/test_verify_capstone.py
git commit -m "feat(verify): add base script and budget guardrail check"
```

---

### Task 2: Storage & Edge Audit
**Files:**
- Modify: `scripts/verify_capstone.py`
- Modify: `scripts/test_verify_capstone.py`

**Step 1: Write test for S3 Public Access Block**
```python
def test_audit_storage_verifies_public_access_block(mocker):
    # Mock s3.get_public_access_block
    pass
```

**Step 2: Implement `audit_storage` function**
(Verify S3 PublicAccessBlock and CloudFront OAC)

**Step 3: Run tests**

**Step 4: Commit**
```bash
git commit -m "feat(verify): add storage and edge audit logic"
```

---

### Task 3: Data Tier Audit (RDS Multi-AZ)
**Files:**
- Modify: `scripts/verify_capstone.py`

**Step 1: Implement `audit_data_tier`**
Check RDS `MultiAZ` property and `StorageEncrypted`.

**Step 2: Commit**
```bash
git commit -m "feat(verify): add rds multi-az and encryption audit"
```

---

### Task 4: Compute Tier & Performance Audit
**Files:**
- Modify: `scripts/verify_capstone.py`

**Step 1: Implement `audit_compute`**
Check ASG Desired Capacity and ALB Health.

**Step 2: Implement `benchmark_performance`**
Measure latency for 10 requests to CloudFront.

**Step 3: Commit**
```bash
git commit -m "feat(verify): add compute tier and performance benchmarking"
```

---

### Task 5: Chaos Audit Module
**Files:**
- Modify: `scripts/verify_capstone.py`

**Step 1: Implement `run_chaos_audit`**
- Pinger thread.
- Instance termination.
- Recovery monitoring.

**Step 2: Commit**
```bash
git commit -m "feat(verify): implement live chaos audit module"
```

---

### Task 6: Final Verification Run
**Action:** Execute the script and capture output for the report.

Run: `python scripts/verify_capstone.py --chaos`
Expected: Markdown table summary.

**Step 2: Update `Week06_Capstone_Final.md`**
Paste the results into the report.

**Step 3: Final Commit**
```bash
git commit -m "docs(capstone): finalize verification report with automated audit results"
```
