#!/usr/bin/env python3
"""Build Bible Book 9: Adam and Eve's Beautiful Garden."""
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
    print("BIBLE #9: Adam and Eve's Beautiful Garden")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    D='/home/team/shared/adam-eve-illustrations';O='/home/team/shared/bible9-adam-eve-kdp.pdf'
    txt={
        2:'In the very beginning, God made a wonderful world. He made the blue sky, the bright sun, and the deep, sparkly sea.',
        3:'Then, God made a special place called the Garden of Eden. It was the most beautiful garden in the whole world.',
        4:'God made a kind man named Adam to live in the garden. Adam loved his new home very much.',
        5:'The garden was full of animals! There were big animals, small animals, and everything in between.',
        6:'God gave Adam a very special job. "Adam," God\'s gentle voice said, "can you give all the animals a name?"',
        7:'Adam looked at a tall, yellow animal with a very long neck. "I will call you Giraffe!" he said with a smile.',
        8:'Next came a big, orange animal with a fluffy mane. "You look like a Lion!" Adam said. The lion gave a happy, soft roar.',
        9:'Adam named the Elephant, the Monkey, and the little blue Bird. He loved every single one of them.',
        10:'But Adam was all alone. God said, "It is not good for Adam to be alone. I will make a friend for him."',
        11:'So, God made a kind woman named Eve. When Adam saw Eve, he was so happy!',
        12:'Adam and Eve loved living in the garden together. They walked through the soft grass and listened to the birds sing.',
        13:'The garden had so many yummy things to eat! There were sweet red apples, juicy oranges, and crunchy nuts.',
        14:'Adam and Eve took very good care of the garden. They watered the thirsty flowers and helped the plants grow tall.',
        15:'They took care of the animals, too. Eve brushed the soft fur of the deer, and Adam played games with the monkeys.',
        16:'Everything in the garden was perfect. The air smelled like sweet flowers, and the water was always cool and clear.',
        17:'One day, they found a giant tree with the biggest, shiniest fruit they had ever seen.',
        18:'They sat under the tree and talked about all the wonderful things God had made.',
        19:'The animals loved to sleep near Adam and Eve. At night, the garden was very quiet and peaceful.',
        20:'God\'s gentle voice came to them in the cool of the evening. "Are you happy in the garden?" God asked.',
        21:'"Yes, God!" they answered. "We love the animals, the trees, and each other. Everything is wonderful!"',
        22:'God was very happy with His creation. He saw that everything He had made was very, very good.',
        23:'Every day was a new adventure in the garden. There was always a new flower to find or a new bird song to hear.',
        24:'Adam and Eve knew they were very loved. They would always live in God\'s beautiful garden.',
    }
    c=canvas.Canvas(O,pagesize=(PG,PH))
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12);c.setFillColorRGB(0.1,0.6,0.2)
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
    blurb=("Discover the beautiful Garden of Eden! Adam names the\nanimals, Eve becomes his friend, and together they care\nfor God's wonderful creation in this gentle introduction\nto the very first story in the Bible.\n\nAges 2-6 | StorySprout Press")
    lines=blurb.split('\n');y=PH-115
    for line in lines:
        c.drawCentredString(PG/2,y,line);y-=16
    c.setFont("Helvetica",9);c.setFillColorRGB(0.5,0.5,0.5)
    c.drawCentredString(PG/2,55,"StorySprout Press")
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")
    lis=r"""# Bible Series Book #9: "Adam and Eve's Beautiful Garden" - Product Listing
**Title:** Adam and Eve's Beautiful Garden: A Bible Story for Little Ones - The Story of Creation for Children Ages 2-6
**Series:** Bible Adventures (Book 9)
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99
### Amazon Bullet Points
1. **GENTLE CREATION STORY** - A warm, child-friendly retelling of Adam, Eve, and the Garden of Eden, celebrating God's beautiful world.
2. **BEAUTIFUL GARDEN ILLUSTRATIONS** - 24 vibrant illustrations of lush gardens, friendly animals, and the very first people.
3. **TEACHES THANKFULNESS** - A gentle lesson about appreciating nature, caring for animals, and being grateful.
4. **LOVELY CHARACTERS** - Meet Adam, Eve, and friendly animals including lions, giraffes, monkeys, and deer.
5. **NAMING THE ANIMALS** - Fun, interactive element as children discover how each animal got its name.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **PERFECT INTRODUCTION** - A beautiful first Bible story that introduces children to God's love and creation.
### Amazon Backend Keywords
children's bible story, adam and eve, bible story for toddlers, christian children's book, creation story, garden of eden, preschool bible story, bible adventures series, animals naming, sunday school book, old testament for kids, christian toddler book, god's creation, nature appreciation book, first people story
### Etsy Listing
**Title:** Adam and Eve's Beautiful Garden - Printable Bible Storybook PDF | Creation Story for Kids | Christian Children's Book Digital Download
**Tags:** bible storybook, printable book for kids, adam and eve, christian kids book, sunday school, preschool bible, creation story, digital download, faith based, toddler bible, homeschool resource, garden of eden
**Description:** A gentle retelling of Adam and Eve in the Garden of Eden. Adam names the animals, Eve becomes his friend, and together they care for God's beautiful creation! 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-bible9-storybook.md','w') as f:f.write(lis)
    print("  -> /home/team/shared/listings-bible9-storybook.md")
    print("BIBLE BOOK #9 COMPLETE!")
if __name__=='__main__':go()