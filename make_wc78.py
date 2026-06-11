#!/usr/bin/env python3
"""Build WC Books 7 (Dallas) and 8 (LA)."""
import os, textwrap
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

TMP='/home/team/shared/.tmp_build';os.makedirs(TMP,exist_ok=True)
def plc(c,p,w,h):
    if not p or not os.path.exists(p):
        c.setFillColorRGB(1,1,1);c.rect(0,0,w,h,fill=1,stroke=0);return
    i=Image.open(p).convert('RGB');i=i.resize((int(w),int(h)),Image.LANCZOS)
    t=os.path.join(TMP,os.path.basename(p).replace('.png','.jpg'));i.save(t,'JPEG',quality=95);c.drawImage(t,0,0,w,h)

def make(num,title,D,O,texts,color,blurb):
    print(f"WC #{num}: {title}")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    c=canvas.Canvas(O,pagesize=(PG,PH))
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12);c.setFillColorRGB(*color)
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
        c.setFont("Helvetica",11)
        for line in lines:
            c.drawCentredString(PG/2,y,line);y-=16
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")

# WC #7: Dallas - Texas-Sized Soccer
dallas={
2:'In Texas, we like things big! Big hats, big sky, and especially big stadiums. Emma was ready for the biggest day of her life.\n\n"Grandpa, will the stadium really be bigger than our whole neighborhood?" Emma asked.\n\n"Even bigger, Emma!" Grandpa Jim chuckled. "Titan Tex is waiting for us!"',
3:'They drove toward Arlington, the truck bed filled with chairs and a cooler for tailgating. As they got closer, the sun reflected off the stadium\'s massive glass walls. It looked like a giant silver jewel.',
4:'"Titan Tex" stood in all his glory. He had a curved roof like a silver shield and a giant eye that could see everything on the field. Emma felt tiny next to his massive silver feet.',
5:'Titan Tex beamed a welcome from his giant eye. "HOWDY WORLD!" it flashed. "Howdy, Tex!" Emma shouted, waving her cowboy hat high in the air.',
6:'The tailgating was legendary! The smell of smoky Texas brisket filled the air. Emma played cornhole with fans from Germany.',
7:'Walking inside was like entering a giant\'s living room! "Did you know that screen is over 160 feet wide?" Grandpa Jim whispered.',
8:'The pre-game show was a display of Texas precision! The giant end-zone doors were open, letting in a warm Texas breeze.',
9:'Then came Team Germany! They moved with the precision of a fine watch. Titan Tex focused his giant eye on the center circle.',
10:'*WHISTLE!* Germany vs South Korea! Germany controlled the ball like they were following a master plan. South Korea was fast and energetic.',
11:'Suddenly, Germany attacked! A cross came in, and a player leapt high — *THWACK!* — he headed the ball into the corner. *TOR!*\n\nTitan Tex\'s giant eye showed the replay over and over!',
12:'Between periods, Emma had some "Texas-sized" nachos. They were huge! "Soccer is great, but Texas food is even better!"',
13:'The next period was a whirlwind! South Korea pushed hard. They moved the ball with incredible speed, testing the German defense.',
14:'South Korea broke through! A fast counter-attack and — *SWISH!* — the ball was in the net. 1-1! The stadium erupted!',
15:'The final minutes were intense. Germany had a free kick just outside the box. The stadium was so quiet you could hear the wind.',
16:'The ball took flight! It curled over the wall of players. *SWISH!* Germany had scored again! 2-1!',
17:'*TWEET! TWEET! TWEET!* Germany won. Emma watched as the players shook hands. "That was a Texas-sized effort by everyone," Grandpa Jim said.',
18:'As they walked out, Emma met a boy named Hans from Munich. "Hope you liked Texas, Hans!" she said, giving him a high-five.',
19:'The drive home was peaceful. The big Texas moon hung over the stadium. "I\'m going to be a goalie one day, Grandpa."',
20:'Back at home, Emma looked at the stars. She fell asleep dreaming of the World Cup Final in her hometown.',
21:'The fans went home, and Titan Tex rested his massive silver frame. Ready for the next big match.',
22:'The World Cup is coming to Arlington! Are you ready for some Texas-sized fun?',
23:'Texas is a land of legends and hospitality. 2026 will be the biggest year yet!',
24:'**Fun Fact:** AT&T Stadium\'s video board weighs as much as 30 elephants! It also has the world\'s largest retractable glass doors.',
}
make(7,"Texas-Sized Soccer","/home/team/shared/wc2026-dallas-illustrations","/home/team/shared/wc7-dallas-kdp.pdf",dallas,(0.1,0.3,0.6),
    "Join Emma and Grandpa Jim in Arlington for Germany vs\nSouth Korea at AT&T Stadium! Titan Tex's giant eye,\nTexas-sized nachos, and the biggest video board in the\nworld make this a Texas-sized adventure.\n\nAges 5-9 | StorySprout Press")

# WC #8: LA Dreams Big
lax={
2:'In Los Angeles, everyone has a dream! Chloe\'s dream was to be the first director to film a World Cup winning goal.\n\n"Chloe, the lighting is perfect! It\'s time to go!" Dad called.',
3:'They drove through sunny streets, passing palm trees that looked like giant fans. SoFi Stadium appeared like a giant, shimmering silver wave.',
4:'"The Infinity Giant" was the most glamorous stadium Chloe had ever seen! His skin was translucent, letting the LA sun shine through him.',
5:'The Infinity Giant gave a shimmering wink. His glass panels caught the light and turned it into a thousand mini-rainbows.',
6:'The Fan Zone was like a red carpet event! The air smelled like sea salt and fancy snacks. In LA, even soccer feels like a world premiere!',
7:'Walking inside was like magic! The stadium had no walls, only a giant roof. "Did you know this screen is 120 yards long?" Dad said.',
8:'The pre-game show was a masterpiece! Taiko drummers made the ground shake. A golden dragon circled on the Infinity Screen.',
9:'Then came the "Samurai Blue" — Team Japan! They looked focused and ready for their close-up.',
10:'*WHISTLE!* Japan vs Portugal! Japan moved the ball with incredible grace. Portugal was fast and flashy in their red jerseys.',
11:'A Japanese player made a "no-look" pass — *ZIP!* The Infinity Screen showed a close-up of the skill. The crowd gasped!',
12:'Between periods, Chloe visited the "Director\'s Booth." She got to edit her own soccer highlight reel!',
13:'The "Golden Hour" arrived. The light was perfect for a hero\'s journey! The Infinity Giant made his roof glow like a white pearl.',
14:'Suddenly, Japan broke through! *Pass, pass, pass, KICK!* *GOALLLLLL!* The Infinity Screen erupted in digital fireworks!',
15:'Portugal attacked with the speed of a Hollywood car chase! The Japanese defenders blocked every shot.',
16:'Even though the game was intense, players showed sportsmanship. After a tough play, rivals helped each other up.',
17:'*TWEET! TWEET! TWEET!* Japan won 1-0! Chloe danced with the fans in a happy finale. The Infinity Giant blinked farewell.',
18:'As they left, Chloe looked back. "Today was a blockbuster, Dad! I\'m going to make a movie about this stadium."',
19:'Back at home, Chloe was already "editing" her memories. She dreamed of a world where everyone was a star.',
20:'The cameras were off. The Infinity Giant settled into the Inglewood earth. Ready for more big stories in 2026.',
21:'In her dreams, soccer was art and the field was a stage. Chloe was the director of the world.',
22:'The World Cup is coming to Los Angeles! Are you ready for your close-up?',
23:'Los Angeles is a city of creativity and inclusion. 2026 will be a world premiere like no other!',
24:'**Fun Fact:** SoFi Stadium is the most expensive stadium ever built! Its Infinity Screen is the only double-sided video board in the world!',
}
make(8,"LA Dreams Big","/home/team/shared/wc2026-lax-illustrations","/home/team/shared/wc8-lax-kdp.pdf",lax,(0.6,0.1,0.4),
    "Join Chloe and Dad in LA for Japan vs Portugal at\nSoFi Stadium! The Infinity Giant, taiko drummers, and\nHollywood glamour make this World Cup match a\nblockbuster event.\n\nAges 5-9 | StorySprout Press")

print("\n=== WC BOOKS 7 & 8 COMPLETE! ===")