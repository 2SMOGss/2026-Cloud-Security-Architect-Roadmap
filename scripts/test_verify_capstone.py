import pytest
from unittest.mock import Mock
import sys
import os

# Add scripts directory to path for imports
sys.path.append(os.path.dirname(__file__))

def test_audit_guardrails_fails_if_budget_missing(mocker):
    # We'll import inside the test once the file exists
    from verify_capstone import audit_guardrails
    
    mock_client = Mock()
    mock_client.describe_budgets.return_value = {'Budgets': []}
    
    with pytest.raises(Exception, match="VitalStream-Budget not found"):
        audit_guardrails(mock_client, account_id='123456789012')

def test_audit_guardrails_passes_if_budget_exists(mocker):
    from verify_capstone import audit_guardrails
    
    mock_client = Mock()
    mock_client.describe_budgets.return_value = {
        'Budgets': [
            {
                'BudgetName': 'VitalStream-Budget',
                'BudgetLimit': {'Amount': '30.0'}
            }
        ]
    }
    
    assert audit_guardrails(mock_client, account_id='123456789012') is True
