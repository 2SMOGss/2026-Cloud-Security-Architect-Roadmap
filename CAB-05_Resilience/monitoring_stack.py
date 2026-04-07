from aws_cdk import (
    Stack,
    aws_cloudwatch as cloudwatch,
    Tags
)
from constructs import Construct

class VitalStreamMonitoringStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Financial Guardrail: Billing Alarm
        # This monitors EstimatedCharges for the current month
        # Note: Billing metrics are only available in us-east-1
        self.cost_alarm = cloudwatch.CfnAlarm(
            self, "VitalStream-BillingAlarm",
            alarm_name="VitalStream-CAB05-BillingAlarm",
            alarm_description="Alarm when estimated charges exceed $10",
            namespace="AWS/Billing",
            metric_name="EstimatedCharges",
            dimensions=[{"name": "Currency", "value": "USD"}],
            statistic="Maximum",
            period=21600, # 6 hours (standard for billing metrics)
            evaluation_periods=1,
            threshold=10, # $10 threshold
            comparison_operator="GreaterThanThreshold",
        )
        
        Tags.of(self).add("Monitoring", "Financial")
