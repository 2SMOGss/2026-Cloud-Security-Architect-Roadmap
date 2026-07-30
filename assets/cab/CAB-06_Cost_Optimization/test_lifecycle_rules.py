import aws_cdk as cdk
from aws_cdk import assertions
from vitalstream_cost_stack import VitalStreamCostStack


def test_archive_bucket_has_tiering_transitions():
    app = cdk.App()
    stack = VitalStreamCostStack(app, "CostStack")
    template = assertions.Template.from_stack(stack)

    # COST-S3-01: cold data must step down through IA -> Glacier -> Deep Archive
    template.has_resource_properties("AWS::S3::Bucket", {
        "LifecycleConfiguration": {
            "Rules": assertions.Match.array_with([
                assertions.Match.object_like({
                    "Id": "TierDownColdData",
                    "Status": "Enabled",
                    "Transitions": assertions.Match.array_with([
                        assertions.Match.object_like({"StorageClass": "STANDARD_IA"}),
                        assertions.Match.object_like({"StorageClass": "GLACIER"}),
                        assertions.Match.object_like({"StorageClass": "DEEP_ARCHIVE"}),
                    ]),
                })
            ])
        }
    })


def test_noncurrent_versions_expire():
    app = cdk.App()
    stack = VitalStreamCostStack(app, "CostStack")
    template = assertions.Template.from_stack(stack)

    # COST-S3-02: old versions must not accumulate storage cost forever
    template.has_resource_properties("AWS::S3::Bucket", {
        "LifecycleConfiguration": {
            "Rules": assertions.Match.array_with([
                assertions.Match.object_like({
                    "Id": "ExpireOldVersions",
                    "NoncurrentVersionExpiration": {"NoncurrentDays": 30},
                })
            ])
        }
    })


def test_incomplete_multipart_uploads_are_aborted():
    app = cdk.App()
    stack = VitalStreamCostStack(app, "CostStack")
    template = assertions.Template.from_stack(stack)

    # COST-S3-03: orphaned multipart uploads silently bill storage forever
    template.has_resource_properties("AWS::S3::Bucket", {
        "LifecycleConfiguration": {
            "Rules": assertions.Match.array_with([
                assertions.Match.object_like({
                    "Id": "AbortIncompleteMultipartUploads",
                    "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7},
                })
            ])
        }
    })


def test_intelligent_tiering_bucket_configured():
    app = cdk.App()
    stack = VitalStreamCostStack(app, "CostStack")
    template = assertions.Template.from_stack(stack)

    # COST-S3-04: unpredictable-access data should let S3 do the tiering
    template.has_resource_properties("AWS::S3::Bucket", {
        "LifecycleConfiguration": {
            "Rules": assertions.Match.array_with([
                assertions.Match.object_like({
                    "Id": "MoveToIntelligentTieringImmediately",
                    "Transitions": assertions.Match.array_with([
                        assertions.Match.object_like({"StorageClass": "INTELLIGENT_TIERING"}),
                    ]),
                })
            ])
        }
    })
