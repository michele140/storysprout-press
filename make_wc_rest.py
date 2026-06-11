#!/usr/bin/env python3
"""Build all remaining World Cup books (DC, Atlanta, Houston)."""
import os, textwrap, sys
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

TMP='/home/team/shared/.tmp_build';os.makedirs(TMP,exist_ok=True)
def plc(c,p,w,h):
    if not p or not os.path.exists(p):
        c.setFillColorRGB(1,1,1);c.rect(0,0,w,h,fill=1,stroke=0);return
    i=Image.open(p).convert('RGB');i=i.resize((int(w),int(h)),Image.LANCZOS)
    t=os.path.join(TMP,os.path.basename(p).replace('.png','.jpg'));i.save(t,'JPEG',quality=95);c.drawImage(t,0,0,w,h)

def build_book(num, title, img_dir, output, texts, front_color=(0.2,0.2,0.2), blurb=""):
    print(f"WC #{num}: {title}")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    D=img_dir;O=output
    c=canvas.Canvas(O,pagesize=(PG,PH))
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12);c.setFillColorRGB(*front_color)
    c.drawCentredString(PG/2,PH-185,"A StorySprout Press Book");c.showPage()
    for pn in range(1,25):
        plc(c,D+f'/page-{pn:02d}.png',PG,PH)
        if pn in texts:
            t=texts[pn];x0=B+M;y0=B+12;tw=T-2*M
            paras=t.split('\n\n');fs=13;lh=17
            nl=sum(max(1,len(textwrap.wrap(p,width=50))) for p in paras)
            th=max(90,min(200,nl*lh+20))
            c.setFillColorRGB(1,1,1,alpha=0.75)
            c.roundRect(x0,y0,tw,th,8,fill=1,stroke=0)
            c.setFillColorRGB(0.1,0.1,0.15);c.setFont("Helvetica",fs)
            cy=y0+th-lh-5
            for para in paras:
                for line in textwrap.wrap(para,width=50):
                    c.drawCentredString(B+T/2,cy,line);cy-=lh
                cy-=4
        if pn>1:
            c.setFont("Helvetica",9);c.setFillColorRGB(0.5,0.5,0.5)
            c.drawCentredString(B+T/2,B+5,str(pn))
        c.showPage()
    plc(c,D+'/back-cover.png',PG,PH)
    if blurb:
        lines=blurb.split('\n');y=PH-115
        c.setFillColorRGB(0.2,0.2,0.2);c.setFont("Helvetica-Bold",16)
        c.drawCentredString(PG/2,PH-85,"About the Story")
        c.setFillColorRGB(0.2,0.2,0.2);c.setFont("Helvetica",11)
        for line in lines:
            c.drawCentredString(PG/2,y,line);y-=16
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")

# =========== WC #3: DC (FedEx Field) ===========
dc_texts={
    2:'Maya loved two things: history and soccer. She knew every fact about Washington DC, from the Washington Monument to the Smithsonian museums.\n\nBut today, she was going to see history being made — the World Cup at FedEx Field!',
    3:'"Look, Mom! The Washington Monument looks like a giant goalpost!" Maya pointed as they drove past the landmarks.\n\n"Everything looks like a goalpost to you," Mom laughed.',
    4:'FedEx Field loomed ahead, huge and blue. The stadium character, the FedEx Giant, wore a cape made of a giant American flag. He had a heart of gold that glowed with every cheer.',
    5:'The FedEx Giant was known for his powerful voice. "Welcome to DC!" he seemed to boom. "Today, we welcome the world!"\n\nMaya felt a shiver of excitement. The World Cup was here!',
    6:'Inside, the stadium was decorated with flags from every nation. Fans from England wore white and red, while US fans wore red, white, and blue. Everyone was smiling.',
    7:'"This stadium has seen so much history," Mom said. "And now it\'s making more!" Maya nodded, taking it all in.',
    8:'Team England walked out in their classic white kits. The "Three Lions" looked strong and proud. The crowd roared as the players lined up for the anthem.',
    9:'*TWEET!* The game began! England moved the ball with precision passing. The US team countered with speed. It was a chess match on grass.',
    10:'A US player broke free down the wing and crossed the ball. *BANG!* A header toward goal! The English goalkeeper made a spectacular save.',
    11:'England responded with a beautiful passing sequence. Their star striker received the ball, turned, and shot. *GOAL!* 1-0 England!',
    12:'Between periods, Maya ate a hot dog and looked at the DC monuments visible from the upper deck. "This is the best field trip ever," she said.',
    13:'The next period began with intensity. The US team pressed forward. The FedEx Giant\'s heart glowed brighter with every attack.',
    14:'USA scored! A long-range shot that curled into the top corner. 1-1! The stadium erupted. Maya hugged Mom, jumping up and down.',
    15:'The final minutes were tense. Both teams wanted the win. England pushed forward. USA defended with everything they had.',
    16:'England took a final shot. *CLANG!* It hit the post and bounced away! The whistle blew. 1-1! A draw between two great teams!',
    17:'After the match, players exchanged jerseys. Maya saw an English player give his shirt to a young US fan. That was the spirit of the World Cup.',
    18:'As they left, Maya looked back at the stadium. "Thank you, FedEx Giant, for an amazing day!"',
    19:'The FedEx Giant\'s heart pulsed warmly. He loved hosting the world. Washington DC was ready for the world!',
    20:'On the way home, Maya looked at the lit-up monuments. "One day, I\'ll play here," she said. "I know you will," Mom replied.',
    21:'Maya dreamed of scoring the winning goal for the US in a World Cup final at FedEx Field. The crowd roaring her name.',
    22:'The FedEx Giant settled down for the night. His flag cape fluttered gently in the breeze.',
    23:'Washington DC had welcomed the world. And the world had a wonderful time.\n\nAre you ready for the World Cup?',
    24:'**Fun Fact:** FedEx Field is located just outside Washington DC in Landover, Maryland. It\'s one of the largest stadiums in the NFL and has hosted countless historic moments!',
}
build_book(3,"DC's World Cup Welcome","/home/team/shared/wc2026-fedex-illustrations","/home/team/shared/wc3-dc-kdp.pdf",dc_texts,(0.2,0.2,0.7),
    "Join Maya in Washington DC as she watches the World Cup\nat FedEx Field! England vs USA, landmarks, and the\nFedEx Giant with his flag cape make this a day of\nhistory and soccer.\n\nAges 5-9 | StorySprout Press")

# =========== WC #5: Atlanta ===========
atl_texts={
    2:'Atlanta was buzzing! Sofia had been waiting for this day her whole life — the World Cup at Mercedes-Benz Stadium!\n\n"Come on, Dad! We\'re going to be late!" Sofia tugged her father\'s hand.',
    3:'The stadium looked like a giant silver spaceship had landed in the middle of Atlanta. The Mercedes-Benz Giant had a shiny metal body and a halo-roof that glowed with rainbow lights.',
    4:'"Welcome to Atlanta!" the giant seemed to say. His roof — the "Oculus" — opened like a giant flower blooming. Sofia looked up in wonder.',
    5:'Inside, the stadium was massive. A giant video board shaped like a ring hung from the ceiling. "That\'s the largest video board in the world!" Dad said.',
    6:'Fans from Brazil and Germany filled the stands. Samba drums competed with German chants. The energy was electric.\n\n"This is bigger than I imagined!" Sofia whispered.',
    7:'*TWEET!* Brazil vs Germany! Two of the greatest soccer nations faced off. Brazil\'s yellow jerseys moved like sunshine on the green grass.',
    8:'Germany struck first. A powerful shot from outside the box. *GOAL!* 1-0 Germany. The German fans sang loudly.',
    9:'Brazil responded with beautiful samba soccer. Quick passes, dazzling dribbles. The Mercedes-Benz Giant\'s halo glowed yellow and green.',
    10:'Brazil scored! A beautiful team goal. 1-1. Sofia jumped and cheered. This was World Cup soccer at its finest!',
    11:'Between periods, Sofia explored the stadium. "Did you know this roof can open or close in just 8 minutes?" Dad pointed to the giant Oculus.',
    12:'The next period was intense. Germany controlled possession. Brazil looked dangerous on the counter. Both teams wanted the win.',
    13:'Germany scored again. A header from a corner. 2-1. The German fans went wild. Sofia felt a little sad but kept cheering.',
    14:'Brazil pushed forward. They earned a penalty! The crowd held its breath. The Brazilian star stepped up... and scored! 2-2!',
    15:'The match ended 2-2. A thrilling draw! Players shook hands. Sofia waved her Brazilian flag one last time.',
    16:'"That was the most amazing thing I\'ve ever seen," Sofia said. "Me too," Dad smiled.',
    17:'The Mercedes-Benz Giant\'s halo glowed with all the colors of the rainbow. A perfect end to a perfect match.',
    18:'Atlanta had shown its Southern hospitality. The world was welcome here.',
    19:'Sofia fell asleep in the car, dreaming of playing on that field someday.',
    20:'The stadium settled into the night. The giant\'s lights dimmed gently.',
    21:'Are you ready for the World Cup in Atlanta?\n\nThe South is ready to welcome you!',
    22:'**Fun Fact:** Mercedes-Benz Stadium has the world\'s largest video board — a 360-degree ring called the "Halo Board" that weighs as much as 18 elephants!',
}
# Fill missing page texts  
atl_texts[23]='Atlanta\'s Mercedes-Benz Stadium is a marvel of modern engineering.'; atl_texts[24]='The "Oculus" roof opens in 8 minutes — the fastest in the world!'
build_book(5,"Atlanta's Amazing Stadium","/home/team/shared/wc2026-atlanta-illustrations","/home/team/shared/wc5-atlanta-kdp.pdf",atl_texts,(0.5,0.1,0.3),
    "Join Sofia in Atlanta for Brazil vs Germany at\nMercedes-Benz Stadium! The Halo Board, the Oculus\nroof, and samba drums make this World Cup match\nunforgettable.\n\nAges 5-9 | StorySprout Press")

# =========== WC #6: Houston ===========
hou_texts={
    2:'Houston was ready for liftoff! Carlos had his Argentina jersey on and his lucky space socks.\n\n"Today, we\'re going to see the stars play!" his dad said. Houston\'s NRG Stadium was hosting the World Cup!',
    3:'NRG Stadium had a giant retractable roof and walls that could change color. The NRG Giant wore a space helmet and had rocket boosters on his sides.',
    4:'"Welcome to Space City!" the giant seemed to say. His rocket boosters glowed blue as the doors opened.',
    5:'Inside, fans from Argentina and Nigeria filled the stands. Blue and white stripes mixed with green and white. The energy was cosmic!',
    6:'"Houston is the most diverse city in America," Dad said. "Today, the whole world is here!"',
    7:'*TWEET!* Argentina vs Nigeria! The Albiceleste moved the ball with precision. Nigeria countered with speed and power.',
    8:'Argentina scored first. A beautiful passing move ending with a shot into the corner. 1-0! Carlos hugged Dad.',
    9:'Nigeria fought back. Their star player dribbled past three defenders and scored. 1-1! The Nigerian fans celebrated.',
    10:'The match was back and forth. End-to-end action. The NRG Giant\'s rocket boosters pulsed with every attack.',
    11:'Between periods, Carlos ate a famous Texas BBQ sandwich. "This is the best food ever!"',
    12:'The next period started fast. Argentina pressed forward. Nigeria defended bravely. Both teams wanted the win.',
    13:'Argentina scored again. A powerful header from a corner. 2-1! The Argentina fans went wild.',
    14:'Nigeria didn\'t give up. They pushed forward and earned a corner. The cross came in... headed just wide!',
    15:'The final whistle blew. Argentina won 2-1! Carlos jumped for joy.',
    16:'After the match, the Nigerian players hugged the Argentina players. Respect and friendship.',
    17:'"That was out of this world!" Carlos said. "Literally!" Dad laughed, pointing at the space-themed stadium.',
    18:'As they left, the NRG Giant\'s rocket boosters glowed one last time.',
    19:'Houston had shown its big heart and even bigger spirit.',
    20:'Carlos fell asleep dreaming of playing under the stars.',
    21:'Are you ready for the World Cup in Houston?\n\nSpace City is ready for liftoff!',
    22:'**Fun Fact:** NRG Stadium has a retractable roof that opens to the Houston sky. It\'s also home to the Houston Texans and the Houston Livestock Show and Rodeo!',
}
hou_texts[23]='Houston\'s NRG Stadium can seat over 72,000 fans for the World Cup!'; hou_texts[24]='The stadium\'s nickname is "The H" — short for Houston!'
build_book(6,"Houston's Big Heart","/home/team/shared/wc2026-houston-illustrations","/home/team/shared/wc6-houston-kdp.pdf",hou_texts,(0.2,0.4,0.8),
    "Join Carlos in Houston for Argentina vs Nigeria at\nNRG Stadium! Space-themed stadium, Texas BBQ, and\nthe diversity of Houston make this match a celebration.\n\nAges 5-9 | StorySprout Press")

print("\n=== ALL REMAINING WC BOOKS COMPLETE! ===")