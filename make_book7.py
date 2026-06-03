#!/usr/bin/env python3
"""Build Book #7: Stella the Star Who Found Friends."""
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

TMP = '/home/team/shared/.tmp_build'
os.makedirs(TMP, exist_ok=True)

def place_image(c, img_path, w, h):
    if not img_path or not os.path.exists(img_path):
        c.setFillColorRGB(1, 1, 1);
        c.rect(0, 0, w, h, fill=1, stroke=0); return
    img = Image.open(img_path).convert('RGB')
    img = img.resize((int(w), int(h)), Image.LANCZOS)
    tp = os.path.join(TMP, os.path.basename(img_path).replace('.png', '.jpg'))
    img.save(tp, 'JPEG', quality=95)
    c.drawImage(tp, 0, 0, width=w, height=h)

def go():
    print("BOOK #7: Stella the Star Who Found Friends")
    T=8.5*inch; B=0.125*inch; PW=T+2*B; PH=T+2*B
    D='/home/team/shared/stella-star-illustrations'
    O='/home/team/shared/book7-stella-star-kdp.pdf'
    txt={
        2:'High above the world, where the air is thin and the night is deep, lived Stella. She was a tiny star in a very big sky.',
        3:'Stella was beautiful. She was sparkly. But Stella was also very, very lonely.',
        4:'"I wish I had someone to play with," Stella whispered. Her light flickered low.',
        5:'Suddenly, a bright blue streak zipped past her. *WHOOSH!*',
        6:'"Hello there!" a boisterous voice called out. It was Comet Carl. "Why the long face, little star?"',
        7:'"I\'m lonely, Carl," Stella said. "The sky is so big, and I\'m so small."',
        8:'"The sky is only big if you look at the empty spots!" Carl laughed. "Follow me! I\'ll show you something amazing!"',
        9:'Stella tried to move, but she was rooted in her spot. "I can\'t!" she cried. "Stars stay still!"',
        10:'Carl stopped and sighed. "Ah, I forgot. Well, don\'t you worry. If you can\'t come to the party, I\'ll send some guests your way!"',
        11:'Stella waited. The night grew darker. She felt even lonelier than before.',
        12:'Then, she heard a soft, silvery hum. A warm light began to grow around her.',
        13:'"Hello, little Stella," a kind voice said. It was Moona the Moon. She looked like a giant, glowing cradle.',
        14:'"Moona!" Stella gasped. "Am I all alone up here?"',
        15:'Moona chuckled softly. "Oh, Stella. Look closer. Not at the dark, but at the light."',
        16:'Moona breathed a gentle mist of stardust across the sky.',
        17:'As the mist cleared, Stella saw them. Thousands and thousands of stars!',
        18:'Right next to her were two little stars. "Hi!" said one. "Hello!" said the other. It was the Twinkle Twins.',
        19:'"We\'ve been here all along," the first twin said. "We were just waiting for you to say hello."',
        20:'Stella realized that the sky wasn\'t empty at all. It was a giant blanket of friends!',
        21:'Comet Carl zipped by again. "See? I told you!" he yelled. He threw a handful of blue glitter at them.',
        22:'Stella began to pulse her light. *Glow... dim... glow!*',
        23:'All the other stars began to pulse with her. The whole sky was twinkling like a beautiful song.',
        24:'Stella wasn\'t lonely anymore. She knew that even a tiny star is part of a very big, very bright family.',
    }
    c=canvas.Canvas(O,pagesize=(PW,PH))
    place_image(c,D+'/front-cover.png',PW,PH)
    c.setFillColorRGB(0.95,0.85,0.3)
    c.setFont("Helvetica-Bold",34)
    c.drawCentredString(PW/2,PH-90,"Stella the Star")
    c.setFont("Helvetica-Bold",26)
    c.drawCentredString(PW/2,PH-128,"Who Found Friends")
    c.setFont("Helvetica",14)
    c.setFillColorRGB(0.7,0.7,0.9)
    c.drawCentredString(PW/2,PH-168,"A StorySprout Press Book")
    c.showPage()
    for pn in range(1,25):
        place_image(c,D+f'/page-{pn:02d}.png',PW,PH)
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
    place_image(c,D+'/back-cover.png',PW,PH)
    c.setFillColorRGB(0.2,0.2,0.2)
    c.setFont("Helvetica-Bold",18)
    c.drawCentredString(PW/2,PH-90,"About the Story")
    blurb=("Stella is a tiny star in a vast sky, and she feels very\n"
           "lonely. With help from Comet Carl, Moona, and the\n"
           "Twinkle Twins, Stella discovers the sky is full of\n"
           "friends she never knew she had!\n\nAges 2-6 | StorySprout Press")
    c.setFont("Helvetica",12)
    lines=blurb.split('\n'); y=PH-125
    for line in lines:
        c.drawCentredString(PW/2,y,line); y-=18
    c.setFont("Helvetica",10)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawCentredString(PW/2,60,"StorySprout Press")
    c.showPage(); c.save()
    sz=os.path.getsize(O)/(1024*1024)
    print(f"  -> {O} ({sz:.1f} MB)")
    # Listing
    lis=r"""# Book #7: "Stella the Star Who Found Friends" - Product Listing

## Amazon KDP Product Details
**Title:** Stella the Star Who Found Friends: A Heartwarming Children's Picture Book About Loneliness, Friendship, and Belonging
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99

### Amazon Bullet Points
1. **HEARTWARMING FRIENDSHIP STORY** - Stella is a lonely little star in a vast sky. With help from Comet Carl, Moona, and the Twinkle Twins, she discovers friends are closer than she thinks.
2. **BEAUTIFUL NIGHT SKY ILLUSTRATIONS** - 24 stunning full-color illustrations of starry skies, glowing moons, and sparkling comets.
3. **TEACHES CONNECTION & BELONGING** - A gentle lesson about reaching out, making friends, and realizing you're never truly alone.
4. **LOVELY CHARACTERS** - Meet Stella, Moona the crescent moon, Comet Carl with his blue tail, and the giggly Twinkle Twins.
5. **COMFORTING BEDTIME READ** - The soft, warm glow theme makes this perfect for bedtime reading and soothing nighttime fears.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **SOCIAL-EMOTIONAL LEARNING** - Helps children understand and navigate feelings of loneliness in a gentle, reassuring way.

### Amazon Backend Keywords
children's picture book, star book for kids, bedtime story about friendship, night sky book, lonely child book, making friends children's book, moon and stars story, space book for toddlers, social emotional learning, bedtime fears comfort book, preschool read aloud, gift for shy child, friendship tale, twinkle star book, stella book

### Etsy Listing
**Title:** Stella the Star Who Found Friends - Printable Children's Storybook PDF | Bedtime Story About Friendship | Night Sky Digital Download
**Tags:** childrens storybook, printable book for kids, bedtime story pdf, star book, night sky kids book, friendship story, making friends, digital download, preschool book, space for kids, comfort book, homeschool resource
**Description:** Stella is a tiny star in a vast, lonely sky. But when Comet Carl, Moona, and the Twinkle Twins show her that friends are all around, she discovers the sky is a giant blanket of family! 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-book7-storybook.md','w') as f:
        f.write(lis)
    print("  -> /home/team/shared/listings-book7-storybook.md")
    print("BOOK #7 COMPLETE!")

if __name__=='__main__': go()