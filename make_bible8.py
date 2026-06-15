#!/usr/bin/env python3
"""Build Bible Book 8: Joseph's Colorful Coat."""
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
    print("BIBLE #8: Joseph's Colorful Coat")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    D='/home/team/shared/joseph-illustrations';O='/home/team/shared/bible8-joseph-kdp.pdf'
    txt={
        2:'Once there was a boy named Joseph. Joseph lived in a big, happy home with his father and ten older brothers.',
        3:'Joseph\'s father, Jacob, loved him very much. One day, Jacob had a very special surprise for Joseph.',
        4:'Jacob gave Joseph a beautiful coat. It had stripes of red, orange, yellow, green, blue, and purple!',
        5:'Joseph loved his new coat. "Thank you, Father!" he said. He felt like a prince.',
        6:'But Joseph\'s brothers were a little bit jealous. They wished they had colorful coats, too.',
        7:'One night, Joseph had a very special dream. He saw the bright sun, the moon, and eleven stars dancing in the sky.',
        8:'Joseph told his family about his dream. "The stars were all bowing to me!" he said with a smile.',
        9:'Joseph had another dream. He saw bundles of golden wheat in a field. His bundle stood tall while the others bowed.',
        10:'The brothers did not like Joseph\'s dreams. They decided to play a trick on him to take his coat away.',
        11:'One day, when Joseph came to find them in the field, they put him into a deep, dry well.',
        12:'The brothers took Joseph\'s colorful coat. Joseph felt very lonely at the bottom of the well.',
        13:'Soon, some kind travelers came by on their way to a far-away land called Egypt.',
        14:'The travelers found Joseph and helped him out of the well. "Come with us to Egypt!" they said.',
        15:'Joseph traveled a long way on a tall, bumpy camel. Egypt was very big and had many beautiful buildings.',
        16:'In Egypt, Joseph worked very hard. He was so helpful that the King of Egypt made him a very important leader.',
        17:'Joseph had an important job. He saved up lots of grain so that everyone would have plenty of food to eat.',
        18:'Many years passed. Back home, Joseph\'s family ran out of food. They heard that there was food in Egypt.',
        19:'The brothers traveled to Egypt to ask for help. They did not know that the important leader was their brother, Joseph!',
        20:'Joseph saw his brothers. He felt his heart get very warm. He still loved them very much.',
        21:'Joseph told them who he was. "I am your brother, Joseph!" he cried. The brothers were very surprised!',
        22:'Joseph forgave his brothers for their trick. He gave them a big hug and lots of yummy food to take home.',
        23:'Joseph\'s whole family moved to Egypt to live with him. Even his father, Jacob, came to see the beautiful palace.',
        24:'Joseph knew that God had a special plan for him all along. His heart was as bright as his colorful coat.',
    }
    c=canvas.Canvas(O,pagesize=(PG,PH))
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12);c.setFillColorRGB(0.7,0.1,0.3)
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
    blurb=("Joseph gets a beautiful rainbow coat that makes his\nbrothers jealous. After many adventures in Egypt,\nJoseph forgives them and discovers God had a plan\nall along.\n\nAges 2-6 | StorySprout Press")
    lines=blurb.split('\n');y=PH-115
    for line in lines:
        c.drawCentredString(PG/2,y,line);y-=16
    c.setFont("Helvetica",9);c.setFillColorRGB(0.5,0.5,0.5)
    c.drawCentredString(PG/2,55,"StorySprout Press")
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")
    lis=r"""# Bible Series Book #8: "Joseph's Colorful Coat" - Product Listing
**Title:** Joseph's Colorful Coat: A Bible Story for Little Ones - A Gentle Introduction to Joseph for Children Ages 2-6
**Series:** Bible Adventures (Book 8)
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99
### Amazon Bullet Points
1. **GENTLE BIBLE STORY** - A warm, child-friendly retelling of Joseph and his colorful coat, forgiveness, and God's loving plan.
2. **BEAUTIFUL ILLUSTRATIONS** - 24 vibrant illustrations of Joseph, his coat, the Egyptian palace, and Snowball the sheep.
3. **TEACHES FORGIVENESS** - Joseph's journey shows children the power of forgiving others and trusting God's plan.
4. **LOVELY CHARACTERS** - Meet Joseph, Jacob, the ten brothers, and Snowball the fluffy sheep.
5. **COLORFUL COAT THEME** - The rainbow coat is a fun, visual element children will love spotting on every page.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **DREAMS COME TRUE** - A reassuring story about how even hard times can lead to wonderful things.
### Amazon Backend Keywords
children's bible story, joseph and his coat, bible story for toddlers, christian children's book, joseph colorful coat, forgiveness kids book, preschool bible story, bible adventures series, dream story, sunday school book, old testament for kids, christian toddler book, brothers story, egypt bible story, sheep and shepherd
### Etsy Listing
**Title:** Joseph's Colorful Coat - Printable Bible Storybook PDF | Joseph Bible Story for Kids | Christian Children's Book Digital Download
**Tags:** bible storybook, printable book for kids, joseph story, christian kids book, sunday school, preschool bible, colorful coat, digital download, faith based, toddler bible, homeschool resource, forgiveness
**Description:** A gentle retelling of Joseph and his colorful coat. Joseph's brothers are jealous, but after adventures in Egypt, Joseph forgives them and discovers God's plan! 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-bible8-storybook.md','w') as f:f.write(lis)
    print("  -> /home/team/shared/listings-bible8-storybook.md")
    print("BIBLE BOOK #8 COMPLETE!")
if __name__=='__main__':go()