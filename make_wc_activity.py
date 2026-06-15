#!/usr/bin/env python3
"""Build World Cup 2026 Activity & Fact Book (8.5x11 portrait, 40+ pages)."""
import os, textwrap
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

TMP='/home/team/shared/.tmp_build';os.makedirs(TMP,exist_ok=True)
D='/home/team/shared/wc2026-activity-illustrations'
O='/home/team/shared/wc2026-activity-book-kdp.pdf'

TRIM_W=8.5*inch; TRIM_H=11.0*inch; BLEED=0.125*inch
PW=TRIM_W+2*BLEED; PH=TRIM_H+2*BLEED
M=0.5*inch

c=canvas.Canvas(O,pagesize=(PW,PH))

def bg_white():
    c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)

def add_img(p,w=TRIM_W,h=TRIM_H):
    if p and os.path.exists(p):
        i=Image.open(p).convert('RGB')
        i=i.resize((int(w),int(h)),Image.LANCZOS)
        t=os.path.join(TMP,os.path.basename(p).replace('.png','.jpg'))
        i.save(t,'JPEG',quality=95)
        c.drawImage(t,0,0,w,h)
        return True
    return False

def make_bw(p,w=TRIM_W,h=TRIM_H):
    """Convert image to grayscale for coloring pages."""
    if p and os.path.exists(p):
        i=Image.open(p).convert('L')  # grayscale
        i=i.resize((int(w),int(h)),Image.LANCZOS)
        t=os.path.join(TMP,'bw_'+os.path.basename(p).replace('.png','.jpg'))
        i.save(t,'JPEG',quality=95)
        c.drawImage(t,0,0,w,h)
        return True
    return False

def title_page():
    add_img(D+'/front-cover.png')
    c.setFillColorRGB(1,1,1,alpha=0.6)
    c.roundRect(PW/2-150,PH-250,300,55,8,fill=1,stroke=0)
    c.setFillColorRGB(0.1,0.1,0.3)
    c.setFont("Helvetica-Bold",22)
    c.drawCentredString(PW/2,PH-220,"World Cup 2026 Activity & Fact Book")
    c.showPage()

# === COVER ===
title_page()

# === STADIUM PAGES ===
stadiums=[
    ("MetLife Stadium","The Silver Giant","East Rutherford, NJ","stadium-giant-01-metlife.png",
     "40,000 tons of steel — as heavy as 8,000 elephants!",
     "Draw yourself in the center of the field with 82,500 fans cheering!"),
    ("Lincoln Financial Field","The Linc","Philadelphia, PA","stadium-giant-02-linc.png",
     "11,000+ solar panels + 14 wind turbines power every game!",
     "Design a 'Super Scarf' with Philly symbols and soccer balls."),
    ("FedExField","The FedEx Giant","Landover, MD","stadium-giant-03-fedex.png",
     "One of the largest stadiums in the USA!",
     "Draw the FedEx Giant wearing a cape made of world flags."),
    ("Hard Rock Stadium","Hard Rock Hero","Miami, FL","stadium-giant-04-hardrock.png",
     "The roof covers 90% of seats to keep fans cool!",
     "Color the Hero with neon pink, electric blue, and sunny yellow."),
    ("Mercedes-Benz Stadium","The Benz","Atlanta, GA","stadium-giant-05-benz.png",
     "The roof opens like a giant metal flower in 8 minutes!",
     "Draw the 'Halo Board' — a circular screen around the stadium."),
    ("NRG Stadium","NRG Neo","Houston, TX","stadium-giant-06-nrg.png",
     "First retractable-roof stadium in the USA!",
     "Design a 'Soccer Astronaut' suit for game day."),
    ("AT&T Stadium","Titan Tex","Arlington, TX","stadium-giant-07-titantex.png",
     "The 160-ft video board is longer than a Boeing 737!",
     "Draw a Texas-sized snack tray with nachos and brisket."),
    ("SoFi Stadium","The Infinity Giant","Inglewood, CA","stadium-giant-08-infinity.png",
     "Only double-sided video board in the world!",
     "Draw a 'Walk of Fame' star for your favorite soccer player."),
    ("Levi's Stadium","The Silicon Giant","Santa Clara, CA","stadium-giant-09-silicon.png",
     "A real garden on the roof called 'Faithful Farm'!",
     "Draw a soccer field where the grass is made of solar panels."),
    ("Lumen Field","The Roaring Giant","Seattle, WA","stadium-giant-10-roaring.png",
     "Designed to bounce sound — one of the loudest places on Earth!",
     "Draw a 'Roar-O-Meter' showing how loud the fans cheer."),
    ("Gillette Stadium","The Lighthouse Giant","Foxborough, MA","stadium-giant-11-lighthouse.png",
     "Has its own 22-story lighthouse that welcomes fans!",
     "Draw Nora sailing a soccer ship toward the lighthouse."),
]

for name,nick,city,img,fact,activity in stadiums:
    bg_white()
    ip=os.path.join(D,img)
    if os.path.exists(ip):
        # Color image on top half
        i=Image.open(ip).convert('RGB')
        i=i.resize((int(PW),int(PH*0.5)),Image.LANCZOS)
        tp=os.path.join(TMP,'top_'+img.replace('.png','.jpg'))
        i.save(tp,'JPEG',quality=95)
        c.drawImage(tp,0,PH*0.5,PW,PH*0.5)
    
    # White area on bottom half for text + activity
    c.setFillColorRGB(1,1,1)
    c.rect(0,0,PW,PH*0.48,fill=1,stroke=0)
    
    c.setFillColorRGB(0.1,0.1,0.4)
    c.setFont("Helvetica-Bold",18)
    c.drawCentredString(PW/2,PH*0.42,f"{name}")
    c.setFont("Helvetica",12)
    c.setFillColorRGB(0.3,0.3,0.3)
    c.drawCentredString(PW/2,PH*0.38,f"Nickname: {nick} | {city}")
    
    c.setFont("Helvetica-Bold",12)
    c.setFillColorRGB(0.2,0.2,0.2)
    c.drawCentredString(PW/2,PH*0.33,"DID YOU KNOW?")
    c.setFont("Helvetica",11)
    wf=textwrap.wrap(fact,width=60)
    y=PH*0.29
    for l in wf:
        c.drawCentredString(PW/2,y,l);y-=16
    
    c.setFont("Helvetica-Bold",12)
    c.setFillColorRGB(0.5,0.1,0.3)
    c.drawCentredString(PW/2,y-8,"YOUR ACTIVITY:")
    c.setFont("Helvetica",11)
    c.setFillColorRGB(0.3,0.1,0.3)
    wa=textwrap.wrap(activity,width=60)
    y2=y-28
    for l in wa:
        c.drawCentredString(PW/2,y2,l);y2-=16
    
    # Bottom border line
    c.setStrokeColorRGB(0.7,0.7,0.7)
    c.line(BLEED+20,PH*0.05,PW-BLEED-20,PH*0.05)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.setFont("Helvetica",8)
    c.drawCentredString(PW/2,PH*0.03,f"World Cup 2026 Activity Book - {name}")
    c.showPage()

# === COLORING PAGES (B&W) ===
# Re-use stadium images as B&W coloring pages
for name,_,_,img,_,_ in stadiums:
    bg_white()
    ip=os.path.join(D,img)
    if os.path.exists(ip):
        make_bw(ip,TRIM_W,TRIM_H*0.75)
    c.setFillColorRGB(0.1,0.1,0.3)
    c.setFont("Helvetica-Bold",14)
    c.drawCentredString(PW/2,BLEED+M+20,f"Color {name}!")
    c.setFont("Helvetica",10)
    c.setFillColorRGB(0.4,0.4,0.4)
    c.drawCentredString(PW/2,BLEED+M-5,"Use your favorite colors to bring this stadium to life!")
    c.showPage()

# === WORD SEARCH ===
bg_white()
c.setFillColorRGB(0.1,0.1,0.4)
c.setFont("Helvetica-Bold",22)
c.drawCentredString(PW/2,PH-M-30,"Word Search: Stadium Stars")
c.setFont("Helvetica",12)
c.setFillColorRGB(0.2,0.2,0.2)
c.drawCentredString(PW/2,PH-M-65,"Find these words hidden in the grid:")
words=["SOCCER","STADIUM","GIANT","WORLD CUP","GOAL","ROAR","LIGHTHOUSE","SOLAR","HALO","FIESTA"]
c.drawCentredString(PW/2,PH-M-90,", ".join(words))
# Simple letter grid
grid_text=[
    "STADIUMGIA",
    "NTSWORLDCR",
    "UPROARLOVE",
    "QHALOFIEST",
    "AGOSOCCERX",
    "ZLIGHTHOUS",
    "EGOALSOUND"]
c.setFont("Courier-Bold",20)
y=PH-M-140
for row in grid_text:
    c.drawCentredString(PW/2,y,row);y-=30
c.showPage()

# === MATCH CITY TO STADIUM ===
bg_white()
c.setFillColorRGB(0.1,0.1,0.4)
c.setFont("Helvetica-Bold",20)
c.drawCentredString(PW/2,PH-M-30,"Match the City to the Stadium")
c.setFont("Helvetica",14)
c.setFillColorRGB(0.2,0.2,0.2)
pairs=[("1. Philadelphia ___","A. SoFi Stadium"),("2. Miami ___","B. Lincoln Financial Field"),
       ("3. Los Angeles ___","C. Hard Rock Stadium"),("4. Seattle ___","D. Mercedes-Benz Stadium"),
       ("5. Atlanta ___","E. Lumen Field")]
y=PH-M-80
for a,b in pairs:
    c.drawString(BLEED+60,y,f"{a}          {b}");y-=35
c.setFont("Helvetica",10)
c.setFillColorRGB(0.5,0.5,0.5)
c.drawCentredString(PW/2,BLEED+60,"Answers: 1-B, 2-C, 3-A, 4-E, 5-D")
c.showPage()

# === DESIGN YOUR STADIUM ===
bg_white()
add_img(D+'/design-your-stadium.png',TRIM_W,TRIM_H*0.5)
c.setFillColorRGB(0.1,0.1,0.4)
c.setFont("Helvetica-Bold",20)
c.drawCentredString(PW/2,PH-M-20,"Design Your Own Stadium!")
c.setFont("Helvetica",12)
c.setFillColorRGB(0.2,0.2,0.2)
c.drawCentredString(PW/2,PH-M-50,"What would YOUR Stadium Giant look like?")
c.drawCentredString(PW/2,PH-M-70,"What would your roof be made of? What color would your seats be?")
c.drawCentredString(PW/2,PH-M-90,"Draw your stadium in the space above and describe it below!")

# Lines for writing
c.setStrokeColorRGB(0.6,0.6,0.6)
for i in range(5):
    y=PH*0.38-i*30
    c.line(BLEED+40,y,PW-BLEED-40,y)
c.showPage()

# === WORLD CUP FLAGS ===
bg_white()
add_img(D+'/world-cup-flags.png',TRIM_W,TRIM_H*0.5)
c.setFillColorRGB(0.1,0.1,0.4)
c.setFont("Helvetica-Bold",20)
c.drawCentredString(PW/2,PH-M-20,"World Cup Flag Challenge!")
c.setFont("Helvetica",12)
c.setFillColorRGB(0.2,0.2,0.2)
c.drawCentredString(PW/2,PH-M-50,"The World Cup brings together 48 teams!")
c.drawCentredString(PW/2,PH-M-70,"Draw and color the flags of three countries you want to see play.")
c.showPage()

# === SOCCER DOODLE ===
bg_white()
add_img(D+'/soccer-doodle-page.png',TRIM_W,TRIM_H*0.5)
c.setFillColorRGB(0.1,0.1,0.4)
c.setFont("Helvetica-Bold",20)
c.drawCentredString(PW/2,PH-M-20,"Soccer Doodle Page!")
c.setFont("Helvetica",12)
c.setFillColorRGB(0.2,0.2,0.2)
c.drawCentredString(PW/2,PH-M-50,"Draw a goal celebration, your favorite player,")
c.drawCentredString(PW/2,PH-M-70,"or a stadium full of cheering fans!")
c.showPage()

# === QUIZ ===
bg_white()
c.setFillColorRGB(0.1,0.1,0.4)
c.setFont("Helvetica-Bold",20)
c.drawCentredString(PW/2,PH-M-30,"The 'Go Goal!' Quiz")
c.setFont("Helvetica",14)
c.setFillColorRGB(0.2,0.2,0.2)
qs=["1. Which stadium has a roof that opens like a flower?",
    "2. Which stadium has a giant lighthouse?",
    "3. Which city is home to the 'Silver Giant'?",
    "4. Which stadium is the loudest in the world?",
    "5. How many solar panels are at the Linc in Philly?"]
y=PH-M-80
for q in qs:
    c.drawString(BLEED+40,y,q);y-=30
# Answer lines
c.setStrokeColorRGB(0.6,0.6,0.6)
for i in range(6):
    ly=PH*0.35-i*35
    c.line(BLEED+60,ly,PW-BLEED-60,ly)
c.setFont("Helvetica",9)
c.setFillColorRGB(0.5,0.5,0.5)
c.drawCentredString(PW/2,BLEED+50,"Answers: 1. Atlanta  2. Boston  3. NJ/NY  4. Seattle  5. Over 11,000")
c.showPage()

# === FINAL MESSAGE PAGE ===
bg_white()
c.setFillColorRGB(0.1,0.1,0.4)
c.setFont("Helvetica-Bold",28)
c.drawCentredString(PW/2,PH-M-60,"Keep Dreaming.")
c.drawCentredString(PW/2,PH-M-110,"Keep Playing.")
c.drawCentredString(PW/2,PH-M-160,"Keep Roaring!")
c.setFont("Helvetica",14)
c.setFillColorRGB(0.3,0.3,0.3)
c.drawCentredString(PW/2,PH-M-230,"In 2026, the world comes to North America.")
c.drawCentredString(PW/2,PH-M-260,"Whether you're in the stands or watching at home,")
c.drawCentredString(PW/2,PH-M-280,"you're part of the team!")
c.showPage()

# === BACK COVER ===
add_img(D+'/back-cover.png')
c.showPage()

c.save()
sz=os.path.getsize(O)/(1024*1024)
page_count = 1 + len(stadiums)*2 + 7  # cover + (fact + coloring per stadium) + activity pages
print(f"Activity Book saved: {O} ({sz:.1f} MB, ~{page_count} pages)")