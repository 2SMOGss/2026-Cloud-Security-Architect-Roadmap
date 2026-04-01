import os
import subprocess
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

# Helper to run commands
def run_cmd(cmd):
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result.returncode == 0

# 1. GENERATE THE .WAV VOICE OVER
def create_voiceover(text, index, output_dir):
    print(f"Generating voiceover {index}...")
    try:
        # Pronunciation fix for Robert Chich
        spoken_text = text.strip().replace("Chich", "Chick")
        tts = gTTS(text=spoken_text, lang='en')
        temp_mp3 = os.path.join(output_dir, f"temp_{index}.mp3")
        wav_file = os.path.join(output_dir, f"audio_{index}.wav")
        tts.save(temp_mp3)
        
        # Convert to WAV
        if run_cmd(f'ffmpeg -i "{temp_mp3}" -acodec pcm_s16le -ar 44100 "{wav_file}" -y'):
            if os.path.exists(temp_mp3):
                os.remove(temp_mp3)
            return True
    except Exception as e:
        print(f"TTS Error on {index}: {e}")
    return False

# 2. GENERATE THE .JPG SLIDE (Modernized)
def create_jpg_slide(text, index, output_dir, color_scheme):
    print(f"Generating slide {index}...")
    
    # 1. Use backgrounds based on slide index
    project_root = "d:/download_other/AWS/2026 Cloud Security Architect Roadmap"
    bg_path = os.path.join(project_root, "assets", "video_bg_title.png") if index == 0 else os.path.join(project_root, "assets", "video_bg_content.png")
    if os.path.exists(bg_path):
        img = Image.open(bg_path).convert('RGB')
    else:
        # Fallback to gradient if AI backgrounds missing
        img = Image.new('RGB', (1920, 1080), color=color_scheme['bg'])
    
    d = ImageDraw.Draw(img)
    
    # 2. Font Selection (Windows)
    font_bold = "C:\\Windows\\Fonts\\segoeuib.ttf"
    font_reg = "C:\\Windows\\Fonts\\segoeui.ttf"
    
    try:
        h_font = ImageFont.truetype(font_bold, 80) if os.path.exists(font_bold) else None
        b_font = ImageFont.truetype(font_reg, 50) if os.path.exists(font_reg) else None
    except:
        h_font = b_font = None

    # 3. Text Parsing & Drawing
    lines = text.split('.')
    header = lines[0].strip()
    body = ". ".join(lines[1:]).strip()
    
    # Draw header with #00d2ff (Cyan highlight)
    d.text((120, 150), header, font=h_font, fill="#00d2ff")
    
    # Wrap body text manually
    words = body.split()
    body_lines = []
    current_line = []
    for word in words:
        if len(" ".join(current_line + [word])) < 55:
            current_line.append(word)
        else:
            body_lines.append(" ".join(current_line))
            current_line = [word]
    body_lines.append(" ".join(current_line))
    
    y = 300
    for bline in body_lines[:12]:
        d.text((120, y), bline, font=b_font, fill="#e2e8f0")
        y += 70

    img_path = os.path.join(output_dir, f"slide_{index}.jpg")
    img.save(img_path)
    return True

# 3. MAIN ORCHESTRATOR
def main(script_path):
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    with open(script_path, 'r', encoding='utf-8') as f:
        slides_text = [s.strip() for s in f.read().split('\n\n') if s.strip()]
        
    print("\n=== SCRIPT REVIEW ===")
    parsed_segments = []
    for i, text in enumerate(slides_text):
        if "Voiceover:" in text:
            parts = text.split("Voiceover:", 1)
            slide_text = parts[0].strip()
            voice_text = parts[1].strip()
        else:
            slide_text = text
            voice_text = text
        parsed_segments.append((slide_text, voice_text))
        print(f"\n[Segment {i} - Slide Display]:\n{slide_text[:100]}...")
        print(f"[Segment {i} - Voiceover Script]:\n{voice_text[:100]}...")
        
    print("\n=====================")
    approval = input("Do you approve this script for video generation? (y/n): ")
    if approval.lower() != 'y':
        print("Video generation aborted by user. Please update script and try again.")
        return
        
    colors = {'bg': '#3B3838', 'primary': '#D7543C', 'text': '#807355'} 
    
    segments = []
    for i, (slide_text, voice_text) in enumerate(parsed_segments):
        if create_voiceover(voice_text, i, output_dir) and create_jpg_slide(slide_text, i, output_dir, colors):
            img = os.path.join(output_dir, f"slide_{i}.jpg")
            wav = os.path.join(output_dir, f"audio_{i}.wav")
            out = os.path.join(output_dir, f"segment_{i}.mp4")
            
            # Create segment
            if run_cmd(f'ffmpeg -loop 1 -i "{img}" -i "{wav}" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest "{out}" -y'):
                segments.append(out)

    # Concat
    if segments:
        input_list = os.path.join(output_dir, "inputs.txt")
        with open(input_list, "w", encoding='utf-8') as f:
            for s in segments:
                f.write(f"file '{os.path.basename(s)}'\n")
        
        final_video = os.path.join(output_dir, "Final_Video.mp4")
        if run_cmd(f'ffmpeg -f concat -safe 0 -i "{input_list}" -c copy "{final_video}" -y'):
            print(f"Success! Final video: {final_video}")

if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "script.txt")



