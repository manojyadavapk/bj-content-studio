"""Bones & Joints Clinic content studio — Gemini worker.

Reads every briefs/*.json, makes any image or voiceover that does not exist yet
in out/<week>/, and writes out/<week>/status.json. Runs inside GitHub Actions
with the GEMINI_API_KEY secret. Standard library only.

Brief format (written by Claude):
{
  "week": "W02",
  "images": [{"id": "cover", "prompt": "...", "aspect": "4:5"}],
  "voice":  [{"id": "walking_mr", "text": "...", "voice": "Kore",
              "style": "Say warmly, like a caring doctor:"}]
}
"""
import base64, glob, json, os, subprocess, sys, time, urllib.request, urllib.error, wave

API = "https://generativelanguage.googleapis.com/v1beta"
KEY = os.environ.get("GEMINI_API_KEY", "")


def call(path, body=None, method="POST"):
    url = f"{API}/{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json",
                                          "x-goog-api-key": KEY})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:600]}")


def list_models():
    names, token = [], ""
    while True:
        r = call(f"models?pageSize=200{'&pageToken=' + token if token else ''}", method="GET")
        names += [m["name"].split("/", 1)[1] for m in r.get("models", [])
                  if {"generateContent", "predictLongRunning"} & set(m.get("supportedGenerationMethods", []))]
        token = r.get("nextPageToken", "")
        if not token:
            return names


def pick(models, want, prefer):
    """Pick a model whose name contains `want`, favouring names containing `prefer` words."""
    cands = [m for m in models if want in m]
    for p in prefer:
        hit = [m for m in cands if p in m]
        if hit:
            return sorted(hit)[-1]
    return sorted(cands)[-1] if cands else None


def inline_parts(resp):
    for c in resp.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            if "inlineData" in p:
                yield p["inlineData"]


def inline_file(path):
    mime = "image/png" if path.lower().endswith(".png") else "image/jpeg"
    return {"inlineData": {"mimeType": mime, "data": base64.b64encode(open(path, "rb").read()).decode()}}


def make_video(model, item, path):
    inst = {"prompt": item["prompt"]}
    if item.get("image"):
        d = inline_file(item["image"])["inlineData"]
        inst["image"] = {"bytesBase64Encoded": d["data"], "mimeType": d["mimeType"]}
    params = {"aspectRatio": item.get("aspect", "9:16"), "durationSeconds": int(item.get("seconds", 8))}
    if item.get("resolution"):
        params["resolution"] = item["resolution"]
    try:
        op = call(f"models/{model}:predictLongRunning", {"instances": [inst], "parameters": params})
    except RuntimeError as e:
        if "durationSeconds" in str(e) or "resolution" in str(e):
            op = call(f"models/{model}:predictLongRunning",
                      {"instances": [inst], "parameters": {"aspectRatio": params["aspectRatio"]}})
        else:
            raise
    for _ in range(90):  # up to ~15 min
        if op.get("done"):
            break
        time.sleep(10)
        op = call(op["name"], method="GET")
    if "error" in op:
        raise RuntimeError("video error: " + json.dumps(op["error"])[:600])
    resp = op.get("response", {})
    samples = resp.get("generateVideoResponse", {}).get("generatedSamples") or resp.get("generatedVideos") or []
    if not samples:
        raise RuntimeError("no video returned: " + json.dumps(op)[:600])
    uri = samples[0].get("video", {}).get("uri")
    req = urllib.request.Request(uri, headers={"x-goog-api-key": KEY})
    with urllib.request.urlopen(req, timeout=300) as r:
        open(path, "wb").write(r.read())


def make_image(model, item, path):
    parts = [inline_file(r) for r in item.get("refs", [])] + [{"text": item["prompt"]}]
    body = {"contents": [{"parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"],
                                 "imageConfig": {"aspectRatio": item.get("aspect", "4:5")}}}
    try:
        resp = call(f"models/{model}:generateContent", body)
    except RuntimeError as e:
        if "imageConfig" in str(e) or "aspect" in str(e).lower():
            body["generationConfig"].pop("imageConfig")
            resp = call(f"models/{model}:generateContent", body)
        else:
            raise
    for d in inline_parts(resp):
        if d.get("mimeType", "").startswith("image/"):
            open(path, "wb").write(base64.b64decode(d["data"]))
            return
    raise RuntimeError("no image returned: " + json.dumps(resp)[:400])


def make_voice(model, item, path_wav):
    # Send ONLY the words to be spoken. Style instructions get read aloud by the TTS model
    # (found Oct 2026), so "style" is ignored unless "style_prefix": true is set explicitly.
    text = item["text"]
    if item.get("style_prefix") and item.get("style"):
        text = item["style"] + " " + text
    body = {"contents": [{"parts": [{"text": text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig":
                                                  {"voiceName": item.get("voice", "Kore")}}}}}
    resp = call(f"models/{model}:generateContent", body)
    for d in inline_parts(resp):
        if d.get("mimeType", "").startswith("audio/"):
            pcm = base64.b64decode(d["data"])
            with wave.open(path_wav, "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
                w.writeframes(pcm)
            mp3 = path_wav[:-4] + ".mp3"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path_wav,
                            "-b:a", "128k", mp3], check=False)
            return
    raise RuntimeError("no audio returned: " + json.dumps(resp)[:400])


def main():
    if not KEY:
        sys.exit("GEMINI_API_KEY secret is missing")
    models = list_models()
    image_model = os.environ.get("IMAGE_MODEL") or pick(models, "image", ["flash-image", "flash"])
    tts_model = os.environ.get("TTS_MODEL") or pick(models, "tts", ["flash", "pro"])
    video_model = os.environ.get("VIDEO_MODEL") or pick(models, "veo", ["fast", "lite"])
    for brief_path in sorted(glob.glob("briefs/*.json")):
        brief = json.load(open(brief_path, encoding="utf-8"))
        week = brief["week"]
        out = f"out/{week}"
        os.makedirs(out, exist_ok=True)
        status_path = f"{out}/status.json"
        status = json.load(open(status_path)) if os.path.exists(status_path) else {}
        status["models"] = {"image": image_model, "tts": tts_model, "video": video_model}
        jobs = [("image", i, f"{out}/{i['id']}.png") for i in brief.get("images", [])] + \
               [("voice", v, f"{out}/{v['id']}.wav") for v in brief.get("voice", [])] + \
               [("video", v, f"{out}/{v['id']}.mp4") for v in brief.get("videos", [])]
        for kind, item, path in jobs:
            if os.path.exists(path):
                continue
            try:
                if kind == "image":
                    if not image_model:
                        raise RuntimeError("no image model available on this key")
                    make_image(item.get("model") or image_model, item, path)
                elif kind == "video":
                    if not video_model:
                        raise RuntimeError("no Veo model available on this key")
                    if item.get("image") and not os.path.exists(item["image"]):
                        raise RuntimeError("start image missing: " + item["image"])
                    make_video(item.get("model") or video_model, item, path)
                else:
                    if not tts_model:
                        raise RuntimeError("no TTS model available on this key")
                    make_voice(tts_model, item, path)
                status[item["id"]] = {"ok": True, "file": path,
                                      "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}
            except Exception as e:
                status[item["id"]] = {"ok": False, "error": str(e)[:800]}
            print(item["id"], status[item["id"]])
        json.dump(status, open(status_path, "w"), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
