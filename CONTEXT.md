# 📁 Project Context: VitalStream Medical Cloud Migration

## 👤 Candidate Profile
* **Name:** Robert Chich
* **Background:** 20 years as a Paramedic (High-pressure triage and decision-making).
* **Current Path:** Transitioning to Cloud Security Architect (Age 51).
* **Foundation:** Google Cybersecurity Certificate (Bash, Linux, Security Fundamentals).
* **Target:** AWS Solutions Architect Associate (SAA-C03) Certification.

## 🏥 Business Case: VitalStream Medical
* **Industry:** Medical Equipment Distributor.
* **Scenario:** Migrating internal infrastructure to AWS.
* **Compliance Requirements:** Strict HIPAA/HITRUST alignment.
* **Key Needs:** Secure remote access for sales teams and total isolation for Patient Protected Health Information (PHI).

## 🛠️ Technical Strategy
* **Methodology:** 16-Week AI-First Structured Roadmap (Roadmap V2).
* **Cloud Provider:** AWS (Primary Region: us-east-1).
* **Infrastructure as Code:** Mandatory AWS CDK (Python).
* **Security Principle:** Least Privilege and Zero-Trust architecture.

## 🛡️ The Mentors "Ephemeral Architect" Protocol (Golden Rules)
1. **Low-Cost Ephemerality:** All labs must be "spun up" for learning and "torn down" (cdk destroy) immediately after. No resources left running.
2. **IaC First:** AWS CDK (Python) is the mandatory standard. No more manual console or bash-only infrastructure.
3. **Build in Public (BiP):** Documentation of the "Build -> Verify -> Destroy" cycle is a hard requirement for each lab.

## 📍 Current Status
*(Last synced against `roadmap-v3.2.md` — that file is the source of truth if this drifts again.)*
* **Completed:** CAB-01 (VPC Plumbing), CAB-03 (KMS & PHI Protection), CAB-04 (Bedrock & Guardrails), CAB-05 (High Availability).
* **Built, pending live verification:** CAB-02 (IAM & Zero-Trust) and CAB-06 (S3 Lifecycle & Cost Optimization) — CDK code + passing unit tests exist for both; neither has been `cdk deploy`'d against a real account yet. Follow each one's `LAB_GUIDE.md` and update its `AUDIT.md` once deployed.
* **Not started:** CAB-07 (Serverless Performance, Domain 3), CAB-08 (Final Blitz / Cert Prep).
* **Side projects:** `sentinel-badge` (Sentinel View Counter badge, Vercel).
* **Exam-readiness note:** Domain 3 (High-Performing) is now the only domain with zero hands-on coverage — CAB-07 closes that gap and should be prioritized over Phase 6 portfolio extensions (CI/CD, Kinesis/Glue, SageMaker).

## 🤖 AI Interaction Protocol
* **Antigravity Agent Role:** Cloud Engineer / Executioner.
* **Gemini Chat Role:** Lead Architect / Strategic Advisor.
* **Communication:** Agent should refer to this file and the `roadmap-v3.2.md` for all task context.

## 📚 Documentation & Knowledge Sharing Protocol
*   **Trigger:** Create a new Markdown file in `assets/docs/learning_teach/` **each time a new concept or task is completed**.
*   **Format:** MARP-ready Slides (`marp: true`, `theme: 2smogss`).
*   **Naming Convention:** `WeekX_Topic_Name.md` (e.g., `Week1_Securing_Medical_VPC.md`).
*   **Organization:** If `assets/docs/learning_teach/` becomes cluttered, refactor into subfolders (e.g., `assets/docs/learning_teach/Week_1/`).
*   **Content Goal:** Create content suitable for "Building in Public" (X/Twitter posts).

POLICY: Manual Terminal Execution (MTE - Git Bash Preference)
Scope: All terminal commands, AWS CLI operations, and Bash script executions.
Constraint: The AI is strictly prohibited from executing commands or assuming a command was successful without user-provided output.
Action: > 1. All commands must be presented in a bash or python code block.
2. The AI must pause and explicitly ask the user to: "Please execute the above in your terminal and provide the output."
3. Python scripts intended for automation must first be reviewed as "Draft" before the user is prompted to save and run them.
Verification: Success is only verified once the user pastes the CLI JSON response or exit code into the chat.