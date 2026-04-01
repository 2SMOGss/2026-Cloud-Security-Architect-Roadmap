---
name: saa-summary
description: Triggers when Robert says "wrapping up," "finishing for now," or "final part of the session."
---

# 🎓 SAA-C03 Session Closer (Enhanced)

## 🎯 Purpose
To perform a deep-dive technical recap and generate a dynamic practice mini-exam (5-10 questions) based on the volume and complexity of the session's data.

## 🛠️ Trigger Phrase
- "I'm wrapping up for today."
- "Let's start wrapping up."
- "Final part of the session."

## 📜 Execution Logic
1. **Volume Assessment:** - Analyze the session history. 
   - If the session was short/focused: Generate **5 questions**.
   - If the session involved multiple architectural layers or complex debugging: Generate **10 questions**.
2. **Technical Recap:** Provide a bulleted list of the AWS services and security protocols implemented (e.g., IAM policies, Subnet CIDRs, Bedrock limits).
3. **The Mini-Exam:**
   - **Scenario-Based:** All questions must be "Case Study" style (e.g., "A medical distributor needs to...") to match SAA-C03 rigor.
   - **Domain Mapping:** Tag each question with its SAA-C03 Domain (e.g., [Domain 1: Secure Architectures]).
4. **Approval & Reveal:** - Present the questions without answers.
   - Wait for Robert's signal: "Ready for the key" or "Check my answers."

## 🛑 Hard Requirement
The questions must include at least one "distractor" option that is a valid AWS service but the *wrong* choice for the specific scenario (e.g., using S3 Standard when S3 Glacier Instant Retrieval is the cost-optimized HIPAA choice).