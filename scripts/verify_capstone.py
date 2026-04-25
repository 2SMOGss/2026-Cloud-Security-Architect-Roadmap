import boto3
import requests
import sys

def audit_guardrails(client, account_id):
    print(f"[*] Auditing Guardrails for Account {account_id}...")
    response = client.describe_budgets(AccountId=account_id)
    budgets = response.get('Budgets', [])
    for b in budgets:
        if b['BudgetName'] == 'VitalStream-Budget':
            print("  [+] VitalStream-Budget found.")
            return True
    raise Exception("VitalStream-Budget not found")

def audit_storage(s3_client, cf_client, bucket_name):
    print(f"[*] Auditing Storage: {bucket_name}...")
    # 1. Public Access Block Check
    pab = s3_client.get_public_access_block(Bucket=bucket_name)
    config = pab['PublicAccessBlockConfiguration']
    if not all([config['BlockPublicAcls'], config['IgnorePublicAcls'], 
                config['BlockPublicPolicy'], config['RestrictPublicBuckets']]):
        raise Exception("Public access block not fully enabled")
    print("  [+] Public Access Block fully enabled.")

    # 2. Encryption Check
    enc = s3_client.get_bucket_encryption(Bucket=bucket_name)
    rules = enc['ServerSideEncryptionConfiguration']['Rules']
    if not any(r['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] in ['AES256', 'aws:kms'] for r in rules):
        raise Exception("Bucket encryption not set to HIPAA-compliant standard")
    print("  [+] S3 Encryption verified (AES256/KMS).")
    return True

def audit_data(rds_client, db_instance_id):
    print(f"[*] Auditing Data Tier: {db_instance_id}...")
    res = rds_client.describe_db_instances(DBInstanceIdentifier=db_instance_id)
    db = res['DBInstances'][0]

    # 1. Multi-AZ Check
    if not db.get('MultiAZ', False):
        raise Exception("Multi-AZ is not enabled for the database")
    print("  [+] Multi-AZ High Availability verified.")

    # 2. Encryption Check
    if not db.get('StorageEncrypted', False):
        raise Exception("RDS Storage is not encrypted")
    print("  [+] RDS Storage Encryption verified.")

    # 3. Engine Compliance
    if db['Engine'] != 'postgres' or float(db['EngineVersion'].split('.')[0]) < 15:
        raise Exception(f"RDS Engine {db['Engine']} v{db['EngineVersion']} is not compliant")
    print(f"  [+] RDS Engine verified: {db['Engine']} v{db['EngineVersion']}")
    return True

def audit_compute(alb_client, asg_client, alb_name, asg_name):
    print(f"[*] Auditing Compute Tier: ALB={alb_name}, ASG={asg_name}...")
    # 1. ASG MinSize Check (High Availability)
    res_asg = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    asg = res_asg['AutoScalingGroups'][0]
    if asg['MinSize'] < 2:
        raise Exception(f"ASG MinSize is less than 2 (Actual: {asg['MinSize']})")
    print(f"  [+] ASG HA capacity verified (MinSize: {asg['MinSize']}).")

    # 2. ALB Visibility Check
    res_alb = alb_client.describe_load_balancers(Names=[alb_name])
    alb = res_alb['LoadBalancers'][0]
    if alb['Scheme'] != 'internet-facing':
        raise Exception(f"ALB is not internet-facing (Actual: {alb['Scheme']})")
    print("  [+] ALB visibility verified (internet-facing).")
    return True

def test_endpoint(url):
    print(f"[*] Chaos Hook: Testing endpoint {url}...")
    res = requests.get(url, timeout=10)
    if res.status_code != 200:
        raise Exception(f"Endpoint returned status code {res.status_code}")
    print(f"  [+] Endpoint Health Check: 200 OK")
    return True

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🛡️  VITALSTREAM SENTINEL: THE DEAN'S AUDIT (CAB-06)")
    print("="*50 + "\n")

    # Configuration (Dynamic from CFN)
    ACCOUNT_ID = "570435244246"
    S3_BUCKET = "vitalstream-storage-vitalstreamstaticassets454f463-vu2ee2jzl4jx"
    RDS_ID = "vitalstream-rds-vitalstreamdb63c04ccb-pcoukmitqjn8"
    ALB_NAME = "VitalS-Vital-i0HZKxk8FQca"
    ASG_NAME = "VitalStream-Compute-VitalStreamASGA69A77FE-1s6R3aBgqIVp"
    ALB_URL = "http://VitalS-Vital-i0HZKxk8FQca-2095253827.us-east-1.elb.amazonaws.com"

    # Clients
    session = boto3.Session(region_name="us-east-1")
    budgets = session.client('budgets')
    s3 = session.client('s3')
    cf = session.client('cloudfront')
    rds = session.client('rds')
    elbv2 = session.client('elbv2')
    asg = session.client('autoscaling')

    try:
        audit_guardrails(budgets, ACCOUNT_ID)
        audit_storage(s3, cf, S3_BUCKET)
        audit_data(rds, RDS_ID)
        audit_compute(elbv2, asg, ALB_NAME, ASG_NAME)
        test_endpoint(ALB_URL)
        
        print("\n" + "="*50)
        print("✅ AUDIT COMPLETE: ALL COMPLIANCE GATES PASSED")
        print("="*50 + "\n")
    except Exception as e:
        print(f"\n❌ AUDIT FAILED: {str(e)}")
        sys.exit(1)
