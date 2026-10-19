"""Tall 1080x1920 festival status/story poster: Gemini background + Dr Yadav's REAL cut-out photo,
relit into the scene, premium typography, info panel with phones + real QR ("Scan to save contact").

usage: python3 compose_status.py <bg.png> <cutout.png> <out_prefix> <config.json>
"""
import json, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np

bg_path, cut_path, out_prefix, cfg_path = sys.argv[1:5]
C = json.load(open(cfg_path, encoding='utf-8'))
W, H = 1080, 1920
GF = '/usr/share/fonts/truetype/google-fonts/'
FD = '/root/.fonts/'
REPO = '/home/claude/bj-content-studio/'
MINT = (224, 241, 236); GOLD1 = (250, 222, 150); GOLD2 = (205, 150, 60); CREAM = (255, 244, 220)

def font(path, size, var=None):
    f = ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)
    if var:
        f.set_variation_by_name(var.encode())
    return f

# background, cover-fit
bg = Image.open(bg_path).convert('RGB')
s = max(W / bg.width, H / bg.height)
bg = bg.resize((round(bg.width * s), round(bg.height * s)), Image.LANCZOS)
x0 = (bg.width - W) // 2; y0 = bg.height - H
bg = bg.crop((x0, y0, x0 + W, y0 + H))
canvas = bg.convert('RGBA')

# soft darkening behind the text column (left) for legibility
gd = np.zeros((H, W), np.float32)
xs = np.linspace(1, 0, W)
gd[:] = np.clip((xs - 0.30) / 0.70, 0, 1) ** 1.2 * C.get('shade', 160)
gd[int(H * 0.70):] *= np.linspace(1, 0, H - int(H * 0.70))[:, None]
shade = Image.new('RGBA', (W, H), (6, 18, 40, 0)); shade.putalpha(Image.fromarray(gd.astype(np.uint8)))
canvas = Image.alpha_composite(canvas, shade)

# doctor cut-out, relit
dr = Image.open(cut_path).convert('RGBA')
dr = dr.crop(dr.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox())
th = C.get('photo_h', 1000)
dr = dr.resize((round(dr.width * th / dr.height), th), Image.LANCZOS)
rgb, a = dr.convert('RGB'), dr.getchannel('A')
a = a.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
arr = np.asarray(rgb).astype(np.float32)
arr[..., 0] *= 1.03; arr[..., 1] *= 0.99; arr[..., 2] *= 0.90
arr *= 0.94
arr *= np.linspace(1.06, 0.82, arr.shape[1])[None, :, None]
rgb = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
# fade the cropped left shoulder edge (lower half)
cols = np.ones(dr.width, np.float32)
low = np.asarray(a)[int(dr.height * 0.6):]
lx = int(np.argmax((low > 128).any(axis=0)))
cols[lx:lx + 90] = np.linspace(0, 1, 90) ** 0.8
m = np.ones((dr.height, dr.width), np.float32); m[int(dr.height * 0.55):, :] = cols[None, :]
a = Image.fromarray((np.asarray(a).astype(np.float32) * m).astype(np.uint8))
dr = rgb.copy(); dr.putalpha(a)
edge = ImageChops.subtract(a, a.filter(ImageFilter.MinFilter(9))).filter(ImageFilter.GaussianBlur(4))
rim = Image.new('RGBA', dr.size, (255, 200, 120, 0))
ra = np.asarray(edge).astype(np.float32) * np.linspace(1.0, 0.15, dr.width)[None, :] * 1.2
rim.putalpha(Image.fromarray(np.clip(ra, 0, 255).astype(np.uint8)))

px = W - dr.width + C.get('photo_dx', 95)
py = C['photo_bottom'] - dr.height
gl = Image.new('L', (W, H), 0)
ImageDraw.Draw(gl).ellipse([px + 40, py + 60, px + dr.width - 20, py + dr.height], fill=110)
glow = Image.new('RGBA', (W, H), (255, 190, 110, 0)); glow.putalpha(gl.filter(ImageFilter.GaussianBlur(100)))
canvas = Image.alpha_composite(canvas, glow)
for lay in (dr, rim):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); L.alpha_composite(lay, (px, py)); canvas = Image.alpha_composite(canvas, L)

# foreground (table / diyas) back in front of the coat
fg = bg.convert('RGBA'); fm = np.zeros((H, W), np.float32)
t = C['fg_top']; fm[t:] = 1; fm[t - 24:t] = np.linspace(0, 1, 24)[:, None]
fg.putalpha(Image.fromarray((fm * 255).astype(np.uint8)))
canvas = Image.alpha_composite(canvas, fg)

ref = [canvas]
def gold(xy, text, f):
    x, y = xy
    mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).text((x, y), text, font=f, fill=255)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(mask.filter(ImageFilter.GaussianBlur(7)).point(lambda v: int(v * 0.6)))
    base = Image.alpha_composite(ref[0], ImageChops.offset(sh, 0, 4))
    bb = mask.getbbox(); ga = np.zeros((H, W, 4), np.uint8)
    tt = np.clip((np.arange(H) - bb[1]) / max(1, bb[3] - bb[1]), 0, 1)[:, None]
    for i in range(3):
        ga[..., i] = (GOLD1[i] * (1 - tt) + GOLD2[i] * tt).astype(np.uint8)
    ga[..., 3] = np.asarray(mask)
    ref[0] = Image.alpha_composite(base, Image.fromarray(ga))

def shadowed(xy, text, f, fill):
    mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).text(xy, text, font=f, fill=255)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(mask.filter(ImageFilter.GaussianBlur(5)).point(lambda v: int(v * 0.7)))
    ref[0] = Image.alpha_composite(ref[0], ImageChops.offset(sh, 0, 3))
    ImageDraw.Draw(ref[0]).text(xy, text, font=f, fill=fill)

# header
logo = Image.open(REPO + 'inputs/bj-logo.png').convert('RGBA')
lw = 124; logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
disc = Image.new('RGBA', (lw + 16, lw + 16), (0, 0, 0, 0))
ImageDraw.Draw(disc).ellipse([0, 0, lw + 15, lw + 15], fill=(255, 255, 255, 238))
hy = C.get('header_y', 70)
ref[0].alpha_composite(disc, (56, hy)); ref[0].alpha_composite(logo, (64, hy + 8 + (lw - logo.height) // 2))
shadowed((210, hy + 28), 'BONES & JOINTS CLINIC', font(GF + 'Poppins-Bold.ttf', 36), (255, 255, 255))
shadowed((212, hy + 76), 'Complete Orthopaedic Care', font(GF + 'Poppins-Medium.ttf', 23), MINT)

# greeting block
y = C['greet_y']
gold((64, y), C['line1'], font(FD + 'PlayfairItalic.ttf', C.get('line1_size', 118), 'Medium Italic'))
gold((58, y + 112), C['line2'], font(FD + 'Playfair.ttf', C.get('line2_size', 150), 'Bold'))
y2 = y + 112 + C.get('line2_size', 150) + 40
shadowed((66, y2), C['marathi'], font(FD + 'Mukta-Bold.ttf', C.get('marathi_size', 50)), CREAM)
d = ImageDraw.Draw(ref[0])
y3 = y2 + 95
d.line([(68, y3), (330, y3)], fill=GOLD2, width=3); d.ellipse([336, y3 - 5, 346, y3 + 5], fill=GOLD1)
mf = font(GF + 'Poppins-Regular.ttf', 31)
for i, ln in enumerate(C['message']):
    shadowed((66, y3 + 26 + i * 44), ln, mf, (255, 255, 255))
yn = y3 + 26 + len(C['message']) * 44 + 50
shadowed((66, yn), 'Dr Manoj Yadav', font(GF + 'Poppins-Medium.ttf', 40), (255, 255, 255))
shadowed((66, yn + 54), 'MS (Ortho) · Orthopaedic Surgeon', font(GF + 'Poppins-Medium.ttf', 24), GOLD1)

# info panel. On WhatsApp/Instagram status the bottom ~150px sit under the "Reply" bar,
# so all contact content stays between panel top and H-160.
pt = C.get('panel_top', 1545)
ref[0].alpha_composite(Image.new('RGBA', (W, H - pt), (8, 26, 56, 232)), (0, pt))
d = ImageDraw.Draw(ref[0]); d.line([(0, pt), (W, pt)], fill=GOLD2, width=3)
lab = font(GF + 'Poppins-Medium.ttf', 22); ph = font(GF + 'Poppins-Bold.ttf', 33)
d.text((56, pt + 28), 'NALLASOPARA WEST', font=lab, fill=GOLD1)
d.text((56, pt + 58), '+91 87665 22099', font=ph, fill=(255, 255, 255))
d.text((420, pt + 28), 'VIRAR EAST', font=lab, fill=GOLD1)
d.text((420, pt + 58), '+91 92702 84859', font=ph, fill=(255, 255, 255))
d.text((56, pt + 124), 'bonesnjointsclinic.com  ·  @bonesnjointsclinic', font=font(GF + 'Poppins-Medium.ttf', 22), fill=MINT)
d.text((56, pt + 160), C.get('hours_line', 'Mon–Sat · Sunday closed'), font=font(GF + 'Poppins-Regular.ttf', 21), fill=(215, 222, 235))
qr = Image.open(REPO + 'inputs/qr-card.png').convert('RGBA'); qs = 140
card = Image.new('RGBA', (qs + 16, qs + 16), (0, 0, 0, 0))
ImageDraw.Draw(card).rounded_rectangle([0, 0, qs + 15, qs + 15], 14, fill=(255, 255, 255, 255))
card.alpha_composite(qr.resize((qs, qs), Image.NEAREST), (8, 8))
qx = W - qs - 16 - 44; ref[0].alpha_composite(card, (qx, pt + 18))
lf = font(GF + 'Poppins-Medium.ttf', 18); lbl = 'Scan to save contact'
d.text((qx + (qs + 16 - d.textlength(lbl, font=lf)) / 2, pt + 18 + qs + 16 + 6), lbl, font=lf, fill=GOLD1)
assert pt + 18 + qs + 16 + 30 < H - 150, 'contact content would sit under the status Reply bar'

out = ref[0].convert('RGB'); out.save(out_prefix + '.png'); out.save(out_prefix + '.jpg', quality=95)
print('saved', out_prefix)
