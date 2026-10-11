import io
import json
import random
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

API = "https://collectionapi.metmuseum.org/public/collection/v1"
HERE = Path(__file__).resolve().parent
COVERS_DIR = HERE.parent / "public" / "covers"
USED_FILE = HERE / "used_covers.json"

# Only draw from departments likely to hold abstract / decorative work
DEPT_WORDS = ["asian", "islamic", "european paintings", "modern", "africa"]

# The work must match at least one of these (checked against type, medium, classification)
ALLOW_WORDS = ["painting", "oil on canvas", "acrylic", "watercolor", "gouache", "ink",
               "textile", "silk", "woven", "carpet", "tapestry", "embroider",
               "ceramic", "porcelain", "tile", "glass", "lacquer", "enamel",
               "woodblock", "print", "manuscript", "mixed media", "sculpture"]

# Skip anything containing these (people, nudity, photos, violence, sensitive items)
SKIP_WORDS = ["nude", "naked", "erotic", "nudity", "odalisque", "courtesan", "venus",
              "lingerie", "undress", "bather", "portrait", "bust", "statue", "figure",
              "photograph", "albumen", "gelatin silver", "trade card", "cigarette",
              "cabinet card", "actress", "actor", "dancer", "crucifixion", "skull",
              "weapon", "sword", "mummy", "coffin"]

MAX_TRIES = 40        # artworks checked per attempt
MAX_ATTEMPTS = 30     # artworks fully tried before giving up
OUT_W, OUT_H = 1200, 1500
MIN_HEIGHT = 1000     # skip artworks too small to crop cleanly
MAX_BYTES = 250_000   # target size of the saved cover
CENTER_ZOOM = 1.0     # 1.0 = widest center crop; 0.7 = closer on the middle

Image.MAX_IMAGE_PIXELS = 250_000_000

def _get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _json(url, timeout=20):
    return json.loads(_get(url, timeout))


def _load_used():
    if USED_FILE.exists():
        return set(json.loads(USED_FILE.read_text()))
    return set()


def _object_ids():
    deps = _json(f"{API}/departments")["departments"]
    wanted = [d["departmentId"] for d in deps
              if any(w in d["displayName"].lower() for w in DEPT_WORDS)]
    q = urllib.parse.urlencode({"departmentIds": "|".join(str(i) for i in wanted)})
    return _json(f"{API}/objects?{q}", timeout=90).get("objectIDs") or []


def _candidate(seen, ids):
    tries = 0
    while ids and tries < MAX_TRIES:
        oid = ids.pop()
        if oid in seen:
            continue
        seen.add(oid)
        tries += 1
        try:
            obj = _json(f"{API}/objects/{oid}")
        except Exception:
            continue
        if not obj.get("isPublicDomain") or not obj.get("primaryImage"):
            continue
        tags = " ".join(t.get("term", "") for t in (obj.get("tags") or []))
        kind = " ".join([obj.get("objectName", ""), obj.get("classification", ""),
                         obj.get("medium", "")]).lower()
        text = " ".join([obj.get("title", ""), kind, tags]).lower()
        if any(w in text for w in SKIP_WORDS):
            continue
        if not any(w in kind for w in ALLOW_WORDS):
            continue
        return obj
    return None


def _make_cover(data):
    img = Image.open(io.BytesIO(data)).convert("RGB")
    w, h = img.size
    if w / h > OUT_W / OUT_H:
        bh, bw = h, h * OUT_W / OUT_H
    else:
        bw, bh = w, w * OUT_H / OUT_W
    cw, ch = int(bw * CENTER_ZOOM), int(bh * CENTER_ZOOM)
    if ch < MIN_HEIGHT:
        return None
    x = (w - cw) // 2
    y = (h - ch) // 2
    img = img.crop((x, y, x + cw, y + ch)).resize((OUT_W, OUT_H), Image.LANCZOS)
    buf = io.BytesIO()
    for q in (82, 74, 66, 58):
        buf = io.BytesIO()
        img.save(buf, "WEBP", quality=q, method=6)
        if buf.tell() <= MAX_BYTES:
            break
    return buf.getvalue()


def _fallback(slug):
    existing = list(COVERS_DIR.glob("*.webp")) if COVERS_DIR.exists() else []
    if existing:
        return f"/covers/{random.choice(existing).name}", ""
    return f"https://picsum.photos/seed/{slug}/600/750", ""


def get_cover(slug, dry=False):
    used = _load_used()
    seen = set(used)
    try:
        ids = _object_ids()
        random.shuffle(ids)
        for _ in range(MAX_ATTEMPTS):
            obj = _candidate(seen, ids)
            if not obj:
                break
            try:
                data = _make_cover(_get(obj["primaryImage"], timeout=60))
            except Exception as e:
                print("image failed:", e)
                continue
            if data is None:
                print("skipped: image too small")
                continue
            artist = obj.get("artistDisplayName") or "Unknown artist"
            credit = (f"{obj.get('title', 'Untitled')}, {artist}, "
                      "The Metropolitan Museum of Art, Open Access (CC0)")
            path = f"/covers/{slug}.webp"
            if not dry:
                COVERS_DIR.mkdir(parents=True, exist_ok=True)
                (COVERS_DIR / f"{slug}.webp").write_bytes(data)
                used.add(obj["objectID"])
                USED_FILE.write_text(json.dumps(sorted(used)) + "\n")
            return path, credit
        print("No usable artwork found, using fallback")
    except Exception as e:
        print("Met cover failed:", e)
    return _fallback(slug)