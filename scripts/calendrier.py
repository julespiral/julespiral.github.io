"""Choisit d'avance les images du jour (deux ans par défaut) et les écrit dans scripts/calendrier.json.

Le site lit ensuite l'image du jour dans ce calendrier (scripts/photo_du_jour.py). Le choisir d'avance permet de
regarder chaque œuvre avant sa mise en ligne : les fiches de l'Art Institute ne signalent presque jamais les nus.
    python3 scripts/calendrier.py [AAAA-MM-JJ] [jours]       # calcule le calendrier
    python3 scripts/calendrier.py --planches DOSSIER          # planches contact des œuvres d'art, à vérifier
Une œuvre refusée à la vérification va dans EXCLUES (photo_du_jour.py) ; relancer ensuite le calcul : seuls les jours
touchés changent. Demande Pillow (pip install pillow).
"""
import datetime
import io
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import photo_du_jour as pdj

pdj.REFUS_ACCEPTE = False  # ici, une image refusée est vraiment réservée : on l'écarte


# Images de l'Art Institute réservées (le serveur les refuse même aux visiteurs), repérées à la vérification
REFUSEES = {80551, 46088, 159685, 109277, 57468, 99427, 139798, 99521, 105187, 112323, 241202, 93951, 43081, 179229,
            109457, 8284, 74555, 145542, 136991, 151598}


def calculer(debut, jours):
    dates = [debut + datetime.timedelta(i) for i in range(jours)]
    ancien = json.loads(pdj.CALENDRIER.read_text()) if pdj.CALENDRIER.exists() else {}

    def un(jour):
        # On garde le choix déjà fait s'il est toujours valable (œuvre pas exclue entre-temps)
        # Une œuvre exclue est remplacée par un nouveau tirage ailleurs dans la collection (essai suivant), pas par
        # sa voisine, qui appartient souvent à la même série
        p = ancien.get(jour.isoformat())
        if p and not (p["theme"] == "art" and int(p["lien"].rsplit("/", 1)[1]) in pdj.EXCLUES | REFUSEES):
            return jour, p
        essai = p.get("essai", 0) + 1 if p else 0
        p = pdj.choisir(jour, essai=essai)
        p["essai"] = essai
        return jour, p

    with ThreadPoolExecutor(6) as ex:
        choix = dict(ex.map(un, dates))
    # Pas deux fois la même image : un doublon est remplacé par la suivante
    vues, calendrier = set(), {}
    for jour in dates:
        p = choix[jour]
        if p["lien"] in vues:
            p = pdj.choisir(jour, deja=vues)
        vues.add(p["lien"])
        p["jour"] = jour.isoformat()
        calendrier[jour.isoformat()] = p
    pdj.CALENDRIER.write_text(json.dumps(calendrier, ensure_ascii=False, indent=1) + "\n")
    print(len(calendrier), "jours, du", dates[0], "au", dates[-1])


def planches(dossier, par_planche=48):
    from PIL import Image, ImageDraw
    cal = json.loads(pdj.CALENDRIER.read_text())
    oeuvres = [p for p in cal.values() if p["theme"] == "art"]

    def vignette(p):
        req = urllib.request.Request(p["image"], headers={"User-Agent": pdj.UA, "Referer": "https://julespiral.com/"})
        try:
            im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read())).convert("RGB")
        except Exception:
            im = Image.new("RGB", (200, 200), "white")
        im.thumbnail((230, 230))
        return p, im

    with ThreadPoolExecutor(6) as ex:
        vignettes = list(ex.map(vignette, oeuvres))
    for n in range(0, len(vignettes), par_planche):
        lot = vignettes[n:n + par_planche]
        planche = Image.new("RGB", (8 * 240, ((len(lot) + 7) // 8) * 260), "white")
        dessin = ImageDraw.Draw(planche)
        for k, (p, im) in enumerate(lot):
            x, y = (k % 8) * 240, (k // 8) * 260
            planche.paste(im, (x + 5, y + 5))
            dessin.text((x + 5, y + 240), f"{p['jour']} #{p['lien'].rsplit('/', 1)[1]}", fill="black")
        planche.save(f"{dossier}/planche-{n // par_planche + 1:02d}.jpg", quality=85)
    print(len(vignettes), "œuvres sur", (len(vignettes) + par_planche - 1) // par_planche, "planches")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--planches"]:
        planches(sys.argv[2])
    else:
        debut = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.date.today()
        calculer(debut, int(sys.argv[2]) if len(sys.argv) > 2 else 730)
