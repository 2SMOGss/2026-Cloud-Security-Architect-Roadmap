import os
import argparse

def create_skill_scaffold(skill_name):
    """
    Scaffolds a new AntiGravity skill directory following Robert Chich's 
    Roadmap V2 standards (Python/Boto3).
    """
    # Force the path to be relative to the project root for consistency
    base_path = f".agent/skills/{skill_name}"
    subdirs = ["scripts", "examples", "resources"]
    
    # Create directories
    for subdir in subdirs:
        os.makedirs(os.path.join(base_path, subdir), exist_ok=True)
        print(f"Created: {base_path}/{subdir}")

    # Create SKILL.md template
    skill_md_content = f"""---
name: {skill_name}
description: Automatically generated skill for {skill_name}.
---

# {skill_name.replace('-', ' ').title()}

## Logic
* Use `scripts/main.py` for execution.
* Ensure HIPAA compliance markers are checked.

## Checklist
- [ ] Validation complete
- [ ] Execution logged
"""
    
    with open(os.path.join(base_path, "SKILL.md"), "w") as f:
        f.write(skill_md_content)
    
    # Create a dummy python script
    with open(os.path.join(base_path, "scripts/main.py"), "w") as f:
        f.write("import boto3\nimport sys\n\ndef run():\n    print('Starting Boto3 logic...')\n\nif __name__ == '__main__':\n    run()")

    print(f"\nSuccess: Skill '{skill_name}' initialized.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a new AntiGravity skill.")
    parser.add_argument("name", help="The gerund-form name of the skill (e.g., auditing-vpc-flow-logs)")
    args = parser.parse_args()
    create_skill_scaffold(args.name)
