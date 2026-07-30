from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    CfnOutput,
    aws_s3 as s3,
    aws_budgets as budgets,
)
from constructs import Construct


class VitalStreamCostStack(Stack):
    """
    CAB-06: S3 Lifecycle & Cost Optimization
    SAA-C03 Domain 4 (Design Cost-Optimized Architectures)

    Self-contained (no dependency on other CABs, per the Time Capsule Rule):
      1. An archive bucket with a *predictable* access pattern -- manual
         lifecycle transitions (Standard -> Standard-IA -> Glacier ->
         Deep Archive), noncurrent-version expiration, and abort of
         incomplete multipart uploads.
      2. A second bucket with an *unpredictable* access pattern -- S3
         Intelligent-Tiering, which moves objects between tiers
         automatically with no retrieval fee, trading a small monitoring
         fee for not having to guess an access pattern.
      3. An AWS Budget with a forecasted-spend alert, satisfying the
         "Cost-Aware Engineering" rule in roadmap-v3.2.md.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Archive bucket: known access pattern -> manual lifecycle tiers.
        # SAA-C03: SSE-S3 (free) is the cost-conscious choice here vs.
        # SSE-KMS, which bills per API call -- reserve CMKs (see CAB-03)
        # for data that specifically needs key-level audit/rotation control.
        self.archive_bucket = s3.Bucket(
            self, "VitalStream-Archive-Bucket",
            bucket_name=f"vitalstream-cost-archive-{Stack.of(self).account}",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,  # Ephemeral lab
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="TierDownColdData",
                    enabled=True,
                    transitions=[
                        s3.Transition(
                            storage_class=s3.StorageClass.INFREQUENT_ACCESS,
                            transition_after=Duration.days(30),
                        ),
                        s3.Transition(
                            storage_class=s3.StorageClass.GLACIER,
                            transition_after=Duration.days(90),
                        ),
                        s3.Transition(
                            storage_class=s3.StorageClass.DEEP_ARCHIVE,
                            transition_after=Duration.days(180),
                        ),
                    ],
                ),
                s3.LifecycleRule(
                    id="ExpireOldVersions",
                    enabled=True,
                    noncurrent_version_expiration=Duration.days(30),
                ),
                s3.LifecycleRule(
                    id="AbortIncompleteMultipartUploads",
                    enabled=True,
                    abort_incomplete_multipart_upload_after=Duration.days(7),
                ),
            ],
        )

        # 2. Unpredictable-access bucket: let S3 do the tiering.
        # SAA-C03: Intelligent-Tiering has no retrieval fee and no
        # operational overhead -- the tradeoff is a small per-object
        # monitoring fee versus the "free" but manual lifecycle rules above.
        self.intelligent_bucket = s3.Bucket(
            self, "VitalStream-Intelligent-Bucket",
            bucket_name=f"vitalstream-cost-intelligent-{Stack.of(self).account}",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.DESTROY,
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="MoveToIntelligentTieringImmediately",
                    enabled=True,
                    transitions=[
                        s3.Transition(
                            storage_class=s3.StorageClass.INTELLIGENT_TIERING,
                            transition_after=Duration.days(0),
                        ),
                    ],
                ),
            ],
        )

        # 3. AWS Budget: forecasted-spend alert.
        # SAA-C03: Budgets alert on projected/actual spend; Cost Explorer
        # analyzes historical spend; Trusted Advisor flags specific
        # cost-optimization opportunities (idle resources, low
        # utilization) -- three different tools for three different jobs.
        alert_email = self.node.try_get_context("budget_alert_email") or "changeme@example.com"
        self.monthly_budget = budgets.CfnBudget(
            self, "VitalStream-Monthly-Budget",
            budget=budgets.CfnBudget.BudgetDataProperty(
                budget_name="VitalStream-Monthly-Lab-Budget",
                budget_type="COST",
                time_unit="MONTHLY",
                budget_limit=budgets.CfnBudget.SpendProperty(
                    amount=50,
                    unit="USD",
                ),
            ),
            notifications_with_subscribers=[
                budgets.CfnBudget.NotificationWithSubscribersProperty(
                    notification=budgets.CfnBudget.NotificationProperty(
                        notification_type="FORECASTED",
                        comparison_operator="GREATER_THAN",
                        threshold=80,
                        threshold_type="PERCENTAGE",
                    ),
                    subscribers=[
                        budgets.CfnBudget.SubscriberProperty(
                            subscription_type="EMAIL",
                            address=alert_email,
                        )
                    ],
                )
            ],
        )

        # Outputs
        CfnOutput(self, "ArchiveBucketName", value=self.archive_bucket.bucket_name)
        CfnOutput(self, "IntelligentBucketName", value=self.intelligent_bucket.bucket_name)
        CfnOutput(self, "BudgetName", value="VitalStream-Monthly-Lab-Budget")
