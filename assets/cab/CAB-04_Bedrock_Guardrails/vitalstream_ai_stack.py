from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_bedrock as bedrock,
)
from constructs import Construct

class VitalStreamAiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ARCHITECT: Lookup VPC within the Stack scope (Required for JSII)
        vpc = ec2.Vpc.from_lookup(self, "VPC",
            tags={"Project": "VitalStream-Medical-Cloud"}
        )

        # 1. IAM Role: The "VitalStream-AI-Invoker" (Least Privilege)
        self.ai_role = iam.Role(self, "VitalStream-AI-Invoker",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            description="Role allowed to invoke Bedrock from the Medical VPC App Tier"
        )

        # 2. Security Group for the VPC Endpoint (Interface)
        # SAA-C03: Inbound HTTPS (443) from the App Tier subnets
        self.endpoint_sg = ec2.SecurityGroup(self, "Bedrock-Endpoint-SG",
            vpc=vpc,
            description="Security Group for Bedrock PrivateLink Endpoint",
            allow_all_outbound=True
        )
        self.endpoint_sg.add_ingress_rule(
            ec2.Peer.ipv4(vpc.vpc_cidr_block), 
            ec2.Port.tcp(443),
            "Allow HTTPS from within VPC"
        )

        # 3. Interface VPC Endpoint (Amazon Bedrock Runtime)
        # SAA-C03: Bypasses Public Internet / NAT Gateway for HIPAA compliance
        self.bedrock_endpoint = ec2.InterfaceVpcEndpoint(self, "Bedrock-VPC-Endpoint",
            vpc=vpc,
            service=ec2.InterfaceVpcEndpointService("com.amazonaws.us-east-2.bedrock-runtime"),
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS), # App Tier
            security_groups=[self.endpoint_sg],
            open=False # Locked down by Guardrail
        )

        # 4. Zero-Trust Endpoint Policy (The "Gate")
        self.bedrock_endpoint.add_to_policy(
            iam.PolicyStatement(
                principals=[iam.ArnPrincipal(self.ai_role.role_arn)],
                actions=["bedrock:InvokeModel"],
                resources=[
                    "arn:aws:bedrock:us-east-2::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
                    "arn:aws:bedrock:us-east-2::inference-profile/us.anthropic.claude-3-haiku-20240307-v1:0"
                ],
                effect=iam.Effect.ALLOW
            )
        )

        # 5. Bedrock Guardrail: The "VitalStream-Shield"
        # SAA-C03: Redacts PII/PHI and blocks harmful content in medical prompts
        self.guardrail = bedrock.CfnGuardrail(self, "VitalStream-PHI-Guardrail",
            name="VitalStream-Shield",
            description="HIPAA compliant guardrail for PII/PHI redaction",
            content_policy_config=bedrock.CfnGuardrail.ContentPolicyConfigProperty(
                filters_config=[
                    bedrock.CfnGuardrail.ContentFilterConfigProperty(
                        type="HATE", input_strength="HIGH", output_strength="HIGH"
                    ),
                    bedrock.CfnGuardrail.ContentFilterConfigProperty(
                        type="INSULTS", input_strength="HIGH", output_strength="HIGH"
                    )
                ]
            ),
            sensitive_information_policy_config=bedrock.CfnGuardrail.SensitiveInformationPolicyConfigProperty(
                pii_entities_config=[
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="US_SOCIAL_SECURITY_NUMBER", action="BLOCK"),
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="EMAIL", action="BLOCK"),
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="NAME", action="BLOCK"),
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="ADDRESS", action="BLOCK"), 
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="PHONE", action="BLOCK")
                ]
            ),
            blocked_input_messaging="🚨 Safety Guardrail Triggered: Request blocked for PII/PHI protection.",
            blocked_outputs_messaging="🚨 Safety Guardrail Triggered: Output blocked for PHI protection."
        )

        # 6. Version the Guardrail for Production
        self.guardrail_version = bedrock.CfnGuardrailVersion(self, "VitalStream-Guardrail-Version",
            guardrail_identifier=self.guardrail.attr_guardrail_id,
            description="Initial HIPAA compliant version"
        )
        
        # 7. ARCHITECT OUTPUTS: For Verification Step
        from aws_cdk import CfnOutput
        CfnOutput(self, "GuardrailName", value=self.guardrail.name)
        CfnOutput(self, "GuardrailId", value=self.guardrail.attr_guardrail_id)
        CfnOutput(self, "GuardrailVersion", value=self.guardrail_version.attr_version)
