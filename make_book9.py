#!/usr/bin/env python3
"""Build Book #9: Pip the Garden Gnome's Surprise."""
import os, textwrap
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
    print("BOOK #9: Pip the Garden Gnome's Surprise")
    T=8.5*inch; B=0.125*inch; PG=T+2*B; PH=T+2*B
    MARGIN=0.35*inch  # 0.35" inner margin per task spec
    D='/home/team/shared/gnome-illustrations'; O='/home/team/shared/book9-gnome-kdp.pdf'
    
    # Story text per page number (page 9 is missing from manuscript)
    txt={
        2:'In a corner of a sun-drenched garden, nestled beneath the giant leaves of a rhubarb plant, lived Pip the Gnome.',
        3:'Pip was a very small gnome, but he had a very big secret. He was the Garden\'s Helper.',
        4:'Mr. McGregor loved his flowers, but sometimes he was a bit tired. Pip loved to help when the gardener wasn\'t looking.',
        5:'"What\'s the plan today, Pip?" asked Bella the Butterfly, landing on a nearby daisy.',
        6:'"Mr. McGregor lost his favorite trowel," Pip said. "And the roses are thirsty. We have a lot to do!"',
        7:'First, Pip and Tiptoe the Mouse found the trowel. It was heavy, but together they pushed it into the open.',
        8:'Next, they found a lost packet of seeds and placed it right on Mr. McGregor\'s garden bench.',
        # Page 9 skipped in manuscript
        10:'Then it was time for the biggest surprise. Pip found a tiny leak in the garden hose and used it to fill his acorn cap.',
        11:'One by one, he carried the water to the thirsty roses. *Drip, drop, drip!*',
        12:'By the time the sun began to set, the garden looked magical.',
        13:'Mr. McGregor came out for his evening walk. "Well, I\'ll be!" he said, spotting his trowel.',
        14:'He saw the seeds on the bench. "And here are my sunflowers! I must have left them here this morning."',
        15:'But the best surprise was the roses. They were standing tall and smelling sweeter than ever.',
        16:'"The garden feels full of magic today," the old gardener whispered.',
        17:'Pip, Bella, and Tiptoe watched from their hiding spot. They didn\'t need a "thank you."',
        18:'"Giving a surprise is the best gift of all," Pip said to his friends.',
        19:'That night, the Moon shone down on the garden, silver and bright.',
        20:'Pip went back to his gourd-house. He was tired, but he was already thinking of tomorrow\'s surprise.',
        21:'"Maybe we can help with the birdbath?" Tiptoe suggested, curled up in his bed of soft wool.',
        22:'"Or find those missing spectacles!" Bella added from her leaf-hammock.',
        23:'Pip smiled. The garden was full of friends, and full of magic, and he was the luckiest gnome in the world.',
        24:'Somewhere in the garden, a single firefly blinked. The magic was just getting started.',
    }
    
    c=canvas.Canvas(O,pagesize=(PG,PH))
    
    # Front cover - no duplicate title text per task spec (title is in the image)
    plc(c,D+'/front-cover.png',PG,PH)
    # Just author credit, no title since image already has it
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0.6, 0.2, 0.1)
    c.drawCentredString(PG/2, PH - 185, "A StorySprout Press Book")
    c.showPage()
    
    # Interior pages
    for pn in range(1, 25):
        plc(c,D+f'/page-{pn:02d}.png',PG,PH)
        if pn in txt:
            t=txt[pn]
            # Semi-transparent text background - with 0.35" margins
            c.setFillColorRGB(1,1,1,alpha=0.75)
            x0 = B + MARGIN
            y0 = B + 12
            tw = T - 2*MARGIN
            th = 85
            c.roundRect(x0, y0, tw, th, 8, fill=1, stroke=0)
            
            # Word-wrapped, centered text
            c.setFillColorRGB(0.1, 0.1, 0.15)
            c.setFont("Helvetica", 14)
            wrapped = textwrap.wrap(t, width=48)
            cy = y0 + th - 18
            for line in wrapped:
                c.drawCentredString(B + T/2, cy, line)
                cy -= 18
        if pn > 1:
            c.setFont("Helvetica", 9)
            c.setFillColorRGB(0.5, 0.5, 0.5)
            c.drawCentredString(B + T/2, B + 5, str(pn))
        c.showPage()
    
    # Back cover
    plc(c,D+'/back-cover.png',PG,PH)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(PG/2, PH - 85, "About the Story")
    c.setFont("Helvetica", 11)
    blurb=("Meet Pip, a tiny garden gnome who secretly helps his\n"
           "forgetful gardener, Mr. McGregor. With Bella the Butterfly\n"
           "and Tiptoe the Mouse, Pip shows that the best gift is\n"
           "a surprise given from the heart.\n\nAges 2-6 | StorySprout Press")
    lines=blurb.split('\n'); y=PH-115
    for line in lines:
        c.drawCentredString(PG/2,y,line); y-=16
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawCentredString(PG/2, 55, "StorySprout Press")
    c.showPage(); c.save()
    sz=os.path.getsize(O)/(1024*1024); print(f"  -> {O} ({sz:.1f} MB)")
    
    # Listing
    lis=r"""# Book #9: "Pip the Garden Gnome's Surprise" - Product Listing

## Amazon KDP Product Details
**Title:** Pip the Garden Gnome's Surprise: A Heartwarming Children's Picture Book About Kindness, Helping Others, and Garden Magic
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 2-6**
**Price (Print):** $9.99 | **Price (Digital):** $4.99

### Amazon Bullet Points
1. **MAGICAL GARDEN STORY** - Pip the tiny garden gnome secretly helps Mr. McGregor, proving the best gifts are surprises given from the heart.
2. **BEAUTIFUL GARDEN ILLUSTRATIONS** - 24 vibrant full-color illustrations of flowers, butterflies, and a magical gnome world.
3. **TEACHES KINDNESS & HELPING** - A gentle lesson about helping others without expecting anything in return.
4. **LOVELY CHARACTERS** - Meet Pip (red-hatted gnome), Bella the Butterfly, Tiptoe the Mouse, and Mr. McGregor the gardener.
5. **NATURE & GARDEN THEME** - Introduces children to garden life, flowers, and the joy of caring for living things.
6. **HIGH-QUALITY PRINT** - Square 8.5" x 8.5" format with durable pages.
7. **SURPRISE & DELIGHT** - A heartwarming story about the joy of giving and the magic that exists in every garden.

### Amazon Backend Keywords
children's picture book, garden gnome book, kindness story for kids, garden magic children's book, gnome story for toddlers, butterfly book for kids, helping others tale, nature picture book, flower garden story, mouse character book, bedtime garden story, gift giving book, preschool nature book, secret helper tale, garden friends book

### Etsy Listing
**Title:** Pip the Garden Gnome's Surprise - Printable Children's Storybook PDF | Garden Bedtime Story | Gnome Picture Book Digital Download
**Tags:** childrens storybook, printable book for kids, bedtime story pdf, garden gnome book, butterfly story, nature kids book, kindness tale, digital download, preschool book, garden magic, mouse book, homeschool resource
**Description:** Deep in a sun-drenched garden, Pip the tiny gnome secretly helps Mr. McGregor. With Bella the Butterfly and Tiptoe the Mouse, Pip discovers the joy of giving surprises! 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-book9-storybook.md','w') as f: f.write(lis)
    print("  -> /home/team/shared/listings-book9-storybook.md")
    print("BOOK #9 COMPLETE!")
if __name__=='__main__': go()