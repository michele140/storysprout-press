# PAGE 28: Knockout Bracket - Wall Chart Style with Graphics
c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
c.setFont("Helvetica-Bold",18)
c.setFillColorRGB(0.05,0.05,0.3)
c.drawCentredString(PW/2,PH-M-15,"THE KNOCKOUT BRACKET")
c.setStrokeColorRGB(0.06,0.06,0.3);c.setLineWidth(1)
c.line(PW/2-120,PH-M-29,PW/2+120,PH-M-29)

lx=BLEED+15; full_w=TRIM_W-30; mid=PH/2

# Round labels with colored headers
rnd_info=[("R32",lx+5,0.13,CARD_COLORS[0]),("R16",lx+full_w*0.15,0.13,CARD_COLORS[1]),
          ("QF",lx+full_w*0.30,0.13,CARD_COLORS[2]),("SF",lx+full_w*0.46,0.13,CARD_COLORS[3]),
          ("FINAL",lx+full_w*0.62,0.13,CARD_COLORS[1]),("CHAMP",lx+full_w*0.80,0.14,CARD_COLORS[0])]
for lbl,cx,rw,clr in rnd_info:
    c.setFillColorRGB(*clr)
    c.roundRect(cx,PH-M-55,full_w*rw,16,4,fill=1,stroke=0)
    c.setFont("Helvetica-Bold",8)
    c.setFillColorRGB(1,1,1)
    c.drawCentredString(cx+full_w*rw/2,PH-M-52,lbl)

# Flag color dots for decoration
flag_cols=[(0.2,0.2,0.8),(0.8,0.2,0.2),(0.2,0.6,0.2),(0.9,0.6,0.1),(0.2,0.2,0.8),(0.8,0.2,0.2),
           (0.2,0.6,0.2),(0.9,0.6,0.1),(0.2,0.2,0.8),(0.8,0.2,0.2),(0.2,0.6,0.2),(0.9,0.6,0.1),
           (0.2,0.2,0.8),(0.8,0.2,0.2),(0.2,0.6,0.2),(0.9,0.6,0.1)]

sp=19; sl=50
team_y=[mid+(15-i)*sp for i in range(32)]
r32_x=lx+full_w*0.02

# Draw 32 team slots with flag color dots and fill-in lines
for i in range(32):
    y=team_y[i]
    fc=flag_cols[i%len(flag_cols)]
    c.setFillColorRGB(*fc)
    c.circle(r32_x-3,y+1,3,fill=1,stroke=0)
    c.setStrokeColorRGB(0.3,0.3,0.3);c.setLineWidth(0.5)
    c.line(r32_x+3,y,r32_x+sl,y)
    c.setFont("Helvetica-Bold",5)
    c.setFillColorRGB(0.3,0.3,0.3)
    if i%2==0: c.drawString(r32_x+4,y-9,f"{i//2+1}.")

# R32 pair connections → R16
mid_x=r32_x+sl; r16_x=lx+full_w*0.16
for pi in range(16):
    y1=team_y[pi*2]; y2=team_y[pi*2+1]; ym=(y1+y2)/2
    clr=flag_cols[pi%len(flag_cols)]
    c.setStrokeColorRGB(*clr);c.setLineWidth(0.7)
    c.line(mid_x,y1,mid_x,y2)
    c.line(mid_x,ym,r16_x,ym)

# R16 match lines
c.setStrokeColorRGB(0.2,0.2,0.2);c.setLineWidth(0.5)
r16_sy=[(team_y[i*4]+team_y[i*4+3])/2 for i in range(8)]
for i,ym in enumerate(r16_sy):
    clr=CARD_COLORS[i%len(CARD_COLORS)]
    c.line(r16_x,ym-6,r16_x+sl,ym-6)
    c.line(r16_x,ym+6,r16_x+sl,ym+6)
    c.setFillColorRGB(*clr)
    c.circle(r16_x+3,ym,3,fill=1,stroke=0)
    c.setFont("Helvetica-Bold",5)
    c.setFillColorRGB(0.3,0.3,0.3)
    c.drawString(r16_x+8,ym-15,f"{i+1}.")

# R16 → QF
mid2_x=r16_x+sl; qf_x=lx+full_w*0.31
for pi in range(8):
    y1=r16_sy[pi]-6; y2=r16_sy[pi]+6; ym=(y1+y2)/2
    c.line(mid2_x,ym,mid2_x,y2)
for pi in range(4):
    y1=r16_sy[pi*2]-6; y2=r16_sy[pi*2+1]+6; ym=(y1+y2)/2
    c.line(mid2_x,y1,mid2_x,y2)
    c.line(mid2_x,ym,qf_x,ym)

# QF match lines
qf_sy=[(r16_sy[i*2]-6+r16_sy[i*2+1]+6)/2 for i in range(4)]
for i,ym in enumerate(qf_sy):
    clr=CARD_COLORS[(i+2)%len(CARD_COLORS)]
    c.line(qf_x,ym-8,qf_x+sl,ym-8)
    c.line(qf_x,ym+8,qf_x+sl,ym+8)
    c.setFillColorRGB(*clr)
    c.circle(qf_x+3,ym,3,fill=1,stroke=0)
    c.setFont("Helvetica-Bold",6)
    c.setFillColorRGB(0.3,0.3,0.3)
    c.drawString(qf_x+8,ym-17,f"QF-{i+1}.")

mid3_x=qf_x+sl; sf_x=lx+full_w*0.47
for pi in range(4):
    y1=qf_sy[pi]-8; y2=qf_sy[pi]+8; ym=(y1+y2)/2
    c.line(mid3_x,ym,mid3_x,y2)
for pi in range(2):
    y1=qf_sy[pi*2]-8; y2=qf_sy[pi*2+1]+8; ym=(y1+y2)/2
    c.line(mid3_x,y1,mid3_x,y2);c.line(mid3_x,ym,sf_x,ym)

# SF match lines
sf_sy=[(qf_sy[i*2]-8+qf_sy[i*2+1]+8)/2 for i in range(2)]
for i,ym in enumerate(sf_sy):
    clr=CARD_COLORS[(i+3)%len(CARD_COLORS)]
    c.line(sf_x,ym-8,sf_x+sl,ym-8)
    c.line(sf_x,ym+8,sf_x+sl,ym+8)
    c.setFillColorRGB(*clr)
    c.circle(sf_x+3,ym,3,fill=1,stroke=0)
    c.setFont("Helvetica-Bold",6)
    c.setFillColorRGB(0.3,0.3,0.3)
    c.drawString(sf_x+8,ym-17,f"SF-{i+1}.")

# SF → Final
mid4_x=sf_x+sl; fin_x=lx+full_w*0.63
y1=sf_sy[0]-8; y2=sf_sy[1]+8; ym=(y1+y2)/2
c.line(mid4_x,y1,mid4_x,y2);c.line(mid4_x,ym,fin_x,ym)

# Final match
c.setStrokeColorRGB(0.85,0.25,0.22);c.setLineWidth(1.5)
c.line(fin_x,ym-10,fin_x+sl,ym-10)
c.line(fin_x,ym+10,fin_x+sl,ym+10)
c.setFont("Helvetica-Bold",9)
c.setFillColorRGB(0.85,0.25,0.22)
c.drawCentredString(fin_x+sl/2,ym-22,"FINAL")

# Trophy at Champion
champ_x=lx+full_w*0.78
c.setStrokeColorRGB(0.85,0.25,0.22);c.setLineWidth(0.7)
c.line(fin_x+sl,ym,champ_x,ym)
tx=champ_x+sl/2; ty=ym
c.setFillColorRGB(0.85,0.2,0.2)
c.circle(tx,ty+8,8,fill=1,stroke=0)
c.rect(tx-3,ty-2,6,10,fill=1,stroke=0)
c.rect(tx-6,ty-4,12,3,fill=1,stroke=0)
c.setFont("Helvetica-Bold",6)
c.setFillColorRGB(1,1,1)
c.drawCentredString(tx,ty+5,"*")
c.setFont("Helvetica-Bold",8)
c.setFillColorRGB(0.85,0.2,0.2)
c.drawCentredString(tx,ty-12,"CHAMPION")

# Decorative stars
c.setFont("Helvetica-Bold",7)
c.setFillColorRGB(0.8,0.8,0.9)
c.drawString(lx+5,PH-M-80,"*")
c.drawString(lx+full_w-10,PH-M-80,"*")
c.drawString(lx+full_w/2-3,PH-M-85,"* *")

c.setFont("Helvetica-Bold",TNY)
c.setFillColorRGB(0.5,0.5,0.5)
c.drawString(BLEED+15,BLEED+8,"WORLD CUP 2026 SOUVENIR GUIDEBOOK")
c.drawRightString(PW-BLEED-15,BLEED+8,"Knockout Bracket")
c.showPage()