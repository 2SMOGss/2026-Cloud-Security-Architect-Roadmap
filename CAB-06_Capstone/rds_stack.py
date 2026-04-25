from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_rds as rds,
    aws_ec2 as ec2,
)
from constructs import Construct

class VitalStreamRdsStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # 1. Security Group for RDS
        self.rds_sg = ec2.SecurityGroup(self, "VitalStreamRdsSG",
            vpc=vpc,
            description="Allow inbound traffic to RDS from App Tier",
            allow_all_outbound=True
        )

        # 2. RDS Instance (Multi-AZ for High Availability)
        self.db = rds.DatabaseInstance(self, "VitalStreamDB",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_15
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, 
                ec2.InstanceSize.MICRO
            ),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
            multi_az=True,
            allocated_storage=20,
            max_allocated_storage=50,
            storage_type=rds.StorageType.GP3,
            security_groups=[self.rds_sg],
            removal_policy=RemovalPolicy.DESTROY, # For labs only
            deletion_protection=False,
            backup_retention=ec2.Duration.days(7)
        )
