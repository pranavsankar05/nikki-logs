import json
import time

import covers as c

CREDITS_FILE = c.HERE / "covers_credits.json"


def main():
    pool = json.loads(c.POOL_FILE.read_text())
    credits = json.loads(CREDITS_FILE.read_text()) if CREDITS_FILE.exists() else {}
    c.COVERS_DIR.mkdir(parents=True, exist_ok=True)

    for cat, ids in pool.items():
        if cat not in c.CATEGORIES:      # skips the empty maps_plans entry
            continue
        for oid in ids:
            name = f"{cat}-{oid}.webp"
            path = c.COVERS_DIR / name
            if path.exists():            # safe to re-run
                continue
            try:
                obj = c._json(f"{c.API}/objects/{oid}")
                data = c._make_cover(c._get(obj["primaryImage"], timeout=60),
                                     cat == "sculpture")
            except Exception as e:
                print("failed:", name, e)
                continue
            if data is None:
                print("skipped:", name)
                continue
            path.write_bytes(data)
            artist = obj.get("artistDisplayName") or "Unknown artist"
            credits[name] = (f"{obj.get('title', 'Untitled')}, {artist}, "
                             "The Metropolitan Museum of Art, Open Access (CC0)")
            CREDITS_FILE.write_text(json.dumps(credits, indent=1) + "\n")
            print("saved:", name)
            time.sleep(0.5)              # go gently, the Met rate limits


main()