#!/usr/bin/env python3
import aws_cdk as cdk
from billing_stack import VitalStreamBillingStack
from storage_stack import VitalStreamStorageStack
from rds_stack import VitalStreamRdsStack
from compute_stack import VitalStreamComputeStack

app = cdk.App()

# 1. Financial Guardrails (Budget/Alarm)
billing = VitalStreamBillingStack(app, "VitalStream-Billing",
    env=cdk.Environment(account=app.node.try_get_context("account"), region="us-east-1") # Billing alarms MUST be in us-east-1
)

# 2. Storage & Edge Foundation
storage = VitalStreamStorageStack(app, "VitalStream-Storage",
    env=cdk.Environment(account=app.node.try_get_context("account"), region="us-east-1")
)

# 3. Data Tier (RDS Multi-AZ)
# Note: In a real scenario, we'd fetch the VPC from a Core Stack or context
# For this lab, we assume a VPC is provided or created here.
# Assuming CAB-01 VPC Plumbing is reused via VPC lookup
# vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_name="VitalStream-VPC")

# 4. Compute Tier (ALB + ASG)
# compute = VitalStreamComputeStack(app, "VitalStream-Compute",
#    vpc=vpc,
#    distribution=storage.distribution,
#    env=cdk.Environment(...)
# )

app.synth()
