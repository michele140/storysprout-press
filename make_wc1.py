#!/usr/bin/env python3
"""Build World Cup Book 1: MetLife's Big Match (ages 5-9, more text)."""
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
    print("WC #1: MetLife's Big Match")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    D='/home/team/shared/wc2026-metlife-illustrations';O='/home/team/shared/wc1-metlife-kdp.pdf'
    # More text per page - use taller box and smaller font for older readers
    texts={
        2:'The sun hadn\'t even finished waking up, but Alex was already wide awake! Today wasn\'t just any Saturday. Today was the day of the World Cup Match!\n\n"Alex, are you ready?" Dad called from the hallway.\n\n"I\'ve been ready since last year, Dad!" Alex shouted back, pulling on his lucky jersey.',
        3:'As they drove down the long highway, Alex pressed his face against the window. There it was! MetLife Stadium.\n\nIt looked like a giant silver palace. Did you know MetLife has over 82,000 seats? Alex wondered if he could count them all.',
        4:'As Alex stepped out of the car, he heard a deep, rumbling hum. It wasn\'t the wind — it was the stadium itself!\n\nMetLife was a friendly giant. He had big lights for eyes that glowed a warm yellow, and his skin was made of shimmering glass and metal.',
        5:'The giant stadium stretched out his goalpost arms to welcome everyone. Alex felt like he was walking into the heart of a friendly giant.\n\n"Welcome to the Meadowlands!" the giant seemed to whisper. Alex high-fived a silver panel. It felt cool and strong.',
        6:'Inside, the stadium was buzzing like a beehive! Fans from Argentina wore blue and white stripes, while fans from the USA wore red, white, and blue.\n\nThe air smelled like popcorn and excitement. Alex could hear music playing and people singing songs in different languages.',
        7:'Then, they walked through the tunnel. *WHOOSH!* The stadium opened up! The bright green grass looked like a velvet carpet. The sky was a brilliant blue, and the silver walls reached up toward the clouds.',
        8:'Suddenly, the music got louder. *BOOM!* Fireworks exploded over the silver rim of the stadium, painting the sky with sparkles.\n\nThe pre-game show had begun! Dancers moved across the grass, and giant flags fluttered in the breeze.',
        9:'"There they are!" Dad shouted. The players walked out, looking like heroes in a storybook. Team USA looked strong, and Team Argentina looked fast. Alex cheered as loud as he could.',
        10:'*TWEET!* The whistle blew, and the match began! The ball zipped across the green grass like a shooting star. Argentina\'s star player was as fast as a rabbit! But the USA defenders were as strong as lions.',
        11:'Back and forth they went! Alex watched every move. "Pass it! Pass it!" Alex yelled. The USA player kicked the ball to his teammate. They were moving closer to the goal!',
        12:'The ball flew high into the air. A USA player jumped up and — *BONK!* — he hit the ball with his head! The goalkeeper dived to the left. The ball spun to the right. Everyone held their breath.',
        13:'*GOALLLLLLLL!* The stadium erupted! The roar was so loud that Alex felt it in his toes. Alex and Dad hugged, jumping up and down. Even the MetLife giant shivered with joy!',
        14:'At half-time, Alex enjoyed a delicious stadium hot dog. Suddenly, he looked up at the giant video board. "Dad, look! It\'s us!" Alex and Dad were on the big screen!',
        15:'The second half began, and Argentina was determined. "They\'re very good," Alex said. "They are," Dad agreed. "That\'s why the World Cup is so special — the best teams in the world play here."',
        16:'Argentina kicked a powerful shot. *SWISH!* It went right into the corner of the net. Now the score was tied! Alex felt a little sad, but then he saw the players high-five each other.',
        17:'"That was a great goal," Dad said. "In soccer, we cheer for our team, but we also respect the other team. That\'s called sportsmanship." Alex began to clap for the great play too.',
        18:'The clock was ticking down. Only a few minutes left! The sun began to set, and the MetLife giant\'s silver skin turned orange and gold. He turned on his light-bulb eyes to help everyone see.',
        19:'USA took one last shot. *CLANG!* It hit the post and bounced away. The stadium giant felt the vibration. Everyone groaned, then laughed. It was so close!',
        20:'*TWEET! TWEET! TWEET!* The match was over. It was a tie! Both teams had played their best. Alex saw the players trading jerseys. They were rivals on the field, but friends when the game ended.',
        21:'As they walked back to the car, Alex felt tired but very happy. He had a new World Cup hat and a souvenir program. "That was the best day ever," Alex said.',
        22:'In the car, Alex\'s eyes grew heavy. He dreamed of dribbling the ball through the Meadowlands, scoring the winning goal in the World Cup Final. Dad smiled and turned the radio down low.',
        23:'The fans went home, and the stadium grew quiet. The MetLife giant settled back into the grass. He had a big job coming up in 2026 — hosting the World Cup Final!',
        24:'MetLife Stadium is ready for the world! Will you be there to cheer?\n\n**Fun Fact:** MetLife Stadium will host the 2026 World Cup Final! It\'s made of 40,000 tons of steel — that\'s a lot of metal for one friendly giant!',
    }
    c=canvas.Canvas(O,pagesize=(PG,PH))
    # Front cover
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12)
    c.setFillColorRGB(0.9,0.6,0.0)
    c.drawCentredString(PG/2,PH-185,"A StorySprout Press Book")
    c.showPage()
    # Interior pages
    for pn in range(1,25):
        plc(c,D+f'/page-{pn:02d}.png',PG,PH)
        if pn in texts:
            t=texts[pn];x0=B+M;y0=B+12;tw=T-2*M
            # Calculate text box height based on content
            font_size=13; line_h=17
            # Count paragraphs and line breaks
            paras=t.split('\n\n')
            num_lines=sum(max(1,len(textwrap.wrap(p,width=50))) for p in paras)
            h=max(90,min(200,num_lines*line_h+20))
            th=h
            c.setFillColorRGB(1,1,1,alpha=0.75)
            c.roundRect(x0,y0,tw,th,8,fill=1,stroke=0)
            c.setFillColorRGB(0.1,0.1,0.15)
            c.setFont("Helvetica",font_size)
            cy=y0+th-line_h-5
            for para in paras:
                wrapped=textwrap.wrap(para,width=50)
                for line in wrapped:
                    c.drawCentredString(B+T/2,cy,line);cy-=line_h
                cy-=4  # paragraph spacing
        if pn>1:
            c.setFont("Helvetica",9)
            c.setFillColorRGB(0.5,0.5,0.5)
            c.drawCentredString(B+T/2,B+5,str(pn))
        c.showPage()
    # Back cover - no text overlay (image may have its own text)
    plc(c,D+'/back-cover.png',PG,PH)
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")
    lis=r"""# World Cup Book #1: "MetLife's Big Match" - Product Listing

## Amazon KDP Product Details
**Title:** MetLife's Big Match: A World Cup Soccer Story for Kids - Join Alex at the Biggest Stadium in America!
**Series:** World Cup Adventures (Book 1)
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 5-9**
**Price (Print):** $9.99 | **Price (Digital):** $4.99

### Amazon Bullet Points
1. **WORLD CUP SOCCER ADVENTURE** - Join 7-year-old Alex for the most exciting day of his life at MetLife Stadium, home of the 2026 World Cup Final!
2. **AGES 5-9 FORMAT** - Longer, richer text for older readers with fun soccer facts, sportsmanship lessons, and stadium trivia.
3. **STADIUM COMES TO LIFE** - MetLife Stadium is a friendly giant with glowing light-bulb eyes and goalpost arms who welcomes fans from around the world.
4. **TEACHES SPORTSMANSHIP** - Alex learns to cheer for great plays from both teams and that competition goes hand-in-hand with respect.
5. **FUN SOCCER FACTS** - Did you know MetLife has 82,000 seats and is made of 40,000 tons of steel? Fun facts woven throughout!
6. **BEAUTIFUL ILLUSTRATIONS** - 26 vibrant illustrations of stadiums, players, fireworks, and the magic of match day.
7. **FAMILY BONDING** - A heartwarming father-son story about sharing experiences and making memories.

### Amazon Backend Keywords
children's soccer book, world cup kids book, metlife stadium book, soccer story for kids, sportsmanship children's book, football book ages 5-9, world cup 2026, stadium adventure book, father son story, new jersey sports, soccer fan book, goal kids book, team usa book, sports illustrated kids, world cup final book

### Etsy Listing
**Title:** MetLife's Big Match - Printable Children's Soccer Storybook PDF | World Cup Book for Kids | Stadium Adventure Digital Download
**Tags:** childrens storybook, printable book for kids, soccer book, world cup kids, stadium adventure, sports book, football story, digital download, ages 5-9, sport kids book, father son, homeschool resource
**Description:** Join Alex and his dad for an unforgettable day at MetLife Stadium! From the roar of the crowd to a thrilling goal, this story celebrates soccer, family, and the magic of the beautiful game. 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-wc1-storybook.md','w') as f:f.write(lis)
    print("  -> /home/team/shared/listings-wc1-storybook.md")
    print("WC BOOK #1 COMPLETE!")
if __name__=='__main__':go()