# Working in bj-content-studio

- This repository is the hand-off desk between Claude and Gemini for the Bones & Joints Clinic Instagram.
- To get images or voiceovers made, add or update `briefs/<week>.json` (format in the docstring of `scripts/generate.py`) and push it to `main`. The push starts the GitHub Action.
- Wait about 2–5 minutes, then `git pull`. The results arrive in `out/<week>/`, and `out/<week>/status.json` shows whether each item worked, with the error text if it failed.
- The Actions API is blocked from Claude's sandbox. Check progress with git pull only.
- To bring a file into Canva, use `upload-asset-from-url` with `https://raw.githubusercontent.com/manojyadavapk/bj-content-studio/main/out/<week>/<file>`.
- Item ids must be unique within a week. Existing files are never remade, so to redo one, change its id.
- Image prompts:
  - Never put text in the image; Canva adds all text.
  - Ask for "one continuous full-bleed scene, no bands, borders or panels". Asking for "empty sky in the top third" produced a visible seam line in the first test. Instead, say "simple uncluttered background at the top".
  - No exercise-position images. Exercise slides use the website illustrations (bonesnjointsclinic.com/img/PT-*.jpg).
  - Use Indian people and settings, warm and natural, in the brand colours: green #62AA94, navy #0D2C5C, mint #E0F1EC.
- Voiceovers:
  - Put ONLY the spoken words in "text". The TTS model reads any instruction aloud, so don't add a "style" line. Choose tone with the voice name instead (e.g. Kore = warm female, Charon/Puck = male).
  - Marathi or English, plain patient language.
  - Never claim to be Dr Yadav's own voice.
- Never commit keys, patient names, photos of patients or any patient data. The repository is public.

## Reference photos and video (added Oct 2026)
- Image jobs can take `"refs": ["inputs/<file>"]`, which sends real photos to Gemini as references. `inputs/dr-front.jpg`, `inputs/dr-three-quarter.jpg` and `inputs/dr-side-profile.jpg` are Dr Yadav's own portraits (the ONLY 3 photos to use). Use them for posters with his likeness, and ask Gemini to keep his face identical.
- Video jobs go in `"videos": [{"id", "prompt", "image": "out/<week>/<img>.png", "aspect": "9:16", "seconds": 8}]` and run on Veo 3.1 Fast. Each 8-second clip costs about $0.80, so keep it to 1–2 clips a week. A start image from the same brief is made first.
- Veo garbles signboard and label text as the camera moves in. Use only the first 3–4 seconds of a push-in, or shots without close-up text.
- Push ONE brief per commit and wait for its results. A second brief pushed while a run is in progress can be skipped; if that happens, touch the brief (add `"run": N`) and push again.
- REAL PATIENT FOOTAGE NEVER GOES IN THIS PUBLIC REPO OR TO GEMINI. Edit clinic videos that show patients locally (ffmpeg in Claude's sandbox), and post them only after Dr Yadav confirms the patients' written consent.
- POSTERS (Dr Yadav, 11 Oct 2026). Earlier attempts were rejected for two reasons: text boxes pasted on a picture looked incoherent, and Gemini-drawn posters CHANGED HIS FACIAL FEATURES. The approved method:
  1. Gemini makes ONLY a people-free, text-free background (e.g. out/W00-bg/diwali_bg_navy.png), with calm space on one side.
  2. Use his REAL photo, never an AI-drawn face. His photo set, exactly 3 photos (all real, white coat over a light-blue shirt):
     - inputs/dr-front.jpg: front, grey background, 900x1350
     - inputs/dr-three-quarter.jpg: three-quarter view, slight smile, blue-green gradient background, 1254x1254
     - inputs/dr-side-profile.jpg: right-facing side profile, grey background, 1024x1536. Good for "looking toward the text" layouts: place him on the LEFT, facing the text on the right.
 Cut out inputs/dr-front.jpg locally with rembg (`pip install "rembg[cpu]"`, model isnet-general-use with alpha matting). birefnet-portrait runs out of memory.
  3. Composite locally with PIL so it looks photographed in the scene. See tools/compose_poster_diwali_example.py:
     - warm colour-match plus left-to-right light falloff on the photo
     - golden rim light and a soft glow behind him
     - the diya/flower row re-layered IN FRONT of his coat, so the photo's bottom crop is hidden
     - the cropped shoulder edge faded out; alpha eroded 1px to remove the grey hair fringe
     - he stays on the right, never overlapping the text column (x < 520)
  4. Typography: Playfair Display (gold gradient) for the greeting, Mukta for Marathi, Poppins for everything else. Glass navy info panel at the bottom with a gold hairline, both phones, website, handle, and the real QR (inputs/qr-card.png) on a white card, labelled exactly "Scan to save contact" (never just "Scan to save").
  5. Proofread, verify the QR decodes, then upload the PNG to Canva and to Drive 05 Ready to post.
  Approved example: out/W00-poster/diwali_final_v2.png (three-quarter photo, 820px tall)
- STATUS / STORY posters (1080x1920, e.g. WhatsApp status): use tools/compose_status.py <bg> <cutout> <out_prefix> <config.json>; tools/status_config_navratri_example.json is the example config. The status app covers the top ~150px (name and progress bar) and the bottom ~150px (Reply bar), so the header starts at y>=180 and all contact info ends above y=1770 (the script asserts this). Approved example: out/W00-navratri/navratri_status_green.png.

## Cartoon character (Dr Yadav, 20 Oct 2026)
- Dr Yadav authorised a CARTOON version of himself for educational videos (Reels/YouTube). It does not replace the poster rule above: realistic posters still use only his real photos.
- Master references, made in ChatGPT and approved by him: `inputs/dr-cartoon-presenter.png` (waist-up, explaining) and `inputs/dr-cartoon-expressions.png` (7 expressions). Pass BOTH as `refs` for every cartoon scene and ask Gemini to keep the face, beard, hair and skin tone identical, in the same clean-outline cel-shaded style.
- Every cartoon video carries an on-screen "AI-generated illustration" mark (NMC guidelines, 6 Oct 2026) and is education only: no offers, no booking calls to action.
