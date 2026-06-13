#!/usr/bin/env python3
"""WC 2026 Souvenir Guidebook - 2-column grid facts with category sections."""
import os, re
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit

TMP='/home/team/shared/.tmp_build';os.makedirs(TMP,exist_ok=True)
D='/home/team/shared/wc2026-guidebook-illustrations'
O='/home/team/shared/wc2026-guidebook-kdp.pdf'

PW=8.75*inch; PH=11.25*inch
TRIM_W=8.5*inch; TRIM_H=11.0*inch; BLEED=0.125*inch
M=0.5*inch

c=canvas.Canvas(O,pagesize=(PW,PH),pageCompression=1)

SML=11; HDR=13; TTL=20; TNY=7

def place_photo(p,x,y,box_w,box_h):
    if not p or not os.path.exists(p): return
    i=Image.open(p).convert('RGB')
    iw,ih=i.size
    scale=min(box_w/iw,box_h/ih)
    nw,nh=int(iw*scale),int(ih*scale)
    i=i.resize((nw,nh),Image.LANCZOS)
    t=os.path.join(TMP,os.path.basename(p).replace('.png','.jpg'))
    i.save(t,'JPEG',quality=92)
    cx=x+(box_w-nw)/2; cy=y+(box_h-nh)/2
    c.drawImage(t,cx,cy,nw,nh)

def place_full(p):
    if p and os.path.exists(p):
        i=Image.open(p).convert('RGB')
        i=i.resize((int(PW),int(PH)),Image.LANCZOS)
        t=os.path.join(TMP,os.path.basename(p).replace('.png','.jpg'))
        i.save(t,'JPEG',quality=92)
        c.drawImage(t,0,0,PW,PH)

def strip_cat(t):
    """Strip [CATEGORY] prefix from text, keep emoji and rest."""
    return re.sub(r'^\[[^\]]+\]\s*', '', t)

def draw_category_section(tx, ty, tw, title, facts, header_color=(0.06,0.06,0.3), card_color=(0.95,0.96,1.0)):
    """Draw a category section: colored header bar + 4 facts in 2x2 card grid.
    Returns new y position after the section."""
    # Header bar
    hdr_h = 20
    c.setFillColorRGB(*header_color)
    c.roundRect(tx-2, ty-hdr_h+2, tw+4, hdr_h, 4, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", HDR)
    c.setFillColorRGB(1,1,1)
    c.drawString(tx, ty-hdr_h/2-4, title)
    ty -= hdr_h + 6

    # 4 facts in 2 columns x 2 rows
    col_w = (tw - 8) / 2  # 8pt gap between columns
    gap = 6
    card_h = 24
    
    for row in range(2):
        row_y = ty - row * (card_h + gap)
        for col in range(2):
            idx = row * 2 + col
            if idx >= len(facts): break
            ft = strip_cat(facts[idx])
            cx = tx + col * (col_w + 8)
            
            # Card background
            c.setFillColorRGB(*card_color)
            c.roundRect(cx, row_y-card_h+2, col_w, card_h, 4, fill=1, stroke=0)
            
            # Text - try to fit in the card width
            c.setFont("Helvetica-Bold", SML)
            c.setFillColorRGB(0.1,0.1,0.2)
            # Use simpleSplit to wrap text
            lines = simpleSplit(ft, c._fontname, c._fontsize, col_w - 6)
            if lines:
                c.drawString(cx+3, row_y-card_h/2-4, lines[0])
    
    ty -= 2 * (card_h + gap) - gap + 4
    
    # Divider line between sections
    c.setStrokeColorRGB(0.85,0.85,0.9)
    c.setLineWidth(0.5)
    c.line(tx, ty, tx+tw, ty)
    ty -= 8
    
    return ty

# === DATA (unchanged from v3) ===
S=[
("MetLife Stadium","The Silver Giant","New York / NJ","stadium-01-metlife-nyc.png","number-01-metlife-profile.png",
 "Christian Pulisic","USA","Forward","AC Milan",7,29,
 ["[🏙️ CITY] 🗽 Statue of Liberty — Standing tall in the harbor, this iconic lady has welcomed visitors to the New York area for over 100 years!",
  "[🏙️ CITY] 🏙️ Linguistically Diverse — NYC is the most diverse city on Earth, with over 800 different languages spoken by its amazing residents!",
  "[🏙️ CITY] 🎭 Broadway Stars — The famous theater district hosts 41 professional theaters and draws 12 million excited fans every single year!",
  "[🏙️ CITY] 🍕 Pizza Capital — With more than 1,600 pizzerias, you are never more than a few blocks away from a world-famous New York slice!",
  "[🏟️ STADIUM] 🏟️ Massive Capacity — With 82,500 seats, this stadium is big enough to hold a whole city of cheering soccer fans!",
  "[🏟️ STADIUM] 🎨 Silver Louvers — The stadium's unique silver exterior can glow in different colors to match the teams playing on the field!",
  "[🏟️ STADIUM] 🔥 Steel Giant — It took 40,000 tons of steel to build this stadium, which is the same weight as 8,000 massive African elephants!",
  "[🏟️ STADIUM] ⚽ The Big Stage — This legendary venue has been chosen to host the 2026 World Cup Final, where the new world champion will be crowned!",
  "[🌟 WOW] 🌉 Meadowlands Magic — The stadium is part of a giant 750-acre sports and entertainment complex that was once just a swampy marsh!",
  "[🌟 WOW] 🚕 Yellow Cabs — There are over 13,000 iconic yellow taxis zipping through the city streets, making them a true symbol of New York!",
  "[🌟 WOW] ⚡ Times Square — About 330,000 people walk through this neon-lit intersection every day, making it one of the busiest places on the planet!",
  "[🌟 WOW] ⭐ Glowing Nights — At night, the entire stadium glows brilliantly, creating a stunning view that can be seen from miles away!"],
 ["[⚽ CAREER] 👕 Captain America — Christian Pulisic is the leader of the US team and earned his nickname by being a hero on the soccer pitch!",
  "[⚽ CAREER] ⚡ Speed Demon — Known for his explosive speed and amazing dribbling, Christian can zip past defenders before they even see him!",
  "[⚽ CAREER] 🇩🇪 Dortmund Debut — He started his professional career in Germany with Borussia Dortmund when he was just 16 years old!",
  "[⚽ CAREER] 📈 Young Record-Breaker — Christian holds the record for being the youngest player to ever captain the US Men's National Team!",
  "[🏆 ACHIEVEMENTS] 🇺🇸 National Hero — He has played over 60 times for the USA and has scored 29 goals, including a huge one in the 2022 World Cup!",
  "[🏆 ACHIEVEMENTS] 🌟 Champions League — Christian was the first American man to ever play in and win a UEFA Champions League final!",
  "[🏆 ACHIEVEMENTS] 🔥 Player of the Year — He is so talented that he has been named the US Soccer Male Player of the Year three different times!",
  "[🏆 ACHIEVEMENTS] 🏅 Key Playmaker — Since his debut in 2016, he has been the most important player for the United States in every big tournament!",
  "[🎯 EXTRA] 🌎 Hershey Born — Christian was born and raised in Hershey, Pennsylvania, which is also famous for making delicious chocolate!",
  "[🎯 EXTRA] ⚡ Forward Focus — Whether he is playing for AC Milan in Italy or the USA, Christian always plays as an attacking forward!",
  "[🎯 EXTRA] ⚽ Scoring Touch — He is famous for his 'clutch' goals, meaning he scores when his team needs him the most during big games!",
  "[🎯 EXTRA] 🏠 Soccer Family — Soccer is in his blood; both of his parents played college soccer and his father even played professionally!"]),
("Lincoln Financial Field","The Linc","Philadelphia, PA","stadium-02-philly-linc.png","number-02-philly-profile.png",
 "Vinícius Júnior","Brazil","Forward","Real Madrid",30,5,
 ["[🏙️ CITY] 🏙️ Brotherly Love — Philadelphia is known as the 'City of Brotherly Love' and was the first capital of the United States!",
  "[🏙️ CITY] 🔔 The Liberty Bell — This famous bell with its giant crack is a symbol of American freedom and lives right in the heart of Philly!",
  "[🏙️ CITY] 🥨 Soft Pretzel City — Philly is world-famous for its delicious soft pretzels and refreshing 'Water Ice' treats that kids love!",
  "[🏙️ CITY] 🎨 Mural Masterpiece — Philadelphia has more outdoor murals than any other city in the world, turning the streets into a giant art gallery!",
  "[🏟️ STADIUM] 🏟️ Solar Power — The Linc is covered in 11,000 solar panels, which generate enough clean energy to power 1,000 homes!",
  "[🏟️ STADIUM] 💨 Wind Turbines — To be even greener, the stadium has 14 wind turbines that spin in the breeze to create electricity!",
  "[🏟️ STADIUM] 🦅 Eagle Wings — The stadium's architecture features unique 'wing' shapes on the roof to match the Eagles team that plays there!",
  "[🏟️ STADIUM] 🏈 Historic Turf — Beyond soccer, this field has hosted the famous Army-Navy college football game many times since 1890!",
  "[🌟 WOW] 🏙️ Rocky Steps — You can run up the 72 stone steps at the Art Museum just like Rocky Balboa did in his famous movies!",
  "[🌟 WOW] 🥩 Cheesesteak Challenge — Visitors love to try the city's famous cheesesteaks, usually choosing between 'Pat's' or 'Geno's' shops!",
  "[🌟 WOW] 🔥 Pope's Visit — In 2015, the stadium was so important that Pope Francis held a massive outdoor mass right on the field!",
  "[🌟 WOW] ⭐ Super Fans — Philly fans are known as some of the loudest and most passionate in the world, making the stadium shake with noise!"],
 ["[⚽ CAREER] 👕 Vini Jr. — Vinícius Júnior is a superstar forward from Brazil who uses his incredible skills to dazzle fans around the world!",
  "[⚽ CAREER] 🎯 Samba Dribbler — Growing up in Brazil, Vini learned to dribble with 'Samba' style, making him one of the hardest players to stop!",
  "[⚽ CAREER] 👟 Jersey Number 7 — He wears the legendary number 7 for Real Madrid, the same number worn by many of the greatest players ever!",
  "[⚽ CAREER] 🧒 Futsal Beginnings — Vini started playing futsal, a fast-paced indoor version of soccer, which helped him develop his lightning-fast footwork!",
  "[🏆 ACHIEVEMENTS] 🏆 Champions League Hero — He scored the winning goal in the 2022 Champions League final, making him a legend for Real Madrid!",
  "[🏆 ACHIEVEMENTS] 🌟 Double Final Scorer — He is so talented that he has actually scored in two different Champions League final matches!",
  "[🏆 ACHIEVEMENTS] 🇧🇷 Brazil Pride — Vini has represented Brazil over 30 times and even helped them win the Copa América trophy in 2019!",
  "[🏆 ACHIEVEMENTS] 🔥 Big Transfer — Real Madrid was so impressed by him that they signed him when he was only 18 years old for a huge fee!",
  "[🎯 EXTRA] 🌎 São Gonçalo — Vini was born in São Gonçalo, a city near Rio de Janeiro, where he first started dreaming of becoming a soccer star!",
  "[🎯 EXTRA] 🗣️ Helping Hands — He runs his own charity called the Vini Jr. Institute to help use technology to improve education for kids in Brazil!",
  "[🎯 EXTRA] ⚡ Real Madrid Star — He plays for Real Madrid in Spain, one of the most famous and successful soccer clubs in the entire world!",
  "[🎯 EXTRA] ⚽ Joyful Play — Vini is famous for playing with a big smile on his face and celebrating his goals with amazing dance moves!"]),
("FedExField","The FedEx Giant","Landover, MD (DC)","stadium-03-dc-fedex.png","number-03-dc-profile.png",
 "Harry Kane","England","Striker","Bayern Munich",91,62,
 ["[🏙️ CITY] 🏛️ Capitol Capital — Washington D.C. is the center of the US government and is home to the White House and the beautiful Capitol building!",
  "[🏙️ CITY] 🌸 Cherry Blossoms — Every spring, the city turns pink when 3,000 cherry trees, a gift from Japan, bloom all at once!",
  "[🏙️ CITY] 🏛️ No Skyscrapers — D.C. has no tall skyscrapers because no building is allowed to be much taller than the street is wide!",
  "[🏙️ CITY] 📖 Library of Congress — This amazing building is the largest library in the entire world, with millions of books on its shelves!",
  "[🏟️ STADIUM] 🏟️ Huge Footprint — FedExField is one of the largest stadiums in the NFL, with enough room for 82,000 fans to watch the action!",
  "[🏟️ STADIUM] 🚗 Parking King — The stadium has over 30,000 parking spaces, making it one of the biggest parking lots in all of sports!",
  "[🏟️ STADIUM] 🎵 Concert Central — When the game is over, the stadium hosts giant concerts for stars like Beyoncé and the Rolling Stones!",
  "[🏟️ STADIUM] ⭐ Global Concourse — Fans from all over the world gather here to fly their flags and celebrate their favorite teams!",
  "[🌟 WOW] 📜 National Mall — This 2-mile long park is filled with history, from the Lincoln Memorial to the towering Washington Monument!",
  "[🌟 WOW] 🏛️ Free Museums — All 19 Smithsonian museums in the city are completely free to visit, so you can see dinosaurs and space shuttles for free!",
  "[🌟 WOW] 🌳 Giant Park — Rock Creek Park is a massive forest inside the city that is actually twice as large as New York's Central Park!",
  "[🌟 WOW] ⛸️ Winter Fun — In the winter, the city's Sculpture Garden turns into a giant outdoor ice rink where families go skating!"],
 ["[⚽ CAREER] 👕 England Captain — Harry Kane is the leader of the England national team and one of the best strikers to ever play the game!",
  "[⚽ CAREER] 🎯 Penalty King — Harry is famous for his incredible accuracy from the penalty spot, scoring over 90% of the penalties he takes!",
  "[⚽ CAREER] 🦁 Premier League Legend — Before moving to Germany, Harry scored against every single Premier League team he ever faced!",
  "[⚽ CAREER] ⚡ Striker Power — Whether playing for Bayern Munich or England, Harry is always the 'Number 9' who leads the attack!",
  "[🏆 ACHIEVEMENTS] 🏴󠁧󠁢󠁥󠁮󠁧󠁿 All-Time Scorer — Harry Kane holds the amazing record for scoring the most goals in the history of the England national team!",
  "[🏆 ACHIEVEMENTS] 🏆 Golden Boot — He won the World Cup Golden Boot in 2018 for being the top scorer of the whole tournament with 6 goals!",
  "[🏆 ACHIEVEMENTS] 🌟 Triple Winner — He has won the Premier League Golden Boot award three different times for being the league's best scorer!",
  "[🏆 ACHIEVEMENTS] 🏰 Royal Honor — Because he is such a great representative for his country, the Queen awarded him an MBE medal!",
  "[🎯 EXTRA] 🌎 London Born — Harry was born in London, England, and grew up very close to the stadium where his first pro team played!",
  "[🎯 EXTRA] 🐕 Labrador Love — Harry has two beautiful Labrador dogs named Brady and Wilson, who are named after famous NFL quarterbacks!",
  "[🎯 EXTRA] ⚽ Late Bloomer — When he was very young, one team told him he wasn't good enough, but he worked hard and proved them all wrong!",
  "[🎯 EXTRA] 🧒 Teamwork First — Even though he scores many goals, Harry is famous for helping his teammates and being a great friend on the field!"]),
("Hard Rock Stadium","Hard Rock Hero","Miami Gardens, FL","stadium-04-miami-hardrock.png","number-04-miami-profile.png",
 "Lionel Messi","Argentina","Forward","Inter Miami CF",180,106,
 ["[🏙️ CITY] 🏖️ Sunshine City — Miami is known for its beautiful beaches and gets about 248 days of bright sunshine every single year!",
  "[🏙️ CITY] 🎨 Art Deco Style — The South Beach area is famous for its 'Art Deco' buildings, which are painted in bright, beautiful neon colors!",
  "[🏙️ CITY] ☀️ Nature's Mix — Miami is the only place in the world where both alligators and crocodiles live together in the wild!",
  "[🏙️ CITY] 🚢 Cruise Capital — The Port of Miami is the busiest cruise ship port in the world, with giant ships leaving for the islands every day!",
  "[🏟️ STADIUM] 🏟️ Shade for All — The stadium has a massive 'open-air' canopy that covers 90% of the seats to keep fans dry and out of the sun!",
  "[🏟️ STADIUM] 🏎️ F1 Race Track — Once a year, the area around the stadium is turned into a high-speed Formula 1 race track for the Miami Grand Prix!",
  "[🏟️ STADIUM] 🚢 Ship Mast Spires — The four huge white spires at the corners of the stadium are designed to look like the masts of a giant ship!",
  "[🏟️ STADIUM] ⭐ Tropical Vibe — With its open corners and ocean breezes, watching a game here feels like being at a giant tropical party!",
  "[🌟 WOW] 🎵 Latin Music — Miami is the capital of Latin music, where you can hear the sounds of salsa, reggaeton, and bachata everywhere you go!",
  "[🌟 WOW] 🎨 Wynwood Walls — The city is home to the world's largest collection of street art, where giant murals cover every building!",
  "[🌟 WOW] 🏢 Skyline Views — Miami has the third tallest skyline in the United States, filled with shimmering glass towers along the ocean!",
  "[🌟 WOW] 🌊 Park Paradise — Miami is the only US city bordered by two different National Parks: the Everglades and Biscayne National Park!"],
 ["[⚽ CAREER] 👕 The GOAT — Many fans believe Lionel Messi is the 'Greatest of All Time' because of his incredible magic with the soccer ball!",
  "[⚽ CAREER] 🇦🇷 Argentina's Star — Messi has played a record 180 matches for Argentina and has scored over 100 goals for his home country!",
  "[⚽ CAREER] ⚡ Inter Miami — After playing in Europe for many years, Messi moved to Florida to play for Inter Miami CF in the United States!",
  "[⚽ CAREER] 🎯 Record Breaker — In the year 2012, Messi scored an unbelievable 91 goals, which is the world record for the most goals in one year!",
  "[🏆 ACHIEVEMENTS] 🏆 World Cup Winner — In 2022, Messi finally achieved his biggest dream by leading Argentina to victory in the World Cup!",
  "[🏆 ACHIEVEMENTS] 🌟 Ballon d'Or — He has been named the best player in the world 8 times, winning the Ballon d'Or trophy more than anyone else!",
  "[🏆 ACHIEVEMENTS] 🔥 Trophy King — Messi has won 44 team trophies in his career, which is the most by any soccer player in the history of the sport!",
  "[🏆 ACHIEVEMENTS] ⚽ Goal Machine — He has scored over 800 goals in his career, including some of the most beautiful solo runs ever seen!",
  "[🎯 EXTRA] 🌎 Rosario Born — Messi was born in Rosario, Argentina, and started playing for a local club when he was only five years old!",
  "[🎯 EXTRA] 🧒 Growth Miracle — When he was a kid, he was very small and needed special medicine to help him grow tall enough to play pro soccer!",
  "[🎯 EXTRA] 🥘 Favorite Food — His favorite meal is 'Milanesa a la Napolitana,' which is a special Argentine steak covered in cheese and sauce!",
  "[🎯 EXTRA] ✍️ Napkin Contract — He was so good as a child that his first contract with FC Barcelona was written on a paper napkin at a restaurant!"]),
("Mercedes-Benz Stadium","The Benz","Atlanta, GA","stadium-05-atlanta-benz.png","number-05-atlanta-profile.png",
 "Kylian Mbappé","France","Forward","Real Madrid",75,46,
 ["[🏙️ CITY] 🏙️ Busy Skies — Atlanta's airport is the busiest in the entire world, with thousands of planes taking off and landing every single day!",
  "[🏙️ CITY] 🌲 Forest City — Atlanta is known as the 'City in a Forest' because it has more trees covering it than almost any other major city!",
  "[🏙️ CITY] 🥤 Coke's Home — The world-famous Coca-Cola drink was invented right here in Atlanta way back in the year 1886!",
  "[🏙️ CITY] 🍑 The Peach State — Georgia is famous for its peaches, but surprisingly, its biggest and most valuable crop is actually peanuts!",
  "[🏟️ STADIUM] 🏟️ Petal Roof — The stadium's roof is made of 8 giant 'petals' that open and close just like a blooming flower in only 8 minutes!",
  "[🏟️ STADIUM] 📺 Halo Board — Inside, there is a giant 360-degree video screen called the 'Halo Board' that is the largest screen in all of sports!",
  "[🏟️ STADIUM] ♻️ Super Green — This stadium is 'LEED Platinum' certified, which means it is one of the most environmentally friendly buildings ever made!",
  "[🏟️ STADIUM] 🔥 Fan-Friendly — The stadium is famous for its low food prices, where fans can get hot dogs and popcorn for just a few dollars!",
  "[🌟 WOW] 🌟 Giant Aquarium — Atlanta is home to the Georgia Aquarium, which is the largest in the US and holds 6 million gallons of water!",
  "[🌟 WOW] 🎡 Sky High — You can ride 'SkyView Atlanta,' a massive 20-story tall Ferris wheel that gives you a view of the whole city!",
  "[🌟 WOW] 🦒 Zoo Atlanta — The city's zoo is one of the only places in the United States where you can see giant pandas playing!",
  "[🌟 WOW] ⭐ Tech Wonder — The stadium's massive video board is so big that a jumbo jet could actually fit inside the screen!"],
 ["[⚽ CAREER] 👕 French Phenom — Kylian Mbappé is a lightning-fast superstar from France who is considered the best young player in the world!",
  "[⚽ CAREER] ⚡ Real Madrid Bound — After scoring hundreds of goals in France for PSG, Kylian moved to Spain to play for the famous Real Madrid!",
  "[⚽ CAREER] 🎯 Record Speed — Kylian is one of the fastest players ever recorded, reaching speeds of 38 km/h—almost as fast as a car!",
  "[⚽ CAREER] 🔥 Goal Leader — He has already won 6 league titles in France and has been the top scorer of the league for many years in a row!",
  "[🏆 ACHIEVEMENTS] 🏆 World Cup Winner — Kylian became a legend at just 19 years old when he helped France win the 2018 World Cup!",
  "[🏆 ACHIEVEMENTS] 🌟 Hat-Trick Hero — In the 2022 World Cup final, he scored three goals (a hat-trick), something that hadn't been done in 50 years!",
  "[🏆 ACHIEVEMENTS] 🥇 Golden Boot — He won the Golden Boot award at the 2022 World Cup for being the tournament's top scorer with 8 goals!",
  "[🏆 ACHIEVEMENTS] 🇫🇷 France's Future — Kylian is the captain of the French national team and is on his way to breaking all of their scoring records!",
  "[🎯 EXTRA] 🌎 Bondy Born — Kylian was born in Bondy, a small town near Paris, where his father was his very first soccer coach!",
  "[🎯 EXTRA] 🐢 Ninja Turtle — His teammates give him the funny nickname 'Donatello' because they think he looks like one of the Teenage Mutant Ninja Turtles!",
  "[🎯 EXTRA] 🤝 Giving Back — After winning the World Cup in 2018, he donated all of his prize money to a charity that helps sick and disabled children!",
  "[🎯 EXTRA] ⚽ Childhood Dreams — As a kid, his bedroom walls were completely covered in posters of his hero, Cristiano Ronaldo!"]),
("NRG Stadium","NRG Neo","Houston, TX","stadium-06-houston-nrg.png","number-06-houston-profile.png",
 "Victor Osimhen","Nigeria","Striker","Galatasaray",35,21,
 ["[🏙️ CITY] 🚀 Space City — Houston is home to NASA's Mission Control, which is why it is famously known around the world as 'Space City!'",
  "[🏙️ CITY] 🌮 Foodie Heaven — Houston has one of the most diverse food scenes in America, with over 70 different types of global cuisines to try!",
  "[🏙️ CITY] 🎸 Music Hub — The city is a major center for live music and is the birthplace of many famous singers and superstar performers!",
  "[🏙️ CITY] 🤠 Energy Capital — Houston is known as the 'Energy Capital of the World' because so many of the world's oil and gas companies are based there!",
  "[🏟️ STADIUM] 🏟️ First of its Kind — NRG Stadium was the very first NFL stadium in the United States to be built with a retractable roof!",
  "[🏟️ STADIUM] 🐂 Rodeo Ready — Every year, the stadium is filled with dirt and animals for the Houston Livestock Show and Rodeo, the largest in the world!",
  "[🏟️ STADIUM] ⚽ Soccer History — This field has hosted many huge games, including matches for the Copa América and several Super Bowls!",
  "[🏟️ STADIUM] ⭐ Massive Space — The stadium can hold over 72,000 fans, and the floor space is large enough to host almost any event imaginable!",
  "[🌟 WOW] 🛸 Real Rockets — At Space Center Houston nearby, you can walk inside a real space shuttle and see giant Saturn V rockets!",
  "[🌟 WOW] 🏗️ Multi-Sport — The stadium is so well-designed that it can switch from a soccer field to a rodeo arena in just a few days!",
  "[🌟 WOW] 🚇 Tunnel System — 20 feet below the city streets is a 7-mile long tunnel system filled with shops and restaurants for people to enjoy!",
  "[🌟 WOW] 🏥 Medical Center — Houston is home to the world's largest medical complex, where doctors help thousands of people every day!"],
 ["[⚽ CAREER] 👕 Nigerian Star — Victor Osimhen is a powerful striker from Nigeria who is famous for his incredible strength and scoring ability!",
  "[⚽ CAREER] ⚡ Striker Power — Victor plays as a 'Center Forward,' meaning his main job is to use his speed to get behind defenders and score!",
  "[⚽ CAREER] 🎯 Goal Machine — During the 2022-23 season in Italy, he scored 31 goals, proving he is one of the best finishers on the planet!",
  "[⚽ CAREER] 🦅 Super Eagle — He is the star player for the Nigeria national team, which is nicknamed the 'Super Eagles' by their fans!",
  "[🏆 ACHIEVEMENTS] 🏆 African Player of the Year — In 2023, Victor was officially named the best soccer player in all of Africa!",
  "[🏆 ACHIEVEMENTS] 🌟 Napoli Legend — He led his team, Napoli, to their first Italian league title in 33 years, making him a hero in the city of Naples!",
  "[🏆 ACHIEVEMENTS] 🔥 Serie A Record — Victor holds the record for being the highest-scoring African player in the history of the Italian 'Serie A' league!",
  "[🏆 ACHIEVEMENTS] 👟 Academy Start — He began his soccer journey at the 'Ultimate Strikers Academy' in Lagos, Nigeria, before moving to Europe!",
  "[🎯 EXTRA] 🌎 Lagos Born — Victor was born in Lagos, Nigeria, and as a kid, he helped his family by selling bottled water in the busy city streets!",
  "[🎯 EXTRA] 🎭 The Masked Man — Victor wears a special black protective mask during every game, which has become his famous trademark look!",
  "[🎯 EXTRA] ⚽ Fighting Spirit — He is known for never giving up on a ball and using his amazing 'leap' to win headers high in the air!",
  "[🎯 EXTRA] 🤝 Helping Others — Victor is very proud of his roots and often helps young soccer players in Nigeria reach their dreams of playing pro!"]),
("AT&T Stadium","Titan Tex","Arlington, TX (Dallas)","stadium-07-dallas-titantex.png","number-07-dallas-profile.png",
 "Son Heung-min","South Korea","Forward","Tottenham",127,48,
 ["[🏙️ CITY] 🤠 Cowboy Culture — Dallas is a city where you can see real cowboys, visit the State Fair of Texas, and eat world-class BBQ!",
  "[🏙️ CITY] 🥩 BBQ Capital — Texas is famous for its slow-cooked BBQ, and Dallas is one of the best places to find delicious brisket and ribs!",
  "[🏙️ CITY] 🎢 Six Flags — The very first 'Six Flags' theme park was opened right here in the Dallas area over 60 years ago!",
  "[🏙️ CITY] 🎡 Tallest Wheel — Dallas is home to the 'Texas Star,' which was the tallest Ferris wheel in North America for many years!",
  "[🏟️ STADIUM] 🏟️ Jerry World — This stadium is so big and expensive that people nickname it 'Jerry World' after the owner of the Dallas Cowboys!",
  "[🏟️ STADIUM] 📺 Video Giant — The stadium features a massive video board that is 160 feet wide—that's actually longer than a Boeing 737 airplane!",
  "[🏟️ STADIUM] 🚪 Glass Doors — The stadium has the world's largest retractable glass doors, which can open up to let in the fresh Texas air!",
  "[🏟️ STADIUM] ⭐ Expandable Seats — While it usually holds 80,000 people, the stadium can expand to hold a massive crowd of 105,000 fans!",
  "[🌟 WOW] 🍹 Frozen Drinks — Did you know the very first frozen margarita machine was invented in Dallas in the year 1971?",
  "[🌟 WOW] 📺 TV Overload — There are over 3,000 high-definition TVs located throughout the stadium, so you never miss a second of the game!",
  "[🌟 WOW] 🏟️ Power Hungry — On a game day, this stadium uses more electricity than an entire small town does in a whole day!",
  "[🌟 WOW] 🎡 Fair Fun — The stadium is located right near the site of the State Fair of Texas, where you can see the 55-foot tall 'Big Tex' statue!"],
 ["[⚽ CAREER] 👕 Asia's Icon — Son Heung-min is the most famous soccer player in Asia and the captain of both the South Korea team and Tottenham!",
  "[⚽ CAREER] ⚡ Two-Footed Magic — Son is famous for being able to kick the ball perfectly with both his left and right feet, making him a defender's nightmare!",
  "[⚽ CAREER] 🎯 Tottenham Star — He has played in England for Tottenham Hotspur for many years and has scored over 150 goals for the club!",
  "[⚽ CAREER] 🔥 Forward Focus — Son uses his amazing speed and clever runs to play as a forward or a winger on the side of the field!",
  "[🏆 ACHIEVEMENTS] 🏆 Golden Boot — Son made history in 2022 by becoming the first Asian player ever to win the Premier League Golden Boot!",
  "[🏆 ACHIEVEMENTS] 🌟 Puskás Award — In 2019, he won the Puskás Award for the 'Best Goal of the Year' after a 70-meter solo run where he beat the whole team!",
  "[🏆 ACHIEVEMENTS] 🇰🇷 Korea's Captain — He has played over 120 times for South Korea and has led them in three different World Cup tournaments!",
  "[🏆 ACHIEVEMENTS] 🎖️ Military Service — In 2020, Son showed his dedication by completing his mandatory military training in South Korea during his break!",
  "[🎯 EXTRA] 🌎 Chuncheon Born — Son was born in Chuncheon, South Korea, and was coached by his father, who was also a professional soccer player!",
  "[🎯 EXTRA] 👋 Camera Celebration — Every time he scores, Son makes a 'camera' shape with his hands to show he is 'capturing' the happy memory!",
  "[🎯 EXTRA] 🎹 Piano Player — When he is not playing soccer, Son loves to relax by playing the piano or playing fun video games with his friends!",
  "[🎯 EXTRA] ⚽ Hard Worker — His father once made him practice keepy-uppies for four hours straight without dropping the ball to help him get better!"]),
("SoFi Stadium","The Infinity Giant","Inglewood, CA (LA)","stadium-08-lax-sofi.png","number-08-lax-profile.png",
 "Cristiano Ronaldo","Portugal","Forward","Al Nassr",205,128,
 ["[🏙️ CITY] 🎬 Hollywood Magic — Los Angeles is the movie capital of the world, where you can find the Walk of Fame and the famous Hollywood Sign!",
  "[🏙️ CITY] 🏖️ Beach Life — LA has some of the most famous beaches in the world, like Venice Beach and Santa Monica, where people surf all year!",
  "[🏙️ CITY] 🎬 Landmark Sign — The giant 'HOLLYWOOD' sign on the hill originally said 'HOLLYWOODLAND' when it was first built as an advertisement!",
  "[🏙️ CITY] 🍦 Sweet Invention — Did you know that the delicious 'Hot Fudge Sundae' ice cream treat was actually invented in Los Angeles?",
  "[🏟️ STADIUM] 🏟️ Most Expensive — SoFi Stadium cost $5.5 billion to build, making it the most expensive and high-tech sports stadium ever made!",
  "[🏟️ STADIUM] 🏠 Indoor-Outdoor — The stadium has a giant clear roof, but the sides are open to let the cool ocean breezes flow through the seats!",
  "[🏟️ STADIUM] 🖥️ The Infinity Screen — Hanging from the roof is a double-sided 4K video board that is shaped like a giant oval and is larger than the field!",
  "[🏟️ STADIUM] ⭐ Earthquake Proof — To stay safe, the stadium's massive roof is held up by 37 giant pillars that are designed to withstand earthquakes!",
  "[🌟 WOW] 🌟 Star Power — LA is home to more movie stars and celebrities than any other city, and you might even spot one at a soccer game!",
  "[🌟 WOW] 🏟️ Massive Size — The stadium is so big that it covers 3 million square feet, which is enough space to fit many city blocks inside!",
  "[🌟 WOW] 🔭 Star Gazing — The city is home to the Griffith Observatory, where you can look through giant telescopes at the stars in space!",
  "[🌟 WOW] 🌎 Entertainment Park — The stadium is the center of 'Hollywood Park,' a 298-acre area filled with shops, parks, and a giant lake!"],
 ["[⚽ CAREER] 👕 CR7 Legend — Cristiano Ronaldo is one of the greatest soccer players in history and is famous for his 'CR7' brand!",
  "[⚽ CAREER] 🎯 Goal King — Ronaldo has scored over 900 goals in his career, more than almost any other player who has ever lived!",
  "[⚽ CAREER] ⚡ International Star — He holds the world record for scoring the most goals for a national team, with over 120 goals for Portugal!",
  "[⚽ CAREER] 🔥 Global Journey — In his amazing career, he has played for giant teams like Manchester United, Real Madrid, Juventus, and Al Nassr!",
  "[🏆 ACHIEVEMENTS] 🏆 5x Ballon d'Or — Cristiano has been named the best player in the entire world five different times!",
  "[🏆 ACHIEVEMENTS] 🌟 Champions League — He has won the UEFA Champions League trophy 5 times, which is a record for the modern version of the tournament!",
  "[🏆 ACHIEVEMENTS] 🇵🇹 Euro Champion — In 2016, he led his home country of Portugal to victory in the European Championship for the first time!",
  "[🏆 ACHIEVEMENTS] 🥇 Trophy Collector — Throughout his career, he has won over 30 major trophies, including league titles in England, Spain, and Italy!",
  "[🎯 EXTRA] 🌎 Madeira Born — Ronaldo was born on the small island of Madeira in Portugal, and they even named the island's airport after him!",
  "[🎯 EXTRA] 🏋️ Super Athlete — He is famous for his incredibly strict diet and for working out in the gym for many hours every single day!",
  "[🎯 EXTRA] 🚫 No Tattoos — Unlike many players, Ronaldo has no tattoos because he regularly donates blood and wants to keep his blood healthy!",
  "[🎯 EXTRA] ⚽ Jump Power — Ronaldo can jump higher than a professional basketball player, allowing him to score amazing headers from way up in the air!"]),
("Levi's Stadium","The Silicon Giant","Santa Clara, CA (Bay Area)","stadium-09-bayarea-levis.png","number-09-bayarea-profile.png",
 "Bernardo Silva","Portugal","Midfielder","Manchester City",93,12,
 ["[🏙️ CITY] 🌉 Golden Gate — The San Francisco Bay Area is home to the world-famous Golden Gate Bridge, which is painted a color called 'International Orange!'",
  "[🏙️ CITY] 💻 Silicon Valley — This area is the high-tech center of the world, where famous companies like Google, Apple, and Facebook were started!",
  "[🏙️ CITY] 🚋 Cable Cars — San Francisco is the only city in the world with moving cable cars that people can ride up and down the steep hills!",
  "[🏙️ CITY] 🍪 Fortune Cookies — Even though people think they are from China, the modern fortune cookie was actually invented in San Francisco!",
  "[🏟️ STADIUM] 🏟️ Smart Stadium — At Levi's Stadium, fans can order food and watch replays right from their phone using a special stadium app!",
  "[🏟️ STADIUM] 🧑‍🌾 Rooftop Farm — The stadium has a 'Faithful Farm' on its roof where they grow real tomatoes, peppers, and herbs for the food served inside!",
  "[🏟️ STADIUM] ☀️ Solar Power — The parking lots are covered with 20,000 solar panels that help create enough clean energy to power the entire stadium!",
  "[🏟️ STADIUM] 🌿 Net-Zero Energy — On game days, the stadium creates as much energy as it uses, which is amazing for such a big building!",
  "[🌟 WOW] 🌁 Karl the Fog — San Francisco has a famous fog named 'Karl' that often rolls over the hills and has its own social media page!",
  "[🌟 WOW] 🌲 Alcatraz Island — In the middle of the bay sits the famous Alcatraz prison, which was once home to some of the world's most dangerous criminals!",
  "[🌟 WOW] 🥖 Sourdough Secret — San Francisco is famous for its sourdough bread, which has a unique taste because of the special bacteria only found there!",
  "[🌟 WOW] 🐻 Teddy Bears — The famous 'Teddy Bear' stuffed animal was actually named after President Teddy Roosevelt, who has a strong connection to the area!"],
 ["[⚽ CAREER] 👕 The Architect — Bernardo Silva is called the 'Architect' because he plans and builds attacks like a brilliant engineer!",
  "[⚽ CAREER] 🌟 Midfield Maestro — Bernardo plays as a midfielder, which means he controls the game and makes clever passes to his teammates!",
  "[⚽ CAREER] 🇵🇹 Portugal Pride — He has played over 90 times for Portugal and has been a key player in their most successful teams!",
  "[⚽ CAREER] 🏟️ Man City Star — Bernardo plays for Manchester City in England, one of the best teams in the world!",
  "[🏆 ACHIEVEMENTS] 🏆 4x Premier League — Bernardo has won the Premier League title four times with Manchester City, dominating English soccer!",
  "[🏆 ACHIEVEMENTS] 🌟 Champions League — In 2023, he helped Manchester City win the UEFA Champions League for the first time in their history!",
  "[🏆 ACHIEVEMENTS] 🇵🇹 Nations League — He helped Portugal win the Nations League in 2019, which is a major international tournament!",
  "[🏆 ACHIEVEMENTS] 🥇 Hat-Trick Hero — Bernardo scored a 'perfect hat-trick' (one goal with each foot and one with his head) in a Champions League game!",
  "[🎯 EXTRA] 🌎 Lisbon Born — Bernardo was born in Lisbon, the beautiful capital city of Portugal, and grew up playing soccer in the streets!",
  "[🎯 EXTRA] 🎵 Music Lover — When he's not playing soccer, Bernardo loves to play the guitar and listen to music from all around the world!",
  "[🎯 EXTRA] 🐾 Dog Dad — He has an adorable pet dog named 'Bolota' who has become famous on his social media pages!",
  "[🎯 EXTRA] 🧠 Clever Player — Bernardo is known for his incredible soccer IQ, always being one step ahead of his opponents on the field!"]),
("Lumen Field","The Roaring Giant","Seattle, WA","stadium-10-seattle-lumen.png","number-10-seattle-profile.png",
 "Virgil van Dijk","Netherlands","Defender","Liverpool",68,9,
 ["[🏙️ CITY] 🏔️ Emerald City — Seattle is called the 'Emerald City' because of the evergreen trees and beautiful green forests that surround it!",
  "[🏙️ CITY] ☕ Coffee Capital — The world-famous Starbucks coffee company opened its very first store in Seattle's historic Pike Place Market!",
  "[🏙️ CITY] 🐟 Flying Fish — At Pike Place Market, fish vendors throw giant fish through the air to each other, delighting visitors every day!",
  "[🏙️ CITY] 🌲 City of Hills — Seattle is built on seven different hills, similar to the famous city of Rome in Italy!",
  "[🏟️ STADIUM] 🏟️ Loudest Stadium — Lumen Field is known as the loudest stadium in the world, and has actually caused earthquakes from cheering!",
  "[🏟️ STADIUM] 🎤 Sound Focus — The stadium is shaped like a horseshoe, which focuses the crowd's roar onto the field, making it super intense!",
  "[🏟️ STADIUM] 🏈 Seahawks Home — The stadium is home to the Seattle Seahawks, whose '12th Man' fans are legendary for their noise and passion!",
  "[🏟️ STADIUM] ⚽ Soccer Ready — The grass field at Lumen Field is specially designed to handle the quick turns and action of FIFA soccer!",
  "[🌟 WOW] 🗼 Space Needle — Seattle's most famous landmark is the Space Needle, a 605-foot tall tower built for the 1962 World's Fair!",
  "[🌟 WOW] 🎸 Grunge Music — Seattle is the birthplace of 'grunge' music, which was made famous by bands like Nirvana and Pearl Jam!",
  "[🌟 WOW] ☔ Rain Reputation — Seattle is famous for its rain, but it actually gets less yearly rainfall than many other US cities like New York!",
  "[🌟 WOW] 🚢 Ferry Capital — Seattle has the largest ferry system in the United States, carrying millions of cars and people across the water!"],
 ["[⚽ CAREER] 👕 Defensive Wall — Virgil van Dijk is one of the best defenders in the world, known for being almost impossible to get past!",
  "[⚽ CAREER] 🇳🇱 Dutch Captain — Virgil is the captain of the Netherlands national team and leads from the back with his strength and calmness!",
  "[⚽ CAREER] 🛡️ Never Beaten — For an incredible 50 games in a row, nobody was able to dribble past Virgil — a record for a defender!",
  "[⚽ CAREER] 📏 Towering Height — Standing at 6'4\" (193 cm), Virgil uses his height to win almost every header and block crosses!",
  "[🏆 ACHIEVEMENTS] 🏆 UEFA Player of the Year — In 2019, Virgil was named the best player in Europe, the first defender to win this award!",
  "[🏆 ACHIEVEMENTS] 🌟 Champions League — He led Liverpool to victory in the 2019 Champions League final with his dominant defensive performance!",
  "[🏆 ACHIEVEMENTS] 🥈 Ballon d'Or 2nd — He finished second in the 2019 Ballon d'Or, the highest ever ranking for a defender!",
  "[🏆 ACHIEVEMENTS] 🏆 Premier League King — One year later, he helped Liverpool win the English Premier League for the first time in 30 years!",
  "[🎯 EXTRA] 🌎 Breda Born — Virgil was born in Breda, Netherlands, and started his career cleaning the boots of senior players!",
  "[🎯 EXTRA] 🍳 Breakfast Chef — He is famous for cooking special breakfasts for his teammates, making his own fresh omelettes!",
  "[🎯 EXTRA] 📚 Reading Habit — Virgil loves to read books about leadership and mental strength to help him become a better captain!",
  "[🎯 EXTRA] 🎶 Calm Composure — One of Virgil's secrets is staying calm even in the most chaotic moments of a big match!"]),
("Gillette Stadium","The Lighthouse Giant","Foxborough, MA (Boston)","stadium-11-boston-gillette.png","number-11-boston-profile.png",
 "Gianluigi Donnarumma","Italy","Goalkeeper","PSG",62,0,
 ["[🏙️ CITY] 🏛️ Historic Boston — Boston is one of the oldest cities in America and is where the American Revolution began!",
  "[🏙️ CITY] 🔦 Freedom Trail — You can follow the Freedom Trail, a 2.5 mile walk that takes you past 16 of the most important historic sites in America!",
  "[🏙️ CITY] 🦞 Lobster Love — Boston is world-famous for its delicious lobster rolls and creamy clam chowder soup!",
  "[🏙️ CITY] 📚 First School — Boston opened the first public school in America way back in 1635, which is still open and teaching kids today!",
  "[🏟️ STADIUM] 🏟️ Lighthouse Icon — Gillette Stadium has a real, working 22-story tall lighthouse that lights up the sky and can be seen from far away!",
  "[🏟️ STADIUM] 🏆 Super Bowl Central — This stadium has hosted an incredible six Super Bowls, including the epic 2022 championship game!",
  "[🏟️ STADIUM] 🛶 New England Charm — The stadium has a beautiful bridge modeled after the historic Longfellow Bridge in Boston!",
  "[🏟️ STADIUM] ⚽ Revolution Home — Besides American football, the stadium is also the home of the New England Revolution soccer team!",
  "[🌟 WOW] 🎓 Harvard University — Just a short drive away, you can visit Harvard, the oldest university in America, founded way back in 1636!",
  "[🌟 WOW] ⚾ Fenway Park — Boston is home to Fenway Park, the oldest baseball stadium in America, which opened in 1912!",
  "[🌟 WOW] ☕ Tea Party History — In 1773, angry colonists dumped 342 chests of tea into Boston Harbor to protest unfair taxes!",
  "[🌟 WOW] 🌊 Cheers — Boston is the city that inspired the famous 'Cheers' TV show, and you can still visit the bar where it was filmed!"],
 ["[⚽ CAREER] 👕 Giant in Goal — Gianluigi Donnarumma is a massive 6'5\" goalkeeper from Italy who fills up the entire goal with his reach!",
  "[⚽ CAREER] 🌟 Paris Star — Gigio (his nickname) plays for Paris Saint-Germain in France, one of the most famous clubs in the world!",
  "[⚽ CAREER] 🧤 Italian Legend — He has already played over 60 times for Italy and is on track to become their most-capped goalkeeper ever!",
  "[⚽ CAREER] 🎯 Goals? Not Him! — As a goalkeeper, Gigio's job is to stop goals, not score them, so his goal count stays at zero!",
  "[🏆 ACHIEVEMENTS] 🏆 Euro Hero — Gianluigi was named the Player of the Tournament when Italy won the 2020 European Championship!",
  "[🏆 ACHIEVEMENTS] 🌟 Penalty Stopper — In the Euro 2020 final, he saved two penalties in the shootout to help Italy win the trophy!",
  "[🏆 ACHIEVEMENTS] 🥇 Youngest Ever — When he started playing for AC Milan, he was the youngest goalkeeper to ever debut in the Italian league!",
  "[🏆 ACHIEVEMENTS] 🏆 Ligue 1 Winner — He has won multiple league titles in France and was named the league's best goalkeeper!",
  "[🎯 EXTRA] 🌎 Castellammare Born — Gigio was born in Castellammare di Stabia, a beautiful coastal town near Naples, Italy!",
  "[🎯 EXTRA] 👶 Teenage Debut — He made his professional debut for AC Milan when he was just 16 years old, shocking everyone with his skill!",
  "[🎯 EXTRA] 🧱 Wall Reflexes — Donnarumma is famous for his lightning-fast reflexes, making impossible saves that seem to defy gravity!",
  "[🎯 EXTRA] 🦅 Brother Goalie — Gigio's older brother Antonio is also a professional goalkeeper, so soccer runs in the family!"]),
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
# PAGES 3-24: 11 STADIUM SPREADS (2 pages each)
# ============================================================
ph2 = TRIM_H * 0.38
pw2 = TRIM_W / 2.0

city_photos = ["","city-01-newyork.png","city-02-philadelphia.png","city-03-washington-dc.png",
               "city-04-miami.png","city-05-atlanta.png","city-06-houston.png",
               "city-07-dallas.png","city-08-losangeles.png","city-09-sanfrancisco.png",
               "city-10-seattle.png","city-11-boston.png"]
club_logos = ["club-01-milan.png","club-02-madrid.png","club-03-bayern.png","club-04-intermiami.png",
              "club-05-realmadrid.png","club-06-galatasaray.png","club-07-tottenham.png",
              "club-08-alnassr.png","club-09-mancity.png","club-10-liverpool.png","club-11-psg.png"]

for idx, s in enumerate(S):
    name, nick, city, simg, pimg, pname, pcountry, ppos, pclub, pcaps, pgls, cfacts, pfacts = s

    # ============ STADIUM PAGE ============
    c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
    
    # Top: 2 photos
    place_photo(D+'/'+simg, BLEED, BLEED+TRIM_H-ph2, pw2, ph2)
    cimg = D+'/landmarks/'+city_photos[idx+1]
    if os.path.exists(cimg):
        place_photo(cimg, BLEED+pw2, BLEED+TRIM_H-ph2, pw2, ph2)
    else:
        place_photo(D+'/'+simg, BLEED+pw2, BLEED+TRIM_H-ph2, pw2, ph2)
    
    # Title area
    tx = BLEED + 15
    ty = PH - BLEED - ph2 - 35
    tw = TRIM_W - 30
    
    c.setFillColorRGB(0.95,0.96,1.0)
    c.roundRect(BLEED+8, BLEED+10, TRIM_W-16, TRIM_H-ph2-35, 10, fill=1, stroke=0)
    
    c.setFont("Helvetica-Bold", TTL)
    c.setFillColorRGB(0.05,0.05,0.3)
    c.drawString(tx, ty, f"#{idx+1}  {name}  •  {nick}")
    ty -= 28
    c.setFont("Helvetica-Bold", 13)
    c.setFillColorRGB(0.4,0.4,0.4)
    c.drawString(tx, ty, f"📍 {city}")
    ty -= 8
    
    c.setStrokeColorRGB(0.06,0.06,0.3)
    c.setLineWidth(1)
    c.line(tx, ty, tx+tw, ty)
    ty -= 14
    
    # 3 category sections: CITY, STADIUM, WOW
    cat_config = [
        ("🏙️  CITY SPOTLIGHT", cfacts[:4], (0.06,0.06,0.3)),
        ("🏟️  STADIUM FACTS", cfacts[4:8], (0.06,0.06,0.3)),
        ("🌟  WOW MOMENTS", cfacts[8:12], (0.06,0.06,0.3)),
    ]
    for title, facts, hcolor in cat_config:
        if ty < BLEED + 30: break
        ty = draw_category_section(tx, ty, tw, title, facts, hcolor)
    
    c.setFont("Helvetica-Bold", TNY)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawString(BLEED+15, BLEED+8, "WORLD CUP 2026 SOUVENIR GUIDEBOOK")
    c.drawRightString(PW-BLEED-15, BLEED+8, f"Page {idx*2+3}")
    c.showPage()
    
    # ============ PLAYER PAGE ============
    c.setFillColorRGB(1,1,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
    place_photo(D+'/'+pimg, BLEED, BLEED+TRIM_H-ph2, pw2, ph2)
    cld = '/home/team/shared/wc2026-club-illustrations'
    climg = cld+'/'+club_logos[idx]
    if os.path.exists(climg):
        place_photo(climg, BLEED+pw2, BLEED+TRIM_H-ph2, pw2, ph2)
    else:
        place_photo(D+'/'+simg, BLEED+pw2, BLEED+TRIM_H-ph2, pw2, ph2)
    
    c.setFillColorRGB(0.95,0.96,1.0)
    c.roundRect(BLEED+8, BLEED+10, TRIM_W-16, TRIM_H-ph2-35, 10, fill=1, stroke=0)
    
    ty = PH - BLEED - ph2 - 35
    
    c.setFont("Helvetica-Bold", TTL)
    c.setFillColorRGB(0.05,0.05,0.3)
    c.drawString(tx, ty, "⭐  Player Profile")
    ty -= 28
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0.05,0.05,0.3)
    c.drawString(tx, ty, f"{pname}  •  {pcountry}")
    ty -= 18
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0.4,0.4,0.4)
    c.drawString(tx, ty, f"{ppos}  •  {pclub}")
    ty -= 8
    
    c.setStrokeColorRGB(0.06,0.06,0.3)
    c.setLineWidth(1)
    c.line(tx, ty, tx+tw, ty)
    ty -= 14
    
    # 3 category sections: CAREER, ACHIEVEMENTS, EXTRA
    player_cats = [
        ("⚽  CAREER", pfacts[:4], (0.06,0.06,0.3)),
        ("🏆  ACHIEVEMENTS", pfacts[4:8], (0.06,0.06,0.3)),
        ("🎯  EXTRA", pfacts[8:12], (0.06,0.06,0.3)),
    ]
    for title, facts, hcolor in player_cats:
        if ty < BLEED + 30: break
        ty = draw_category_section(tx, ty, tw, title, facts, hcolor)
    
    c.setFont("Helvetica-Bold", TNY)
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
c.setFillColorRGB(0.98,0.98,1);c.rect(0,0,PW,PH,fill=1,stroke=0)
c.setFont("Helvetica-Bold", TTL)
c.setFillColorRGB(0.05,0.05,0.3)
c.drawCentredString(PW/2, PH-M-25, "World Cup 2026  •  By The Numbers")
ty = PH - M - 55
stats_data = [
    ("48 Nations","Most teams ever"), ("104 Matches","Record-breaking games"),
    ("16 Host Cities","USA, Mexico, Canada"), ("11 Stadium Giants","Unique personalities"),
    ("3 Countries","First tri-host World Cup"), ("5 Billion","Estimated TV viewers"),
    ("40,000 Tons","Steel in MetLife"), ("11,000+ Solar Panels","Power at The Linc"),
    ("160 ft Video Board","AT&T's giant screen"), ("8 Min Roof Open","Mercedes-Benz halo"),
    ("70,000+ Avg Capacity","Across all 11"), ("$5.5B Stadium","SoFi cost"),
]
cols=3; cw=(TRIM_W-40)/cols
for i,(sname,sval) in enumerate(stats_data):
    col=i%cols; row=i//cols
    x=BLEED+15+col*cw; y=ty-row*46
    c.setFont("Helvetica-Bold",14)
    c.setFillColorRGB(0.05,0.05,0.3)
    c.drawString(x,y,sname)
    c.setFont("Helvetica-Bold",10)
    c.setFillColorRGB(0.3,0.3,0.3)
    c.drawString(x,y-17,sval)

c.setFont("Helvetica-Bold", TNY)
c.setFillColorRGB(0.5,0.5,0.5)
c.drawString(BLEED+15, BLEED+8, "WORLD CUP 2026 SOUVENIR GUIDEBOOK")
c.drawRightString(PW-BLEED-15, BLEED+8, "Stats & Records")
c.showPage()

# ============================================================
# PAGE 27: BACK COVER
# ============================================================
place_full(D+'/back-cover.png')
c.showPage()

c.save()
sz=os.path.getsize(O)/(1024*1024)
print(f"✅ Guidebook saved: {O} ({sz:.1f} MB, 27 pages)")
print(f"   New: 2-column grid layout with category sections + card backgrounds")
print(f"   Stadiums: CITY | STADIUM | WOW  | Players: CAREER | ACHIEVEMENTS | EXTRA")