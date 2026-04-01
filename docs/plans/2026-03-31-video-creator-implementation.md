# Sentinel Video Archivist Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Automate MARP-to-Video generation with professional neural voiceovers using free/local tools.

**Architecture:** A Python-based orchestrator that parses MARP scripts from HTML comments, renders slides via `marp-cli`, synthesizes audio via `edge_tts`, and stitches segments with `ffmpeg`.

**Tech Stack:** Python 3.10+, `edge-tts` (Free neural voice), `marp-cli` (via npx), `ffmpeg`.

---

### Task 1: Skill Initialization
**Files:**
- Create: `.agent/skills/documenting-progress-videos/SKILL.md`
- Create: `.agent/skills/documenting-progress-videos/scripts/logic.py`

**Step 1: Create the Skill structure**
Run: `mkdir -p .agent/skills/documenting-progress-videos/scripts`

**Step 2: Initialize SKILL.md**
Write the frontmatter and instructions for the skill.

**Step 3: Commit**
`git add .agent/skills/documenting-progress-videos`
`git commit -m "feat: initialize video-archivist skill structure"`

### Task 2: Implement MARP Script Parser (TDD)
**Files:**
- Create: `.agent/skills/documenting-progress-videos/scripts/parser.py`
- Create: `.agent/skills/documenting-progress-videos/scripts/test_parser.py`

**Step 1: Write failing test for comment extraction**
```python
def test_extract_voiceover():
    content = "# Slide 1\n<!-- voiceover: Hello world -->\n---\n# Slide 2\n<!-- voiceover: Second slide -->"
    from parser import parse_marp
    scripts = parse_marp(content)
    assert scripts == ["Hello world", "Second slide"]
```

**Step 2: Run test to verify it fails**
`pytest .agent/skills/documenting-progress-videos/scripts/test_parser.py`

**Step 3: Implement `parse_marp`**
```python
import re
def parse_marp(text):
    slides = text.split('---')
    scripts = []
    for slide in slides:
        match = re.search(r'<!--\s*voiceover:\s*(.*?)\s*-->', slide, re.DOTALL)
        if match:
            scripts.append(match.group(1).strip())
        else:
            # Fallback to slide header or empty
            scripts.append("")
    return scripts
```

### Task 3: Integrate Edge-TTS Synthesis
**Files:**
- Modify: `.agent/skills/documenting-progress-videos/scripts/logic.py`

**Step 1: Install Dependencies**
`pip install edge-tts`

**Step 2: Implement audio synthesis function**
```python
import edge_tts
import asyncio

async def synthesize_audio(text, output_path):
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural")
    await communicate.save(output_path)
```

### Task 4: Implement High-Fidelity Rendering
**Files:**
- Modify: `.agent/skills/documenting-progress-videos/scripts/logic.py`

**Step 1: Invoke marp-cli via subprocess**
```python
import subprocess
def render_slides(md_path, output_dir):
    cmd = f"npx @marp-team/marp-cli {md_path} --images png --output {output_dir}/slide"
    subprocess.run(cmd, shell=True, check=True)
```

### Task 5: Final Orchestration & FFmpeg Assembly
**Files:**
- Modify: `.agent/skills/documenting-progress-videos/scripts/logic.py`

**Step 1: Implement FFmpeg stitching**
For each slide/audio pair, measure audio, create segment, then concat.

**Step 2: Final Verification**
Test with `learning_teach/Week_06/Week6_AI_Sentinel_Shield.md`.
