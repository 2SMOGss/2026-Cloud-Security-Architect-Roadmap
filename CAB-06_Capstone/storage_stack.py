from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_cloudfront as cf,
    aws_cloudfront_origins as origins,
)
from constructs import Construct

class VitalStreamStorageStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # 1. S3 Bucket for Static Assets (Images, CSS, etc.)
        self.static_bucket = s3.Bucket(self, "VitalStreamStaticAssets",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=RemovalPolicy.DESTROY, # For labs only; use RETAIN for prod
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True
        )

        # 2. CloudFront Distribution with OAC (Origin Access Control)
        # Note: CDK modern S3Origin uses OAC by default
        self.distribution = cf.Distribution(self, "VitalStreamCDN",
            default_behavior=cf.BehaviorOptions(
                origin=origins.S3Origin(self.static_bucket),
                viewer_protocol_policy=cf.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cf.CachePolicy.CACHING_OPTIMIZED
            ),
            comment="VitalStream Edge Delivery Layer",
            default_root_object="index.html"
        )
