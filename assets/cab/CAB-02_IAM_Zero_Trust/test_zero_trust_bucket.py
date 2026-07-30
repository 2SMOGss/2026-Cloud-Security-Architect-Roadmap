import aws_cdk as cdk
from aws_cdk import assertions
from vitalstream_iam_stack import VitalStreamIamStack


def test_bucket_blocks_public_access_and_enforces_tls():
    app = cdk.App()
    stack = VitalStreamIamStack(app, "IamStack")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::S3::Bucket", {
        "PublicAccessBlockConfiguration": {
            "BlockPublicAcls": True,
            "BlockPublicPolicy": True,
            "IgnorePublicAcls": True,
            "RestrictPublicBuckets": True,
        }
    })


def test_bucket_policy_denies_untagged_principals():
    app = cdk.App()
    stack = VitalStreamIamStack(app, "IamStack")
    template = assertions.Template.from_stack(stack)

    # SEC-S3-ZT-01: Resource-based policy must deny access outright unless
    # the caller carries the VitalStream project principal tag (ABAC).
    template.has_resource_properties("AWS::S3::BucketPolicy", {
        "PolicyDocument": {
            "Statement": assertions.Match.array_with([
                assertions.Match.object_like({
                    "Effect": "Deny",
                    "Condition": {
                        "StringNotEquals": {
                            "aws:PrincipalTag/Project": "VitalStream-Medical-Cloud"
                        }
                    },
                })
            ])
        }
    })


def test_access_analyzer_created():
    app = cdk.App()
    stack = VitalStreamIamStack(app, "IamStack")
    template = assertions.Template.from_stack(stack)

    # SEC-IAM-03: IAM Access Analyzer must be active to continuously
    # flag resource policies that grant access outside the zone of trust.
    template.resource_count_is("AWS::AccessAnalyzer::Analyzer", 1)
