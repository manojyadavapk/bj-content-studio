# B&J Content Studio

The workshop for the Bones & Joints Clinic Instagram (@bonesnjointsclinic).

1. **Claude writes the brief.** A file in `briefs/` lists the images and voiceovers needed for the week.
2. **Gemini makes them.** GitHub runs `scripts/generate.py` as soon as a brief arrives. The images and audio land in `out/<week>/`, and `status.json` records whether each item worked.
3. **Claude builds the posts in Canva.** It pulls in these files plus the clinic logo, QR code and website illustrations.
4. **Dr Yadav schedules them** in Meta Business Suite on Sunday.

Nothing private goes here: no patient data, and no keys. The Gemini key lives only in the repository's Actions secret `GEMINI_API_KEY`.
