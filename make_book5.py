#!/usr/bin/env python3
"""Build Book #5: Bubbles the Helpful Whale."""
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
    print("BOOK #5: Bubbles the Helpful Whale")
    TRIM = 8.5 * inch; BLEED = 0.125 * inch
    PW = TRIM + 2*BLEED; PH = TRIM + 2*BLEED
    IMG_DIR = '/home/team/shared/bubbles-whale-illustrations'
    OUT = '/home/team/shared/book5-bubbles-whale-kdp.pdf'
    texts = {
        2: 'Deep in the sparkling blue ocean lived a little whale named Bubbles. Bubbles was small, but she had a very big heart.',
        3: 'Every morning, Bubbles would swim through the Coral Kingdom. She loved to help her friends.',
        4: 'First, she met Finley the Clownfish. Finley\'s home in the anemone was full of tangled seaweed.',
        5: '"Don\'t worry, Finley! I can help!" Bubbles said. She used her soft fins to sweep away the seaweed.',
        6: 'Next, she saw Captain Kelp. The reef was very busy, and all the fish were swimming in different directions!',
        7: 'Bubbles blew a stream of heart-shaped bubbles to show the fish which way to go. "Follow the hearts!" she cheered.',
        8: 'Then Bubbles found Shelly the Sea Turtle. Shelly was trying to move a heavy rock to reach some tasty sea-grapes.',
        9: '*OOF!* Bubbles gave the rock a gentle nudge with her nose. It rolled right over!',
        10: 'By lunchtime, Bubbles was very tired. But she saw a group of baby crabs who had lost their ball in a deep crevice.',
        11: '"I... can... help..." Bubbles puffed. She tried to reach into the hole, but she was too big.',
        12: 'She tried and tried, but her fins were too sore. She couldn\'t do it all by herself.',
        13: 'Finley, Shelly, and Captain Kelp saw Bubbles looking sad. They swam over to her.',
        14: '"What\'s wrong, Bubbles?" Finley asked. "I\'m too tired to help," Bubbles whispered. "And I\'m too big for this hole."',
        15: 'Shelly smiled her wise turtle smile. "Bubbles, you have helped us all morning. Now, let us help you!"',
        16: '"Teamwork makes the dream work!" Captain Kelp shouted. He used his long fronds to steady Finley.',
        17: 'Finley was small and fast. He darted into the crevice and grabbed the lost ball.',
        18: 'Shelly used her strong shell to block the current, making it easy for Finley to swim back out.',
        19: '*POP!* Finley came out with the ball. The baby crabs cheered and danced!',
        20: 'Bubbles realized something important. "Helping is great," she said, "but helping together is even better!"',
        21: 'That afternoon, the friends worked as a team to clean the whole reef. It was much faster and more fun!',
        22: 'Bubbles didn\'t feel tired anymore because she wasn\'t doing it all alone.',
        23: 'As the sun began to set, the ocean turned a beautiful shade of pink.',
        24: 'Bubbles blew one last heart-shaped bubble into the twilight. "Goodnight, friends," she hummed.',
    }
    c = canvas.Canvas(OUT, pagesize=(PW, PH))
    place_image(c, os.path.join(IMG_DIR, 'front-cover.png'), PW, PH)
    c.setFillColorRGB(0.1, 0.3, 0.7)
    c.setFont("Helvetica-Bold", 38)
    c.drawCentredString(PW/2, PH - 95, "Bubbles the")
    c.drawCentredString(PW/2, PH - 140, "Helpful Whale")
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.7, 0.8, 1.0)
    c.drawCentredString(PW/2, PH - 175, "A StorySprout Press Book")
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
    blurb = ("Join Bubbles the little blue whale on an underwater\n"
             "adventure! With heart-shaped bubbles and a helping fin,\n"
             "she assists all her ocean friends. But when she gets\n"
             "too tired, Bubbles learns that teamwork makes the\n"
             "dream work!\n\nAges 2-6 | StorySprout Press")
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
    listing = r"""# Book #5: "Bubbles the Helpful Whale" - Product Listing

## Amazon KDP Product Details
**Title:** Bubbles the Helpful Whale: A Heartwarming Children's Picture Book About Teamwork and Helping Others
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99

### Amazon Bullet Points
1. **HEARTWARMING OCEAN STORY** - Bubbles the little whale loves helping her friends, but learns that teamwork is even better than doing it all alone.
2. **BEAUTIFUL UNDERWATER ILLUSTRATIONS** - 24 vibrant full-color illustrations of coral reefs, ocean creatures, and sparkling heart-shaped bubbles.
3. **TEACHES TEAMWORK & KINDNESS** - A gentle lesson about helping others and knowing when to ask for help in return.
4. **LOVELY CHARACTERS** - Meet Bubbles, Finley the Clownfish, Shelly the Sea Turtle, and Captain Kelp in a charming ocean world.
5. **UNIQUE BUBBLE CONCEPT** - Bubbles' special heart-shaped bubbles add a magical, whimsical element children will adore.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **PERFECT BEDTIME READ** - The gentle ocean theme and heartwarming message make this ideal for bedtime.

### Amazon Backend Keywords
children's picture book, whale book for kids, ocean story for toddlers, teamwork children's book, helping others kids book, sea animals picture book, coral reef book, friendship story preschool, underwater adventure kids book, marine life for children, bedtime ocean story, baby shower book gift, kindness tale, clownfish book, sea turtle kids book

### Etsy Listing
**Title:** Bubbles the Helpful Whale - Printable Children's Storybook PDF | Ocean Bedtime Story | Whale Picture Book Digital Download
**Tags:** childrens storybook, printable book for kids, bedtime story pdf, whale book, ocean kids book, teamwork story, sea animals, digital download, preschool learning, underwater adventure, kindness book, homeschool resource
**Description:** Deep in the sparkling ocean, Bubbles the little blue whale loves to help her friends! But when she tries to do everything alone, she learns that teamwork makes the dream work. 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-book5-storybook.md', 'w') as f:
        f.write(listing)
    print("  -> /home/team/shared/listings-book5-storybook.md")

if __name__ == '__main__':
    make_storybook()
    make_listings()
    print("BOOK #5 COMPLETE!")