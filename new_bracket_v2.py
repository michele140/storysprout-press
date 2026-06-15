# PAGE 28: Knockout Bracket - Bilateral Groups converging to Final
c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
c.setFont("Helvetica-Bold",16)
c.setFillColorRGB(0.05,0.05,0.3)
c.drawCentredString(PW/2,PH-M-10,"KNOCKOUT BRACKET - ROUND OF 32")
c.setStrokeColorRGB(0.06,0.06,0.3);c.setLineWidth(1)
c.line(100,PH-M-26,PW-100,PH-M-26)
ty=PH-M-45; sp=21; ml=42

# Group labels for 32 teams (A1,A2,B1,B2...)
left_groups=["A1","A2","B1","B2","C1","C2","D1","D2","E1","E2","F1","F2","G1","G2","H1","H2"]
right_groups=["I1","I2","J1","J2","K1","K2","L1","L2","3rd×8"]
right_groups_full=["I1","I2","J1","J2","K1","K2","L1","L2","3A","3B","3C","3D","3E","3F","3G","3H"]

flag_cols=[(0.2,0.2,0.8),(0.8,0.2,0.2),(0.2,0.6,0.2),(0.9,0.6,0.1)]*8

# Left side teams (16)
lx=BLEED+8; team_w=50
c.setFont("Helvetica-Bold",6)
for i in range(16):
    y=ty-i*sp
    c.setFillColorRGB(*flag_cols[i%4])
    c.rect(lx,y-2,6,6,fill=1,stroke=0)
    c.setFillColorRGB(0.05,0.05,0.3)
    c.drawString(lx+8,y-1,left_groups[i])
    c.setStrokeColorRGB(0.3,0.3,0.3);c.setLineWidth(0.5)
    c.line(lx+30,y,lx+50,y)

# Left R32 connections
r32_l=lx+team_w
r16_l=r32_l+ml
for i in range(16):
    y1=ty-i*sp; y2=ty-(i+1)*sp if i%2==0 else y1
    if i%2==0:
        c.line(r32_l,ty-i*sp,r32_l+ml,ty-i*sp)
    else:
        c.line(r32_l,ty-(i-1)*sp,r32_l+ml,ty-(i-1)*sp)
        c.line(r32_l,ty-(i-1)*sp,r32_l,ty-i*sp)
# Connect pairs
for p in range(8):
    y1=ty-p*2*sp; y2=ty-(p*2+1)*sp; ym=(y1+y2)/2
    c.line(r32_l,y1,r32_l,y2)
    c.line(r32_l,ym,r16_l,ym)

# R16 left slots
for i in range(8):
    ym=ty-(i*2+0.5)*sp
    c.line(r16_l,ym-4,r16_l+ml,ym-4)
    c.line(r16_l,ym+4,r16_l+ml,ym+4)

# R16 left to center QF
qf_l=r16_l+ml
for p in range(4):
    y1=ty-(p*4+0.5)*sp; y2=ty-(p*4+2.5)*sp; ym=(y1+y2)/2
    c.line(r16_l+ml,y1,r16_l+ml,y2)
    c.line(r16_l+ml,ym,qf_l,ym)

# Right side teams (16)
rx=PW-BLEED-8
for i in range(16):
    y=ty-i*sp
    c.setFillColorRGB(*flag_cols[(i+2)%4])
    c.rect(rx-6,y-2,6,6,fill=1,stroke=0)
    c.setFillColorRGB(0.05,0.05,0.3)
    c.drawRightString(rx-8,y-1,right_groups_full[i])
    c.setStrokeColorRGB(0.3,0.3,0.3);c.setLineWidth(0.5)
    c.line(rx-50,y,rx-30,y)

# Right R32 connections
r32_r=rx-50
r16_r=r32_r-ml
for i in range(16):
    if i%2==0:
        c.line(r32_r-ml,ty-i*sp,r32_r,ty-i*sp)
    else:
        c.line(r32_r-ml,ty-(i-1)*sp,r32_r,ty-(i-1)*sp)
        c.line(r32_r,ty-(i-1)*sp,r32_r,ty-i*sp)
for p in range(8):
    y1=ty-p*2*sp; y2=ty-(p*2+1)*sp; ym=(y1+y2)/2
    c.line(r32_r,y1,r32_r,y2)
    c.line(r32_r,ym,r16_r,ym)

# R16 right slots
c.setStrokeColorRGB(0.3,0.3,0.3);c.setLineWidth(0.5)
for i in range(8):
    ym=ty-(i*2+0.5)*sp
    c.line(r16_r-ml,ym-4,r16_r,ym-4)
    c.line(r16_r-ml,ym+4,r16_r,ym+4)

# R16 right to center QF
qf_r=r16_r-ml
for p in range(4):
    y1=ty-(p*4+0.5)*sp; y2=ty-(p*4+2.5)*sp; ym=(y1+y2)/2
    c.line(r16_r,y1,r16_r,y2)
    c.line(r16_r,ym,qf_r,ym)

# Center: QF → SF → Final
c.setStrokeColorRGB(0.2,0.2,0.2);c.setLineWidth(0.6)
mid=PW/2
# QF slots (4) at center
for i in range(4):
    ym=ty-(i*4+1.5)*sp
    c.line(mid-30,ym-5,mid+30,ym-5)
    c.line(mid-30,ym+5,mid+30,ym+5)
    c.setFont("Helvetica-Bold",5);c.setFillColorRGB(0.3,0.3,0.3)
    c.drawCentredString(mid,ym-14,f"QF-{i+1}")

# QF to SF connections
sf_y=[ty-(i*4+1.5)*sp for i in range(4)]
for p in range(2):
    y1=sf_y[p*2]-5; y2=sf_y[p*2+1]+5; ym=(y1+y2)/2
    c.line(mid-30,y1,mid-30,y2)
    c.line(mid+30,y1,mid+30,y2)
    c.line(mid-30,ym,mid-15,ym)
    c.line(mid+30,ym,mid+15,ym)

# SF slots (2)
for i in range(2):
    ym=sf_y[i*2]-5+((sf_y[i*2+1]+5)-(sf_y[i*2]-5))/2
    c.line(mid-15,ym-6,mid+15,ym-6)
    c.line(mid-15,ym+6,mid+15,ym+6)
    c.setFont("Helvetica-Bold",6);c.setFillColorRGB(0.3,0.3,0.3)
    c.drawCentredString(mid,ym-15,f"SF-{i+1}")

# SF to Final
sf_mid=[sf_y[0]-5+((sf_y[1]+5)-(sf_y[0]-5))/2,
        sf_y[2]-5+((sf_y[3]+5)-(sf_y[2]-5))/2]
ym_fin=(sf_mid[0]+sf_mid[1])/2
c.line(mid-15,sf_mid[0],mid-15,sf_mid[1])
c.line(mid+15,sf_mid[0],mid+15,sf_mid[1])
c.line(mid-15,ym_fin,mid+15,ym_fin)

# FINAL
c.setStrokeColorRGB(0.85,0.25,0.22);c.setLineWidth(1.5)
c.line(mid-20,ym_fin-8,mid+20,ym_fin-8)
c.line(mid-20,ym_fin+8,mid+20,ym_fin+8)
c.setFont("Helvetica-Bold",8);c.setFillColorRGB(0.85,0.25,0.22)
c.drawCentredString(mid,ym_fin-18,"FINAL")

# Champion trophy
c.setFont("Helvetica-Bold",9);c.setFillColorRGB(0.85,0.2,0.2)
c.drawCentredString(mid,ym_fin+20,"CHAMPION")
c.setFillColorRGB(0.85,0.2,0.2)
c.circle(mid,ym_fin+32,6,fill=1,stroke=0)
c.rect(mid-2,ym_fin+22,4,10,fill=1,stroke=0)
c.rect(mid-5,ym_fin+20,10,3,fill=1,stroke=0)

# Round labels at top
for lbl,xpos,wid in [("R32",0,0.22),("R16",0.22,0.16),("QF",0.38,0.14),("SF",0.52,0.12),("FINAL",0.64,0.12)]:
    cx=lx+xpos*(PW-40)
    c.setFillColorRGB(*CARD_COLORS[int(xpos*4)%4])
    c.roundRect(cx,PH-M-72,PW*wid,12,3,fill=1,stroke=0)
    c.setFont("Helvetica-Bold",6);c.setFillColorRGB(1,1,1)
    c.drawCentredString(cx+PW*wid/2,PH-M-69,lbl)
c.setFillColorRGB(*CARD_COLORS[0])
c.roundRect(PW-150,PH-M-72,50,12,3,fill=1,stroke=0)
c.setFont("Helvetica-Bold",6);c.setFillColorRGB(1,1,1)
c.drawCentredString(PW-125,PH-M-69,"CHAMP")

c.setFont("Helvetica-Bold",TNY)
c.setFillColorRGB(0.5,0.5,0.5)
c.drawString(BLEED+15,BLEED+8,"WORLD CUP 2026 SOUVENIR GUIDEBOOK")
c.drawRightString(PW-BLEED-15,BLEED+8,"Knockout Bracket")
c.showPage()