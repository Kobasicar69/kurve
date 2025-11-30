# generate_manifest.py
# Usage: python generate_manifest.py
# Optional env var INLINE=1 or --inline to produce index_inlined.html

import os
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MEDIA_DIR = ROOT / "media"
OUT_FILE = MEDIA_DIR / "manifest.json"
INLINE_OUT = ROOT / "index_inlined.html"

IMAGE_EXTS = {'.jpg','.jpeg','.png','.gif','.webp','.bmp','.heic'}
VIDEO_EXTS = {'.mp4','.webm','.ogg','.mov'}

if not MEDIA_DIR.exists():
    print("media/ directory not found. Create a folder named 'media' and put your files there.")
    sys.exit(1)

files = [f for f in sorted(MEDIA_DIR.iterdir(), key=lambda p: p.name.lower()) if not f.name.startswith('.')]

entries = []
for f in files:
    ext = f.suffix.lower()
    if ext in IMAGE_EXTS:
        t = 'image'
    elif ext in VIDEO_EXTS:
        t = 'video'
    else:
        continue
    entries.append({
        "type": t,
        "filename": f.name,
        "path": f"media/{f.name}"
    })

OUT_FILE.write_text(json.dumps(entries, indent=2), encoding='utf-8')
print(f"Wrote {len(entries)} entries to {OUT_FILE}")

if (os.getenv('INLINE') == '1') or ('--inline' in sys.argv):
    template = (ROOT / 'index.template.html').read_text(encoding='utf-8')
    out = template.replace('<!-- MANIFEST_JSON -->', json.dumps(entries, indent=2))
    INLINE_OUT.write_text(out, encoding='utf-8')
    print(f"Wrote inlined HTML to {INLINE_OUT}")
