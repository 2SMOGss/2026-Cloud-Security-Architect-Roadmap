# 💰 S3 Lifecycle & Cost Optimization Audit

**Project**: VitalStream Medical Cloud
**Compliance Focus**: Cost-Optimized Architectures (SAA-C03 Domain 4)
**Status**: 🔲 Code scaffolded and locally verified. **Live AWS deployment/verification pending** — update this file with real proof once deployed (per the Manual Terminal Execution policy in `CONTEXT.md`).

## 🎯 Objective
Show two different cost strategies side by side, and a spend guardrail on top of both:
1. A **predictable** access pattern (medical imaging archive) using manual S3 lifecycle transitions.
2. An **unpredictable** access pattern using S3 Intelligent-Tiering, which removes the guesswork (and the retrieval-fee risk) at the cost of a small per-object monitoring fee.
3. An AWS Budget that alerts on **forecasted** spend, not just actual spend.

## 🏗️ Architecture Design (SAA-C03 Domain 4)
- **`VitalStream-Archive-Bucket`**: SSE-S3 (not SSE-KMS — no per-request key cost for archival data that doesn't need CMK-level audit control). Lifecycle: Standard → Standard-IA (30d) → Glacier (90d) → Glacier Deep Archive (180d). Noncurrent versions expire after 30 days. Incomplete multipart uploads abort after 7 days (a commonly missed cost leak).
- **`VitalStream-Intelligent-Bucket`**: objects move into S3 Intelligent-Tiering immediately — no manual transition schedule, no retrieval fee, small monitoring fee per object.
- **`VitalStream-Monthly-Lab-Budget`**: AWS Budget, `$50`/month, alerts at 80% of **forecasted** spend (not actual — catches a runaway trend before the bill actually lands).

## 🛠️ Design Notes / Tradeoffs
| Decision | Why |
| :--- | :--- |
| SSE-S3 instead of SSE-KMS on both buckets | This data doesn't need per-key rotation/audit (that's what CAB-03's CMKs are for) — SSE-KMS bills per API call, SSE-S3 does not. |
| Manual lifecycle vs Intelligent-Tiering | Manual tiering is cheaper when the access pattern is known and stable. Intelligent-Tiering wins when access is unpredictable, since a wrong manual guess triggers early-deletion or retrieval fees. |
| FORECASTED vs ACTUAL budget threshold | ACTUAL only fires after the money is already spent; FORECASTED fires on the trend, giving time to react before the month closes. |
| `budget_alert_email` passed via CDK context, not hardcoded | This file is committed to a public repo — a real email address doesn't belong in source control. |

## ✅ Local Verification (Completed)
- `python app.py` synthesizes without error.
- `pytest` — 5/5 tests passing:
  - Archive bucket has the Standard-IA → Glacier → Deep Archive transition chain.
  - Noncurrent version expiration is set to 30 days.
  - Incomplete multipart uploads abort after 7 days.
  - Intelligent-Tiering bucket transitions objects immediately.
  - Monthly budget exists with a FORECASTED 80% threshold and email subscriber.

## ⏳ Pending Live Verification (do this next)
Follow `LAB_GUIDE.md` to deploy, then replace this section with real output:
1. `cdk deploy -c budget_alert_email=<your-email>` succeeds; confirm the SNS/email subscription confirmation arrives.
2. Upload a test object to each bucket, then check the console/CLI for the `LifecycleConfiguration` actually attached.
3. (Optional, needs Business/Enterprise support) Cross-check AWS Trusted Advisor's cost-optimization checks against what this stack already does — Trusted Advisor isn't provisioned by CDK, it's a support-plan feature you review manually.
4. `cdk destroy` to keep the lab ephemeral, and paste the exit code here.
