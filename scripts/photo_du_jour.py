"""Va chercher l'image du jour et l'écrit dans data/photo.json (lue par partials/photo.html).

Le thème alterne d'un jour à l'autre :
    0. photo de l'espace (photothèque images.nasa.gov)
    1. art, sans nus : deux fois sur trois une peinture de l'Art Institute of Chicago, sinon de l'art abstrait
       (motifs géométriques de l'Art Institute, ou Wikimedia Commons : Kandinsky, Mondrian, Klee, Hilma af Klint, Malevitch…)
Si une source échoue, on prend l'autre. Le choix dépend seulement de la date.
Lancé chaque matin par .github/workflows/photo-du-jour.yml ; à la main :
    python3 scripts/photo_du_jour.py [AAAA-MM-JJ] [nasa|art]
"""
import datetime
import hashlib
import io
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


NASA_SUJETS = ["Hubble galaxy", "Hubble nebula", "Carina Nebula", "Orion Nebula", "Andromeda galaxy", "Blue Marble",
               "aurora space station", "Saturn Cassini", "Jupiter Juno", "Mars Perseverance panorama",
               "solar dynamics observatory", "comet", "star cluster", "supernova remnant", "Earth at night"]
# Photos d'événements, de réunions ou de matériel, qu'on ne veut pas en image du jour
NASA_EXCLUS = re.compile(r"town hall|panel|meeting|press|briefing|conference|ceremony|award|interview|"
                         r"workshop|team|install|cleanroom|mirror|test|visit|chart|graph|diagram|plot|"
                         r"president|keynote|address|patch|history|administrator|portrait|logo|poster|previews|"
                         r"Q and A|indicator|first images of|hangout", re.I)


def lisible(url):
    """Vrai si le carré recadré au centre n'est ni presque noir, ni délavé, ni uniforme."""
    try:
        from PIL import Image, ImageStat
    except ImportError:  # sans Pillow, on ne vérifie pas
        return True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://julespiral.com/"})
        with urllib.request.urlopen(req, timeout=60) as r:
            im = Image.open(io.BytesIO(r.read())).convert("L")
    except Exception:  # image introuvable ou format illisible : on passe à la suivante
        return False
    c = min(im.size)
    g, h = (im.width - c) // 2, (im.height - c) // 2
    st = ImageStat.Stat(im.crop((g, h, g + c, h + c)).resize((200, 200)))
    return 18 < st.mean[0] < 215 and st.stddev[0] > 20


def evenement(d):
    """Photo prise par un photographe sur Terre (conférence, visite, lancement) plutôt qu'une image de l'espace.
    Les images des télescopes et des sondes n'ont pas de photographe ; celles des astronautes ont une cote « iss »."""
    if d.get("center") == "HQ" or d["nasa_id"].startswith("NHQ"):
        return True
    return bool(d.get("photographer")) and not d["nasa_id"].lower().startswith("iss")


def nasa(jour):
    # L'API de l'image astronomique du jour (APOD) ne renvoie plus que le logo de la NASA depuis
    # son déménagement sur science.nasa.gov : on pioche dans la photothèque images.nasa.gov.
    base = nombre(jour, "sujet", len(NASA_SUJETS))
    for i in range(len(NASA_SUJETS)):  # sujet sans image lisible : on essaie le suivant
        sujet = NASA_SUJETS[(base + i) % len(NASA_SUJETS)]
        q = urllib.parse.urlencode({"q": sujet, "media_type": "image", "page_size": 100})
        items = [o for o in lire(f"https://images-api.nasa.gov/search?{q}")["collection"]["items"]
                 if " " in o["data"][0]["title"] and not NASA_EXCLUS.search(o["data"][0]["title"])
                 and not evenement(o["data"][0])]
        depart = nombre(jour, "nasa", len(items)) if items else 0
        for k in range(min(25, len(items))):  # fiche sans JPEG ou image illisible une fois recadrée : on passe à la suivante
            o = items[(depart + k) % len(items)]
            d = o["data"][0]
            image = next((f for taille in ("~medium.jpg", "~large.jpg", "~orig.jpg")
                          for f in lire(o["href"]) if f.endswith(taille)), None)
            if image and lisible(image.replace("http://", "https://")):
                break
        else:
            continue
        break
    else:
        raise ValueError("pas d'image lisible")
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


# Grands noms de l'abstraction, morts avant 1960 : leurs œuvres sont dans le domaine public
ABSTRAIT = ["Abstract paintings by Wassily Kandinsky", "Abstract paintings by Piet Mondrian", "Abstract paintings by Paul Klee",
            "Paintings by Hilma af Klint", "Suprematist paintings by Kazimir Malevich", "Suprematist paintings by Lyubov Popova",
            "Paintings by Robert Delaunay", "Abstract paintings by Theo van Doesburg",
            "Paintings by Arthur G. Dove", "AIC", "AIC"]  # AIC : motifs géométriques de l'Art Institute (deux parts)
NU = re.compile(r"nude|naked|nudity|bather|baigneu|akt\b|\bnu\b|\bnus\b|erotic", re.I)
# Photos de salles d'exposition ou de ventes plutôt que de l'œuvre elle-même
SALLE = re.compile(r"exhibition|ausstellung|exposition|auction|museum|musée|museo|galerie|gallery|installation|vitrine|"
                   r"by shakko|\(GRM\)|visitors|hall\b|room\b", re.I)
# Hilma af Klint a aussi peint des portraits et des paysages : on ne garde que ses séries abstraites
KLINT = re.compile(r"seri|group|untitled|sans titre|altar|ten largest|tio största|swan|svan|dove|duvan|tree of knowledge|"
                   r"evolution|primordial|urkaos|wu\b|rose|standpoint|parsifal|atom|buddha|temple|nr|no\.", re.I)
# Œuvres figuratives des mêmes peintres (af Klint et Delaunay ont aussi peint des fermes et des portraits)
FIGURATIF = re.compile(r"portrait of|portrait de|farm|landscape|paysage|still life|nature morte|flower|fleur|"
                       r"woman|femme|girl|man with|homme|portrait|\bp \d+|page|book|livre", re.I)


def champ(h):
    """Nettoie un champ de Commons : retire les blocs Wikidata cachés et garde la version anglaise s'il y en a une."""
    h = re.sub(r'<div style="display: ?none;?">.*?</div>', "", h or "", flags=re.S)
    h = re.sub(r'<span class="language[^"]*"[^>]*>.*?</span>', "", h, flags=re.S)
    en = re.search(r'lang="en"[^>]*>(.*?)</div>', h, flags=re.S)
    if en:
        return texte(en.group(1))
    autre = re.search(r'lang="[a-z-]+"[^>]*>(.*?)</div>', h, flags=re.S)
    t = texte(autre.group(1) if autre else h)
    double = re.fullmatch(r"(.+?)\s*\1", t)  # « Unknown authorUnknown author »
    return double.group(1) if double else t


def fichiers(categorie):
    api = "https://commons.wikimedia.org/w/api.php?"
    p = {"action": "query", "list": "categorymembers", "cmtitle": f"Category:{categorie}", "cmtype": "file",
         "cmlimit": 500, "format": "json"}
    noms = []
    while True:
        j = lire(api + urllib.parse.urlencode(p))
        noms += [m["title"] for m in j["query"]["categorymembers"]]
        if "continue" not in j:
            return sorted(n for n in noms if re.search(r"\.(jpe?g|png|tiff?)$", n, re.I) and not NU.search(n) and not SALLE.search(n)
                          and not FIGURATIF.search(n))
        p["cmcontinue"] = j["continue"]["cmcontinue"]


def geometrique(jour):
    """Motifs géométriques du domaine public de l'Art Institute of Chicago : peintures et textiles, sans figures humaines."""
    requete = {
        "query": {"bool": {
            "must": [{"term": {"is_public_domain": True}}, {"exists": {"field": "image_id"}},
                     {"terms": {"subject_titles.keyword": ["geometric", "geometric motif", "lines", "diamond shapes"]}},
                     # seulement des peintures et des textiles (pas de gravures, de vases ni d'objets)
                     {"terms": {"classification_titles.keyword": ["painting", "oil on canvas", "textile", "weaving",
                                                                  "weaving - coverlet", "coverlet", "quilt", "tunic",
                                                                  "tapestry", "rug", "carpet", "blanket"]}}],
            "must_not": [{"terms": {"subject_titles.keyword": ["portraits", "women", "men", "figures", "children",
                                                                "religion", "saints"] + SUJETS_NUS}},
                         ]}},
        "fields": ["id", "title", "artist_title", "date_display", "image_id", "thumbnail"],
        "limit": 100,
    }
    j = lire("https://api.artic.edu/api/v1/artworks/search", json.dumps(requete).encode())
    oeuvres = sorted(j["data"], key=lambda o: o["id"])
    depart = nombre(jour, "aic", len(oeuvres))
    for k in range(min(25, len(oeuvres))):
        o = oeuvres[(depart + k) % len(oeuvres)]
        image = f"{j['config']['iiif_url']}/{o['image_id']}/full/843,/0/default.jpg"
        if lisible(image):
            break
    else:
        raise ValueError("pas d'œuvre lisible")
    t = o.get("thumbnail") or {}
    return {
        "theme": "art",
        "titre": o["title"],
        "auteur": o.get("artist_title") or "",
        "date": o.get("date_display") or "",
        "licence": "CC0",
        "image": image,
        "lien": f"https://www.artic.edu/artworks/{o['id']}",
        "source": "Art Institute of Chicago",
        "largeur": t.get("width", 0),
        "hauteur": t.get("height", 0),
    }


# Nus : sujets étiquetés par l'Art Institute, et titres des thèmes classiques qui en montrent souvent
SUJETS_NUS = ["nudes", "nudity", "bathers", "bathing", "bath", "Venus"]
TITRES_NUS = re.compile(r"nude|naked|bather|baign|bath|venus|vénus|nymph|eve\b|adam|leda|danae|danaë|susanna|suzanne|"
                        r"odalis|toilet|psyche|andromeda|diana|bacchan|satyr|graces|sebastian|judith|lucretia|cleopatra|"
                        r"sleeping|dormeuse|amor|cupid|venere|galatea|europa|\bjob\b|jerome|jérôme|penitent|pénitent|magdalen|"
                        r"madeleine|flagellation|bathsheba|samson|hercules|prometheus|mars and", re.I)


def peinture(jour):
    """Peinture du domaine public de l'Art Institute of Chicago, de toutes les époques, sans nus."""
    requete = {
        "query": {"bool": {
            "must": [{"term": {"is_public_domain": True}}, {"exists": {"field": "image_id"}},
                     {"term": {"artwork_type_title.keyword": "Painting"}}],
            "must_not": [{"terms": {"subject_titles.keyword": SUJETS_NUS}}]}},
        "fields": ["id", "title", "artist_title", "date_display", "image_id", "thumbnail"],
        "limit": 100,
        "page": 1 + nombre(jour, "page", 10),  # l'API refuse au-delà des 1000 premiers résultats
    }
    j = lire("https://api.artic.edu/api/v1/artworks/search", json.dumps(requete).encode())
    oeuvres = sorted((o for o in j["data"] if not TITRES_NUS.search(o["title"])), key=lambda o: o["id"])
    depart = nombre(jour, "peinture", len(oeuvres))
    for k in range(min(25, len(oeuvres))):
        o = oeuvres[(depart + k) % len(oeuvres)]
        image = f"{j['config']['iiif_url']}/{o['image_id']}/full/843,/0/default.jpg"
        if lisible(image):
            break
    else:
        raise ValueError("pas de peinture lisible")
    t = o.get("thumbnail") or {}
    return {
        "theme": "art",
        "titre": o["title"],
        "auteur": o.get("artist_title") or "",
        "date": o.get("date_display") or "",
        "licence": "CC0",
        "image": image,
        "lien": f"https://www.artic.edu/artworks/{o['id']}",
        "source": "Art Institute of Chicago",
        "largeur": t.get("width", 0),
        "hauteur": t.get("height", 0),
    }


def art(jour):
    """Deux jours sur trois une peinture de l'Art Institute, un jour sur trois une œuvre abstraite."""
    if nombre(jour, "melange", 3):
        try:
            return peinture(jour)
        except Exception:
            pass
    return abstrait(jour)


def abstrait(jour):
    """Art abstrait du domaine public ou sous licence libre (Wikimedia Commons), sans nus."""
    api = "https://commons.wikimedia.org/w/api.php?"
    base = nombre(jour, "categorie", len(ABSTRAIT))
    if ABSTRAIT[base] == "AIC":
        try:
            return geometrique(jour)
        except Exception:
            pass
    for i in range(len(ABSTRAIT)):
        if ABSTRAIT[(base + i) % len(ABSTRAIT)] == "AIC":
            continue
        categorie = ABSTRAIT[(base + i) % len(ABSTRAIT)]
        noms = fichiers(categorie)
        if "Hilma" in categorie:
            noms = [n for n in noms if KLINT.search(n)]
        depart = nombre(jour, "art", len(noms)) if noms else 0
        for k in range(min(25, len(noms))):
            nom = noms[(depart + k) % len(noms)]
            p = {"action": "query", "titles": nom, "prop": "imageinfo|categories", "iiprop": "url|size|extmetadata",
                 "iiurlwidth": LARGEUR, "cllimit": 500, "format": "json"}
            page = next(iter(lire(api + urllib.parse.urlencode(p))["query"]["pages"].values()))
            if any(NU.search(c["title"]) or FIGURATIF.search(c["title"]) for c in page.get("categories", [])):
                continue
            info = page["imageinfo"][0]
            if lisible(info["thumburl"]):
                break
        else:
            continue
        break
    else:
        raise ValueError("pas d'œuvre lisible")
    m = info["extmetadata"]
    return {
        "theme": "art",
        "titre": champ(m.get("ObjectName", {}).get("value")) or re.sub(r"\.\w+$", "", nom.removeprefix("File:")),
        "auteur": champ(m.get("Artist", {}).get("value")),
        "date": champ(m.get("DateTimeOriginal", {}).get("value"))[:30],
        "licence": texte(m.get("LicenseShortName", {}).get("value")),
        "image": info["thumburl"].split("?")[0],
        "lien": info["descriptionurl"],
        "source": "Wikimedia Commons",
        "largeur": info["width"],
        "hauteur": info["height"],
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
