import os
import re
import yaml
import sys

def get_skill_metadata(skill_path):
    """
    Parses the YAML frontmatter from a SKILL.md file.
    """
    try:
        with open(os.path.join(skill_path, 'SKILL.md'), 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
            if match:
                return yaml.safe_load(match.group(1))
    except Exception as e:
        print(f"Error reading {skill_path}: {e}")
    return None

def check_for_overlaps():
    """
    Analyzes all skills in .agent/skills/ for overlap and potential conflicts.
    """
    skills_dir = '.agent/skills/'
    if not os.path.exists(skills_dir):
        print(f"Directory {skills_dir} not found.")
        return

    skill_list = []
    for d in os.listdir(skills_dir):
        path = os.path.join(skills_dir, d)
        if os.path.isdir(path):
            meta = get_skill_metadata(path)
            if meta:
                meta['path'] = path
                skill_list.append(meta)

    print(f"--- Meta-Efficiency Audit: {len(skill_list)} Skills Detected ---")

    # 1. Simple Keyword Overlap
    keywords_to_watch = ['monitor', 'compliance', 's3', 'iam', 'rotation', 'audit', 'verification']
    overlap_map = {kw: [] for kw in keywords_to_watch}

    for skill in skill_list:
        desc = skill.get('description', '').lower()
        name = skill.get('name', '').lower()
        for kw in keywords_to_watch:
            if kw in desc or kw in name:
                overlap_map[kw].append(name)

    # 2. Results
    conflicts_found = False
    for kw, owners in overlap_map.items():
        if len(owners) > 1:
            print(f"⚠️ POTENTIAL OVERLAP: Keyword '{kw}' used in multiple skills: {', '.join(owners)}")
            conflicts_found = True

    if not conflicts_found:
        print("✅ NO CORE OVERLAP DETECTED: Each skill maintains a distinct domain.")
    else:
        print("💡 RECOMMENDATION: Ensure specialized agents (e.g. EPT vs Ulta) have non-overlapping triggers.")

if __name__ == "__main__":
    check_for_overlaps()
