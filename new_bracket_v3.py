# PAGE 28: KNOCKOUT BRACKET - LANDSCAPE FULL PAGE
c.setPageSize((PH, PW))  # swap to landscape (wider, shorter)
lx=BLEED+10; ly=BLEED+10; pw=PH-20; ph=PW-20
mid_x=lx+pw/2; mid_y=ly+ph/2

# Background
c.setFillColorRGB(0.98,0.98,1);c.rect(0,0,PH,PW,fill=1,stroke=0)

# Title 
c.setFont("Helvetica-Bold",20);c.setFillColorRGB(0.05,0.05,0.3)
c.drawCentredString(mid_x,PH-35,"WORLD CUP 2026 - KNOCKOUT BRACKET")
c.setStrokeColorRGB(0.06,0.06,0.3);c.setLineWidth(1)
c.line(mid_x-180,PH-50,mid_x+180,PH-50)

y_top=PH-75; sp=18; ml=55

# Flag designs for each group (2-color patterns)
flags={}
for i in range(16):
    idx=i%4
    if idx==0: flags[i]=[(0.2,0.2,0.8),(1,1,1),(0.8,0.2,0.2)]  # blue/white/red
    elif idx==1: flags[i]=[(0.2,0.6,0.2),(1,1,0),(0.2,0.2,0.8)]  # green/yellow/blue
    elif idx==2: flags[i]=[(1,1,1),(0.8,0.2,0.2)]  # white/red
    else: flags[i]=[(1,0.6,0),(0,0.4,0.8),(1,1,1)]  # orange/blue/white

# LEFT: Teams A1-H2  
left_groups=["A1","A2","B1","B2","C1","C2","D1","D2","E1","E2","F1","F2","G1","G2","H1","H2"]
lx_team=lx+10
c.setFont("Helvetica-Bold",5.5)
for i in range(16):
    y=y_top-i*sp
    # Draw flag stripes
    fc=flags[i]
    stripe_w=9/len(fc)
    for si,sc in enumerate(fc):
        c.setFillColorRGB(*sc)
        c.rect(lx_team+si*stripe_w,y-2,stripe_w+1,8,fill=1,stroke=0)
    c.setStrokeColorRGB(0.3,0.3,0.3);c.setLineWidth(0.3)
    c.rect(lx_team,y-2,9,8,fill=0,stroke=1)
    # Group label
    c.setFillColorRGB(0.05,0.05,0.3)
    c.drawString(lx_team+12,y-1,left_groups[i])
    # Team fill-in line
    c.setStrokeColorRGB(0.4,0.4,0.4);c.setLineWidth(0.5)
    c.line(lx_team+32,y,lx_team+55,y)

# R32 left connections
r32_l=lx_team+55; r16_l=r32_l+ml
for p in range(16):
    y1=y_top-p*sp
    c.line(r32_l,y1,r32_l+(ml if p%2==1 else 0),y1)
    if p%2==1: c.line(r32_l,y1,r32_l,y_top-(p-1)*sp)
for p in range(8):
    y1=y_top-p*2*sp; y2=y_top-(p*2+1)*sp; ym=(y1+y2)/2
    c.line(r32_l,y1,r32_l,y2);c.line(r32_l,ym,r16_l,ym)

# R16 left slots
for i in range(8):
    ym=y_top-(i*2+0.5)*sp
    c.line(r16_l,ym-4,r16_l+ml,ym-4);c.line(r16_l,ym+4,r16_l+ml,ym+4)
    c.setFont("Helvetica-Bold",5);c.setFillColorRGB(0.3,0.3,0.3)
    c.drawCentredString(r16_l+ml/2,ym-14,f"R16-{i+1}")

# R16 left to QF
qf_l=r16_l+ml
for p in range(4):
    y1=y_top-(p*4+0.5)*sp; y2=y_top-(p*4+2.5)*sp; ym=(y1+y2)/2
    c.line(r16_l+ml,y1,r16_l+ml,y2);c.line(r16_l+ml,ym,qf_l,ym)

# RIGHT: Teams I1-3H
rx_team=lx+pw-10
for i in range(16):
    y=y_top-i*sp
    fc=flags[(i+2)%4]
    stripe_w=9/len(fc)
    for si,sc in enumerate(fc):
        c.setFillColorRGB(*sc)
        c.rect(rx_team-9+si*stripe_w,y-2,stripe_w+1,8,fill=1,stroke=0)
    c.rect(rx_team-9,y-2,9,8,fill=0,stroke=1)
    c.setFillColorRGB(0.05,0.05,0.3)
    c.drawRightString(rx_team-12,y-1,["I1","I2","J1","J2","K1","K2","L1","L2","3A","3B","3C","3D","3E","3F","3G","3H"][i])
    c.line(rx_team-55,y,rx_team-32,y)

# R32 right connections
r32_r=rx_team-55; r16_r=r32_r-ml
for p in range(16):
    y1=y_top-p*sp
    c.line(r32_r-(ml if p%2==1 else 0),y1,r32_r,y1)
    if p%2==1: c.line(r32_r,y1,r32_r,y_top-(p-1)*sp)
for p in range(8):
    y1=y_top-p*2*sp; y2=y_top-(p*2+1)*sp; ym=(y1+y2)/2
    c.line(r32_r,y1,r32_r,y2);c.line(r32_r,ym,r16_r,ym)

# R16 right slots
for i in range(8):
    ym=y_top-(i*2+0.5)*sp
    c.line(r16_r-ml,ym-4,r16_r,ym-4);c.line(r16_r-ml,ym+4,r16_r,ym+4)
    c.setFont("Helvetica-Bold",5);c.setFillColorRGB(0.3,0.3,0.3)
    c.drawCentredString(r16_r-ml/2,ym-14,f"R16-{i+1}")

# R16 right to QF
qf_r=r16_r-ml
for p in range(4):
    y1=y_top-(p*4+0.5)*sp; y2=y_top-(p*4+2.5)*sp; ym=(y1+y2)/2
    c.line(r16_r,y1,r16_r,y2);c.line(r16_r,ym,qf_r,ym)

# CENTER: QF → SF → FINAL
c.setStrokeColorRGB(0.2,0.2,0.2);c.setLineWidth(0.7)
# QF slots
for i in range(4):
    ym=y_top-(i*4+1.5)*sp
    c.line(mid_x-30,ym-5,mid_x+30,ym-5);c.line(mid_x-30,ym+5,mid_x+30,ym+5)
    c.setFont("Helvetica-Bold",6);c.setFillColorRGB(0.06,0.06,0.3)
    c.drawCentredString(mid_x,ym-14,"QF")

# QF to SF
sf_y=[y_top-(i*4+1.5)*sp for i in range(4)]
for p in range(2):
    y1=sf_y[p*2]-5; y2=sf_y[p*2+1]+5; ym=(y1+y2)/2
    c.line(mid_x-30,y1,mid_x-30,y2);c.line(mid_x+30,y1,mid_x+30,y2)
    c.line(mid_x-30,ym,mid_x-15,ym);c.line(mid_x+30,ym,mid_x+15,ym)

# SF slots
for i in range(2):
    ym=sf_y[i*2]-5+((sf_y[i*2+1]+5)-(sf_y[i*2]-5))/2
    c.line(mid_x-15,ym-6,mid_x+15,ym-6);c.line(mid_x-15,ym+6,mid_x+15,ym+6)
    c.setFont("Helvetica-Bold",7);c.setFillColorRGB(0.06,0.06,0.3)
    c.drawCentredString(mid_x,ym-15,"SF")

# SF to Final
sf_m=[sf_y[0]-5+((sf_y[1]+5)-(sf_y[0]-5))/2,sf_y[2]-5+((sf_y[3]+5)-(sf_y[2]-5))/2]
yf=(sf_m[0]+sf_m[1])/2
c.line(mid_x-15,sf_m[0],mid_x-15,sf_m[1]);c.line(mid_x+15,sf_m[0],mid_x+15,sf_m[1])
c.line(mid_x-15,yf,mid_x+15,yf)

# FINAL with red highlight
c.setStrokeColorRGB(0.85,0.25,0.22);c.setLineWidth(2)
c.line(mid_x-25,yf-9,mid_x+25,yf-9);c.line(mid_x-25,yf+9,mid_x+25,yf+9)
c.setFont("Helvetica-Bold",10);c.setFillColorRGB(0.85,0.25,0.22)
c.drawCentredString(mid_x,yf-20,"FINAL")

# WORLD CUP TROPHY
tx=mid_x; ty=yf+55
# Trophy glow
c.setFillColorRGB(1,0.95,0.8)
c.circle(tx,ty+5,35,fill=1,stroke=0)
c.setFillColorRGB(0.95,0.85,0.6)
c.circle(tx,ty+5,25,fill=1,stroke=0)
# Trophy base
c.setFillColorRGB(0.85,0.7,0.3)
c.rect(tx-12,ty-15,24,8,fill=1,stroke=0)
c.rect(tx-8,ty-30,16,15,fill=1,stroke=0)
c.rect(tx-5,ty-45,10,15,fill=1,stroke=0)
# Trophy cup (globe shape)
c.setFillColorRGB(0.9,0.75,0.35)
c.circle(tx,ty-10,10,fill=1,stroke=0)
c.circle(tx,ty-25,8,fill=1,stroke=0)
c.circle(tx,ty-38,6,fill=1,stroke=0)
# Trophy star
c.setFillColorRGB(1,1,1)
c.setFont("Helvetica-Bold",8)
c.drawCentredString(tx,ty-10,"*")
# Champion text underneath
c.setFont("Helvetica-Bold",12);c.setFillColorRGB(0.85,0.2,0.2)
c.drawCentredString(mid_x,ty-55,"CHAMPION")

# Round labels at top
for lbl,xp,w in [("R32",20,70),("R16",90,45),("QF",160,35),("SF",215,30),("FINAL",270,35)]:
    cx=lx+xp
    c.setFillColorRGB(*CARD_COLORS[int(xp/70)%4])
    c.roundRect(cx,y_top+30,w,14,4,fill=1,stroke=0)
    c.setFont("Helvetica-Bold",7);c.setFillColorRGB(1,1,1)
    c.drawCentredString(cx+w/2,y_top+33,lbl)
c.setFillColorRGB(*CARD_COLORS[0])
c.roundRect(mid_x+25,y_top+30,50,14,4,fill=1,stroke=0)
c.setFont("Helvetica-Bold",7);c.setFillColorRGB(1,1,1)
c.drawCentredString(mid_x+50,y_top+33,"CHAMP")

# Decorative stars
c.setFont("Helvetica-Bold",9);c.setFillColorRGB(0.8,0.8,1)
c.drawString(lx+5,y_top+55,"* *");c.drawString(lx+pw-20,y_top+55,"* *")

c.setFont("Helvetica-Bold",6);c.setFillColorRGB(0.5,0.5,0.5)
c.drawString(lx+5,ly+5,"WORLD CUP 2026 SOUVENIR GUIDEBOOK")
c.drawRightString(lx+pw-5,ly+5,"Knockout Bracket")
c.showPage()
c.setPageSize((PW, PH))  # restore to portrait