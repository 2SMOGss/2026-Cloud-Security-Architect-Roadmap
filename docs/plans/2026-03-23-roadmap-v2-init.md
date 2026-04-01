# Roadmap V2 Initialization Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Refactor the project structure to support the 16-week AI-First, CDK-centric, and low-cost "Ephemeral Architect" approach.

**Architecture:** Transition from many slow bash-based weeks to 8 high-intensity "Architecture Blocks" focused on IaC (CDK) and AI (Bedrock). All labs will follow a spin-up/tear-down/document (BiP) cycle.

**Tech Stack:** AWS CDK (Python), Markdown, Git.

---

### Task 1: Protocol & Rule Update
**Files:**
- Modify: `CONTEXT.md`

**Step 1: Update CONTEXT.md with Golden Rules**
Add the following "Ephemeral Architect" and "BiP" rules to the "Technical Strategy" section.

```markdown
## 🛡️ The Mentors "Ephemeral Architect" Protocol (Golden Rules)
1. **Low-Cost Ephemerality:** All labs must be "spun up" for learning and "torn down" (cdk destroy) immediately after. No resources left running.
2. **IaC First:** AWS CDK (Python) is the mandatory standard. No more manual console or bash-only infrastructure.
3. **Build in Public (BiP):** Documentation of the "Build -> Verify -> Destroy" cycle is a hard requirement for each lab.
```

**Step 2: Commit changes**
```bash
git add CONTEXT.md
git commit -m "chore: update context with ephemeral and bip rules"
```

---

### Task 2: Roadmap V2 Creation
**Files:**
- Create: `ROADMAP_V2.md`

**Step 1: Create ROADMAP_V2.md with 8 Architecture Blocks**
Define the 16-week high-intensity path.

```markdown
# 🚀 2026 AI-First Cloud Security Architect Roadmap (V2)
*The Ephemeral Path to SAA-C03 and AWS AI Credentials*

## 🗺️ The Architecture Blocks (CABs)

| Block | Phase | Weeks | Focus | Goal |
| :--- | :--- | :--- | :--- | :--- |
| **CAB-01** | Foundations | 1-2 | **CDK & IAM Zero-Trust** | Rebuild Medical VPC with CDK. Implement Org-level SCPs. |
| **CAB-02** | Security | 3-4 | **Network Hardening** | ALBs, WAF, and VPC Endpoints for PHI isolation. |
| **CAB-03** | Data | 5-6 | **KMS & PHI Protection** | Automatic encryption of patient records at rest/transit. |
| **CAB-04** | AI | 7-8 | **Bedrock Compliance** | Use Bedrock to audit infrastructure logs for HIPAA compliance. |
| **CAB-05** | Resilience | 9-10 | **High Availability** | Global Accelerator and Multi-Region DR strategies. |
| **CAB-06** | DevOps | 11-12 | **CI/CD Architecture** | Automate the spin-up/tear-down labs via GitHub Actions. |
| **CAB-07** | Intelligence | 13-14 | **SageMaker Security** | Private link and EMR security for medical data science. |
| **CAB-08** | Final Blitz | 15-16 | **Certification & Portfolio** | SAA-C03 Blitz + AI Specialty preparation. |
```

**Step 2: Commit changes**
```bash
git add ROADMAP_V2.md
git commit -m "feat: initialize roadmap v2"
```

---

### Task 3: Cleanup & Tracker Initialization
**Files:**
- Delete: `TODO.md`
- Create: `docs/plans/task.md`

**Step 1: Initialize the live task tracker**
Create the tracker file for the execution skill.

```markdown
| id | task | status | notes |
| --- | --- | --- | --- |
| v2-prep-1 | Update Context Rules | pending | |
| v2-prep-2 | Initialize Roadmap V2 | pending | |
| v2-prep-3 | Cleanup Legacy TODO | pending | |
```

**Step 2: Remove legacy TODO.md**
```bash
rm TODO.md
```

**Step 3: Commit changes**
```bash
git add docs/plans/task.md TODO.md
git commit -m "chore: migrate from TODO.md to live task tracker"
```
