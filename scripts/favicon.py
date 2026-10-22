"""Compose le favicon à partir des deux rats (static/img/rat-capuchon.svg et rat-albinos.svg) :
le rat à capuchon en haut, l'albinos en dessous, tourné dans l'autre sens. Relancer après scripts/rats.py :
    python3 scripts/favicon.py
Les versions PNG (32, 48, 96, 180, 192, 512 px) et favicon.ico se rendent ensuite à partir de favicon-rats.svg, et
img/favicon.svg en est une copie : Google avait mémorisé ces anciennes adresses, qui montraient un mortier bleu.
"""
import re
from pathlib import Path

IMG = Path(__file__).resolve().parent.parent / "static" / "img"


def interieur(nom):
    svg = (IMG / nom).read_text()
    corps = svg[svg.index(">", svg.index("<svg")) + 1:svg.rindex("</svg>")]
    return re.sub(r'class="[^"]*"', "", corps)  # pas d'animation dans l'icône


# Corps et tête occupent x 10 à 140, y 14 à 68 dans le dessin de 232 × 72 ; la queue est coupée par le cadre
haut = interieur("rat-capuchon.svg")
bas = interieur("rat-albinos.svg")
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 132 132">
<rect width="132" height="132" rx="22" fill="#FAFAF8"/>
<svg x="0" y="4" width="132" height="60" viewBox="10 12 132 60">{haut}</svg>
<g transform="translate(132 0) scale(-1 1)"><svg x="0" y="66" width="132" height="60" viewBox="10 12 132 60">{bas}</svg></g>
</svg>
'''
(IMG / "favicon-rats.svg").write_text(svg)
print(len(svg) // 1024, "Ko")
