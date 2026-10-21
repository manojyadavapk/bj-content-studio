"""YouTube channel banner 2560x1440 for @bonesnjointsclinic.
Gemini seamless background + Dr Yadav's REAL photo cut-out (three-quarter), text set locally.
Everything that matters sits inside YouTube's mobile safe area (centre 1546x423)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np

W, H = 2560, 1440
SX0, SY0, SX1, SY1 = 507, 508, 2053, 931          # safe area (all devices)
CUT = '/tmp/claude-0/-home-claude/f9b31ed6-da9c-55f3-bdc2-46abd5e5e59b/scratchpad/poster/dr-three-quarter_cut.png'
BG = '/home/claude/bj-content-studio/out/W00-yt-banner/yt_banner_bg_v2.png'
OUT = '/home/claude/bj-content-studio/out/W00-yt-banner/yt_banner_final.png'
GF = '/usr/share/fonts/truetype/google-fonts/'; FD = '/root/.fonts/'
WHITE = (255, 255, 255); MINT = (224, 241, 236); NAVY = (13, 44, 92); GOLD = (230, 173, 60)

def F(path, size):
    return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)

bg = Image.open(BG).convert('RGB')
s = max(W / bg.width, H / bg.height)
bg = bg.resize((round(bg.width * s), round(bg.height * s)), Image.LANCZOS)
bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
canvas = bg.convert('RGBA')

# soft navy veil behind the text column so white type reads on the green part too
veil = np.zeros((H, W), np.float32)
xs = np.arange(W)
col = np.clip(1 - np.abs(xs - 1050) / 760, 0, 1) ** 1.4 * 120
veil[:] = col
ys = np.arange(H)[:, None]
veil *= np.clip(1 - np.abs(ys - 720) / 420, 0, 1) ** 0.8
v = Image.new('RGBA', (W, H), (8, 26, 58, 0)); v.putalpha(Image.fromarray(veil.astype(np.uint8)).filter(ImageFilter.GaussianBlur(40)))
canvas = Image.alpha_composite(canvas, v)

# --- real photo, head and shoulders, bottom on the safe-area floor, on the light right side
dr = Image.open(CUT).convert('RGBA')
dr = dr.crop(dr.getchannel('A').point(lambda p: 255 if p > 20 else 0).getbbox())
target_h = 470
dr = dr.resize((round(dr.width * target_h / dr.height), target_h), Image.LANCZOS)
a = dr.getchannel('A').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
arr = np.asarray(dr.convert('RGB')).astype(np.float32)
arr *= np.linspace(0.96, 1.03, arr.shape[1])[None, :, None]    # light from the right (bright side)
rgb = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
# fade the bottom crop of the coat into the background
am = np.asarray(a).astype(np.float32)
fade = np.ones(am.shape[0]); n = 90; fade[-n:] = np.linspace(1, 0, n)
am *= fade[:, None]
dr = rgb.copy(); dr.putalpha(Image.fromarray(am.astype(np.uint8)))
px = SX1 - dr.width + 10; py = SY1 - dr.height + 8
# soft glow behind him
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
cx, cy = px + dr.width // 2, py + dr.height // 2
gd.ellipse((cx - 330, cy - 290, cx + 330, cy + 290), fill=(255, 255, 255, 55))
canvas = Image.alpha_composite(canvas, glow.filter(ImageFilter.GaussianBlur(110)))
canvas.alpha_composite(dr, (px, py))

d = ImageDraw.Draw(canvas)
tx = SX0 + 40
logo = Image.open('/home/claude/bj-content-studio/inputs/bj-logo.png').convert('RGBA')
logo.thumbnail((120, 120), Image.LANCZOS)
# white disc behind the logo
disc = Image.new('RGBA', (132, 132), (0, 0, 0, 0)); ImageDraw.Draw(disc).ellipse((0, 0, 131, 131), fill=(255, 255, 255, 245))
canvas.alpha_composite(disc, (tx, SY0 + 22)); canvas.alpha_composite(logo, (tx + 6, SY0 + 28))
d.text((tx + 160, SY0 + 34), 'BONES & JOINTS CLINIC', font=F(GF + 'Poppins-Medium.ttf', 34), fill=MINT)
d.text((tx + 160, SY0 + 78), 'Complete Orthopaedic Care', font=F(GF + 'Poppins-Regular.ttf', 30), fill=(200, 230, 220))
d.text((tx, SY0 + 168), 'Dr Manoj Yadav', font=F(GF + 'Poppins-Bold.ttf', 96), fill=WHITE)
d.text((tx + 4, SY0 + 290), 'Orthopaedic Surgeon  ·  MBBS, MS (Orthopaedics)  ·  MMC Reg. 2017073017',
       font=F(GF + 'Poppins-Regular.ttf', 29), fill=MINT)
d.rounded_rectangle((tx, SY0 + 342, tx + 4, SY0 + 398), radius=2, fill=GOLD)
d.text((tx + 22, SY0 + 340), 'हाडं, सांधे आणि मणक्याची सोपी माहिती  ·  Bone, joint & spine health made simple',
       font=F(FD + 'Mukta-SemiBold.ttf', 34), fill=WHITE)

bar = Image.new('RGBA', (W, H), (0,0,0,0)); ImageDraw.Draw(bar).rounded_rectangle((SX0 + 20, SY1 + 52, SX0 + 1545, SY1 + 128), radius=38, fill=(13, 44, 92, 150))
canvas = Image.alpha_composite(canvas, bar); d = ImageDraw.Draw(canvas)
# outside the safe area (desktop/TV only): channel rhythm + website
d.text((SX0 + 40, SY1 + 70), 'New video every Wednesday  ·  bonesnjointsclinic.com  ·  Nallasopara West | Virar East',
       font=F(GF + 'Poppins-Medium.ttf', 34), fill=WHITE, stroke_width=0)

canvas.convert('RGB').save(OUT, optimize=True)
prev = canvas.convert('RGB').resize((1280, 720), Image.LANCZOS)
pd = ImageDraw.Draw(prev); pd.rectangle((SX0 / 2, SY0 / 2, SX1 / 2, SY1 / 2), outline=(255, 80, 80), width=2)
prev.save('/tmp/claude-0/-home-claude/f9b31ed6-da9c-55f3-bdc2-46abd5e5e59b/scratchpad/yt_banner_preview.jpg', quality=90)
print(OUT)
