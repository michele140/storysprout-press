#!/usr/bin/env python3
"""Build Book #6: Benny the Bus."""
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
    print("BOOK #6: Benny the Bus")
    TRIM = 8.5 * inch; BLEED = 0.125 * inch
    PW = TRIM + 2*BLEED; PH = TRIM + 2*BLEED
    IMG_DIR = '/home/team/shared/benny-bus-illustrations'
    OUT = '/home/team/shared/book6-benny-bus-kdp.pdf'
    texts = {
        2: 'The sun was just peeking over the hills when Benny the Bus woke up. *Yawn!* His headlights blinked open.',
        3: 'Depot Dan arrived with a whistle. "Good morning, Benny! Let\'s get you ready for your big adventure."',
        4: 'Dan checked Benny\'s tires. *Thump, thump!* He checked Benny\'s oil. *Dip, dip!* Benny felt strong and sturdy.',
        5: '"Everything looks great!" Dan said, giving Benny a final polish. Benny\'s yellow paint sparkled in the light.',
        6: 'Benny rolled out of the depot. *Vroom, vroom!* "Beep beep! Here comes the school bus!" he sang.',
        7: 'The neighborhood was quiet and still. Benny knew exactly where to go. He loved his morning route.',
        8: 'At the first stop, Benny saw Mia. She was holding her purple backpack very tightly.',
        9: 'Benny pulled up to the curb. *Hiss-swish!* His doors opened wide like a big, welcoming hug.',
        10: '"Don\'t be nervous, Mia," Benny seemed to say with a soft hum. Mia stepped inside and saw the comfy seats.',
        11: 'Benny\'s stop sign arm popped out. *Click-clack!* It told all the other cars to wait while Mia got settled.',
        12: 'Next stop was Liam. He hopped onto the bus with his green toy dinosaur. "Rawr!" said the dinosaur.',
        13: '"Good morning, Liam! Good morning, Dinosaur!" Benny hummed as they rolled along.',
        14: 'More stops and more friends! Soon, Benny was full of happy chatter and silly songs.',
        15: 'The children sang, "The wheels on the bus go round and round!" Benny\'s wheels turned happily.',
        16: 'Finally, they arrived at the big brick school. "School is an adventure too!" Benny cheered with a beep.',
        17: 'The children hopped off, one by one. "Bye, Benny! See you later!" they called.',
        18: 'While the children were in class, Benny waited in the big parking lot. He rested his engine and watched the birds.',
        19: 'The sun moved across the sky. Benny felt the warm breeze on his mirrors. He was ready to bring his friends home.',
        20: 'The school bell rang! *Ding-dong!* The children came running out, full of stories about their day.',
        21: 'Benny picked everyone up. The ride home was even noisier than the morning ride!',
        22: 'Benny dropped off Liam and his dinosaur. He dropped off Mia and her purple backpack. "See you tomorrow!"',
        23: 'Benny rolled back to the depot as the sky turned orange and pink. He was tired, but his heart was full.',
        24: 'Depot Dan was waiting. "Great job, Benny," he said. Benny closed his headlight eyes and fell fast asleep.',
    }
    c = canvas.Canvas(OUT, pagesize=(PW, PH))
    place_image(c, os.path.join(IMG_DIR, 'front-cover.png'), PW, PH)
    c.setFillColorRGB(0.95, 0.5, 0.1)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(PW/2, PH - 95, "Benny the Bus")
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(PW/2, PH - 135, "A Big Day for a Friendly Bus")
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.3, 0.3, 0.3)
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
    blurb = ("Join Benny the friendly school bus on the best day of\n"
             "the year - the first day of school! From picking up\n"
             "nervous Mia and her purple backpack to the noisy ride\n"
             "home, Benny proves that a friendly bus makes every\n"
             "adventure better.\n\nAges 2-6 | StorySprout Press")
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
    listing = r"""# Book #6: "Benny the Bus" - Product Listing

## Amazon KDP Product Details
**Title:** Benny the Bus: A Big Day for a Friendly Bus - A Heartwarming Children's Picture Book About School and Friendship
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99

### Amazon Bullet Points
1. **HEARTWARMING SCHOOL STORY** - Follow Benny the friendly school bus on the first day of school as he helps nervous children feel welcome and safe.
2. **BEAUTIFUL VEHICLE ILLUSTRATIONS** - 24 vibrant illustrations of Benny, the bus depot, and neighborhood streets full of color and detail.
3. **TEACHES KINDNESS & COMMUNITY** - Benny's gentle, caring nature shows children the importance of helping others feel comfortable and valued.
4. **PERFECT FOR SCHOOL PREP** - Ideal for children starting preschool, kindergarten, or any new adventure that might feel a little scary.
5. **FUN SOUND WORDS** - Engaging text with *Vroom, vroom!*, *Click-clack!*, *Hiss-swish!*, and *Ding-dong!* makes story time extra fun.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **BELOVED CHARACTERS** - Features Benny, Depot Dan, Mia (with purple backpack), Liam (with toy dinosaur), and the iconic Stop Sign.

### Amazon Backend Keywords
children's picture book, school bus book, first day of school book, vehicle book for kids, transportation kids book, school bus story, back to school children's book, bus driver book, preschool starting school, kindergarten readiness, bedtime story about school, kids book about bus, friendly bus story, social emotional learning, school adventure book

### Etsy Listing
**Title:** Benny the Bus - Printable Children's Storybook PDF | School Bus Bedtime Story | First Day of School Picture Book Digital Download
**Tags:** childrens storybook, printable book for kids, bedtime story pdf, school bus book, first day of school, vehicle kids book, back to school, transportation story, digital download, preschool readiness, kindness book, homeschool resource
**Description:** Join Benny the friendly school bus on the best day of the year! From picking up nervous Mia to the noisy ride home, Benny proves a friendly bus makes every adventure better. 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-book6-storybook.md', 'w') as f:
        f.write(listing)
    print("  -> /home/team/shared/listings-book6-storybook.md")

if __name__ == '__main__':
    make_storybook()
    make_listings()
    print("BOOK #6 COMPLETE!")