# B&J working style: read this before making any post, carousel or Reel

This is the house style for Bones & Joints Clinic social content (Dr Manoj Yadav). The rules in CLAUDE.md (NMC, consent, patient data, voice) still apply on top of it.

## Brand
- Colours: navy #0D2C5C (text and bands), green #62AA94 and mint #E0F1EC (soft fills), gold #E6AD3C (chips, bars and highlights only, never as text on white). The accent word ink on white is deep green #2F7A64, which passes contrast; the secondary text is slate #4A6283.
- Fonts: Mukta for Marathi and Hindi, Poppins for English. Playfair Display only for festival greetings.
- Languages: carousels are Hindi (large) with English (small) below (Dr Yadav, 5 Nov 2026: Marathi speakers understand Hindi too, so Hindi reaches more viewers). YouTube titles are in Hindi. Reuse the knowledge pack's Hindi wherever it exists.
- Never criticise treatments other doctors offer (e.g. keyhole washout, joint injections) (Dr Yadav, 5 Nov 2026). Warnings about quacks, chemists and shop-bought products are fine: say "taken from quacks" (नीम-हकीम / झोलाछाप).
- His photo must look part of the slide, never a pasted rectangle: rembg cut-out, mint circle, soft green glow and shadow, light rim, faded shoulder edge, bottom crop hidden behind the navy band (as in the Navratri post). The script is tools/compose_carousel_photo.py.
- Put the website guide link in the first comment after posting; the last slide says "Link in comments".
- Every piece shows "Dr Manoj Yadav · MS (Ortho)" and "MMC Reg. 2017073017". On a Reel it appears in the first 2 seconds.

## Clinical facts
- Every claim comes from repo manojyadavapk/Aescora-knowledge- (textbook-regional/<region>/<rx>.json and textbooks/data/cond/<rx>.json, including its `website` block). If the repo does not cover a claim, ask the to-knowledge inbox before posting. Dr Yadav checks every line before posting.
- No drug names or doses in posts, no brands, no "best", no guarantees, no booking calls to action, no testimonials.

## Carousel (4:5, 1080x1350, 10 slides) — approved format, Nov 2026
Template: templates/carousel/ (Design-canvas .dc.html files). First one: the knee arthritis carousel (Claude Design canvas "B&J Knee Arthritis Carousel").
1. Cover: a big Hindi title with one accent word, an English subtitle, his REAL photo (inputs/, never AI-made), a row of 5 topic chips, "Swipe", and a navy band with name, MMC and handle.
2. Slides 2-9 are one point each:
   - the "NN — 10" counter top left, and a giant ghost numeral in mint top right
   - the green number, then a 1-2 line Hindi title with one accent word and a small English title
   - 4-5 check rows (Hindi line plus a small English line)
   - a mint "डॉक्टरांचा सल्ला · Doctor's tip" box with a gold tag
   - a bold one-line takeaway at the bottom, plus name and MMC
3. The red-flag slide is navy with gold alert icons. It carries every red flag from the pack, never stricter than the pack states it.
4. Last slide: "मोफत मार्गदर्शक" (free guide), a QR code to the website page (verify it decodes), the URL, "Comment GUIDE" and "Save this" chips, a navy band with both clinic phones, and "केवळ माहितीसाठी · For awareness only. Please consult your doctor."
- Comment-to-DM: reply with the free link only. Never diagnose by DM; the reply is "please visit for examination".

## Reels
- Hook: the first 3 seconds decide reach. Make 2-3 openings (A, B, C) on the same body, upload them as versions in Instagram Edits (Add version), and archive the loser after 24-48 h. Never open on a graphic or bloody frame (the first Walking Again Short got 0 views because of it).
- Caption bar: a navy strip with the key word in gold italic, plus a step tracker ("STEP 2/5") for multi-point Reels. Cut to full-screen X-ray or illustration cards every few seconds. End with "Save करा".
- Talking head, Mode 1: Sync 3 on his stock footage (CLAUDE.md). Mode 2: prompter/ page. He says each line himself on the front camera, and the ElevenLabs Voice Changer turns his voice into the cloned voice (voice 254q2GqljB4tv1hLDQjA) with the same timing. Label "AI-cloned voice" in both modes.
- Animated captions and titles: tools/remotion (Remotion 4, free licence up to 3 employees).

## Where things live
- Laptop folder Downloads\BJ_Video_Editor\{Raw, References, Render, _inbox, _outbox}. The laptop's Claude Code session only downloads (yt-dlp) and moves files; all heavy work (frames, transcription, editing) is done in the cloud chat.
- "Me" stock footage: Downloads\BJ_Me_Footage\Stock_1080 on the laptop, never in this public repo.
- Posted log: Drive "Aescora Sync / Clinical Social Media / B&J Social — Posted Log".
- References are for studying style only; never reuse another creator's footage.

## HOUSE STYLE: carousel (approved by Dr Yadav, 5 Nov 2026)
Approved example: the knee-arthritis carousel (Design canvas "B&J Knee Arthritis Carousel", copy in templates/carousel/). Build every condition carousel this way:
- 4:5 (1080x1350), white slides with a big faint slide number, one navy warning slide, Hindi (large) with English (small) under every line.
- Order: cover (his blended real photo, 5 chips, "Swipe") → who gets it (risk factors only: age, weight, sex) → signs (the history and symptoms) → myths and tests → treatment slides → avoid (quacks and shop products only, never other doctors' treatments) → injections/surgery when → red flags (navy, all of the pack's red flags) → free guide (blended photo, QR to the condition page, "Link in comments", both phones, awareness line).
- Each content slide: green number, a 1-line Hindi title with one accent word, English subtitle, 3-5 check rows, a "डॉक्टर की सलाह · Doctor's tip" box, and a bottom line with name and MMC Reg.
- Facts from the knowledge pack; anything he adds that the pack lacks goes to to-knowledge the same day.
- Post: guide link as the first comment; boost through Meta Ads Manager (Vasai, Virar, Palghar, 25+, no location expansion, awareness only).
