import os
import aws_cdk as cdk
from vitalstream_ai_stack import VitalStreamAiStack

# ARCHITECT: Robert Chich
# PRINCIPLE: Clean Entrypoint, Internal Lookup

app = cdk.App()

# Environment is required for VPC lookup within the stack
env = cdk.Environment(
    account="570435244246", 
    region="us-east-2"
)

# VPC lookup happens inside the Stack constructor
VitalStreamAiStack(app, "VitalStream-AI-Sentinel-Stack", env=env)

app.synth()
