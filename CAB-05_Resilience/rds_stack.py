from aws_cdk import (Stack, aws_rds as rds, aws_ec2 as ec2, Tags)
from constructs import Construct

class VitalStreamRdsStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Multi-AZ RDS Instance for High Availability
        # Synchronous standby in separate AZ for failover
        self.db = rds.DatabaseInstance(
            self, "VitalStream-DB",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_15),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO),
            vpc=vpc,
            multi_az=True,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Data"),
            allocated_storage=20,
            publicly_accessible=False,
            database_name="vitalstream"
        )
        
        Tags.of(self.db).add("Tier", "Data")
        Tags.of(self.db).add("Availability", "Multi-AZ")

        # Allow ingress from App Subnets (breaks cycle with ComputeStack)
        app_subnets = vpc.select_subnets(subnet_group_name="App")
        for subnet in app_subnets.subnets:
            self.db.connections.allow_default_port_from(ec2.Peer.ipv4(subnet.ipv4_cidr_block))
