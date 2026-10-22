"""Pro v2 (22. 10. 2026): nové exporty z LAYLA_ig_posty_pro.ai (social/ig_pro) → export-p + thumbs-p, nové služby s01–s05,
uprataný návrh poradia (63 postov, duplicity v odložených). Spúšťať po build.py nie je treba – upravuje len Pro vrstvu a návrh."""
import json, re, io, base64, pathlib, importlib.util, contextlib
import numpy as np
from PIL import Image, ImageFilter
ROOT = pathlib.Path(__file__).parent
SRC = pathlib.Path(r"C:/Users/samue/layla-cennik/social/ig_pro")

def look(im, seed):
    a = np.asarray(im).astype(float) / 255
    a = a + 0.08 * (a - 0.5) * (1 - np.abs(2 * a - 1)); a = 0.008 + 0.992 * a
    a[..., 0] *= 1.025; a[..., 1] *= 1.005; a[..., 2] *= 0.96
    g = a.mean(axis=2, keepdims=True); a = g + (a - g) * 0.95
    rng = np.random.default_rng(seed); a += rng.normal(0, 0.010, a.shape[:2])[..., None]
    return Image.fromarray((a.clip(0, 1) * 255).astype("uint8"))

ids = json.loads((pathlib.Path(r"C:/Users/samue/layla-cennik/social/clean/v2/ids.json")).read_text())
for pid in ids:
    im = look(Image.open(SRC / f"{pid}.png").convert("RGB").resize((1080, 1350), Image.LANCZOS), sum(map(ord, pid)))
    im.save(ROOT / "export-p" / f"{pid}.jpg", quality=90)
    th = im.resize((540, 675), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=0.8, percent=60, threshold=2))
    th.save(ROOT / "thumbs-p" / f"{pid}.webp", quality=88)
    if pid.startswith("s"):   # nové posty nemajú pôvodnú ani čistú verziu → rovnaký obrázok aj tam
        for d, t in (("export", "thumbs"), ("export-c", "thumbs-c")):
            im.save(ROOT / d / f"{pid}.jpg", quality=90); th.save(ROOT / t / f"{pid}.webp", quality=88)

# data.js / posts.json: doplniť s01–s05
posts = json.loads((ROOT / "posts.json").read_text(encoding="utf-8"))
have = {p["id"] for p in posts}
NEW = {"s01": ("masaz", "hlava", "Masáž hlavy a tváre"), "s02": ("masaz", "makke", "Mäkké techniky"), "s03": ("masaz", "komplex", "Komplexná regenerácia"),
       "s04": ("madero", "madtvar", "Maderoterapia tváre"), "s05": ("masaz", "scratch", "Scratching therapy")}
for pid, (cat, grp, title) in NEW.items():
    if pid in have: continue
    a = np.asarray(Image.open(ROOT / "export-p" / f"{pid}.jpg").convert("L").resize((200, 250))).astype(float)
    e = np.concatenate([a[:8].ravel(), a[-8:].ravel(), a[:, :8].ravel(), a[:, -8:].ravel()]).mean()
    posts.append(dict(id=pid, cat=cat, kind="V", grp=grp, title=title, tone="light", L=round(a.mean()), red=0, head="s_" + grp, q=3, edge=round(e), darkShare=round((a < 80).mean(), 2)))
(ROOT / "posts.json").write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
(ROOT / "data.js").write_text("window.POSTS=" + json.dumps(posts, ensure_ascii=False) + ";\n", encoding="utf-8")
# nová fotka zo štúdia r24 (z001 – svetlá na stene)
if "r24" not in {p["id"] for p in posts}:
    from PIL import ImageOps
    src = ImageOps.fit(Image.open(r"C:/Users/samue/layla-cennik/social/foto/z001.jpg").convert("RGB"), (1080, 1350), Image.LANCZOS)
    im = look(src, sum(map(ord, "r24"))); th = im.resize((540, 675), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=0.8, percent=60, threshold=2))
    for d, t in (("export", "thumbs"), ("export-c", "thumbs-c"), ("export-p", "thumbs-p")):
        im.save(ROOT / d / "r24.jpg", quality=90); th.save(ROOT / t / "r24.webp", quality=88)
    a = np.asarray(im.convert("L").resize((200, 250))).astype(float)
    posts.append(dict(id="r24", cat="priestor", kind="F", grp=None, title="Fotka zo štúdia – Svetlá na stene", tone="light", L=round(a.mean()), red=0, head="f_svetla", q=3, edge=round(a.mean()), darkShare=round((a < 80).mean(), 2)))
    (ROOT / "posts.json").write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
    (ROOT / "data.js").write_text("window.POSTS=" + json.dumps(posts, ensure_ascii=False) + ";\n", encoding="utf-8")
NEW["r24"] = None
# THUMBS (náhľad na stiahnutie gridu)
t = (ROOT / "thumbs-data.js").read_text(encoding="utf-8"); TH = json.loads(t[t.index("{"):t.rindex("}") + 1])
for pid in NEW:
    b = io.BytesIO(); Image.open(ROOT / "thumbs-p" / f"{pid}.webp").save(b, "WEBP", quality=78); TH[pid] = "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()
(ROOT / "thumbs-data.js").write_text("window.THUMBS=" + json.dumps(TH) + ";\n", encoding="utf-8")

# návrh poradia v2: v každom riadku aspoň jedna fotka, žiadne duplicitné témy, služby rozptýlené
ROWS = [
    "r01 d22 d23", "d31 d29 r21", "d50 r10 d06", "r09 d32 r04", "e2 d16 r23", "s01 r02 d07", "r20 d10 d21",
    "r12 e1 s02", "d19 r15 d13", "r16 d03 s04", "c1 d26 r03", "d51 r18 e5", "s05 r19 d08", "r22 d42 d44",
    "d45 r07 d24", "d46 r13 s03", "r05 e3 d38", "d33 r17 d28", "r11 e4 d18", "d25 r24 d30", "r14 d02 r06",
]
grid = " ".join(ROWS).split()
assert len(grid) == len(set(grid)), "duplicita v návrhu"
allids = [p["id"] for p in posts]
missing = [g for g in grid if g not in allids]; assert not missing, missing
parked = [i for i in allids if i not in grid]
(ROOT / "proposal.js").write_text(f"window.PROPOSAL={json.dumps(grid)};\nwindow.PROPOSAL_PARKED={json.dumps(parked)};\n", encoding="utf-8")
print("grid", len(grid), "parked", len(parked), parked)
