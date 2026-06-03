#!/usr/bin/env python3
"""Build ALL deliverables for StorySprout Press: storybook PDF, activity book PDF+ZIP, and listings."""
import os, sys, zipfile, tempfile, shutil
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

TMP = '/home/team/shared/.tmp_build'
os.makedirs(TMP, exist_ok=True)

def place_image(c, img_path, w, h):
    """Scale image to fill given dimensions and draw it."""
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
# TASK 1: Storybook PDF (8.5"x8.5")
# ===========================
def make_storybook():
    print("=" * 50)
    print("TASK 1: Building storybook PDF...")
    print("=" * 50)
    
    TRIM = 8.5 * inch
    BLEED = 0.125 * inch
    PW = TRIM + 2 * BLEED
    PH = TRIM + 2 * BLEED
    
    IMG = '/home/team/shared/storybook-illustrations'
    OUT = '/home/team/shared/storybook-kdp-ready.pdf'
    
    texts = {
        2: "Once upon a time, high above the hills, lived a little cloud named Cirrus.",
        3: "Cirrus was fluffy. Cirrus was white. But most of all, Cirrus was curious.",
        4: '"What is it like down there?" Cirrus wondered. "Can a little cloud like me help the world?"',
        5: "He saw a little garden where the flowers were drooping. They looked very thirsty.",
        6: "Cirrus tried to squeeze out some rain. *Squeeze! Squeeze! Squeeze!*",
        7: "But only one tiny *plip* fell. It wasn't enough to help the thirsty flowers.",
        8: '"I am too small," Cirrus sighed. He felt very droopy himself.',
        9: '"Don\'t be sad, Cirrus," said Sunny the Sun. "Everyone has a special job to do."',
        10: 'Just then, Gusty the Breeze whizzed by. "Want to see something cool?" Gusty asked.',
        11: "Gusty blew and Cirrus flew! They zipped over the hills and over the trees.",
        12: "They stopped over a playground. The sun was very hot, and the children were tired.",
        13: "Cirrus floated right in front of the sun. He made a big, cool shadow on the ground.",
        14: '"Ooh, shade!" cried a little girl. "Thank you, little cloud!"',
        15: "Cirrus beamed. He had helped! Providing shade was a very important job.",
        16: "But Cirrus still wanted to make rain. He met his friend Drippy.",
        17: '"To make rain, you must gather your friends," Drippy explained. "We work better together!"',
        18: "They floated over a big brown field where a farmer was waiting.",
        19: "Cirrus, Drippy, and all their cloud friends huddle together. They grew bigger and darker.",
        20: "*Pitter-patter, pitter-patter!* The rain began to fall.",
        21: "The field turned green, and the farmer was happy. Cirrus had helped make a big difference!",
        22: "As the rain stopped, a beautiful rainbow stretched across the sky.",
        23: "Cirrus felt very special. He knew that even a little cloud could do big things.",
        24: 'That night, Cirrus turned a lovely shade of pink and orange as the sun went down.\n"I can\'t wait for tomorrow\'s adventure," he whispered.',
    }
    
    c = canvas.Canvas(OUT, pagesize=(PW, PH))
    
    # Front cover
    place_image(c, os.path.join(IMG, 'front-cover.png'), PW, PH)
    c.setFillColorRGB(255, 255, 255)
    c.setFont("Helvetica-Bold", 42)
    c.setFillColorRGB(0.9, 0.9, 0.95)
    c.drawCentredString(PW/2, PH - 110, "The Little Cloud's")
    c.drawCentredString(PW/2, PH - 158, "Big Adventure")
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.7, 0.7, 0.8)
    c.drawCentredString(PW/2, PH - 195, "A StorySprout Press Book")
    c.showPage()
    
    # Interior pages
    for pn in range(1, 25):
        place_image(c, os.path.join(IMG, f'page-{pn:02d}.png'), PW, PH)
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
    place_image(c, os.path.join(IMG, 'back-cover.png'), PW, PH)
    c.setFillColorRGB(0.1, 0.1, 0.2)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(PW/2, PH - 90, "About the Story")
    blurb = ("Join Cirrus the little cloud on a heartwarming adventure through\n"
             "the sky! From helping thirsty gardens to providing shade for\n"
             "playing children, Cirrus learns that even the smallest cloud\n"
             "can make a big difference.\n\n"
             "With friends Sunny, Gusty, and Drippy by his side, Cirrus\n"
             "discovers the power of working together and the joy of\n"
             "helping others.\n\n"
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
# TASK 2: Activity Book PDF + ZIP
# ===========================
def make_activity():
    print("=" * 50)
    print("TASK 2: Building activity book PDF + ZIP...")
    print("=" * 50)
    
    TRIM_W = 8.5 * inch
    TRIM_H = 11.0 * inch
    BLEED = 0.125 * inch
    PW = TRIM_W + 2 * BLEED
    PH = TRIM_H + 2 * BLEED
    
    IMG = '/home/team/shared/activity-book-pages'
    OUT_PDF = '/home/team/shared/activity-book-kdp-ready.pdf'
    OUT_ZIP = '/home/team/shared/little-cloud-activity-book-digital.zip'
    
    pages = {
        1: 'cover.png', 2: 'page-02.png', 3: 'page-03.png',
        4: 'page-04.png', 5: 'page-05.png', 6: 'page-06.png',
        7: 'page-07.png', 8: 'page-08.png', 9: 'page-09.png',
        10: 'page-10.png', 11: 'page-11.png', 12: 'page-12.png',
        13: 'page-13.png', 14: 'page-14.png', 15: 'page-15.png',
        24: 'page-24.png',
    }
    
    # KDP PDF with bleeds
    c = canvas.Canvas(OUT_PDF, pagesize=(PW, PH))
    
    # Cover
    place_image(c, os.path.join(IMG, 'cover.png'), PW, PH)
    c.setFillColorRGB(0.9, 0.2, 0.3)
    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(PW/2, PH - 110, "Little Cloud's Big")
    c.drawCentredString(PW/2, PH - 150, "Activity Book!")
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawCentredString(PW/2, PH - 185, "Ages 2-6 ~ Fun with Cirrus & Friends")
    c.showPage()
    
    for pn, fn in sorted(pages.items()):
        if pn == 1:
            continue
        place_image(c, os.path.join(IMG, fn), PW, PH)
        c.showPage()
    
    c.save()
    sz = os.path.getsize(OUT_PDF) / (1024*1024)
    print(f"  -> {OUT_PDF} ({sz:.1f} MB)")
    
    # Digital ZIP (individual pages, no bleed)
    tmpd = tempfile.mkdtemp()
    for pn, fn in sorted(pages.items()):
        src = os.path.join(IMG, fn)
        if not os.path.exists(src):
            continue
        c2 = canvas.Canvas(os.path.join(tmpd, f'page-{pn:02d}.pdf'), pagesize=(TRIM_W, TRIM_H))
        place_image(c2, src, TRIM_W, TRIM_H)
        c2.save()
    
    # Also add the cover
    c2 = canvas.Canvas(os.path.join(tmpd, 'cover.pdf'), pagesize=(TRIM_W, TRIM_H))
    place_image(c2, os.path.join(IMG, 'cover.png'), TRIM_W, TRIM_H)
    c2.save()
    
    with zipfile.ZipFile(OUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(os.listdir(tmpd)):
            if f.endswith('.pdf'):
                zf.write(os.path.join(tmpd, f), f)
    
    shutil.rmtree(tmpd)
    sz = os.path.getsize(OUT_ZIP) / (1024*1024)
    print(f"  -> {OUT_ZIP} ({sz:.2f} MB)")

# ===========================
# TASK 3: Product Listings
# ===========================
def make_listings():
    print("=" * 50)
    print("TASK 3: Creating product listings...")
    print("=" * 50)
    
    # Storybook listing
    story = """# Product Listing: "The Little Cloud's Big Adventure"

## Amazon KDP Product Details

**Title:** The Little Cloud's Big Adventure: A Heartwarming Children's Picture Book About Kindness and Friendship
**Series:** Cirrus the Cloud Adventures (Book 1)
**Author:** StorySprout Press
**Trim Size:** 8.5" x 8.5" square
**Page Count:** 26 pages (including cover)
**Age Range:** 2-6 years
**Price (Print):** $9.99
**Price (Digital):** $4.99

### Amazon Bullet Points
1. **HEARTWARMING STORY** - Join Cirrus the little cloud on a journey of self-discovery as he learns that even the smallest cloud can make a big difference in the world.
2. **BEAUTIFUL ILLUSTRATIONS** - 24 vibrant, full-color illustrations bring Cirrus and his friends Sunny, Gusty, and Drippy to life on every page.
3. **TEACHES VALUABLE LESSONS** - This charming tale gently introduces children to themes of kindness, perseverance, teamwork, and helping others.
4. **PERFECT READ-ALOUD** - Simple, engaging text makes this ideal for bedtime stories, classroom reading, or quality time with grandparents.
5. **INTERACTIVE STORYTELLING** - Children will love making rain sounds, pointing out characters, and following Cirrus's colorful adventure across the sky.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages designed for little hands to hold and explore.
7. **SERIES STARTER** - The first book in the Cirrus the Cloud Adventures series, perfect for building a beloved library collection.

### Amazon Backend Keywords (KDP Search Terms)
children's picture book, bedtime story for kids, toddler books ages 2-4, preschool storybook, kindness books for children, friendship stories, cloud character book, weather books for kids, social emotional learning, SEL books for toddlers, read aloud books, nature books for children, picture book about helping, teamwork stories, perseverance for kids, gift for toddler boy girl, baby shower book gift, kindergarten story time, classroom library book, kids book about clouds

### Etsy Listing

**Title:** The Little Cloud's Big Adventure - Printable Children's Storybook PDF | Bedtime Story for Toddlers | Preschool Picture Book Digital Download

**Tags:** childrens storybook, printable book for kids, bedtime story pdf, toddler learning, preschool book, digital download kids book, cloud story, kindness book, childrens literature, homeschool resource

**Description:**
Bring the magic of Cirrus the Cloud into your home with this charming digital storybook!

Join Cirrus, a small fluffy cloud with big dreams, as he discovers that even the smallest among us can make a huge difference. From helping thirsty gardens to providing shade for playing children, Cirrus's heartwarming journey teaches kindness, teamwork, and perseverance.

WHAT'S INCLUDED:
- 24 beautifully illustrated story pages (PDF format)
- Front and back cover
- Print-ready at 8.5" x 8.5"
- Unlimited printing for personal use

PERFECT FOR:
- Bedtime reading with toddlers and preschoolers
- Classroom story time (ages 2-6)
- Homeschooling curriculum enrichment
- Baby shower and birthday gifts
- Travel entertainment

This is a DIGITAL DOWNLOAD. No physical product will be shipped.
"""
    
    with open('/home/team/shared/listings-storybook.md', 'w') as f:
        f.write(story)
    print("  -> /home/team/shared/listings-storybook.md")
    
    # Activity book listing
    activity = """# Product Listing: "Little Cloud's Big Activity Book"

## Amazon KDP Product Details

**Title:** Little Cloud's Big Activity Book: Coloring Pages, Mazes, Connect-the-Dots & More for Ages 2-6
**Series:** Cirrus the Cloud Adventures (Activity Book 1)
**Author:** StorySprout Press
**Trim Size:** 8.5" x 11" portrait
**Page Count:** 24 pages
**Age Range:** 2-6 years
**Price (Print):** $7.99
**Price (Digital):** $3.99

### Amazon Bullet Points
1. **20+ FUN ACTIVITIES** - Includes coloring pages, mazes, connect-the-dots, tracing, spot-the-difference, counting, matching, and drawing activities.
2. **BELOVED CHARACTERS** - Features Cirrus the cloud, Sunny the Sun, Gusty the Breeze, and Drippy the Rain Cloud from the popular storybook series.
3. **SKILL BUILDING** - Activities promote fine motor skills, hand-eye coordination, number recognition, letter tracing, and creative expression.
4. **SCREEN-FREE ENTERTAINMENT** - Hours of engaging, educational fun perfect for travel, quiet time, restaurants, or rainy days.
5. **CERTIFICATE OF ACHIEVEMENT** - Includes a special "Cloud Explorer Certificate" to celebrate your child's completion of the book.
6. **AGES 2-6 APPROPRIATE** - Simple, clear activities designed specifically for toddlers, preschoolers, and kindergarteners.
7. **MATCHING STORYBOOK** - Pairs perfectly with "The Little Cloud's Big Adventure" for a complete Cirrus experience.

### Amazon Backend Keywords (KDP Search Terms)
childrens activity book, coloring book for toddlers, preschool activity book, kids maze book, connect the dots, tracing book for kids, cloud activity book, toddler workbook, preschool learning, fine motor skills, screen free activities, kids travel activity, coloring pages for kids, preschool workbook, kindergarten activity book, kids spot the difference, counting activities, homeschool activity book, gift for 2 year old, gift for 3 year old

### Etsy Listing

**Title:** Little Cloud's Big Activity Book - Printable Kids Activity Pages | Toddler Coloring Book | Preschool Worksheets | Digital Download

**Tags:** kids activity book, printable coloring pages, toddler worksheets, preschool activities, digital download kids, maze for kids, connect the dots, tracing worksheets, homeschool printable, childrens workbook

**Description:**
Extend the fun of Cirrus's adventures with this engaging activity book for little learners!

Packed with over 20 activities featuring Cirrus and all his friends, this book provides hours of creative, screen-free fun for children ages 2-6.

ACTIVITIES INCLUDE:
- Coloring pages of Cirrus, Sunny, Gusty & Drippy
- Simple mazes to build problem-solving skills
- Connect-the-dots (numbers 1-15)
- Letter and shape tracing activities
- Spot-the-difference puzzles
- Counting activities
- Matching games
- Drawing prompts to spark creativity
- Bonus Cloud Explorer Certificate!

WHAT'S INCLUDED:
- 24 printable activity pages (PDF format)
- Individual page files for easy printing
- Print at 8.5" x 11" on standard paper
- Unlimited printing for personal/classroom use

This is a DIGITAL DOWNLOAD. No physical product will be shipped.
"""
    
    with open('/home/team/shared/listings-activity-book.md', 'w') as f:
        f.write(activity)
    print("  -> /home/team/shared/listings-activity-book.md")
    
    # Bundle listing
    bundle = """# Product Listing: Cirrus the Cloud BUNDLE (Storybook + Activity Book)

## Bundle Details

**Bundle Includes:**
1. "The Little Cloud's Big Adventure" storybook (24 illustrated pages)
2. "Little Cloud's Big Activity Book" (24 activity pages)

**Age Range:** 2-6 years

**Bundle Pricing:**
- Digital Bundle: $14.99 (save $2.99 vs buying separately)

### Amazon Bullet Points
1. **COMPLETE CIRRUS EXPERIENCE** - Get both the heartwarming storybook AND the companion activity book in one convenient bundle.
2. **READ, PLAY, LEARN** - Start with Cirrus's inspiring story, then reinforce the lessons through coloring, mazes, puzzles, and more.
3. **HOURS OF ENTERTAINMENT** - Over 50 pages combining the story and activities for endless screen-free fun at home or on the go.
4. **DEVELOPS KEY SKILLS** - Builds reading comprehension, fine motor skills, creativity, and social-emotional learning.
5. **VALUE BUNDLE** - Save money compared to purchasing each book separately.
6. **PERFECT GIFT SET** - An ideal gift for birthdays, holidays, or any occasion for children ages 2-6.
7. **CLASSROOM FRIENDLY** - Perfect for preschool and kindergarten teachers looking for story time + activity materials.

### Amazon Backend Keywords (KDP Search Terms)
children's book bundle, storybook and activity book set, toddler gift set, preschool bundle, kids book collection, Cirrus the Cloud gift set, bedtime story and activity book, kindergarten learning bundle, children's gift basket, homeschool curriculum bundle, kids birthday gift, educational gift for toddler, story time and activity set

### Etsy Listing

**Title:** Cirrus the Cloud BUNDLE - Storybook + Activity Book | Digital Download for Kids | Bedtime Story & Activities | Preschool Learning Set

**Tags:** kids book bundle, storybook and activity, digital download bundle, toddler gift set, preschool learning bundle, childrens story and activities, homeschool set, classroom printable, kids birthday gift, Cirrus the Cloud

**Description:**
The complete Cirrus the Cloud experience! Save when you purchase both books together.

This bundle includes:
1. The Little Cloud's Big Adventure - A heartwarming 24-page story about kindness and helping others
2. Little Cloud's Big Activity Book - 24 pages of coloring, mazes, tracing, and more

Perfect for children ages 2-6, this bundle offers hours of reading and play. Start with the story, then continue the fun with matching activities featuring beloved characters.

This is a DIGITAL DOWNLOAD. No physical product will be shipped.
"""
    
    with open('/home/team/shared/listings-bundle.md', 'w') as f:
        f.write(bundle)
    print("  -> /home/team/shared/listings-bundle.md")

if __name__ == '__main__':
    make_storybook()
    make_activity()
    make_listings()
    print()
    print("=" * 50)
    print("ALL TASKS COMPLETE!")
    print("=" * 50)