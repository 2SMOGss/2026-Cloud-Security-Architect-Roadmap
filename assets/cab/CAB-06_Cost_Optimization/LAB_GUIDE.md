# 🧪 CAB-06 Lab Guide: S3 Lifecycle & Cost Optimization

Self-contained — no dependency on CAB-01/02/03/04/05 resources. Safe to deploy and destroy on its own.

## Step 1: Set up the environment
```bash
cd assets/cab/CAB-06_Cost_Optimization
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2: Run the unit tests (no AWS credentials needed)
```bash
pytest -v
```
Expect 5 passed — this only checks the synthesized CloudFormation, it does not touch your AWS account.

## Step 3: Deploy
```bash
cdk bootstrap   # only if this account/region hasn't been bootstrapped before
cdk deploy -c budget_alert_email=you@example.com
```
Use a real inbox — AWS Budgets sends an SNS/email subscription confirmation you must click before alerts will fire. Paste the CLI output back so it can be recorded in `AUDIT.md`.

## Step 4: Verify cost behavior manually
1. Upload a small test file to `vitalstream-cost-archive-<account>` and confirm in the S3 console that its lifecycle rule shows the Standard-IA → Glacier → Deep Archive schedule.
2. Upload a test file to `vitalstream-cost-intelligent-<account>` and confirm it shows `INTELLIGENT_TIERING` as its storage class shortly after upload.
3. In AWS Budgets, confirm `VitalStream-Monthly-Lab-Budget` exists with an 80%-forecasted alert threshold.
4. (Optional) If your account has Business/Enterprise support, compare against AWS Trusted Advisor's cost-optimization checks — Trusted Advisor isn't something CDK provisions, it's a console/API feature you review.

## Step 5: Tear down (ephemeral lab rule)
```bash
cdk destroy
```
Paste the exit code/confirmation back so `AUDIT.md` can be marked complete.
