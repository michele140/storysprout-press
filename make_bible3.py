#!/usr/bin/env python3
"""Build Bible Series Book #3: Jonah and the Big Fish."""
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
    print("BIBLE #3: Jonah and the Big Fish")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    D='/home/team/shared/jonah-illustrations';O='/home/team/shared/bible3-jonah-kdp.pdf'
    txt={
        2:'Long ago, there lived a man named Jonah. Jonah loved God, but sometimes he found it hard to listen.',
        3:'One day, God said, "Jonah, please go to the city of Nineveh. Tell the people there that I love them."',
        4:'But Jonah did not want to go to Nineveh. He decided to run away instead!',
        5:'Jonah went down to the big blue sea. He found a sturdy wooden boat.',
        6:'"Where are you going?" the Captain asked. "Far away!" Jonah said. He hopped onto the boat.',
        7:'The boat sailed out into the deep water. Jonah went downstairs to take a long nap.',
        8:'Suddenly, the sky turned grey. *Whoosh!* The wind began to blow. *Splash!* The waves grew big.',
        9:'The sailors were afraid. "The sea is very grumpy today!" they cried.',
        10:'Jonah woke up and came upstairs. He knew why the sea was grumpy. "I am running away from God," he said quietly.',
        11:'"If you throw me into the water, the sea will be calm again," Jonah told them.',
        12:'The sailors tried to row to land, but the waves were too big. Finally, they gently lifted Jonah and... *Splash!*',
        13:'As soon as Jonah hit the water, the wind stopped. The sea became smooth and quiet again.',
        14:'But Jonah was under the water! *Gurgle, gurgle.* Just then, a very Big Fish swam by.',
        15:'*Gulp!* The Big Fish swallowed Jonah whole!',
        16:'Inside the Big Fish, it wasn\'t scary at all. It was warm and dark, like a cozy cave.',
        17:'Jonah sat down on a soft spot. He had a lot of time to think.',
        18:'"I\'m sorry, God," Jonah prayed. "I should have listened to you. Please give me another chance."',
        19:'Jonah stayed inside the Big Fish for three whole days. He sang songs and talked to God.',
        20:'God heard Jonah\'s prayer. He spoke to the Big Fish. "It\'s time to let Jonah go," God said.',
        21:'The Big Fish swam close to the shore. *Wiggle, wiggle, burp!* Jonah flew out onto the dry sand.',
        22:'"Thank you, Big Fish!" Jonah called out. The fish wiggled its tail and swam back into the sea.',
        23:'This time, Jonah listened! He walked all the way to Nineveh and told everyone about God\'s love.',
        24:'Jonah was happy because he listened to God. And God was happy because Jonah was his friend.',
    }
    c=canvas.Canvas(O,pagesize=(PG,PH))
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12)
    c.setFillColorRGB(0.1,0.3,0.6)
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
    blurb=("Jonah learns that running away isn't the answer. After\n"
           "being swallowed by a friendly Big Fish, he prays for a\n"
           "second chance and discovers that God always listens.\n\nAges 2-6 | StorySprout Press")
    lines=blurb.split('\n');y=PH-115
    for line in lines:
        c.drawCentredString(PG/2,y,line);y-=16
    c.setFont("Helvetica",9)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawCentredString(PG/2,55,"StorySprout Press")
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")
    lis=r"""# Bible Series Book #3: "Jonah and the Big Fish" - Product Listing

## Amazon KDP Product Details
**Title:** Jonah and the Big Fish: A Bible Story for Little Ones - A Gentle Introduction to Jonah for Children Ages 2-6
**Series:** Bible Adventures (Book 3)
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99

### Amazon Bullet Points
1. **GENTLE BIBLE STORY** - A warm, child-friendly retelling of Jonah, featuring a friendly Big Fish and a message of second chances.
2. **BEAUTIFUL OCEAN ILLUSTRATIONS** - 24 vibrant full-color illustrations of boats, storms, and a happy Big Fish.
3. **TEACHES LISTENING & OBEDIENCE** - Jonah's journey helps children understand the importance of listening and saying sorry.
4. **LOVELY CHARACTERS** - Meet Jonah, the friendly Big Fish, the brave Captain, and kind Sailors.
5. **SOUND WORDS** - Fun text with *Whoosh!*, *Splash!*, *Gulp!*, and *Wiggle, wiggle, burp!* makes reading interactive.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **SECOND CHANCES** - A reassuring message about forgiveness and God's love.

### Amazon Backend Keywords
children's bible story, jonah and the whale for kids, bible story for toddlers, christian children's book, jonah and the big fish, ocean bible story, preschool bible story, bible adventures series, second chances book, sunday school book, old testament for kids, christian toddler book, fish story for kids, obedience book, forgiveness children's book

### Etsy Listing
**Title:** Jonah and the Big Fish - Printable Bible Storybook PDF | Jonah and the Whale for Kids | Christian Children's Book Digital Download
**Tags:** bible storybook, printable book for kids, jonah and the whale, christian kids book, sunday school, preschool bible, ocean story, digital download, faith based, toddler bible, homeschool resource, second chances
**Description:** A gentle retelling of Jonah for little ones. When Jonah runs away, a friendly Big Fish teaches him about listening, second chances, and God's love. 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-bible3-storybook.md','w') as f:f.write(lis)
    print("  -> /home/team/shared/listings-bible3-storybook.md")
    print("BIBLE BOOK #3 COMPLETE!")
if __name__=='__main__':go()