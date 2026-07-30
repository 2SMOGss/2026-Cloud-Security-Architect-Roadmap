#!/usr/bin/env python3
import os
import aws_cdk as cdk
from vitalstream_serverless_stack import VitalStreamServerlessStack

# ARCHITECT: Robert Chich
# CAB-07: Serverless Decoupling & Performance (self-contained, no dependency on other CABs)

app = cdk.App()

env = cdk.Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION", "us-east-2"),
)

VitalStreamServerlessStack(app, "VitalStream-CAB07-Serverless", env=env)

app.synth()
