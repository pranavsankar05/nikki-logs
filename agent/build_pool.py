import io
import json
import random
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from PIL import Image

import covers as c

ROUNDS = 5  # batches of 200 per category per run
REQUIRE = {}  # the colour check already filters dull art


def _good(oid, cat):
    obj = c._check(oid, c.CATEGORIES[cat], cat == "sculpture")
    if obj == "FAILED":
        return None, "request failed"
    if not obj:
        return None, "wrong type or filtered"
    need = REQUIRE.get(cat)
    if need and not any(w in obj.get("medium", "").lower() for w in need):
        return None, "no colour in medium"
    small = obj.get("primaryImageSmall")
    if cat != "sculpture" and small:
        try:
            img = Image.open(io.BytesIO(c._get(small, timeout=20, retries=1))).convert("RGB")
            if c._too_dull(img, quiet=True):
                return None, "too dull"
        except Exception:
            return None, "image failed"
    return oid, "ok"


def main():
    pool = json.loads(c.POOL_FILE.read_text()) if c.POOL_FILE.exists() else {}
    only = sys.argv[1:]  # optional: python build_pool.py sculpture paintings
    cats = [x for x in c.CATEGORIES
            if c.WEIGHTS.get(x, 1) > 0 and (not only or x in only)]

    state = {}
    for cat in cats:
        have = set(pool.get(cat, []))
        ids = c._object_ids(c.CATEGORY_DEPTS[cat])
        random.shuffle(ids)
        state[cat] = (have, [i for i in ids if i not in have])

    for r in range(ROUNDS):
        for cat in cats:  # one batch per category, then the next category
            have, ids = state[cat]
            batch = [ids.pop() for _ in range(min(c.BATCH, len(ids)))]
            if not batch:
                continue
            with ThreadPoolExecutor(c.WORKERS) as ex:
                results = list(ex.map(lambda o: _good(o, cat), batch))
            have.update(o for o, _ in results if o)
            pool[cat] = sorted(have)
            c.POOL_FILE.write_text(json.dumps(pool))
            why = dict(Counter(reason for _, reason in results))
            print(f"{cat}: round {r + 1}/{ROUNDS}, pool has {len(have)} | {why}")


main()