#!/usr/bin/env python3
"""
Build a print-ready PDF for "The Little Cloud's Big Adventure" 
for Amazon KDP submission (8.5" x 8.5" square, 300 DPI, with 0.125" bleeds).
"""
import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch

# --- Configuration ---
TRIM_WIDTH = 8.5 * inch       # 8.5 inches
TRIM_HEIGHT = 8.5 * inch      # 8.5 inches
BLEED = 0.125 * inch           # 0.125 inch bleed
PAGE_WIDTH = TRIM_WIDTH + 2 * BLEED   # 8.75 inches
PAGE_HEIGHT = TRIM_HEIGHT + 2 * BLEED  # 8.75 inches

DPI = 300
# At 300 DPI, page in points: 8.75" = 630pt, 8.75" = 630pt
# Image sizes: 1024x1024 px
# We need to place them at print resolution
# At 300 DPI, 8.5" = 2550px, so images at 1024px are ~3.41" at 300 DPI
# We'll upscale them to fill the trim area with some margin

TMP = '/home/team/shared/.tmp_build'
os.makedirs(TMP, exist_ok=True)

IMG_DIR = '/home/team/shared/storybook-illustrations'
MANUSCRIPT_FILE = '/home/team/shared/little-cloud-adventure.md'
OUTPUT_FILE = '/home/team/shared/storybook-kdp-ready.pdf'

# Story text from the manuscript (page by page, excluding title page)
STORY_TEXT = {
    1: "",  # Page 1 is title page - text on cover
    2: "Once upon a time, high above the hills, lived a little cloud named Cirrus.",
    3: "Cirrus was fluffy. Cirrus was white. But most of all, Cirrus was curious.",
    4: '"What is it like down there?" Cirrus wondered. "Can a little cloud like me help the world?"',
    5: "He saw a little garden where the flowers were drooping. They looked very thirsty.",
    6: "Cirrus tried to squeeze out some rain. *Squeeze! Squeeze! Squeeze!*",
    7: "But only one tiny *plip* fell. It wasn't enough to help the thirsty flowers.",
    8: '"I am too small," Cirrus sighed. He felt very droopy himself.',
    9: '"Don\'t be sad, Cirrus," said Sunny the Sun. "Everyone has a special job to do."',
    10: 'Just then, Gusty the Breeze whizzed by. "Want to see something cool?" Gusty asked.',
    11: "Gusty blew and Cirrus flew! They zipped over the hills and over the trees.",
    12: "They stopped over a playground. The sun was very hot, and the children were tired.",
    13: "Cirrus floated right in front of the sun. He made a big, cool shadow on the ground.",
    14: '"Ooh, shade!" cried a little girl. "Thank you, little cloud!"',
    15: "Cirrus beamed. He had helped! Providing shade was a very important job.",
    16: "But Cirrus still wanted to make rain. He met his friend Drippy.",
    17: '"To make rain, you must gather your friends," Drippy explained. "We work better together!"',
    18: "They floated over a big brown field where a farmer was waiting.",
    19: "Cirrus, Drippy, and all their cloud friends huddle together. They grew bigger and darker.",
    20: "*Pitter-patter, pitter-patter!* The rain began to fall.",
    21: "The field turned green, and the farmer was happy. Cirrus had helped make a big difference!",
    22: "As the rain stopped, a beautiful rainbow stretched across the sky.",
    23: "Cirrus felt very special. He knew that even a little cloud could do big things.",
    24: 'That night, Cirrus turned a lovely shade of pink and orange as the sun went down.\n"I can\'t wait for tomorrow\'s adventure," he whispered.',
}


def make_page_bg(c, width, height):
    """Draw a white background with a trim box guide."""
    # White background
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, width, height, fill=1, stroke=0)


def add_text_on_page(c, text, page_width, page_height, trim_width, trim_height, bleed):
    """Add story text at the bottom of the page within the trim area."""
    if not text:
        return
    
    # Calculate trim area boundaries
    trim_left = bleed
    trim_bottom = bleed
    trim_right = bleed + trim_width
    trim_top = bleed + trim_height
    
    # Text box: centered horizontally, near bottom of trim area
    text_margin = 20  # pt from trim edge
    text_x = trim_left + text_margin
    text_width = trim_width - 2 * text_margin
    text_y = trim_bottom + text_margin + 40  # room for font
    
    # Font
    c.setFont("Helvetica", 16)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    
    # Draw a semi-transparent text background for readability
    text_bg_margin = 10
    c.setFillColorRGB(1, 1, 1, alpha=0.7)
    c.roundRect(
        trim_left + text_margin - text_bg_margin,
        trim_bottom + text_margin,
        text_width + 2 * text_bg_margin,
        80,
        8,
        fill=1,
        stroke=0
    )
    
    # Draw text
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.setFont("Helvetica", 16)
    
    # Handle multi-line text
    lines = text.split('\n')
    line_y = text_y + 55
    for line in lines:
        c.drawString(text_x + 10, line_y, line)
        line_y -= 22


def add_page_number(c, page_num, page_width, page_height, trim_width, trim_height, bleed):
    """Add page number centered at bottom of trim area."""
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawCentredString(
        bleed + trim_width / 2,
        bleed + 15,
        str(page_num)
    )


def build_storybook_pdf():
    print(f"Building storybook PDF: {OUTPUT_FILE}")
    print(f"Page size: {PAGE_WIDTH/72:.2f}\" x {PAGE_HEIGHT/72:.2f}\" (with bleed)")
    print(f"Trim size: {TRIM_WIDTH/72:.2f}\" x {TRIM_HEIGHT/72:.2f}\"")
    
    c = canvas.Canvas(OUTPUT_FILE, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    # --- FRONT COVER ---
    print("Adding front cover...")
    cover_path = os.path.join(IMG_DIR, 'front-cover.png')
    cover_img = Image.open(cover_path).convert('RGB')
    # Upscale cover to fill page
    cover_img = cover_img.resize(
        (int(PAGE_WIDTH), int(PAGE_HEIGHT)),
        Image.LANCZOS
    )
    cover_img_path = os.path.join(TMP, 'front-cover-resized.jpg')
    cover_img.save(cover_img_path, 'JPEG', quality=95)
    c.drawImage(cover_img_path, 0, 0, width=PAGE_WIDTH, height=PAGE_HEIGHT)
    
    # Title on front cover
    c.setFillColorRGB(0.9, 0.9, 0.95)
    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 120, "The Little Cloud's")
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 170, "Big Adventure")
    
    # Author credit
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.7, 0.7, 0.8)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 210, "A StorySprout Press Book")
    
    c.showPage()
    
    # --- INSIDE PAGES (Page 1 = Title page, Pages 2-24 = Story pages) ---
    for page_num in range(1, 25):
        print(f"Adding page {page_num}...")
        
        # Get image
        img_path = os.path.join(IMG_DIR, f'page-{page_num:02d}.png')
        if not os.path.exists(img_path):
            print(f"WARNING: {img_path} not found, using white page")
            make_page_bg(c, PAGE_WIDTH, PAGE_HEIGHT)
        else:
            img = Image.open(img_path).convert('RGB')
            # Upscale to fill page
            img = img.resize(
                (int(PAGE_WIDTH), int(PAGE_HEIGHT)),
                Image.LANCZOS
            )
            img_temp = os.path.join(TMP, f'page-{page_num:02d}.jpg')
            img.save(img_temp, 'JPEG', quality=95)
            c.drawImage(img_temp, 0, 0, width=PAGE_WIDTH, height=PAGE_HEIGHT)
        
        # Add story text on the page (only for story pages, not title page)
        if page_num in STORY_TEXT:
            text = STORY_TEXT[page_num]
            if text:
                add_text_on_page(c, text, PAGE_WIDTH, PAGE_HEIGHT, 
                                TRIM_WIDTH, TRIM_HEIGHT, BLEED)
        
        # Page number (skip for title page 1)
        if page_num > 1:
            add_page_number(c, page_num, PAGE_WIDTH, PAGE_HEIGHT,
                          TRIM_WIDTH, TRIM_HEIGHT, BLEED)
        
        c.showPage()
    
    # --- BACK COVER ---
    print("Adding back cover...")
    back_cover_path = os.path.join(IMG_DIR, 'back-cover.png')
    if os.path.exists(back_cover_path):
        back_img = Image.open(back_cover_path).convert('RGB')
        back_img = back_img.resize(
            (int(PAGE_WIDTH), int(PAGE_HEIGHT)),
            Image.LANCZOS
        )
        back_img_path = os.path.join(TMP, 'back-cover-resized.jpg')
        back_img.save(back_img_path, 'JPEG', quality=95)
        c.drawImage(back_img_path, 0, 0, width=PAGE_WIDTH, height=PAGE_HEIGHT)
    else:
        make_page_bg(c, PAGE_WIDTH, PAGE_HEIGHT)
    
    # Blurb on back cover
    c.setFillColorRGB(0.1, 0.1, 0.2)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 100, "About the Story")
    
    blurb = ("Join Cirrus the little cloud on a heartwarming adventure\n"
             "through the sky! From helping thirsty gardens to providing\n"
             "shade for playing children, Cirrus learns that even the\n"
             "smallest cloud can make a big difference.\n\n"
             "With friends like Sunny, Gusty, and Drippy by his side,\n"
             "Cirrus discovers the power of working together and the\n"
             "joy of helping others.\n\n"
             "Perfect for children ages 2-6, this charming tale teaches\n"
             "kindness, perseverance, and the beauty of friendship.")
    
    c.setFont("Helvetica", 14)
    text_lines = blurb.split('\n')
    y = PAGE_HEIGHT - 140
    for line in text_lines:
        c.drawCentredString(PAGE_WIDTH / 2, y, line)
        y -= 22
    
    # ISBN / Barcode area
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawCentredString(PAGE_WIDTH / 2, 60, "StorySprout Press")
    
    c.showPage()
    
    # --- SAVE ---
    c.save()
    print(f"PDF saved to: {OUTPUT_FILE}")
    file_size = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"File size: {file_size:.1f} MB")

pt = 1  # 1 point = 1/72 inch, ReportLab uses points natively

if __name__ == '__main__':
    build_storybook_pdf()