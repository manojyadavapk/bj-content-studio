"""Instagram carousel (1080x1350): Osteoporotic spine fracture. Content from the website's
Osteoporosis page and guide SPEC-05 (English + Marathi)."""
import os, qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = '/home/claude/carousel/spine'; os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350
NAVY = (13, 44, 92); GREEN = (98, 170, 148); MINT = (224, 241, 236); GOLD = (230, 173, 60); RED = (200, 70, 60)
WHITE = (255, 255, 255); INK = (30, 45, 70)
FD = '/root/.fonts/'; REPO = '/home/claude/bj-content-studio/'; WEB = '/home/claude/bones-and-joints-website/img/'
N = 7
def F(n, s): return ImageFont.truetype(FD + n, s, layout_engine=ImageFont.Layout.RAQM)

def wrap(d, text, font, maxw):
    out = []
    for para in text.split('\n'):
        cur = ''
        for w in para.split(' '):
            t = (cur + ' ' + w).strip()
            if d.textlength(t, font=font) <= maxw: cur = t
            else: out.append(cur); cur = w
        out.append(cur)
    return out

def text(d, xy, s, font, fill, maxw, lh):
    x, y = xy
    for l in wrap(d, s, font, maxw):
        d.text((x, y), l, font=font, fill=fill); y += lh
    return y

LOGO = Image.open(REPO + 'inputs/bj-logo.png').convert('RGBA')
def logo(size):
    l = LOGO.resize((size, round(LOGO.height * size / LOGO.width)), Image.LANCZOS)
    disc = Image.new('RGBA', (size + 12, size + 12), (0, 0, 0, 0)); ImageDraw.Draw(disc).ellipse([0, 0, size + 11, size + 11], fill=WHITE + (255,))
    disc.alpha_composite(l, (6, 6 + (size - l.height) // 2)); return disc

def base(i, bg=MINT):
    im = Image.new('RGBA', (W, H), bg + (255,)); d = ImageDraw.Draw(im)
    im.alpha_composite(logo(64), (48, 1252))
    d.text((132, 1262), 'Bones & Joints Clinic', font=F('Poppins-Bold.ttf', 24), fill=NAVY)
    d.text((132, 1292), '@bonesnjointsclinic', font=F('Poppins-Medium.ttf', 20), fill=GREEN)
    pill = f'{i}/{N}'; f = F('Poppins-Bold.ttf', 24); tw = d.textlength(pill, font=f)
    d.rounded_rectangle([W - 48 - tw - 36, 1266, W - 48, 1310], 22, fill=NAVY); d.text((W - 48 - tw - 18, 1272), pill, font=f, fill=WHITE)
    return im, d

def heading(d, en, mr, y=90):
    d.rounded_rectangle([60, y + 6, 72, y + 120], 6, fill=GREEN)
    d.text((96, y), en, font=F('Poppins-Bold.ttf', 58), fill=NAVY)
    d.text((98, y + 78), mr, font=F('Mukta-Bold.ttf', 44), fill=GREEN)
    return y + 160

def bullets(d, y, items, icon='•', col=GREEN, gap=34):
    for en, mr in items:
        d.ellipse([84, y + 14, 112, y + 42], fill=col)
        if icon != '•': d.text((98, y + 28), icon, font=F('Poppins-Bold.ttf', 22), fill=WHITE, anchor='mm')
        y = text(d, (136, y), en, F('Poppins-SemiBold.ttf' if os.path.exists(FD + 'Poppins-SemiBold.ttf') else 'Poppins-Medium.ttf', 38), INK, 880, 50)
        y = text(d, (136, y + 2), mr, F('Mukta-SemiBold.ttf', 34), GREEN, 880, 46) + gap
    return y

def ai_tag(im, x, y):
    return
    d = ImageDraw.Draw(im); f = F('Poppins-Medium.ttf', 20); t = 'AI-generated illustration'; tw = d.textlength(t, font=f)
    d.rounded_rectangle([x - tw - 28, y, x, y + 38], 14, fill=NAVY + (220,)); d.text((x - tw - 14, y + 6), t, font=f, fill=WHITE)

def card_img(path, w, h):
    src = Image.open(path).convert('RGB'); s = max(w / src.width, h / src.height)
    src = src.resize((round(src.width * s), round(src.height * s)), Image.LANCZOS)
    x0, y0 = (src.width - w) // 2, (src.height - h) // 2
    src = src.crop((x0, y0, x0 + w, y0 + h)).convert('RGBA')
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 30, fill=255); src.putalpha(m); return src

slides = []
# 1 cover
im, d = base(1)
cov = Image.open(REPO + 'out/W00-carousel-spine/cover_stooped.png').convert('RGB').resize((W, H), Image.LANCZOS).convert('RGBA')
im.alpha_composite(cov.crop((0, 0, W, H - 190)), (0, 190))
sh = Image.new('RGBA', (W, 560), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
for yy in range(560): sd.line([(0, yy), (W, yy)], fill=MINT + (int(255 * min(1, (560 - yy) / 260)),))
im.alpha_composite(sh, (0, 0)); d = ImageDraw.Draw(im)
d.text((60, 70), 'Sudden back pain', font=F('Poppins-Bold.ttf', 76), fill=NAVY)
d.text((60, 160), 'after 50?', font=F('Poppins-Bold.ttf', 76), fill=NAVY)
d.text((62, 262), '५० नंतर अचानक पाठदुखी?', font=F('Mukta-Bold.ttf', 58), fill=GREEN)
yy = text(d, (62, 350), 'It may be a spine fracture from weak bones.', F('Poppins-Medium.ttf', 34), INK, 640, 46)
text(d, (62, yy + 4), 'ठिसूळ हाडांमुळे मणक्याचं फ्रॅक्चर असू शकतं.', F('Mukta-SemiBold.ttf', 32), INK, 640, 44)
ai_tag(im, W - 40, 1180)
d.rounded_rectangle([W - 250, 1100, W - 40, 1160], 30, fill=NAVY); d.text((W - 170, 1130), 'Swipe', font=F('Poppins-Bold.ttf', 30), fill=WHITE, anchor='mm'); d.text((W - 92, 1128), '→', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 34), fill=WHITE, anchor='mm')
# re-draw footer over the image
f2, d2 = base(1); im.alpha_composite(f2.crop((0, 1236, W, H)), (0, 1236)); slides.append(im)

# 2 warning signs
im, d = base(2)
y = heading(d, 'Warning signs', 'ही लक्षणं ओळखा')
y = bullets(d, y + 20, [
    ('Sudden, severe back pain — often with no fall', 'अचानक तीव्र पाठदुखी — बहुतेक वेळा पडल्याशिवाय'),
    ('You are losing height', 'उंची कमी होत आहे'),
    ('Your upper back is becoming rounded', 'पाठ पुढे वाकत आहे, कुबड येत आहे'),
    ('A bone broke after a simple fall from standing height', 'उभ्या उंचीवरून साध्या पडण्याने हाड मोडलं'),
], icon='!', col=RED)
d.rounded_rectangle([60, y + 10, W - 60, y + 200], 24, fill=WHITE)
yy = text(d, (90, y + 30), 'Any of these after 50? Get it checked — it can be treated.', F('Poppins-Medium.ttf', 32), NAVY, 880, 42)
text(d, (90, yy + 6), '५० नंतर यापैकी काही असेल तर तपासणी करा — उपचार शक्य आहेत.', F('Mukta-SemiBold.ttf', 30), GREEN, 880, 40)
slides.append(im)

# 3 why it happens
im, d = base(3)
y = heading(d, 'Why it happens', 'हे का होतं?')
c = card_img(REPO + 'out/W00-bsn/spine_fracture.png', 960, 470); im.alpha_composite(c, (60, y)); ai_tag(im, 1004, y + 418)
y += 500; d = ImageDraw.Draw(im)
y = text(d, (60, y), 'Osteoporosis makes bones thin and fragile. A vertebra (spine bone) can collapse with a minor fall — or even a strong bend.', F('Poppins-Medium.ttf', 34), INK, 960, 46)
y = text(d, (60, y + 10), 'ऑस्टिओपोरोसिसमध्ये हाड पातळ आणि ठिसूळ होतं. किरकोळ पडण्यानेही किंवा जोर लावल्यानेही मणका दबू शकतो.', F('Mukta-SemiBold.ttf', 32), GREEN, 960, 44)
text(d, (60, y + 14), 'There is no pain until something breaks.  ·  मोडेपर्यंत काहीच दुखत नाही.', F('Poppins-Bold.ttf', 28), NAVY, 960, 40)
slides.append(im)

# 4 lift the safe way
im, d = base(4)
y = heading(d, 'Lift the safe way', 'सुरक्षित पद्धतीने उचला')
for k, (fn, ok, en, mr) in enumerate([('POST-03_lifting-correct.jpg', True, 'Bend knees and hips, keep the back straight', 'गुडघे आणि खुबे वाका, पाठ सरळ ठेवा'),
                                       ('POST-03_lifting-wrong.jpg', False, "Don't bend forward with a rounded back", 'पाठ गोल करून कमरेतून पुढे वाकू नका')]):
    x = 60 + k * 490
    im.alpha_composite(card_img(WEB + fn, 470, 560), (x, y)); d = ImageDraw.Draw(im)
    cc = GREEN if ok else RED
    if ok: d.ellipse([x + 16, y + 16, x + 86, y + 86], fill=cc); d.text((x + 51, y + 51), '✓', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 44), fill=WHITE, anchor='mm')
    yy = text(d, (x + 6, y + 580), en, F('Poppins-SemiBold.ttf' if os.path.exists(FD + 'Poppins-SemiBold.ttf') else 'Poppins-Medium.ttf', 30), cc if not ok else NAVY, 460, 40)
    text(d, (x + 6, yy + 4), mr, F('Mukta-SemiBold.ttf', 28), GREEN if ok else RED, 460, 38)
d.rounded_rectangle([60, 1110, W - 60, 1220], 24, fill=WHITE)
text(d, (90, 1124), 'Also avoid forceful twisting and heavy lifting.', F('Poppins-Medium.ttf', 30), NAVY, 900, 40)
text(d, (90, 1166), 'कणा जोरात पिळणं आणि जड वजन उचलणं टाळा.', F('Mukta-SemiBold.ttf', 28), GREEN, 900, 38)
slides.append(im)

# 5 protect your bones
im, d = base(5)
y = heading(d, 'Protect your bones', 'हाडांचं संरक्षण करा')
bullets(d, y + 20, [
    ('Calcium and vitamin D every day', 'कॅल्शियम आणि व्हिटॅमिन डी रोज'),
    ('Brisk walking — 30 minutes on most days', 'जलद चालणे — बहुतेक दिवशी 30 मिनिटे'),
    ('Balance practice daily, holding the kitchen counter', 'रोज ओटा धरून तोलाचा सराव'),
    ('Sunlight — 10–15 minutes daily, between 10 am and 2 pm', 'रोज 10–15 मिनिटं ऊन (सकाळी 10 ते दुपारी 2)'),
    ('Make the home fall-safe: no loose rugs, good lighting', 'घरात पडण्याचा धोका टाळा: सैल चटई नको, पुरेसा उजेड'),
], icon='✓' if False else '•', col=GREEN, gap=26)
slides.append(im)

# 6 myth vs fact
im, d = base(6, bg=NAVY)
d = ImageDraw.Draw(im)
d.text((60, 90), 'MYTH', font=F('Poppins-Bold.ttf', 34), fill=GOLD)
y = text(d, (60, 140), '“Bones get weak with age. Nothing can be done.”', F('Poppins-Bold.ttf', 56), WHITE, 960, 70)
y = text(d, (60, y + 10), '“वयानुसार हाडं कमजोर होतात, काही करता येत नाही.”', F('Mukta-Bold.ttf', 46), MINT, 960, 60)
d.rectangle([60, y + 40, 260, y + 44], fill=GOLD)
d.text((60, y + 80), 'FACT', font=F('Poppins-Bold.ttf', 34), fill=GREEN)
y = text(d, (60, y + 130), 'Weak bones can be tested with a bone density (DEXA) scan, and treated. Treatment measurably reduces fractures.', F('Poppins-Medium.ttf', 38), WHITE, 960, 52)
y = text(d, (60, y + 14), 'हाडांची घनता (DEXA स्कॅन) तपासता येते आणि उपचार करता येतात. उपचाराने फ्रॅक्चरचा धोका कमी होतो.', F('Mukta-SemiBold.ttf', 34), MINT, 960, 48)
text(d, (60, y + 30), "Take bone medicine as advised — don't stop because you feel fine.", F('Poppins-Medium.ttf', 30), GOLD, 960, 42)
f2, _ = base(6); im.alpha_composite(f2.crop((0, 1236, W, H)), (0, 1236)); slides.append(im)

# 7 free guide
im, d = base(7)
y = heading(d, 'Free guide', 'मोफत मार्गदर्शिका')
d.rounded_rectangle([60, y + 10, W - 60, y + 560], 30, fill=WHITE)
d.text((100, y + 50), 'Living with Osteoporosis', font=F('Poppins-Bold.ttf', 46), fill=NAVY)
d.text((100, y + 112), 'ऑस्टिओपोरोसिससह जगणे', font=F('Mukta-Bold.ttf', 42), fill=GREEN)
d.text((100, y + 180), 'English  ·  हिंदी  ·  मराठी', font=F('Mukta-SemiBold.ttf', 34), fill=INK)
d.text((100, y + 236), 'Free to download — no sign-up.', font=F('Poppins-Medium.ttf', 30), fill=INK)
url = 'https://bonesnjointsclinic.com/g/SPEC-05'
q = qrcode.QRCode(border=2, box_size=10); q.add_data(url); q.make(fit=True)
qi = q.make_image(fill_color='#0D2C5C', back_color='white').convert('RGBA').resize((260, 260), Image.NEAREST)
im.alpha_composite(qi, (W - 60 - 40 - 260, y + 280)); d = ImageDraw.Draw(im)
d.text((100, y + 330), 'bonesnjointsclinic.com', font=F('Poppins-Bold.ttf', 34), fill=NAVY)
d.text((100, y + 378), '/g/SPEC-05', font=F('Poppins-Bold.ttf', 34), fill=GREEN)
d.text((100, y + 440), 'Scan to open the guide', font=F('Poppins-Medium.ttf', 26), fill=INK)
y += 600
d.text((60, y), 'Dr Manoj Yadav', font=F('Poppins-Bold.ttf', 40), fill=NAVY)
d.text((60, y + 54), 'MS (Ortho) · Orthopaedic Surgeon · MMC Reg. 2017073017', font=F('Poppins-Medium.ttf', 28), fill=INK)
d.text((60, y + 100), 'For awareness only. Please consult your doctor.', font=F('Poppins-Regular.ttf', 26), fill=INK)
slides.append(im)

for k, s in enumerate(slides, 1):
    s.convert('RGB').save(f'{OUT}/spine_{k}.jpg', quality=93)
print('saved', len(slides))
