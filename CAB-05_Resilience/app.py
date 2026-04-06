#!/usr/bin/env python3
import aws_cdk as cdk
from vpc_stack import VitalStreamVpcStack
from rds_stack import VitalStreamRdsStack
from compute_stack import VitalStreamComputeStack

app = cdk.App()

# 1. Infrastructure Tier (VPC across 2 AZs)
infra = VitalStreamVpcStack(app, "VitalStream-HA-VPC-Stack")

# 2. Data Tier (Multi-AZ RDS)
data = VitalStreamRdsStack(app, "VitalStream-HA-RDS-Stack", 
    vpc=infra.vpc
)

# 3. Compute Tier (ALB + ASG Self-Healing)
compute = VitalStreamComputeStack(app, "VitalStream-HA-Compute-Stack", 
    vpc=infra.vpc
)

app.synth()
