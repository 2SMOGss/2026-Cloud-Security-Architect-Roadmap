# 🧪 CAB-07 Lab Guide: Serverless Decoupling & Performance

Self-contained — no dependency on CAB-01/02/03/04/05/06 resources. Safe to deploy and destroy on its own.

## Step 1: Set up the environment
```bash
cd assets/cab/CAB-07_Serverless_Performance
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2: Run the unit tests (no AWS credentials needed)
```bash
pytest -v
```
Expect 6 passed — this only checks the synthesized CloudFormation, it does not touch your AWS account.

## Step 3: Deploy
```bash
cdk bootstrap   # only if this account/region hasn't been bootstrapped before
cdk deploy
```
CloudFront distributions take 10-15 minutes to fully deploy the first time — that's normal. Paste the CLI output (including the four `CfnOutput` values) back so it can be recorded in `AUDIT.md`.

## Step 4: Verify the decoupling and caching manually
```bash
# Send a normal message
aws sqs send-message --queue-url <IngestQueueUrl> --message-body '{"device_id": "abc123", "reading": 98.6}'

# Check the consumer Lambda's logs a minute later
aws logs tail /aws/lambda/<consumer-function-name> --since 5m

# Publish a domain event on the custom bus
aws events put-events --entries '[{
  "Source": "vitalstream.records",
  "DetailType": "PatientRecordUpdated",
  "EventBusName": "vitalstream-events",
  "Detail": "{\"patientId\": \"p-001\"}"
}]'

# Check the subscriber Lambda's logs
aws logs tail /aws/lambda/<subscriber-function-name> --since 5m
```
Then upload a test object to the portal bucket and fetch it via `https://<DistributionDomainName>/<key>` — it should succeed. Try fetching the same object directly from the S3 URL — it should be denied, proving CloudFront's Origin Access Control is the only path in.

## Step 5: Tear down (ephemeral lab rule)
```bash
cdk destroy
```
Paste the exit code/confirmation back so `AUDIT.md` can be marked complete.
