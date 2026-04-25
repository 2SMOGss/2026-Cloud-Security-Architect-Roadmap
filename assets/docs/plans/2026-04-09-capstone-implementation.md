# Week 06 Capstone: Frugal High-Performance Portal Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Build a production-grade, HIPAA-aligned medical portal that leverages CloudFront for performance and Multi-AZ for resilience, all within a $30/month budget.

**Architecture:** A 4-layer CDK approach:
1. **Guardrails Tier**: Budget alarms and SNS notifications.
2. **Storage Tier**: S3 for static assets + CloudFront OAC.
3. **Data Tier**: Multi-AZ RDS PostgreSQL.
4. **Compute Tier**: ALB + ASG + CloudFront Hybrid Origin.

**Tech Stack:** AWS CDK (Python), S3, CloudFront, ALB, ASG, RDS, Flask.

---

### Task 1: Update Financial Guardrails
**Files:**
- Create: `CAB-06_Capstone/billing_stack.py`

**Step 1: Implement $30 Budget and $1 Alarm**
```python
from aws_cdk import (Stack, aws_budgets as budgets, aws_cloudwatch as cw, aws_sns as sns)

class VitalStreamBillingStack(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        topic = sns.Topic(self, "BudgetAlert")
        budgets.CfnBudget(self, "MonthlyBudget",
            budget=budgets.CfnBudget.BudgetDataProperty(
                budget_limit=budgets.CfnBudget.SpendProperty(amount=30, unit="USD"),
                budget_type="COST",
                time_unit="MONTHLY"
            )
        )
```

**Step 2: Commit**
```bash
git add CAB-06_Capstone/billing_stack.py
git commit -m "feat(capstone): add $30 budget guardrails"
```

---

### Task 2: Storage & Edge Foundation (Domain 2 & 4)
**Files:**
- Create: `CAB-06_Capstone/storage_stack.py`

**Step 1: Create S3 Static Bucket and CloudFront OAC**
```python
from aws_cdk import (Stack, aws_s3 as s3, aws_cloudfront as cf, aws_cloudfront_origins as origins)

class VitalStreamStorageStack(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.static_bucket = s3.Bucket(self, "VitalStreamStatic")
        self.distribution = cf.Distribution(self, "VitalStreamDist",
            default_behavior=cf.BehaviorOptions(origin=origins.S3Origin(self.static_bucket))
        )
```

**Step 2: Commit**
```bash
git add CAB-06_Capstone/storage_stack.py
git commit -m "feat(capstone): add s3 and cloudfront edge layer"
```

---

### Task 3: Multi-AZ Data Tier (Domain 1)
**Files:**
- Create: `CAB-06_Capstone/rds_stack.py`

**Step 1: Implement Multi-AZ RDS Cluster**
```python
from aws_cdk import (Stack, aws_rds as rds, aws_ec2 as ec2)

class VitalStreamRdsStack(Stack):
    def __init__(self, scope, id, vpc, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.db = rds.DatabaseInstance(self, "VitalStreamDB",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_15),
            vpc=vpc,
            multi_az=True,
            allocated_storage=20
        )
```

**Step 2: Commit**
```bash
git add CAB-06_Capstone/rds_stack.py
git commit -m "feat(capstone): add multi-az rds data tier"
```

---

### Task 4: Hybrid Compute Tier (ALB + ASG)
**Files:**
- Create: `CAB-06_Capstone/compute_stack.py`

**Step 1: Define ALB and ASG with CloudFront as Origin**
```python
from aws_cdk import (Stack, aws_elasticloadbalancingv2 as alb, aws_autoscaling as asg)

# Logic to add ALB as a secondary origin to the CloudFront Distribution
```

**Step 2: Commit**
```bash
git add CAB-06_Capstone/compute_stack.py
git commit -m "feat(capstone): add alb/asg compute tier"
```

---

### Task 5: The Final Dean's Audit (Verification)
**Step 1: Chaos Audit**
- Terminate one instance.
- Verify 0% packet loss via CloudFront.

**Step 2: Performance Audit**
- Compare latency of static assets via S3 vs. CloudFront Edge.

**Step 3: Commit Documentation**
```bash
git add docs/reports/Week06_Capstone_Final.md
git commit -m "docs(capstone): finalize week 06 verification"
```
