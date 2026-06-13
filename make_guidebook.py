#!/usr/bin/env python3
"""WC 2026 Souvenir Guidebook - HIGH GLOSS. Left half photo, right half text fills column."""
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

TMP='/home/team/shared/.tmp_build';os.makedirs(TMP,exist_ok=True)
D='/home/team/shared/wc2026-guidebook-illustrations'
O='/home/team/shared/wc2026-guidebook-kdp.pdf'

PW=8.75*inch; PH=11.25*inch
TRIM_W=8.5*inch; TRIM_H=11.0*inch; BLEED=0.125*inch
M=0.5*inch

c=canvas.Canvas(O,pagesize=(PW,PH),pageCompression=1)

def place_photo(p,x,y,box_w,box_h):
    """Place image maintaining aspect ratio, centered in box, with white background."""
    if not p or not os.path.exists(p): return
    i=Image.open(p).convert('RGB')
    iw, ih = i.size
    # Scale to fit within box_w x box_h maintaining aspect ratio
    scale = min(box_w/iw, box_h/ih)
    nw, nh = int(iw*scale), int(ih*scale)
    i=i.resize((nw,nh),Image.LANCZOS)
    t=os.path.join(TMP,os.path.basename(p).replace('.png','.jpg'))
    i.save(t,'JPEG',quality=92)
    # Center in the box
    cx = x + (box_w - nw)/2
    cy = y + (box_h - nh)/2
    c.drawImage(t, cx, cy, nw, nh)

def place_full(p):
    """Full-bleed page image."""
    if p and os.path.exists(p):
        i=Image.open(p).convert('RGB')
        i=i.resize((int(PW),int(PH)),Image.LANCZOS)
        t=os.path.join(TMP,os.path.basename(p).replace('.png','.jpg'))
        i.save(t,'JPEG',quality=92)
        c.drawImage(t,0,0,PW,PH)

# === DATA: 11 stadiums ===
S=[
("MetLife Stadium","The Silver Giant","New York / NJ","stadium-01-metlife-nyc.png","number-01-metlife-profile.png",
 "Christian Pulisic","USA","Forward","AC Milan",7,29,
 ["🗽 City: NYC — Statue of Liberty, 800+ languages, Broadway, Times Sq","🏟️ Stadium: 82,500 seats, 40K tons steel, hosts 2026 Final","🌉 Meadowlands sports complex — home to Giants + Jets","🎨 Silver louvers change color for each team playing","⚽ World Cup Final — eyes of the world on this stadium!","🔥 Fun Fact: Built with 40,000 tons of steel = 8,000 elephants!","⭐ Fan Moment: The stadium glows team colors at night","🌎 The Meadowlands — 750 acres of sports + entertainment"],
 ["👕 Christian Pulisic — 'Captain America'","🇺🇸 69 caps, 29 goals for USMNT","⚡ Forward for AC Milan / Chelsea","🏆 Youngest USMNT captain ever (age 20)","🌟 First American to play in UCL final","🎯 Known for explosive speed + dribbling","🔥 3x US Soccer Player of the Year","🌎 Born in Hershey, Pennsylvania"]),
("Lincoln Financial Field","The Linc","Philadelphia, PA","stadium-02-philly-linc.png","number-02-philly-profile.png",
 "Vinícius Júnior","Brazil","Forward","Real Madrid",30,5,
 ["🏙️ City: Philly — Liberty Bell (famous crack!), Cheesesteaks","🏟️ Stadium: 69,176 seats, 11K solar panels, net-zero energy","🇺🇸 First US capital 1790 — Independence Hall, Rocky Steps","💨 14 wind turbines + LEED Gold — one of greenest stadiums!","🦅 'Eagle Wings' architecture — iconic Philly skyline","🔥 Fun Fact: The Linc hosted Pope Francis mass in 2015!","⭐ Home to Eagles — one of NFL's loudest stadiums","🌎 11,000 solar panels = enough to power 1,000 homes"],
 ["👕 Vinícius Júnior — 'Vini'","🇧🇷 30 caps, 5 goals for Brazil","⚡ Forward for Real Madrid","🏆 Won Copa América 2019 + UCL 2022","🌟 Scored winning goal in UCL final!","🎯 Samba dribbling — one of world's best","🔥 Joined Real Madrid at 18 for €45M","🌎 Born in São Gonçalo, Brazil"]),
("FedExField","The FedEx Giant","Landover, MD (DC)","stadium-03-dc-fedex.png","number-03-dc-profile.png",
 "Harry Kane","England","Striker","Bayern Munich",91,62,
 ["🏛️ City: DC — White House, Lincoln Memorial, Smithsonian (free!)","🏟️ Stadium: 82,000 seats, near Capitol Hill, huge footprint","🌸 Cherry blossoms — 3,000 trees gifted from Japan","📜 National Mall — 2 miles of American history","🎵 Hosted Rolling Stones, Beyoncé, and major concerts","🔥 Fun Fact: 30,000+ parking spaces — one of NFL's biggest!","⭐ Near Washington Monument — 555 ft tall obelisk","🌎 19 Smithsonian museums — all free admission"],
 ["👕 Harry Kane — England captain","🏴󠁧󠁢󠁥󠁮󠁧󠁿 91 caps, 62 goals (all-time top scorer)","⚡ Striker for Bayern Munich","🏆 Golden Boot — 2018 World Cup (6 goals)","🌟 3x Premier League Golden Boot winner","🎯 Deadly penalty accuracy — 90%+ conversion","🔥 Scored on Premier League debut at 18","🌎 Born in London, England"]),
("Hard Rock Stadium","Hard Rock Hero","Miami Gardens, FL","stadium-04-miami-hardrock.png","number-04-miami-profile.png",
 "Lionel Messi","Argentina","Forward","Inter Miami CF",180,106,
 ["🏖️ City: Miami — South Beach, Art Deco, Cuban coffee, 248 sun days","🏟️ Stadium: 65,326 seats, canopy covers 90%, F1 Grand Prix","🎨 Art Deco District — 960+ colorful buildings","🚢 Port of Miami — #1 cruise port in the world","🎵 Latin music capital — salsa, reggaeton, and more","🔥 Fun Fact: Hosts Miami Grand Prix — F1 cars race around it!","⭐ Open-air tropical vibe — corner spires like ship masts","🌎 $500M renovation in 2016 transformed the stadium"],
 ["👕 Lionel Messi — The GOAT","🇦🇷 180 caps, 106 goals for Argentina","⚡ Forward for Inter Miami CF","🏆 8x Ballon d'Or winner — most ever!","🌟 Won 2022 World Cup with Argentina","🎯 800+ career goals — legendary scorer","🔥 91 goals in 2012 — world record!","🌎 Born in Rosario, Argentina"]),
("Mercedes-Benz Stadium","The Benz","Atlanta, GA","stadium-05-atlanta-benz.png","number-05-atlanta-profile.png",
 "Kylian Mbappé","France","Forward","Real Madrid",75,46,
 ["🏙️ City: Atlanta — world's busiest airport, Southern hospitality","🏟️ Stadium: 71K+ seats, roof opens like flower in 8 min","🐟 Georgia Aquarium — largest in US (6.3 million gallons)","📺 Halo Board — 360° video screen, largest in NFL","♻️ LEED Platinum — highest green building certification","🔥 Fun Fact: Fan-friendly pricing — $2 hot dogs, $5 beers!","⭐ Retractable roof — 8 'petals' that open in 8 minutes","🌎 Coca-Cola was invented in Atlanta in 1886"],
 ["👕 Kylian Mbappé — French phenom","🇫🇷 75 caps, 46 goals for France","⚡ Forward for Real Madrid","🏆 World Cup winner at age 19 (2018)!","🌟 Hat-trick in 2022 World Cup final","🎯 Fastest player ever recorded on pitch","🔥 6 Ligue 1 titles with PSG","🌎 Born in Bondy, France"]),
("NRG Stadium","NRG Neo","Houston, TX","stadium-06-houston-nrg.png","number-06-houston-profile.png",
 "Victor Osimhen","Nigeria","Striker","Galatasaray",35,21,
 ["🚀 City: Houston — Space City! NASA Mission Control HQ","🏟️ Stadium: 72,220 seats, first retractable roof in US","🛸 Space Center Houston — see real rockets and astronaut training","🌮 Most diverse food scene in Texas — 70+ cuisines","🎸 Live music capital of the South","🔥 Fun Fact: First NFL stadium with a retractable roof!","⭐ Hosted Super Bowls XXXVIII + LI + 2017 World Series","🌎 Texas Medical Center — world's largest medical complex"],
 ["👕 Victor Osimhen — Nigerian superstar","🇳🇬 35 caps, 21 goals for Nigeria","⚡ Striker for Galatasaray","🏆 African Footballer of the Year 2023","🌟 31 goals in Serie A 2022-23 season","🎯 Known for aerial ability + lightning speed","🔥 Led Napoli to first Serie A title in 33 years","🌎 Born in Lagos, Nigeria"]),
("AT&T Stadium","Titan Tex","Arlington, TX (Dallas)","stadium-07-dallas-titantex.png","number-07-dallas-profile.png",
 "Son Heung-min","South Korea","Forward","Tottenham",127,48,
 ["🤠 City: Dallas — Texas BBQ, State Fair, Reunion Tower","🏟️ Stadium: 80K+ seats, 160-ft video board (size of a 737!)","🥩 Texas BBQ capital — brisket, ribs, and sausage","📺 3,000+ HD TVs throughout the concourse","🚪 World's largest retractable glass doors","🔥 Fun Fact: Video board is longer than a Boeing 737 airplane!","⭐ 'Jerry World' — named after Cowboys owner Jerry Jones","🌎 Can expand to 105,000 seats for big events"],
 ["👕 Son Heung-min — Asia's biggest star","🇰🇷 127 caps, 48 goals for South Korea","⚡ Forward for Tottenham Hotspur","🏆 Premier League Golden Boot 2021-22","🌟 First Asian to win PL Golden Boot ever!","🎯 Puskás Award — 70m solo run goal 2019","🔥 Captain of South Korea since 2022","🌎 Born in Chuncheon, South Korea"]),
("SoFi Stadium","The Infinity Giant","Inglewood, CA (LA)","stadium-08-lax-sofi.png","number-08-lax-profile.png",
 "Cristiano Ronaldo","Portugal","Forward","Al Nassr",205,128,
 ["🎬 City: LA — Hollywood Sign, Venice Beach, Walk of Fame, studios","🏟️ Stadium: 70K+ seats, $5.5B — most expensive stadium ever!","🖥️ Only double-sided 4K video board in the world","🏠 Indoor-outdoor design — ocean breeze flows through","🌟 Hosted Super Bowl LVI + will host 2028 Olympics","🔥 Fun Fact: $5.5 billion — most expensive sports venue ever!","⭐ 3 million square feet — one of largest stadiums globally","🌎 Located in Hollywood Park — 298 acres of entertainment"],
 ["👕 Cristiano Ronaldo — CR7 legend","🇵🇹 205 caps, 128 goals (all-time top scorer!)","⚡ Forward for Al Nassr FC","🏆 5x Ballon d'Or winner","🌟 Won Euro 2016 with Portugal","🎯 900+ career goals — one of greatest ever","🔥 All-time international top scorer in history","🌎 Born in Funchal, Madeira, Portugal"]),
("Levi's Stadium","The Silicon Giant","Santa Clara, CA (Bay Area)","stadium-09-bayarea-levis.png","number-09-bayarea-profile.png",
 "Bernardo Silva","Portugal","Midfielder","Manchester City",93,12,
 ["🌉 City: SF Bay — Golden Gate Bridge (1.7 miles), Silicon Valley","🏟️ Stadium: 68,500 seats, net-zero energy, solar parking","🚋 Cable cars — iconic San Francisco transport since 1873","🧑‍🌾 Faithful Farm — rooftop garden grows veggies for games!","💻 Silicon Valley — tech capital of the world","🔥 Fun Fact: Roof garden grows tomatoes, peppers, herbs for food!","⭐ Super Bowl 50 was hosted here in 2016","🌎 Fog rolls in — 'Karl the Fog' is a local celebrity"],
 ["👕 Bernardo Silva — midfield maestro","🇵🇹 93 caps, 12 goals for Portugal","⚡ Midfielder for Manchester City","🏆 4x Premier League champion","🌟 Won Champions League with Man City 2023","🎯 Known for incredible ball control + passing","🔥 UEFA Nations League winner 2019","🌎 Born in Lisbon, Portugal"]),
("Lumen Field","The Roaring Giant","Seattle, WA","stadium-10-seattle-lumen.png","number-10-seattle-profile.png",
 "Virgil van Dijk","Netherlands","Defender","Liverpool",68,9,
 ["🏔️ City: Seattle — Space Needle (605 ft), coffee capital","🏟️ Stadium: 69,000 seats — LOUDEST stadium in the world!","☕ Starbucks was born in Seattle at Pike Place Market 1971","🌲 Pacific Northwest — stunning forests, mountains, water","🎸 Grunge music birthplace — Nirvana, Pearl Jam, Soundgarden","🔥 Fun Fact: Fans caused measured earthquakes when cheering!","⭐ Horseshoe shape focuses sound like a giant megaphone","🌎 Pike Place Market — famous flying fish since 1907"],
 ["👕 Virgil van Dijk — defensive wall","🇳🇱 68 caps, 9 goals for Netherlands","⚡ Defender for Liverpool FC","🏆 UEFA Men's Player of the Year 2019","🌟 Won Champions League with Liverpool 2019","🎯 Known as one of best defenders in history","🔥 Captain of Netherlands national team","🌎 Born in Breda, Netherlands"]),
("Gillette Stadium","The Lighthouse Giant","Foxborough, MA (Boston)","stadium-11-boston-gillette.png","number-11-boston-profile.png",
 "Gianluigi Donnarumma","Italy","Goalkeeper","Paris Saint-Germain",62,0,
 ["🏛️ City: Boston — Freedom Trail (2.5 miles), Tea Party, Harvard","🏟️ Stadium: 65,878 seats, 22-story lighthouse — iconic beacon!","🦞 Famous for lobster rolls, clam chowder, and baked beans","🏆 Hosted 6 Super Bowls — one of NFL's legendary venues","🎓 Harvard (1636) + MIT — world's top universities","🔥 Fun Fact: 22-story lighthouse is a real working beacon!","⭐ Lighthouse + bridge entrance — like a New England postcard","🌎 Home to Patriots + Revolution — football + soccer"],
 ["👕 Gianluigi Donnarumma — giant in goal","🇮🇹 62 caps, 0 goals (goalkeeper!)","⚡ Goalkeeper for Paris Saint-Germain","🏆 Euro 2020 Player of the Tournament!","🌟 Won Euro 2020 with Italy","🎯 Saved 2 penalties in Euro 2020 final shootout","🔥 Debut at AC Milan at age 16 — youngest ever","🌎 Born in Castellammare di Stabia, Italy"]),
]

# ============================================================
# PAGE 1: COVER
# ============================================================
place_full(D+'/front-cover.png')
c.showPage()

# ============================================================
# PAGE 2: WORLD CUP HISTORY
# ============================================================
place_full(D+'/section-world-cup-history.png')
c.showPage()

# ============================================================
# PAGES 3-24: 11 STADIUMS × 2 PAGES EACH
# ============================================================
for idx, s in enumerate(S):
    name, nick, city, simg, pimg, pname, pcountry, ppos, pclub, pcaps, pgls, city_facts, player_facts = s
    
    # ----- PAGE 1: STADIUM PAGE (photo left, facts fill right) -----
    c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
    # LEFT: photo centered avoiding stretch
    photo_w = TRIM_W*0.48
    photo_h = TRIM_H*0.95
    place_photo(D+'/'+simg, BLEED+8, BLEED+12, photo_w, photo_h)
    # RIGHT: facts column
    rx = BLEED + TRIM_W*0.50 + 18
    rw = TRIM_W*0.50 - 30
    ry = PH - BLEED - 25
    
    # Light background for text area
    c.setFillColorRGB(0.95,0.96,1.0)
    c.roundRect(rx-8, BLEED+5, rw+12, TRIM_H-30, 12, fill=1, stroke=0)
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.setFillColorRGB(0.05,0.05,0.3)
    c.drawString(rx, ry, f"#{idx+1}  {name}")
    ry -= 38
    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0.4,0.4,0.4)
    c.drawString(rx, ry, f'\"{nick}\"  |  {city}')
    ry -= 30
    
    # Dark header bar
    c.setFillColorRGB(0.06,0.06,0.3)
    c.roundRect(rx-2, ry-2, rw+4, 24, 4, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 13)
    c.setFillColorRGB(1,1,1)
    c.drawString(rx, ry-1, "🏙️  CITY + STADIUM FACTS")
    ry -= 32
    
    # Facts — fill the rest of the column
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0.1,0.1,0.2)
    for ft in city_facts:
        if ry < BLEED + 15: break
        c.drawString(rx, ry, ft)
        ry -= 20
    
    # Footer
    c.setFont("Helvetica-Bold", 7)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawString(BLEED+15, BLEED+8, "WORLD CUP 2026 SOUVENIR GUIDEBOOK")
    c.drawRightString(PW-BLEED-15, BLEED+8, f"Page {idx*2+3}")
    c.showPage()
    
    # ----- PAGE 2: PLAYER PROFILE (photo left, facts fill right) -----
    c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
    place_photo(D+'/'+pimg, BLEED+8, BLEED+12, photo_w, photo_h)
    
    rx = BLEED + TRIM_W*0.50 + 18
    ry = PH - BLEED - 25
    
    # Light background
    c.setFillColorRGB(0.95,0.96,1.0)
    c.roundRect(rx-8, BLEED+5, rw+12, TRIM_H-30, 12, fill=1, stroke=0)
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.setFillColorRGB(0.05,0.05,0.3)
    c.drawString(rx, ry, "⭐  Player Profile")
    ry -= 38
    c.setFont("Helvetica-Bold", 18)
    c.setFillColorRGB(0.05,0.05,0.3)
    c.drawString(rx, ry, pname)
    ry -= 28
    c.setFont("Helvetica-Bold", 13)
    c.setFillColorRGB(0.4,0.4,0.4)
    c.drawString(rx, ry, f"{pcountry}  |  {ppos}  |  {pclub}")
    ry -= 26
    
    # Stat badges
    stats = [("🇺🇳 Caps", pcaps), ("⚽ Goals", pgls), ("🎯 Position", ppos), ("🏟️ Club", pclub)]
    bw = rw*0.47
    bh = 28
    for si, (label, val) in enumerate(stats):
        col = si%2; row = si//2
        bx = rx + col*(bw+6)
        by = ry - row*(bh+6)
        c.setFillColorRGB(0.06,0.06,0.3)
        c.roundRect(bx, by-bh+4, bw, bh, 4, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 14)
        c.setFillColorRGB(1,1,1)
        c.drawCentredString(bx+bw/2, by-bh/2+5, str(val))
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(bx+bw/2, by-bh/2-9, label)
    ry -= 2*(bh+6) + 12
    
    # Fun facts header
    if ry > BLEED + 50:
        c.setFillColorRGB(0.06,0.06,0.3)
        c.roundRect(rx-2, ry-2, rw+4, 24, 4, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 13)
        c.setFillColorRGB(1,1,1)
        c.drawString(rx, ry-1, "🔥  FUN FACTS")
        ry -= 30
        
        c.setFont("Helvetica-Bold", 12)
        c.setFillColorRGB(0.1,0.1,0.2)
        for ff in player_facts:
            if ry < BLEED + 15: break
            c.drawString(rx, ry, ff)
            ry -= 20
    
    # Footer
    c.setFont("Helvetica-Bold", 7)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawString(BLEED+15, BLEED+8, "WORLD CUP 2026 SOUVENIR GUIDEBOOK")
    c.drawRightString(PW-BLEED-15, BLEED+8, f"{pname}  |  {pcountry}")
    c.showPage()

# ============================================================
# PAGE 25: TECH & STATS
# ============================================================
place_full(D+'/section-stats-tech.png')
c.showPage()

# ============================================================
# PAGE 26: STATS PAGE
# ============================================================
place_full(D+'/back-cover.png')
c.showPage()

c.save()
sz=os.path.getsize(O)/(1024*1024)
print(f"✅ Guidebook saved: {O} ({sz:.1f} MB, {len(S)*2+4} pages)")
print(f"   Each stadium: 8 city/stadium facts + 8 player fun facts")
print(f"   Layout: Full photo left, full text fills right column")