# Working in bj-content-studio

- This repository is the hand-off desk between Claude and Gemini for the Bones & Joints Clinic Instagram.
- To get images or voiceovers made, add or update `briefs/<week>.json` (format in the docstring of `scripts/generate.py`) and push it to `main`. The push starts the GitHub Action.
- Wait about 2–5 minutes, then `git pull`. The results arrive in `out/<week>/`, and `out/<week>/status.json` shows whether each item worked, with the error text if it failed.
- The Actions API is blocked from Claude's sandbox. Check progress with git pull only.
- To bring a file into Canva, use `upload-asset-from-url` with `https://raw.githubusercontent.com/manojyadavapk/bj-content-studio/main/out/<week>/<file>`.
- Item ids must be unique within a week. Existing files are never remade, so to redo one, change its id.
- Image prompts:
  - Never put text in the image; Canva adds all text.
  - No exercise-position images. Exercise slides use the website illustrations (bonesnjointsclinic.com/img/PT-*.jpg).
  - Use Indian people and settings, warm and natural, in the brand colours: green #62AA94, navy #0D2C5C, mint #E0F1EC.
- Voiceovers:
  - Marathi or English, plain patient language.
  - Never claim to be Dr Yadav's own voice.
- Never commit keys, patient names, photos of patients or any patient data. The repository is public.
