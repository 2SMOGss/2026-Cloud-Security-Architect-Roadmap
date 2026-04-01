#!/bin/bash

# 🎯 CONFIGURATION
# SOURCE_DIR="/mnt/d/download_other/AWS/2026 Cloud Security Architect Roadmap/.agent_ON_ICE/skills"
# DEST_DIR="/mnt/d/download_other/gem_agent/skills"

# Detect Operating System for Path Resolution
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Git Bash / Windows
    SOURCE_DIR="/d/download_other/AWS/2026 Cloud Security Architect Roadmap/.agent_ON_ICE/skills"
    DEST_DIR="/d/download_other/gem_agent/skills"
else
    # WSL / Linux
    SOURCE_DIR="/mnt/d/download_other/AWS/2026 Cloud Security Architect Roadmap/.agent_ON_ICE/skills"
    DEST_DIR="/mnt/d/download_other/gem_agent/skills"
fi

# 🚀 TARGET SUITES
SENTINEL_AGENTS=("ept-security-agent" "ulta-architecture-agent" "token-watchdog" "sitrep-monitor" "optimizing-agentic-efficiency")
PRODUCTION_SUITE=("video-producer" "generating-marp-slides" "marp-cli-slides")
EDUCATION_SUITE=("generating-saa-quizzes" "using-superpowers" "generating-antigravity-skills")

# Merge into one master list
TARGET_MIGRATION=("${SENTINEL_AGENTS[@]}" "${PRODUCTION_SUITE[@]}" "${EDUCATION_SUITE[@]}")

# 1. Target Preparation
echo "[*] Initializing targeted migration at: $DEST_DIR"
mkdir -p "$DEST_DIR"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "[!] Error: Source directory $SOURCE_DIR not found. Please check paths."
    exit 1
fi

# 2. Sequential Migration & Integrity Check
count=0
for skill in "${TARGET_MIGRATION[@]}"; do
    if [ -d "$SOURCE_DIR/$skill" ]; then
        echo "[✓] Porting Skill: $skill"
        cp -rv "$SOURCE_DIR/$skill" "$DEST_DIR/"
        count=$((count + 1))
    else
        echo "[!] Note: Skill $skill not found in source. Skipping..."
    fi
done

# 3. Final Summary
echo "--------------------------------------------------------"
echo "[✓] SENTINEL SUITE ARCHIVED"
echo "Target: $DEST_DIR"
echo "Total skills ported: $count"
ls -F "$DEST_DIR"
