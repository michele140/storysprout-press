#!/usr/bin/env python3
"""Build ALL deliverables for Book #2: The Brave Little Seed."""
import os, sys, zipfile, tempfile, shutil
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

# ===========================
# STORYBOOK PDF (8.5"x8.5")
# ===========================
def make_storybook():
    print("=" * 50)
    print("BOOK #2: Building Brave Little Seed storybook PDF...")
    print("=" * 50)
    
    TRIM = 8.5 * inch
    BLEED = 0.125 * inch
    PW = TRIM + 2 * BLEED
    PH = TRIM + 2 * BLEED
    
    IMG_DIR = '/home/team/shared/brave-little-seed-illustrations'
    OUT = '/home/team/shared/book2-brave-little-seed-kdp.pdf'
    
    texts = {
        2: 'Once there was a tiny seed named Pip. Pip lived in a cozy paper packet with all his friends.',
        3: 'Pip was small. Pip was brown. And Pip was very, very worried.',
        4: '"It\'s time to grow!" the farmer said. He picked up Pip with his big, gentle hand.',
        5: '"Wait!" Pip cried. "The world is too big! I\'m just a little seed!"',
        6: '"Don\'t be afraid, little one," a soft voice whispered. It was Mama Sunflower, leaning down from the sky.',
        7: 'The farmer tucked Pip into a little hole in the soft, brown earth.',
        8: 'It was very dark. It was very quiet. Pip missed his cozy packet.',
        9: '*Wiggle, waggle, wiggle!* Suddenly, a friendly face popped through the dirt. It was Wiggly Worm.',
        10: '"Don\'t worry, Pip!" Wiggly said. "The soil isn\'t scary. It\'s just a cozy blanket to help you grow."',
        11: 'Pip started to feel a little better. But he still felt very small and very stuck.',
        12: 'Then, a happy song filled the air. *Plink! Plank! Plunk!* Raindrop Rita landed right on Pip\'s head.',
        13: '"Drink up, Pip!" Rita sang. "The rain brings strength! The rain brings magic!"',
        14: 'Pip felt a strange tickle in his tummy. He felt warmer. He felt stronger.',
        15: '"I\'m doing it!" Pip whispered. He stretched his tiny green arms as high as he could.',
        16: '*Pop!* Pip\'s head poked through the ground. The world was bright and beautiful!',
        17: '"You did it, Pip!" Mama Sunflower cheered. The sun felt warm and kind on his new green leaves.',
        18: 'Every day, the sun shone and the rain sang. And every day, Pip grew a little bit taller.',
        19: 'Pip wasn\'t afraid of the wind anymore. He loved to dance with the breeze.',
        20: 'He wasn\'t afraid of the dark anymore. He knew the stars were watching over him.',
        21: 'Soon, Pip had a big, round head of his own. It was filled with tiny, golden buds.',
        22: 'One morning, *burst!* Pip opened up. He was a bright, beautiful sunflower!',
        23: '"Growing is a big adventure," Pip said to a tiny seed on the ground. "And you are going to be so brave!"',
        24: 'Pip stood tall and proud in the garden. He was the bravest little seed of all.',
    }
    
    c = canvas.Canvas(OUT, pagesize=(PW, PH))
    
    # Front cover
    place_image(c, os.path.join(IMG_DIR, 'front-cover.png'), PW, PH)
    c.setFillColorRGB(0.95, 0.85, 0.5)
    c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(PW/2, PH - 100, "The Brave")
    c.drawCentredString(PW/2, PH - 145, "Little Seed")
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.2, 0.5, 0.2)
    c.drawCentredString(PW/2, PH - 180, "A StorySprout Press Book")
    c.showPage()
    
    # Interior pages
    for pn in range(1, 25):
        place_image(c, os.path.join(IMG_DIR, f'page-{pn:02d}.png'), PW, PH)
        if pn in texts:
            t = texts[pn]
            # Semi-transparent text background
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
    blurb = ("Meet Pip, a tiny seed who is afraid to leave his cozy packet.\n"
             "With the help of Mama Sunflower, Wiggly Worm, and Raindrop\n"
             "Rita, Pip learns that growing is a big adventure!\n\n"
             "A heartfelt tale about courage, growth, and the beauty of\n"
             "becoming who you were meant to be.\n\n"
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

# ===========================
# PRODUCT LISTINGS
# ===========================
def make_listings():
    print("=" * 50)
    print("BOOK #2: Creating listings...")
    print("=" * 50)
    
    story = r"""# Book #2: "The Brave Little Seed" - Product Listings

## Amazon KDP Product Details

**Title:** The Brave Little Seed: A Heartwarming Children's Picture Book About Courage and Growing Up
**Series:** StorySprout Press Collection (Book 2)
**Trim Size:** 8.5" x 8.5" square
**Page Count:** 26 pages (including cover)
**Age Range:** 2-6 years
**Price (Print):** $9.99
**Price (Digital):** $4.99

### Amazon Bullet Points
1. **HEARTWARMING GROWTH STORY** - Follow Pip the tiny seed on his journey from a cozy packet to a beautiful sunflower, learning that courage comes from within.
2. **BEAUTIFUL GARDEN ILLUSTRATIONS** - 24 vibrant, full-color illustrations bring Pip, Mama Sunflower, Wiggly Worm, and Raindrop Rita to life on every page.
3. **TEACHES COURAGE & PERSEVERANCE** - This gentle tale helps children understand that facing fears and trying new things leads to wonderful growth.
4. **PERFECT READ-ALOUD** - Simple, engaging text with fun sound words (*Wiggle, waggle!* *Pop!* *Plink! Plank! Plunk!*) makes this ideal for story time.
5. **NATURE & SCIENCE THEME** - Introduces children to how seeds grow, the role of sun, rain, and soil, and the miracle of plant life.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages designed for little hands.
7. **COMFORTING MESSAGE** - Perfect for children facing new experiences like starting school, moving, or any big change.

### Amazon Backend Keywords (KDP Search Terms)
children's picture book, seed growing book, nature book for kids, bedtime story about courage, preschool garden book, plant life cycle for children, sunflower book for toddlers, overcoming fear kids book, spring picture book, kindergarten read aloud, social emotional learning, garden story for kids, nature and growth, seed to flower book, toddler book about bravery

### Etsy Listing

**Title:** The Brave Little Seed - Printable Children's Storybook PDF | Garden Bedtime Story | Nature Picture Book Digital Download

**Tags:** childrens storybook, printable book for kids, bedtime story pdf, seed growing book, garden theme, nature kids book, courage story, digital download, preschool learning, sunflower book, plant life cycle, homeschool resource

**Description:**
A heartwarming story about courage, growth, and the beauty of becoming who you're meant to be!

Meet Pip, a tiny seed who feels safe in his cozy packet. When it's time to grow, Pip is scared - the world is so big! With help from Mama Sunflower, Wiggly Worm, and Raindrop Rita, Pip discovers that growing is a big adventure.

WHAT'S INCLUDED:
- 24 beautifully illustrated story pages (PDF format)
- Front and back cover
- Print-ready at 8.5" x 8.5"
- Unlimited printing for personal use

PERFECT FOR:
- Bedtime reading with toddlers and preschoolers
- Classroom story time (ages 2-6)
- Homeschooling nature units
- Baby shower and birthday gifts

This is a DIGITAL DOWNLOAD.
"""
    
    with open('/home/team/shared/listings-book2-storybook.md', 'w') as f:
        f.write(story)
    print("  -> /home/team/shared/listings-book2-storybook.md")
    
    bundle = r"""# Book #2: "The Brave Little Seed" - BUNDLE Listing

## Bundle Details

**Bundle Includes:**
1. "The Brave Little Seed" storybook (24 illustrated pages)
2. "The Brave Little Seed's Garden Adventure Activity Book" (24 activity pages - coming soon)

**Age Range:** 2-6 years

**Bundle Pricing:**
- Digital Bundle: $14.99 (save vs buying separately)

### Amazon Bullet Points
1. **COMPLETE PIP THE SEED EXPERIENCE** - Get the heartwarming story plus the companion activity book in one bundle.
2. **READ, PLAY, LEARN** - Start with Pip's inspiring growth story, then reinforce learning through coloring, mazes, tracing, and more.
3. **HOURS OF GARDEN FUN** - Over 50 pages combining story and activities for endless screen-free fun.
4. **DEVELOPS KEY SKILLS** - Builds reading comprehension, fine motor skills, creativity, and nature awareness.
5. **VALUE BUNDLE** - Save money compared to purchasing separately.
6. **PERFECT GIFT SET** - An ideal gift for birthdays, holidays, or any occasion.
7. **CLASSROOM FRIENDLY** - Perfect for preschool and kindergarten nature units.

### Amazon Backend Keywords (KDP Search Terms)
children's book bundle, storybook and activity book set, garden theme kids gift, seed growing bundle, preschool nature set, Pip the seed gift, children's garden gift, homeschool nature curriculum, kids birthday gift, educational gift for toddler

### Etsy Listing

**Title:** The Brave Little Seed BUNDLE - Storybook + Activity Book | Digital Download for Kids | Garden Theme Bedtime Story | Preschool Learning Set

**Tags:** kids book bundle, storybook and activity, digital download bundle, garden theme, toddler gift set, preschool learning bundle, seed growing set, homeschool nature, classroom printable, Pip the seed

**Description:**
The complete Brave Little Seed experience! Save when you purchase both books together.

This bundle includes:
1. The Brave Little Seed - A heartwarming 24-page story about courage and growing up
2. The Brave Little Seed's Garden Adventure Activity Book - 24 pages of coloring, mazes, tracing, and more (available soon!)

Perfect for children ages 2-6, this bundle offers hours of reading and garden-themed fun.

This is a DIGITAL DOWNLOAD.
"""
    
    with open('/home/team/shared/listings-book2-bundle.md', 'w') as f:
        f.write(bundle)
    print("  -> /home/team/shared/listings-book2-bundle.md")

if __name__ == '__main__':
    make_storybook()
    make_listings()
    print()
    print("=" * 50)
    print("BOOK #2 COMPLETE!")
    print("=" * 50)