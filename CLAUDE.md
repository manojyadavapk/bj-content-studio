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
- Image jobs can take `"refs": ["inputs/<file>"]`, which sends real photos to Gemini as references. `inputs/dr-front.jpg` and `inputs/dr-three-quarter.jpg` are Dr Yadav's own portraits (already public on his website). Use them for posters with his likeness, and ask Gemini to keep his face identical.
- Video jobs go in `"videos": [{"id", "prompt", "image": "out/<week>/<img>.png", "aspect": "9:16", "seconds": 8}]` and run on Veo 3.1 Fast. Each 8-second clip costs about $0.80, so keep it to 1–2 clips a week. A start image from the same brief is made first.
- Veo garbles signboard and label text as the camera moves in. Use only the first 3–4 seconds of a push-in, or shots without close-up text.
- Push ONE brief per commit and wait for its results. A second brief pushed while a run is in progress can be skipped; if that happens, touch the brief (add `"run": N`) and push again.
- REAL PATIENT FOOTAGE NEVER GOES IN THIS PUBLIC REPO OR TO GEMINI. Edit clinic videos that show patients locally (ffmpeg in Claude's sandbox), and post them only after Dr Yadav confirms the patients' written consent.
- POSTERS (Dr Yadav, 11 Oct 2026). Earlier attempts were rejected for two reasons: text boxes pasted on a picture looked incoherent, and Gemini-drawn posters CHANGED HIS FACIAL FEATURES. The approved method:
  1. Gemini makes ONLY a people-free, text-free background (e.g. out/W00-bg/diwali_bg_navy.png), with calm space on one side.
  2. Use his REAL photo, never an AI-drawn face. Cut out inputs/dr-front.jpg locally with rembg (`pip install "rembg[cpu]"`, model isnet-general-use with alpha matting). birefnet-portrait runs out of memory.
  3. Composite locally with PIL so it looks photographed in the scene. See tools/compose_poster_diwali_example.py:
     - warm colour-match plus left-to-right light falloff on the photo
     - golden rim light and a soft glow behind him
     - the diya/flower row re-layered IN FRONT of his coat, so the photo's bottom crop is hidden
     - the cropped shoulder edge faded out; alpha eroded 1px to remove the grey hair fringe
     - he stays on the right, never overlapping the text column (x < 520)
  4. Typography: Playfair Display (gold gradient) for the greeting, Mukta for Marathi, Poppins for everything else. Glass navy info panel at the bottom with a gold hairline, both phones, website, handle, and the real QR (inputs/qr-card.png) on a white card.
  5. Proofread, verify the QR decodes, then upload the PNG to Canva and to Drive 05 Ready to post.
  Approved example: out/W00-poster/diwali_final_real_photo.png
