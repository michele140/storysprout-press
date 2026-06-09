#!/usr/bin/env python3
"""Build World Cup Book 2: Philly's Big Game."""
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

def go():
    print("WC #2: Philly's Big Game")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    D='/home/team/shared/wc2026-philly-illustrations';O='/home/team/shared/wc2-philly-kdp.pdf'
    texts={
        2:'In Philadelphia, sports aren\'t just games — they\'re part of the city\'s heart! Leo had been practicing her "Samba" kicks all week.\n\n"Uncle Joe, do you think Brazil will play the Philly way today?" Leo asked, spinning the ball on her finger.\n\n"The Philly way is with heart and hustle, Leo," Uncle Joe laughed. "And tonight, the Linc is going to roar!"',
        3:'To get to the game, they hopped on the Broad Street Line. The subway car was a sea of yellow, green, and Philly blue.\n\n"Go Brazil!" someone shouted.\n"Go Philly!" Leo shouted back, making everyone cheer.',
        4:'As they walked toward Lincoln Financial Field, the "Linc" stood tall. It looked like a modern fortress of steel and glass.\n\nBut the Linc wasn\'t just a building. He had "eyes" made of high-tech cameras and a heart that glowed with solar power.',
        5:'The Linc felt the energy of the crowd. He spread his giant metallic wings as if he were about to take flight!\n\n"Welcome to the City of Brotherly Love!" the stadium seemed to boom. In Philly, everyone is family when the game begins.',
        6:'Outside the gates, it was a giant party! Leo and Uncle Joe shared a famous Philly soft pretzel.\n\n"Look at all the flags, Uncle Joe!" Leo pointed to banners from countries all over the map.',
        7:'They found their seats high up in the stands. "Did you know the Linc is one of the \'greenest\' stadiums?" Uncle Joe pointed to the wind turbines and solar panels.',
        8:'The stadium grew quiet as the Brazilian national anthem began. The Linc giant stood at attention, his solar-powered heart glowing bright green.',
        9:'*WHISTLE!* The game was on! Brazil moved the ball with "Samba" style — dancing and spinning past the defenders.\n\n"Let\'s go, Brazil! Let\'s go, Philly!" Leo chanted. *Thump-thump-CLAP!*',
        10:'Suddenly, the ball was crossed high into the box. A Brazilian player leapt into the air — *BICYCLE KICK!*\n\nThe ball sailed toward the goal. The crowd gasped like a giant gust of wind.',
        11:'The match was tough, and the players were getting tired. "They need our help!" Leo said. She started the Wave. The Linc giant joined in, his goalposts swaying.',
        12:'At half-time, the score was still 0-0. "Philly has a long history of great teams," Uncle Joe said. "We never give up. We\'re like Rocky!"',
        13:'The second half brought a light Philly drizzle. The Linc giant didn\'t mind the rain. It washed his silver skin and made his heart glow even brighter.',
        14:'Finally, a break! A Brazilian player dribbled through three defenders and curled the ball into the net. *GOALLLL!*\n\nThe Linc shook with the sound of 70,000 people screaming for joy.',
        15:'But Italy wasn\'t finished. With only five minutes left, they scored a header. 1-1! The stadium went quiet, but then Leo stood up. "Don\'t stop now!"',
        16:'One of the players fell down, looking frustrated. He saw Leo waving her Philly scarf. He remembered the "Rocky" spirit and got back up.',
        17:'Brazil had one last free kick. The stadium was so quiet you could hear a pin drop. The Linc giant leaned in, listening to the heartbeat of the fans.',
        18:'The ball hit the bar with a loud *K-RANG!* and bounced away. The whistle blew. The game was over. A draw! Both teams had given everything.',
        19:'As they left, Leo met a young fan wearing an Italy jersey. In the World Cup, we are rivals for 90 minutes, but friends for life.',
        20:'You can\'t go to a Philly game without a post-match snack! Leo and Uncle Joe stopped for a legendary cheesesteak. The perfect end to a perfect day.',
        21:'The Linc giant watched the last of the fans head home. He tucked his wings in and prepared for a peaceful night\'s sleep.',
        22:'Back at home, Leo was exhausted but her mind was still racing. "I\'m going to play for Brazil one day," she whispered.',
        23:'In her dreams, Leo was the one on the pitch, hearing the crowd roar her name. The Linc would always be there, waiting for the next big game.',
        24:'Philly is ready for the World Cup! Are you?\n\n**Fun Fact:** Lincoln Financial Field has 11,000 solar panels and 14 wind turbines — producing enough clean energy to power every home match!',
    }
    c=canvas.Canvas(O,pagesize=(PG,PH))
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12);c.setFillColorRGB(0.1,0.4,0.7)
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
    c.setFillColorRGB(0.2,0.2,0.2);c.setFont("Helvetica-Bold",16)
    c.drawCentredString(PG/2,PH-85,"About the Story")
    c.setFont("Helvetica",11)
    blurb=("Join Leo and Uncle Joe for an unforgettable day at\n"
           "Lincoln Financial Field! From subway chants to a\n"
           "thrilling Brazil vs Italy match, this story celebrates\n"
           "Philly passion, sportsmanship, and the Linc's green energy.\n\nAges 5-9 | StorySprout Press")
    lines=blurb.split('\n');y=PH-115
    for line in lines:
        c.drawCentredString(PG/2,y,line);y-=16
    c.setFont("Helvetica",9);c.setFillColorRGB(0.5,0.5,0.5)
    c.drawCentredString(PG/2,55,"StorySprout Press")
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")
    lis=r"""# World Cup Book #2: "Philly's Big Game" - Product Listing

## Amazon KDP Product Details
**Title:** Philly's Big Game: A World Cup Soccer Story for Kids - Join Leo at Lincoln Financial Field!
**Series:** World Cup Adventures (Book 2)
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 5-9**
**Price (Print):** $9.99 | **Price (Digital):** $4.99

### Amazon Bullet Points
1. **WORLD CUP SOCCER ADVENTURE** - Join 8-year-old Leo in Philadelphia for an unforgettable Brazil vs Italy match at Lincoln Financial Field!
2. **AGES 5-9 FORMAT** - Longer, richer text with soccer action, Philly culture, and green energy fun facts.
3. **THE LINC COMES TO LIFE** - Lincoln Financial Field is a winged steel giant with a solar-powered green heart.
4. **TEACHES SPORTSMANSHIP** - Leo trades stickers with an Italy fan, showing rivals can be friends.
5. **PHILLY CULTURE** - Soft pretzels, cheesesteaks, the "Rocky" spirit, and the legendary Philly sports passion!
6. **BEAUTIFUL ILLUSTRATIONS** - 26 vibrant illustrations of the stadium, the match, and the city of Philadelphia.
7. **GREEN ENERGY FUN FACT** - Did you know the Linc has 11,000 solar panels? Clean energy meets soccer!

### Amazon Backend Keywords
children's soccer book, world cup kids book, philly soccer story, lincoln financial field book, phillies stadium, brazil vs italy, philadelphia kids book, sportsmanship children's, world cup 2026, stadium adventure, uncle and niece, samba soccer, green stadium, philly sports fan, soccer story ages 5-9

### Etsy Listing
**Title:** Philly's Big Game - Printable Children's Soccer Storybook PDF | World Cup Philadelphia | Lincoln Financial Field Digital Download
**Tags:** childrens storybook, printable book for kids, soccer book, world cup philly, philadelphia kids, stadium adventure, sports book, digital download, ages 5-9, soccer story, lincoln financial field, linc stadium
**Description:** Join Leo and Uncle Joe for an unforgettable day at Lincoln Financial Field! Brazil vs Italy, the Linc's solar-powered heart, and the Philly spirit make this a story to remember. 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-wc2-storybook.md','w') as f:f.write(lis)
    print("  -> /home/team/shared/listings-wc2-storybook.md")
    print("WC BOOK #2 COMPLETE!")
if __name__=='__main__':go()