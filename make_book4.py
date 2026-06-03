#!/usr/bin/env python3
"""Build Book #4: Leo the Light-Up Firefly."""
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
    print("BOOK #4: Leo the Light-Up Firefly")
    TRIM = 8.5 * inch; BLEED = 0.125 * inch
    PW = TRIM + 2*BLEED; PH = TRIM + 2*BLEED
    IMG_DIR = '/home/team/shared/leo-firefly-illustrations'
    OUT = '/home/team/shared/book4-leo-firefly-kdp.pdf'
    texts = {
        2: 'When the sun went down over the Whisper Meadow, the magic began.',
        3: '*Blink! Flash! Glow!* All the fireflies started their nighttime dance.',
        4: 'Leo tried as hard as he could. He squeezed his eyes shut. He held his breath.',
        5: 'But Leo didn\'t blink. Leo didn\'t flash. Leo stayed dark.',
        6: '"What\'s wrong, Leo?" asked Luna, zipping down beside him. Her light was as bright as a diamond.',
        7: '"I\'m broken, Luna," Leo whispered. "I don\'t have a light like everyone else."',
        8: 'Bella the Beetle waved an antenna. "Everyone has something special, Leo. Maybe your light is just shy."',
        9: '"Let\'s ask Grandfather Glow," Luna suggested. They flew toward the Great Mushroom.',
        10: 'Grandfather Glow sat on top of the tallest mushroom. He listened to Leo\'s story.',
        11: '"A light that flashes is for finding friends," the old firefly said. "But there are many kinds of light in this world."',
        12: 'Leo still felt sad. As they flew home, they heard a tiny, shivering sound.',
        13: 'It was Barnaby the Baby Bunny. He was lost in the thorns and very scared.',
        14: '"We\'ll help you!" cried the other fireflies. They flew into the bushes, flashing their bright lights.',
        15: '*Flash! Flash! Flash!* But the light was too fast. It made the shadows jump, and Barnaby hid his eyes.',
        16: '"Stop!" Leo cried. "You\'re scaring him!" Leo landed right in front of the bunny.',
        17: 'Leo didn\'t try to flash. Instead, he thought about a warm, cozy campfire. He started to hum a soft tune.',
        18: 'Slowly, Leo\'s tail began to shine. It wasn\'t a flash. It was a steady, warm, golden glow.',
        19: 'It was like a tiny nightlight. Barnaby the Bunny stopped shivering. He looked at Leo and felt safe.',
        20: '"Follow me," Leo said gently. He stayed close to the ground, lighting the way through the grass.',
        21: 'Bella the Beetle helped move the leaves. "Go this way, Barnaby!" she called.',
        22: 'Soon, they found the bunny\'s burrow. His mother was waiting for him.',
        23: '"Leo\'s light stayed on!" Luna cheered. "He has a lantern-light!"',
        24: 'Leo felt a warm glow in his heart. He wasn\'t broken at all. He had a special light that could save the day.',
    }
    c = canvas.Canvas(OUT, pagesize=(PW, PH))
    place_image(c, os.path.join(IMG_DIR, 'front-cover.png'), PW, PH)
    c.setFillColorRGB(0.95, 0.9, 0.2)
    c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(PW/2, PH - 100, "Leo the")
    c.drawCentredString(PW/2, PH - 145, "Light-Up Firefly")
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.5, 0.3, 0.0)
    c.drawCentredString(PW/2, PH - 180, "A StorySprout Press Book")
    c.showPage()
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
                c.drawString(BLEED + 25, y, line); y -= 20
        if pn > 1:
            c.setFont("Helvetica", 10)
            c.setFillColorRGB(0.5, 0.5, 0.5)
            c.drawCentredString(BLEED + TRIM/2, BLEED + 12, str(pn))
        c.showPage()
    place_image(c, os.path.join(IMG_DIR, 'back-cover.png'), PW, PH)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(PW/2, PH - 90, "About the Story")
    blurb = ("Leo the firefly can't flash like his friends. Feeling broken,\n"
             "he learns that his gentle, steady glow is exactly what's\n"
             "needed when a lost bunny needs help.\n\n"
             "A heartwarming story about finding your unique light.\n\n"
             "Ages 2-6 | StorySprout Press")
    c.setFont("Helvetica", 12)
    lines = blurb.split('\n'); y = PH - 125
    for line in lines:
        c.drawCentredString(PW/2, y, line); y -= 18
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawCentredString(PW/2, 60, "StorySprout Press")
    c.showPage()
    c.save()
    sz = os.path.getsize(OUT) / (1024*1024)
    print(f"  -> {OUT} ({sz:.1f} MB)")

def make_listings():
    listing = r"""# Book #4: "Leo the Light-Up Firefly" - Product Listing

## Amazon KDP Product Details
**Title:** Leo the Light-Up Firefly: A Heartwarming Children's Picture Book About Finding Your Unique Gift
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99

### Amazon Bullet Points
1. **HEARTWARMING STORY** - Leo the firefly can't flash like his friends, but discovers his gentle, steady glow is exactly what's needed to save the day.
2. **BEAUTIFUL NIGHTTIME ILLUSTRATIONS** - 24 stunning full-color illustrations of glowing fireflies, moonlit meadows, and starry skies.
3. **TEACHES SELF-ACCEPTANCE** - A gentle lesson about embracing your unique qualities and finding your own special light.
4. **FRIENDSHIP & HELPING OTHERS** - Leo's kindness and perseverance show children the power of helping those in need.
5. **NATURE & SCIENCE THEME** - Introduces children to fireflies, meadows, and nocturnal animals in a charming story context.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **COMFORTING BEDTIME READ** - The soft, warm glow theme makes this perfect for bedtime reading.

### Amazon Backend Keywords
children's picture book, firefly book for kids, bedtime story, insect book for toddlers, being different children's book, nighttime story, glow in the dark book, self-esteem kids book, meadow animals, preschool nature book, unique gift children's book, read aloud ages 2-6, baby shower book gift, kindness story, friend helping friend

### Etsy Listing
**Title:** Leo the Light-Up Firefly - Printable Children's Storybook PDF | Firefly Bedtime Story | Nighttime Nature Picture Book Digital Download
**Tags:** childrens storybook, printable book for kids, bedtime story pdf, firefly kids book, insect story, nature kids book, being yourself, digital download, preschool learning, glow story, kindness book, homeschool resource
**Description:** Leo the firefly can't flash. But when a lost bunny needs help, Leo discovers his gentle glow is the most special light of all! 24 beautifully illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-book4-storybook.md', 'w') as f:
        f.write(listing)
    print("  -> /home/team/shared/listings-book4-storybook.md")

if __name__ == '__main__':
    make_storybook()
    make_listings()
    print("BOOK #4 COMPLETE!")