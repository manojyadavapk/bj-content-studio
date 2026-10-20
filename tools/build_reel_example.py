"""Bone-Strong Naari Reel (v1 draft): tightened talk, 3:4 crop in a 9:16 frame,
Marathi + English captions, brand bands, end card. All local (patient footage never leaves)."""
import json, subprocess, os
from PIL import Image, ImageDraw, ImageFont

SRC = '/mnt/user-data/uploads/VID-20261019-WA0136_2.mp4'
AUD = '/home/claude/bsn/clean_full.wav'
OUT = '/home/claude/bsn/reel'
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
NAVY = (13, 44, 92); GREEN = (98, 170, 148); MINT = (224, 241, 236); GOLD = (230, 173, 60)
FD = '/root/.fonts/'
def F(name, size): return ImageFont.truetype(FD + name, size, layout_engine=ImageFont.Layout.RAQM)

# ---- speech segments -> kept intervals (pauses shortened) ----
p = [tuple(map(float, l.split())) for l in open('/home/claude/bsn/pauses.txt')]
segs, prev = [], 0.0
for s, e in p:
    if s - prev > 0.2: segs.append((prev, s))
    prev = e
segs.append((prev, 215.5))
import sys
RANGES = json.loads(sys.argv[1]) if len(sys.argv) > 1 else [[0, 216]]
NAME = sys.argv[2] if len(sys.argv) > 2 else 'BJ_BoneStrongNaari_reel_v3'
segs = [(max(a, r0), min(b, r1)) for a, b in segs for r0, r1 in RANGES if min(b, r1) - max(a, r0) > 0.15]
keep = []
for a, b in segs:
    rr = [r for r in RANGES if r[0] <= a + 0.01 and b <= r[1] + 0.01][0]
    a, b = max(rr[0], a - 0.15), min(rr[1], b + 0.22)
    if keep and a <= keep[-1][1] + 0.05: keep[-1] = (keep[-1][0], b)
    else: keep.append((a, b))

def out_t(t):
    """map source time -> output time"""
    acc = 0.0
    for a, b in keep:
        if t < a: return acc
        if t <= b: return acc + (t - a)
        acc += b - a
    return acc
TOTAL = sum(b - a for a, b in keep)

# ---- captions: (src_start, src_end, marathi, english) ----
CAP = [
 (0.9, 7.5,  'आपल्यासमोर ७५ वर्षांच्या आजी आहेत', 'This is a 75-year-old mother.'),
 (8.4, 16.4, 'त्यांना कंबरदुखी आहे, आणि कंबर पुढे वाकली आहे', 'She has back pain, and her back has bent forward.'),
 (17.2, 24.0, 'चला, ऑस्टियोपोरोसिसबद्दल बोलूया', "Let's talk about osteoporosis."),
 (24.5, 30.9, 'हाडांची गुणवत्ता तशीच राहते, पण हाडांचं प्रमाण कमी होतं', 'Bone quality stays the same, but the amount of bone goes down.'),
 (32.5, 38.7, 'ऑस्टियोपोरोसिसचे दोन मुख्य प्रकार आहेत', 'There are two main types of osteoporosis.'),
 (39.4, 48.2, '१. पोस्ट-मेनोपॉझल — ५० वर्षांनंतर (पाळी बंद झाल्यावर)', '1. Post-menopausal — after age 50 (after periods stop).'),
 (49.5, 55.7, '२. सेनाइल (वयामुळे) — ७५ वर्षांनंतर', '2. Senile (age-related) — after age 75.'),
 (57.6, 59.3, 'आजींना हे दोन्ही प्रकार लागू होतात', 'This mother has both types.'),
 (60.0, 67.3, '५० वर्षांवरील दर ३ पैकी १ महिलेला फ्रॅक्चर होतं', '1 in 3 women over 50 will break a bone'),
 (68.1, 75.1, 'हाडं कमजोर झाल्यामुळे — ऑस्टियोपोरोसिसमुळे', 'because of weak bones — osteoporosis.'),
 (75.9, 89.9, 'आणि बहुतेकांना हे माहितीच नसतं', "And most of them don't even know it."),
 (91.3, 97.3, 'हे तेव्हाच कळतं, जेव्हा हाड मोडतं', 'They find out only when a bone breaks.'),
 (97.8, 106.8, 'आजींच्या कण्याचं हाड मोडून पुढे वाकलं — म्हणून कंबरदुखी', 'Her spine bone broke and bent forward — that is her back pain.'),
 (107.6, 112.0, 'याआधी त्यांना कंबरदुखी नव्हती', 'She had no back pain before this.'),
 (113.8, 117.9, 'याच जागरूकतेसाठी हा व्हिडिओ', 'That is why we made this awareness video.'),
 (119.5, 126.7, 'मग ऑस्टियोपोरोसिस टाळायचा कसा?', 'So how do we prevent osteoporosis?'),
 (127.1, 135.6, 'कॅल्शियम आणि व्हिटॅमिन D आवश्यक आहे', 'We need calcium and vitamin D.'),
 (136.4, 141.9, 'आहारात दूध, दही, नाचणी, हिरव्या भाज्या', 'Eat milk, curd, ragi and green vegetables.'),
 (143.2, 151.7, 'व्हिटॅमिन D साठी रोज १०–१५ मिनिटं ऊन — सकाळी १० ते दुपारी २ दरम्यान', 'For vitamin D: 10–15 minutes of sun daily, between 10 am and 2 pm.'),
 (152.9, 157.8, 'व्यायाम हाडांसाठी खूप महत्त्वाचा आहे', 'Exercise is very important for bones.'),
 (159.2, 165.8, 'हाडं मजबूत ठेवण्यासाठी थोडं वजन उचला — डॉक्टरांच्या सल्ल्याने', 'To keep bones strong, lift some weight — as advised by your doctor.'),
 (166.2, 173.7, '५ ते १० किलोसुद्धा पुरेसं. आधी फ्रॅक्चर झालं असेल तर डॉक्टरांना विचारा', 'Even 5–10 kg is enough. Had a fracture before? Ask your doctor first.'),
 (177.0, 186.4, 'हा व्हिडिओ सर्व आई-बहिणींना शेअर करा', 'Share this video with all mothers and sisters'),
 (187.3, 195.1, 'आणि घरातील वयस्कर मंडळींना', 'and the elderly in your family,'),
 (196.3, 206.7, 'ऑस्टियोपोरोसिस हा एक छुपा आजार आहे', 'because osteoporosis is a hidden disease.'),
 (207.0, 214.4, 'म्हणून जागरूकता आवश्यक आहे. धन्यवाद!', 'That is why awareness matters. Thank you!'),
]

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(' '), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def caption_png(i, mr, en):
    im = Image.new('RGBA', (W, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fm, fe = F('Mukta-Bold.ttf', 58), F('Poppins-Medium.ttf', 34)
    lm, le = wrap(d, mr, fm, 940), wrap(d, en, fe, 940)
    hm, he = 72, 46
    h = len(lm) * hm + len(le) * he + 44
    y0 = 300 - h
    d.rounded_rectangle([40, y0, W - 40, 300], 26, fill=(8, 26, 56, 215))
    d.rounded_rectangle([40, y0, 52, 300], 6, fill=GREEN + (255,))
    y = y0 + 16
    for l in lm:
        d.text(((W - d.textlength(l, font=fm)) / 2, y), l, font=fm, fill=(255, 255, 255)); y += hm
    for l in le:
        d.text(((W - d.textlength(l, font=fe)) / 2, y), l, font=fe, fill=MINT); y += he
    path = f'{OUT}/cap_{i:02d}.png'; im.save(path); return path

def frame_png():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 250], fill=NAVY + (255,)); d.rectangle([0, 246, W, 250], fill=GOLD + (255,))
    logo = Image.open('/home/claude/bj-content-studio/inputs/bj-logo.png').convert('RGBA')
    lw = 120; logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    disc = Image.new('RGBA', (lw + 16, lw + 16), (0, 0, 0, 0)); ImageDraw.Draw(disc).ellipse([0, 0, lw + 15, lw + 15], fill=(255, 255, 255, 255))
    im.alpha_composite(disc, (48, 92)); im.alpha_composite(logo, (56, 100 + (lw - logo.height) // 2))
    d.text((200, 96), 'BONE-STRONG NAARI', font=F('Poppins-Bold.ttf', 50), fill=(255, 255, 255))
    d.text((202, 164), 'ऑस्टियोपोरोसिस जागरूकता · Osteoporosis awareness', font=F('Mukta-SemiBold.ttf', 32), fill=MINT)
    d.rectangle([0, 1690, W, H], fill=NAVY + (255,)); d.rectangle([0, 1690, W, 1694], fill=GOLD + (255,))
    d.text((56, 1712), 'Dr Manoj Yadav', font=F('Poppins-Bold.ttf', 40), fill=(255, 255, 255))
    d.text((56, 1764), 'MS (Ortho) · Orthopaedic Surgeon · MMC Reg. 2017073017', font=F('Poppins-Medium.ttf', 26), fill=MINT)
    d.text((56, 1806), 'Bones & Joints Clinic · @bonesnjointsclinic', font=F('Poppins-Medium.ttf', 26), fill=GOLD)
    im.save(f'{OUT}/frame.png')

def endcard_png():
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    logo = Image.open('/home/claude/bj-content-studio/inputs/bj-logo.png').convert('RGBA')
    lw = 300; logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    disc = Image.new('RGBA', (lw + 40, lw + 40), (0, 0, 0, 0)); ImageDraw.Draw(disc).ellipse([0, 0, lw + 39, lw + 39], fill=(255, 255, 255, 255))
    im.paste(disc, ((W - lw - 40) // 2, 380), disc); im.paste(logo, ((W - lw) // 2, 400 + (lw - logo.height) // 2), logo)
    def c(y, t, f, col): d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=col)
    c(820, 'मजबूत हाडं, मजबूत आयुष्य', F('Mukta-Bold.ttf', 76), (255, 255, 255))
    c(920, 'Strong bones, strong life', F('Poppins-Medium.ttf', 44), MINT)
    d.rectangle([(W - 200) // 2, 1010, (W + 200) // 2, 1014], fill=GOLD)
    c(1060, 'Dr Manoj Yadav', F('Poppins-Bold.ttf', 56), (255, 255, 255))
    c(1140, 'MS (Ortho) · Orthopaedic Surgeon', F('Poppins-Medium.ttf', 34), MINT)
    c(1190, 'MMC Reg. 2017073017', F('Poppins-Medium.ttf', 34), MINT)
    c(1290, 'Bones & Joints Clinic', F('Poppins-Bold.ttf', 40), GOLD)
    c(1345, 'Nallasopara West · Virar East', F('Poppins-Medium.ttf', 32), (220, 228, 240))
    c(1395, '@bonesnjointsclinic · bonesnjointsclinic.com', F('Poppins-Medium.ttf', 32), (220, 228, 240))
    c(1520, 'For awareness only. Please consult your doctor.', F('Poppins-Regular.ttf', 28), (190, 200, 215))
    im.save(f'{OUT}/endcard.png')

frame_png(); endcard_png()
ILL = '/home/claude/bj-content-studio/out/W00-bsn/'
CARDS = [('bone_compare', 24.5), ('postmeno_woman', 39.4), ('senile_couple', 49.5), ('one_in_three', 60.0),
         ('spine_fracture', 102.3), ('calcium_foods', 136.4), ('sunlight', 143.2), ('light_weights', 159.2), ('family_share', 177.0)]
def card_png(name):
    from PIL import ImageFilter
    src = Image.open(ILL + name + '.png').convert('RGB')
    bg = src.resize((round(1440 * src.width / src.height), 1440), Image.LANCZOS)
    x0 = (bg.width - 1080) // 2; bg = bg.crop((x0, 0, x0 + 1080, 1440)).filter(ImageFilter.GaussianBlur(28))
    bg = Image.blend(bg, Image.new('RGB', bg.size, (224, 241, 236)), 0.35)
    fg = src.resize((1080, round(1080 * src.height / src.width)), Image.LANCZOS)
    bg.paste(fg, (0, (1440 - fg.height) // 2 - 120))
    d = ImageDraw.Draw(bg); f = F('Poppins-Medium.ttf', 24); t = 'AI-generated illustration'; tw = d.textlength(t, font=f)
    d.rounded_rectangle([1080 - tw - 52, 40, 1040, 84], 16, fill=(13, 44, 92)); d.text((1080 - tw - 38, 46), t, font=f, fill=(255, 255, 255))
    p = f'{OUT}/card_{name}.png'; bg.save(p)
    clip = f'{OUT}/card_{name}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', p, '-vf',
        "scale=2160:2880,zoompan=z='1+0.0006*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=120:s=1080x1440:fps=30,fade=t=in:st=0:d=0.25,fade=t=out:st=3.75:d=0.25",
        '-frames:v', '120', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', clip], check=True)
    return clip
cards = []
for name, st in CARDS:
    if any(r0 <= st <= r1 - 1 for r0, r1 in RANGES):
        cards.append((out_t(st), out_t(st) + 4.0, card_png(name)))
CAP = [c for c in CAP if any(min(c[1], r1) - max(c[0], r0) > 0.5 for r0, r1 in RANGES)]
caps = [(out_t(a), out_t(b), caption_png(i, mr, en)) for i, (a, b, mr, en) in enumerate(CAP)]
# extend each caption to the next one's start (no flicker), max +1.2 s
caps2 = []
for i, (a, b, pth) in enumerate(caps):
    nxt = caps[i + 1][0] if i + 1 < len(caps) else TOTAL
    caps2.append((a, min(nxt, b + 1.2), pth))

sel = '+'.join(f'between(t,{a:.3f},{b:.3f})' for a, b in keep)
# crop centre per shot (source time), 540x720 crop of the 1280x720 frame
cx = "if(lt(t,3.5),0,if(lt(t,7.5),370*(t-3.5)/4,if(lt(t,16.4),370,if(lt(t,76.4),350,if(lt(t,118.5),340,if(lt(t,146.7),250,if(lt(t,161.6),210,230)))))))"
inputs = ['-i', SRC, '-i', AUD, '-i', f'{OUT}/frame.png']
for _, _, pth in caps2: inputs += ['-i', pth]
for _, _, pth in cards: inputs += ['-i', pth]
HAS_BR = any(a <= 97.8 and b >= 102.2 for a, b in RANGES)
T0, T1 = out_t(97.8), out_t(102.2)
fc = [f"[0:v]split=2[vm][vb]", f"[vb]trim=start=1.0:duration={T1-T0:.3f},setpts=PTS-STARTPTS+{T0:.3f}/TB,crop=540:720:0:0,scale=1080:1440:flags=lanczos,eq=contrast=1.04:saturation=1.06[broll]",
      f"[vm]crop=540:720:x='{cx}':y=0,scale=1080:1440:flags=lanczos,eq=contrast=1.04:saturation=1.06,"
      f"select='{sel}',setpts=N/FRAME_RATE/TB,pad=1080:1920:0:250:color=0x0D2C5C[v0]",
      f"[1:a]aselect='{sel}',asetpts=N/SR/TB,afade=t=out:st={TOTAL-0.06:.2f}:d=0.06,aformat=channel_layouts=stereo:sample_rates=48000[a0]",
      "[v0][broll]overlay=0:250:enable='between(t,%.3f,%.3f)':eof_action=pass[v0b]" % (T0, T1) if HAS_BR else "[v0]null[v0b]",
      "[v0b][2:v]overlay=0:0[v1]"]
if not HAS_BR: fc[1] = "[vb]nullsink"
last = 'v1'
for j, (a, b, _) in enumerate(cards):
    fc.append(f"[{len(caps2)+3+j}:v]setpts=PTS-STARTPTS+{a:.3f}/TB[cl{j}]"); fc.append(f"[{last}][cl{j}]overlay=0:250:enable='between(t,{a:.3f},{b:.3f})':eof_action=pass[k{j}]"); last = f'k{j}'
for k, (a, b, _) in enumerate(caps2):
    fc.append(f"[{last}][{k+3}:v]overlay=0:1060:enable='between(t,{a:.3f},{b:.3f})'[c{k}]"); last = f'c{k}'
fc.append(f"[{last}]fps=30,format=yuv420p[vout]")
open(f'{OUT}/fc.txt', 'w').write(';\n'.join(fc))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, '-filter_complex_script', f'{OUT}/fc.txt',
                '-map', '[vout]', '-map', '[a0]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
                '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', f'{OUT}/body.mp4'], check=True)
# end card 3 s with silence
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-t', '3', '-i', f'{OUT}/endcard.png',
                '-f', 'lavfi', '-t', '3', '-i', 'anullsrc=r=48000:cl=stereo',
                '-vf', 'fps=30,format=yuv420p,fade=t=in:st=0:d=0.4', '-c:v', 'libx264', '-crf', '20',
                '-c:a', 'aac', '-b:a', '160k', '-shortest', f'{OUT}/end.mp4'], check=True)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{OUT}/body.mp4', '-i', f'{OUT}/end.mp4', '-filter_complex',
                '[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]', '-map', '[v]', '-map', '[a]',
                '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k',
                '-movflags', '+faststart', f'{OUT}/{NAME}.mp4'], check=True)
print('total body', round(TOTAL, 1), 's; kept intervals', len(keep))
