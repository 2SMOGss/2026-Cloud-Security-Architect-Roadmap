#!/usr/bin/env python3
import aws_cdk as cdk
from vitalstream_vpc_stack import VitalStreamVpcStack
from vitalstream_data_stack import VitalStreamDataStack

app = cdk.App()

# 1. Foundation VPC (CAB-01)
vpc_stack = VitalStreamVpcStack(app, "VitalStream-CAB01-VPC", 
    env=cdk.Environment(region="us-east-2")
)

# 2. Data Encryption Core (CAB-03)
VitalStreamDataStack(app, "VitalStream-CAB03-Data",
    vpc=vpc_stack.vpc,
    env=cdk.Environment(region="us-east-2")
)

app.synth()
