# 🧪 CAB-02 Lab Guide: IAM & Zero-Trust

Self-contained — no dependency on CAB-01/03/04 resources. Safe to deploy and destroy on its own.

## Step 1: Set up the environment
```bash
cd assets/cab/CAB-02_IAM_Zero_Trust
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
cdk deploy
```
Paste the CLI output (including the three `CfnOutput` values) back so it can be recorded in `AUDIT.md`.

## Step 4: Verify Zero-Trust manually
1. In the IAM console, confirm `VitalStream-App-Tier-Role` shows a Permissions Boundary of `VitalStream-AppTier-Boundary`.
2. Try to assume the App-Tier role from a principal that does **not** have a `Project=VitalStream-Medical-Cloud` tag — it should be denied.
3. Try `aws s3api get-object` against the `vitalstream-zero-trust-<account>` bucket using credentials without the matching principal tag — it should be denied even though no identity-based policy said "deny."
4. Open IAM Access Analyzer and confirm the `VitalStream-ZeroTrust-Analyzer` is active.

## Step 5: Tear down (ephemeral lab rule)
```bash
cdk destroy
```
Paste the exit code/confirmation back so `AUDIT.md` can be marked complete.
