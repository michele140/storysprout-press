#!/usr/bin/env python3
"""Build Bible Book 7: The Good Samaritan."""
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
    print("BIBLE #7: The Good Samaritan")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    D='/home/team/shared/samaritan-illustrations';O='/home/team/shared/bible7-samaritan-kdp.pdf'
    txt={
        2:'Once there was a traveler named Thomas. Thomas loved to go on long walks to see new places.',
        3:'One day, Thomas went on a very long walk. The road was dusty and full of big, grey rocks.',
        4:'Thomas walked and walked. *Tramp, tramp, tramp.* The sun was very hot, and his legs began to feel heavy.',
        5:'Oh no! Thomas tripped over a big rock. *Ouch!* He sat down on the side of the road.',
        6:'Thomas was very tired. He needed someone to help him get to the next town.',
        7:'Soon, a man came walking by. Thomas waved his hand. "Hello! Can you help me?" he asked.',
        8:'But the man did not stop. He was in a big hurry. He walked right past Thomas.',
        9:'Then, another man came by. He saw Thomas sitting there, but he walked on the other side of the road.',
        10:'Thomas felt very lonely. "Will anyone stop to help me?" he wondered.',
        11:'Suddenly, he heard a new sound. *Clip-clop, clip-clop.* A little donkey was coming down the road.',
        12:'It was a man from a place called Samaria. People called him the Good Samaritan because he had a big heart.',
        13:'The Good Samaritan knelt down. "Don\'t worry, friend," he said. "I will help you."',
        14:'He gently cleaned Thomas\'s scrape and put on a soft white bandage. Thomas began to feel much better.',
        15:'Then, the Good Samaritan helped Thomas stand up. "You can ride on my donkey," he said.',
        16:'He lifted Thomas up onto the donkey\'s back. The donkey\'s fur was very soft and fuzzy.',
        17:'They traveled together down the long road. The Good Samaritan walked beside them, holding the donkey\'s rope.',
        18:'They reached a cozy inn. An inn is like a big house where travelers can sleep in warm beds.',
        19:'The Innkeeper came to the door. "Welcome! Welcome!" he said. "We have plenty of room."',
        20:'The Good Samaritan helped Thomas into a soft, comfy bed. He gave him a cool drink of water.',
        21:'The next morning, the Good Samaritan spoke to the Innkeeper. He gave him some shiny coins.',
        22:'"Please take good care of my friend," the Good Samaritan said. "I want him to be strong and happy."',
        23:'Thomas thanked the Good Samaritan for being such a good neighbor. "You are very kind," he said.',
        24:'The Good Samaritan smiled. "Always be kind and help others," he said. And Thomas promised he would.',
    }
    c=canvas.Canvas(O,pagesize=(PG,PH))
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12);c.setFillColorRGB(0.8,0.4,0.1)
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
    blurb=("When Thomas the Traveler gets hurt on a long road, two\npeople pass him by. But a kind Samaritan stops to help,\nshowing that being a good neighbor means helping anyone\nin need.\n\nAges 2-6 | StorySprout Press")
    lines=blurb.split('\n');y=PH-115
    for line in lines:
        c.drawCentredString(PG/2,y,line);y-=16
    c.setFont("Helvetica",9);c.setFillColorRGB(0.5,0.5,0.5)
    c.drawCentredString(PG/2,55,"StorySprout Press")
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")
    lis=r"""# Bible Series Book #7: "The Good Samaritan" - Product Listing
**Title:** The Good Samaritan: A Bible Story for Little Ones - A Gentle Lesson in Kindness for Children Ages 2-6
**Series:** Bible Adventures (Book 7)
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99
### Amazon Bullet Points
1. **GENTLE PARABLE STORY** - Jesus's beloved parable of the Good Samaritan, retold warmly for little ones with a focus on kindness and helping others.
2. **BEAUTIFUL ILLUSTRATIONS** - 24 vibrant illustrations of travelers, donkeys, and a cozy inn on a sunny road.
3. **TEACHES KINDNESS** - A clear, gentle lesson about helping people in need, no matter who they are.
4. **LOVELY CHARACTERS** - Meet Thomas the Traveler, the Good Samaritan, the Little Donkey, and the cheerful Innkeeper.
5. **SOUND WORDS** - Fun text with *Tramp, tramp, tramp*, *Ouch!*, and *Clip-clop, clip-clop*.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **BEING A GOOD NEIGHBOR** - A timeless message about compassion that every child can understand and practice.
### Amazon Backend Keywords
children's bible story, good samaritan for kids, bible story for toddlers, christian children's book, parable for children, kindness book, preschool bible story, bible adventures series, helping others, sunday school book, new testament for kids, christian toddler book, neighbor story, compassion book, jesus parable
### Etsy Listing
**Title:** The Good Samaritan - Printable Bible Storybook PDF | Parable for Kids | Christian Children's Book Digital Download
**Tags:** bible storybook, printable book for kids, good samaritan, christian kids book, sunday school, preschool bible, kindness story, digital download, faith based, toddler bible, homeschool resource, helping others
**Description:** A gentle retelling of the Good Samaritan. When Thomas gets hurt on the road, a kind man stops to help. A timeless lesson in kindness and being a good neighbor. 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-bible7-storybook.md','w') as f:f.write(lis)
    print("  -> /home/team/shared/listings-bible7-storybook.md")
    print("BIBLE BOOK #7 COMPLETE!")
if __name__=='__main__':go()