#!/usr/bin/env python3
"""Build WC Books 10 (Seattle) and 11 (Boston)."""
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

def make(num,title,D,O,t,color):
    print(f"WC #{num}: {title}")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    c=canvas.Canvas(O,pagesize=(PG,PH))
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12);c.setFillColorRGB(*color)
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

# WC #10: Seattle
sea={
2:'In Seattle, the coffee is strong, the rain is gentle, and the fans are the loudest in the world! Sam had been practicing his "Seattle roar" all week.\n\n"Dad, do you think the Netherlands will hear us from across the ocean?" Sam asked.\n\n"With your voice, they might!" Dad laughed.',
3:'They took the ferry across the sparkling bay. The Seattle skyline gleamed against the mountains. The Space Needle looked like a giant soccer trophy.',
4:'Lumen Field rose ahead — the "Roaring Giant." A stadium built of green and blue glass with two soaring white arches that looked like eyebrows raised in excitement.',
5:'The Roaring Giant\'s voice echoed across the city. "Welcome to the Emerald City!" he seemed to say. Sam felt the sound in his chest.',
6:'Inside, the stadium was famous for its "12th Man" energy — the fans themselves! Every seat was a voice waiting to cheer.',
7:'"Did you know this is one of the loudest stadiums in the world?" Dad said. Sam looked at the towering walls. "Let\'s make it even louder!"',
8:'The pre-game show was a Cascadian celebration! Native drummers, folk dancers, and a giant flag featuring a soccer ball and evergreen trees.',
9:'Team Netherlands walked out in bright orange. The "Oranje" looked confident and skilled. Sam waved his orange scarf high.',
10:'*WHISTLE!* Netherlands vs South Korea! The Dutch moved the ball with artistic flair. South Korea countered with lightning speed.',
11:'Netherlands scored first! A beautiful volley from a cross. *GOAL!* 1-0. The stadium roared so loud it shook!',
12:'Between periods, Sam had some Seattle-style hot chocolate with local honey. "The best in the world!"',
13:'South Korea answered with a stunning goal. A long-range shot that curled into the top corner. 1-1!',
14:'The fans didn\'t stop cheering. The Roaring Giant\'s glass panels vibrated with the sound of 70,000 voices.',
15:'The final minutes were intense. Both teams pushed for the win. The cheering was a wall of sound.',
16:'Netherlands scored the winner! A header from a corner. 2-1! The stadium exploded with joy!',
17:'*TWEET! TWEET! TWEET!* Netherlands won. The players celebrated together. Sam hugged Dad.',
18:'As they left, Sam was hoarse from cheering. "My voice is gone, but my heart is so full!"',
19:'The Roaring Giant settled into the night. His green glass shimmered in the moonlight.',
20:'The World Cup is coming to Seattle! Are you ready to roar?',
21:'Seattle is a city of nature, coffee, and the loudest fans in America!',
22:'**Fun Fact:** Lumen Field is famous for its "12th Man" — the fans are so loud they\'ve caused small earthquakes!',
}
make(10,"Seattle's Roar","/home/team/shared/wc2026-seattle-illustrations","/home/team/shared/wc10-seattle-kdp.pdf",sea,(0.2,0.5,0.3))

# WC #11: Boston
bos={
2:'In Boston, history is everywhere. Nora knew every story about the American Revolution. But today, she was here to make history — the World Cup at Gillette Stadium!\n\n"Grandma, did they have soccer in 1776?" Nora asked.\n\n"They had heart, Nora. Just like you!" Grandma Elin smiled.',
3:'They drove past the USS Constitution and Paul Revere\'s statue. "Today, we\'re fighting for a goal!" Nora said.',
4:'Gillette Stadium\'s "Lighthouse Giant" stood proud. He had a body of red brick and silver steel, and a towering lighthouse head that shone a guiding light.',
5:'The Lighthouse Giant\'s beam swept across the crowd. "Welcome to the Revolution!" he seemed to say. "Today, we fight for victory!"',
6:'The stadium was decked in blue and white. Italy\'s fans were passionate. The other team\'s fans were just as loud.',
7:'"This stadium was built on the spirit of champions," Grandma said. Nora felt the weight of history on her shoulders.',
8:'The pre-game show featured the Boston Pops playing an orchestral version of a soccer anthem. Nora got goosebumps.',
9:'Team Italy — the "Azzurri" — walked out in classic blue. They looked like warriors. Nora waved her Italian flag.',
10:'*WHISTLE!* Italy vs Belgium! Italy passed with precision. Belgium was powerful and fast.',
11:'Italy scored! A beautiful team goal. Passing, moving, *KICK!* The ball hit the net. *GOAL!* 1-0!',
12:'Between periods, Nora had a famous New England clam chowder. "Fuel for champions!" Grandma said.',
13:'Belgium fought back. A powerful shot from outside the box. 1-1. The game was wide open.',
14:'The Lighthouse Giant\'s beam swept across the field, lighting up the action. The crowd was electric.',
15:'Italy took the lead again! A header from a corner kick. 2-1! The Azzurri fans sang loudly.',
16:'The final whistle blew! Italy won 2-1. Nora jumped for joy. "That was revolutionary!" she shouted.',
17:'As they left, Nora looked at the lighthouse beam one last time. "Today, I saw history being made."',
18:'The Lighthouse Giant dimmed his light. Another day of glory at Gillette Stadium.',
19:'The World Cup is coming to Boston! Are you ready for the revolution?',
20:'Boston is a city of bravery, history, and champions. 2026 will be a historic year!',
21:'**Fun Fact:** Gillette Stadium is home to the New England Revolution and has hosted some of the biggest soccer matches in US history!',
}
make(11,"Boston's Victory","/home/team/shared/wc2026-boston-illustrations","/home/team/shared/wc11-boston-kdp.pdf",bos,(0.3,0.2,0.5))

print("\n=== WC BOOKS 10 & 11 COMPLETE! WC SERIES FINALE! 🎉 ===")