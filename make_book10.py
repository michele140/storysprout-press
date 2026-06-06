#!/usr/bin/env python3
"""Build Book #10: The Moon Who Wanted to Play."""
import os, textwrap
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

TMP='/home/team/shared/.tmp_build'; os.makedirs(TMP,exist_ok=True)
def plc(c,p,w,h):
    if not p or not os.path.exists(p):
        c.setFillColorRGB(1,1,1);c.rect(0,0,w,h,fill=1,stroke=0);return
    i=Image.open(p).convert('RGB');i=i.resize((int(w),int(h)),Image.LANCZOS)
    t=os.path.join(TMP,os.path.basename(p).replace('.png','.jpg'));i.save(t,'JPEG',quality=95);c.drawImage(t,0,0,w,h)

def go():
    print("BOOK #10: The Moon Who Wanted to Play")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    D='/home/team/shared/moon-illustrations';O='/home/team/shared/book10-moon-kdp.pdf'
    txt={
        2:'Every night, when the world went to sleep, Luna the Moon woke up. She loved her job of lighting the way for owls and dreamers.',
        3:'But Luna had a secret wish. She watched the children playing in the sunshine during the day and wished she could join them.',
        4:'"It looks so much fun down there," Luna sighed. "I want to run in the grass and hear the children laugh."',
        5:'"Why can\'t I play in the daytime?" she asked her friend Twinkle the Star.',
        6:'"Because you\'re the Moon!" Twinkle giggled. "You\'d get a sunburn! Plus, who would watch over the night?"',
        7:'Luna didn\'t care. She waited and waited until the morning light began to peek over the hills.',
        8:'*BOOM!* Sol the Sun rose into the sky, big and bright and warm. "Good morning, world!" he cheered.',
        9:'"Sol! Wait!" Luna called out. "Can I stay and play today?"',
        10:'Sol looked at Luna with surprise. "Stay? But Luna, you need your rest. The night is long and quiet."',
        11:'"Please, Sol! Just for a little while. I want to see the flowers open and the birds sing."',
        12:'Sol thought for a moment. "Very well, Luna. You may stay. But remember, the day is very different from the night."',
        13:'Luna was so happy! She stayed in the sky as the children came out to play. She saw Milly running with her kite.',
        14:'"Look! The Moon is still there!" Milly shouted, pointing up. "Hello, Moon!"',
        15:'But as the day grew hotter, Luna began to feel very tired. The sun was so bright, it made her silvery light hard to see.',
        16:'She tried to hear the children\'s laughter, but the world was so noisy! Cars honked, dogs barked, and lawnmowers whirred.',
        17:'"It\'s so... busy," Luna whispered. She missed the quiet whisper of the wind in the trees at night.',
        18:'The flowers were beautiful, but they didn\'t glow like the moonflowers she knew. Everything was so bright, it hurt her eyes.',
        19:'"Sol was right," Luna sighed. "The day is wonderful, but I don\'t belong here. I\'m a creature of the quiet and the stars."',
        20:'As the sun began to set, Sol looked at Luna. "Are you ready to wake up the night, Luna?"',
        21:'"Yes, Sol," Luna said, feeling her strength return as the sky grew dark. "The night is waiting for me."',
        22:'She saw Milly getting ready for bed. Milly looked up and waved one last time. "Goodnight, Moon! I\'m glad you\'re back."',
        23:'Luna smiled her dreamy smile. She realized that she didn\'t need to play in the day to be special.',
        24:'She had the best job in the world — watching over the dreams of children and lighting the way through the night.',
    }
    c=canvas.Canvas(O,pagesize=(PG,PH))
    # Front cover - no duplicate title
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12)
    c.setFillColorRGB(0.3,0.3,0.6)
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
    # Back cover
    plc(c,D+'/back-cover.png',PG,PH)
    c.setFillColorRGB(0.2,0.2,0.2)
    c.setFont("Helvetica-Bold",16)
    c.drawCentredString(PG/2,PH-85,"About the Story")
    c.setFont("Helvetica",11)
    blurb=("Luna the Moon loves her job lighting the night sky, but\n"
           "she dreams of playing in the sunshine. When Sol the Sun\n"
           "lets her stay for a day, Luna discovers that the day is\n"
           "wonderful — but the night is where she truly belongs.\n\nAges 2-6 | StorySprout Press")
    lines=blurb.split('\n');y=PH-115
    for line in lines:
        c.drawCentredString(PG/2,y,line);y-=16
    c.setFont("Helvetica",9)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawCentredString(PG/2,55,"StorySprout Press")
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")
    lis=r"""# Book #10: "The Moon Who Wanted to Play" - Product Listing

## Amazon KDP Product Details
**Title:** The Moon Who Wanted to Play: A Heartwarming Children's Picture Book About Discovering Where You Belong
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99

### Amazon Bullet Points
1. **HEARTWARMING STORY** - Luna the Moon loves her job but dreams of playing in the daytime. When Sol lets her stay, she discovers the night is where she truly belongs.
2. **BEAUTIFUL DAY-AND-NIGHT ILLUSTRATIONS** - 24 stunning full-color illustrations capturing both the quiet beauty of night and the vibrant energy of daytime.
3. **TEACHES SELF-ACCEPTANCE** - A gentle lesson about appreciating your unique gifts and discovering where you truly belong.
4. **LOVELY CHARACTERS** - Meet Luna the crescent moon, Sol the warm sun, Milly the curious girl, and Twinkle the cheeky star.
5. **DAY AND NIGHT THEME** - Introduces children to the cycle of day and night, the sun and moon's roles, and the beauty of both.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **COMFORTING BEDTIME READ** - The perfect bedtime story that celebrates the magic of nighttime and the comfort of being yourself.

### Amazon Backend Keywords
children's picture book, moon book for kids, sun and moon story, bedtime story, day and night book, self-acceptance children's book, crescent moon tale, star book for toddlers, nature cycle book, kid who loves the moon, preschool astronomy, bedtime fears comfort book, girl and moon story, Sol and Luna book, discovering strengths kids book

### Etsy Listing
**Title:** The Moon Who Wanted to Play - Printable Children's Storybook PDF | Bedtime Story About Day and Night | Moon Picture Book Digital Download
**Tags:** childrens storybook, printable book for kids, bedtime story pdf, moon book, sun and moon story, day and night, self-acceptance, digital download, preschool book, nature kids book, space for kids, homeschool resource
**Description:** Luna the Moon loves her job lighting the night sky. But she dreams of playing in the sunshine! When Sol lets her stay for a day, Luna discovers that the night is where she truly belongs. 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-book10-storybook.md','w') as f:f.write(lis)
    print("  -> /home/team/shared/listings-book10-storybook.md")
    print("BOOK #10 COMPLETE! SERIES 1 FINALE!")
if __name__=='__main__':go()