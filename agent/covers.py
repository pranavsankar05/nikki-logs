import functools
import io
import json
import random
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

API = "https://collectionapi.metmuseum.org/public/collection/v1"
HERE = Path(__file__).resolve().parent
COVERS_DIR = HERE.parent / "public" / "covers"
USED_FILE = HERE / "used_covers.json"
POOL_FILE = HERE / "pool.json"

# ---------------------------------------------------------------- settings
OUT_W, OUT_H = 1200, 1500
BATCH = 200              # artworks checked at once
WORKERS = 2              # parallel requests (8 got rate limited with 403s)
MAX_ROUNDS = 30          # batches tried per category before moving on
MIN_HEIGHT = 900         # skip flat artworks too small to crop cleanly
MAX_BYTES = 250_000      # target size of the saved cover
CENTER_ZOOM = 0.9        # 1.0 = widest center crop; lower zooms in a little
MIN_COLOUR_SHARE = 0.12  # share of non-beige colour needed (higher = stricter)
OBJECT_PAD = 0.12        # breathing room around sculpture crops

Image.MAX_IMAGE_PIXELS = 250_000_000

# ------------------------------------------------------ what to pick from
# Comment a line out to drop that category (also remove it from WEIGHTS below).
CATEGORIES = {
    "prints":       ["woodblock", "lithograph", "aquatint", "color print"],
    "paintings":    ["painting", "oil on canvas", "oil on panel", "oil on wood",
                     "watercolor", "gouache", "acrylic", "tempera"],
    # "ink":          ["ink on", "ink and", "handscroll", "hanging scroll", "album leaf"],
    # "drawings":     ["drawing", "pen and", "charcoal", "pencil", "chalk", "graphite"],
    # "manuscripts":  ["manuscript", "illuminat", "calligraph", "folio"],
    # "maps_plans":   ["map", "plan", "elevation", "architectural"],
    "sculpture":    ["sculpture", "statue", "statuette", "bust", "relief", "carving"],
}

# How likely each category is to be picked. Equal = even mix. 0 = never.
WEIGHTS = {
    "prints": 1,
    "paintings": 1,
    "sculpture": 1,
}

# Which Met departments to search for each category
CATEGORY_DEPTS = {
    "prints":     ["asian art", "drawings and prints"],
    "paintings":  ["european paintings", "american wing", "modern and contemporary",
                   "asian art"],
    "sculpture":  ["european sculpture", "arts of africa", "asian art"],
}

# Always skipped: nudity, photos, violence, religion, vessels, weapons, textiles,
# ancient tools and small objects.
SKIP_WORDS = [
    "nude", "nudes", "naked", "erotic", "nudity", "odalisque", "courtesan", "venus",
    "lingerie", "undress", "bather", "shunga", "pillow book",
    "photograph", "albumen", "gelatin silver", "trade card", "cigarette", "cabinet card",
    "crucifixion", "skull", "weapon", "sword", "mummy", "coffin", "martyr", "last judgment",
    "krishna", "vishnu", "shiva", "ganesha", "buddha", "bodhisattva", "durga", "lakshmi",
    "hanuman", "radha", "deity", "avatar", "mandala", "devi",
    "vase", "jar", "bowl", "cup", "vessel", "jug", "bottle", "teapot", "ewer", "urn",
    "amphora", "flask", "pottery", "platter", "dish", "ceramic", "porcelain", "stoneware",
    "armor", "armour", "helmet", "dagger", "jewelry", "jewellery", "ring", "brooch",
    "costume", "textile", "silk", "woven", "carpet", "rug", "tapestry", "embroider",
    "tile", "furniture", "instrument", "coin", "medal", "mask",
    "lacquer", "enamel",
    "pulidor", "polisher", "burnisher", "tool", "implement", "bead", "amulet", "scarab",
    "pestle", "mortar", "axe", "adze", "celt", "blade",
    "shard", "sherd", "pendant", "button", "spindle", "whorl", "palette",
]

# Skipped for everything EXCEPT sculpture (people in paintings and prints)
HUMAN_WORDS = [
    "portrait", "figure", "bust", "torso", "boy", "girl", "child", "baby",
    "goddess", "god", "angel", "madonna", "saint", "christ", "virgin",
    "warrior", "king", "queen", "mother", "father", "couple", "actress",
    "actor", "dancer", "bijin", "cupid", "putto", "putti", "nymph", "satyr",
]

# Pattern books, design sheets and ornament (dropped)
PATTERN_WORDS = [
    "pattern", "ornament", "design for", "wallpaper", "border", "frieze", "lace",
    "decorative", "arabesque", "grotesque", "model book", "textile design", "motif",
]


def _re(words):
    return re.compile(r"\b(" + "|".join(re.escape(w) for w in words) + r")s?\b")


SKIP_RE = _re(SKIP_WORDS)
HUMAN_RE = _re(HUMAN_WORDS)
PATTERN_RE = _re(PATTERN_WORDS)
# --------------------------------------------------------------- networking
def _get(url, timeout=20, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404 or attempt == retries - 1:
                raise          # missing artwork, or out of retries
            time.sleep(3 * (attempt + 1))
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(2 * (attempt + 1))


def _json(url, timeout=20):
    return json.loads(_get(url, timeout))


def _load_used():
    if USED_FILE.exists():
        return set(json.loads(USED_FILE.read_text()))
    return set()


@functools.lru_cache(maxsize=1)
def _departments():
    return _json(f"{API}/departments")["departments"]


def _object_ids(dept_words):
    wanted = [d["departmentId"] for d in _departments()
              if any(w in d["displayName"].lower() for w in dept_words)]
    q = urllib.parse.urlencode({"departmentIds": "|".join(str(i) for i in wanted)})
    return _json(f"{API}/objects?{q}", timeout=90).get("objectIDs") or []


# ---------------------------------------------------------------- filtering
def _kind(obj):
    return " ".join([obj.get("objectName", ""), obj.get("classification", ""),
                     obj.get("medium", "")]).lower()


def _check(oid, words, sculpture):
    """Fetch one artwork's details. Returns the object if it passes the type filters,
    None if filtered or missing, or the string "FAILED" if the request itself failed."""
    try:
        obj = json.loads(_get(f"{API}/objects/{oid}", timeout=15, retries=2))
    except urllib.error.HTTPError as e:
        return None if e.code == 404 else "FAILED"
    except Exception:
        return "FAILED"
    if not obj.get("isPublicDomain") or not obj.get("primaryImage"):
        return None
    tags = " ".join(t.get("term", "") for t in (obj.get("tags") or []))
    kind = _kind(obj)
    text = " ".join([obj.get("title", ""), kind, tags]).lower()
    if SKIP_RE.search(text) or PATTERN_RE.search(text):
        return None
    if not any(w in kind for w in words):
        return None
    if not sculpture and HUMAN_RE.search(text):
        return None
    return obj


def _candidates(seen, ids, words, sculpture):
    batch = []
    while ids and len(batch) < BATCH:
        oid = ids.pop()
        if oid not in seen:
            seen.add(oid)
            batch.append(oid)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        results = list(pool.map(lambda o: _check(o, words, sculpture), batch))
    found = [o for o in results if isinstance(o, dict)]
    failed = sum(1 for o in results if o == "FAILED")
    print(f"checked {len(batch)} artworks, {len(found)} matched, {failed} requests failed")
    return found


# ------------------------------------------------------------ colour check
def _too_dull(img, quiet=False):
    """True if the picture is mostly beige/brown/grey (no blues, greens, reds, pinks)."""
    small = img.resize((160, 200)).convert("HSV")
    pixels = list(small.getdata())
    colourful = 0
    for h, s, v in pixels:
        if s < 70 or v < 60:
            continue                  # pale, grey or too dark: no colour
        if 6 <= h <= 45 and s < 150:
            continue                  # beige, tan, sepia, brown
        colourful += 1
    share = colourful / len(pixels)
    if not quiet:
        print(f"colour check: {share:.2f} colourful (need {MIN_COLOUR_SHARE})")
    return share < MIN_COLOUR_SHARE
# ---------------------------------------------------------------- cropping
def _trim_margins(img):
    """Cut plain borders (paper margins, mounts) around flat art."""
    bg = Image.new("RGB", img.size, img.getpixel((0, 0)))
    box = ImageChops.difference(img, bg).convert("L").point(
        lambda p: 255 if p > 24 else 0).getbbox()
    if not box:
        return img
    w, h = img.size
    # only trim if it keeps at least 60% of the picture
    if (box[2] - box[0]) < w * 0.6 or (box[3] - box[1]) < h * 0.6:
        return img
    return img.crop(box)


def _flat_cover(img):
    """Flat artwork: trim margins, then a centered 4:5 crop."""
    img = _trim_margins(img)
    w, h = img.size
    if w / h > OUT_W / OUT_H:
        bh, bw = h, h * OUT_W / OUT_H
    else:
        bw, bh = w, w * OUT_H / OUT_W
    cw, ch = int(bw * CENTER_ZOOM), int(bh * CENTER_ZOOM)
    if ch < MIN_HEIGHT:
        print("skipped: too small")
        return None
    x, y = (w - cw) // 2, (h - ch) // 2
    return img.crop((x, y, x + cw, y + ch)).resize((OUT_W, OUT_H), Image.LANCZOS)


def _is_object_photo(img):
    """True if all four edges are plain, i.e. an object on a backdrop."""
    w, h = img.size
    m = max(8, int(min(w, h) * 0.08))
    strips = [img.crop((0, 0, w, m)), img.crop((0, h - m, w, h)),
              img.crop((0, 0, m, h)), img.crop((w - m, 0, w, h))]
    spread = max(ImageStat.Stat(s.convert("L")).stddev[0] for s in strips)
    return spread < 14


def _object_cover(img):
    """Sculpture on a backdrop: crop tight around it, pad with the backdrop colour."""
    w, h = img.size
    m = max(8, int(min(w, h) * 0.05))
    edge = [img.crop((0, 0, w, m)), img.crop((0, h - m, w, h)),
            img.crop((0, 0, m, h)), img.crop((w - m, 0, w, h))]
    bg = tuple(int(sum(ImageStat.Stat(e).median[c] for e in edge) / 4) for c in range(3))
    box = ImageChops.difference(img, Image.new("RGB", img.size, bg)).convert("L").point(
        lambda p: 255 if p > 40 else 0).getbbox()
    if not box:
        return None
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    if bw < w * 0.15 or bh < h * 0.15:
        print("skipped: object too small in photo")
        return None
    bw2, bh2 = bw * (1 + 2 * OBJECT_PAD), bh * (1 + 2 * OBJECT_PAD)
    ratio = OUT_W / OUT_H
    if bw2 / bh2 > ratio:
        bh2 = bw2 / ratio
    else:
        bw2 = bh2 * ratio
    ww, wh = int(bw2), int(bh2)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    # keep the crop window inside the photo, so no fake backdrop edge shows
    left = int(min(max(cx - ww / 2, 0), max(w - ww, 0)))
    top = int(min(max(cy - wh / 2, 0), max(h - wh, 0)))
    canvas = Image.new("RGB", (ww, wh), bg)
    canvas.paste(img.crop((left, top, min(left + ww, w), min(top + wh, h))), (0, 0))
    return canvas.resize((OUT_W, OUT_H), Image.LANCZOS)


def _save(img):
    buf = io.BytesIO()
    for q in (82, 74, 66, 58):
        buf = io.BytesIO()
        img.save(buf, "WEBP", quality=q, method=6)
        if buf.tell() <= MAX_BYTES:
            break
    return buf.getvalue()


def _make_cover(data, is_sculpture):
    img = Image.open(io.BytesIO(data)).convert("RGB")
    if is_sculpture:
        # sculpture: no colour check (stone and bronze are never colourful)
        if _is_object_photo(img):
            out = _object_cover(img)
        else:
            out = _flat_cover(img)
        return _save(out) if out is not None else None
    # flat art: crop first, then check the colour of what will actually show
    out = _flat_cover(img)
    if out is None:
        return None
    if _too_dull(out):
        print("skipped: too dull")
        return None
    return _save(out)
# --------------------------------------------------------------- main entry
def _fallback(slug):
    existing = list(COVERS_DIR.glob("*.webp")) if COVERS_DIR.exists() else []
    if existing:
        return f"/covers/{random.choice(existing).name}", ""
    return f"https://picsum.photos/seed/{slug}/600/750", ""


def _category_order():
    """Weighted random order of categories: first is the pick, the rest are backups."""
    names = [c for c in CATEGORIES if WEIGHTS.get(c, 1) > 0]
    order = []
    while names:
        pick = random.choices(names, weights=[WEIGHTS.get(c, 1) for c in names])[0]
        order.append(pick)
        names.remove(pick)
    return order


def _store(slug, dry, used, obj, data):
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


def _cover_from_pool(slug, dry, used):
    """Fast path: pick from the saved list built by build_pool.py."""
    if not POOL_FILE.exists():
        return None
    pool = json.loads(POOL_FILE.read_text())
    for cat in _category_order():
        ids = [i for i in pool.get(cat, []) if i not in used]
        random.shuffle(ids)
        print(f"pool category: {cat} ({len(ids)} unused)")
        for oid in ids[:15]:
            try:
                obj = _json(f"{API}/objects/{oid}")
                data = _make_cover(_get(obj["primaryImage"], timeout=60),
                                   cat == "sculpture")
            except Exception as e:
                print("pool item failed:", e)
                continue
            if data is not None:
                return _store(slug, dry, used, obj, data)
    return None


def _cover_from_category(slug, dry, used, cat):
    """Slow path: search the Met live for one category."""
    sculpture = cat == "sculpture"
    seen = set(used)
    ids = _object_ids(CATEGORY_DEPTS[cat])
    random.shuffle(ids)
    for _ in range(MAX_ROUNDS):
        found = _candidates(seen, ids, CATEGORIES[cat], sculpture)
        if not found and not ids:
            break              # ran out of artworks
        for obj in found:
            # quick rejection of dull flat art using the small preview image
            small = obj.get("primaryImageSmall")
            if small and not sculpture:
                try:
                    preview = Image.open(io.BytesIO(_get(small))).convert("RGB")
                    if _too_dull(preview):
                        print("skipped: too dull (preview)")
                        continue
                except Exception:
                    pass
            try:
                data = _make_cover(_get(obj["primaryImage"], timeout=60), sculpture)
            except Exception as e:
                print("image failed:", e, obj["primaryImage"])
                continue
            if data is not None:
                return _store(slug, dry, used, obj, data)
    return None


def _get_cover_live(slug, dry=False):
    """Backup: pool or live Met search. Used only if no saved covers exist."""
    used = _load_used()
    result = _cover_from_pool(slug, dry, used)
    if result:
        return result
    for cat in _category_order():
        print(f"trying category: {cat}")
        try:
            result = _cover_from_category(slug, dry, used, cat)
        except Exception as e:
            print("Met cover failed:", e)
            continue
        if result:
            return result
    print("No usable artwork found, using fallback")
    return _fallback(slug)


def get_cover(slug, dry=False):
    """Pick an unused saved cover from public/covers (those listed in covers_credits.json)."""
    credits_file = HERE / "covers_credits.json"
    credits = json.loads(credits_file.read_text()) if credits_file.exists() else {}
    saved = [n for n in credits if (COVERS_DIR / n).exists()]
    if not saved:
        print("no saved covers, searching the Met live")
        return _get_cover_live(slug, dry)

    def oid_of(name):
        return int(name.rsplit("-", 1)[1].split(".")[0])

    used = _load_used()
    fresh = [n for n in saved if oid_of(n) not in used]
    if not fresh:
        print("all saved covers used once, starting over")
        used = set()
        fresh = saved

    by_cat = {}
    for n in fresh:
        by_cat.setdefault(n.rsplit("-", 1)[0], []).append(n)
    cats = list(by_cat)
    cat = random.choices(cats, weights=[max(WEIGHTS.get(x, 1), 0.01) for x in cats])[0]
    name = random.choice(by_cat[cat])
    print(f"cover: {name} ({len(fresh)} unused of {len(saved)})")

    if not dry:
        used.add(oid_of(name))
        USED_FILE.write_text(json.dumps(sorted(used)) + "\n")
    return f"/covers/{name}", credits[name]