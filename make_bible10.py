#!/usr/bin/env python3
"""Build Bible Book 10: The Lost Little Sheep."""
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
    print("BIBLE #10: The Lost Little Sheep")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    D='/home/team/shared/lost-sheep-illustrations';O='/home/team/shared/bible10-lost-sheep-kdp.pdf'
    txt={
        2:'Once there was a kind Shepherd who had one hundred fluffy white sheep. He knew each of them by name.',
        3:'The Shepherd loved his sheep very much. Every morning, he led them to the greenest grass and the coolest water.',
        4:'Among the sheep was a tiny lamb named Daisy. Daisy was very small and very, very curious.',
        5:'While the other sheep ate their grass, Daisy liked to look at the butterflies and the ladybugs.',
        6:'One afternoon, Daisy saw a beautiful blue bird named Pip. Pip was flying toward a high, rocky hill.',
        7:'"I wonder what is over that hill," Daisy thought. She began to walk away from the other sheep.',
        8:'Daisy walked and walked. She saw new flowers and heard new sounds. She was having so much fun!',
        9:'But soon, the sun began to go down. The sky turned a deep, dark orange.',
        10:'Back at the fold, the Shepherd began to count his sheep. "One... two... three..."',
        11:'"Ninety-eight... ninety-nine..." The Shepherd stopped. "Oh no! One is missing! Where is Daisy?"',
        12:'The Shepherd didn\'t say, "Oh well, I still have ninety-nine." He loved Daisy too much to leave her alone.',
        13:'The Shepherd went back out into the dark fields. "Daisy! Daisy!" he called in his loud, kind voice.',
        14:'He looked behind big rocks. He looked under tall trees. But Daisy was not there.',
        15:'High above, Pip and Peep heard the Shepherd calling. They flew down to help him look.',
        16:'Daisy was cold and scared. She was stuck in some prickly bushes. "Baa! Baa!" she cried softly.',
        17:'The Shepherd heard a tiny sound. He followed the sound all the way to the prickly bushes.',
        18:'"I found you, Daisy!" the Shepherd cried. He gently reached into the bushes to help her.',
        19:'The Shepherd lifted Daisy out of the bushes. He brushed the leaves off her wool and gave her a big hug.',
        20:'Daisy was so happy to see her Shepherd. She felt warm and safe in his strong arms.',
        21:'The Shepherd carried Daisy all the way home. He didn\'t make her walk because she was so tired.',
        22:'When they reached the fold, all the other sheep were happy to see Daisy. "Baa! Baa!" they cheered.',
        23:'The Shepherd told his friends the good news. "My lost sheep is found!" he said with a big smile.',
        24:'The Shepherd knew that every single sheep was important. And Daisy knew she would always be loved.',
    }
    c=canvas.Canvas(O,pagesize=(PG,PH))
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12);c.setFillColorRGB(0.1,0.5,0.2)
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
    blurb=("When Daisy the little lamb wanders off and gets lost,\n"
           "the kind Shepherd leaves his 99 sheep to find her.\n"
           "A heartwarming parable about being loved and never\n"
           "forgotten.\n\nAges 2-6 | StorySprout Press")
    lines=blurb.split('\n');y=PH-115
    for line in lines:
        c.drawCentredString(PG/2,y,line);y-=16
    c.setFont("Helvetica",9);c.setFillColorRGB(0.5,0.5,0.5)
    c.drawCentredString(PG/2,55,"StorySprout Press")
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")
    lis=r"""# Bible Series Book #10: "The Lost Little Sheep" - Product Listing
**Title:** The Lost Little Sheep: A Bible Story for Little Ones - The Parable of the Lost Sheep for Children Ages 2-6
**Series:** Bible Adventures (Book 10)
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99
### Amazon Bullet Points
1. **GENTLE PARABLE STORY** - A warm, child-friendly retelling of Jesus's parable of the lost sheep, celebrating God's unconditional love.
2. **BEAUTIFUL PASTURE ILLUSTRATIONS** - 24 vibrant illustrations of green hills, fluffy sheep, and a kind shepherd searching with a lantern.
3. **TEACHES BEING LOVED** - A comforting message that every child is precious and will always be found.
4. **LOVELY CHARACTERS** - Meet the kind Shepherd, Daisy the curious lamb, the 99 sheep, and Pip and Peep the blue birds.
5. **GENTLE ADVENTURE** - Daisy's curiosity leads her away, but the Shepherd's love brings her home safely.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **PERFECT BEDTIME READ** - A warm, reassuring story for little ones who might feel scared or lost.
### Amazon Backend Keywords
children's bible story, lost sheep parable, bible story for toddlers, christian children's book, good shepherd, jesus parable for kids, preschool bible story, bible adventures series, sheep book for kids, sunday school book, new testament for kids, christian toddler book, being loved story, never forgotten book, shepherd and sheep
### Etsy Listing
**Title:** The Lost Little Sheep - Printable Bible Storybook PDF | Parable of the Lost Sheep for Kids | Christian Children's Book Digital Download
**Tags:** bible storybook, printable book for kids, lost sheep, christian kids book, sunday school, preschool bible, good shepherd, digital download, faith based, toddler bible, homeschool resource, parable
**Description:** A gentle retelling of the parable of the lost sheep. When Daisy wanders off, the kind Shepherd searches until he finds her. A comforting story about being loved and never forgotten. 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-bible10-storybook.md','w') as f:f.write(lis)
    print("  -> /home/team/shared/listings-bible10-storybook.md")
    print("BIBLE BOOK #10 COMPLETE! BIBLE SERIES FINALE!")
if __name__=='__main__':go()