#!/usr/bin/env python3
"""Build Book #8: The Curious Little Penguin."""
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

TMP = '/home/team/shared/.tmp_build'; os.makedirs(TMP, exist_ok=True)
def plc(c, p, w, h):
    if not p or not os.path.exists(p):
        c.setFillColorRGB(1,1,1); c.rect(0,0,w,h,fill=1,stroke=0); return
    i=Image.open(p).convert('RGB'); i=i.resize((int(w),int(h)),Image.LANCZOS)
    t=os.path.join(TMP,os.path.basename(p).replace('.png','.jpg')); i.save(t,'JPEG',quality=95); c.drawImage(t,0,0,w,h)

def go():
    print("BOOK #8: The Curious Little Penguin")
    T=8.5*inch; B=0.125*inch; PW=T+2*B; PH=T+2*B
    D='/home/team/shared/curious-penguin-illustrations'; O='/home/team/shared/book8-curious-penguin-kdp.pdf'
    txt={
        2:'In the middle of the Great White North, where the ice is thick and the wind whistles tunes, lived Pip.',
        3:'Pip was a small penguin with a very big question for everything he saw.',
        4:'"Why is the snow white?" Pip asked. "Why is the water cold?"',
        5:'Waddles would laugh. "That\'s just how the world is, Pip. Stay close to the colony, it\'s safe here."',
        6:'But Pip\'s curiosity was like a little engine. He wanted to see what was beyond the next snowy hill.',
        7:'He waddled up the hill. *Slip, slide, thump!* He tumbled down the other side into a valley of blue ice.',
        8:'"Oh my!" Pip gasped. The ice here wasn\'t white. It was bright, glowing blue!',
        9:'"It\'s blue because it\'s very old," said a voice. Pip looked up and saw Professor Puffin.',
        10:'"Is the whole world blue?" Pip asked. "Not at all!" the Professor chirped. "The world is as many colors as a rainbow!"',
        11:'Pip was amazed. He wanted to see more colors! He thanked the Professor and waddled on.',
        12:'He came to a frozen slide. *Whoosh!* Squiggles the Seal zipped past him on his belly.',
        13:'"Want to race?" Squiggles barked. "I... I\'m not supposed to go fast," Pip said. "But I am curious!"',
        14:'Pip lay on his belly. *One, two, three... GO!*',
        15:'They slid over the ice and under the frozen arches. Pip saw the silver ocean and the golden sun.',
        16:'But then, the wind began to growl. A big, grey cloud covered the sun.',
        17:'"A storm is coming!" Squiggles said. "I have to go back to my mama. You should too, Pip!"',
        18:'Pip looked around. The snowy hill looked very different in the dark. He didn\'t know which way was home.',
        19:'"Waddles? Mama? Papa?" Pip called out. But the wind just whistled back.',
        20:'Pip remembered what Professor Puffin said. "The stars can show the way when the sun is gone."',
        21:'He saw the brightest star. It was right over the hill where the colony lived!',
        22:'*Waddle, trip, waddle!* Pip pushed through the snow. He was tired, but he kept going.',
        23:'At the top, he saw a line of penguins. Waddles was at the front, calling his name.',
        24:'"I found so many colors, Waddles!" Pip chirped as he was hugged. "The world is big, but I\'m glad I\'m home."',
    }
    c=canvas.Canvas(O,pagesize=(PW,PH))
    plc(c,D+'/front-cover.png',PW,PH)
    c.setFillColorRGB(0.1,0.3,0.7)
    c.setFont("Helvetica-Bold",36)
    c.drawCentredString(PW/2,PH-90,"The Curious")
    c.drawCentredString(PW/2,PH-135,"Little Penguin")
    c.setFont("Helvetica",14)
    c.setFillColorRGB(0.7,0.8,0.9)
    c.drawCentredString(PW/2,PH-175,"A StorySprout Press Book")
    c.showPage()
    for pn in range(1,25):
        plc(c,D+f'/page-{pn:02d}.png',PW,PH)
        if pn in txt:
            t=txt[pn]
            c.setFillColorRGB(1,1,1,alpha=0.75)
            c.roundRect(B+10,B+10,T-20,80,8,fill=1,stroke=0)
            c.setFillColorRGB(0.1,0.1,0.15)
            c.setFont("Helvetica",15)
            lines=t.split('\n'); y=B+65
            for line in lines:
                c.drawString(B+25,y,line); y-=20
        if pn>1:
            c.setFont("Helvetica",10)
            c.setFillColorRGB(0.5,0.5,0.5)
            c.drawCentredString(B+T/2,B+12,str(pn))
        c.showPage()
    plc(c,D+'/back-cover.png',PW,PH)
    c.setFillColorRGB(0.2,0.2,0.2)
    c.setFont("Helvetica-Bold",18)
    c.drawCentredString(PW/2,PH-90,"About the Story")
    blurb=("Pip the penguin has a question for everything he sees!\n"
           "When his curiosity leads him away from the safety of\n"
           "the colony, Pip must find his way home through a\n"
           "snowstorm. A tale of adventure, nature, and home.\n\nAges 2-6 | StorySprout Press")
    c.setFont("Helvetica",12)
    lines=blurb.split('\n'); y=PH-125
    for line in lines:
        c.drawCentredString(PW/2,y,line); y-=18
    c.setFont("Helvetica",10)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawCentredString(PW/2,60,"StorySprout Press")
    c.showPage(); c.save()
    sz=os.path.getsize(O)/(1024*1024); print(f"  -> {O} ({sz:.1f} MB)")
    lis=r"""# Book #8: "The Curious Little Penguin" - Product Listing

## Amazon KDP Product Details
**Title:** The Curious Little Penguin: A Charming Children's Picture Book About Curiosity, Adventure, and Finding Your Way Home
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99

### Amazon Bullet Points
1. **CURIOUS ADVENTURE STORY** - Pip the penguin has a question for everything! When his curiosity leads him beyond the colony, he discovers a world of color and adventure.
2. **BEAUTIFUL ANTARCTIC ILLUSTRATIONS** - 24 stunning full-color illustrations of icy landscapes, blue ice caves, and playful seals.
3. **TEACHES CURIOSITY & SAFETY** - A gentle balance between exploring the world and the importance of finding your way home.
4. **LOVELY CHARACTERS** - Meet Pip the curious penguin, Waddles the loving parent, Professor Puffin with his spectacles, and Squiggles the playful seal.
5. **NATURE & SCIENCE THEME** - Introduces children to Antarctic animals, ice formations, and using stars for navigation.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **COMFORTING MESSAGE** - A reassuring story about getting lost and finding your way home to loving family.

### Amazon Backend Keywords
children's picture book, penguin book for kids, curiosity children's book, antarctic story for toddlers, polar animals book, adventure picture book, baby penguin story, bedtime story about exploring, ice and snow book, animal friends tale, preschool nature book, getting lost story, finding home book, puffin character, seal kids book

### Etsy Listing
**Title:** The Curious Little Penguin - Printable Children's Storybook PDF | Penguin Bedtime Story | Arctic Animal Picture Book Digital Download
**Tags:** childrens storybook, printable book for kids, bedtime story pdf, penguin book, arctic animals, curiosity story, adventure book, digital download, preschool book, nature kids book, polar animals, homeschool resource
**Description:** Pip the penguin is full of questions! When his curiosity leads him away from the colony, he discovers blue ice caves, a puffin professor, and a playful seal. 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-book8-storybook.md','w') as f: f.write(lis)
    print("  -> /home/team/shared/listings-book8-storybook.md")
    print("BOOK #8 COMPLETE!")
if __name__=='__main__': go()