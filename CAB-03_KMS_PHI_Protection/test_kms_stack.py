import aws_cdk as cdk
from aws_cdk import assertions
from vitalstream_vpc_stack import VitalStreamVpcStack
from vitalstream_data_stack import VitalStreamDataStack

def test_kms_rotation_enabled():
    app = cdk.App()
    vpc_stack = VitalStreamVpcStack(app, "VpcStack")
    data_stack = VitalStreamDataStack(app, "DataStack", vpc=vpc_stack.vpc)
    template = assertions.Template.from_stack(data_stack)

    # SEC-KMS-01: Ensure All Customer Managed Keys have rotation enabled
    template.resource_count_is("AWS::KMS::Key", 4) # S3, RDS, EBS, Audit
    template.has_resource_properties("AWS::KMS::Key", {
        "EnableKeyRotation": True
    })
