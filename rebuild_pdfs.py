#!/usr/bin/env python3
"""Rebuild all KDP PDFs with proper margins so nothing goes off the page."""
import os, json
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

TMP = '/home/team/shared/.tmp_build'
os.makedirs(TMP, exist_ok=True)

def make_storybook(book_num, title, subtitle, img_dir, text_file, out_file, texts_dict, trim_w=8.5, trim_h=8.5, cover_color=(0.95, 0.5, 0.1)):
    """Build a storybook PDF with proper margins and safe areas."""
    BLEED = 0.125 * inch
    MARGIN = 0.35 * inch  # extra interior margin for safety
    TRIM_W = trim_w * inch
    TRIM_H = trim_h * inch
    PW = TRIM_W + 2 * BLEED  # full page width with bleeds
    PH = TRIM_H + 2 * BLEED
    
    # Image safe area: inside trim minus margin
    IMG_W = TRIM_W - 2 * MARGIN
    IMG_H = TRIM_H - 2 * MARGIN
    IMG_X = BLEED + MARGIN
    IMG_Y = BLEED + MARGIN

    c = canvas.Canvas(out_file, pagesize=(PW, PH))
    
    def place_image_safe(img_path, pg_num=None):
        """Place image scaled to fit within safe area, centered, with background."""
        # Fill background so bleed area has color
        c.setFillColorRGB(1, 1, 1)
        c.rect(0, 0, PW, PH, fill=1, stroke=0)
        
        if img_path and os.path.exists(img_path):
            img = Image.open(img_path).convert('RGB')
            iw, ih = img.size
            # Scale to fit safe area while maintaining aspect ratio
            scale = min(IMG_W / iw, IMG_H / ih)
            dw = iw * scale
            dh = ih * scale
            # Center in safe area
            dx = IMG_X + (IMG_W - dw) / 2
            dy = IMG_Y + (IMG_H - dh) / 2
            # Use PIL to resize
            new_size = (int(dw), int(dh))
            resized = img.resize(new_size, Image.LANCZOS)
            tmp_path = os.path.join(TMP, f'tmp_{pg_num or "cover"}.jpg')
            resized.save(tmp_path, 'JPEG', quality=95)
            c.drawImage(tmp_path, dx, dy, width=dw, height=dh)
    
    # --- Front Cover ---
    place_image_safe(os.path.join(img_dir, 'front-cover.png'), 'cover')
    # Cover already has title from illustrator — just add StorySprout Press branding
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawCentredString(PW/2, BLEED + 55, "A StorySprout Press Book")
    c.showPage()
    
    # --- Interior Pages ---
    for pn in range(1, 25):
        place_image_safe(os.path.join(img_dir, f'page-{pn:02d}.png'), pn)
        if pn in texts_dict:
            t = texts_dict[pn]
            # Text box at the bottom within safe area
            tx = BLEED + MARGIN + 15
            ty = BLEED + MARGIN + 22
            tw = IMG_W - 30
            font_size = 15
            c.setFont("Helvetica", font_size)
            line_h = font_size * 1.35
            margin_x = 12
            
            # Wrap text to fit within box width
            max_text_w = tw - margin_x * 2
            words = t.split()
            wrapped = []
            cur_line = ''
            for w in words:
                test = cur_line + (' ' if cur_line else '') + w
                if c.stringWidth(test, "Helvetica", font_size) <= max_text_w:
                    cur_line = test
                else:
                    if cur_line:
                        wrapped.append(cur_line)
                    cur_line = w
            if cur_line:
                wrapped.append(cur_line)
            
            n = len(wrapped)
            # Make box taller if more lines needed
            th = max(80, n * line_h + 20)
            ty = BLEED + MARGIN + 15  # reset y
            
            # Draw background box
            c.setFillColorRGB(1, 1, 1, alpha=0.85)
            c.roundRect(tx, ty, tw, th, 6, fill=1, stroke=0)
            c.setFillColorRGB(0.1, 0.1, 0.15)
            
            # Center text block vertically in the box
            box_center_y = ty + th / 2
            first_y = box_center_y + (n - 1) * line_h / 2 - 2
            cx = tx + tw / 2
            for i, line in enumerate(wrapped):
                c.drawCentredString(cx, first_y - i * line_h, line)
        # Page number
        if pn > 1:
            c.setFont("Helvetica", 9)
            c.setFillColorRGB(0.5, 0.5, 0.5)
            c.drawCentredString(PW/2, BLEED + 12, str(pn))
        c.showPage()
    
    # --- Back Cover ---
    # Just place the back cover image — no text overlay to avoid overlapping
    place_image_safe(os.path.join(img_dir, 'back-cover.png'), 'back')
    # Small credit at very bottom
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawCentredString(PW/2, BLEED + 50, "StorySprout Press")
    c.showPage()
    
    c.save()
    sz = os.path.getsize(out_file) / (1024*1024)
    print(f"  -> {out_file} ({sz:.1f} MB)")

def build_texts_from_file(filepath):
    """Parse a story manuscript markdown file to extract page texts."""
    texts = {}
    try:
        with open(filepath) as f:
            content = f.read()
        import re
        pages = re.findall(r'### Page (\d+)\n\*\*Text:\*\* (.*?)(?:\n|$)', content)
        for pg_num, txt in pages:
            texts[int(pg_num)] = txt.strip()
    except:
        pass
    return texts

# ====== BOOK CONFIGURATIONS ======
books = []

# Book 1: The Little Cloud's Big Adventure
texts_b1 = build_texts_from_file('/home/team/shared/little-cloud-adventure.md')
texts_b1['blurb'] = ("Join Cirrus the little cloud on a heartwarming journey\n"
                     "as he discovers that even the smallest cloud can make a\n"
                     "big difference. A story about kindness, teamwork, and\n"
                     "believing in yourself.\n\nAges 2-6 | StorySprout Press")
books.append({
    'num': 1, 'out': '/home/team/shared/storybook-kdp-ready.pdf',
    'title': "The Little Cloud's Big Adventure", 'subtitle': '',
    'img_dir': '/home/team/shared/storybook-illustrations',
    'texts': texts_b1, 'color': (0.3, 0.6, 0.9)
})

# Book 2: The Brave Little Seed
texts_b2 = build_texts_from_file('/home/team/shared/brave-little-seed.md')
texts_b2['blurb'] = ("Follow Pip the tiny seed on his journey from a\n"
                     "cozy packet to a beautiful sunflower. With help from\n"
                     "Mama Sunflower, Wiggly Worm, and Raindrop Rita, Pip\n"
                     "learns that growing up is the bravest adventure of all.\n\nAges 2-6 | StorySprout Press")
books.append({
    'num': 2, 'out': '/home/team/shared/book2-brave-little-seed-kdp.pdf',
    'title': 'The Brave Little Seed', 'subtitle': '',
    'img_dir': '/home/team/shared/brave-little-seed-illustrations',
    'texts': texts_b2, 'color': (0.2, 0.7, 0.3)
})

# Book 3: Daisy the Dancing Duck
texts_b3 = build_texts_from_file('/home/team/shared/daisy-dancing-duck.md')
texts_b3['blurb'] = ("Daisy the duckling loves to dance, but the other ducks\n"
                     "think she should waddle like everyone else. With help\n"
                     "from Oliver the Owl and the Frog Choir, Daisy learns\n"
                     "that the best rhythm is your own.\n\nAges 2-6 | StorySprout Press")
books.append({
    'num': 3, 'out': '/home/team/shared/book3-daisy-dancing-duck-kdp.pdf',
    'title': 'Daisy the Dancing Duck', 'subtitle': '',
    'img_dir': '/home/team/shared/daisy-dancing-duck-illustrations',
    'texts': texts_b3, 'color': (0.9, 0.6, 0.1)
})

# Book 4: Leo the Light-Up Firefly
texts_b4 = build_texts_from_file('/home/team/shared/leo-lightup-firefly.md')
texts_b4['blurb'] = ("Leo the firefly can't flash like the others, but he\n"
                     "discovers he has a special steady lantern-light that\n"
                     "saves the day. A story about being different and\n"
                     "finding your own superpower.\n\nAges 2-6 | StorySprout Press")
books.append({
    'num': 4, 'out': '/home/team/shared/book4-leo-firefly-kdp.pdf',
    'title': 'Leo the Light-Up Firefly', 'subtitle': '',
    'img_dir': '/home/team/shared/leo-firefly-illustrations',
    'texts': texts_b4, 'color': (0.8, 0.7, 0.1)
})

# Book 5: Bubbles the Helpful Whale
texts_b5 = build_texts_from_file('/home/team/shared/bubbles-whale.md')
texts_b5['blurb'] = ("Bubbles the young whale loves to help everyone in the\n"
                     "ocean, but she learns that teamwork makes helping even\n"
                     "better! A heartwarming story about friendship and\n"
                     "knowing when to ask for help.\n\nAges 2-6 | StorySprout Press")
books.append({
    'num': 5, 'out': '/home/team/shared/book5-bubbles-whale-kdp.pdf',
    'title': 'Bubbles the Helpful Whale', 'subtitle': '',
    'img_dir': '/home/team/shared/bubbles-whale-illustrations',
    'texts': texts_b5, 'color': (0.2, 0.5, 0.9)
})

# Book 6: Benny the Bus
texts_b6 = build_texts_from_file('/home/team/shared/benny-the-bus.md')
texts_b6['blurb'] = ("Join Benny the friendly school bus on the best day of\n"
                     "the year - the first day of school! From picking up\n"
                     "nervous Mia to the noisy ride home, Benny proves that\n"
                     "a friendly bus makes every adventure better.\n\nAges 2-6 | StorySprout Press")
books.append({
    'num': 6, 'out': '/home/team/shared/book6-benny-bus-kdp.pdf',
    'title': 'Benny the Bus', 'subtitle': 'A Big Day for a Friendly Bus',
    'img_dir': '/home/team/shared/benny-bus-illustrations',
    'texts': texts_b6, 'color': (0.95, 0.5, 0.1)
})

# Book 7: Stella the Star
texts_b7 = build_texts_from_file('/home/team/shared/stella-star.md')
texts_b7['blurb'] = ("Stella is a tiny star who feels lonely in the vast\n"
                     "night sky. With help from Comet Carl and Moona the\n"
                     "Moon, she discovers she's surrounded by thousands of\n"
                     "friends. A story about friendship and belonging.\n\nAges 2-6 | StorySprout Press")
books.append({
    'num': 7, 'out': '/home/team/shared/book7-stella-star-kdp.pdf',
    'title': 'Stella the Star Who Found Friends', 'subtitle': '',
    'img_dir': '/home/team/shared/stella-star-illustrations',
    'texts': texts_b7, 'color': (0.6, 0.3, 0.8)
})

# Book 8: The Curious Little Penguin
texts_b8 = build_texts_from_file('/home/team/shared/curious-penguin.md')
texts_b8['blurb'] = ("Pip the penguin is full of questions about the world.\n"
                     "When his curiosity leads him on an Antarctic adventure,\n"
                     "he discovers amazing things - and finds his way home\n"
                     "with a little help from the stars.\n\nAges 2-6 | StorySprout Press")
books.append({
    'num': 8, 'out': '/home/team/shared/book8-curious-penguin-kdp.pdf',
    'title': 'The Curious Little Penguin', 'subtitle': '',
    'img_dir': '/home/team/shared/curious-penguin-illustrations',
    'texts': texts_b8, 'color': (0.1, 0.6, 0.7)
})

if __name__ == '__main__':
    for b in books:
        print(f"\nBuilding Book #{b['num']}: {b['title']}")
        make_storybook(
            book_num=b['num'],
            title=b['title'],
            subtitle=b['subtitle'],
            img_dir=b['img_dir'],
            text_file=None,
            out_file=b['out'],
            texts_dict=b['texts'],
            cover_color=b['color']
        )
    print("\n=== ALL BOOKS REBUILT ===")
