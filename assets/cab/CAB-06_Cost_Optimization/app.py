#!/usr/bin/env python3
import os
import aws_cdk as cdk
from vitalstream_cost_stack import VitalStreamCostStack

# ARCHITECT: Robert Chich
# CAB-06: S3 Lifecycle & Cost Optimization (self-contained, no dependency on other CABs)

app = cdk.App()

env = cdk.Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION", "us-east-2"),
)

# Pass your real notification address at deploy time -- do NOT hardcode
# it here, this file is committed to a public repo:
#   cdk deploy -c budget_alert_email=you@example.com
VitalStreamCostStack(app, "VitalStream-CAB06-Cost", env=env)

app.synth()
