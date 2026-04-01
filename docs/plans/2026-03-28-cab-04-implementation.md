# CAB-04: AI & Guardrails - Live Sentinel Deployment

> **For Antigravity:** This implementation plan follows the **writing-plans** skill.

**Goal:** Correct the AI Sentinel infrastructure to link with the existing Medical VPC and deploy Bedrock Guardrails.

**Architecture:**
- Use `ec2.Vpc.from_lookup` to connect to the CAB-01 VPC via tags.
- Deploy an Interface VPC Endpoint for Amazon Bedrock.
- Implement a HIPAA-compliant Guardrail (VitalStream-Shield) for PII redaction.

---

### Task 1: Environment & Code Refactor

**Files:**
- Modify: `CAB-04_Bedrock_Guardrails/app.py`
- Modify: `CAB-04_Bedrock_Guardrails/vitalstream_ai_stack.py`
- Modify: `CAB-04_Bedrock_Guardrails/ai_protocol_assistant.py`

**Step 1: Update app.py for VPC Lookup**
- Add environment context (account/region).
- Implement VPC lookup via tags.

**Step 2: Fix Guardrail Typo & Add Outputs**
- Fix `ADRESS` -> `ADDRESS` in `vitalstream_ai_stack.py`.
- Add `CfnOutput` for Guardrail ID and Version.

**Step 3: Fix Test Client Case Sensitivity**
- Update `guardrailIdentifier` to 'VitalStream-Shield' in `ai_protocol_assistant.py`.

### Task 2: CDK Deployment

**Commands:**
```bash
cd CAB-04_Bedrock_Guardrails
cdk bootstrap
cdk deploy
```

### Task 3: Security Verification

**Commands:**
```bash
python ai_protocol_assistant.py
```
**Expected Outcome:** The PII in the prompt (MRN-123456789) should trigger the guardrail or be redacted if configured to block/mask.
