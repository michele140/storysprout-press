#!/usr/bin/env python3
"""Build Bible Book 5: The First Christmas."""
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
    print("BIBLE #5: The First Christmas")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    D='/home/team/shared/christmas-illustrations';O='/home/team/shared/bible5-christmas-kdp.pdf'
    txt={
        2:'Long ago, in a town called Nazareth, lived a kind young woman named Mary. She loved God with all her heart.',
        3:'One day, a bright Angel appeared! "Do not be afraid, Mary," the Angel said with a smile. "God has a special gift for the world."',
        4:'Mary was going to have a baby boy. His name would be Jesus, and He would be very special.',
        5:'Mary was married to a kind man named Joseph. Joseph promised to take care of Mary and the new baby.',
        6:'One day, they had to go on a long journey to a town called Bethlehem.',
        7:'*Clip-clop, clip-clop.* The little donkey walked and walked. The road was long, and the sun was warm.',
        8:'When they reached Bethlehem, the sun was setting. The town was very full of people.',
        9:'Joseph knocked on many doors. "Is there any room for us?" he asked. But every house was full.',
        10:'Finally, one kind man said, "You can stay in my stable. It is warm and dry with lots of hay."',
        11:'Inside the stable, it was quiet and peaceful. Friendly animals were resting there.',
        12:'That very night, Baby Jesus was born! Mary wrapped Him in soft cloth and laid Him in a manger.',
        13:'Nearby, in the dark fields, some shepherds were watching their fluffy sheep.',
        14:'Suddenly, the sky filled with light! A bright Angel appeared, and the shepherds were very surprised.',
        15:'"Good news!" the Angel sang. "A special Baby is born in Bethlehem! Go and see Him."',
        16:'The shepherds ran to the town. "Look!" they cried. "Just like the Angel said!"',
        17:'Far away in the East, three Wise Men saw a new, bright star in the sky.',
        18:'"That star will lead us to the new King!" the Wise Men said. They packed their bags and began their journey.',
        19:'The star moved across the sky, leading them all the way to the little stable in Bethlehem.',
        20:'The Wise Men walked into the stable. They knelt down and gave Baby Jesus special gifts.',
        21:'There was gold, frankincense, and myrrh. The Wise Men were so happy to find the special Baby.',
        22:'Everyone in the stable felt the wonder and love of that first Christmas night.',
        23:'High in the sky, the big star kept shining, telling the whole world the good news.',
        24:'The first Christmas was a night of love and joy. And it all started with a tiny Baby in a manger.',
    }
    c=canvas.Canvas(O,pagesize=(PG,PH))
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12);c.setFillColorRGB(0.8,0.1,0.1)
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
    for line in ("The beautiful story of the very first Christmas. Mary and","Joseph travel to Bethlehem, where Baby Jesus is born.","Angels, shepherds, and Wise Men gather to celebrate.","","Ages 2-6 | StorySprout Press"):pass
    blurb=("The beautiful story of the very first Christmas. Mary and\nJoseph travel to Bethlehem, where Baby Jesus is born.\nAngels, shepherds, and Wise Men gather to celebrate.\n\nAges 2-6 | StorySprout Press")
    lines=blurb.split('\n');y=PH-115
    for line in lines:
        c.drawCentredString(PG/2,y,line);y-=16
    c.setFont("Helvetica",9);c.setFillColorRGB(0.5,0.5,0.5)
    c.drawCentredString(PG/2,55,"StorySprout Press")
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")
    lis=r"""# Bible Series Book #5: "The First Christmas" - Product Listing
**Title:** The First Christmas: A Bible Story for Little Ones - The Nativity Story for Children Ages 2-6
**Series:** Bible Adventures (Book 5)
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99
### Amazon Bullet Points
1. **GENTLE NATIVITY STORY** - A warm, child-friendly retelling of the first Christmas, from the Angel's visit to the Wise Men's gifts.
2. **BEAUTIFUL ILLUSTRATIONS** - 24 vibrant full-color illustrations of Mary, Joseph, shepherds, angels, and the Baby in the manger.
3. **TEACHES CHRISTMAS MEANING** - Helps children understand the true meaning of Christmas in a simple, comforting way.
4. **LOVELY CHARACTERS** - Meet Mary, Joseph, Baby Jesus, Angels, Shepherds, Wise Men, and the gentle donkey.
5. **SOUND WORDS** - Fun text with *Clip-clop, clip-clop* makes the journey to Bethlehem come alive.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **PERFECT HOLIDAY GIFT** - A wonderful Christmas gift for little ones that they'll treasure year after year.
### Amazon Backend Keywords
children's bible story, christmas nativity book, bible story for toddlers, christian children's book, first christmas, jesus birth story, preschool bible story, bible adventures series, nativity for kids, sunday school book, christmas gift for toddler, christian toddler book, mary and joseph, baby jesus book, wise men story
### Etsy Listing
**Title:** The First Christmas - Printable Nativity Storybook PDF | Christmas Bible Story for Kids | Christian Children's Book Digital Download
**Tags:** bible storybook, printable book for kids, christmas nativity, christian kids book, sunday school, preschool bible, jesus birth, digital download, holiday gift, toddler bible, homeschool resource, nativity story
**Description:** A gentle retelling of the very first Christmas. Follow Mary and Joseph to Bethlehem, where angels sing, shepherds visit, and Baby Jesus is born! 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-bible5-storybook.md','w') as f:f.write(lis)
    print("  -> /home/team/shared/listings-bible5-storybook.md")
    print("BIBLE BOOK #5 COMPLETE!")
if __name__=='__main__':go()