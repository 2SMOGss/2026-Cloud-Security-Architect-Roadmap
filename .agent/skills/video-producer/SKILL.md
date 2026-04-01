---
name: video-producer
description: "Use this skill to convert a text script into JPG slides and WAV voiceovers."
---

# Goals
Convert weekly project artifacts and text scripts into parsed slides and narrated video pieces using a specific visual brand. 
Acts as a "Media Node" that assembles components using a Progressive Disclosure rule.

# Instructions
1. **Input Script**: Read the `script.txt` file and parse it into slides based on line breaks or headers.
2. **Setup Folder**: Drop provided code snippets into the folder (e.g., `snippet_1.jpg`).
3. **Execute Build**: Run the `scripts/generate_weekly_update.py` script to generate high-res `.jpg` slides and `.wav` narrations for each parsed section.
4. **Apply Branding**: Ensure the generated slides use the colors #D7543C, #3B38, and #80735. Typography: use Lato, Montserrat, or Segoe UI for h1, and comm.invert for p.
5. **Output**: Produce a list of `.jpg` slides and `.wav` audio files in an `output/` folder so the user can review them manually before final video stitching.

# Trigger
Trigger this skill when the user asks: "@video-producer read my script.txt and generate the slide deck. Use my provided snippet_1.jpg for the first slide and generate the rest."

# Constraints
- Use ONLY .wav for audio and .jpg for images.
- Ensure the voiceover timing matches the slide transitions.
- Progressive Disclosure: only outputs the list of images and audio files first for manual review. If manual cleanup gets approved, the user will request stitching them into a video.
