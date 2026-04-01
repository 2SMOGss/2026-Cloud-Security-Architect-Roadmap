from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_logs as logs,
    Tags,
    CfnOutput,
)
from constructs import Construct

class VitalStreamVpcStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Create the VPC (3-Tier: Public, Private, Isolated)
        self.vpc = ec2.Vpc(
            self, "VitalStream-Prod-VPC",
            ip_addresses=ec2.IpAddresses.cidr("10.50.0.0/16"),
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="App",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Iso-PHI",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ]
        )

        # 2. Enable VPC Flow Logs (HIPAA Compliance)
        self.vpc.add_flow_log(
            "VitalStream-FlowLogs",
            destination=ec2.FlowLogDestination.to_cloud_watch_logs(
                logs.LogGroup(
                    self, "VitalStream-VPC-FlowLogs-Group", 
                    retention=logs.RetentionDays.ONE_WEEK
                )
            )
        )

        # 3. Add Corporate Branding Tags
        Tags.of(self.vpc).add("Project", "VitalStream-Medical-Cloud")
        Tags.of(self.vpc).add("Environment", "Production")
        Tags.of(self.vpc).add("Owner", "Robert-Chich")

        # 4. Outputs
        CfnOutput(self, "VpcId", value=self.vpc.vpc_id, description="The ID of the VitalStream Production VPC")
