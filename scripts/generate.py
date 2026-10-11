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
                  if "generateContent" in m.get("supportedGenerationMethods", [])]
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


def make_image(model, item, path):
    body = {"contents": [{"parts": [{"text": item["prompt"]}]}],
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
    text = (item.get("style", "Say warmly and clearly, like a caring doctor talking to a patient:")
            + " " + item["text"])
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
    for brief_path in sorted(glob.glob("briefs/*.json")):
        brief = json.load(open(brief_path, encoding="utf-8"))
        week = brief["week"]
        out = f"out/{week}"
        os.makedirs(out, exist_ok=True)
        status_path = f"{out}/status.json"
        status = json.load(open(status_path)) if os.path.exists(status_path) else {}
        status["models"] = {"image": image_model, "tts": tts_model}
        jobs = [("image", i, f"{out}/{i['id']}.png") for i in brief.get("images", [])] + \
               [("voice", v, f"{out}/{v['id']}.wav") for v in brief.get("voice", [])]
        for kind, item, path in jobs:
            if os.path.exists(path):
                continue
            try:
                if kind == "image":
                    if not image_model:
                        raise RuntimeError("no image model available on this key")
                    make_image(image_model, item, path)
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
