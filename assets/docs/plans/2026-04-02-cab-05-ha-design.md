# CAB-05: Resilience & High Availability - VitalStream Portal

## Design: Zero-Downtime Architecture

### Overview
Build a 3-tier, highly available medical portal on AWS us-east-1 across 2 Availability Zones.

### Goal
Implement a self-healing application tier (ALB/ASG) and a synchronously replicated data tier (RDS Multi-AZ) to survive AZ failure with zero data loss (RPO=0) and minimal downtime (RTO < 2min).

### Architecture Components

1. **Infrastructure Tier (VPC)**
   - 2 AZs (us-east-1a, us-east-1b)
   - 6 Subnets (2 Public for ALB, 2 Private for App, 2 Isolated for RDS)
   - Cascading Security Groups (ALB -> EC2 -> RDS)

2. **Application Tier (ALB + ASG)**
   - **Application Load Balancer (ALB):** Publicly accessible, health checks pointing to `/health`.
   - **Auto Scaling Group (ASG):** 
     - **Fleet Size:** Min 2, Max 4, Desired 2.
     - **Instance Type:** t3.micro (Amazon Linux 2023).
     - **IAM Role:** `VitalStreamAppRole` with permissions for RDS and SSM (no port 22 access).
   - **App Logic:** Python/Flask web portal to interact with RDS.

3. **Data Tier (RDS Multi-AZ)**
   - **Engine:** PostgreSQL or MySQL (Multi-AZ enabled).
   - **Availability:** One Primary, one Synchronous Standby in separate AZ.
   - **Security:** Inbound only from App Security Group.

4. **Identity & Access (IAM RBAC)**
   - **VitalStream-Admin:** Full access to CRUD patient records.
   - **VitalStream-Viewer:** Read-only access to `/health` and record lookups.

5. **Financial Health Tier (Cost Monitoring)**
   - **AWS Budget:** $1.00 threshold alert with SNS notification.
   - **CloudWatch Billing Alarm:** Monitor `EstimatedCharges` in `us-east-1`.
   - **Real-Time Cost Display:** Integrated into Flask portal for visibility.

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

### The "Chaos Audit" Plan
1. **ASG Self-Healing:** Terminate an instance manually; verify ASG launches replacement.
2. **RDS Failover:** Force a reboot with failover; verify DNS swap and app reconnection.
3. **RBAC Verification:** Attempt a "Delete" record with a Viewer role and verify 403 Forbidden.

### Metrics for Success
- **Elasticity:** CloudWatch metric for `GroupInServiceInstances` shows recovery.
- **Resilience:** ALB `HealthyHostCount` dips but stays above 1.
- **Security:** IAM Policy prevents unauthorized API calls from EC2.
