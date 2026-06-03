#!/usr/bin/env python3
"""
Build print-ready PDF for "Little Cloud's Big Activity Book" for Amazon KDP (8.5"x11")
and a digital download ZIP for Etsy.
"""
import os, shutil, zipfile, tempfile
from PIL import Image

TMP = '/home/team/shared/.tmp_build'
os.makedirs(TMP, exist_ok=True)
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

# Config
TRIM_W = 8.5 * inch
TRIM_H = 11.0 * inch
BLEED = 0.125 * inch
PAGE_W = TRIM_W + 2 * BLEED
PAGE_H = TRIM_H + 2 * BLEED

IMG_DIR = '/home/team/shared/activity-book-pages'
OUTPUT_KDP = '/home/team/shared/activity-book-kdp-ready.pdf'
OUTPUT_ZIP = '/home/team/shared/little-cloud-activity-book-digital.zip'

# Page mapping (manuscript outline page # -> filename)
PAGE_FILES = {
    1: 'cover.png',
    2: 'page-02.png',
    3: 'page-03.png',
    4: 'page-04.png',
    5: 'page-05.png',
    6: 'page-06.png',
    7: 'page-07.png',
    8: 'page-08.png',
    9: 'page-09.png',
    10: 'page-10.png',
    11: 'page-11.png',
    12: 'page-12.png',
    13: 'page-13.png',
    14: 'page-14.png',
    15: 'page-15.png',
    16: None,  # page-16 not available
    17: None,  # page-17 not available
    18: None,  # page-18 not available
    19: None,  # page-19 not available
    20: None,  # page-20 not available
    21: None,  # page-21 not available
    22: None,  # page-22 not available
    23: None,  # page-23 not available
    24: 'page-24.png',
}

def add_image_to_page(c, img_path, page_w, page_h):
    """Add an image scaled to fill the page."""
    if not img_path or not os.path.exists(img_path):
        # White page
        c.setFillColorRGB(1, 1, 1)
        c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
        return
    
    img = Image.open(img_path).convert('RGB')
    img = img.resize((int(page_w), int(page_h)), Image.LANCZOS)
    tmp = os.path.join(TMP, f'activity_page_{os.path.basename(img_path)}.jpg')
    img.save(tmp, 'JPEG', quality=95)
    c.drawImage(tmp, 0, 0, width=page_w, height=page_h)

def build_kdp_pdf():
    c = canvas.Canvas(OUTPUT_KDP, pagesize=(PAGE_W, PAGE_H))
    
    # Cover
    cover_path = os.path.join(IMG_DIR, 'cover.png')
    add_image_to_page(c, cover_path, PAGE_W, PAGE_H)
    
    # Title overlay on cover
    c.setFillColorRGB(0.9, 0.2, 0.3)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(PAGE_W/2, PAGE_H - 120, "Little Cloud's Big")
    c.drawCentredString(PAGE_W/2, PAGE_H - 160, "Activity Book!")
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawCentredString(PAGE_W/2, PAGE_H - 195, "Ages 2-6 | Fun with Cirrus & Friends")
    c.showPage()
    
    # Interior pages
    for pagenum in sorted(PAGE_FILES.keys()):
        if pagenum == 1:
            continue  # already did cover
        fname = PAGE_FILES[pagenum]
        if fname:
            img_path = os.path.join(IMG_DIR, fname)
        else:
            img_path = None
        
        add_image_to_page(c, img_path, PAGE_W, PAGE_H)
        c.showPage()
    
    c.save()
    size_mb = os.path.getsize(OUTPUT_KDP) / (1024*1024)
    print(f"KDP PDF saved: {OUTPUT_KDP} ({size_mb:.1f} MB)")

def build_digital_zip():
    """Create individual PDF pages for each activity page, no bleed."""
    tmpdir = tempfile.mkdtemp()
    
    for pagenum in sorted(PAGE_FILES.keys()):
        if pagenum == 1:
            continue  # skip cover for individual pages? Include it
        fname = PAGE_FILES[pagenum]
        if not fname:
            continue
        
        src = os.path.join(IMG_DIR, fname)
        if not os.path.exists(src):
            continue
        
        # Create a single-page PDF at 8.5x11 with no bleed
        single_pdf = os.path.join(tmpdir, f'page-{pagenum:02d}.pdf')
        c = canvas.Canvas(single_pdf, pagesize=(TRIM_W, TRIM_H))
        
        img = Image.open(src).convert('RGB')
        img = img.resize((int(TRIM_W), int(TRIM_H)), Image.LANCZOS)
        tmp_jpg = os.path.join(TMP, f'digital_page_{pagenum}.jpg')
        img.save(tmp_jpg, 'JPEG', quality=95)
        c.drawImage(tmp_jpg, 0, 0, width=TRIM_W, height=TRIM_H)
        c.save()
    
    # Also include the cover as a separate PDF
    cover_src = os.path.join(IMG_DIR, 'cover.png')
    if os.path.exists(cover_src):
        cover_pdf = os.path.join(tmpdir, 'cover.pdf')
        c = canvas.Canvas(cover_pdf, pagesize=(TRIM_W, TRIM_H))
        img = Image.open(cover_src).convert('RGB')
        img = img.resize((int(TRIM_W), int(TRIM_H)), Image.LANCZOS)
        tmp_jpg = os.path.join(TMP, 'digital_cover.jpg')
        img.save(tmp_jpg, 'JPEG', quality=95)
        c.drawImage(tmp_jpg, 0, 0, width=TRIM_W, height=TRIM_H)
        c.save()
    
    # Zip them up
    with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(os.listdir(tmpdir)):
            if f.endswith('.pdf'):
                zf.write(os.path.join(tmpdir, f), f)
    
    shutil.rmtree(tmpdir)
    size_mb = os.path.getsize(OUTPUT_ZIP) / (1024*1024)
    print(f"Digital ZIP saved: {OUTPUT_ZIP} ({size_mb:.2f} MB)")

if __name__ == '__main__':
    build_kdp_pdf()
    build_digital_zip()