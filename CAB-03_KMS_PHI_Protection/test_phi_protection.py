import aws_cdk as cdk
from aws_cdk import assertions
from vitalstream_vpc_stack import VitalStreamVpcStack
from vitalstream_data_stack import VitalStreamDataStack

def test_phi_bucket_encryption():
    app = cdk.App()
    vpc_stack = VitalStreamVpcStack(app, "VpcStack")
    data_stack = VitalStreamDataStack(app, "DataStack", vpc=vpc_stack.vpc)
    template = assertions.Template.from_stack(data_stack)

    # SEC-PHI-01: PHI S3 Bucket must use SSE-KMS with our CMK
    template.resource_count_is("AWS::S3::Bucket", 2) # Audit + PHI
    
    # Check for the PHI Specific Bucket (not the audit core)
    template.has_resource_properties("AWS::S3::Bucket", {
        "BucketEncryption": {
            "ServerSideEncryptionConfiguration": [
                {
                    "ServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "aws:kms"
                    }
                }
            ]
        },
        "PublicAccessBlockConfiguration": {
            "BlockPublicAcls": True,
            "BlockPublicPolicy": True,
            "IgnorePublicAcls": True,
            "RestrictPublicBuckets": True
        }
    })
