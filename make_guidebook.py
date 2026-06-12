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
     ["🗽 City: New York / NJ — The Big Apple!","🏛️ Landmark: Statue of Liberty — a gift from France!","🌎 800+ languages spoken — most diverse city!","🎭 Broadway shows, Central Park, yellow taxis","🍕 Pizza, bagels, and the best delis in the US","⚡ Times Square — the Crossroads of the World!"],
     ["🏟️ Built: 2010 | Capacity: 82,500 seats","🛠️ 40,000 tons of steel = 8,000 elephants!","🏆 Hosts the 2026 World Cup Final!","🎨 Silver louvers change color for each team","🏈 Home to NFL's Giants & Jets","🌉 Located in the Meadowlands sports complex"],
     ["Christian Pulisic","USA 🇺🇸","Forward","Chelsea / AC Milan","69 international caps","29 international goals","Youngest USMNT captain in modern era","Nicknamed 'Captain America'","First American to play in a Champions League final","Known for explosive speed and dribbling"]),
    ("Lincoln Financial Field","The Linc","Philadelphia, PA","stadium-02-philly-linc.png","number-02-philly-profile.png",
     ["🏙️ City: Philadelphia — City of Brotherly Love","🔔 Landmark: Liberty Bell (it has a famous crack!)","🇺🇸 First capital of the United States!","🥪 Home of the Philly Cheesesteak!","🏃 Rocky steps at the Philadelphia Museum of Art","📜 Independence Hall where Declaration was signed"],
     ["🏟️ Built: 2003 | Capacity: 69,176 seats","☀️ 11,000+ solar panels — super green!","💨 14 wind turbines make clean energy!","🌱 Net-zero energy — one of the greenest stadiums","🦅 'Eagle Wings' architecture design","🏈 Home to the Philadelphia Eagles"],
     ["Vinícius Júnior","Brazil 🇧🇷","Forward","Real Madrid","30 international caps","5 international goals","Known for 'Samba' style dribbling","Won Copa America & Champions League","Nicknamed 'Vini' by fans worldwide","One of the fastest players in the world"]),
    ("FedExField","The FedEx Giant","Landover, MD","stadium-03-dc-fedex.png","number-03-dc-profile.png",
     ["🏛️ City: Washington DC — Nation's Capital!","🏠 Landmark: The White House (home of the President)","🏛️ Lincoln Memorial — 'I Have a Dream' speech","🌍 Smithsonian museums — all FREE to visit!","🌸 Cherry blossoms every spring!","📜 National Mall — 2 miles of history"],
     ["🏟️ Built: 1997 | Capacity: 82,000 seats","🏈 Hosted iconic NFL and soccer matches","🌎 Near Washington Monument & Capitol Hill","🅿️ One of the largest stadium footprints in US","🎵 Hosted concerts by The Rolling Stones & more","⭐ Near DC's historic landmarks"],
     ["Harry Kane","England 🏴󠁧󠁢󠁥󠁮󠁧󠁿","Striker","Bayern Munich","91 international caps","62 international goals","England's ALL-TIME leading scorer!","Won Golden Boot at 2018 World Cup","Known for 'deadly' penalty accuracy","Also won Premier League Golden Boot 3x"]),
    ("Hard Rock Stadium","Hard Rock Hero","Miami, FL","stadium-04-miami-hardrock.png","number-04-miami-profile.png",
     ["🏖️ City: Miami — The Magic City!","🌴 Landmark: South Beach & Ocean Drive","🎨 Art Deco architecture — colorful buildings!","🌮 Cuban coffee, pastelitos, Latin flavor!","☀️ 248 sunny days per year!","🚢 Port of Miami — Cruise Ship Capital of World"],
     ["🏟️ Built: 1987 | Capacity: 65,326 seats","☂️ Open-air canopy covers 90% of seats!","🏎️ Hosts the F1 Miami Grand Prix!","🎵 Iconic concerts by legends","🌊 Near beautiful Biscayne Bay","⭐ Home of the Miami Dolphins NFL team"],
     ["Lionel Messi","Argentina 🇦🇷","Forward","Inter Miami CF","180 international caps","106 international goals","8x Ballon d'Or winner — GOAT!","Won 2022 World Cup with Argentina!","Scored 800+ career goals","Widely considered the greatest ever"]),
    ("Mercedes-Benz Stadium","The Benz","Atlanta, GA","stadium-05-atlanta-benz.png","number-05-atlanta-profile.png",
     ["🏙️ City: Atlanta — The ATL!","🐟 Landmark: Georgia Aquarium — biggest in US!","✈️ World's busiest airport — Hartsfield-Jackson!","🍑 Southern hospitality and peach cobbler!","🎵 Hip-hop & music capital of the South","🌳 Piedmont Park — Atlanta's green heart"],
     ["🏟️ Built: 2017 | Capacity: 71,000+ seats","🌼 Roof opens like a flower in just 8 minutes!","📺 Halo Board — 360° video screen!","♻️ LEED Platinum certified — super green!","🏈 Home to Atlanta Falcons & Atlanta United","⭐ Largest retractable roof in the world"],
     ["Kylian Mbappé","France 🇫🇷","Forward","Real Madrid","75 international caps","46 international goals","World Cup winner at age 19!","Scored hat-trick in 2022 World Cup final!","One of the fastest players in history","Won 4 Ligue 1 titles with PSG"]),
    ("NRG Stadium","NRG Neo","Houston, TX","stadium-06-houston-nrg.png","number-06-houston-profile.png",
     ["🚀 City: Houston — Space City!","🛸 Landmark: Space Center Houston — NASA!","🌮 Most diverse food scene in Texas!","🎸 Live music capital of the South!","🏛️ Houston Museum of Natural Science","🛍️ The Galleria — Texas's biggest mall"],
     ["🏟️ Built: 2002 | Capacity: 72,220 seats","☀️ First retractable roof stadium in the US!","🐄 Hosts Houston Livestock Show & Rodeo","🏈 Home to the Houston Texans","🎵 Hosted Super Bowls and Final Fours","🌪️ Hurricane-resistant design"],
     ["Victor Osimhen","Nigeria 🇳🇬","Striker","Galatasaray","35 international caps","21 international goals","African Footballer of the Year!","Known for incredible aerial ability","Scored 30+ goals in Serie A season","One of Africa's most exciting stars"]),
    ("AT&T Stadium","Titan Tex","Arlington, TX","stadium-07-dallas-titantex.png","number-07-dallas-profile.png",
     ["🤠 City: Dallas-Fort Worth — Everything's Bigger!","🏛️ Landmark: Dealey Plaza & Sixth Floor Museum","🥩 Texas BBQ capital — brisket & ribs!","🎡 Biggest state fair in the US!","🏀 Home of the Dallas Mavericks (NBA)","🌟 Reunion Tower — iconic Dallas skyline"],
     ["🏟️ Built: 2009 | Capacity: 80,000+ seats","📺 Video board: 160 ft wide — like a 737 plane!","🚪 World's largest retractable glass doors!","🏈 Home to the Dallas Cowboys","🎪 Can expand to 105,000 for big events!","⭐ 3,000+ HD TVs throughout stadium"],
     ["Son Heung-min","South Korea 🇰🇷","Forward","Tottenham Hotspur","127 international caps","48 international goals","Asia's biggest soccer superstar!","Won Premier League Golden Boot 2022","First Asian to win PL Golden Boot","Known for incredible two-footed ability"]),
    ("SoFi Stadium","The Infinity Giant","Inglewood, CA","stadium-08-lax-sofi.png","number-08-lax-profile.png",
     ["🎬 City: Los Angeles — Entertainment Capital!","🎥 Landmark: Hollywood Sign!","🌴 Venice Beach, palm trees, and stars!","🎭 Home to movie studios & celebs!","🏖️ Santa Monica Pier & beautiful beaches","🌮 LA taco trucks — best Mexican food!"],
     ["🏟️ Built: 2020 | Capacity: 70,000+ seats","💰 Most expensive stadium ever built ($5.5B)!","🖥️ Only double-sided video board in the world!","🏠 Indoor-outdoor design — open to the sky!","🏈 Home to LA Rams & LA Chargers","🌟 Hosted Super Bowl LVI & 2028 Olympics"],
     ["Cristiano Ronaldo","Portugal 🇵🇹","Forward","Al Nassr FC","205 international caps","128 international goals","ALL-TIME international top scorer!","5x Ballon d'Or winner","Won Euro 2016 with Portugal","Scored 900+ career goals — legend!"]),
    ("Levi's Stadium","The Silicon Giant","Santa Clara, CA","stadium-09-bayarea-levis.png","number-09-bayarea-profile.png",
     ["🌉 City: San Francisco Bay Area!","🌁 Landmark: Golden Gate Bridge — 1.7 miles long!","💻 Silicon Valley — tech capital of the world!","🚋 Cable cars — iconic SF transport!","🥖 Sourdough bread & clam chowder!","🌫️ Famous Karl the Fog rolls over the hills"],
     ["🏟️ Built: 2014 | Capacity: 68,500 seats","🌿 Net-zero energy during games!","🧑‍🌾 Rooftop garden 'Faithful Farm' grows veggies!","☀️ Solar panels cover the parking lots!","🏈 Home to the San Francisco 49ers","📱 Super Bowl 50 was hosted here!"],
     ["Bernardo Silva","Portugal 🇵🇹","Midfielder","Manchester City","93 international caps","12 international goals","4x Premier League champion!","Known for incredible ball control","Won Champions League with Man City","One of the smartest playmakers in soccer"]),
    ("Lumen Field","The Roaring Giant","Seattle, WA","stadium-10-seattle-lumen.png","number-10-seattle-profile.png",
     ["🏔️ City: Seattle — The Emerald City!","🗼 Landmark: Space Needle — 605 ft tall!","☕ Coffee culture capital — Starbucks was born here!","🌲 Stunning Pacific Northwest nature & forests!","🎸 Grunge music history — Nirvana, Pearl Jam!","🐟 Pike Place Market — flying fish!"],
     ["🏟️ Built: 2002 | Capacity: 69,000 seats","📣 One of the LOUDEST stadiums in the world!","🌊 Fans caused measured earthquakes when cheering!","🎤 Horseshoe shape focuses sound like a megaphone!","🏈 Home to the Seattle Seahawks","⚽ Hosted 2026 World Cup matches!"],
     ["Virgil van Dijk","Netherlands 🇳🇱","Defender","Liverpool FC","68 international caps","9 international goals","UEFA Men's Player of the Year 2019!","Won Champions League with Liverpool!","Known as one of the best defenders ever","Captain of the Netherlands national team"]),
    ("Gillette Stadium","The Lighthouse Giant","Foxborough, MA","stadium-11-boston-gillette.png","number-11-boston-profile.png",
     ["🏛️ City: Boston, MA — Historic New England!","🔦 Landmark: Freedom Trail — 2.5 miles of history!","☕ Boston Tea Party — started the Revolution!","🦞 Famous for lobster rolls & clam chowder!","🎓 Harvard & MIT — world's top universities!","⚾ Fenway Park — oldest ballpark in MLB!"],
     ["🏟️ Built: 2002 | Capacity: 65,878 seats","💡 22-story lighthouse — iconic beacon!","🏆 Hosted 6 Super Bowls!","🛶 Lighthouse & bridge entrance design!","🏈 Home to the New England Patriots","⚽ Home to New England Revolution MLS"],
     ["Gianluigi Donnarumma","Italy 🇮🇹","Goalkeeper","Paris Saint-Germain","62 international caps","0 international goals","Euro 2020 Player of the Tournament!","Won Euro 2020 with Italy!","One of the best goalkeepers in the world","Standing 6'5\" — giant in the goal!"]),
]

for name,nick,city,stadium_img,profile_img,city_facts,stadium_facts,player_data in stadiums:
    # PAGE 1: Stadium spread
    bg(c,0.95,0.95,0.98)
    # Place stadium image on left/top
    place(D+'/'+stadium_img,TRIM_W*0.50,TRIM_H)
    # Right side: city info + stadium facts
    # City box background
    c.setFillColorRGB(0.05,0.05,0.2,alpha=0.08)
    c.roundRect(PW*0.52,PH*0.25,TRIM_W*0.44,TRIM_H*0.72,12,fill=1,stroke=0)
    # Title
    c.setFillColorRGB(0.1,0.1,0.4)
    c.setFont("Helvetica-Bold",20)
    c.drawString(PW*0.55,PH-M-15,f"{name}")
    c.setFont("Helvetica-Bold",13)
    c.setFillColorRGB(0.4,0.4,0.4)
    c.drawString(PW*0.55,PH-M-40,f'"{nick}" | {city}')
    
    # City highlights - BOLD font
    c.setFillColorRGB(0.2,0.2,0.6)
    c.setFont("Helvetica-Bold",13)
    c.drawString(PW*0.55,PH-M-75,"🏙️ CITY HIGHLIGHTS")
    c.setFont("Helvetica-Bold",10)
    c.setFillColorRGB(0.2,0.2,0.2)
    y=PH-M-95
    for fact in city_facts:
        c.drawString(PW*0.55,y,fact);y-=17
    
    # Stadium facts - BOLD font
    c.setFillColorRGB(0.2,0.2,0.6)
    c.setFont("Helvetica-Bold",13)
    c.drawString(PW*0.55,y-10,"🏟️ STADIUM FACTS")
    c.setFont("Helvetica-Bold",10)
    c.setFillColorRGB(0.2,0.2,0.2)
    y2=y-30
    for fact in stadium_facts:
        c.drawString(PW*0.55,y2,fact);y2-=17
    
    # Divider line
    c.setStrokeColorRGB(0.7,0.7,0.7)
    c.setLineWidth(0.5)
    c.line(PW*0.51,PH*0.08,PW*0.51,PH*0.92)
    
    # Page number at bottom
    c.setFont("Helvetica",8)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawString(BLEED+20,BLEED+10,"World Cup 2026 Souvenir Guidebook")
    c.drawRightString(PW-BLEED-20,BLEED+10,f"{name}")
    c.showPage()
    
    # PAGE 2: Player profile
    pname,pcountry,ppos,pclub,pcaps,pgls,pfun1,pfun2,pfun3,pfun4 = player_data
    bg(c,0.05,0.05,0.15)
    place(D+'/'+profile_img,TRIM_W*0.50,TRIM_H)
    # Right side: player stats panel
    c.setFillColorRGB(0.1,0.1,0.25,alpha=0.92)
    c.roundRect(PW*0.48,PH*0.05,TRIM_W*0.48,TRIM_H*0.90,12,fill=1,stroke=0)
    c.setFillColorRGB(1,1,1)
    c.setFont("Helvetica-Bold",22)
    c.drawCentredString(PW*0.72,PH*0.90,"⭐ Player Spotlight")
    c.setFont("Helvetica-Bold",16)
    c.drawCentredString(PW*0.72,PH*0.84,f"{pname}")
    c.setFont("Helvetica-Bold",12)
    c.setFillColorRGB(0.8,0.8,1)
    c.drawCentredString(PW*0.72,PH*0.80,f"{pcountry} | {ppos}")
    
    # Player stats box
    c.setFillColorRGB(0.2,0.2,0.4,alpha=0.9)
    c.roundRect(PW*0.52,PH*0.28,TRIM_W*0.40,TRIM_H*0.48,8,fill=1,stroke=0)
    
    stats_lines=[
        f"🏟️ Club: {pclub}",
        f"🇺🇳 International Caps: {pcaps}",
        f"⚽ International Goals: {pgls}",
    ]
    c.setFont("Helvetica-Bold",12)
    c.setFillColorRGB(1,1,1)
    y=PH*0.70
    for line in stats_lines:
        c.drawString(PW*0.55,y,line);y-=24
    
    # Fun facts
    c.setFont("Helvetica-Bold",13)
    c.setFillColorRGB(1,0.85,0.2)
    c.drawString(PW*0.55,y-10,"🔥 FUN FACTS")
    c.setFont("Helvetica-Bold",11)
    c.setFillColorRGB(0.9,0.9,1)
    y=y-35
    for fact in [pfun1,pfun2,pfun3,pfun4]:
        c.drawString(PW*0.55,y,f"• {fact}");y-=20
    
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
c.setFont("Helvetica-Bold",20)
c.drawCentredString(PW/2,PH-M-30,"🌍 World Cup 2026: By The Numbers")
c.setFont("Helvetica-Bold",12)
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