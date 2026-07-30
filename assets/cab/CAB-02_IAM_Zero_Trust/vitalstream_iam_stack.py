from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput,
    aws_iam as iam,
    aws_s3 as s3,
    aws_accessanalyzer as accessanalyzer,
)
from constructs import Construct


class VitalStreamIamStack(Stack):
    """
    CAB-02: IAM & Zero-Trust
    SAA-C03 Domain 1 (Design Secure Architectures)

    Demonstrates, self-contained and ephemeral (no dependency on other CABs
    per the Time Capsule Rule):
      1. A Permission Boundary that caps the maximum privilege any App-Tier
         role can ever hold, even if its inline/managed policies are widened later.
      2. A least-privilege App-Tier role (identity-based policy) scoped to
         specific actions on specifically-tagged resources only.
      3. ABAC (Attribute-Based Access Control): the role can only be assumed
         by principals carrying the matching `Project` tag.
      4. A Zero-Trust S3 bucket policy (resource-based policy) that denies
         any request that isn't TLS and isn't a VitalStream-tagged principal.
      5. IAM Access Analyzer, to continuously flag any resource policy that
         grants access to a principal outside the account/zone of trust.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        project_tag = "VitalStream-Medical-Cloud"

        # 1. Permission Boundary: hard ceiling on App-Tier privilege.
        # SAA-C03: a boundary is the *maximum* a role can do -- its own
        # policies can only narrow that, never widen past the boundary.
        self.app_tier_boundary = iam.ManagedPolicy(
            self, "VitalStream-AppTier-Boundary",
            managed_policy_name="VitalStream-AppTier-Boundary",
            description="Max-permission ceiling for any VitalStream App-Tier role",
            statements=[
                iam.PolicyStatement(
                    sid="AllowScopedDataAndSecrets",
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "s3:GetObject",
                        "s3:PutObject",
                        "secretsmanager:GetSecretValue",
                    ],
                    resources=["*"],
                    conditions={
                        "StringEquals": {"aws:ResourceTag/Project": project_tag}
                    },
                ),
                iam.PolicyStatement(
                    sid="DenyIamAndOrgEscalation",
                    effect=iam.Effect.DENY,
                    actions=[
                        "iam:*",
                        "organizations:*",
                        "account:*",
                    ],
                    resources=["*"],
                ),
            ],
        )

        # 2. Least-Privilege App-Tier Role (identity-based policy).
        # SAA-C03: identity-based policy attached to the role/user/group,
        # as distinct from a resource-based policy (see the bucket below).
        self.app_tier_role = iam.Role(
            self, "VitalStream-App-Tier-Role",
            role_name="VitalStream-App-Tier-Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            description="Least-privilege role for App-Tier EC2 instances",
            permissions_boundary=self.app_tier_boundary,
        )
        self.app_tier_role.add_to_policy(
            iam.PolicyStatement(
                sid="ReadWritePhiScopedByTag",
                effect=iam.Effect.ALLOW,
                actions=["s3:GetObject", "s3:PutObject"],
                resources=["*"],
                conditions={
                    "StringEquals": {"aws:ResourceTag/Project": project_tag}
                },
            )
        )
        self.app_tier_role.add_to_policy(
            iam.PolicyStatement(
                sid="ReadSecretsScopedByTag",
                effect=iam.Effect.ALLOW,
                actions=["secretsmanager:GetSecretValue"],
                resources=["*"],
                conditions={
                    "StringEquals": {"aws:ResourceTag/Project": project_tag}
                },
            )
        )

        # 3. ABAC: only principals tagged for this project may assume the role.
        # SAA-C03: Attribute-Based Access Control scales least privilege
        # without hand-maintaining a role per resource.
        self.app_tier_role.assume_role_policy.add_statements(
            iam.PolicyStatement(
                sid="DenyAssumeWithoutProjectTag",
                effect=iam.Effect.DENY,
                principals=[iam.AnyPrincipal()],
                actions=["sts:AssumeRole"],
                conditions={
                    "StringNotEquals": {"aws:PrincipalTag/Project": project_tag}
                },
            )
        )

        # 4. Zero-Trust bucket: resource-based policy, deny-by-default posture.
        # SAA-C03: a bucket policy is a resource-based policy -- it applies
        # regardless of what identity-based policy the caller holds.
        self.zero_trust_bucket = s3.Bucket(
            self, "VitalStream-ZeroTrust-Bucket",
            bucket_name=f"vitalstream-zero-trust-{Stack.of(self).account}",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,  # Ephemeral lab: torn down after CAB-02
        )
        self.zero_trust_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                sid="DenyUntaggedPrincipals",
                effect=iam.Effect.DENY,
                principals=[iam.AnyPrincipal()],
                actions=["s3:*"],
                resources=[
                    self.zero_trust_bucket.bucket_arn,
                    f"{self.zero_trust_bucket.bucket_arn}/*",
                ],
                conditions={
                    "StringNotEquals": {"aws:PrincipalTag/Project": project_tag}
                },
            )
        )

        # 5. IAM Access Analyzer: continuously flags resource policies
        # (like the bucket policy above) that grant access beyond the
        # zone of trust -- an exam-relevant Domain 1 auditing control.
        self.access_analyzer = accessanalyzer.CfnAnalyzer(
            self, "VitalStream-Access-Analyzer",
            analyzer_name="VitalStream-ZeroTrust-Analyzer",
            type="ACCOUNT",
        )

        # Outputs
        CfnOutput(self, "AppTierRoleArn", value=self.app_tier_role.role_arn)
        CfnOutput(self, "ZeroTrustBucketArn", value=self.zero_trust_bucket.bucket_arn)
        CfnOutput(self, "AccessAnalyzerName", value=self.access_analyzer.analyzer_name)
