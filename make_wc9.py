#!/usr/bin/env python3
"""Build WC Book 9: Bay Area Blast."""
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
    print("WC #9: Bay Area Blast")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    D='/home/team/shared/wc2026-bayarea-illustrations';O='/home/team/shared/wc9-bayarea-kdp.pdf'
    t={
2:'In the SF Bay Area, we connect everything! Kai was checking real-time data for today\'s World Cup match.\n\n"Mom, the stadium is already at 80% power from its solar panels!" Kai said.\n\n"Ready to see Portugal play at Levi\'s Stadium?" Mom laughed.',
3:'They hopped on the train, zooming past tech company headquarters. "Look at the Golden Gate Bridge, Kai!" Mom pointed. The train was full of fans from all over the world.',
4:'"The Silicon Giant" stood tall — the smartest stadium in the world! He had a head made of video screens and a "hat" of real green grass on his roof.',
5:'The Silicon Giant gave a digital pulse of welcome. A "Welcome" notification appeared on Kai\'s phone!',
6:'Inside, Kai tried salsa made from tomatoes grown on the stadium\'s roof. "It tastes like sunshine!" he said.',
7:'Walking into the bowl was like entering a giant\'s playground. "Did you know this is the first net-zero energy stadium?" Mom said.',
8:'The pre-game show was a drone spectacular! Hundreds of tiny lights formed a glowing soccer ball in the sky.',
9:'Team Portugal walked out looking powerful and confident. The Silicon Giant blinked red and green in rhythm with the chants.',
10:'*WHISTLE!* Portugal moved the ball with the speed of fiber-optic cable! Their passes were like lines of code building a perfect play.',
11:'A Portuguese star did lightning step-overs. The stadium Giant showed the move in super-slow motion on his giant screens.',
12:'Between periods, Kai learned how the stadium saves water. "Even a giant needs to take care of the earth," Kai said.',
13:'"Karl the Fog" drifted over the walls. The Silicon Giant used anti-glare lights so everyone could see through the mist.',
14:'Portugal had a free kick! *BEND!* The ball curled around the wall. *GOAL.EXE COMPLETED!* Digital fireworks exploded!',
15:'The other team launched a counter-attack as fast as a viral video. The Portuguese defense worked like a well-synced team.',
16:'After a tough tackle, two players shared a laugh and a handshake. The Silicon Giant showed a giant "Heart" emoji.',
17:'*TWEET! TWEET! TWEET!* Portugal won 1-0! The Silicon Giant gave a multi-colored light show farewell.',
18:'"Today was a total upload of fun! I want to code the apps for the next World Cup!" Kai said.',
19:'Back at home, Kai shared his photos. He felt connected to millions of fans who had watched the same game.',
20:'The data was saved. The Silicon Giant rested his processors. Ready for more blasts of fun in 2026.',
21:'In his dreams, soccer was logic and magic combined. Kai was the architect of the win.',
22:'The World Cup is coming to the Bay Area! Are you ready to connect?',
23:'The Bay Area is a place of innovation and natural beauty. 2026 will be a year of incredible connections!',
24:'**Fun Fact:** Levi\'s Stadium has a 27,000 sq ft Green Roof! It also powers every home game with solar panels.',
    }
    c=canvas.Canvas(O,pagesize=(PG,PH))
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12);c.setFillColorRGB(0.2,0.6,0.3)
    c.drawCentredString(PG/2,PH-185,"A StorySprout Press Book");c.showPage()
    for pn in range(1,25):
        plc(c,D+f'/page-{pn:02d}.png',PG,PH)
        if pn in t:
            tx=t[pn];x0=B+M;y0=B+12;tw=T-2*M
            paras=tx.split('\n\n');fs=13;lh=17
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
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")
    print("WC BOOK #9 COMPLETE!")
if __name__=='__main__':go()