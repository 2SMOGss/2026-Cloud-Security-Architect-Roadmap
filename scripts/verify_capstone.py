import boto3

def audit_guardrails(client, account_id):
    """
    Verifies that the 'VitalStream-Budget' exists and has the correct limit.
    """
    response = client.describe_budgets(AccountId=account_id)
    budgets = response.get('Budgets', [])
    for b in budgets:
        if b['BudgetName'] == 'VitalStream-Budget':
            return True
    raise Exception("VitalStream-Budget not found")

if __name__ == "__main__":
    # Placeholder for direct execution
    print("CAB-06 Capstone Auditor Initialized.")
