#!/usr/bin/env python3
"""World Cup 2026 Bracket & Fan Journal - 72 Page KDP Interior"""
import math, os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

PW=8.75*72; PH=11.25*72
TRIM_W=8.5*72; TRIM_H=11.0*72; BLEED=0.125*72
M=0.5*72

O='/home/team/shared/wc2026-bracket-journal.pdf'
TMP='/home/team/shared/.tmp_build'
c=canvas.Canvas(O,pagesize=(PW,PH),pageCompression=1)

NAVY=(0.043,0.239,0.569); GOLD=(0.831,0.686,0.216); GREEN=(0.18,0.545,0.341)
CHARCOAL=(0.2,0.2,0.2); WHITE=(1,1,1); LGRAY=(0.95,0.95,0.95)
CARD_COLORS=[NAVY,(0.8,0.2,0.2),GREEN,(0.9,0.6,0.1)]

def place_full(p):
    if p and os.path.exists(p):
        i=Image.open(p).convert('RGB')
        i=i.resize((int(PW),int(PH)),Image.LANCZOS)
        t=os.path.join(TMP,os.path.basename(p).replace('.png','.jpg'))
        i.save(t,'JPEG',quality=92)
        c.drawImage(t,0,0,PW,PH)

def header_bar(title, ty, color=NAVY, size=18):
    c.setFillColorRGB(*color);c.roundRect(BLEED,ty-22,TRIM_W,22,4,fill=1,stroke=0)
    c.setFont("Helvetica-Bold",size);c.setFillColorRGB(1,1,1)
    c.drawCentredString(PW/2,ty-18,title)
    return ty-26

def footer(num):
    c.setFont("Helvetica-Bold",6);c.setFillColorRGB(0.5,0.5,0.5)
    c.drawString(BLEED+10,BLEED+5,"WORLD CUP 2026 BRACKET & FAN JOURNAL")
    c.drawRightString(PW-BLEED-10,BLEED+5,f"Page {num}")

def draw_group_table(tx, ty, tw, gname, color_idx):
    """Draw group table with flag, team name, standings"""
    clr=CARD_COLORS[color_idx%len(CARD_COLORS)]
    c.setFillColorRGB(*clr)
    c.roundRect(tx,ty-18,tw,18,4,fill=1,stroke=0)
    c.setFont("Helvetica-Bold",10);c.setFillColorRGB(1,1,1)
    c.drawString(tx+6,ty-15,f"Group {gname}")
    c.setFont("Helvetica-Bold",6);c.setFillColorRGB(*CHARCOAL)
    c.drawString(tx+6,ty-32,"TEAM");c.drawString(tx+tw-60,ty-32,"W D L PTS")
    c.setStrokeColorRGB(0.7,0.7,0.7);c.setLineWidth(0.3)
    c.line(tx+tw-65,ty-32,tx+tw-5,ty-32)
    for ti in range(4):
        yy=ty-40-ti*14
        c.setFillColorRGB(*CARD_COLORS[(color_idx+ti)%len(CARD_COLORS)])
        c.rect(tx+4,yy-2,8,6,fill=1,stroke=0)
        c.setFont("Helvetica-Bold",7);c.setFillColorRGB(*CHARCOAL)
        c.drawString(tx+15,yy-1,f"______________")
        for bi in range(4):
            bx=tx+tw-60+bi*14
            c.line(bx,yy-1,bx+10,yy-1)

def draw_match_prediction(tx, ty, tw, num):
    c.setStrokeColorRGB(0.7,0.7,0.7);c.setLineWidth(0.5)
    c.setFillColorRGB(1,1,1);c.roundRect(tx,ty-65,tw,65,6,fill=1,stroke=1)
    c.setFont("Helvetica-Bold",8);c.setFillColorRGB(*NAVY)
    c.drawString(tx+6,ty-12,f"Match {num}")
    c.setFont("Helvetica-Bold",6);c.setFillColorRGB(*CHARCOAL)
    c.drawString(tx+6,ty-25,"Team 1:");c.line(tx+45,ty-25,tx+tw-10,ty-25)
    c.drawString(tx+6,ty-35,"Team 2:");c.line(tx+45,ty-35,tx+tw-10,ty-35)
    c.drawString(tx+6,ty-45,"Prediction:");c.line(tx+55,ty-45,tx+tw-10,ty-45)
    c.drawString(tx+6,ty-58,"Result:");c.line(tx+45,ty-58,tx+tw-10,ty-58)
    c.setFont("Helvetica-Bold",7);c.setFillColorRGB(*NAVY)
    c.drawRightString(tx+tw-6,ty-12,"R")

# ============================================================
# PAGE 1: TITLE PAGE
# ============================================================
c.setFillColorRGB(*NAVY);c.rect(0,0,PW,PH,fill=1,stroke=0)
c.setFillColorRGB(*GOLD);c.rect(BLEED,PH*0.6,TRIM_W,4,fill=1,stroke=0)
c.setFont("Helvetica-Bold",36);c.setFillColorRGB(1,1,1)
c.drawCentredString(PW/2,PH*0.7,"WORLD CUP 2026")
c.setFont("Helvetica-Bold",18)
c.drawCentredString(PW/2,PH*0.62,"Bracket  *  Tracker  *  Fan Journal")
c.setFont("Helvetica-Bold",10)
c.drawCentredString(PW/2,PH*0.55,"Track Every Match  *  Predict Every Winner  *  Follow Every Group")
c.setFillColorRGB(*GOLD);c.rect(BLEED,PH*0.5,TRIM_W,4,fill=1,stroke=0)
footer(1);c.showPage()

# ============================================================
# PAGE 2: COPYRIGHT
# ============================================================
c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
c.setFont("Helvetica-Bold",12);c.setFillColorRGB(*CHARCOAL)
c.drawCentredString(PW/2,PH-M-20,"Copyright & Disclaimer")
c.setFont("Helvetica",9)
lines=["2026 FIFA World Cup Bracket & Fan Journal","","Published by StorySprout Press","","All rights reserved. No part of this publication may be reproduced,","distributed, or transmitted in any form or by any means.","","This journal is an unofficial fan publication.","FIFA and World Cup are registered trademarks.","","All images, logos, and trademarks are property of their respective owners.","","Designed for personal use only.","","Printed in the United States of America."]
ty=PH-M-50
for l in lines: c.drawCentredString(PW/2,ty,l);ty-=14
footer(2);c.showPage()

# ============================================================
# PAGE 3: HOW TO USE
# ============================================================
c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
ty=header_bar("HOW TO USE THIS JOURNAL",PH-M-5)
sections=[("GROUP STAGE",f"Track all 12 groups from A to L. Record team names, wins, draws, losses, and points. Check off which teams advance."),
         ("MATCH PREDICTIONS",f"Predict each match! Write in your predicted winner, then record the actual result. Track Player of the Match and best moments."),
         ("KNOCKOUT BRACKET",f"Follow the tournament from Round of 32 through to the Final. Fill in each match winner as the bracket narrows to the Champion."),
         ("TOURNAMENT TRACKERS",f"Keep stats on the Golden Boot race, assist leaders, clean sheets, cards, team stats, and the biggest upsets."),
         ("FAN JOURNAL",f"Record your favorite goals, matches, players, saves, and host city experiences. Write down your tournament memories!")]
for title,desc in sections:
    c.setFillColorRGB(*NAVY);c.roundRect(BLEED+15,ty-18,TRIM_W-30,18,4,fill=1,stroke=0)
    c.setFont("Helvetica-Bold",9);c.setFillColorRGB(1,1,1)
    c.drawString(BLEED+22,ty-15,title);ty-=24
    c.setFont("Helvetica",8);c.setFillColorRGB(*CHARCOAL)
    for line in [desc[i:i+80] for i in range(0,len(desc),80)]:
        c.drawString(BLEED+22,ty,line);ty-=12
    ty-=6
footer(3);c.showPage()

# ============================================================
# PAGE 4: TOURNAMENT OVERVIEW
# ============================================================
c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
ty=header_bar("TOURNAMENT OVERVIEW",PH-M-5)
overview=[("Host Countries","USA, Mexico, Canada"),("Number of Teams","48 nations"),("Groups","12 groups of 4"),("Format","Group stage + knockout"),("Teams that Advance","32 (top 2 from each group + 8 best 3rd)"),("Total Matches","80 matches"),("Group Stage","48 matches"),("Knockout Stage","32 matches"),("Tournament Dates","June - July 2026"),("Mascot","TBD"),("Final Venue","MetLife Stadium, New Jersey")]
for label,value in overview:
    c.setFillColorRGB(*NAVY);c.roundRect(BLEED+30,ty-16,120,16,4,fill=1,stroke=0)
    c.setFont("Helvetica-Bold",8);c.setFillColorRGB(1,1,1)
    c.drawString(BLEED+36,ty-13,label)
    c.setFont("Helvetica",9);c.setFillColorRGB(*CHARCOAL)
    c.drawString(BLEED+160,ty-13,value)
    ty-=22
footer(4);c.showPage()

# ============================================================
# PAGES 5-16: GROUP STAGE (12 groups, 2 per page)
# ============================================================
groups=["A","B","C","D","E","F","G","H","I","J","K","L"]
group_titles=[("Groups A-B",0,1),("Groups C-D",2,3),("Groups E-F",4,5),
              ("Groups G-H",6,7),("Groups I-J",8,9),("Groups K-L",10,11)]
for pg,(title,g1,g2) in enumerate(group_titles,5):
    c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
    ty=header_bar(f"GROUP STAGE - {title}",PH-M-5)
    cw=(TRIM_W-40)/2
    for gi,[gn,ci] in enumerate([(groups[g1],g1),(groups[g2],g2)]):
        gx=BLEED+15+gi*(cw+10)
        draw_group_table(gx,ty,cw,gn,ci)
    ty2=ty-120
    for gi,[gn,ci] in enumerate([(groups[g1],g1),(groups[g2],g2)]):
        gx=BLEED+15+gi*(cw+10)
        c.setFont("Helvetica-Bold",7);c.setFillColorRGB(*NAVY)
        c.drawString(gx,ty2-10,"Notes:")
        c.setStrokeColorRGB(0.7,0.7,0.7);c.setLineWidth(0.3)
        for ni in range(6):
            yy=ty2-26-ni*14
            c.line(gx+5,yy,gx+cw-5,yy)
    c.setFillColorRGB(*GOLD);c.rect(BLEED+15,ty2-115,TRIM_W-30,10,fill=1,stroke=0)
    c.setFont("Helvetica-Bold",7);c.setFillColorRGB(1,1,1)
    c.drawCentredString(PW/2,ty2-113,"Teams that advance and qualify for the knockout stage check here")
    c.drawRightString(PW-30,ty2-113,"Qualified: [  ]")
    footer(pg);c.showPage()

print("✅ Group stage pages done (5-16)")

# ============================================================
# PAGES 17-36: MATCH PREDICTIONS (20 pages, 2 matches per page)
# ============================================================
for pg in range(17,37):
    c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
    ty=header_bar(f"MATCH PREDICTIONS - Round {pg-16}",PH-M-5)
    cw=TRIM_W-40
    for mi in range(2):
        draw_match_prediction(BLEED+15,ty-10,cw,(pg-17)*2+mi+1)
        ty-=70
    c.setFont("Helvetica-Bold",7);c.setFillColorRGB(*NAVY)
    c.drawString(BLEED+15,ty-10,"Player of the Match:");c.line(BLEED+100,ty-10,PW-BLEED-15,ty-10)
    c.drawString(BLEED+15,ty-22,"Best Moment:");c.line(BLEED+75,ty-22,PW-BLEED-15,ty-22)
    c.drawString(BLEED+15,ty-34,"Notes:");c.line(BLEED+45,ty-34,PW-BLEED-15,ty-34)
    footer(pg);c.showPage()

print("✅ Match prediction pages done (17-36)")

# ============================================================
# PAGES 37-40: ROUND OF 32 (4 pages, 4 matches per page)
# ============================================================
for pg in range(37,41):
    c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
    ty=header_bar(f"ROUND OF 32 - Matches {(pg-37)*4+1}-{(pg-37+1)*4}",PH-M-5)
    cw=(TRIM_W-30)/2
    for mi in range(4):
        col=mi%2;row=mi//2
        mx=BLEED+15+col*(cw+10);my=ty-10-row*90
        c.setStrokeColorRGB(0.6,0.6,0.6);c.setLineWidth(0.5)
        c.roundRect(mx,my-85,cw,85,4,fill=0,stroke=1)
        c.setFont("Helvetica-Bold",9);c.setFillColorRGB(*NAVY)
        c.drawString(mx+8,my-14,f"R32 - Match {(pg-37)*4+mi+1}")
        c.setFont("Helvetica-Bold",7);c.setFillColorRGB(*CHARCOAL)
        c.drawString(mx+8,my-28,"Team 1:");c.line(mx+55,my-28,mx+cw-8,my-28)
        c.drawString(mx+8,my-42,"Team 2:");c.line(mx+55,my-42,mx+cw-8,my-42)
        c.drawString(mx+8,my-56,"Score:");c.line(mx+45,my-56,mx+cw-8,my-56)
        c.drawString(mx+8,my-75,"Advancing:");c.line(mx+60,my-75,mx+cw-8,my-75)
    footer(pg);c.showPage()

print("✅ Round of 32 pages done (37-40)")

# ============================================================
# PAGES 41-44: ROUND OF 16 (4 pages, 2 matches per page)
# ============================================================
for pg in range(41,45):
    c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
    ty=header_bar(f"ROUND OF 16 - Matches {(pg-41)*2+1}-{(pg-41+1)*2}",PH-M-5)
    for mi in range(2):
        mx=BLEED+30;my=ty-10-mi*130
        c.setStrokeColorRGB(0.6,0.6,0.6);c.setLineWidth(0.5)
        c.roundRect(mx,my-120,TRIM_W-60,120,6,fill=0,stroke=1)
        c.setFont("Helvetica-Bold",11);c.setFillColorRGB(*NAVY)
        c.drawString(mx+12,my-18,f"R16 - Match {(pg-41)*2+mi+1}")
        c.setFont("Helvetica-Bold",8);c.setFillColorRGB(*CHARCOAL)
        c.drawString(mx+12,my-35,"Team 1:");c.line(mx+60,my-35,mx+TRIM_W-80,my-35)
        c.drawString(mx+12,my-50,"Team 2:");c.line(mx+60,my-50,mx+TRIM_W-80,my-50)
        c.drawString(mx+12,my-65,"Score:");c.line(mx+50,my-65,mx+100,my-65)
        c.drawString(mx+120,my-65,"Penalties:");c.line(mx+175,my-65,mx+TRIM_W-80,my-65)
        c.drawString(mx+12,my-82,"Player of the Match:");c.line(mx+110,my-82,mx+TRIM_W-80,my-82)
        c.drawString(mx+12,my-100,"Advancing:");c.line(mx+70,my-100,mx+TRIM_W-80,my-100)
        # Colored side accent
        c.setFillColorRGB(*CARD_COLORS[(pg+mi)%4])
        c.rect(mx,my-120,5,120,fill=1,stroke=0)
    footer(pg);c.showPage()

print("✅ Round of 16 pages done (41-44)")

# ============================================================
# PAGES 45-46: QUARTERFINALS (2 pages, 2 matches per page)
# ============================================================
for pg in range(45,47):
    c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
    ty=header_bar(f"QUARTERFINALS - Matches {(pg-45)*2+1}-{(pg-45+1)*2}",PH-M-5)
    for mi in range(2):
        mx=BLEED+30;my=ty-10-mi*140
        c.setStrokeColorRGB(0.6,0.6,0.6);c.setLineWidth(0.5)
        c.roundRect(mx,my-130,TRIM_W-60,130,6,fill=0,stroke=1)
        c.setFont("Helvetica-Bold",12);c.setFillColorRGB(*NAVY)
        c.drawString(mx+12,my-20,f"QF - Match {(pg-45)*2+mi+1}")
        c.setFont("Helvetica-Bold",9);c.setFillColorRGB(*CHARCOAL)
        c.drawString(mx+12,my-38,"Team 1:");c.line(mx+60,my-38,mx+TRIM_W-80,my-38)
        c.drawString(mx+12,my-55,"Team 2:");c.line(mx+60,my-55,mx+TRIM_W-80,my-55)
        c.drawString(mx+12,my-72,"Score:");c.line(mx+50,my-72,mx+100,my-72)
        c.drawString(mx+120,my-72,"Extra Time:");c.line(mx+180,my-72,mx+250,my-72)
        c.drawString(mx+270,my-72,"Penalties:");c.line(mx+325,my-72,mx+TRIM_W-80,my-72)
        c.drawString(mx+12,my-90,"Player of the Match:");c.line(mx+110,my-90,mx+TRIM_W-80,my-90)
        c.drawString(mx+12,my-110,"Advancing to Semifinals:");c.line(mx+130,my-110,mx+TRIM_W-80,my-110)
        c.setFillColorRGB(*CARD_COLORS[(pg+mi)%4])
        c.rect(mx,my-130,5,130,fill=1,stroke=0)
    footer(pg);c.showPage()

print("✅ Quarterfinals pages done (45-46)")

# ============================================================
# PAGES 47-48: SEMIFINALS (2 pages, 1 match per page)
# ============================================================
for pg in range(47,49):
    c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
    ty=header_bar(f"SEMIFINALS - Match {pg-46}",PH-M-5)
    mx=BLEED+40;my=PH*0.6
    c.setStrokeColorRGB(0.6,0.6,0.6);c.setLineWidth(0.5)
    c.roundRect(mx,my-180,TRIM_W-80,180,8,fill=0,stroke=1)
    c.setFont("Helvetica-Bold",14);c.setFillColorRGB(*NAVY)
    c.drawCentredString(PW/2,my-22,f"SEMIFINAL {pg-46}")
    c.setFont("Helvetica-Bold",10);c.setFillColorRGB(*CHARCOAL)
    c.drawString(mx+15,my-45,"Team 1:");c.line(mx+70,my-45,mx+TRIM_W-100,my-45)
    c.drawString(mx+15,my-65,"Team 2:");c.line(mx+70,my-65,mx+TRIM_W-100,my-65)
    c.drawString(mx+15,my-85,"Score:");c.line(mx+55,my-85,mx+120,my-85)
    c.drawString(mx+140,my-85,"Extra Time:");c.line(mx+200,my-85,mx+270,my-85)
    c.drawString(mx+290,my-85,"Penalties:");c.line(mx+345,my-85,mx+TRIM_W-100,my-85)
    c.drawString(mx+15,my-105,"Player of the Match:");c.line(mx+120,my-105,mx+TRIM_W-100,my-105)
    c.drawString(mx+15,my-125,"Best Moment:");c.line(mx+85,my-125,mx+TRIM_W-100,my-125)
    c.drawString(mx+15,my-148,"Advancing to Final:");c.line(mx+120,my-148,mx+TRIM_W-100,my-148)
    c.setFillColorRGB(*GOLD)
    c.rect(mx,my-180,5,180,fill=1,stroke=0)
    footer(pg);c.showPage()

print("✅ Semifinals pages done (47-48)")

# ============================================================
# PAGE 49: THIRD PLACE MATCH
# ============================================================
c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
ty=header_bar("THIRD PLACE MATCH",PH-M-5)
mx=BLEED+40;my=PH*0.6
c.setStrokeColorRGB(0.6,0.6,0.6);c.setLineWidth(0.5)
c.roundRect(mx,my-170,TRIM_W-80,170,8,fill=0,stroke=1)
c.setFont("Helvetica-Bold",14);c.setFillColorRGB(*NAVY)
c.drawCentredString(PW/2,my-20,"THIRD PLACE MATCH")
c.setFont("Helvetica-Bold",10);c.setFillColorRGB(*CHARCOAL)
c.drawString(mx+15,my-42,"Team 1 (SF Loser):");c.line(mx+120,my-42,mx+TRIM_W-100,my-42)
c.drawString(mx+15,my-62,"Team 2 (SF Loser):");c.line(mx+120,my-62,mx+TRIM_W-100,my-62)
c.drawString(mx+15,my-82,"Score:");c.line(mx+55,my-82,mx+120,my-82)
c.drawString(mx+140,my-82,"Penalties:");c.line(mx+195,my-82,mx+270,my-82)
c.drawString(mx+15,my-102,"Player of the Match:");c.line(mx+120,my-102,mx+TRIM_W-100,my-102)
c.drawString(mx+15,my-125,"Third Place Winner:");c.line(mx+120,my-125,mx+TRIM_W-100,my-125)
c.setFillColorRGB(*GREEN)
c.rect(mx,my-170,5,170,fill=1,stroke=0)
footer(49);c.showPage()

print("✅ Third place page done (49)")

# ============================================================
# PAGE 50: FINAL
# ============================================================
c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
ty=header_bar("THE FINAL",PH-M-5)
mx=BLEED+50;my=PH*0.6
c.setStrokeColorRGB(0.85,0.2,0.2);c.setLineWidth(1)
c.roundRect(mx,my-200,TRIM_W-100,200,10,fill=0,stroke=1)
c.setFont("Helvetica-Bold",18);c.setFillColorRGB(0.85,0.2,0.2)
c.drawCentredString(PW/2,my-22,"FINAL")
# Trophy
tx=PW/2;ty=my+15
c.setFillColorRGB(0.85,0.2,0.2)
c.circle(tx,ty+10,10,fill=1,stroke=0)
c.rect(tx-3,ty-2,6,12,fill=1,stroke=0)
c.rect(tx-7,ty-5,14,4,fill=1,stroke=0)
c.setFont("Helvetica-Bold",10);c.setFillColorRGB(*CHARCOAL)
c.drawString(mx+15,my-50,"Team 1:");c.line(mx+65,my-50,mx+TRIM_W-120,my-50)
c.drawString(mx+15,my-72,"Team 2:");c.line(mx+65,my-72,mx+TRIM_W-120,my-72)
c.drawString(mx+15,my-94,"Score:");c.line(mx+55,my-94,mx+120,my-94)
c.drawString(mx+140,my-94,"Extra Time:");c.line(mx+200,my-94,mx+270,my-94)
c.drawString(mx+290,my-94,"Penalties:");c.line(mx+345,my-94,mx+TRIM_W-120,my-94)
c.drawString(mx+15,my-116,"Player of the Match:");c.line(mx+120,my-116,mx+TRIM_W-120,my-116)
c.drawString(mx+15,my-138,"Winning Goal Scorer:");c.line(mx+130,my-138,mx+TRIM_W-120,my-138)
c.drawString(mx+15,my-162,"2026 WORLD CHAMPION:");c.line(mx+145,my-162,mx+TRIM_W-120,my-162)
c.setFillColorRGB(0.85,0.2,0.2)
c.rect(mx,my-200,5,200,fill=1,stroke=0)
footer(50);c.showPage()

print("✅ Final page done (50)")

# ============================================================
# PAGE 51: CHAMPION PAGE
# ============================================================
c.setFillColorRGB(*NAVY);c.rect(0,0,PW,PH,fill=1,stroke=0)
c.setFillColorRGB(*GOLD);c.rect(BLEED,PH*0.55,TRIM_W,4,fill=1,stroke=0)
c.setFont("Helvetica-Bold",30);c.setFillColorRGB(1,1,1)
c.drawCentredString(PW/2,PH*0.7,"2026 WORLD CHAMPION")
c.setFont("Helvetica-Bold",22);c.setFillColorRGB(*GOLD)
c.drawCentredString(PW/2,PH*0.58,"_____________________________")
c.setFont("Helvetica-Bold",12);c.setFillColorRGB(1,1,1)
c.drawCentredString(PW/2,PH*0.48,"Runner-Up: _________________")
c.drawCentredString(PW/2,PH*0.43,"Final Score: __________________")
c.setFillColorRGB(*GOLD);c.rect(BLEED,PH*0.38,TRIM_W,4,fill=1,stroke=0)
c.setFont("Helvetica-Bold",10);c.setFillColorRGB(1,1,1)
c.drawCentredString(PW/2,PH*0.32,"Champion's Journey:")
c.setStrokeColorRGB(1,1,1);c.setLineWidth(0.5)
for li in range(8): c.line(BLEED+40,PH*0.28-li*14,PW-BLEED-40,PH*0.28-li*14)
footer(51);c.showPage()

print("✅ Champion page done (51)")

# ============================================================
# PAGES 52-58: TOURNAMENT TRACKERS
# ============================================================
trackers=[("GOLDEN BOOT","Player","Nationality","Goals"),("ASSIST LEADERS","Player","Nationality","Assists"),
          ("CLEAN SHEETS","Goalkeeper","Nationality","Clean Sheets"),("YELLOW CARDS","Player","Nationality","Yellow Cards"),
          ("RED CARDS","Player","Nationality","Red Cards"),("TEAM STATISTICS","Team","Stat","Value"),
          ("BIGGEST UPSETS","Match","Underdog","Score")]
for pg,(title,c1,c2,c3) in enumerate(trackers,52):
    c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
    ty=header_bar(f"TOURNAMENT TRACKER - {title}",PH-M-5)
    c.setFont("Helvetica-Bold",8);c.setFillColorRGB(*NAVY)
    c.roundRect(BLEED+15,ty-16,TRIM_W-30,16,4,fill=1,stroke=0)
    c.setFillColorRGB(1,1,1)
    for ci,cl in enumerate([c1,c2,c3]): c.drawString(BLEED+25+ci*150,ty-13,cl)
    c.setStrokeColorRGB(0.7,0.7,0.7);c.setLineWidth(0.3)
    for ri in range(15):
        yy=ty-30-ri*16
        c.line(BLEED+15,yy,PW-BLEED-15,yy)
        for ci in range(3):
            bx=BLEED+25+ci*150
            c.drawString(bx,yy-10,"_____________")
    footer(pg);c.showPage()

print("✅ Tournament tracker pages done (52-58)")

# ============================================================
# PAGES 59-72: FAN JOURNAL (14 pages)
# ============================================================
journal_pages=[("FAVORITE GOALS","Goal","Match","Why it was amazing:"),
               ("FAVORITE MATCHES","Match","Score","Best moment:"),
               ("BEST PLAYERS","Player","Team","Why they stood out:"),
               ("BEST SAVES","Goalkeeper","Match","Description:"),
               ("HOST CITIES","City","Stadium visited","Notes:"),
               ("TRAVEL NOTES","City","Date","Experience:"),
               ("TOURNAMENT MEMORIES 1","Memory of the Day","Date","Details:"),
               ("TOURNAMENT MEMORIES 2","Memory of the Day","Date","Details:"),
               ("MY FAN EXPERIENCE","What I loved most","Best match I watched","Where I watched it:"),
               ("PLAYERS I DISCOVERED","Player Name","Team","Why I'll follow them:"),
               ("BEST GOALS RANKING","Rank","Goal Scorer","Match:"),
               ("DREAM FINAL I WOULD LOVE","Team 1","Team 2","Predicted Score:"),
               ("JOURNAL - FREE PAGE 1","","",""),
               ("JOURNAL - FREE PAGE 2","","","")]
for pg,(title,f1,f2,f3) in enumerate(journal_pages,59):
    c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
    ty=header_bar(f"FAN JOURNAL - {title}",PH-M-5)
    if "FREE" not in title:
        for fi,[fl,fr] in enumerate([(f1,180),(f2,180),(f3,TRIM_W-50)]):
            c.setFont("Helvetica-Bold",9);c.setFillColorRGB(*CHARCOAL)
            c.drawString(BLEED+25,ty-28-fi*70,fl)
            c.line(BLEED+fr,ty-28-fi*70,PW-BLEED-15,ty-28-fi*70)
            for ni in range(4):
                yy=ty-48-fi*70-ni*14
                c.line(BLEED+25,yy,PW-BLEED-15,yy)
    # Journal lines for free pages
    for li in range(38):
        yy=ty-18-li*14
        if yy<BLEED+20:break
        c.setStrokeColorRGB(0.8,0.8,0.9);c.setLineWidth(0.3)
        c.line(BLEED+25,yy,PW-BLEED-25,yy)
    footer(pg);c.showPage()

print("✅ Fan journal pages done (59-72)")

c.save()
sz=os.path.getsize(O)/(1024*1024)
print(f"\n✅ WC2026 Bracket & Fan Journal saved: {O} ({sz:.1f} MB, 72 pages)")
print(f"   Pages 1-4: Front matter")
print(f"   Pages 5-16: Group Stage (A-L)")
print(f"   Pages 17-36: Match Predictions")
print(f"   Pages 37-40: Round of 32")
print(f"   Pages 41-44: Round of 16")
print(f"   Pages 45-46: Quarterfinals")
print(f"   Pages 47-48: Semifinals")
print(f"   Page 49: Third Place")
print(f"   Page 50: Final")
print(f"   Page 51: Champion Page")
print(f"   Pages 52-58: Tournament Trackers")
print(f"   Pages 59-72: Fan Journal")