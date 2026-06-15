#!/usr/bin/env python3
"""WC2026 Guidebook - KDP Wraparound Cover (front + spine + back)"""
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image
import os

# KDP cover dimensions for 8.5x11, 29 pages, white paper
PAGE_W=8.5*inch; PAGE_H=11.0*inch; BLEED=0.125*inch
SPINE=0.065*inch  # ~0.002252" per page × 29 pages

# Total cover size with bleed
CW=PAGE_W*2+SPINE+BLEED*2  # 17.315"
CH=PAGE_H+BLEED*2  # 11.25"

O='/home/team/shared/wc2026-guidebook-cover.pdf'
c=canvas.Canvas(O,pagesize=(CW,CH),pageCompression=1)

NAVY=(0.05,0.05,0.3); GOLD=(0.85,0.7,0.2); WHITE=(1,1,1)
CARD_COLORS=[(0.22,0.42,0.78),(0.85,0.25,0.22),(0.15,0.65,0.30),(0.90,0.55,0.10)]

# Back cover x-range: 0 to PAGE_W+BLEED
# Spine x-range: PAGE_W+BLEED to PAGE_W+BLEED+SPINE  
# Front cover x-range: PAGE_W+BLEED+SPINE to CW

fc_lx=PAGE_W+BLEED+SPINE  # front cover left edge
bc_lx=0  # back cover left edge

# === FRONT COVER ===
c.setFillColorRGB(*NAVY);c.rect(fc_lx-1,0,PAGE_W+BLEED+1,CH,fill=1,stroke=0)

# Gold accent line
c.setFillColorRGB(*GOLD)
c.rect(fc_lx+30,CH*0.62,PAGE_W-60,3,fill=1,stroke=0)
c.rect(fc_lx+30,CH*0.35,PAGE_W-60,3,fill=1,stroke=0)

# Title
c.setFont("Helvetica-Bold",36);c.setFillColorRGB(*WHITE)
c.drawCentredString(fc_lx+PAGE_W/2,CH*0.8,"WORLD CUP 2026")
c.setFont("Helvetica-Bold",22)
c.drawCentredString(fc_lx+PAGE_W/2,CH*0.72,"UNITED IN PLAY")

# Subtitle
c.setFont("Helvetica-Bold",10);c.setFillColorRGB(0.7,0.7,0.9)
c.drawCentredString(fc_lx+PAGE_W/2,CH*0.65,"SOUVENIR GUIDEBOOK")

# Soccer ball graphic
bx=fc_lx+PAGE_W/2; by=CH*0.47
c.setFillColorRGB(0.9,0.9,0.95)
c.circle(bx,by,25,fill=1,stroke=0)
c.setStrokeColorRGB(0.3,0.3,0.3);c.setLineWidth(1.5)
c.circle(bx,by,25,fill=0,stroke=1)
c.setFont("Helvetica-Bold",14);c.setFillColorRGB(*NAVY)
c.drawCentredString(bx,by-7,"*")

# Bottom text
c.setFont("Helvetica-Bold",9);c.setFillColorRGB(0.5,0.5,0.7)
c.drawCentredString(fc_lx+PAGE_W/2,CH*0.28,"USA * Mexico * Canada")
c.drawCentredString(fc_lx+PAGE_W/2,CH*0.25,"2026 FIFA World Cup")

# Color stripe at bottom
for si,sc in enumerate(CARD_COLORS):
    sw=PAGE_W/4
    c.setFillColorRGB(*sc)
    c.rect(fc_lx+si*sw,BLEED,sw,8,fill=1,stroke=0)

# === SPINE ===
sp_mid=PAGE_W+BLEED+SPINE/2
c.setFillColorRGB(*NAVY);c.rect(PAGE_W+BLEED,BLEED,SPINE,CH-BLEED*2,fill=1,stroke=0)
c.setFont("Helvetica-Bold",7)
c.setFillColorRGB(*WHITE)
c.rotate(90)
c.drawCentredString((BLEED+CH)/2,-sp_mid-2,"WORLD CUP 2026")
c.rotate(-90)
# Gold line on spine
c.setFillColorRGB(*GOLD)
c.rect(PAGE_W+BLEED,CH*0.5-10,SPINE,2,fill=1,stroke=0)

# === BACK COVER ===
c.setFillColorRGB(*NAVY);c.rect(0,0,PAGE_W+BLEED,CH,fill=1,stroke=0)
c.setFillColorRGB(*GOLD)
c.rect(BLEED+30,CH*0.72,PAGE_W-60,3,fill=1,stroke=0)

# Back cover text
c.setFont("Helvetica-Bold",20);c.setFillColorRGB(*WHITE)
c.drawCentredString(bc_lx+PAGE_W/2,CH*0.85,"Keep Dreaming.")
c.setFont("Helvetica-Bold",16)
c.drawCentredString(bc_lx+PAGE_W/2,CH*0.78,"Keep Playing.")
c.setFont("Helvetica-Bold",14)
c.drawCentredString(bc_lx+PAGE_W/2,CH*0.72,"Keep Roaring!")

# Feature bullets
features=["Group Stage Tracker (A-L)","Knockout Bracket (R32-Final)","Match Predictions & Notes",
          "Golden Boot Tracker","Fan Journal Pages","World Cup History & Stats"]
c.setFont("Helvetica",9);c.setFillColorRGB(0.7,0.7,0.9)
for li,ft in enumerate(features):
    c.drawString(BLEED+40,CH*0.58-li*16,f"* {ft}")

# Color stripe on back
for si,sc in enumerate(CARD_COLORS):
    sw=PAGE_W/4
    c.setFillColorRGB(*sc)
    c.rect(bc_lx+si*sw,BLEED,sw,8,fill=1,stroke=0)

# Barcode area (white box for user to overlay)
c.setFillColorRGB(0.7,0.7,0.9)
c.roundRect(BLEED+30,BLEED+25,120,80,4,fill=1,stroke=0)
c.setFont("Helvetica-Bold",7);c.setFillColorRGB(*NAVY)
c.drawCentredString(BLEED+90,BLEED+65,"BARCODE")
c.drawCentredString(BLEED+90,BLEED+55,"(upload your")
c.drawCentredString(BLEED+90,BLEED+48,"KDP barcode)")

# ISBN/price area
c.setFont("Helvetica-Bold",6);c.setFillColorRGB(0.5,0.5,0.7)
c.drawRightString(CW-BLEED-30,BLEED+95,"ISBN 978-0-0000000-0-0")
c.drawRightString(CW-BLEED-30,BLEED+88,"$14.99 USD")

c.save()
sz=os.path.getsize(O)/(1024*1024)
print(f"✅ KDP Wraparound Cover saved: {O} ({sz:.1f} MB)")
print(f"   Total size: {CW/72:.3f} x {CH/72:.3f} inches")
print(f"   Front: 8.5 x 11 | Spine: {SPINE/72:.3f} | Back: 8.5 x 11")