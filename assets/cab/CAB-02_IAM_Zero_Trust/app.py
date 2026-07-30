#!/usr/bin/env python3
import os
import aws_cdk as cdk
from vitalstream_iam_stack import VitalStreamIamStack

# ARCHITECT: Robert Chich
# CAB-02: IAM & Zero-Trust (self-contained, no dependency on other CABs)

app = cdk.App()

# Account/region come from the CDK CLI's own environment resolution
# (CDK_DEFAULT_ACCOUNT / CDK_DEFAULT_REGION, set by `aws configure` +
# `cdk bootstrap`) rather than a hardcoded account ID.
env = cdk.Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION", "us-east-2"),
)

VitalStreamIamStack(app, "VitalStream-CAB02-IAM", env=env)

app.synth()
