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
* **Methodology:** 24-Week Structured Roadmap (Build-in-Public).
* **Cloud Provider:** AWS (Primary Region: us-east-1).
* **Infrastructure as Code:** Moving from Bash/CLI scripts to AWS CDK (Python).
* **Security Principle:** Least Privilege and Zero-Trust architecture.

## 📍 Current Status
* **Phase:** 1 (Foundations & Shell Automation).
* **Week:** 2 (IAM + Security Architecture).
* **Completed Tasks:** * Week 1: 3-Tier Medical VPC Architecture (Bash/CLI).
    * Default Security Group Hardening implemented and verified.
    * VPC Flow Logs enabled (CloudWatch).
    * Documentation for Week 1 created in `learning_teach/`.

## 🤖 AI Interaction Protocol
* **Antigravity Agent Role:** Cloud Engineer / Executioner.
* **Gemini Chat Role:** Lead Architect / Strategic Advisor.
* **Communication:** Agent should refer to this file and the `Roadmap_2026.md` for all task context.

## 📚 Documentation & Knowledge Sharing Protocol
*   **Trigger:** Create a new Markdown file in `learning_teach/` **each time a new concept or task is completed**.
*   **Format:** MARP-ready Slides (`marp: true`, `theme: 2smogss`).
*   **Naming Convention:** `WeekX_Topic_Name.md` (e.g., `Week1_Securing_Medical_VPC.md`).
*   **Organization:** If `learning_teach/` becomes cluttered, refactor into subfolders (e.g., `learning_teach/Week_1/`).
*   **Content Goal:** Create content suitable for "Building in Public" (X/Twitter posts).

POLICY: Manual Terminal Execution (MTE)
Scope: All terminal commands, AWS CLI operations, and Bash script executions.
Constraint: The AI is strictly prohibited from executing commands or assuming a command was successful without user-provided output.
Action: > 1. All commands must be presented in a bash or python code block.
2. The AI must pause and explicitly ask the user to: "Please execute the above in your terminal and provide the output."
3. Python scripts intended for automation must first be reviewed as "Draft" before the user is prompted to save and run them.
Verification: Success is only verified once the user pastes the CLI JSON response or exit code into the chat.