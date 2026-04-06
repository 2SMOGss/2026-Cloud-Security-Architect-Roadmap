import aws_cdk as cdk
from aws_cdk import (
    Stack, 
    aws_ec2 as ec2, 
    aws_elasticloadbalancingv2 as elbv2, 
    aws_autoscaling as autoscaling,
    aws_iam as iam,
    Tags
)
from constructs import Construct

class VitalStreamComputeStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # 1. IAM Role for EC2 Instances
        app_role = iam.Role(
            self, "VitalStreamAppRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
            ]
        )
        
        # 2. Application Load Balancer (Public)
        self.alb = elbv2.ApplicationLoadBalancer(
            self, "VitalStream-ALB",
            vpc=vpc,
            internet_facing=True,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Public")
        )
        
        # 3. Auto Scaling Group (Private Subnets)
        # Self-healing if instances fail
        self.asg = autoscaling.AutoScalingGroup(
            self, "VitalStream-ASG",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            min_capacity=2,
            max_capacity=4,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="App"),
            role=app_role
        )
        
        # 4. ALB Listener and Target Group
        listener = self.alb.add_listener("PublicListener", port=80)
        listener.add_targets(
            "AppTarget",
            port=80,
            targets=[self.asg],
            health_check=elbv2.HealthCheck(
                path="/health",
                interval=cdk.Duration.seconds(30)
            )
        )
        
        Tags.of(self.asg).add("Tier", "App")
        Tags.of(self.alb).add("Tier", "Web")
