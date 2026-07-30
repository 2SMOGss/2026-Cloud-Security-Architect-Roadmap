import aws_cdk as cdk
from aws_cdk import assertions
from vitalstream_cost_stack import VitalStreamCostStack


def test_monthly_budget_created_with_forecast_alert():
    app = cdk.App()
    stack = VitalStreamCostStack(app, "CostStack")
    template = assertions.Template.from_stack(stack)

    # COST-BUDGET-01: a forecasted-spend alert, distinct from Cost Explorer
    # (historical analysis) and Trusted Advisor (specific idle-resource checks)
    template.has_resource_properties("AWS::Budgets::Budget", {
        "Budget": assertions.Match.object_like({
            "BudgetType": "COST",
            "TimeUnit": "MONTHLY",
            "BudgetLimit": {"Amount": 50, "Unit": "USD"},
        }),
        "NotificationsWithSubscribers": assertions.Match.array_with([
            assertions.Match.object_like({
                "Notification": assertions.Match.object_like({
                    "NotificationType": "FORECASTED",
                    "ComparisonOperator": "GREATER_THAN",
                    "Threshold": 80,
                }),
            })
        ]),
    })
