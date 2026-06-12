#!/usr/bin/env python3
"""Build WC 2026 Souvenir Guidebook - premium magazine-style (8.5x11)."""
import os, textwrap
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

TMP='/home/team/shared/.tmp_build';os.makedirs(TMP,exist_ok=True)
D='/home/team/shared/wc2026-guidebook-illustrations'
O='/home/team/shared/wc2026-guidebook-kdp.pdf'

TRIM_W=8.5*inch; TRIM_H=11.0*inch; BLEED=0.125*inch
PW=TRIM_W+2*BLEED; PH=TRIM_H+2*BLEED
M=0.5*inch

c=canvas.Canvas(O,pagesize=(PW,PH),pageCompression=1)

def bg(c, r=1, g=1, b=1):
    c.setFillColorRGB(r,g,b);c.rect(0,0,PW,PH,fill=1,stroke=0)

def place(p,w=TRIM_W,h=TRIM_H):
    if p and os.path.exists(p):
        i=Image.open(p).convert('RGB')
        i=i.resize((int(w),int(h)),Image.LANCZOS)
        t=os.path.join(TMP,os.path.basename(p).replace('.png','.jpg'))
        i.save(t,'JPEG',quality=92)
        c.drawImage(t,0,0,w,h)
        return True
    return False

def section_header(text, subtitle="", y_offset=200):
    """Draw a section header over a dark background."""
    c.setFillColorRGB(1,1,1,alpha=0.85)
    c.roundRect(PW/2-200,PH-y_offset-30,400,60,10,fill=1,stroke=0)
    c.setFillColorRGB(0.1,0.1,0.3)
    c.setFont("Helvetica-Bold",24)
    c.drawCentredString(PW/2,PH-y_offset,text)
    if subtitle:
        c.setFont("Helvetica",12)
        c.setFillColorRGB(0.3,0.3,0.3)
        c.drawCentredString(PW/2,PH-y_offset-22,subtitle)

# === COVER ===
place(D+'/front-cover.png')
c.showPage()

# === SECTION 1: WORLD CUP HISTORY ===
# Image has embedded text - no overlay to avoid overlapping
place(D+'/section-world-cup-history.png')
c.showPage()

# === STADIUM SPREADS (11 sections, each with stadium + city info + profile) ===
stadiums=[
    ("MetLife Stadium","The Silver Giant","New York / New Jersey","stadium-01-metlife-nyc.png","number-01-metlife-profile.png",
     ["Host City: The Big Apple","Landmark: Statue of Liberty","Languages spoken: 800+","Broadway, Central Park, yellow taxis"],
     ["Stadium built: 2010","Capacity: 82,500 seats","40,000 tons of steel","Hosts World Cup 2026 Final!"]),
    ("Lincoln Financial Field","The Linc","Philadelphia, PA","stadium-02-philly-linc.png","number-02-philly-profile.png",
     ["Host City: City of Brotherly Love","Landmark: Liberty Bell","Famous for cheesesteaks","Rocky: Iconic Philly spirit"],
     ["Stadium built: 2003","Capacity: 69,176 seats","11,000+ solar panels","14 wind turbines, net-zero energy"]),
    ("FedExField","The FedEx Giant","Landover, MD","stadium-03-dc-fedex.png","number-03-dc-profile.png",
     ["Host City: Washington DC","Landmark: White House","Smithsonian museums","National Mall & Monuments"],
     ["Stadium built: 1997","Capacity: 82,000 seats","Iconic NFL + soccer host","Near DC's historic landmarks"]),
    ("Hard Rock Stadium","Hard Rock Hero","Miami, FL","stadium-04-miami-hardrock.png","number-04-miami-profile.png",
     ["Host City: Magic City","Landmark: South Beach","Art Deco architecture","Vibrant Latin American culture"],
     ["Stadium built: 1987","Capacity: 65,326 seats","Open-air canopy covers 90%","Hosts F1 Grand Prix race too!"]),
    ("Mercedes-Benz Stadium","The Benz","Atlanta, GA","stadium-05-atlanta-benz.png","number-05-atlanta-profile.png",
     ["Host City: The ATL","Landmark: Georgia Aquarium","World's busiest airport","Southern hospitality capital"],
     ["Stadium built: 2017","Capacity: 71,000+ seats","World's largest video board","Roof opens like a flower in 8 min"]),
    ("NRG Stadium","NRG Neo","Houston, TX","stadium-06-houston-nrg.png","number-06-houston-profile.png",
     ["Host City: Space City","Landmark: Space Center Houston","Diverse, global cuisine","Home to NASA Mission Control"],
     ["Stadium built: 2002","Capacity: 72,220 seats","First retractable roof in US","Hosts Houston Livestock Show"]),
    ("AT&T Stadium","Titan Tex","Arlington, TX","stadium-07-dallas-titantex.png","number-07-dallas-profile.png",
     ["Host City: Dallas-Fort Worth","Landmark: Dealey Plaza","Texas BBQ capital","Biggest state fair in the US"],
     ["Stadium built: 2009","Capacity: 80,000+ seats","160-ft video board (like a 737!)","World's largest retractable glass doors"]),
    ("SoFi Stadium","The Infinity Giant","Inglewood, CA","stadium-08-lax-sofi.png","number-08-lax-profile.png",
     ["Host City: Los Angeles","Landmark: Hollywood Sign","Entertainment capital","Venice Beach, palm trees, stars"],
     ["Stadium built: 2020","Capacity: 70,000+ seats","Most expensive stadium ever built","Only double-sided video board in world"]),
    ("Levi's Stadium","The Silicon Giant","Santa Clara, CA","stadium-09-bayarea-levis.png","number-09-bayarea-profile.png",
     ["Host City: San Francisco Bay","Landmark: Golden Gate Bridge","Silicon Valley tech hub","Innovation & sustainability"],
     ["Stadium built: 2014","Capacity: 68,500 seats","Net-zero energy during games","Rooftop garden 'Faithful Farm'"]),
    ("Lumen Field","The Roaring Giant","Seattle, WA","stadium-10-seattle-lumen.png","number-10-seattle-profile.png",
     ["Host City: Emerald City","Landmark: Space Needle","Coffee culture capital","Stunning Pacific Northwest nature"],
     ["Stadium built: 2002","Capacity: 69,000 seats","One of the loudest stadiums","Fans caused measured earthquakes!"]),
    ("Gillette Stadium","The Lighthouse Giant","Foxborough, MA","stadium-11-boston-gillette.png","number-11-boston-profile.png",
     ["Host City: Boston, MA","Landmark: Freedom Trail","Historic New England","Home of the American Revolution"],
     ["Stadium built: 2002","Capacity: 65,878 seats","22-story lighthouse beacon","Hosts New England Revolution MLS"]),
]

for name,nick,city,stadium_img,profile_img,city_facts,stadium_facts in stadiums:
    # PAGE 1: Stadium spread
    bg(c,0.95,0.95,0.98)
    # Place stadium image on left/top
    place(D+'/'+stadium_img,TRIM_W*0.55,TRIM_H)
    # Right side: city info + stadium facts
    # City box
    c.setFillColorRGB(0.1,0.1,0.4)
    c.setFont("Helvetica-Bold",18)
    c.drawString(PW*0.58,PH-M-20,f"{name}")
    c.setFont("Helvetica",12)
    c.setFillColorRGB(0.4,0.4,0.4)
    c.drawString(PW*0.58,PH-M-45,f'"{nick}" | {city}')
    
    # City highlights
    c.setFillColorRGB(0.2,0.2,0.6)
    c.setFont("Helvetica-Bold",11)
    c.drawString(PW*0.58,PH-M-75,"City Highlights")
    c.setFont("Helvetica",10)
    c.setFillColorRGB(0.2,0.2,0.2)
    y=PH-M-95
    for fact in city_facts:
        c.drawString(PW*0.58,y,f"• {fact}");y-=16
    
    # Stadium facts
    c.setFillColorRGB(0.2,0.2,0.6)
    c.setFont("Helvetica-Bold",11)
    c.drawString(PW*0.58,y-10,"Stadium Facts")
    c.setFont("Helvetica",10)
    c.setFillColorRGB(0.2,0.2,0.2)
    y2=y-30
    for fact in stadium_facts:
        c.drawString(PW*0.58,y2,f"• {fact}");y2-=16
    
    # Divider line
    c.setStrokeColorRGB(0.7,0.7,0.7)
    c.setLineWidth(0.5)
    c.line(PW*0.57,PH*0.08,PW*0.57,PH*0.92)
    
    # Page number at bottom
    c.setFont("Helvetica",8)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawString(BLEED+20,BLEED+10,"World Cup 2026 Souvenir Guidebook")
    c.drawRightString(PW-BLEED-20,BLEED+10,f"{name}")
    c.showPage()
    
    # PAGE 2: Player profile
    bg(c,0.90,0.92,0.95)
    place(D+'/'+profile_img,TRIM_W*0.5,TRIM_H)
    # Right side: player stats
    c.setFillColorRGB(0.05,0.05,0.15,alpha=0.85)
    c.roundRect(PW*0.52,PH*0.2,TRIM_W*0.42,TRIM_H*0.7,8,fill=1,stroke=0)
    c.setFillColorRGB(1,1,1)
    c.setFont("Helvetica-Bold",16)
    c.drawCentredString(PW*0.73,PH*0.85,"⭐ Player Spotlight")
    c.setFont("Helvetica-Bold",13)
    c.drawCentredString(PW*0.73,PH*0.80,city.split(",")[0]+" Star")
    c.setFont("Helvetica",10)
    c.setFillColorRGB(0.9,0.9,1)
    
    # Real player stats by stadium name
    player_data={
        "MetLife Stadium": ("Christian Pulisic","USA","Forward","Chelsea / AC Milan","69 caps","29 goals","Youngest USMNT captain in modern era"),
        "Lincoln Financial Field": ("Vinícius Júnior","Brazil","Forward","Real Madrid","30 caps","5 goals","Known for 'Samba' dribbling style"),
        "FedExField": ("Harry Kane","England","Striker","Bayern Munich","91 caps","62 goals","England's all-time leading scorer"),
        "Hard Rock Stadium": ("Lionel Messi","Argentina","Forward","Inter Miami CF","180 caps","106 goals","8x Ballon d'Or winner"),
        "Mercedes-Benz Stadium": ("Kylian Mbappé","France","Forward","Real Madrid","75 caps","46 goals","World Cup winner at age 19"),
        "NRG Stadium": ("Victor Osimhen","Nigeria","Striker","Galatasaray","35 caps","21 goals","African Footballer of the Year"),
        "AT&T Stadium": ("Son Heung-min","South Korea","Forward","Tottenham Hotspur","127 caps","48 goals","Asia's biggest soccer star"),
        "SoFi Stadium": ("Cristiano Ronaldo","Portugal","Forward","Al Nassr FC","205 caps","128 goals","All-time international top scorer"),
        "Levi's Stadium": ("Bernardo Silva","Portugal","Midfielder","Manchester City","93 caps","12 goals","Key player in 4 Premier League titles"),
        "Lumen Field": ("Virgil van Dijk","Netherlands","Defender","Liverpool FC","68 caps","9 goals","UEFA Men's Player of the Year 2019"),
        "Gillette Stadium": ("Gianluigi Donnarumma","Italy","Goalkeeper","Paris Saint-Germain","62 caps","0 goals","Euro 2020 Player of the Tournament"),
    }
    pname,pcountry,ppos,pclub,pcaps,pgls,pfun = player_data.get(name,("Star Player","","","","","",""))
    
    stats_items=[
        f"Name: {pname}",
        f"Country: {pcountry}",
        f"Position: {ppos}",
        f"Club: {pclub}",
        f"International Caps: {pcaps}",
        f"International Goals: {pgls}",
        f"",
        f"Fun Fact:",
        f"{pfun}"
    ]
    
    y=PH*0.73
    for item in stats_items:
        c.drawString(PW*0.55,y,item);y-=18
    
    c.setFont("Helvetica",8)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawString(BLEED+20,BLEED+10,"World Cup 2026 Souvenir Guidebook")
    c.drawRightString(PW-BLEED-20,BLEED+10,f"{name} Profile")
    c.showPage()

# === SECTION 2: TECH & STATS ===
# Image has embedded text - no overlay
place(D+'/section-stats-tech.png')
c.showPage()

# Stats page
bg(c,0.95,0.95,0.98)
c.setFillColorRGB(0.1,0.1,0.4)
c.setFont("Helvetica-Bold",22)
c.drawCentredString(PW/2,PH-M-30,"World Cup 2026: By The Numbers")
c.setFont("Helvetica",12)
c.setFillColorRGB(0.2,0.2,0.2)

stats=[
    ("48 Nations","The most teams ever in a World Cup"),
    ("104 Matches","Record-breaking number of games"),
    ("16 Host Cities","Across USA, Mexico & Canada"),
    ("11 Stadium Giants","Each with a unique personality"),
    ("3 Countries","First World Cup hosted by three nations"),
    ("Billions of Fans","Global audience watching worldwide"),
    ("40,000 Tons","Steel used in MetLife Stadium alone"),
    ("11,000+ Solar Panels","Powering Lincoln Financial Field"),
    ("160 Feet","AT&T Stadium's massive video board"),
    ("8 Minutes","Mercedes-Benz roof opens or closes"),
]

y=PH-M-80
for i,(stat,desc) in enumerate(stats):
    col = i % 2
    row = i // 2
    x = BLEED+M + col*(TRIM_W//2)
    y_pos = y - row*60
    c.setFillColorRGB(0.1,0.1,0.4)
    c.setFont("Helvetica-Bold",16)
    c.drawString(x,y_pos,stat)
    c.setFont("Helvetica",10)
    c.setFillColorRGB(0.3,0.3,0.3)
    c.drawString(x,y_pos-20,desc)

c.setFont("Helvetica",8)
c.setFillColorRGB(0.5,0.5,0.5)
c.drawString(BLEED+20,BLEED+10,"World Cup 2026 Souvenir Guidebook")
c.drawRightString(PW-BLEED-20,BLEED+10,"Stats & Records")
c.showPage()

# === BACK COVER ===
place(D+'/back-cover.png')
c.showPage()

c.save()
sz=os.path.getsize(O)/(1024*1024)
print(f"Guidebook saved: {O} ({sz:.1f} MB, magazine-style, {len(stadiums)*2+5} pages)")