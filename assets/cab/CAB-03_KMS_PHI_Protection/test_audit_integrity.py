import aws_cdk as cdk
from aws_cdk import assertions
from vitalstream_vpc_stack import VitalStreamVpcStack
from vitalstream_data_stack import VitalStreamDataStack

def test_audit_bucket_integrity():
    app = cdk.App()
    vpc_stack = VitalStreamVpcStack(app, "VpcStack")
    data_stack = VitalStreamDataStack(app, "DataStack", vpc=vpc_stack.vpc)
    template = assertions.Template.from_stack(data_stack)

    # SEC-S3-01: Audit Bucket must have Object Lock enabled & compliance mode
    template.has_resource_properties("AWS::S3::Bucket", {
        "ObjectLockEnabled": True,
        "ObjectLockConfiguration": {
            "ObjectLockEnabled": "Enabled",
            "Rule": {
                "DefaultRetention": {
                    "Mode": "COMPLIANCE"
                }
            }
        }
    })

    # SEC-S3-02: Audit Bucket must be encrypted with the Audit-Key (CMK)
    template.has_resource_properties("AWS::S3::Bucket", {
        "BucketEncryption": {
            "ServerSideEncryptionConfiguration": [
                {
                    "ServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "aws:kms"
                    }
                }
            ]
        }
    })
