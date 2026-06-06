#!/usr/bin/env python3
"""Build Bible Series Book #2: David and the Giant."""
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
    print("BIBLE #2: David and the Giant")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    D='/home/team/shared/david-goliath-illustrations';O='/home/team/shared/bible2-david-kdp.pdf'
    txt={
        2:'High in the green hills, lived a boy named David.',
        3:'David was a shepherd. He took care of his fluffy sheep every single day.',
        4:'David had a special friend named Woolly. Woolly was a little lamb who followed David everywhere.',
        5:'One day, David\'s father said, "Please take some bread and cheese to your brothers. They are at the army camp."',
        6:'David and Woolly walked and walked. They saw many colorful tents and many tall soldiers.',
        7:'Just then, a very big man stepped out. His name was Goliath.',
        8:'Goliath was as tall as a tree! "Who will come and play a game with me?" he called out.',
        9:'All the soldiers were afraid. They hid behind their big shields. But not David!',
        10:'"I am not afraid," David said. "God is with me, and God is very big and strong."',
        11:'David went to see King Saul. The king sat on a throne and wore a bright gold crown.',
        12:'"You are just a boy," King Saul said. "Goliath is very big." David smiled. "God helps me take care of my sheep. He will help me now."',
        13:'King Saul tried to give David his armor. It was very heavy and very shiny.',
        14:'"This is too big!" David laughed. "I don\'t need a sword. I have my sling and my faith."',
        15:'David walked down to the sparkling stream. He looked for something special.',
        16:'*One, two, three, four, five.* David picked up five smooth, round stones.',
        17:'David put the stones in his pouch. He took his sling in his hand. "Let\'s go, Woolly!"',
        18:'Goliath saw David coming. "You are very small!" Goliath shouted.',
        19:'David shouted back, "You have a sword, but I have God on my side!"',
        20:'David put a stone in his sling. He whirled it around and around. *Whish! Whish! Whish!*',
        21:'*Pop!* The stone flew through the air. It hit Goliath right on his forehead.',
        22:'*Thump!* Goliath fell down. He was very big, so he made a very big sound.',
        23:'All the soldiers cheered. "Hooray for David!" they cried.',
        24:'David went back to his sheep in the hills. He knew that with God\'s help, anyone can be brave.',
    }
    c=canvas.Canvas(O,pagesize=(PG,PH))
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12)
    c.setFillColorRGB(0.5,0.3,0.1)
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
    blurb=("Young David is a shepherd who trusts God. When the giant\n"
           "Goliath challenges the army, everyone is afraid. But David\n"
           "knows that with God, even a boy can be brave.\n\nAges 2-6 | StorySprout Press")
    lines=blurb.split('\n');y=PH-115
    for line in lines:
        c.drawCentredString(PG/2,y,line);y-=16
    c.setFont("Helvetica",9)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawCentredString(PG/2,55,"StorySprout Press")
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")
    lis=r"""# Bible Series Book #2: "David and the Giant" - Product Listing

## Amazon KDP Product Details
**Title:** David and the Giant: A Bible Story for Little Ones - A Gentle Introduction to David and Goliath for Children Ages 2-6
**Series:** Bible Adventures (Book 2)
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99

### Amazon Bullet Points
1. **GENTLE BIBLE STORY** - A warm, child-friendly retelling of David and Goliath with a focus on courage, faith, and trusting God.
2. **BEAUTIFUL ILLUSTRATIONS** - 24 stunning full-color illustrations of shepherds, sheep, soldiers, and the friendly giant.
3. **TEACHES COURAGE & FAITH** - David's trust in God shows children that bravery comes from believing in something bigger than yourself.
4. **LOVELY CHARACTERS** - Meet young David, Woolly the lamb, King Saul, and Goliath the gentle giant.
5. **SOUND WORDS** - Fun text with *Whish! Whish! Whish!*, *Pop!*, and *Thump!* makes reading interactive.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **COMFORTING MESSAGE** - A reassuring story about facing big challenges with faith and courage.

### Amazon Backend Keywords
children's bible story, david and goliath for kids, bible story for toddlers, christian children's book, david and the giant, faith based kids book, courage bible story, preschool bible story, bible adventures series, shepherd boy story, sunday school book, old testament for kids, christian toddler book, brave book for kids, sheep and shepherd story

### Etsy Listing
**Title:** David and the Giant - Printable Bible Storybook PDF | David and Goliath for Kids | Christian Children's Book Digital Download
**Tags:** bible storybook, printable book for kids, david and goliath, christian kids book, sunday school, preschool bible, courage story, digital download, faith based, toddler bible, homeschool resource, brave boy book
**Description:** A gentle retelling of David and Goliath for little ones. Young David trusts God and faces the giant with five smooth stones and a brave heart! 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-bible2-storybook.md','w') as f:f.write(lis)
    print("  -> /home/team/shared/listings-bible2-storybook.md")
    print("BIBLE BOOK #2 COMPLETE!")
if __name__=='__main__':go()