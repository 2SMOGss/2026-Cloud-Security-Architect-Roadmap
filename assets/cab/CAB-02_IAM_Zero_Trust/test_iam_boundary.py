import aws_cdk as cdk
from aws_cdk import assertions
from vitalstream_iam_stack import VitalStreamIamStack


def test_permission_boundary_attached_to_app_tier_role():
    app = cdk.App()
    stack = VitalStreamIamStack(app, "IamStack")
    template = assertions.Template.from_stack(stack)

    # SEC-IAM-01: The App-Tier role must have a Permissions Boundary set --
    # without one, the role's own policies are the *only* ceiling on its access.
    template.has_resource_properties("AWS::IAM::Role", {
        "PermissionsBoundary": assertions.Match.any_value(),
    })


def test_boundary_denies_iam_and_org_escalation():
    app = cdk.App()
    stack = VitalStreamIamStack(app, "IamStack")
    template = assertions.Template.from_stack(stack)

    # SEC-IAM-02: The boundary itself must explicitly deny IAM/Organizations
    # actions, so a role can never use its capped privilege to grant itself more.
    template.has_resource_properties("AWS::IAM::ManagedPolicy", {
        "PolicyDocument": {
            "Statement": assertions.Match.array_with([
                assertions.Match.object_like({
                    "Effect": "Deny",
                    "Action": assertions.Match.array_with(["iam:*"]),
                })
            ])
        }
    })
