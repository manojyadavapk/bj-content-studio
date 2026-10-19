"""Dussehra Google Business Profile post, 1200x900. No phone numbers (Google rejects them)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np
W, H = 1200, 900
GF = '/usr/share/fonts/truetype/google-fonts/'; FD = '/root/.fonts/'; REPO = '/home/claude/bj-content-studio/'
MINT = (224, 241, 236); GOLD1 = (250, 222, 150); GOLD2 = (205, 150, 60); CREAM = (255, 244, 220)

def font(p, s, v=None):
    f = ImageFont.truetype(p, s, layout_engine=ImageFont.Layout.RAQM)
    if v: f.set_variation_by_name(v.encode())
    return f

bg = Image.open(REPO + 'out/W00-dussehra/dussehra_bg_landscape_v2.png').convert('RGB').resize((W, H), Image.LANCZOS)
cv = bg.convert('RGBA')
# soft shade on the left text area for legibility
g = np.zeros((H, W), np.float32)
g[:] = np.clip((np.linspace(1, 0, W) - 0.25) / 0.75, 0, 1)[None, :] ** 1.1 * 150
g[:150] *= np.linspace(0, 1, 150)[:, None]
sh = Image.new('RGBA', (W, H), (6, 18, 40, 0)); sh.putalpha(Image.fromarray(g.astype(np.uint8)))
cv = Image.alpha_composite(cv, sh)
ref = [cv]

def gold(xy, text, f):
    mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).text(xy, text, font=f, fill=255)
    s = Image.new('RGBA', (W, H), (0, 0, 0, 0)); s.putalpha(mask.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.6)))
    base = Image.alpha_composite(ref[0], ImageChops.offset(s, 0, 4))
    bb = mask.getbbox(); ga = np.zeros((H, W, 4), np.uint8)
    t = np.clip((np.arange(H) - bb[1]) / max(1, bb[3] - bb[1]), 0, 1)[:, None]
    for i in range(3): ga[..., i] = (GOLD1[i] * (1 - t) + GOLD2[i] * t).astype(np.uint8)
    ga[..., 3] = np.asarray(mask); ref[0] = Image.alpha_composite(base, Image.fromarray(ga))

def txt(xy, text, f, fill):
    mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).text(xy, text, font=f, fill=255)
    s = Image.new('RGBA', (W, H), (0, 0, 0, 0)); s.putalpha(mask.filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v * 0.75)))
    ref[0] = Image.alpha_composite(ref[0], ImageChops.offset(s, 0, 3)); ImageDraw.Draw(ref[0]).text(xy, text, font=f, fill=fill)

logo = Image.open(REPO + 'inputs/bj-logo.png').convert('RGBA'); lw = 92
logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
disc = Image.new('RGBA', (lw + 14, lw + 14), (0, 0, 0, 0)); ImageDraw.Draw(disc).ellipse([0, 0, lw + 13, lw + 13], fill=(255, 255, 255, 238))
ref[0].alpha_composite(disc, (60, 190)); ref[0].alpha_composite(logo, (67, 197 + (lw - logo.height) // 2))
txt((172, 206), 'BONES & JOINTS CLINIC', font(GF + 'Poppins-Bold.ttf', 30), (255, 255, 255))
txt((174, 246), 'Complete Orthopaedic Care', font(GF + 'Poppins-Medium.ttf', 20), MINT)

gold((64, 318), 'Happy', font(FD + 'PlayfairItalic.ttf', 86, 'Medium Italic'))
gold((58, 392), 'Dussehra', font(FD + 'Playfair.ttf', 124, 'Bold'))
txt((66, 548), 'दसऱ्याच्या हार्दिक शुभेच्छा!', font(FD + 'Mukta-Bold.ttf', 42), CREAM)
d = ImageDraw.Draw(ref[0]); d.line([(68, 616), (300, 616)], fill=GOLD2, width=3); d.ellipse([306, 611, 316, 621], fill=GOLD1)
txt((66, 634), 'सोनं घ्या, सोन्यासारखं राहा!', font(FD + 'Mukta-SemiBold.ttf', 32), (255, 255, 255))
txt((66, 680), 'Wishing your family good health and strength.', font(GF + 'Poppins-Regular.ttf', 26), (255, 255, 255))
txt((66, 752), 'Dr Manoj Yadav  ·  MS (Ortho)', font(GF + 'Poppins-Medium.ttf', 26), GOLD1)
txt((66, 792), 'Nallasopara West  ·  Virar East  ·  bonesnjointsclinic.com', font(GF + 'Poppins-Medium.ttf', 20), MINT)

out = ref[0].convert('RGB'); out.save('/home/claude/dussehra/dussehra_gbp.jpg', quality=93); print('saved')
