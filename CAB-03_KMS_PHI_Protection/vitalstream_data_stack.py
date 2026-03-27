import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_kms as kms,
    aws_s3 as s3,
    aws_iam as iam,
    RemovalPolicy,
)
from constructs import Construct

class VitalStreamDataStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. KMS Root of Trust: Customer Managed Keys (CMKs)
        # SAA-C03: All keys have enable_key_rotation=True (HIPAA requirement)
        
        # A. S3 PHI Encryption Key
        self.phi_key = kms.Key(self, "VitalStream-S3-PHI-Key",
            alias="alias/vitalstream/s3-phi",
            description="KMS Key for Patient Health Information (S3)",
            enable_key_rotation=True,
            pending_window=cdk.Duration.days(30)
        )

        # B. RDS Data Encryption Key
        self.rds_key = kms.Key(self, "VitalStream-RDS-Data-Key",
            alias="alias/vitalstream/rds-data",
            description="KMS Key for RDS Database Encryption",
            enable_key_rotation=True
        )

        # C. EBS Tier Encryption Key
        self.ebs_key = kms.Key(self, "VitalStream-EBS-Tier-Key",
            alias="alias/vitalstream/ebs-tier",
            description="KMS Key for EC2 EBS Volume Encryption",
            enable_key_rotation=True
        )

        # D. Audit Log Encryption Key
        self.audit_key = kms.Key(self, "VitalStream-Audit-Key",
            alias="alias/vitalstream/audit-logs",
            description="KMS Key for Immutable Audit Logs",
            enable_key_rotation=True
        )

        # 2. Immutable Audit Core: S3 Bucket with Object Lock
        # (Already implemented in Task 3)
        self.audit_bucket = s3.Bucket(self, "VitalStream-Audit-S3-Bucket",
            bucket_name=f"vitalstream-audit-core-{cdk.Stack.of(self).account}",
            encryption=s3.BucketEncryption.KMS,
            encryption_key=self.audit_key,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            versioned=True,
            object_lock_enabled=True,
            object_lock_default_retention=s3.ObjectLockRetention.compliance(cdk.Duration.days(365 * 7)),
            removal_policy=RemovalPolicy.RETAIN
        )

        # 3. PHI Data Protection: Medical Records S3 Bucket
        # SAA-C03: SSE-KMS with Customer Managed Key is the HIPAA requirement
        self.phi_bucket = s3.Bucket(self, "VitalStream-PHI-Records-Bucket",
            bucket_name=f"vitalstream-phi-data-{cdk.Stack.of(self).account}",
            encryption=s3.BucketEncryption.KMS,
            encryption_key=self.phi_key,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY  # SAA-C03: Labs use DESTROY for cost control
        )

        # Outputs
        cdk.CfnOutput(self, "PhiBucketArn", value=self.phi_bucket.bucket_arn)
        cdk.CfnOutput(self, "AuditBucketArn", value=self.audit_bucket.bucket_arn)
