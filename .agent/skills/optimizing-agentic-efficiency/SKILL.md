---
name: optimizing-agentic-efficiency
description: Monitors skill and agent execution to prevent redundancy, conflict, and logical drift between specialized Sentinel tools.
---

# 🚀 Optimizing Agentic Efficiency

## 🎯 Purpose
The **Optimizing Agentic Efficiency** skill is the "Conductor" of the VitalStream Sentinel ecosystem. It ensures that the overall system of skills (e.g., EPT, Ulta, Watchdog) works in a unified, efficient manner without logical collisions or redundant sub-tasks.

## 🛠️ Triggers
- When a new skill or agent is added to the `.agent/` directory.
- Before executing a multi-step **CAB (Architecture Block)** implementation plan.
- If the agent detects redundant logic between two or more existing skills.
- When the agent is choosing between **Low-Level CLI** and **High-Level Abstractions** (Boto3/CDK).

## 📜 Execution Logic
1.  **Skill Redundancy Audit**: Before invoking a new automation, scan the `.agent/skills/` directory for existing markdown patterns or Python scripts that perform similar AWS or file operations.
2.  **Constraint Conflict Check**: Verify that "Hard Rules" in one skill (e.g., naming conventions in `generating-antigravity-skills`) do not conflict with requirements in another (e.g., HIPAA-compliance markers in `ulta-architecture-agent`).
3.  **Performance Optimization**: Propose the most "Architecturally Sound" method for a task:
    - **Tier 1 (Elite)**: Python Boto3 logic via `scripts/logic.py`.
    - **Tier 2 (Standard)**: High-level CLI tools (e.g., `s3 sync` vs `s3 cp`).
    - **Tier 3 (Legacy)**: Low-level terminal commands (Avoid if possible).
4.  **Feedback Loop**: Log an "Efficiency Sitrep" when a more streamlined path is identified, and update the associated implementation plans as a result.

## 🏁 Hard Requirements
- **No Logical Overlap**: Every skill must have a unique purpose without duplicating the core logic of another (Ref: `token-watchdog` for costs vs this skill for execution methods).
- **Consistency**: All skills must adhere to the **VitalStream Prefixes** (e.g., `vitalstream-`, `S3-PHI-`, etc.).

## 📂 Resources
- `scripts/analyze_skills.py`: Search tool for keyword/intent overlap in the skills directory.
- `resources/efficiency_baseline.yaml`: Standardized naming and architectural patterns to enforce.
