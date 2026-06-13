#!/usr/bin/env python3
"""Build WC 2026 Souvenir Guidebook - COMPLETE REWRITE.
   8 city facts + 8 stadium facts + 8 fun facts per stadium.
   Helvetica-Bold 22pt/14pt/11pt. Emoji-rich short punchy lines."""
import os, textwrap
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

TMP='/home/team/shared/.tmp_build';os.makedirs(TMP,exist_ok=True)
D='/home/team/shared/wc2026-guidebook-illustrations'
O='/home/team/shared/wc2026-guidebook-kdp.pdf'

TRIM_W=8.5*inch; TRIM_H=11.0*inch; BLEED=0.125*inch
PW=TRIM_W+2*BLEED; PH=TRIM_H+2*BLEED
M=0.5*inch

c=canvas.Canvas(O,pagesize=(PW,PH),pageCompression=1)

# Font - Helvetica-Bold only, three sizes
TITLE=22; HEAD=14; BODY=11; TINY=7

def place(p,w=TRIM_W,h=TRIM_H):
    if p and os.path.exists(p):
        i=Image.open(p).convert('RGB')
        i=i.resize((int(w),int(h)),Image.LANCZOS)
        t=os.path.join(TMP,os.path.basename(p).replace('.png','.jpg'))
        i.save(t,'JPEG',quality=92)
        c.drawImage(t,0,0,w,h)

def dw(text,x,y,sz=BODY,r=0,g=0,b=0):
    """Draw a Helvetica-Bold line. Returns next y position."""
    c.setFont("Helvetica-Bold",sz)
    c.setFillColorRGB(r,g,b)
    c.drawString(x,y,text)
    return y - sz*1.8

def dwc(text,x,y,sz=TITLE,r=0,g=0,b=0):
    c.setFont("Helvetica-Bold",sz)
    c.setFillColorRGB(r,g,b)
    c.drawCentredString(x,y,text)
    return y - sz*1.4

def dwr(text,x,y,sz=TINY,r=0.5,g=0.5,b=0.5):
    c.setFont("Helvetica-Bold",sz)
    c.setFillColorRGB(r,g,b)
    c.drawRightString(x,y,text)

def box(c,x,y,w,h,rgb=(0.05,0.05,0.25)):
    c.setFillColorRGB(*rgb)
    c.roundRect(x-4,y-2,w+8,h+4,4,fill=1,stroke=0)

# === STADIUM DATA: 11 stadiums × 8 city facts + 8 stadium facts + player with 8 fun facts ===
S=[
("MetLife Stadium","The Silver Giant","New York / New Jersey","stadium-01-metlife-nyc.png","number-01-metlife-profile.png",
 ["🗽 NYC — Most visited US city!","🏛️ Lady Liberty — gift from France 1886","🌎 800+ languages — most diverse","🎭 Broadway — 41 theaters, 12M fans","🚕 13,000+ yellow cabs in NYC","🍕 Pizza capital — 1,600+ pizzerias","⚡ Times Sq — 330,000 people daily","🌉 Meadowlands — NJ sports hub"],
 ["🏟️ Built 2010 | Capacity: 82,500","🛠️ 40K tons steel = 8,000 elephants","🏆 Hosts 2026 World Cup FINAL","🎨 Silver louvers change per team","🏈 Home to NY Giants + NY Jets","🌆 Meadowlands sports complex NJ","💰 $1.6B construction cost","🌐 Final match — eyes of the world!"],
 "Christian Pulisic","USA 🇺🇸","Forward","AC Milan",7,29,
 ["🇺🇸 Youngest USMNT captain ever (20)","⚡ 'Captain America' — explosive speed","🏆 1st American in UCL final","🇩🇪 Started at Dortmund age 16","🌟 US Soccer POTY 3x (2017-2019)","🌎 Scored in 2022 WC vs Iran","🎯 Known for fearless dribbling","🏅 Most capped US player under 25"]),

("Lincoln Financial Field","The Linc","Philadelphia, PA","stadium-02-philly-linc.png","number-02-philly-profile.png",
 ["🏙️ Philly — City of Brotherly Love","🔔 Liberty Bell — iconic crack since 1846","🇺🇸 First US capital 1790-1800","🥪 Cheesesteak capital of the world","🏃 Rocky Steps — 72 steps at Art Museum","📜 Independence Hall — Declaration 1776","🎓 Penn + Drexel — top universities","🎸 Live music scene — rich history"],
 ["🏟️ Built 2003 | Capacity: 69,176","☀️ 11,000+ solar panels on site","💨 14 wind turbines — net-zero energy","🌱 LEED Gold certified — green","🦅 'Eagle Wings' architecture","🏈 Home to Philadelphia Eagles","🎤 Hosted Pope Francis mass 2015","♻️ One of greenest stadiums ever"],
 "Vinícius Júnior","Brazil 🇧🇷","Forward","Real Madrid",30,5,
 ["💃 Samba dribbling — world-class style","🏆 Won Copa América 2019 with Brazil","⚽ Scored winning UCL final goal 2022","👑 Joined Real Madrid at 18 (€45M)","🌟 La Liga Best Player award 2023","🎉 Famous goal celebration dancer","🔥 Known as 'Vini' worldwide","🌎 Born in São Gonçalo, Brazil"]),

("FedExField","The FedEx Giant","Landover, MD (DC)","stadium-03-dc-fedex.png","number-03-dc-profile.png",
 ["🏛️ DC — Nation's Capital!","🏠 White House — 132 rooms, built 1792","🏛️ Lincoln Memorial — 36 columns","🌍 Smithsonian — 19 free museums","🌸 Cherry blossoms — 3,000 from Japan","📜 National Mall — 2 miles of history","🍽️ #1 Ethiopian food in USA","🎭 Kennedy Center — performing arts"],
 ["🏟️ Built 1997 | Capacity: 82,000","🎪 One of largest NFL stadiums","🌎 Near Washington Monument + Capitol","🅿️ 30,000+ parking spaces","🎵 Hosted Rolling Stones + Beyoncé","🏈 Home to Washington Commanders","📺 HD screens on all 4 sides","⭐ Massive stadium footprint"],
 "Harry Kane","England 🏴󠁧󠁢󠁥󠁮󠁧󠁿","Striker","Bayern Munich",91,62,
 ["🏴󠁧󠁢󠁥󠁮󠁧󠁿 England's ALL-TIME top scorer!","🥇 Golden Boot — 2018 WC (6 goals)","⚽ Golden Boot 3x in Premier League","🌟 Scored on PL debut at 18","📈 First English 40+ goal season","🎯 Deadly penalty accuracy 90%+","👨‍✈️ Captain of England since 2018","🏆 Scored 50+ goals for Spurs"]),

("Hard Rock Stadium","Hard Rock Hero","Miami Gardens, FL","stadium-04-miami-hardrock.png","number-04-miami-profile.png",
 ["🏖️ Miami — Magic City beaches!","🌴 South Beach — 40 Art Deco blocks","🎨 Art Deco District — 960+ buildings","🌮 Cuban coffee + pastelitos daily","☀️ 248 sunny days per year","🚢 Port of Miami — #1 cruise port","🎵 Latin music — salsa, reggaeton","🌊 Biscayne Bay views everywhere"],
 ["🏟️ Built 1987 | Capacity: 65,326","☂️ Canopy covers 90% of all seats","🏎️ Hosts F1 Miami Grand Prix","🎤 Concerts: Stones, U2, Beyoncé","🏈 Home to Miami Dolphins NFL","💸 $500M renovation in 2016","🌴 Corner spires like ship masts","⭐ Open-air tropical vibe"],
 "Lionel Messi","Argentina 🇦🇷","Forward","Inter Miami CF",180,106,
 ["👑 8x Ballon d'Or — GOAT!","🏆 Won 2022 World Cup with Argentina","⚽ 800+ career goals scored","📅 91 goals in 2012 — record!","🏟️ 4 UCL titles with Barcelona","🌟 Youngest El Clásico scorer (19)","🇦🇷 Argentina's all-time top scorer","🔥 Now plays for Inter Miami MLS"]),

("Mercedes-Benz Stadium","The Benz","Atlanta, GA","stadium-05-atlanta-benz.png","number-05-atlanta-profile.png",
 ["🏙️ Atlanta — The ATL!","🐟 World's largest aquarium (6.3M gal)","✈️ Busiest airport — 106M travelers","🍑 Southern hospitality + peach cobbler","🎵 Hip-hop capital of the South","🌳 Piedmont Park — 185 acres","🏛️ MLK Jr. National Historic Park","🥤 Coca-Cola was born here!"],
 ["🏟️ Built 2017 | Capacity: 71,000+","🌼 Roof opens like flower in 8 min","📺 Halo Board — 360° video screen","♻️ LEED Platinum — highest green","🏈 Home to Falcons + Atlanta United","⭐ Largest retractable roof NFL","🍔 $2 hot dogs — fan pricing","💎 State-of-art stadium design"],
 "Kylian Mbappé","France 🇫🇷","Forward","Real Madrid",75,46,
 ["🏆 World Cup winner at age 19 (2018)!","⚽ Hat-trick in 2022 WC final","💨 Fastest player ever on pitch","🏟️ 6 Ligue 1 titles with PSG","🌟 1st teen since Pelé in WC final","🥇 Top scorer 2022 WC (8 goals)","🇫🇷 French football phenomenon","👑 Signed for Real Madrid 2024"]),

("NRG Stadium","NRG Neo","Houston, TX","stadium-06-houston-nrg.png","number-06-houston-profile.png",
 ["🚀 Houston — Space City! NASA HQ","🛸 Space Center — see real rockets","🌮 Most diverse food scene in TX","🎸 Live music capital of the South","🏛️ 19 museums in museum district","🛍️ Galleria — TX biggest mall (2.5M sf)","🌪️ Hurricane-resistant city","⭐ Medical center — world's largest"],
 ["🏟️ Built 2002 | Capacity: 72,220","☀️ First retractable roof stadium USA","🐄 Hosts Livestock Show + Rodeo","🏈 Home to Houston Texans NFL","🏆 Super Bowls XXXVIII + LI","⚾ Hosted 2017 World Series","⭐ 1st NFL stadium with retractable roof","🎵 Hosts major concerts + events"],
 "Victor Osimhen","Nigeria 🇳🇬","Striker","Galatasaray",35,21,
 ["🏆 African Footballer of the Year 2023","🔥 Known for aerial ability + speed","⚽ 31 goals in Serie A 2022-23","🇮🇹 Napoli — 1st Serie A in 33 years","🌟 Africa Cup of Nations top scorer","🏃 Started in Lagos streets","🌎 One of Africa's most exciting","👑 Nigerian football superstar"]),

("AT&T Stadium","Titan Tex","Arlington, TX (Dallas)","stadium-07-dallas-titantex.png","number-07-dallas-profile.png",
 ["🤠 Dallas — Everything's bigger!","🥩 Texas BBQ — brisket + ribs","🎡 State Fair — biggest in USA","🏀 Dallas Mavericks NBA home","🌟 Reunion Tower — 561 ft icon","🎶 Deep Ellum — live music hub","🛍️ NorthPark Center — shopping","⭐ Fort Worth Stockyards nearby"],
 ["🏟️ Built 2009 | Capacity: 80,000+","📺 Video board 160ft — size of 737!","🚪 World's largest glass doors","🏈 Home to Dallas Cowboys NFL","🎪 Expands to 105,000 for events","📺 3,000+ HD TVs in concourse","💰 $1.3B construction cost","⭐ 'Jerry World' nickname"],
 "Son Heung-min","South Korea 🇰🇷","Forward","Tottenham Hotspur",127,48,
 ["🌟 Asia's biggest soccer superstar!","🥇 PL Golden Boot 2021-22","🏆 First Asian to win PL Golden Boot","⚽ Two-footed finishing master","🏃 Puskás Award — 70m solo run 2019","🥇 Asian Games gold medalist","👨‍✈️ Captain South Korea since 2022","🇰🇷 National hero in Korea"]),

("SoFi Stadium","The Infinity Giant","Inglewood, CA (LA)","stadium-08-lax-sofi.png","number-08-lax-profile.png",
 ["🎬 LA — Entertainment Capital!","🎥 Hollywood Sign — 45ft letters","🌴 Venice Beach — canals + skate","🎭 Walk of Fame — 2,700+ stars","🏖️ Santa Monica Pier since 1909","🌮 Best Mexican food outside MX","🎬 200+ movie studios in area","🌟 Beverly Hills — iconic lifestyle"],
 ["🏟️ Built 2020 | Capacity: 70,000+","💰 $5.5B — most expensive stadium!","🖥️ Double-sided 4K video board","🏠 Indoor-outdoor ocean breeze","🏈 Home to LA Rams + Chargers","🏆 Super Bowl LVI + 2028 Olympics","🎵 Built-in concert acoustics","⭐ 3M sq ft — massive complex"],
 "Cristiano Ronaldo","Portugal 🇵🇹","Forward","Al Nassr FC",205,128,
 ["👑 ALL-TIME international top scorer!","🏆 5x Ballon d'Or winner","⚽ 900+ career goals — legend","🇵🇹 Won Euro 2016 with Portugal","🌍 1st to score in 5 World Cups","🏟️ 140 UCL goals — all-time record","📱 600M+ Instagram followers","🔥 SIUUU celebration worldwide!"]),

("Levi's Stadium","The Silicon Giant","Santa Clara, CA (Bay Area)","stadium-09-bayarea-levis.png","number-09-bayarea-profile.png",
 ["🌉 SF Bay Area — tech capital!","🌁 Golden Gate Bridge — 1.7 miles","💻 Silicon Valley — Apple, Google, Meta","🚋 Cable cars — moving National Monument","🥖 Sourdough since Gold Rush","🌫️ 'Karl the Fog' — SF famous fog","🎓 Stanford + UC Berkeley top","🌉 Oakland Bay Bridge — 8 miles"],
 ["🏟️ Built 2014 | Capacity: 68,500","🌿 Net-zero energy on game days","🧑‍🌾 'Faithful Farm' — rooftop garden","☀️ 20,000 solar panels on lots","🏈 Home to 49ers NFL","🏆 Super Bowl 50 hosted here 2016","📱 Smart stadium app technology","🌎 Eco-friendly design award"],
 "Bernardo Silva","Portugal 🇵🇹","Midfielder","Manchester City",93,12,
 ["🏆 4x Premier League champion","🏟️ Won UCL 2023 with Man City","🧠 'The Architect' — vision master","🇵🇹 Nations League winner 2019","💰 Joined Man City from Monaco €50M","🌟 Most creative playmaker in soccer","🎯 Incredible ball control","⚽ Fan favorite for work rate"]),

("Lumen Field","The Roaring Giant","Seattle, WA","stadium-10-seattle-lumen.png","number-10-seattle-profile.png",
 ["🏔️ Seattle — Emerald City!","🗼 Space Needle — 605ft, 1962 fair","☕ Starbucks born here 1971","🌲 Olympic + Cascade mountains","🎸 Grunge — Nirvana, Pearl Jam, SG","🐟 Pike Place — flying fish since 1907","☔ 152 rainy days — keeps green!","🚢 Puget Sound — ferry capital"],
 ["🏟️ Built 2002 | Capacity: 69,000","📣 LOUDEST stadium on Earth!","🌊 Fans caused measured earthquakes","🎤 Horseshoe design = sound megaphone","🏈 Home to Seattle Seahawks NFL","⚽ Hosted 2026 WC matches","🏳️ '12th Man' flag tradition","🎵 Concussion-like noise levels"],
 "Virgil van Dijk","Netherlands 🇳🇱","Defender","Liverpool FC",68,9,
 ["🏆 UEFA Player of the Year 2019","🏟️ Won UCL 2019 with Liverpool","🥈 2nd Ballon d'Or 2019 — best D","👨‍✈️ Captain Netherlands national team","🏆 Premier League winner 2020","🛡️ Best defender in the world","🔥 50 games never dribbled past","💪 6'4\" — dominant in air"]),

("Gillette Stadium","The Lighthouse Giant","Foxborough, MA (Boston)","stadium-11-boston-gillette.png","number-11-boston-profile.png",
 ["🏛️ Boston — Historic New England","🔦 Freedom Trail — 2.5 miles, 16 sites","☕ Boston Tea Party — Revolution!","🦞 Lobster rolls + clam chowder","🎓 Harvard 1636 + MIT — finest","⚾ Fenway Park — oldest ballpark 1912","📚 First public school USA 1635","🚢 Boston Harbor — historic port"],
 ["🏟️ Built 2002 | Capacity: 65,878","💡 22-story lighthouse — iconic!","🏆 Hosted 6 Super Bowls","🛶 Bridge like Longfellow Bridge","🏈 Home to New England Patriots","⚽ Home to Revolution MLS","📯 'Foghorn' blast when home scores","🌉 New England charm everywhere"],
 "Gianluigi Donnarumma","Italy 🇮🇹","Goalkeeper","Paris Saint-Germain",62,0,
 ["🏆 Euro 2020 Player of Tournament","🇮🇹 Won Euro 2020 with Italy","📏 6'5\" — giant in goal!","👶 Debut at AC Milan at age 16","🧤 Saved 2 penalties in Euro final","🏟️ Won Ligue 1 with PSG","🌟 Youngest 200 Serie A games GK","🧱 Wall in the goal — incredible reflexes"]),
]

# ============================================================
# PAGE 1: COVER
# ============================================================
place(D+'/front-cover.png')
c.showPage()

# ============================================================
# PAGE 2: WORLD CUP HISTORY
# ============================================================
place(D+'/section-world-cup-history.png')
c.showPage()

# ============================================================
# PAGES 3-24: 11 STADIUM SPREADS (2 pages each)
# ============================================================
for idx, s in enumerate(S):
    name, nick, city, simg, pimg, cfacts, sfacts, pname, pcountry, ppos, pclub, pcaps, pgls, pfun = s

    # ----- PAGE 1: STADIUM PAGE -----
    c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
    # Stadium image left half
    place(D+'/'+simg, TRIM_W*0.50, TRIM_H)

    rx = PW * 0.52  # right column X
    rw = TRIM_W * 0.44
    ry = PH - BLEED - M - 15

    # Title
    c.setFont("Helvetica-Bold", TITLE)
    c.setFillColorRGB(0.05,0.05,0.3)
    c.drawString(rx, ry, f"#{idx+1}  {name}")
    ry -= TITLE * 1.4
    c.setFont("Helvetica-Bold", HEAD)
    c.setFillColorRGB(0.4,0.4,0.4)
    c.drawString(rx, ry, f"{nick}  •  {city}")
    ry -= HEAD * 1.6

    # ===== CITY HIGHLIGHTS =====
    box(c, rx, ry-1, rw, HEAD*1.35+4)
    c.setFont("Helvetica-Bold", HEAD)
    c.setFillColorRGB(1,1,1)
    c.drawString(rx, ry, "🏙️ CITY HIGHLIGHTS")
    ry -= HEAD * 1.3

    c.setFont("Helvetica-Bold", BODY)
    c.setFillColorRGB(0.1,0.1,0.2)
    for ft in cfacts:
        if ry < BLEED + M: break
        c.drawString(rx, ry, ft)
        ry -= BODY * 1.4

    ry -= 6

    # ===== STADIUM FACTS =====
    box(c, rx, ry-1, rw, HEAD*1.35+4)
    c.setFont("Helvetica-Bold", HEAD)
    c.setFillColorRGB(1,1,1)
    c.drawString(rx, ry, "🏟️ STADIUM FACTS")
    ry -= HEAD * 1.3

    c.setFont("Helvetica-Bold", BODY)
    c.setFillColorRGB(0.1,0.1,0.2)
    for ft in sfacts:
        if ry < BLEED + M: break
        c.drawString(rx, ry, ft)
        ry -= BODY * 1.4

    # Footer
    c.setFont("Helvetica-Bold", TINY)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawString(BLEED+20, BLEED+12, "WORLD CUP 2026 SOUVENIR GUIDEBOOK")
    c.drawRightString(PW-BLEED-20, BLEED+12, name)
    c.showPage()

    # ----- PAGE 2: PLAYER PROFILE -----
    c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
    place(D+'/'+pimg, TRIM_W*0.50, TRIM_H)

    rx2 = PW * 0.52
    rw2 = TRIM_W * 0.44
    ry2 = PH - BLEED - M - 15

    # Header
    c.setFont("Helvetica-Bold", TITLE)
    c.setFillColorRGB(0.05,0.05,0.3)
    c.drawString(rx2, ry2, "⭐ Player Spotlight")
    ry2 -= TITLE * 1.4

    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0.05,0.05,0.3)
    c.drawString(rx2, ry2, f"{pname}")
    ry2 -= 20
    c.setFont("Helvetica-Bold", BODY)
    c.setFillColorRGB(0.4,0.4,0.4)
    c.drawString(rx2, ry2, f"{pcountry}  🎯 {ppos}  🏟️ {pclub}")
    ry2 -= 30

    # Stat badges 2x2
    stats_grid = [
        ("🇺🇳 Caps", str(pcaps)),
        ("⚽ Goals", str(pgls)),
        ("🎯 Position", ppos),
        ("🏟️ Club", pclub.split()[-1]),
    ]
    bw = rw2*0.47
    bh = BODY*2.0
    for si, (label, val) in enumerate(stats_grid):
        col = si%2; row = si//2
        bx = rx2 + col*(bw+8)
        by = ry2 - row*(bh+8)
        c.setFillColorRGB(0.05,0.05,0.25)
        c.roundRect(bx, by-bh+4, bw, bh, 4, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", BODY-2)
        c.setFillColorRGB(1,1,1)
        c.drawCentredString(bx+bw/2, by-bh/2+6, val)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(bx+bw/2, by-bh/2-8, label)

    ry2 -= 2*(bh+8) + 15

    # Fun facts
    box(c, rx2, ry2-1, rw2, HEAD*1.35+4)
    c.setFont("Helvetica-Bold", HEAD)
    c.setFillColorRGB(1,1,1)
    c.drawString(rx2, ry2, "🔥 FUN FACTS")
    ry2 -= HEAD * 1.3

    c.setFont("Helvetica-Bold", BODY)
    c.setFillColorRGB(0.1,0.1,0.2)
    for ff in pfun:
        if ry2 < BLEED + M: break
        c.drawString(rx2, ry2, f"• {ff}")
        ry2 -= BODY * 1.4

    # Footer
    c.setFont("Helvetica-Bold", TINY)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawString(BLEED+20, BLEED+12, "WORLD CUP 2026 SOUVENIR GUIDEBOOK")
    c.drawRightString(PW-BLEED-20, BLEED+12, f"{pname} | {pcountry}")
    c.showPage()

# ============================================================
# PAGE 25: TECH & STATS SPREAD
# ============================================================
place(D+'/section-stats-tech.png')
c.showPage()

# ============================================================
# PAGE 26: STATS PAGE
# ============================================================
c.setFillColorRGB(0.98,0.98,1);c.rect(0,0,PW,PH,fill=1,stroke=0)

dwc("🌍 World Cup 2026: By The Numbers", PW/2, PH-M-25,
    TITLE, r=0.05, g=0.05, b=0.3)

stats = [
    ("48 Nations","Most teams ever"), ("104 Matches","Record number of games"),
    ("16 Cities","USA, Mexico, Canada"), ("11 Stadiums","Each with unique giant"),
    ("3 Countries","First tri-host WC"), ("5 Billion","Estimated TV viewers"),
    ("40,000 Tons","Steel in MetLife alone"), ("11,000","Solar panels at Linc"),
    ("160 ft","AT&T video board"), ("8 minutes","Benz roof opens"),
    ("70,000+","Average capacity"), ("$5.5 Billion","SoFi Stadium cost"),
]
cols=3; cw=(TRIM_W-2*M)/cols
sx = BLEED + M
sy = PH - M - 80
for i,(sname,sval) in enumerate(stats):
    col=i%cols; row=i//cols
    x=sx+col*cw; y=sy-row*52
    c.setFont("Helvetica-Bold",15)
    c.setFillColorRGB(0.05,0.05,0.3)
    c.drawString(x,y,sname)
    c.setFont("Helvetica-Bold",BODY)
    c.setFillColorRGB(0.3,0.3,0.3)
    c.drawString(x,y-18,sval)

c.setFont("Helvetica-Bold",TINY)
c.setFillColorRGB(0.5,0.5,0.5)
c.drawString(BLEED+20,BLEED+12,"WORLD CUP 2026 SOUVENIR GUIDEBOOK")
c.drawRightString(PW-BLEED-20,BLEED+12,"Stats & Records")
c.showPage()

# ============================================================
# BACK COVER
# ============================================================
place(D+'/back-cover.png')
c.showPage()

# ============================================================
# SAVE
# ============================================================
c.save()
sz=os.path.getsize(O)/(1024*1024)
pages = 2 + 11*2 + 2 + 1
print(f"✅ Guidebook saved: {O} ({sz:.1f} MB, {pages} pages)")
print(f"   Each: {len(cfacts)} city + {len(sfacts)} stadium + {len(pfun)} fun facts")
print("   Font: Helvetica-Bold (22pt/14pt/11pt) | Emoji-rich content")