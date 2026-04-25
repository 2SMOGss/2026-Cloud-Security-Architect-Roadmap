from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as alb,
    aws_autoscaling as asg,
    aws_cloudfront as cf,
    aws_cloudfront_origins as origins,
)
from constructs import Construct

class VitalStreamComputeStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc: ec2.IVpc, distribution: cf.Distribution, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # 1. Security Group for ALB
        self.alb_sg = ec2.SecurityGroup(self, "VitalStreamAlbSG",
            vpc=vpc,
            description="Allow HTTP traffic from CloudFront",
            allow_all_outbound=True
        )
        self.alb_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80)) # Should be restricted to CF IP ranges in prod

        # 2. Application Load Balancer
        self.alb = alb.ApplicationLoadBalancer(self, "VitalStreamALB",
            vpc=vpc,
            internet_facing=True,
            security_group=self.alb_sg
        )

        # 3. Auto Scaling Group
        self.asg = asg.AutoScalingGroup(self, "VitalStreamASG",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, 
                ec2.InstanceSize.MICRO
            ),
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
            ),
            min_capacity=2,
            max_capacity=4,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            )
        )

        # 4. Attach ALB to ASG
        listener = self.alb.add_listener("PublicListener", port=80)
        listener.add_targets("AppFleet",
            port=80,
            targets=[self.asg]
        )

        # 5. Add ALB as Origin to CloudFront Distribution for Dynamic Content
        distribution.add_origin(origins.LoadBalancerV2Origin(self.alb,
            protocol_policy=cf.OriginProtocolPolicy.HTTP_ONLY # For lab simplicity; use HTTPS for prod
        ))

        # 6. Add Behavior for /api/* or dynamic paths
        distribution.add_behavior("/api/*", 
            origin=origins.LoadBalancerV2Origin(self.alb),
            viewer_protocol_policy=cf.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            allowed_methods=cf.AllowedMethods.ALLOW_ALL,
            cache_policy=cf.CachePolicy.CACHING_DISABLED,
            origin_request_policy=cf.OriginRequestPolicy.ALL_VIEWER
        )
