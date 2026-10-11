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
  - Marathi or English, plain patient language.
  - Never claim to be Dr Yadav's own voice.
- Never commit keys, patient names, photos of patients or any patient data. The repository is public.

## Reference photos and video (added Oct 2026)
- Image jobs can take `"refs": ["inputs/<file>"]`, which sends real photos to Gemini as references. `inputs/dr-front.jpg` and `inputs/dr-three-quarter.jpg` are Dr Yadav's own portraits (already public on his website). Use them for posters with his likeness, and ask Gemini to keep his face identical.
- Video jobs go in `"videos": [{"id", "prompt", "image": "out/<week>/<img>.png", "aspect": "9:16", "seconds": 8}]` and run on Veo 3.1 Fast. Each 8-second clip costs about $0.80, so keep it to 1–2 clips a week. A start image from the same brief is made first.
- Veo garbles signboard and label text as the camera moves in. Use only the first 3–4 seconds of a push-in, or shots without close-up text.
- Push ONE brief per commit and wait for its results. A second brief pushed while a run is in progress can be skipped; if that happens, touch the brief (add `"run": N`) and push again.
- REAL PATIENT FOOTAGE NEVER GOES IN THIS PUBLIC REPO OR TO GEMINI. Edit clinic videos that show patients locally (ffmpeg in Claude's sandbox), and post them only after Dr Yadav confirms the patients' written consent.
- Posters: let Gemini make the art with no text, then add all text, logo (MAHXq0wgMyM), QR (MAHXrkbIq0I), phones and addresses in Canva, so every detail is exact. Example: Canva design DAHXr6uyJiI (Diwali 2026).
