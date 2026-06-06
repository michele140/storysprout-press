#!/usr/bin/env python3
"""Build Bible Series Book #1: Noah's Big Boat."""
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
    print("BIBLE #1: Noah's Big Boat")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    D='/home/team/shared/noahs-ark-illustrations';O='/home/team/shared/bible1-noah-kdp.pdf'
    txt={
        2:'Long ago, there was a man named Noah. He was very kind and he loved God very much.',
        3:'One day, God spoke to Noah. "Build a big, big boat," God said. "It will be a safe home for you and the animals."',
        4:'Noah started to work right away. *Clunk, clunk, clunk!* He used big pieces of wood to build the boat.',
        5:'Mrs. Noah helped too. She packed many baskets of yummy food for everyone to eat.',
        6:'Some people watched and laughed. "A boat on dry land?" they asked. But Noah just smiled. He knew God had a wonderful plan.',
        7:'Soon, the big boat was finished. It was huge! It had a big wooden door and a little window at the very top.',
        8:'Then, something amazing happened. From near and far, the animals began to arrive!',
        9:'They came two by two. Two big, grey elephants came *stomp, stomp, stomp* up the ramp.',
        10:'Two tall, spotted giraffes came *stretch, stretch, stretch* with their long necks.',
        11:'Two orange lions came *pad, pad, pad* with their soft paws. Every animal was invited to the safe home.',
        12:'Birds of every color flew inside. *Flap, flap, flap!* The big boat was filling up with friends.',
        13:'Once everyone was safe and sound inside, the big wooden door slowly closed.',
        14:'Then, the rain began to fall. *Pitter-patter, pitter-patter.* The big boat began to float on the water.',
        15:'It rained and it rained for a long time. But inside the boat, it was warm and very cozy.',
        16:'The lions napped. The elephants played. Noah and his family were safe and happy in their floating home.',
        17:'One day, the *pitter-patter* stopped. The sun began to peek through the clouds again.',
        18:'Noah opened the window wide. He sent a little white dove to fly out and look for land.',
        19:'The dove flew and flew, but she only saw water. She came back to the boat to rest with Noah.',
        20:'A few days later, Noah sent the dove out again. "Find us a sign," he whispered.',
        21:'This time, the dove returned with something special — a bright green olive branch! "Land is near!" Noah cheered.',
        22:'The big boat came to rest on the top of a high mountain. The sun was warm, and the water was going away.',
        23:'Everyone came out of the boat. The animals ran, hopped, and flew for joy! It was a brand new day.',
        24:'Look up! A beautiful rainbow stretched across the sky. It was God\'s colorful promise to always love the world.',
    }
    c=canvas.Canvas(O,pagesize=(PG,PH))
    # Front cover
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12)
    c.setFillColorRGB(0.8,0.6,0.1)
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
    blurb=("Follow Noah as he builds a big boat, fills it with\n"
           "animals two by two, and sets sail through a great rain.\n"
           "When a dove returns with an olive branch, the rainbow\n"
           "appears — God's promise of love for all the world.\n\nAges 2-6 | StorySprout Press")
    lines=blurb.split('\n');y=PH-115
    for line in lines:
        c.drawCentredString(PG/2,y,line);y-=16
    c.setFont("Helvetica",9)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawCentredString(PG/2,55,"StorySprout Press")
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")
    lis=r"""# Bible Series Book #1: "Noah's Big Boat" - Product Listing

## Amazon KDP Product Details
**Title:** Noah's Big Boat: A Bible Story for Little Ones - A Gentle Introduction to Noah's Ark for Children Ages 2-6
**Series:** Bible Adventures (Book 1)
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99

### Amazon Bullet Points
1. **GENTLE BIBLE STORY** - A warm, child-friendly retelling of Noah's Ark that introduces little ones to this beloved Bible story in a comforting way.
2. **BEAUTIFUL ARK ILLUSTRATIONS** - 24 stunning full-color illustrations of the Ark, animals, Noah's family, and the beautiful rainbow promise.
3. **TEACHES OBEDIENCE & TRUST** - Noah's faith and trust in God's plan teaches children the value of doing what is right, even when others don't understand.
4. **BELOVED ANIMALS** - Elephants, giraffes, lions, and birds of every color march two by two onto the big boat.
5. **SOUND WORDS** - Fun text with *Clunk, clunk, clunk!*, *Stomp, stomp, stomp!*, and *Flap, flap, flap!* makes reading interactive and engaging.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **RAINBOW PROMISE** - The story ends with God's colorful rainbow promise, a message of love and hope for all children.

### Amazon Backend Keywords
children's bible story, noah's ark book for kids, bible story for toddlers, christian children's book, noah and the ark, animals two by two, religious book for kids, preschool bible story, bible adventures series, noah's boat picture book, faith based children's book, sunday school book, rainbow promise, old testament for kids, christian toddler book

### Etsy Listing
**Title:** Noah's Big Boat - Printable Bible Storybook PDF | Noah's Ark for Kids | Christian Children's Book Digital Download
**Tags:** bible storybook, printable book for kids, noah's ark, christian kids book, sunday school, preschool bible, animals story, digital download, faith based, toddler bible, homeschool resource, rainbow promise
**Description:** A gentle retelling of Noah's Ark for little ones. Follow Noah as he builds a big boat, fills it with animals two by two, and discovers God's rainbow promise! 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-bible1-storybook.md','w') as f:f.write(lis)
    print("  -> /home/team/shared/listings-bible1-storybook.md")
    print("BIBLE BOOK #1 COMPLETE!")
if __name__=='__main__':go()