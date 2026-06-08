#!/usr/bin/env python3
"""Build Bible Book 6: Moses and the Amazing Sea."""
import os,textwrap
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
    print("BIBLE #6: Moses and the Amazing Sea")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    D='/home/team/shared/moses-illustrations';O='/home/team/shared/bible6-moses-kdp.pdf'
    txt={
        2:'Long ago, a kind man named Moses had a very big job. God asked him to lead a large group of families to a new, beautiful home.',
        3:'Moses\' sister, Miriam, helped him. "Don\'t worry," she told the people. "God is going to take care of us!"',
        4:'The families began their journey. They walked across the warm, sandy desert.',
        5:'*Crunch, crunch, crunch.* Their sandals made a soft sound on the sand. The sun was bright, but they were happy to be together.',
        6:'After walking for many days, they reached the edge of a giant, blue sea called the Red Sea.',
        7:'The people stopped. "The water is too big!" they said. "How will we ever get across?"',
        8:'Suddenly, they heard a sound in the distance. *Thump, thump, thump.* Pharaoh\'s army was coming!',
        9:'The people were afraid. But Moses stood tall. "Do not be afraid," he said. "Watch and see what God will do!"',
        10:'Moses walked right up to the edge of the water. He took a deep breath and prayed.',
        11:'Then, Moses stretched out his wooden staff over the big, blue waves.',
        12:'*Whoosh!* A strong, gentle wind began to blow. It blew and it blew all through the night.',
        13:'Then, something amazing happened. The water began to move! It pushed back further and further.',
        14:'The Red Sea parted! On the left and on the right, the water stood up like tall, shimmering curtains.',
        15:'In the middle of the sea, there was a wide, dry path. "Look!" Miriam cried. "We can walk right through!"',
        16:'Moses led the way. One by one, the families began to walk onto the dry ground between the walls of water.',
        17:'The children looked up at the water walls. "Wow!" they whispered. The water looked like a giant, blue window.',
        18:'The Israelites walked and walked. They felt very safe because they knew God was protecting them.',
        19:'Finally, the very last person stepped onto the other side of the sea. They were safe!',
        20:'Moses stretched out his staff once more. *Splash!* The walls of water began to lean back down.',
        21:'Soon, the Red Sea was just a big, blue body of water again. Pharaoh\'s army couldn\'t follow them anymore.',
        22:'Miriam grabbed her tambourine. *Jingle, jingle, shake!* "Let\'s celebrate!" she cried.',
        23:'Everyone began to sing and dance. They were so happy to be free and safe in their new home.',
        24:'Moses smiled as he watched his friends. He knew that with God\'s help, even the biggest sea could be an amazing path.',
    }
    c=canvas.Canvas(O,pagesize=(PG,PH))
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12);c.setFillColorRGB(0.2,0.4,0.8)
    c.drawCentredString(PG/2,PH-185,"A StorySprout Press Book");c.showPage()
    for pn in range(1,25):
        plc(c,D+f'/page-{pn:02d}.png',PG,PH)
        if pn in txt:
            t=txt[pn];x0=B+M;y0=B+12;tw=T-2*M;th=85
            c.setFillColorRGB(1,1,1,alpha=0.75)
            c.roundRect(x0,y0,tw,th,8,fill=1,stroke=0)
            c.setFillColorRGB(0.1,0.1,0.15);c.setFont("Helvetica",14)
            wrapped=textwrap.wrap(t,width=48);cy=y0+th-18
            for line in wrapped:
                c.drawCentredString(B+T/2,cy,line);cy-=18
        if pn>1:
            c.setFont("Helvetica",9);c.setFillColorRGB(0.5,0.5,0.5)
            c.drawCentredString(B+T/2,B+5,str(pn))
        c.showPage()
    plc(c,D+'/back-cover.png',PG,PH)
    c.setFillColorRGB(0.2,0.2,0.2);c.setFont("Helvetica-Bold",16)
    c.drawCentredString(PG/2,PH-85,"About the Story")
    c.setFont("Helvetica",11)
    blurb=("Moses leads the Israelites through the desert, but a\nmighty sea blocks their way. With God's help, the waters\npart and they walk through on dry ground!\n\nAges 2-6 | StorySprout Press")
    lines=blurb.split('\n');y=PH-115
    for line in lines:
        c.drawCentredString(PG/2,y,line);y-=16
    c.setFont("Helvetica",9);c.setFillColorRGB(0.5,0.5,0.5)
    c.drawCentredString(PG/2,55,"StorySprout Press")
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")
    lis=r"""# Bible Series Book #6: "Moses and the Amazing Sea" - Product Listing
**Title:** Moses and the Amazing Sea: A Bible Story for Little Ones - The Exodus Story for Children Ages 2-6
**Series:** Bible Adventures (Book 6)
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99
### Amazon Bullet Points
1. **GENTLE EXODUS STORY** - A warm, child-friendly retelling of Moses parting the Red Sea, with a focus on faith and God's protection.
2. **BEAUTIFUL OCEAN ILLUSTRATIONS** - 24 vibrant illustrations of the desert journey and the amazing walls of water.
3. **TEACHES FAITH & TRUST** - Moses shows children that with God, impossible things become possible.
4. **LOVELY CHARACTERS** - Meet Moses, Miriam with her tambourine, and the happy Israelite families.
5. **SOUND WORDS** - Fun text with *Crunch, crunch, crunch*, *Whoosh!*, *Splash!*, and *Jingle, jingle, shake!*.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **CELEBRATION OF FREEDOM** - A joyful story about God's protection and the happiness of reaching a new home.
### Amazon Backend Keywords
children's bible story, moses red sea, bible story for toddlers, christian children's book, exodus for kids, parting the sea, preschool bible story, bible adventures series, moses story, sunday school book, old testament for kids, christian toddler book, israelites story, faith and trust book, miriam tambourine
### Etsy Listing
**Title:** Moses and the Amazing Sea - Printable Bible Storybook PDF | Moses Parts the Red Sea | Christian Children's Book Digital Download
**Tags:** bible storybook, printable book for kids, moses red sea, christian kids book, sunday school, preschool bible, exodus story, digital download, faith based, toddler bible, homeschool resource, miracle story
**Description:** A gentle retelling of Moses and the Red Sea. When the Israelites are trapped by the sea, God parts the waters and they walk through on dry ground! 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-bible6-storybook.md','w') as f:f.write(lis)
    print("  -> /home/team/shared/listings-bible6-storybook.md")
    print("BIBLE BOOK #6 COMPLETE!")
if __name__=='__main__':go()