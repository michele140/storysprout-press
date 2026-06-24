#!/usr/bin/env python3
"""
Build Outlaw Book 1: The Great Canyon Crossing — KDP-ready PDF + Wraparound Cover
6" x 9" chapter book, grayscale interior, cream paper aesthetic
"""

import os, re, glob, math
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Image, PageBreak, Spacer,
    Table, TableStyle, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage

# ─── Paths ───────────────────────────────────────────────────────────────
OUTPUT_DIR = "/home/team/shared"
MANUSCRIPT = os.path.join(OUTPUT_DIR, "outlaw-book1.md")
ILLUS_DIR = os.path.join(OUTPUT_DIR, "outlaw-illustrations")
TEMPDIR = os.path.join(OUTPUT_DIR, ".tmp_build")
os.makedirs(TEMPDIR, exist_ok=True)

# ─── Layout Constants ───────────────────────────────────────────────────
TRIM_W = 6.0 * inch
TRIM_H = 9.0 * inch
MARGIN = 0.75 * inch
TEXT_W = TRIM_W - 2 * MARGIN
TEXT_H = TRIM_H - 2 * MARGIN
BLEED = 0.125 * inch

FONT_BODY = "Times-Roman"
FONT_BOLD = "Times-Bold"
FONT_ITALIC = "Times-Italic"

PAGE_ESTIMATE = 60

# ─── Colors ──────────────────────────────────────────────────────────────
NAVY = HexColor("#1B2A4A")
GOLD = HexColor("#D4A843")
SUNSET_TOP = HexColor("#FF6B35")
SUNSET_MID = HexColor("#D4432A")
SUNSET_BOT = HexColor("#7B1E2B")
DARK_BG = HexColor("#1A1A2E")
CREAM = HexColor("#FFF8E7")


# ═══════════════════════════════════════════════════════════════════════════
# PART 1: PARSE MANUSCRIPT
# ═══════════════════════════════════════════════════════════════════════════

def strip_nonascii(text):
    """Remove non-ASCII characters (emojis, smart quotes, etc.)."""
    return re.sub(r'[^\x20-\x7E\n]', '', text)


def parse_manuscript(filepath):
    """Parse the manuscript into chapters with text and illustration markers."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    text = strip_nonascii(text)

    # Split on ## headings
    sections = re.split(r'^## ', text, flags=re.MULTILINE)

    chapters = []
    chapter_num = 0
    dedication_text = None
    preamble_done = False

    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue

        lines = sec.split('\n')
        heading = lines[0].strip().rstrip('#').strip()
        body = '\n'.join(lines[1:]).strip()

        # Handle title
        if heading.startswith('# ') or heading.startswith('# Outlaw'):
            heading = heading.lstrip('#').strip()
            if heading == 'Outlaw: The Great Canyon Crossing':
                continue  # skip title line, handled in the page layout

        # Handle dedication
        if heading == 'Dedication':
            dedication_text = body
            continue

        # Everything else is a chapter heading
        chapter_num += 1
        ch_title = f"Chapter {chapter_num}: {heading}" if not heading.startswith('Chapter') else heading

        # Extract illustration markers
        illus_descriptions = re.findall(r'\[Illustration:(.*?)\]', body)
        text_parts = re.split(r'\[Illustration:.*?\]', body)
        text_parts = [p.strip() for p in text_parts]

        ch = {
            'type': 'chapter',
            'num': chapter_num,
            'title': ch_title,
            'text_parts': text_parts,
            'illus_count': len(illus_descriptions),
        }
        chapters.append(ch)

    # Generate illustration filenames for each chapter
    for ch in chapters:
        if ch['type'] == 'chapter':
            ch['illus_files'] = []
            for i in range(ch['illus_count']):
                fname = f"ch{ch['num']:02d}-{i+1:02d}.png"
                fpath = os.path.join(ILLUS_DIR, fname)
                ch['illus_files'].append(fpath if os.path.exists(fpath) else None)

    return chapters, dedication_text


# ═══════════════════════════════════════════════════════════════════════════
# PART 2: STYLES
# ═══════════════════════════════════════════════════════════════════════════

def build_styles():
    styles = {}

    styles['ChapterTitle'] = ParagraphStyle(
        'ChapterTitle', fontName=FONT_BOLD, fontSize=20,
        leading=28, alignment=TA_CENTER, spaceAfter=24, textColor=black
    )

    styles['ChapterNumber'] = ParagraphStyle(
        'ChapterNumber', fontName=FONT_BOLD, fontSize=14,
        leading=20, alignment=TA_CENTER, spaceAfter=6,
        textColor=HexColor("#666666")
    )

    styles['Body'] = ParagraphStyle(
        'Body', fontName=FONT_BODY, fontSize=13,
        leading=19.5, alignment=TA_JUSTIFY,
        spaceAfter=8, textColor=black
    )

    styles['Title'] = ParagraphStyle(
        'Title', fontName=FONT_BOLD, fontSize=28,
        leading=36, alignment=TA_CENTER, spaceAfter=12, textColor=black
    )

    styles['Subtitle'] = ParagraphStyle(
        'Subtitle', fontName=FONT_ITALIC, fontSize=16,
        leading=22, alignment=TA_CENTER, spaceAfter=6,
        textColor=HexColor("#555555")
    )

    styles['Copyright'] = ParagraphStyle(
        'Copyright', fontName=FONT_BODY, fontSize=9,
        leading=13, alignment=TA_CENTER, textColor=HexColor("#888888")
    )

    styles['Dedication'] = ParagraphStyle(
        'Dedication', fontName=FONT_ITALIC, fontSize=14,
        leading=20, alignment=TA_CENTER, textColor=HexColor("#555555")
    )

    styles['TOC'] = ParagraphStyle(
        'TOC', fontName=FONT_BODY, fontSize=12,
        leading=22, alignment=TA_LEFT, leftIndent=20, textColor=black
    )

    styles['TOCChapter'] = ParagraphStyle(
        'TOCChapter', fontName=FONT_BOLD, fontSize=12,
        leading=22, alignment=TA_LEFT, textColor=black
    )

    styles['CharDesc'] = ParagraphStyle(
        'CharDesc', fontName=FONT_BODY, fontSize=12,
        leading=18, alignment=TA_LEFT, spaceAfter=12,
        leftIndent=18, rightIndent=18, textColor=black
    )

    return styles


# ═══════════════════════════════════════════════════════════════════════════
# PART 3: BUILD INTERIOR PDF
# ═══════════════════════════════════════════════════════════════════════════

def make_grayscale_copy(src_path, dst_path, max_width=300):
    """Convert a color PNG to grayscale and resize."""
    if not src_path or not os.path.exists(src_path):
        return None
    try:
        img = PILImage.open(src_path).convert('L')
        w, h = img.size
        ratio = max_width / w
        new_w = int(w * ratio)
        new_h = int(h * ratio)
        img = img.resize((new_w, new_h), PILImage.LANCZOS)
        img.save(dst_path, 'PNG')
        return dst_path
    except Exception as e:
        print(f"  [WARN] Could not process {src_path}: {e}")
        return None


def clean_text(text):
    """Clean up text for PDF rendering."""
    text = text.replace('--', '&mdash;')
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    # Italic
    text = re.sub(r'\*(\w[^*]*\w)\*', r'<i>\1</i>', text)
    text = re.sub(r'_(\w[^_]*\w)_', r'<i>\1</i>', text)
    # Bold
    text = re.sub(r'\*\*(\w[^*]*\w)\*\*', r'<b>\1</b>', text)
    return text


def split_into_paragraphs(text):
    """Split text into paragraphs at blank lines."""
    paragraphs = []
    current = []
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            if current:
                paragraphs.append('\n'.join(current))
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append('\n'.join(current))
    return paragraphs if paragraphs else [text]


def build_interior_pdf(chapters, dedication_text, styles, output_path):
    """Build the 6x9 interior PDF using platypus."""
    print("Building interior PDF...")

    # Convert all illustrations to grayscale
    grayscale_illus = {}
    for ch in chapters:
        for i, fp in enumerate(ch['illus_files']):
            if fp:
                dst = os.path.join(TEMPDIR, f"gs_ch{ch['num']:02d}_{i+1:02d}.png")
                result = make_grayscale_copy(fp, dst, TEXT_W * 0.92)
                grayscale_illus[(ch['num'], i)] = result

    doc = SimpleDocTemplate(
        output_path,
        pagesize=(TRIM_W, TRIM_H),
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="Outlaw: The Great Canyon Crossing",
        author="StorySprout Press",
        subject="Children's Chapter Book"
    )

    story = []

    # ── Page 1: Title Page ──
    story.append(Spacer(1, TRIM_H * 0.25))
    story.append(Paragraph("OUTLAW", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("The Great Canyon Crossing", styles['Subtitle']))
    story.append(Spacer(1, 36))
    story.append(Paragraph("A Wild Horse Adventure", styles['Subtitle']))
    story.append(Spacer(1, 48))
    story.append(Paragraph("StorySprout Press", ParagraphStyle(
        'Author', fontName=FONT_BOLD, fontSize=14,
        leading=20, alignment=TA_CENTER, textColor=HexColor("#333333")
    )))

    # ── Page 2: Dedication Page ──
    story.append(PageBreak())
    story.append(Spacer(1, TRIM_H * 0.3))
    if dedication_text:
        ded_clean = clean_text(dedication_text)
        for line in ded_clean.split('\n'):
            line = line.strip()
            if line:
                story.append(Paragraph(line, styles['Dedication']))
                story.append(Spacer(1, 8))
    else:
        story.append(Paragraph("For every wild heart that longs to run free", styles['Dedication']))

    # ── Page 3: Copyright Page ──
    story.append(PageBreak())
    story.append(Spacer(1, TRIM_H * 0.15))
    copyright_lines = [
        "Outlaw: The Great Canyon Crossing",
        "Outlaw Wild Horse Series, Book 1",
        "",
        "Published by StorySprout Press",
        "",
        "Copyright &copy; 2026 StorySprout Press",
        "All rights reserved.",
        "",
        "No part of this book may be reproduced or transmitted",
        "in any form or by any means without written permission",
        "from the publisher.",
        "",
        "ISBN: 978-0-000-00000-0 (print)",
        "ISBN: 978-0-000-00000-0 (ebook)",
        "",
        "Printed in the United States of America",
        "",
        "First Edition: June 2026",
        "",
        "10 9 8 7 6 5 4 3 2 1"
    ]
    for line in copyright_lines:
        if not line:
            story.append(Spacer(1, 4))
        else:
            story.append(Paragraph(line, styles['Copyright']))

    # ── Page 4: Table of Contents ──
    story.append(PageBreak())
    story.append(Spacer(1, 24))
    story.append(Paragraph("Contents", styles['ChapterTitle']))
    story.append(Spacer(1, 18))

    story.append(Paragraph("<b>Meet the Herd</b>", styles['TOCChapter']))
    story.append(Paragraph("Character Introductions", styles['TOC']))
    story.append(Spacer(1, 8))

    for ch in chapters:
        story.append(Paragraph(f"<b>{ch['title']}</b>", styles['TOCChapter']))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 18))
    story.append(Paragraph("<b>About the Author</b>", styles['TOCChapter']))

    # ── Page 5: Meet the Herd ──
    story.append(PageBreak())
    story.append(Spacer(1, 30))
    story.append(Paragraph("Meet the Herd", styles['ChapterTitle']))
    story.append(Spacer(1, 16))

    characters = [
        ("Outlaw", "A magnificent black stallion with a midnight coat and a brave heart. The leader of the herd."),
        ("Sunny", "A wise golden palomino mare who has seen many winters. Outlaw's most trusted friend."),
        ("Swift", "A young bay colt full of energy and excitement. Always ready for adventure."),
        ("Bramble", "A sturdy grey gelding with steady feet and a calm soul. Keeps watch at the rear."),
        ("Clover", "A curious sorrel filly who loves to explore the world around her."),
        ("Shadow", "A powerful black-and-white paint stallion with a mean streak -- but a hidden heart."),
    ]
    for name, desc in characters:
        story.append(Paragraph(f"<b>{name}</b> &mdash; {desc}", styles['CharDesc']))

    # ── Chapters ──
    for ch in chapters:
        story.append(PageBreak())

        # Chapter title page section
        story.append(Spacer(1, TRIM_H * 0.2))
        story.append(Paragraph(f"Chapter {ch['num']}", styles['ChapterNumber']))
        story.append(Paragraph(ch['title'], styles['ChapterTitle']))
        story.append(Spacer(1, 10))
        story.append(Paragraph("<i>* * *</i>", ParagraphStyle(
            'dec', fontName=FONT_ITALIC, fontSize=10,
            alignment=TA_CENTER, textColor=HexColor("#888888")
        )))
        story.append(Spacer(1, 20))

        # Interleave text parts and illustrations
        for i, text_part in enumerate(ch['text_parts']):
            if not text_part.strip():
                continue

            # Render text paragraphs
            paragraphs = split_into_paragraphs(text_part)
            for para in paragraphs:
                para = clean_text(para)
                if para.strip():
                    story.append(Paragraph(para, styles['Body']))

            # After rendering this text part, place the matching illustration
            # (text_part[i] goes before illus[i])
            if i < ch['illus_count']:
                illus_key = (ch['num'], i)
                if illus_key in grayscale_illus and grayscale_illus[illus_key]:
                    img_path = grayscale_illus[illus_key]
                    try:
                        with PILImage.open(img_path) as img:
                            iw, ih = img.size
                        scale = min(TEXT_W * 0.95 / iw, 220 / ih)
                        iw2 = iw * scale
                        ih2 = ih * scale
                        report_img = Image(img_path, width=iw2, height=ih2)
                        story.append(Spacer(1, 10))
                        story.append(report_img)
                        story.append(Spacer(1, 10))
                    except Exception as e:
                        print(f"  [WARN] Could not add image {img_path}: {e}")

    # ── About the Author ──
    story.append(PageBreak())
    story.append(Spacer(1, TRIM_H * 0.15))
    story.append(Paragraph("About the Author", styles['ChapterTitle']))
    story.append(Spacer(1, 20))
    author_bio = (
        "StorySprout Press creates charming, adventurous chapter books "
        "for young readers who love animals, nature, and epic journeys. "
        "The Outlaw Wild Horse Series was inspired by the wild mustangs "
        "of the American West -- their freedom, their courage, and their "
        "unbreakable spirit."
    )
    story.append(Paragraph(author_bio, styles['Body']))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "Coming soon: Outlaw Book 2 &mdash; <i>The Secret of the Silver Canyon</i>",
        ParagraphStyle('Preview', fontName=FONT_ITALIC, fontSize=12,
                       leading=18, alignment=TA_CENTER, textColor=HexColor("#555555"))
    ))

    print("  Rendering...")
    doc.build(story)
    print(f"  Done! PDF saved to {output_path}")
    return output_path


# ═══════════════════════════════════════════════════════════════════════════
# PART 4: BUILD COVER PDF
# ═══════════════════════════════════════════════════════════════════════════

def build_cover_pdf(output_path):
    """Build the wraparound cover PDF."""
    print("Building wraparound cover...")

    spine_pt = 0.002252 * PAGE_ESTIMATE * inch
    if spine_pt < 0.125 * inch:
        spine_pt = 0.125 * inch

    COVER_W = TRIM_W + spine_pt + TRIM_W
    COVER_H = TRIM_H + 2 * BLEED

    c = canvas.Canvas(output_path, pagesize=(COVER_W, COVER_H))

    # ── Full background ──
    c.setFillColor(NAVY)
    c.rect(0, 0, COVER_W, COVER_H, stroke=0, fill=1)

    # Front cover area
    fx0 = TRIM_W + spine_pt
    fy0 = 0

    # ── Sunset gradient (front cover) ──
    bands = 80
    for i in range(bands):
        t = i / bands
        r = SUNSET_BOT.red + (SUNSET_TOP.red - SUNSET_BOT.red) * t
        g = SUNSET_BOT.green + (SUNSET_TOP.green - SUNSET_BOT.green) * t
        b = SUNSET_BOT.blue + (SUNSET_TOP.blue - SUNSET_BOT.blue) * t
        c.setFillColor(Color(r, g, b))
        y = fy0 + (COVER_H) * t / bands
        h = COVER_H / bands + 1
        c.rect(fx0, y, COVER_W - fx0, h, stroke=0, fill=1)

    # ── Sun (large, glowing) ──
    sun_cx = fx0 + (COVER_W - fx0) * 0.65
    sun_cy = COVER_H * 0.55
    sun_r = 1.2 * inch

    # Outer glow rings
    for g in range(10, 0, -1):
        alpha = 0.06 * g
        c.setFillColor(Color(1, 0.85, 0.3, alpha=alpha))
        c.circle(sun_cx, sun_cy, sun_r + g * 0.12 * inch, stroke=0, fill=1)

    # Sun body
    c.setFillColor(HexColor("#FFD700"))
    c.circle(sun_cx, sun_cy, sun_r, stroke=0, fill=1)

    # Inner brightness
    c.setFillColor(HexColor("#FFF8DC"))
    c.circle(sun_cx, sun_cy, sun_r * 0.4, stroke=0, fill=1)

    # ── Canyon silhouettes ──
    def draw_canyon_ridge(c, x0, x1, y_base, color, peak_factor=1.0):
        c.setFillColor(color)
        p = c.beginPath()
        p.moveTo(x0, y_base)
        # Create a canyon skyline with multiple peaks
        points = [
            (0.05, 0.4), (0.08, 0.6), (0.12, 0.8), (0.15, 1.2),
            (0.18, 0.9), (0.22, 1.1), (0.25, 1.5), (0.28, 1.0),
            (0.32, 1.3), (0.35, 1.8), (0.38, 1.4), (0.42, 1.0),
            (0.45, 1.6), (0.48, 0.8), (0.52, 1.4), (0.55, 2.0),
            (0.58, 1.5), (0.62, 0.9), (0.65, 1.7), (0.68, 1.1),
            (0.72, 1.5), (0.75, 0.7), (0.78, 1.2), (0.82, 0.5),
            (0.85, 0.9), (0.88, 0.4), (0.92, 0.6), (0.95, 0.3),
            (1.0, 0.2)
        ]
        for frac_x, height in points:
            px = x0 + (x1 - x0) * frac_x
            py = y_base + height * 0.3 * inch * peak_factor
            p.lineTo(px, py)
        p.lineTo(x1, y_base)
        p.close()
        c.drawPath(p, stroke=0, fill=1)

    # Draw canyon layers
    draw_canyon_ridge(c, fx0, COVER_W, 0, HexColor("#1A1A2E"), 1.0)
    draw_canyon_ridge(c, fx0, COVER_W, COVER_H * 0.1, HexColor("#2D1B2E"), 0.7)
    draw_canyon_ridge(c, fx0, COVER_W, COVER_H * 0.05, HexColor("#3D1B1E"), 0.5)

    # ── Horse silhouette (simplified but recognizable) ──
    # Use a polygon approach for a cleaner horse shape
    horse_x = fx0 + (COVER_W - fx0) * 0.35
    horse_y = COVER_H * 0.2

    c.setFillColor(black)
    p = c.beginPath()

    # Head to back (facing right)
    p.moveTo(horse_x + 0.05*inch, horse_y + 0.8*inch)
    p.curveTo(horse_x + 0.15*inch, horse_y + 0.95*inch,
              horse_x + 0.25*inch, horse_y + 0.85*inch,
              horse_x + 0.3*inch, horse_y + 0.7*inch)   # nose
    p.curveTo(horse_x + 0.28*inch, horse_y + 0.6*inch,
              horse_x + 0.25*inch, horse_y + 0.5*inch,
              horse_x + 0.2*inch, horse_y + 0.3*inch)   # neck down
    p.lineTo(horse_x + 0.25*inch, horse_y)              # front leg
    p.lineTo(horse_x + 0.2*inch, horse_y)               # hoof
    p.lineTo(horse_x + 0.15*inch, horse_y + 0.15*inch)  # leg up
    p.lineTo(horse_x + 0.1*inch, horse_y + 0.1*inch)    # belly
    p.lineTo(horse_x + 0.05*inch, horse_y)              # back leg
    p.lineTo(horse_x - 0.0*inch, horse_y)               # hoof
    p.lineTo(horse_x - 0.05*inch, horse_y + 0.2*inch)   # leg up
    p.curveTo(horse_x - 0.15*inch, horse_y + 0.25*inch,
              horse_x - 0.25*inch, horse_y + 0.3*inch,
              horse_x - 0.3*inch, horse_y + 0.25*inch)  # hindquarters
    p.curveTo(horse_x - 0.4*inch, horse_y + 0.35*inch,
              horse_x - 0.45*inch, horse_y + 0.5*inch,
              horse_x - 0.4*inch, horse_y + 0.6*inch)   # tail
    p.curveTo(horse_x - 0.35*inch, horse_y + 0.55*inch,
              horse_x - 0.3*inch, horse_y + 0.5*inch,
              horse_x - 0.25*inch, horse_y + 0.45*inch) # tail curve back
    p.curveTo(horse_x - 0.15*inch, horse_y + 0.5*inch,
              horse_x - 0.05*inch, horse_y + 0.6*inch,
              horse_x + 0.0*inch, horse_y + 0.7*inch)   # back to neck
    p.curveTo(horse_x + 0.02*inch, horse_y + 0.75*inch,
              horse_x + 0.03*inch, horse_y + 0.78*inch,
              horse_x + 0.05*inch, horse_y + 0.8*inch)  # ear
    p.close()
    c.drawPath(p, stroke=0, fill=1)

    # ── Title on cover ──
    title_x = fx0 + (COVER_W - fx0) * 0.5
    title_y = COVER_H * 0.75

    # Title shadow
    c.setFillColor(black)
    c.setFont(FONT_BOLD, 38)
    c.drawCentredString(title_x + 1, title_y - 1, "OUTLAW")

    c.setFillColor(white)
    c.setFont(FONT_BOLD, 38)
    c.drawCentredString(title_x, title_y, "OUTLAW")

    c.setFillColor(HexColor("#FFE4B5"))
    c.setFont(FONT_ITALIC, 18)
    c.drawCentredString(title_x, title_y - 34, "The Great Canyon Crossing")

    c.setFillColor(GOLD)
    c.setFont(FONT_ITALIC, 13)
    c.drawCentredString(title_x, title_y - 56, "A Wild Horse Adventure")

    # ── Spine ──
    spine_cx = TRIM_W + spine_pt / 2
    c.saveState()
    c.translate(spine_cx, COVER_H / 2)
    c.rotate(90)
    c.setFillColor(GOLD)
    c.setFont(FONT_BOLD, 13)
    c.drawCentredString(0, 0, "OUTLAW")
    c.setFillColor(HexColor("#DDDDDD"))
    c.setFont(FONT_ITALIC, 8)
    c.drawCentredString(0, -15, "StorySprout Press")
    c.restoreState()

    # ── Back Cover ──
    back_cx = TRIM_W / 2
    back_top = COVER_H * 0.75

    c.setFillColor(white)
    c.setFont(FONT_BOLD, 14)
    c.drawCentredString(back_cx, back_top, "OUTLAW")

    c.setFillColor(GOLD)
    c.setFont(FONT_ITALIC, 11)
    c.drawCentredString(back_cx, back_top - 18, "The Great Canyon Crossing")

    # Divider line
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(back_cx - 1.0*inch, back_top - 25, back_cx + 1.0*inch, back_top - 25)

    blurb_lines = [
        ("The first frost has arrived, and the herd must", 11),
        ("reach the Hidden Valley before the blizzard hits.", 11),
        ("But the path leads through the treacherous", 11),
        ("Painted Canyon -- where a rival stallion", 11),
        ("challenges Outlaw's leadership at every turn.", 11),
        ("", 0),
        ("With danger lurking around every bend and", 11),
        ("a flash flood threatening to sweep them away,", 11),
        ("can Outlaw bring his herd to safety in time?", 11),
        ("", 0),
        ("A wild horse adventure for ages 6-9.", 12),
    ]

    c.setFillColor(HexColor("#DDDDDD"))
    line_y = back_top - 40
    for text, size in blurb_lines:
        if text:
            c.setFont(FONT_BODY, size)
            c.drawCentredString(back_cx, line_y, text)
        line_y -= 15

    # Barcode area
    bar_y = 0.7 * inch
    bar_w = 1.5 * inch
    bar_h = 1.0 * inch
    c.setFillColor(white)
    c.roundRect(back_cx - bar_w/2, bar_y, bar_w, bar_h, 4, stroke=0, fill=1)
    c.setStrokeColor(HexColor("#999999"))
    c.setLineWidth(0.5)
    c.roundRect(back_cx - bar_w/2, bar_y, bar_w, bar_h, 4, stroke=1, fill=0)

    c.setFillColor(HexColor("#888888"))
    c.setFont(FONT_BODY, 7)
    c.drawCentredString(back_cx, bar_y + 0.12*inch, "PLACE BARCODE HERE")
    c.drawCentredString(back_cx, bar_y - 0.12*inch, "ISBN 978-0-000-00000-0")

    c.setFillColor(HexColor("#999999"))
    c.setFont(FONT_ITALIC, 9)
    c.drawCentredString(back_cx, 0.35*inch, "StorySprout Press")

    c.save()
    print(f"  Cover saved to {output_path}")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("OUTLAW BOOK 1: KDP BUILD")
    print("=" * 60)

    print("\n1. Parsing manuscript...")
    chapters, dedication_text = parse_manuscript(MANUSCRIPT)
    print(f"   Found {len(chapters)} chapters")
    for ch in chapters:
        print(f"   Ch {ch['num']}: {ch['title']} ({ch['illus_count']} illus)")
    if dedication_text:
        ded_short = strip_nonascii(dedication_text)[:60]
        print(f"   Dedication: \"{ded_short}...\"")

    print("\n2. Building styles...")
    styles = build_styles()

    print("\n3. Building interior PDF...")
    interior_path = os.path.join(OUTPUT_DIR, "outlaw-book1-kdp.pdf")
    build_interior_pdf(chapters, dedication_text, styles, interior_path)

    print("\n4. Building wraparound cover...")
    cover_path = os.path.join(OUTPUT_DIR, "outlaw-book1-cover.pdf")
    build_cover_pdf(cover_path)

    print("\n" + "=" * 60)
    print("BUILD COMPLETE!")
    print(f"  Interior: {interior_path}")
    print(f"  Cover:    {cover_path}")
    for path in [interior_path, cover_path]:
        if os.path.exists(path):
            size_kb = os.path.getsize(path) / 1024
            print(f"  Size:     {size_kb:.1f} KB")