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

def test_audit_storage_fails_if_public_access_allowed(mocker):
    from verify_capstone import audit_storage
    s3_mock = Mock()
    cf_mock = Mock()
    
    # Mock public access block partially disabled
    s3_mock.get_public_access_block.return_value = {
        'PublicAccessBlockConfiguration': {
            'BlockPublicAcls': False,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }
    }
    
    with pytest.raises(Exception, match="Public access block not fully enabled"):
        audit_storage(s3_mock, cf_mock, bucket_name='test-bucket')

def test_audit_storage_passes_if_secure(mocker):
    from verify_capstone import audit_storage
    s3_mock = Mock()
    cf_mock = Mock()
    
    s3_mock.get_public_access_block.return_value = {
        'PublicAccessBlockConfiguration': {
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }
    }
    s3_mock.get_bucket_encryption.return_value = {
        'ServerSideEncryptionConfiguration': {
            'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]
        }
    }
    
    assert audit_storage(s3_mock, cf_mock, bucket_name='test-bucket') is True

def test_audit_data_fails_if_single_az(mocker):
    from verify_capstone import audit_data
    rds_mock = Mock()
    
    rds_mock.describe_db_instances.return_value = {
        'DBInstances': [{
            'DBInstanceIdentifier': 'test-db',
            'MultiAZ': False,
            'StorageEncrypted': True,
            'Engine': 'postgres',
            'EngineVersion': '15.4'
        }]
    }
    
    with pytest.raises(Exception, match="Multi-AZ is not enabled"):
        audit_data(rds_mock, 'test-db')

def test_audit_data_passes_if_resilient(mocker):
    from verify_capstone import audit_data
    rds_mock = Mock()
    
    rds_mock.describe_db_instances.return_value = {
        'DBInstances': [{
            'DBInstanceIdentifier': 'test-db',
            'MultiAZ': True,
            'StorageEncrypted': True,
            'Engine': 'postgres',
            'EngineVersion': '15.4'
        }]
    }
    
    assert audit_data(rds_mock, 'test-db') is True

def test_audit_compute_fails_if_low_capacity(mocker):
    from verify_capstone import audit_compute
    asg_mock = Mock()
    alb_mock = Mock()
    
    asg_mock.describe_auto_scaling_groups.return_value = {
        'AutoScalingGroups': [{
            'AutoScalingGroupName': 'test-asg',
            'MinSize': 1,
        }]
    }
    
    with pytest.raises(Exception, match="ASG MinSize is less than 2"):
        audit_compute(alb_mock, asg_mock, 'test-alb', 'test-asg')

def test_audit_compute_passes_if_scaled(mocker):
    from verify_capstone import audit_compute
    asg_mock = Mock()
    alb_mock = Mock()
    
    asg_mock.describe_auto_scaling_groups.return_value = {
        'AutoScalingGroups': [{
            'AutoScalingGroupName': 'test-asg',
            'MinSize': 2,
        }]
    }
    alb_mock.describe_load_balancers.return_value = {
        'LoadBalancers': [{
            'LoadBalancerName': 'test-alb',
            'Scheme': 'internet-facing'
        }]
    }
    
    assert audit_compute(alb_mock, asg_mock, 'test-alb', 'test-asg') is True

def test_test_endpoint_success(mocker):
    from verify_capstone import test_endpoint
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.status_code = 200
    
    assert test_endpoint('http://test-url.com') is True
