import os
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

# 1. GENERATE THE .WAV VOICE OVER
def create_voiceover(text, index):
    tts = gTTS(text=text, lang='en')
    temp_mp3 = f"temp_{index}.mp3"
    wav_file = f"output/audio_{index}.wav"
    tts.save(temp_mp3)
    # Convert to WAV using FFmpeg (standard for high-quality audio nodes)
    os.system(f"ffmpeg -i {temp_mp3} -acodec pcm_s16le -ar 44100 {wav_file} -y")
    if os.path.exists(temp_mp3):
        os.remove(temp_mp3)

# 2. GENERATE THE .JPG SLIDE
def create_jpg_slide(text, index, color_scheme):
    # Standard 1080p slide
    img = Image.new('RGB', (1920, 1080), color=color_scheme['bg'])
    d = ImageDraw.Draw(img)
    
    # Simple branding bar
    d.rectangle([0, 0, 1920, 120], fill=color_scheme['primary'])
    
    # Add Text (Simplified - you can add font paths here)
    d.text((100, 400), text[:100] + "...", fill=color_scheme['text'])
    
    os.makedirs("output", exist_ok=True)
    img.save(f"output/slide_{index}.jpg")

# 3. MAIN ORCHESTRATOR
def process_script(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # Split script into slides by double newline
        slides = f.read().split('\n\n')
        
    # Updated to use custom branding colors from image
    colors = {'bg': '#3B3838', 'primary': '#D7543C', 'text': '#807355'} 
    
    for i, slide_text in enumerate(slides):
        if not slide_text.strip():
            continue
        create_voiceover(slide_text, i)
        create_jpg_slide(slide_text, i, colors)
        print(f"Generated Slide {i} and Audio {i}")

# 4. FINAL STITCHING (Run after manual review)
def stitch_video(num_slides):
    # Step 1: Combine each slide and audio into a temporary video snippet
    with open("output/inputs.txt", "w", encoding='utf-8') as f:
        for i in range(num_slides):
            img_file = f"output/slide_{i}.jpg"
            wav_file = f"output/audio_{i}.wav"
            out_file = f"output/segment_{i}.mp4"
            
            # Create video segment for this slide
            os.system(f"ffmpeg -loop 1 -i {img_file} -i {wav_file} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest {out_file} -y")
            
            # Add to concat list
            f.write(f"file 'segment_{i}.mp4'\n")
            
    # Step 2: Concatenate all segments into the final video
    os.system("ffmpeg -f concat -safe 0 -i output/inputs.txt -c copy output/Final_Video.mp4 -y")
    print("Final video assembled at output/Final_Video.mp4")

if __name__ == "__main__":
    import sys
    script_path = sys.argv[1] if len(sys.argv) > 1 else "script.txt"
    process_script(script_path)
    # Perform final stitching
    stitch_video(len(open(script_path, encoding='utf-8').read().split('\n\n')))



