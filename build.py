"""LAYLA IG grid 2: nové posty z layla-cennik/social (ig/, organic_posts/, edu_a2/, carousel v2) → export/, thumbs/, data.js, thumbs-data.js, proposal.js
Návrh poradia = „Výber s fotkami zo štúdia“ (v každom riadku jedna reálna fotka) + obálky carouselov; ostatné posty sú v odložených."""
import json, base64, io, pathlib
import numpy as np
from PIL import Image, ImageFilter
ROOT = pathlib.Path(__file__).parent
S = pathlib.Path(r"C:\Users\samue\layla-cennik\social")

# id: (súbor, kind, cat, grp, head, q, title)   kind: T typografia, F fotka, O detail, V fotka + text
T = {}
def add(i, f, kind, cat, grp, head, q, title): T[i] = (f, kind, cat, grp, head, q, title)
P = "ig/LAYLA_post_%s_1080x1350.png"
add("d01", P % "01_studio", "V", "priestor", "studio", None, 2, "Pokojné štúdio v Piešťanoch")
add("d02", P % "02_citat", "V", "citat", "dotyk", "dotyk", 3, "Dotyk, ktorý uvoľní telo aj myseľ")
add("d03", P % "03_maderoterapia", "V", "madero", "madero", None, 3, "Maderoterapia – oblúk a cena")
add("d04", P % "04_bankovanie", "V", "masaz", "banky", None, 2, "Bankovanie")
add("d05", P % "05_poukaz", "V", "poukaz", "poukaz", None, 2, "Darujte chvíľu pokoja")
add("d06", P % "06_sluzby", "V", "sluzby", "sluzby", None, 3, "Naše služby – štyri oblúky")
add("d07", P % "07_prva_navsteva", "V", "rezervacia", "prva", None, 3, "Prvá návšteva – ako to prebieha")
add("d08", P % "08_nohy", "V", "masaz", "nohy", None, 2, "Ľahší krok – masáž nôh")
add("d09", P % "09_rezervacia", "V", "rezervacia", "rezerv", None, 3, "Rezervujte si svoj čas")
add("d10", P % "10_chrbat", "V", "masaz", "chrbat", None, 2, "Masáž chrbta, šije a ramien")
add("d11", P % "11_mozaika", "V", "priestor", "studio", None, 2, "Miesto, kde spomalíte – mozaika")
add("d12", P % "12_kruh", "V", "citat", "telomysel", "telo", 2, "Telo v pohode – kruh")
add("d13", P % "13_otvorene", "V", "rezervacia", "hodiny", None, 2, "Otvorené každý deň 8 – 20")
add("d14", P % "14_magazin", "V", "masaz", None, None, 2, "Magazín – Chvíľa pre seba")
add("d15", P % "15_polaroid", "V", "rezervacia", None, None, 1, "Polaroid – prvá masáž")
add("d16", P % "16_cas", "V", "sluzby", "dlzka", None, 3, "Koľko času máte?")
add("d17", P % "17_diagonala", "V", "madero", "madero", None, 2, "Drevo, teplo a pokoj")
add("d18", P % "18_nadych", "T", "citat", "dych", None, 2, "Nádych. Výdych.")
add("d19", P % "19_preco", "V", "sluzby", "preco", None, 3, "Prečo práve my?")
add("d20", P % "20_ram", "V", "masaz", "uvolnenie", None, 2, "Uvoľnenie od hlavy po päty – rám")
add("d21", P % "21_rovnovaha", "T", "citat", "dotyk", "dotyk", 3, "Dotyk, ktorý navracia rovnováhu")
add("d22", P % "22_hero", "V", "znacka", "telo", "telo", 3, "Telo v pohode – hero")
add("d23", P % "23_logo", "T", "znacka", "logo", None, 3, "Logo LAYLA")
add("d24", P % "24_zlava", "V", "rezervacia", "zlava", None, 2, "−10 % na prvú masáž")
add("d25", P % "25_spomalte", "V", "citat", "spomal", None, 3, "Spomaľte.")
add("d26", P % "26_stacit_prist", "T", "citat", None, None, 3, "Nemusíte nič robiť. Stačí prísť.")
add("d27", P % "27_ponuka", "T", "sluzby", "sluzby", None, 3, "Ponuka veľkými")
add("d28", P % "28_od_hlavy", "V", "masaz", "uvolnenie", None, 3, "Od hlavy po päty")
add("d29", P % "29_poukaz", "V", "poukaz", "poukaz", None, 3, "Darujte pokoj")
add("d30", P % "30_kde", "V", "rezervacia", "kde", None, 2, "Kde nás nájdete")
add("d31", P % "31_pokoj", "V", "citat", None, None, 3, "pokoj. – foto v písme")
add("d32", P % "32_ticho", "V", "citat", None, None, 3, "ticho.")
add("d33", P % "33_okna", "V", "priestor", "studio", None, 3, "Päť okien – štúdio")
add("d34", P % "34_obeh", "V", "citat", "spomal", None, 3, "Večer len pre vás")
add("d35", P % "35_pasy", "V", "sluzby", "sluzby", None, 3, "Vyberte si svoj rytmus")
add("d36", P % "36_stuha", "V", "sluzby", None, None, 2, "Telo si pamätá – stuha")
add("d37", P % "37_vstupenka", "V", "poukaz", "poukaz", None, 3, "Poukaz ako vstupenka")
add("d38", P % "38_kolaz", "V", "priestor", "studio", None, 3, "Priestor, ktorý dýcha")
add("d39", P % "39_tyzden", "V", "rezervacia", "hodiny", None, 3, "Každý deň 8 – 20")
add("d40", P % "40_dychajte", "V", "citat", "dych", None, 3, "Dýchajte.")
add("d41", P % "41_pre_dvoch", "V", "pary", "pary", None, 3, "Pre dvoch")
add("d42", P % "42_rande", "V", "pary", "pary", None, 2, "Rande inak")
add("d43", P % "43_ty_a_ja", "V", "pary", "pary", None, 2, "Ty a ja")
add("d44", P % "44_2x60", "V", "pary", "pary", None, 2, "2 × 60 minút")
add("d45", P % "45_darcek_dvoch", "V", "poukaz", "poukaz", None, 2, "Darujte čas pre dvoch")
add("d46", P % "46_bez_telefonu", "T", "pary", "pary", None, 2, "Bez telefónu")
ORG = [("o073", "priestor", "Štúdio"), ("o010", "priestor", "Uteráky a sviečky"), ("o148", "masaz", "Masáž hlavy"), ("o057", "priestor", "Svetlo, ktoré upokojí"),
       ("o094", "madero", "Nástroje na maderoterapiu"), ("o131", "masaz", "Masáž chrbta"), ("o047", "priestor", "Monstera a sviečky"), ("o103", "masaz", "Banky"),
       ("o163", "masaz", "Masáž nôh"), ("o003", "priestor", "Oddychový kútik"), ("o157", "masaz", "Masáž chrbta – štyri ruky"), ("o170", "priestor", "Hodžova 4304/20")]
for k, (o, cat, title) in enumerate(ORG, 1):
    add(f"r{k:02d}", f"organic_posts/LAYLA_org_{k:02d}_{o}.png", "F", cat, None, None, 3, "Fotka zo štúdia – " + title)
EDU = [("1_bankovanie", "Carousel: Prečo po bankovaní ostanú kruhy?"), ("2_maderoterapia", "Carousel: Maderoterapia – čo robia valčeky?"),
       ("3_prva_masaz", "Carousel: Idete na prvú masáž?"), ("4_30_60_90", "Carousel: 30, 60 alebo 90 minút?"), ("5_scratching", "Carousel: Scratching therapy")]
for k, (e, title) in enumerate(EDU, 1):
    add(f"e{k}", f"edu_a2/LAYLA_edu_{e}_1.png", "V", "edukacia", "edu", None, 3, title)
add("c1", "LAYLA_carousel_1_v2_1080x1350.png", "V", "cennik", "cennik", None, 3, "Carousel: Cenník masáží")

# posty z tej istej fotky nesmú byť blízko seba → spoločný „head“ (rytmus ho drží od seba)
SAME = {"f_banky": ["e1", "r08", "d04", "d35", "d06"], "f_madero": ["e2", "r05", "d06", "d11"], "f_hlava": ["e3", "r03", "d10", "d16", "d35", "d41"],
        "f_chrbat": ["e4", "r06", "d14", "d38"], "f_studio": ["r01", "d01", "d38", "d13"], "f_ruky": ["e5", "r11", "d20"], "f_lounge": ["r10", "d07", "d12"]}
HEAD = {}
for h, ids in SAME.items():
    for i in ids: HEAD.setdefault(i, h)
# návrh: výber (24 navrhnutých) + v každom riadku jedna reálna fotka po uhlopriečke, medzi to obálky carouselov
VYBER = ["d22", "d23", "d25", "d26", "d32", "d21", "d33", "d27", "d02", "d34", "d40", "d29", "d28", "d39", "d36", "d37", "d31", "d09", "d38", "d16", "d03", "d06", "d07", "d35"]
grid, d = [], 0
for r in range(12):
    for c in range(3):
        if c == r % 3: grid.append(f"r{r + 1:02d}")
        else: grid.append(VYBER[d]); d += 1
for k, cid in zip([4, 13, 22, 31, 40, 49], ["c1", "e1", "e2", "e3", "e4", "e5"]):
    grid.insert(k, cid)
PARKED = [i for i in T if i not in grid]

posts, thumbs = [], {}
for pid, (f, kind, cat, grp, head, q, title) in T.items():
    im = Image.open(S / f).convert("RGB")
    full = im.resize((1080, 1350), Image.LANCZOS); full.save(ROOT / "export" / f"{pid}.jpg", quality=90)
    th = im.resize((540, 675), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=0.8, percent=60, threshold=2))
    th.save(ROOT / "thumbs" / f"{pid}.webp", quality=88)
    b = io.BytesIO(); th.save(b, "WEBP", quality=78); thumbs[pid] = "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()
    a = np.asarray(im.convert("L").resize((200, 250))).astype(float)
    L = a.mean(); dark = (a < 80).mean()
    e = np.concatenate([a[:8].ravel(), a[-8:].ravel(), a[:, :8].ravel(), a[:, -8:].ravel()]).mean()
    posts.append(dict(id=pid, cat=cat, kind=kind, grp=grp, title=title, tone="dark" if L < 125 else "light",
                      L=round(L), red=0, head=HEAD.get(pid, head), q=q, edge=round(e), darkShare=round(dark, 2)))
(ROOT / "data.js").write_text("window.POSTS=" + json.dumps(posts, ensure_ascii=False) + ";\n", encoding="utf-8")
(ROOT / "thumbs-data.js").write_text("window.THUMBS=" + json.dumps(thumbs) + ";\n", encoding="utf-8")
(ROOT / "posts.json").write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
(ROOT / "proposal.js").write_text(f"window.PROPOSAL={json.dumps(grid)};\nwindow.PROPOSAL_PARKED={json.dumps(PARKED)};\n", encoding="utf-8")
print("posts", len(posts), "grid", len(grid), "parked", len(PARKED))
