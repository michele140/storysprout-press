#!/usr/bin/env python3
"""Build Bible Book 4: Daniel and the Friendly Lions."""
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
    print("BIBLE #4: Daniel and the Friendly Lions")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    D='/home/team/shared/daniel-illustrations';O='/home/team/shared/bible4-daniel-kdp.pdf'
    txt={
        2:'Long ago, there was a kind man named Daniel. Daniel worked hard and he always did his best.',
        3:'King Darius liked Daniel very much. "You are a good helper, Daniel," the King said with a smile.',
        4:'But some other men in the palace were jealous. They didn\'t want the King to like Daniel so much.',
        5:'The men made a trick rule. "Everyone must pray only to the King for thirty days!" they told the King.',
        6:'Daniel heard the rule. But Daniel loved to talk to God. He prayed every morning, every noon, and every night.',
        7:'The jealous men watched Daniel. "Look!" they cried. "Daniel is still praying to God! He broke the rule!"',
        8:'The men went to the King. "Daniel broke the rule," they said. "He must go into the lions\' pit."',
        9:'King Darius didn\'t want to hurt Daniel. But he had already made the rule. He had to follow it.',
        10:'The soldiers took Daniel to a big, deep pit. Inside the pit lived a group of big, fluffy lions.',
        11:'*Roar!* went the lions. But they didn\'t sound scary. They sounded like they were saying hello!',
        12:'Daniel stepped into the pit. The lions didn\'t bite. They just sniffed Daniel\'s colorful coat.',
        13:'One lion began to purr. *Purr, purr, purr.* It sounded like a little motor.',
        14:'Another lion wanted to play! It rolled onto its back and showed its fluffy tummy.',
        15:'Suddenly, the pit became very bright. A gentle Angel of light appeared in the middle of the lions.',
        16:'The Angel smiled at Daniel. "Do not be afraid," the Angel whispered. "God is watching over you."',
        17:'The Angel patted the lions on their heads. One by one, the lions began to yawn. *Yaaaawn!*',
        18:'The lions curled up into big, orange balls of fluff. Soon, they were all fast asleep.',
        19:'Up in the palace, King Darius couldn\'t sleep. He was too worried about his friend Daniel.',
        20:'As soon as the sun came up, the King ran to the pit. "Daniel! Daniel! Are you okay?" he called out.',
        21:'Daniel looked up and waved. "I am safe, King Darius! God sent an Angel to stay with me."',
        22:'King Darius was so happy! He told the soldiers to help Daniel out of the pit right away.',
        23:'The King told everyone the good news. "God is very strong! He protects his friends," the King said.',
        24:'Daniel went back to his work with a happy heart. He knew that God would always be his best friend.',
    }
    c=canvas.Canvas(O,pagesize=(PG,PH))
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12)
    c.setFillColorRGB(0.9,0.5,0.1)
    c.drawCentredString(PG/2,PH-185,"A StorySprout Press Book")
    c.showPage()
    for pn in range(1,25):
        plc(c,D+f'/page-{pn:02d}.png',PG,PH)
        if pn in txt:
            t=txt[pn];x0=B+M;y0=B+12;tw=T-2*M;th=85
            c.setFillColorRGB(1,1,1,alpha=0.75)
            c.roundRect(x0,y0,tw,th,8,fill=1,stroke=0)
            c.setFillColorRGB(0.1,0.1,0.15)
            c.setFont("Helvetica",14)
            wrapped=textwrap.wrap(t,width=48);cy=y0+th-18
            for line in wrapped:
                c.drawCentredString(B+T/2,cy,line);cy-=18
        if pn>1:
            c.setFont("Helvetica",9)
            c.setFillColorRGB(0.5,0.5,0.5)
            c.drawCentredString(B+T/2,B+5,str(pn))
        c.showPage()
    plc(c,D+'/back-cover.png',PG,PH)
    c.setFillColorRGB(0.2,0.2,0.2)
    c.setFont("Helvetica-Bold",16)
    c.drawCentredString(PG/2,PH-85,"About the Story")
    c.setFont("Helvetica",11)
    blurb=("Daniel is thrown into a pit of lions for praying to God.\n"
           "But the lions are friendly, and an Angel keeps Daniel\n"
           "safe through the night. A story of faith and courage.\n\nAges 2-6 | StorySprout Press")
    lines=blurb.split('\n');y=PH-115
    for line in lines:
        c.drawCentredString(PG/2,y,line);y-=16
    c.setFont("Helvetica",9)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawCentredString(PG/2,55,"StorySprout Press")
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")
    lis=r"""# Bible Series Book #4: "Daniel and the Friendly Lions" - Product Listing

## Amazon KDP Product Details
**Title:** Daniel and the Friendly Lions: A Bible Story for Little Ones - A Gentle Introduction to Daniel for Children Ages 2-6
**Series:** Bible Adventures (Book 4)
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99

### Amazon Bullet Points
1. **GENTLE BIBLE STORY** - A warm, child-friendly retelling of Daniel in the lions' den, featuring cuddly lions and a glowing angel.
2. **BEAUTIFUL ILLUSTRATIONS** - 24 vibrant full-color illustrations of palaces, lions, and a gentle angel made of light.
3. **TEACHES FAITH & COURAGE** - Daniel's trust in God shows children the power of staying true to their beliefs.
4. **LOVELY CHARACTERS** - Meet Daniel, King Darius, the friendly lions, and the glowing Angel.
5. **FUN SOUND WORDS** - Playful text with *Roar!*, *Purr, purr, purr*, and *Yaaaawn!* makes reading engaging.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **COMFORTING MESSAGE** - A reassuring story about God's protection and the power of prayer.

### Amazon Backend Keywords
children's bible story, daniel and the lions den, bible story for toddlers, christian children's book, daniel bible story, lion book for kids, preschool bible story, bible adventures series, faith courage book, sunday school book, old testament for kids, christian toddler book, lion and angel story, prayer kids book, king darius story

### Etsy Listing
**Title:** Daniel and the Friendly Lions - Printable Bible Storybook PDF | Daniel in the Lions Den for Kids | Christian Children's Book Digital Download
**Tags:** bible storybook, printable book for kids, daniel and the lions, christian kids book, sunday school, preschool bible, lion story, digital download, faith based, toddler bible, homeschool resource, angel story
**Description:** A gentle retelling of Daniel in the lions' den. When Daniel is thrown to the lions for praying, he discovers they're friendly - and an Angel keeps him safe! 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-bible4-storybook.md','w') as f:f.write(lis)
    print("  -> /home/team/shared/listings-bible4-storybook.md")
    print("BIBLE BOOK #4 COMPLETE!")
if __name__=='__main__':go()