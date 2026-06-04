#!/usr/bin/env python3
"""Rebuild activity book PDF with proper margins so content stays on page."""
import os, shutil, zipfile, tempfile
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

TMP = '/home/team/shared/.tmp_build'
os.makedirs(TMP, exist_ok=True)

TRIM_W = 8.5 * inch
TRIM_H = 11.0 * inch
BLEED = 0.125 * inch
PAGE_W = TRIM_W + 2 * BLEED
PAGE_H = TRIM_H + 2 * BLEED
MARGIN = 0.35 * inch  # safe margin

IMG_DIR = '/home/team/shared/activity-book-pages'
OUTPUT_KDP = '/home/team/shared/activity-book-kdp-ready.pdf'
OUTPUT_ZIP = '/home/team/shared/little-cloud-activity-book-digital.zip'

# Safe image area
IMG_W = TRIM_W - 2 * MARGIN
IMG_H = TRIM_H - 2 * MARGIN
IMG_X = BLEED + MARGIN
IMG_Y = BLEED + MARGIN

PAGE_FILES = {
    1: 'cover.png', 2: 'page-02.png', 3: 'page-03.png', 4: 'page-04.png',
    5: 'page-05.png', 6: 'page-06.png', 7: 'page-07.png', 8: 'page-08.png',
    9: 'page-09.png', 10: 'page-10.png', 11: 'page-11.png', 12: 'page-12.png',
    13: 'page-13.png', 14: 'page-14.png', 15: 'page-15.png', 16: None,
    17: None, 18: None, 19: None, 20: None, 21: None, 22: None, 23: None,
    24: 'page-24.png',
}

def add_image_safe(c, img_path, page_w, page_h):
    """Place image scaled to fit within safe area, centered on page."""
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    
    if img_path and os.path.exists(img_path):
        img = Image.open(img_path).convert('RGB')
        iw, ih = img.size
        scale = min(IMG_W / iw, IMG_H / ih)
        dw = iw * scale
        dh = ih * scale
        dx = IMG_X + (IMG_W - dw) / 2
        dy = IMG_Y + (IMG_H - dh) / 2
        new_size = (int(dw), int(dh))
        resized = img.resize(new_size, Image.LANCZOS)
        tmp = os.path.join(TMP, f'act_{os.path.basename(img_path)}.jpg')
        resized.save(tmp, 'JPEG', quality=95)
        c.drawImage(tmp, dx, dy, width=dw, height=dh)

def build_kdp_pdf():
    c = canvas.Canvas(OUTPUT_KDP, pagesize=(PAGE_W, PAGE_H))
    
    # Cover
    add_image_safe(c, os.path.join(IMG_DIR, 'cover.png'), PAGE_W, PAGE_H)
    c.setFillColorRGB(0.9, 0.2, 0.3)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(PAGE_W/2, PAGE_H - 110 - BLEED, "Little Cloud's Big")
    c.drawCentredString(PAGE_W/2, PAGE_H - 150 - BLEED, "Activity Book!")
    c.setFont("Helvetica", 13)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawCentredString(PAGE_W/2, PAGE_H - 185 - BLEED, "Ages 2-6 | Fun with Cirrus & Friends")
    c.showPage()
    
    for pagenum in sorted(PAGE_FILES.keys()):
        if pagenum == 1:
            continue
        fname = PAGE_FILES[pagenum]
        add_image_safe(c, os.path.join(IMG_DIR, fname) if fname else None, PAGE_W, PAGE_H)
        c.showPage()
    
    c.save()
    sz = os.path.getsize(OUTPUT_KDP) / (1024*1024)
    print(f"KDP PDF: {OUTPUT_KDP} ({sz:.1f} MB)")

def build_digital_zip():
    """Digital download PDFs at trim size with margins."""
    tmpdir = tempfile.mkdtemp()
    DIG_MARGIN = 0.3 * inch
    
    for pagenum in sorted(PAGE_FILES.keys()):
        fname = PAGE_FILES.get(pagenum)
        if not fname or not os.path.exists(os.path.join(IMG_DIR, fname)):
            continue
        
        src = os.path.join(IMG_DIR, fname)
        single_pdf = os.path.join(tmpdir, f'page-{pagenum:02d}.pdf')
        c = canvas.Canvas(single_pdf, pagesize=(TRIM_W, TRIM_H))
        
        img = Image.open(src).convert('RGB')
        iw, ih = img.size
        dw = TRIM_W - 2 * DIG_MARGIN
        dh = TRIM_H - 2 * DIG_MARGIN
        scale = min(dw / iw, dh / ih)
        sw = iw * scale
        sh = ih * scale
        sx = DIG_MARGIN + (dw - sw) / 2
        sy = DIG_MARGIN + (dh - sh) / 2
        new_size = (int(sw), int(sh))
        resized = img.resize(new_size, Image.LANCZOS)
        tmp_jpg = os.path.join(TMP, f'dig_page_{pagenum}.jpg')
        resized.save(tmp_jpg, 'JPEG', quality=95)
        c.drawImage(tmp_jpg, sx, sy, width=sw, height=sh)
        c.save()
    
    if os.path.exists(os.path.join(IMG_DIR, 'cover.png')):
        cover_pdf = os.path.join(tmpdir, 'cover.pdf')
        c = canvas.Canvas(cover_pdf, pagesize=(TRIM_W, TRIM_H))
        img = Image.open(os.path.join(IMG_DIR, 'cover.png')).convert('RGB')
        scale = min((TRIM_W-2*DIG_MARGIN)/img.width, (TRIM_H-2*DIG_MARGIN)/img.height)
        sw = img.width * scale; sh = img.height * scale
        sx = (TRIM_W - sw) / 2; sy = (TRIM_H - sh) / 2
        new_size = (int(sw), int(sh))
        resized = img.resize(new_size, Image.LANCZOS)
        tmp_jpg = os.path.join(TMP, 'dig_cover.jpg')
        resized.save(tmp_jpg, 'JPEG', quality=95)
        c.drawImage(tmp_jpg, sx, sy, width=sw, height=sh)
        c.save()
    
    with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(os.listdir(tmpdir)):
            if f.endswith('.pdf'):
                zf.write(os.path.join(tmpdir, f), f)
    
    shutil.rmtree(tmpdir)
    sz = os.path.getsize(OUTPUT_ZIP) / (1024*1024)
    print(f"Digital ZIP: {OUTPUT_ZIP} ({sz:.2f} MB)")

if __name__ == '__main__':
    build_kdp_pdf()
    build_digital_zip()
    print("=== ACTIVITY BOOK REBUILT ===")
