"""Compose the B&J Diwali poster: Gemini background + REAL cut-out photo, relit to match the scene,
with premium typography. Output 1080x1350."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance
import numpy as np

W, H = 1080, 1350
D = '/tmp/claude-0/-home-claude/f9b31ed6-da9c-55f3-bdc2-46abd5e5e59b/scratchpad/poster/'
GF = '/usr/share/fonts/truetype/google-fonts/'
FD = '/root/.fonts/'
NAVY = (13, 44, 92); MINT = (224, 241, 236); GREEN = (98, 170, 148)
GOLD1 = (250, 222, 150); GOLD2 = (205, 150, 60); CREAM = (255, 244, 220)
which = sys.argv[1] if len(sys.argv) > 1 else 'dr-front'

def font(path, size, var=None):
    f = ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)
    if var:
        f.set_variation_by_name(var.encode() if isinstance(var,str) else var)
    return f

# --- background
bg = Image.open('/home/claude/bj-content-studio/out/W00-bg/diwali_bg_navy.png').convert('RGB')
s = H / bg.height
bg = bg.resize((round(bg.width * s), H), Image.LANCZOS)
x0 = (bg.width - W) // 2
bg = bg.crop((x0, 0, x0 + W, H))
canvas = bg.convert('RGBA')

# darken the left text column slightly for legibility (soft gradient)
grad = Image.new('L', (W, H))
gd = np.zeros((H, W), np.float32)
xs = np.linspace(1, 0, W)
gd[:] = np.clip((xs - 0.35) / 0.65, 0, 1) ** 1.3 * 150
grad = Image.fromarray(gd.astype(np.uint8))
shade = Image.new('RGBA', (W, H), (6, 18, 40, 0)); shade.putalpha(grad)
canvas = Image.alpha_composite(canvas, shade)

# --- doctor cut-out, relit to match warm scene
dr = Image.open(D + f'{which}_cut.png').convert('RGBA')
bbox = dr.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
dr = dr.crop(bbox)
target_h = 880
dr = dr.resize((round(dr.width * target_h / dr.height), target_h), Image.LANCZOS)
rgb, a = dr.convert('RGB'), dr.getchannel('A')
a = a.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
# warm grade: slight warm tint + a touch lower brightness so whites aren't paper-flat
arr = np.asarray(rgb).astype(np.float32)
arr[..., 0] *= 1.03; arr[..., 1] *= 0.99; arr[..., 2] *= 0.90
arr *= 0.94
# light falls from the left: horizontal gradient brighter on left edge, darker right
g = np.linspace(1.06, 0.82, arr.shape[1])[None, :, None]
arr *= g
rgb = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
dr = rgb.copy(); dr.putalpha(a)
# golden rim light on the left edge
edge = ImageChops.subtract(a, a.filter(ImageFilter.MinFilter(9)))
edge = edge.filter(ImageFilter.GaussianBlur(4))
rim = Image.new('RGBA', dr.size, (255, 200, 120, 0))
rim_a = np.asarray(edge).astype(np.float32)
rim_a *= np.linspace(1.0, 0.15, dr.width)[None, :]
rim.putalpha(Image.fromarray(np.clip(rim_a * 1.2, 0, 255).astype(np.uint8)))
# fade the bottom of the cut-out so it melts into the diya row
fade = np.ones((dr.height, dr.width), np.float32)
fstart = int(dr.height * 0.97)
fade[fstart:] = np.linspace(1, 0, dr.height - fstart)[:, None]
cols = np.ones(dr.width, np.float32)
acol = (np.asarray(a) > 128).any(axis=0); first = int(np.argmax(acol))
lowrows = np.asarray(a)[int(dr.height*0.6):]
lx = int(np.argmax((lowrows > 128).any(axis=0)))
cols[lx:lx+90] = np.linspace(0, 1, 90) ** 0.8
bottom = np.ones((dr.height, dr.width), np.float32)
bottom[int(dr.height*0.55):, :] = cols[None, :]
fade = fade * bottom
a2 = Image.fromarray((np.asarray(a).astype(np.float32) * fade).astype(np.uint8))
dr.putalpha(a2)
rim_a2 = Image.fromarray((np.asarray(rim.getchannel('A')).astype(np.float32) * fade).astype(np.uint8))
rim.putalpha(rim_a2)

px = W - dr.width + 95
py = 1110 - dr.height
# soft glow behind doctor (separates him from the background)
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
gl = Image.new('L', (W, H), 0)
ImageDraw.Draw(gl).ellipse([px + 40, py + 60, px + dr.width - 20, py + dr.height], fill=110)
gl = gl.filter(ImageFilter.GaussianBlur(90))
glow = Image.new('RGBA', (W, H), (255, 190, 110, 0)); glow.putalpha(gl)
canvas = Image.alpha_composite(canvas, glow)
layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); layer.alpha_composite(dr, (px, py))
canvas = Image.alpha_composite(canvas, layer)
layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); layer.alpha_composite(rim, (px, py))
canvas = Image.alpha_composite(canvas, layer)

# bring the diya row back IN FRONT of the doctor (depth)
fg = bg.convert('RGBA')
m = np.zeros((H, W), np.float32)
top = 1040
m[top:] = 1
m[top - 22:top] = np.linspace(0, 1, 22)[:, None]
fg.putalpha(Image.fromarray((m * 255).astype(np.uint8)))
canvas = Image.alpha_composite(canvas, fg)

d = ImageDraw.Draw(canvas)

def gold_text(xy, text, f, anchor='la'):
    """Gold vertical gradient text with soft shadow."""
    x, y = xy
    mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mask).text((x, y), text, font=f, fill=255, anchor=anchor)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(mask.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.55)))
    base = Image.alpha_composite(canvas_ref[0], ImageChops.offset(sh, 0, 4))
    bb = mask.getbbox()
    gradimg = Image.new('RGBA', (W, H))
    ga = np.zeros((H, W, 4), np.uint8)
    t = np.clip((np.arange(H) - bb[1]) / max(1, bb[3] - bb[1]), 0, 1)[:, None]
    for i in range(3):
        ga[..., i] = (GOLD1[i] * (1 - t) + GOLD2[i] * t).astype(np.uint8)
    ga[..., 3] = np.asarray(mask)
    canvas_ref[0] = Image.alpha_composite(base, Image.fromarray(ga))

canvas_ref = [canvas]
# --- header: logo + name
logo = Image.open('/home/claude/bj-content-studio/inputs/bj-logo.png').convert('RGBA')
lw = 118; logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
# white disc behind logo so it reads on dark
disc = Image.new('RGBA', (lw + 16, lw + 16), (0, 0, 0, 0))
ImageDraw.Draw(disc).ellipse([0, 0, lw + 15, lw + 15], fill=(255, 255, 255, 235))
canvas_ref[0].alpha_composite(disc, (56, 52)); canvas_ref[0].alpha_composite(logo, (64, 60 + (lw - logo.height) // 2))
d = ImageDraw.Draw(canvas_ref[0])
d.text((200, 78), 'BONES & JOINTS CLINIC', font=font(GF + 'Poppins-Bold.ttf', 34), fill=(255, 255, 255))
d.text((202, 124), 'Complete Orthopaedic Care', font=font(GF + 'Poppins-Medium.ttf', 22), fill=MINT)

# --- greeting
gold_text((64, 300), 'Happy', font(FD + 'PlayfairItalic.ttf', 112, 'Medium Italic'))
gold_text((60, 400), 'Diwali', font(FD + 'Playfair.ttf', 168, 'Bold'))
d = ImageDraw.Draw(canvas_ref[0])
d.text((66, 605), 'दीपावलीच्या हार्दिक शुभेच्छा!', font=font(FD + 'Mukta-Bold.ttf', 50), fill=CREAM)
d.line([(68, 690), (330, 690)], fill=GOLD2, width=3)
d.ellipse([336, 685, 346, 695], fill=GOLD1)
msg = font(GF + 'Poppins-Regular.ttf', 30)
d.text((66, 716), 'Wishing you light,', font=msg, fill=(255, 255, 255))
d.text((66, 756), 'good health and strong bones.', font=msg, fill=(255, 255, 255))
d.text((66, 840), 'Dr Manoj Yadav', font=font(GF + 'Poppins-Medium.ttf', 38), fill=(255, 255, 255))
d.text((66, 890), 'MS (Ortho) · Orthopaedic Surgeon', font=font(GF + 'Poppins-Medium.ttf', 23), fill=GOLD1)

# --- bottom info panel (glass)
panel_top = 1188
pnl = Image.new('RGBA', (W, H - panel_top), (8, 26, 56, 225))
canvas_ref[0].alpha_composite(pnl, (0, panel_top))
d = ImageDraw.Draw(canvas_ref[0])
d.line([(0, panel_top), (W, panel_top)], fill=GOLD2, width=3)
lab = font(GF + 'Poppins-Medium.ttf', 21); ph = font(GF + 'Poppins-Bold.ttf', 32)
d.text((56, panel_top + 26), 'NALLASOPARA WEST', font=lab, fill=GOLD1)
d.text((56, panel_top + 56), '+91 87665 22099', font=ph, fill=(255, 255, 255))
d.text((420, panel_top + 26), 'VIRAR EAST', font=lab, fill=GOLD1)
d.text((420, panel_top + 56), '+91 92702 84859', font=ph, fill=(255, 255, 255))
d.text((56, panel_top + 112), 'bonesnjointsclinic.com  ·  @bonesnjointsclinic', font=font(GF + 'Poppins-Medium.ttf', 22), fill=MINT)
# QR card
qr = Image.open('/home/claude/bj-content-studio/inputs/qr-card.png').convert('RGBA')
qs = 128
card = Image.new('RGBA', (qs + 16, qs + 16), (0, 0, 0, 0))
ImageDraw.Draw(card).rounded_rectangle([0, 0, qs + 15, qs + 15], 14, fill=(255, 255, 255, 255))
card.alpha_composite(qr.resize((qs, qs), Image.NEAREST), (8, 8))
canvas_ref[0].alpha_composite(card, (W - qs - 16 - 44, panel_top + 8))
d.text((W - 44 - (qs + 16) - 150, panel_top + 112), 'Scan to save', font=font(GF + 'Poppins-Medium.ttf', 20), fill=MINT)

out = canvas_ref[0].convert('RGB')
out.save(D + f'diwali_{which}.png')
out.save(D + f'diwali_{which}.jpg', quality=95)
print('saved')
