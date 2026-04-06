from aws_cdk import (Stack, aws_ec2 as ec2, Tags)
from constructs import Construct

class VitalStreamVpcStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # 3-Tier Multi-AZ VPC
        self.vpc = ec2.Vpc(
            self, "VitalStream-HA-VPC",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
                ec2.SubnetConfiguration(name="App", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24),
                ec2.SubnetConfiguration(name="Data", subnet_type=ec2.SubnetType.PRIVATE_ISOLATED, cidr_mask=24)
            ]
        )
        
        Tags.of(self.vpc).add("Project", "VitalStream-Resilience")
        Tags.of(self.vpc).add("Phase", "CAB-05")
