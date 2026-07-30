# ⚡ Serverless Decoupling & Performance Audit

**Project**: VitalStream Medical Cloud
**Compliance Focus**: High-Performing Architectures (SAA-C03 Domain 3)
**Status**: 🔲 Code scaffolded and locally verified. **Live AWS deployment/verification pending** — update this file with real proof once deployed (per the Manual Terminal Execution policy in `CONTEXT.md`).

## 🎯 Objective
Show two distinct decoupling shapes plus one performance technique, all of which show up as separate exam concepts even though they're often confused with each other:
1. **Point-to-point decoupling** (SQS) — a buffer between producer and consumer so a traffic spike doesn't hit the consumer directly.
2. **Pub/sub decoupling** (EventBridge) — a publisher raises an event without knowing (or caring) who's subscribed.
3. **Edge caching** (CloudFront + private S3 via OAC) — static assets served from edge locations instead of the origin on every request.

## 🏗️ Architecture Design (SAA-C03 Domain 3)
- **`vitalstream-ingest-queue`**: buffers device-telemetry ingestion. Visibility timeout = 180s (6x the consumer's 30s Lambda timeout) so a message isn't redelivered to a second worker while the first is still processing it. Backed by `vitalstream-ingest-dlq` after 3 failed receives.
- **`VitalStream-Ingest-Consumer`**: SQS-triggered Lambda with `reserved_concurrent_executions=5` — caps parallel invocations so a queue backlog can't overwhelm whatever this function calls downstream.
- **`vitalstream-events`**: custom EventBridge bus, isolated from the noisy default bus. A rule matches `source=vitalstream.records`, `detail-type=PatientRecordUpdated` and fans out to `VitalStream-Event-Subscriber` — the publisher never calls the subscriber directly.
- **CloudFront distribution**: fronts a fully private S3 bucket (`BLOCK_ALL` public access) via Origin Access Control — the bucket itself is never public, only reachable through the distribution.

## 🛠️ Design Notes / Tradeoffs
| Decision | Why |
| :--- | :--- |
| Visibility timeout = 6x consumer timeout | AWS's own guidance to avoid double-processing: if the consumer is still working when the timeout expires, SQS makes the message visible again and a second worker could pick it up. |
| Reserved concurrency instead of unbounded scaling | Domain 3 isn't just "make it fast" — it's also "don't let a spike take down something slower downstream." Reserved concurrency is the throttle. |
| EventBridge bus+rule vs. calling the subscriber Lambda directly | Direct invocation is tight coupling — adding a second subscriber later means changing the publisher's code. A bus+rule needs zero publisher changes to add subscribers. |
| OAC instead of a public bucket + public CloudFront | The exam explicitly tests "should this bucket ever be public" — the answer for anything behind CloudFront is no, use Origin Access Control. |

## ✅ Local Verification (Completed)
- `python app.py` synthesizes without error.
- `pytest` — 6/6 tests passing:
  - Ingest queue has a DLQ redrive policy (`maxReceiveCount: 3`).
  - Ingest queue visibility timeout is 180s.
  - Consumer Lambda has `ReservedConcurrentExecutions: 5`.
  - Custom EventBridge bus + rule exist with the expected event pattern.
  - Portal bucket blocks all public access.
  - CloudFront distribution redirects viewer traffic to HTTPS.

## ⏳ Pending Live Verification (do this next)
Follow `LAB_GUIDE.md` to deploy, then replace this section with real output:
1. `cdk deploy` succeeds; note the queue URL, DLQ URL, event bus name, and CloudFront domain from the outputs.
2. Send a test message to the ingest queue and confirm the consumer Lambda's CloudWatch Logs show it processing.
3. Send a malformed message that will fail 3 times and confirm it lands in the DLQ.
4. Put a test event on the custom bus (`aws events put-events`) with `source=vitalstream.records`, `detail-type=PatientRecordUpdated` and confirm the subscriber Lambda's logs show it firing.
5. Upload a test file to the portal bucket and fetch it through the CloudFront domain — confirm a direct S3 URL request is denied (proving OAC is actually enforced) while the CloudFront URL works.
6. `cdk destroy` to keep the lab ephemeral, and paste the exit code here.
