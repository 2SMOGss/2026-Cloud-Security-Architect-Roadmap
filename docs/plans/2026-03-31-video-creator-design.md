# Design Doc: 2026-03-31 - Sentinel Video Archivist

## Goal
Automate the production of professional-grade "Build in Public" videos for the 2026 Cloud Security Architect Roadmap. The agent must convert MARP slides into narrated videos with modern aesthetics and high-fidelity audio.

## Architecture

### 1. Data Source
- **Input**: MARP-compliant Markdown files (`.md`).
- **Narration Hook**: Hidden HTML comments in the format `<!-- voiceover: "Script text" -->`.

### 2. High-Fidelity Rendering
- **Engine**: `@marp-team/marp-cli` (invoked via `npx`).
- **Format**: High-resolution PNG exports (1920x1080).
- **Benefit**: Preserves complex CSS, custom themes (like `2smogss`), and layout perfectly.

### 3. Audio Synthesis (Free/Local Tier)
- **Engine**: `edge-tts` (Python library).
- **Voice**: `en-US-ChristopherNeural` (Authoritative, clean).
- **Output**: Individual `.mp3` files per slide.

### 4. Media Assembly
- **Orchestrator**: Python logic (`scripts/logic.py`).
- **Engine**: `ffmpeg`.
- **Logic**: 
    1. Measure `.mp3` duration.
    2. Create a video segment for each slide image matching that duration.
    3. Concatenate all segments using the `concat` protocol.

## Structural Pattern (per generating-antigravity-skills)
- **Skill Directory**: `.agent/skills/documenting-progress-videos/`
- **Logic**: `scripts/logic.py`
- **Examples**: `examples/sample_slides.md`
- **Checklist**: Plan-Validate-Execute pattern for HIPAA-compliant logging and security.

## Error Handling
- **Missing Audio**: Fallback to 3 seconds of silence and header-text read.
- **Marp Errors**: Trap `marp-cli` exit codes and report line-number failures.
- **FFmpeg Conflicts**: Ensure output directories are clean before runs.

## Next Steps
1. Initialize the skill directory.
2. Implement the MARP parser.
3. Integrate `edge-tts`.
4. Validate with `learning_teach/Week_06/Week6_AI_Sentinel_Shield.md`.
