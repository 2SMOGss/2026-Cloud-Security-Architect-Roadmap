---
name: generating-antigravity-skills
description: Generates standardized, Boto3-based skill directories for the AntiGravity environment, ensuring HIPAA-compliant structural patterns for Robert Chich.
---

# Skill Generation Workflow

This skill automates the creation of new capabilities within the `.agent/skills/` directory. It enforces the Python/Boto3 requirement and maintains the "Plan-Validate-Execute" pattern essential for VitalStream's security posture.

## 1. Initial Assessment
* Identify the specific AWS service or security task (e.g., IAM rotation, S3 encryption audit).
* Define the "Gerund" name for the folder (e.g., `monitoring-cloudtrail-logs`).
* Ensure no Bash scripts are planned; use `scripts/logic.py` instead.

## 2. Structural Checklist
- [ ] Create directory: `.agent/skills/<skill-name>/`
- [ ] Create `SKILL.md` with YAML frontmatter.
- [ ] Create `scripts/` directory for Python logic.
- [ ] Initialize `examples/` for sample configurations.

## 3. Execution Pattern
1. **Plan**: Define the Boto3 calls required.
2. **Validate**: Run script with `--dry-run` or `--verify` flags.
3. **Execute**: Perform the actual cloud modification.

## 4. Error Handling
* If a Boto3 exception occurs, the agent must capture the `ClientError`.
* If unsure of parameters, run `python scripts/<name>.py --help`.

> **Note:** All paths must use forward slashes (`/`) for cross-platform compatibility within the agent environment.