---
name: commit-changes
description: "Use when the user asks to commit changes. Performs a comprehensive HIPAA and security audit to prevent exfiltration of PHI, AWS keys, private IPs, and credentials before preparing the commit message and pushing to GitHub."
---

# Antigravity Standard Skill: commit-changes
# Purpose: Maintain architectural consistency, HIPAA data isolation, and verify that no sensitive credentials leak into source control.

When the user asks you to commit changes to the repository, you **MUST** follow this structured auditing protocol autonomously before making any commits.

## Phase 1: Data Isolation Check
You must actively search the working directory (specifically focusing on modified or untracked files) to verify there are absolutely no sensitive artifacts left behind. 

Scan for the following patterns:
1. **AWS Secrets:** `AKIA[0-9A-Z]{16}`
2. **PHI (Protected Health Information):** `SSN:`, `DOB:`, `PATIENT_ID`
3. **Private IP Addresses:** `10\.\d+\.\d+\.\d+`, `172\.(1[6-9]|2[0-9]|3[0-1])\.\d+\.\d+`, `192\.168\.\d+\.\d+`
4. **Credentials/Logins:** Patterns like `password\s*=`, `login\s*=`, or general hardcoded authentication credentials.

**If any prohibited patterns are detected:**
- Announce ❌ `[AUDIT FAILURE]: Sensitive data pattern detected.`
- Specify which files failed the check and halt the commit process immediately. Ask the Architect to clean the files before you proceed.

**If no patterns are detected:**
- Announce ✅ `[AUDIT PASSED]: No prohibited patterns found.`
- Stage the files automatically using `git add .`

## Phase 2: Unified Tone & Commit Drafting
Ask the user to describe the update (e.g., "Hardened WAF" or "Added Bedrock Guardrails").
Once you receive their description, format the commit message to perfectly align with the Architect Roadmap V2:

`COMMIT_MSG="VitalStream Architecture: {user_input} | Verified for HIPAA"`

## Phase 3: Final Sign-off
Present the generated `COMMIT_MSG` to the user and prompt them:
`"🚀 READY FOR DEPLOYMENT. Confirm standardized push? (y/n)"`

If they confirm, execute:
- `git commit -m "{COMMIT_MSG}"`
- `git push origin main`
And announce ✨ `[SUCCESS]: Repository synchronized.`

If they deny, state ✋ `[HALT]: Push deferred by Architect.`