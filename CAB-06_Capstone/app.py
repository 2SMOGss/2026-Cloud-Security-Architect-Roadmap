#!/usr/bin/env python3
import aws_cdk as cdk
from vpc_stack import VitalStreamVpcStack
from billing_stack import VitalStreamBillingStack
from storage_stack import VitalStreamStorageStack
from rds_stack import VitalStreamRdsStack
from compute_stack import VitalStreamComputeStack

app = cdk.App()
env = cdk.Environment(account=app.node.try_get_context("account"), region="us-east-1")

# 1. Network Foundation (HIPAA VPC)
vpc_stack = VitalStreamVpcStack(app, "VitalStream-Network", env=env)

# 2. Financial Guardrails (Budget/Alarm)
billing = VitalStreamBillingStack(app, "VitalStream-Billing", env=env)

# 3. Storage & Edge Foundation
storage = VitalStreamStorageStack(app, "VitalStream-Storage", env=env)

# 4. Data Tier (RDS Multi-AZ)
rds = VitalStreamRdsStack(app, "VitalStream-RDS", 
    vpc=vpc_stack.vpc, 
    env=env
)

# 5. Compute Tier (ALB + ASG)
compute = VitalStreamComputeStack(app, "VitalStream-Compute",
    vpc=vpc_stack.vpc,
    distribution=storage.distribution,
    env=env
)

app.synth()
