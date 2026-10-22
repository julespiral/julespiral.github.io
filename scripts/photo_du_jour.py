"""Va chercher l'image du jour et l'écrit dans data/photo.json (lue par partials/photo.html).

Le thème alterne d'un jour à l'autre :
    0. photo de l'espace (photothèque images.nasa.gov)
    1. peinture du domaine public de l'Art Institute of Chicago
Si une source échoue, on prend l'autre. Le choix dépend seulement de la date.
Lancé chaque matin par .github/workflows/photo-du-jour.yml ; à la main :
    python3 scripts/photo_du_jour.py [AAAA-MM-JJ] [nasa|art]
"""
import datetime
import hashlib
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

UA = "julespiral.com photo du jour (https://julespiral.com; jules.piral.1@ulaval.ca)"
SORTIE = Path(__file__).resolve().parent.parent / "data" / "photo.json"
LARGEUR = 800


def lire(url, donnees=None):
    req = urllib.request.Request(url, data=donnees, headers={"User-Agent": UA, "AIC-User-Agent": UA, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def texte(h):
    """Retire les balises HTML d'un champ de métadonnées."""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h or ""))).strip()


def nombre(jour, sel, n):
    """Nombre entre 0 et n-1 tiré de la date, stable d'une exécution à l'autre."""
    return int(hashlib.sha256(f"{jour}{sel}".encode()).hexdigest(), 16) % n


NASA_SUJETS = ["Hubble galaxy", "Hubble nebula", "Webb telescope image", "Blue Marble", "aurora space station",
               "Saturn Cassini", "Jupiter Juno", "Mars Perseverance panorama", "Apollo Earthrise", "solar dynamics observatory",
               "comet", "Pillars of Creation", "star cluster", "supernova remnant", "Earth at night"]
# Photos d'événements, de réunions ou de matériel, qu'on ne veut pas en image du jour
NASA_EXCLUS = re.compile(r"town hall|panel|meeting|press|briefing|conference|ceremony|award|interview|"
                         r"workshop|team|install|cleanroom|mirror|test|visit|chart|graph|diagram|plot|"
                         r"president|keynote|address|patch|history|administrator|portrait|logo|poster|previews", re.I)


def nasa(jour):
    # L'API de l'image astronomique du jour (APOD) ne renvoie plus que le logo de la NASA depuis
    # son déménagement sur science.nasa.gov : on pioche dans la photothèque images.nasa.gov.
    sujet = NASA_SUJETS[nombre(jour, "sujet", len(NASA_SUJETS))]
    q = urllib.parse.urlencode({"q": sujet, "media_type": "image", "page_size": 100})
    items = [o for o in lire(f"https://images-api.nasa.gov/search?{q}")["collection"]["items"]
             if " " in o["data"][0]["title"] and not NASA_EXCLUS.search(o["data"][0]["title"])
             and not o["data"][0]["nasa_id"].startswith("NHQ")]  # NHQ : photos d'événements au siège de la NASA
    o = items[nombre(jour, "nasa", len(items))]
    d = o["data"][0]
    fichiers = lire(o["href"])
    image = next((f for taille in ("~medium.jpg", "~large.jpg", "~orig.jpg") for f in fichiers if f.endswith(taille)), None)
    if not image:
        raise ValueError("pas d'image utilisable")
    return {
        "theme": "nasa",
        "titre": d["title"],
        "auteur": texte(d.get("photographer") or d.get("secondary_creator")) or f"NASA ({d.get('center', '')})".replace(" ()", ""),
        "date": d.get("date_created", "")[:10],
        "licence": "Domaine public",
        "image": image.replace("http://", "https://"),
        "lien": f"https://images.nasa.gov/details/{d['nasa_id']}",
        "source": "NASA Image and Video Library",
        "largeur": 0,
        "hauteur": 0,
    }


def art(jour):
    requete = {
        "query": {"bool": {"must": [
            {"term": {"is_public_domain": True}},
            {"term": {"artwork_type_title.keyword": "Painting"}},
            {"exists": {"field": "image_id"}},
        ]}},
        "fields": ["id", "title", "artist_title", "date_display", "image_id", "thumbnail"],
        "limit": 1,
        "page": 1 + nombre(jour, "art", 1000),  # l'API refuse au-delà des 1000 premiers résultats
    }
    j = lire("https://api.artic.edu/api/v1/artworks/search", json.dumps(requete).encode())
    o = j["data"][0]
    t = o.get("thumbnail") or {}
    return {
        "theme": "art",
        "titre": o["title"],
        "auteur": o.get("artist_title") or "",
        "date": o.get("date_display") or "",
        "licence": "CC0",
        "image": f"{j['config']['iiif_url']}/{o['image_id']}/full/843,/0/default.jpg",
        "lien": f"https://www.artic.edu/artworks/{o['id']}",
        "source": "Art Institute of Chicago",
        "largeur": t.get("width", 0),
        "hauteur": t.get("height", 0),
    }


THEMES = [nasa, art]


def main():
    jour = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.date.today()
    choix = THEMES[jour.toordinal() % len(THEMES)]
    if len(sys.argv) > 2:
        choix = next(f for f in THEMES if f.__name__ == sys.argv[2])
    try:
        photo = choix(jour)
    except Exception as e:  # source en panne : on prend l'autre thème
        autre = THEMES[1 - THEMES.index(choix)]
        print(f"{choix.__name__} a échoué ({e}), repli sur {autre.__name__}", file=sys.stderr)
        photo = autre(jour)
    photo["jour"] = jour.isoformat()
    SORTIE.parent.mkdir(exist_ok=True)
    SORTIE.write_text(json.dumps(photo, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(photo, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
