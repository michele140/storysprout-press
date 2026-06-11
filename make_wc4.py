#!/usr/bin/env python3
"""Build World Cup Book 4: Miami's Fiesta."""
import os, textwrap
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

TMP='/home/team/shared/.tmp_build';os.makedirs(TMP,exist_ok=True)
def plc(c,p,w,h):
    if not p or not os.path.exists(p):
        c.setFillColorRGB(1,1,1);c.rect(0,0,w,h,fill=1,stroke=0);return
    i=Image.open(p).convert('RGB');i=i.resize((int(w),int(h)),Image.LANCZOS)
    t=os.path.join(TMP,os.path.basename(p).replace('.png','.jpg'));i.save(t,'JPEG',quality=95);c.drawImage(t,0,0,w,h)

def go():
    print("WC #4: Miami's Fiesta")
    T=8.5*inch;B=0.125*inch;PG=T+2*B;PH=T+2*B;M=0.35*inch
    D='/home/team/shared/wc2026-miami-illustrations';O='/home/team/shared/wc4-miami-kdp.pdf'
    texts={
        2:'In Miami, the sun is always shining, and there\'s always a reason to celebrate! Mateo\'s house was full of music and the smell of Abuela\'s famous empanadas.\n\n"Mateo, stop dancing and help me with the cooler!" Abuela laughed.\n\n"I can\'t help it, Abuela! Argentina is playing at the Hard Rock Stadium today!"',
        3:'They drove across the bridge, seeing the blue water sparkle like diamonds.\n\n"Look, Abuela! Even the boats have flags!" Mateo pointed to a sailboat flying the sun-symbol of Argentina.',
        4:'The "Hard Rock Hero" stood tall. He was the coolest stadium in the world! He wore a facade painted with bright tropical leaves and huge "sunglasses" made of his white roof canopy.',
        5:'The stadium giant adjusted his sunglasses as if to say, "Let\'s get this party started!" "Bienvenidos!" a neon sign on his wall flashed. The energy was as warm as the Miami sun.',
        6:'Outside the gates, the "Fan Zone" was a sea of colors. A DJ played lively music, and fans from Argentina and Mexico were dancing together.\n\n"The World Cup is the world\'s biggest party, Mateo," Abuela said.',
        7:'Walking into the stands, the stadium felt wide and breezy. The bright blue seats matched the color of the sky.\n\n"Did you know this stadium keeps fans cool?" Abuela pointed to the huge white canopy umbrella.',
        8:'The pre-game show was a splash! Fountains sprayed water high into the air, making rainbows in the sunshine. The Hard Rock Hero flashed his neon pink and teal lights.',
        9:'Finally, Team Argentina walked out! The crowd went wild. Mateo held his sign high, screaming at the top of his lungs. The stadium\'s corner spikes vibrated with excitement.',
        10:'*TWEET!* The game began! Argentina\'s players moved the ball like they were dancing on the grass. Mexico was just as fast, their green jerseys flashing like light.',
        11:'Suddenly, the Argentinian star player took a shot from far away. *ZOOM!* The ball curled into the corner of the net. *GOALLLLLL!* Confetti rain fell from the canopy!',
        12:'Between periods, Mateo enjoyed a sweet mango-on-a-stick. "Soccer is a language everyone speaks," Abuela said. Mateo had made friends with a boy in a Mexico jersey.',
        13:'The next period began as the sky turned the color of cotton candy. The Hard Rock Hero turned on his neon lights — bright pink, electric blue, and sunny yellow.',
        14:'Mexico scored! A beautiful shot that zipped past the goalie. *SWISH!* The score was 1-1. Mateo clapped for the Mexican players. They were very good!',
        15:'The final minutes were full of tension. The crowd began a rhythmic chant. The Hard Rock Hero\'s walls pulsed with light, matching the heartbeat of the fans.',
        16:'Argentina took a powerful shot. *CLANG!* It hit the post and bounced away. "So close!" Mateo cried. Everyone was on the edge of their seats!',
        17:'*TWEET! TWEET! TWEET!* The match was over — a tie! Mateo watched as the players swapped jerseys. "It was a great fiesta," Abuela said.',
        18:'As they left, Mateo and his new friend Diego practiced their moves together. In Miami, the World Cup is about making new friends and sharing the joy.',
        19:'Leaving the stadium, Mateo looked back. The Hard Rock Hero was glowing in neon pink and green. "Goodnight, Hero," Mateo whispered.',
        20:'Back at home, Mateo couldn\'t stop smiling. He looked at the photo of him and Abuela at the stadium. A day he would never forget!',
        21:'Mateo fell asleep to the sound of Abuela\'s music. He dreamed of scoring the winning goal in a stadium made of light.',
        22:'The fans were gone, and the fiesta was over for now. The Hard Rock Hero settled down for a rest. Ready for the next match!',
        23:'The World Cup is coming to Miami! Are you ready for the fiesta? Hard Rock Stadium is waiting for you!',
        24:'**Fun Fact:** Hard Rock Stadium has an open-air canopy covering 90% of seats, keeping fans cool and dry. It also hosts the Formula 1 race!',
    }
    c=canvas.Canvas(O,pagesize=(PG,PH))
    plc(c,D+'/front-cover.png',PG,PH)
    c.setFont("Helvetica",12);c.setFillColorRGB(0.9,0.2,0.5)
    c.drawCentredString(PG/2,PH-185,"A StorySprout Press Book");c.showPage()
    for pn in range(1,25):
        plc(c,D+f'/page-{pn:02d}.png',PG,PH)
        if pn in texts:
            t=texts[pn];x0=B+M;y0=B+12;tw=T-2*M
            paras=t.split('\n\n');fs=13;lh=17
            nl=sum(max(1,len(textwrap.wrap(p,width=50))) for p in paras)
            th=max(90,min(200,nl*lh+20))
            c.setFillColorRGB(1,1,1,alpha=0.75)
            c.roundRect(x0,y0,tw,th,8,fill=1,stroke=0)
            c.setFillColorRGB(0.1,0.1,0.15);c.setFont("Helvetica",fs)
            cy=y0+th-lh-5
            for para in paras:
                for line in textwrap.wrap(para,width=50):
                    c.drawCentredString(B+T/2,cy,line);cy-=lh
                cy-=4
        if pn>1:
            c.setFont("Helvetica",9);c.setFillColorRGB(0.5,0.5,0.5)
            c.drawCentredString(B+T/2,B+5,str(pn))
        c.showPage()
    plc(c,D+'/back-cover.png',PG,PH)
    c.showPage();c.save()
    sz=os.path.getsize(O)/(1024*1024);print(f"  -> {O} ({sz:.1f} MB)")
    lis=r"""# World Cup Book #4: "Miami's Fiesta" - Product Listing
**Title:** Miami's Fiesta: A World Cup Soccer Story for Kids - Join Mateo at Hard Rock Stadium!
**Series:** World Cup Adventures (Book 4)
**Trim Size:** 8.5" x 8.5" square | **26 pages** | **Ages 5-9**
**Price (Print):** $9.99 | **Price (Digital):** $4.99
### Amazon Bullet Points
1. **WORLD CUP SOCCER ADVENTURE** - Join 8-year-old Mateo in Miami for an Argentina vs Mexico match at the neon-lit Hard Rock Stadium!
2. **AGES 5-9 FORMAT** - Longer, richer text with Miami culture, soccer action, and stadium fun facts.
3. **HARD ROCK HERO** - The stadium comes alive as a cool character with neon lights, tropical patterns, and giant sunglasses.
4. **TEACHES SPORTSMANSHIP** - Mateo cheers for Mexico's goal too and makes a new friend from the opposing team.
5. **MIAMI CULTURE** - Empanadas, mango-on-a-stick, salsa music, and the vibrant energy of Miami!
6. **BEAUTIFUL ILLUSTRATIONS** - 26 vibrant illustrations of the stadium, the match, and tropical Miami.
7. **FUN STADIUM FACT** - Hard Rock's canopy covers 90% of seats and it hosts the Formula 1 race!
### Amazon Backend Keywords
children's soccer book, world cup kids book, miami soccer story, hard rock stadium book, argentina vs mexico, miami kids book, sportsmanship children's, world cup 2026, stadium adventure, abuela and grandson, argentina soccer, miami culture, neon stadium, soccer story ages 5-9, tropical sports book
### Etsy Listing
**Title:** Miami's Fiesta - Printable Children's Soccer Storybook PDF | World Cup Miami | Hard Rock Stadium Digital Download
**Tags:** childrens storybook, printable book for kids, soccer book, world cup miami, hard rock stadium, miami kids, stadium adventure, sports book, digital download, ages 5-9, argentina soccer, miami culture
**Description:** Join Mateo and Abuela for an unforgettable day at Hard Rock Stadium! Argentina vs Mexico, neon lights, empanadas, and the spirit of Miami make this a story to remember. 24 illustrated pages. Print-ready 8.5" x 8.5". DIGITAL DOWNLOAD.
"""
    with open('/home/team/shared/listings-wc4-storybook.md','w') as f:f.write(lis)
    print("  -> /home/team/shared/listings-wc4-storybook.md")
    print("WC BOOK #4 COMPLETE!")
if __name__=='__main__':go()