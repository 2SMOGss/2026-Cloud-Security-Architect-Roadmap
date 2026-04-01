#!/usr/bin/env python3
import aws_cdk as cdk
from vitalstream_vpc_stack import VitalStreamVpcStack

app = cdk.App()
VitalStreamVpcStack(app, "VitalStream-CAB01-VPC", 
    env=cdk.Environment(region="us-east-2")
)
app.synth()
