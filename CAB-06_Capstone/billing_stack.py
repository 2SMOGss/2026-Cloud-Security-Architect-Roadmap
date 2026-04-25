from aws_cdk import (
    Stack,
    aws_budgets as budgets,
    aws_cloudwatch as cw,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
)
from constructs import Construct

class VitalStreamBillingStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # 1. Create SNS Topic for Alerts
        topic = sns.Topic(self, "BudgetAlertTopic", 
            display_name="VitalStream Budget Alerts"
        )
        
        # Note: In a real scenario, we'd add a subscription here.
        # topic.add_subscription(subscriptions.EmailSubscription("your-email@example.com"))

        # 2. Implement $30 Monthly Budget
        budgets.CfnBudget(self, "MonthlyBudget",
            budget=budgets.CfnBudget.BudgetDataProperty(
                budget_limit=budgets.CfnBudget.SpendProperty(
                    amount=30,
                    unit="USD"
                ),
                budget_type="COST",
                time_unit="MONTHLY"
            ),
            notifications_with_subscribers=[
                budgets.CfnBudget.NotificationWithSubscribersProperty(
                    notification=budgets.CfnBudget.NotificationProperty(
                        comparison_operator="GREATER_THAN",
                        notification_type="ACTUAL",
                        threshold=80,  # Alert at 80% ($24)
                        threshold_type="PERCENTAGE"
                    ),
                    subscribers=[
                        budgets.CfnBudget.SubscriberProperty(
                            address=topic.topic_arn,
                            subscription_type="SNS"
                        )
                    ]
                )
            ]
        )

        # 3. Implement $1 Billing Alarm (CloudWatch)
        # Note: Billing alarms must be in us-east-1
        cw.Alarm(self, "BillingAlarmLowThreshold",
            metric=cw.Metric(
                namespace="AWS/Billing",
                metric_name="EstimatedCharges",
                dimensions_map={"Currency": "USD"}
            ),
            threshold=1,
            evaluation_periods=1,
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_THRESHOLD,
            alarm_description="Alert when charges exceed $1"
        )
