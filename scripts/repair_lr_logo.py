from pathlib import Path
from PIL import Image
import numpy as np

source = Path("assets/images/logo-lr-web.png")
destination = Path("assets/images/lr-credit-logo-v2.png")
im = Image.open(source).convert("RGBA")
pixels = np.asarray(im).copy()
opacity = pixels[:, :, 3]
ys, xs = np.where(opacity > 10)
if not len(xs):
    raise SystemExit("The original monogram has no visible pixels")
left, right = int(xs.min()), int(xs.max()) + 1
top, bottom = int(ys.min()), int(ys.max()) + 1
margin_x = max(12, round((right - left) * 0.055))
margin_y = max(8, round((bottom - top) * 0.08))
left = max(0, left - margin_x)
right = min(im.width, right + margin_x)
top = max(0, top - margin_y)
bottom = min(im.height, bottom + margin_y)
cut = pixels[top:bottom, left:right].copy()
a = cut[:, :, 3].astype(np.float32)
cut[:, :, 3] = np.clip((a - 7) * 255 / 240, 0, 255).astype(np.uint8)
cut[cut[:, :, 3] == 0, :3] = 0
out = Image.fromarray(cut, mode="RGBA")
if out.width < 350 or out.height < 200 or not 1.5 < (out.width / out.height) < 2.3:
    raise SystemExit(f"Unexpected logo proportions {out.size}")
if not np.any(cut[:, :, 3] > 220):
    raise SystemExit("Logo alpha reconstruction failed")
out.save(destination, optimize=True)
print(f"Original {im.size}, visible bbox {(left, top, right, bottom)}, repaired {out.size}; saved {destination}")
