# ✅ Master Plan & Progress Tracker

Canonical roadmap detail lives in [`roadmap-v3.2.md`](./roadmap-v3.2.md). This file tracks live status — update it as CABs move, don't let it drift like the old `CONTEXT.md` did.

## CAB Progress (SAA-C03 Domain Coverage)

| CAB | Focus | Exam Domain | Status |
| :--- | :--- | :--- | :--- |
| CAB-01 | VPC Plumbing & CLI | Domain 1 | ✅ Complete |
| CAB-02 | IAM & Zero-Trust | Domain 1 | 🟡 Built, pending live AWS verification (see its `LAB_GUIDE.md`) |
| CAB-03 | KMS & PHI Protection | Domain 1 | ✅ Complete |
| CAB-04 | Bedrock & Guardrails | Domain 1 | ✅ Complete |
| CAB-05 | High Availability | Domain 2 | ✅ Complete |
| CAB-06 | S3 Lifecycle & Cost Optimization | Domain 4 | 🟡 Built, pending live AWS verification (see its `LAB_GUIDE.md`) |
| CAB-07 | Serverless Decoupling | Domain 3 | 🟡 Built, pending live AWS verification (see its `LAB_GUIDE.md`) |
| CAB-08 | Cert Prep & Portfolio Launch | All | 🔲 Not started |

## Exam Domain Coverage at a Glance

| Domain | Weight | Labs Covering It | Status |
| :--- | :--- | :--- | :--- |
| Domain 1: Secure Architectures | ~30% | CAB-01, 02, 03, 04 | 3 of 4 done, 1 built pending live verification |
| Domain 2: Resilient Architectures | ~26% | CAB-05 | Done |
| Domain 3: High-Performing Architectures | ~24% | CAB-07 | Built, pending live verification |
| Domain 4: Cost-Optimized Architectures | ~20% | CAB-06 | Built, pending live verification |

**Priority order:** Deploy & verify CAB-02, CAB-06, and CAB-07 (all three are built, code ready) → CAB-08 (Final Blitz). Every exam domain now has code; the only thing left is real deployment/verification and the cert-prep pass.

## Repo Sync Checklist

- [x] Reconcile README.md / roadmap-v3.2.md / MINDMAP.md into one canonical table
- [x] Fix dead `TODO.md` link (this file)
- [x] Fix `saa-quizmaster` broken question-bank path
- [x] Fix mojibake in tracked markdown files
- [x] Redact real AWS resource IDs from `AUDIT.md`
- [x] Refresh `CONTEXT.md` status tracker
- [x] Update `CONTRIBUTING.md` for the CAB-XX/`assets/cab/` convention
- [x] Repair the corrupted `.gitignore` tail (UTF-16 garbage lines)

## Phase 6: Portfolio Extensions (Optional, Post-Cert)

- [ ] CI/CD automation (GitHub Actions deploy/destroy pipeline)
- [ ] Data ingestion lab (Kinesis + Glue)
- [ ] SageMaker/ML network isolation lab
