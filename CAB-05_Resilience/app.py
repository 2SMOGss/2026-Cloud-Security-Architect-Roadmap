#!/usr/bin/env python3
import aws_cdk as cdk
from vpc_stack import VitalStreamVpcStack
from rds_stack import VitalStreamRdsStack
from compute_stack import VitalStreamComputeStack
from monitoring_stack import VitalStreamMonitoringStack

app = cdk.App()

# Common env for Billing metrics (always us-east-1)
us_east_1 = cdk.Environment(region="us-east-1")

# 1. Infrastructure Tier (VPC across 2 AZs)
infra = VitalStreamVpcStack(app, "VitalStream-HA-VPC-Stack")

# 2. Data Tier (Multi-AZ RDS)
data = VitalStreamRdsStack(app, "VitalStream-HA-RDS-Stack", 
    vpc=infra.vpc
)

# 3. Compute Tier (ALB + ASG Self-Healing)
compute = VitalStreamComputeStack(app, "VitalStream-HA-Compute-Stack", 
    vpc=infra.vpc,
    rds_instance=data.db
)

# 4. Monitoring Tier (Financial Guardrails)
monitoring = VitalStreamMonitoringStack(app, "VitalStream-HA-Monitoring-Stack", 
    env=us_east_1
)

app.synth()
