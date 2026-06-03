#!/usr/bin/env python3
"""
Build a book trailer video for "The Little Cloud's Big Adventure"
Output: 1080x1920 vertical MP4 for YouTube Shorts / Instagram Reels
"""

import subprocess, os, math, struct, wave, json, tempfile, shutil
from pathlib import Path

ILLUSTRATIONS = Path("/home/team/shared/storybook-illustrations")
OUTPUT = Path("/home/team/shared/little-cloud-trailer.mp4")
TMP_DIR = Path("/tmp/trailer_build")
TMP_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# Image selection & captions - key story moments
# ============================================================
# Pick ~10 key illustrations that tell the story arc
SLIDES = [
    ("front-cover.png", "✨ The Little Cloud's Big Adventure", 4.0),
    ("page-02.png", "High above the hills lived a little cloud named Cirrus", 3.0),
    ("page-04.png", '"What is it like down there?" Cirrus wondered', 3.0),
    ("page-05.png", "The flowers were drooping and very thirsty", 3.0),
    ("page-07.png", "But only one tiny plip fell...", 3.0),
    ("page-09.png", '"Everyone has a special job to do" — Sunny', 3.0),
    ("page-11.png", "Gusty blew and Cirrus flew!", 3.0),
    ("page-13.png", "Cirrus made a big, cool shadow on the playground", 3.0),
    ("page-17.png", '"We work better together!" said Drippy', 3.0),
    ("page-20.png", "Pitter-patter! The rain began to fall", 3.5),
    ("page-22.png", "A beautiful rainbow stretched across the sky", 3.0),
    ("page-24.png", '"I can\'t wait for tomorrow\'s adventure"', 3.5),
]

def get_image_size(path):
    """Get image dimensions using ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=width,height",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True
    )
    parts = result.stdout.strip().split(",")
    if len(parts) == 2:
        return int(parts[0]), int(parts[1])
    return None, None

def create_title_card():
    """Create title card using ffmpeg drawtext."""
    out = TMP_DIR / "card_title.png"
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=#87CEEB:s=1080x1920:d=0.1",
        "-vf",
        "drawtext=text='The Little Cloud's\nBig Adventure':fontcolor=white:fontsize=72:"
        "x=(w-text_w)/2:y=(h-text_h)/2-120:line_spacing=10:"
        "borderw=3:bordercolor=#4A90D9:"
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf,"
        "drawtext=text='StorySprout Press':fontcolor=white:fontsize=36:"
        "x=(w-text_w)/2:y=(h+text_h)/2+40:"
        "borderw=2:bordercolor=#4A90D9:"
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "-frames:v", "1", str(out)
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    return out

def create_end_card():
    """Create end card."""
    out = TMP_DIR / "card_end.png"
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=#87CEEB:s=1080x1920:d=0.1",
        "-vf",
        "drawtext=text='Available Now!':fontcolor=white:fontsize=64:"
        "x=(w-text_w)/2:y=(h-text_h)/2-140:borderw=3:bordercolor=#4A90D9:"
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf,"
        "drawtext=text='Amazon KDP  |  Etsy':fontcolor=white:fontsize=42:"
        "x=(w-text_w)/2:y=(h-text_h)/2-40:borderw=2:bordercolor=#4A90D9:"
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf,"
        "drawtext=text='Get your copy today!':fontcolor=white:fontsize=36:"
        "x=(w-text_w)/2:y=(h+text_h)/2+60:borderw=2:bordercolor=#4A90D9:"
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "-frames:v", "1", str(out)
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    return out

def create_captioned_slide(image_path, caption_text, output_path, target_w=1080, target_h=1920):
    """
    Scale image to fit the canvas (with padding/letterboxing),
    then overlay caption text.
    """
    # Get original dimensions
    w, h = get_image_size(image_path)
    if w is None or h is None:
        print(f"  WARNING: Could not read {image_path}, skipping")
        return None

    # Calculate scaling to fit within 1080x1920 while maintaining aspect ratio
    scale_w = target_w / w
    scale_h = target_h / h
    scale = min(scale_w, scale_h)  # fit entirely

    new_w = int(w * scale)
    new_h = int(h * scale)
    
    # Pad to 1080x1920
    pad_x = (target_w - new_w) // 2
    pad_y = (target_h - new_h) // 2

    # Build caption with word wrapping
    # For vertical video, split long text into 2 lines
    words = caption_text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if len(test_line) > 30 and current_line:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    if current_line:
        lines.append(current_line)

    # Build drawtext for each line
    drawtext_filters = []
    base_y = target_h - 200  # bottom of screen
    line_height = 60
    
    for i, line in enumerate(lines):
        y_pos = base_y - (len(lines) - 1 - i) * line_height
        # Escape quotes for ffmpeg filter
        escaped = line.replace("'", "'\\\\\\''").replace(":", "\\:").replace("'", "'")
        drawtext_filters.append(
            f"drawtext=text='{line}':fontcolor=white:fontsize=42:"
            f"x=(w-text_w)/2:y={y_pos}:"
            f"borderw=3:bordercolor=#00000080:"
            f"fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        )

    vf_parts = [
        f"scale={new_w}:{new_h}",
        f"pad={target_w}:{target_h}:{pad_x}:{pad_y}:color=#B0E0E6"
    ] + drawtext_filters

    vf_str = ",".join(vf_parts)

    cmd = [
        "ffmpeg", "-y", "-i", str(image_path),
        "-vf", vf_str,
        "-frames:v", "1", str(output_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR creating slide: {result.stderr[:200]}")
        return None
    return output_path

def generate_background_music(output_path, duration_sec):
    """Generate a gentle ambient background music track using sine waves."""
    sample_rate = 44100
    num_samples = int(sample_rate * duration_sec)
    
    # Create a gentle ambient sound with multiple sine waves
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        # Soft pad-like chords: C major (261.63, 329.63, 392.00) with slight detune
        val = (
            0.08 * math.sin(2 * math.pi * 261.63 * t) +  # C4
            0.06 * math.sin(2 * math.pi * 329.63 * t) +  # E4
            0.05 * math.sin(2 * math.pi * 392.00 * t) +  # G4
            0.04 * math.sin(2 * math.pi * 523.25 * t) +  # C5
            0.03 * math.sin(2 * math.pi * 349.23 * t) +  # F4 (slight tension)
            # Soft pad effect with slow tremolo
            0.03 * math.sin(2 * math.pi * 0.5 * t) * math.sin(2 * math.pi * 440.00 * t)
        )
        # Apply fade in/out (first 2 sec, last 2 sec)
        fade_in = min(1.0, t / 2.0)
        fade_out = min(1.0, (duration_sec - t) / 2.0)
        val *= fade_in * fade_out
        # Convert to 16-bit signed integer
        samples.append(int(val * 12000))
    
    # Write WAV file
    wav_path = TMP_DIR / "music.wav"
    with wave.open(str(wav_path), 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(struct.pack(f'<{len(samples)}h', *samples))
    
    # Convert to AAC for video
    aac_path = TMP_DIR / "music.aac"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(wav_path),
        "-c:a", "aac", "-b:a", "128k", str(aac_path)
    ], capture_output=True)
    return aac_path

def build_video():
    print("=" * 60)
    print("Building book trailer: The Little Cloud's Big Adventure")
    print("=" * 60)
    
    # Step 1: Create title and end cards
    print("\n[1/4] Creating title and end cards...")
    title_card = create_title_card()
    end_card = create_end_card()
    print(f"  Title card: {title_card}")
    print(f"  End card: {end_card}")
    
    # Step 2: Create captioned slide images
    print("\n[2/4] Creating captioned slides...")
    slide_images = []
    slide_durations = []
    
    # First slide is title card
    slide_images.append(title_card)
    slide_durations.append(3.0)
    
    for filename, caption, duration in SLIDES:
        src = ILLUSTRATIONS / filename
        if not src.exists():
            print(f"  WARNING: {src} not found, skipping")
            continue
        out = TMP_DIR / f"slide_{filename}"
        print(f"  Processing: {filename} -> '{caption[:40]}...'")
        result = create_captioned_slide(src, caption, out)
        if result:
            slide_images.append(result)
            slide_durations.append(duration)
    
    # Add end card
    slide_images.append(end_card)
    slide_durations.append(4.0)
    
    total_duration = sum(slide_durations)
    print(f"\n  Total slides: {len(slide_images)}, Duration: {total_duration:.1f}s")
    
    # Step 3: Generate background music
    print("\n[3/4] Generating background music...")
    music_path = generate_background_music(OUTPUT, total_duration + 2.0)  # extra for transitions
    print(f"  Music: {music_path}")
    
    # Step 4: Create video with transitions using concat
    print("\n[4/4] Stitching video with transitions...")
    
    # Create an image sequence with crossfade using a concat approach
    # We'll use the concat filter with crossfades
    
    # First, create individual video segments for each slide with the right duration
    segments = []
    for i, (img_path, dur) in enumerate(zip(slide_images, slide_durations)):
        seg_out = TMP_DIR / f"seg_{i:03d}.mp4"
        segments.append(seg_out)
        
        # Create a video segment from the image
        # Add a gentle zoom-in effect for visual interest
        zoom = f"zoompan=z='min(zoom+0.001,1.05)':d={int(dur*25)}:s=1080x1920"
        
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(img_path),
            "-c:v", "libx264", "-t", str(dur),
            "-pix_fmt", "yuv420p", "-r", "25",
            "-vf", zoom,
            "-preset", "ultrafast",
            str(seg_out)
        ]
        subprocess.run(cmd, capture_output=True, text=True)
        print(f"  Segment {i+1}/{len(slide_images)}: {seg_out.name} ({dur}s)")
    
    # Build concat file list
    concat_file = TMP_DIR / "concat_list.txt"
    
    # Apply crossfade between segments using overlay filter
    # Simpler approach: use concat demuxer
    with open(concat_file, 'w') as f:
        for seg in segments:
            f.write(f"file '{seg}'\n")
    
    # First concat all segments
    concat_video = TMP_DIR / "concat_raw.mp4"
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy", str(concat_video)
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    
    # Apply crossfade between segments using frameno approach
    # Simple approach: just use crossfade filter between consecutive segments
    # Since we have up to 14 segments, let's use a simpler approach:
    # concat all, then apply a global fade at start and end
    
    fade_video = TMP_DIR / "concat_faded.mp4"
    fade_duration = 1.0  # 1 second fade in/out
    cmd = [
        "ffmpeg", "-y", "-i", str(concat_video),
        "-vf",
        f"fade=t=in:st=0:d={fade_duration},fade=t=out:st={total_duration-fade_duration}:d={fade_duration}",
        "-af",
        f"afade=t=in:st=0:d={fade_duration},afade=t=out:st={total_duration-fade_duration}:d={fade_duration}",
        "-c:a", "aac", "-b:a", "128k",
        str(fade_video)
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    
    # Now mix in background music
    # First get the audio from fade_video (silent since we didn't add audio yet)
    # Actually, the video has no audio track. Let's add music.
    
    # Add music as background track, slightly quieter
    final_video = OUTPUT
    cmd = [
        "ffmpeg", "-y",
        "-i", str(fade_video),
        "-i", str(music_path),
        "-filter_complex",
        "[1:a]volume=0.3[a1]",  # reduce music volume
        "-map", "0:v:0",
        "-map", "[a1]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest", str(final_video)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr[:500]}")
        return False
    
    print(f"\n✅ Trailer created: {final_video}")
    print(f"   Duration: {total_duration:.1f}s")
    print(f"   Resolution: 1080x1920")
    
    # Get file size
    size_mb = os.path.getsize(final_video) / (1024 * 1024)
    print(f"   File size: {size_mb:.1f} MB")
    
    return True

if __name__ == "__main__":
    success = build_video()
    if not success:
        print("\n❌ Failed to build trailer")
        exit(1)