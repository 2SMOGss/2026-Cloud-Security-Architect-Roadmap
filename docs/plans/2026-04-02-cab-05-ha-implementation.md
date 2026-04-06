# CAB-05: Resilience & High Availability Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Build a 3-tier, self-healing medical portal with Multi-AZ RDS and ALB/ASG.

**Architecture:** 3-stack CDK approach (Infrastructure -> Data -> Compute). All tiers span 2 AZs.

**Tech Stack:** AWS CDK (Python), Amazon RDS, ALB, ASG, Flask, IAM RBAC.

---

### Task 1: Initialize CAB-05 Infrastructure Stack (VPC)
**Files:**
- Create: `CAB-05_Resilience/vpc_stack.py`
- Create: `CAB-05_Resilience/app.py`

**Step 1: Create the VPC Stack with 3-tier subnets**
```python
from aws_cdk import (Stack, aws_ec2 as ec2, Tags)
from constructs import Construct

class VitalStreamVpcStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = ec2.Vpc(
            self, "VitalStream-HA-VPC",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
                ec2.SubnetConfiguration(name="App", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24),
                ec2.SubnetConfiguration(name="Data", subnet_type=ec2.SubnetType.PRIVATE_ISOLATED, cidr_mask=24)
            ]
        )
```

**Step 2: Commit**
```bash
git add CAB-05_Resilience/
git commit -m "feat(cab05): initialize HA vpc stack"
```

### Task 2: Deploy Multi-AZ RDS Data Tier
**Files:**
- Create: `CAB-05_Resilience/rds_stack.py`

**Step 1: Implement Multi-AZ RDS Cluster**
```python
from aws_cdk import (Stack, aws_rds as rds, aws_ec2 as ec2)
class VitalStreamRdsStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.db = rds.DatabaseInstance(
            self, "VitalStream-DB",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_15),
            vpc=vpc,
            multi_az=True,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Data"),
            allocated_storage=20
        )
```

**Step 2: Commit**
```bash
git add CAB-05_Resilience/rds_stack.py
git commit -m "feat(cab05): add multi-az rds stack"
```

### Task 3: Implement ALB + ASG Compute Tier
**Files:**
- Create: `CAB-05_Resilience/compute_stack.py`

**Step 1: Define ALB and ASG with Health Checks**
Include an Auto Scaling Group with min_capacity=2 and an ALB in the Public subnets.

**Step 2: Commit**
```bash
git add CAB-05_Resilience/compute_stack.py
git commit -m "feat(cab05): add alb and asg compute tier"
```

### Task 4: Create Flask Portal & IAM RBAC
**Files:**
- Create: `CAB-05_Resilience/app/main.py`
- Create: `CAB-05_Resilience/app/templates/index.html`

**Step 1: Implement Stateless Flask App**
Add `/health` route and `/records` route with conditional IAM-based logic.

**Step 2: Commit**
```bash
git add CAB-05_Resilience/app/
git commit -m "feat(cab05): implement flask portal with rbac logic"
```

### Task 5: The "Chaos Audit" (Verification)
**Step 1: Verify ASG Self-Healing**
`aws ec2 terminate-instances --instance-ids <id>`
Expect: New instance appears in `aws autoscaling describe-auto-scaling-groups`.

**Step 2: Verify RDS Failover**
`aws rds reboot-db-instance --db-instance-identifier <id> --force-failover`
Expect: Minimal connectivity dip, then app reconnects to standby.

### Task 6: Real-Time Cost Monitoring Setup
**Files:**
- Create: `CAB-05_Resilience/billing_stack.py`

**Step 1: Implement AWS Budget and CloudWatch Billing Alarm**
1. Create an SNS Topic for alerts.
2. Define an AWS Budget for $1.00.
3. Create a CloudWatch Alarm for `EstimatedCharges` > $1.00.

**Step 2: Commit**
```bash
git add CAB-05_Resilience/billing_stack.py
git commit -m "feat(cab05): add real-time cost monitoring guardrails"
```
