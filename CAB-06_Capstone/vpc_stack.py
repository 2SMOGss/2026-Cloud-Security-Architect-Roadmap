from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct

class VitalStreamVpcStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a HIPAA-aligned VPC with 3 distinct tiers
        self.vpc = ec2.Vpc(self, "VitalStreamVPC",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2, # High availability across 2 AZs
            nat_gateways=1, # Single NAT to keep lab costs low
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24, # 256 IPs per subnet
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="Isolated",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24,
                )
            ]
        )
