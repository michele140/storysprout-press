#!/usr/bin/env python3
"""Build ALL deliverables for Book #3: Daisy the Dancing Duck."""
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

TMP = '/home/team/shared/.tmp_build'
os.makedirs(TMP, exist_ok=True)

def place_image(c, img_path, w, h):
    if not img_path or not os.path.exists(img_path):
        c.setFillColorRGB(1, 1, 1)
        c.rect(0, 0, w, h, fill=1, stroke=0)
        return
    img = Image.open(img_path).convert('RGB')
    img = img.resize((int(w), int(h)), Image.LANCZOS)
    tmp_path = os.path.join(TMP, os.path.basename(img_path).replace('.png', '.jpg'))
    img.save(tmp_path, 'JPEG', quality=95)
    c.drawImage(tmp_path, 0, 0, width=w, height=h)

def make_storybook():
    print("=" * 50)
    print("BOOK #3: Building Daisy the Dancing Duck storybook PDF...")
    print("=" * 50)

    TRIM = 8.5 * inch
    BLEED = 0.125 * inch
    PW = TRIM + 2 * BLEED
    PH = TRIM + 2 * BLEED

    IMG_DIR = '/home/team/shared/daisy-dancing-duck-illustrations'
    OUT = '/home/team/shared/book3-daisy-dancing-duck-kdp.pdf'

    texts = {
        2: 'Down at the Willow Pond, the morning started just like any other.',
        3: 'All the ducks lined up for their morning walk. *Waddle, waddle, waddle.*',
        4: 'But Daisy didn\'t want to waddle. Daisy had a secret. In her heart, she wanted to dance!',
        5: 'While the others went *left, right, left*, Daisy went *tap, tap, twirl!*',
        6: '"Daisy!" the big ducks quacked. "Ducks do not twirl. Ducks waddle!"',
        7: 'Daisy tried to be a good duck. She tried to waddle just like everyone else.',
        8: 'But it was very hard. Her feet felt like they were full of bouncy springs!',
        9: '"I\'m just not a good waddler," Daisy sighed. She sat under the old oak tree, feeling very droopy.',
        10: '"Whoo-whoo is looking so sad?" asked a voice from above. It was Oliver the Owl.',
        11: '"I want to dance, Oliver," Daisy said. "But ducks are supposed to waddle."',
        12: 'Oliver adjusted his glasses. "The pond is big enough for many rhythms, Daisy. Why hide your spark?"',
        13: 'Puddles arrived and sat next to Daisy. "I like your dancing," he whispered. "It makes me want to wiggle!"',
        14: 'Just then, they heard a sound from the reeds. *Ribbit-hop! Ribbit-rock!*',
        15: '"We need a star for our show!" the lead frog croaked. "Will you dance for us, Daisy?"',
        16: 'Daisy looked at Oliver. She looked at Puddles. Then, she stood up and took a deep breath.',
        17: 'The Frog Choir began to play a groovy, lily-pad beat.',
        18: 'Daisy started slow. *Shuffle, shuffle, flap!*',
        19: 'Then she went fast! *Spin, spin, leap!* She was dancing like a golden sunbeam.',
        20: 'Puddles couldn\'t help it. He started to wiggle his tail. *Shake, shake, shake!*',
        21: 'The other ducks came to see what the noise was about. They had never seen anything like it!',
        22: '"Look at Daisy!" cried a duckling. "She\'s beautiful!"',
        23: 'Soon, the whole pond was moving. Some waddled to the beat, and some found a brand new dance.',
        24: 'Daisy led the way, dancing to her own rhythm. She was a duck, and she was a dancer, too!',
    }

    c = canvas.Canvas(OUT, pagesize=(PW, PH))

    # Front cover
    place_image(c, os.path.join(IMG_DIR, 'front-cover.png'), PW, PH)
    c.setFillColorRGB(1, 0.85, 0.3)
    c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(PW/2, PH - 100, "Daisy the")
    c.drawCentredString(PW/2, PH - 145, "Dancing Duck")
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.9, 0.4, 0.1)
    c.drawCentredString(PW/2, PH - 180, "A StorySprout Press Book")
    c.showPage()

    # Interior pages
    for pn in range(1, 25):
        place_image(c, os.path.join(IMG_DIR, f'page-{pn:02d}.png'), PW, PH)
        if pn in texts:
            t = texts[pn]
            c.setFillColorRGB(1, 1, 1, alpha=0.75)
            c.roundRect(BLEED + 10, BLEED + 10, TRIM - 20, 80, 8, fill=1, stroke=0)
            c.setFillColorRGB(0.1, 0.1, 0.15)
            c.setFont("Helvetica", 15)
            lines = t.split('\n')
            y = BLEED + 65
            for line in lines:
                c.drawString(BLEED + 25, y, line)
                y -= 20
        if pn > 1:
            c.setFont("Helvetica", 10)
            c.setFillColorRGB(0.5, 0.5, 0.5)
            c.drawCentredString(BLEED + TRIM/2, BLEED + 12, str(pn))
        c.showPage()

    # Back cover
    place_image(c, os.path.join(IMG_DIR, 'back-cover.png'), PW, PH)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(PW/2, PH - 90, "About the Story")
    blurb = ("Daisy the duckling loves to dance, but the other ducks say\n"
             "ducks should waddle. With help from Oliver the Owl, Puddles\n"
             "the duck, and the Frog Choir, Daisy learns to embrace her\n"
             "unique rhythm and shine!\n\n"
             "A joyful tale about staying true to yourself and the magic\n"
             "of dancing to your own beat.\n\n"
             "Ages 2-6 | StorySprout Press")
    c.setFont("Helvetica", 12)
    lines = blurb.split('\n')
    y = PH - 125
    for line in lines:
        c.drawCentredString(PW/2, y, line)
        y -= 18
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawCentredString(PW/2, 60, "StorySprout Press")
    c.showPage()
    c.save()

    sz = os.path.getsize(OUT) / (1024*1024)
    print(f"  -> {OUT} ({sz:.1f} MB)")

def make_listings():
    print("=" * 50)
    print("BOOK #3: Creating listings...")
    print("=" * 50)

    story = r"""# Book #3: "Daisy the Dancing Duck" - Product Listing

## Amazon KDP Product Details

**Title:** Daisy the Dancing Duck: A Joyful Children's Picture Book About Being Yourself and Dancing to Your Own Beat
**Series:** StorySprout Press Collection (Book 3)
**Trim Size:** 8.5" x 8.5" square
**Page Count:** 26 pages (including cover)
**Age Range:** 2-6 years
**Price (Print):** $9.99
**Price (Digital):** $4.99

### Amazon Bullet Points
1. **JOYFUL SELF-EXPRESSION STORY** - Daisy the duckling loves to dance, but when the other ducks say she should waddle, she must find the courage to be herself.
2. **BEAUTIFUL POND ILLUSTRATIONS** - 24 vibrant, full-color illustrations bring Daisy, Puddles, Oliver the Owl, and the Frog Choir to life on every page.
3. **TEACHES BEING YOURSELF** - This delightful tale encourages children to embrace their unique talents and not be afraid to stand out.
4. **FUN READ-ALOUD WITH SOUND WORDS** - Playful text with *tap, tap, twirl!*, *Ribbit-hop!*, and *Shake, shake, shake!* makes story time extra engaging.
5. **MUSIC & DANCE THEME** - Perfect for little dancers and music lovers, featuring a frog choir with tiny instruments.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages designed for little hands.
7. **EMPOWERING MESSAGE** - A heartwarming reminder that being different is something to celebrate, not hide.

### Amazon Backend Keywords (KDP Search Terms)
children's picture book, duck book for kids, dancing story for toddlers, being yourself children's book, farm animal story, pond life for kids, preschool dance book, individuality kids book, bedtime story about confidence, duckling picture book, animal friendship stories, read aloud books preschool, social emotional learning, following your dreams, toddler book about being unique

### Etsy Listing

**Title:** Daisy the Dancing Duck - Printable Children's Storybook PDF | Duck Bedtime Story | Dance Picture Book Digital Download

**Tags:** childrens storybook, printable book for kids, bedtime story pdf, duck book for toddlers, dance story for kids, pond animals, being yourself, confidence book, digital download kids book, preschool story, homeschool resource, friendship tale

**Description:**
A joyful tale about dancing to your own beat!

Down at Willow Pond, all the ducks waddle in a line. But Daisy doesn't want to waddle - she wants to dance! With help from Oliver the Owl, Puddles the duck, and the Frog Choir, Daisy discovers that the best rhythm is the one that comes from your heart.

WHAT'S INCLUDED:
- 24 beautifully illustrated story pages (PDF format)
- Front and back cover
- Print-ready at 8.5" x 8.5"
- Unlimited printing for personal use

PERFECT FOR:
- Bedtime reading with toddlers and preschoolers
- Classroom story time (ages 2-6)
- Dance-themed parties and activities
- Baby shower and birthday gifts

This is a DIGITAL DOWNLOAD. No physical product will be shipped.
"""

    with open('/home/team/shared/listings-book3-storybook.md', 'w') as f:
        f.write(story)
    print("  -> /home/team/shared/listings-book3-storybook.md")

if __name__ == '__main__':
    make_storybook()
    make_listings()
    print()
    print("=" * 50)
    print("BOOK #3 COMPLETE!")
    print("=" * 50)