"""Génère les deux rats à l'encre du site (static/img/rat-capuchon.svg et rat-albinos.svg).

Le pelage est fait de centaines de petits traits orientés vers l'arrière, plus denses
dans les zones d'ombre, à la manière d'un dessin à la plume. Les SVG sont insérés tels
quels dans la page (partial rat.html) : les pattes (.patte) et le museau (.museau) sont
animés par la feuille de style du site. Relancer après modification :
    python3 scripts/rats.py
"""
import math
import random
from pathlib import Path

INK = "#1A1A1A"
PAPER = "#FAFAF8"
PINK = "#E3A1A1"
W, H = 160, 72

# Formes du corps, vu de côté, tête à gauche : (cx, cy, rx, ry, rotation en degrés)
BODY = (90, 41, 34, 20, -8)
NECK = (64, 38, 14, 13, 0)
HEAD = (46, 38, 17, 10, -4)
SNOUT = (30, 43, 11, 4.4, -14)
HIP = (108, 45, 19, 17, 0)
SHAPES = [BODY, NECK, HEAD, SNOUT, HIP]


def local(shape, x, y):
    cx, cy, rx, ry, rot = shape
    a = math.radians(-rot)
    dx, dy = x - cx, y - cy
    u = dx * math.cos(a) - dy * math.sin(a)
    v = dx * math.sin(a) + dy * math.cos(a)
    return u / rx, v / ry


def inside(x, y, margin=1.0):
    return any(sum(t * t for t in local(s, x, y)) <= margin for s in SHAPES)


def on_shape(shape, t):
    cx, cy, rx, ry, rot = shape
    a = math.radians(rot)
    u, v = rx * math.cos(t), ry * math.sin(t)
    return cx + u * math.cos(a) - v * math.sin(a), cy + u * math.sin(a) + v * math.cos(a)


def ellipse(s, **attrs):
    extra = "".join(f' {k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<ellipse cx="{s[0]}" cy="{s[1]}" rx="{s[2]}" ry="{s[3]}" transform="rotate({s[4]} {s[0]} {s[1]})"{extra}/>'


def stroke(x, y, ang, length, bend):
    ex, ey = x + length * math.cos(ang), y + length * math.sin(ang)
    mx = (x + ex) / 2 - bend * math.sin(ang)
    my = (y + ey) / 2 + bend * math.cos(ang)
    return f"M{x:.1f} {y:.1f}Q{mx:.1f} {my:.1f} {ex:.1f} {ey:.1f}"


def fur_angle(x, y):
    # Le poil part vers l'arrière (droite) et retombe sur les flancs.
    if x < 40:  # sur le museau, le poil suit la pente du nez
        return math.radians(-20)
    return math.atan2(0.45 * (y - 40) / 20 + 0.05, 1.0)


def in_hood(x, y):
    # Capuchon : tête, cou, épaules, et une bande sur le dos jusqu'à la queue.
    if x < 72 - (y - 20) * 0.35:
        return True
    return y < 30 + (x - 72) * 0.06


def make(kind, seed):
    rnd = random.Random(seed)
    hooded = kind == "capuchon"
    dark, light, outline = [], [], []

    # Pelage intérieur ; les poils sont plus courts sur la tête
    for _ in range(12000):
        x, y = rnd.uniform(16, 130), rnd.uniform(18, 64)
        if not inside(x, y, 0.92):
            continue
        shade = max(0.0, (y - 44) / 18) + max(0.0, (x - 112) / 25) * 0.5
        ang = fur_angle(x, y) + rnd.gauss(0, 0.18)
        length = rnd.uniform(4, 8) * (0.45 if x < 58 else 1)
        bend = rnd.gauss(0, 0.5)
        if hooded and in_hood(x, y):
            if rnd.random() < 0.09:
                light.append(stroke(x, y, ang, length * 0.8, bend))
        elif hooded and in_hood(x - 7, y - 4) and rnd.random() < 0.7:
            dark.append(stroke(x - 6, y, ang, length * 1.1, bend))  # bord du capuchon effiloché
        else:
            p = 0.02 + 0.4 * shade * shade + 0.02 * max(0.0, (30 - y) / 6)
            if x < 58:
                p *= 0.5  # visage plus doux
            if rnd.random() < p:
                dark.append(stroke(x, y, ang, length, bend))

    # Contour en poils : petits traits tirés vers l'extérieur et l'arrière ; net sur la tête
    for s in SHAPES:
        for i in range(260):
            t = 2 * math.pi * i / 260 + rnd.uniform(-0.01, 0.01)
            x, y = on_shape(s, t)
            if any(o is not s and sum(q * q for q in local(o, x, y)) < 0.97 for o in SHAPES):
                continue
            nx, ny = x - s[0], y - s[1]
            n = math.hypot(nx, ny) or 1
            out = math.atan2(ny / n, nx / n)
            back = fur_angle(x, y)
            ang = math.atan2(math.sin(out) * 0.5 + math.sin(back), math.cos(out) * 0.5 + math.cos(back))
            if x < 56:
                if rnd.random() < 0.6:
                    outline.append(stroke(x, y, back, rnd.uniform(1, 2.2), 0))
                continue
            if rnd.random() < 0.75:
                outline.append(stroke(x - 1.2 * math.cos(ang), y - 1.2 * math.sin(ang), ang, rnd.uniform(1.8, 4), rnd.gauss(0, 0.5)))

    eye = "#C8102E" if not hooded else INK
    clip = f"corps-{kind}"
    hood = ""
    if hooded:
        hood = (
            f'<clipPath id="{clip}">{"".join(ellipse(s) for s in SHAPES)}</clipPath>'
            f'<path clip-path="url(#{clip})" fill="{INK}" d="M0 0H160V36C116 33 86 31 60 30Z"/>'
            f'<path clip-path="url(#{clip})" fill="{INK}" d="M0 0H72C70 30 66 50 62 72H0Z"/>'
        )

    leg = f'fill="none" stroke="{INK}" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"'

    def toes(x, y):
        return f"M{x} {y}l-3.6 0.5M{x} {y}l-3 1.8M{x} {y}l-1 2.2"

    # Pattes : la diagonale avant-gauche / arrière-droite bouge ensemble (classe a), l'autre en opposition (classe b).
    # Les pattes du côté caché sont plus pâles.
    legs = f'''<g class="patte b loin"><path {leg} d="M58 47L58 64L54 65"/><path {leg} d="{toes(54, 65)}"/></g>
<g class="patte a loin"><path {leg} d="M114 52L110 63L102 65"/><path {leg} d="{toes(102, 65)}"/></g>
<g class="patte a"><path {leg} d="M50 47L48 64L43 65"/><path {leg} d="{toes(43, 65)}"/></g>
<g class="patte b"><path {leg} d="M104 54L98 64L90 66"/><path {leg} d="{toes(90, 66)}"/></g>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<g class="queue">
<path d="M122 49C140 61 152 58 159 43" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>
<path d="M122 49C140 61 152 58 159 43" fill="none" stroke="{PINK}" stroke-width="1.6" stroke-linecap="round"/>
<path d="M128 53l1-2M134 56l1-2M140 57l0.6-2M146 56l0.4-2M152 53l0.2-2" stroke="{INK}" stroke-width="0.5"/>
</g>
{legs}
<g fill="{PAPER}">{"".join(ellipse(s) for s in SHAPES)}</g>
{hood}
<path fill="none" stroke="{INK}" stroke-width="0.38" stroke-linecap="round" d="{"".join(dark)}"/>
<path fill="none" stroke="{PAPER}" stroke-width="0.5" stroke-linecap="round" opacity="0.85" d="{"".join(light)}"/>
<path fill="none" stroke="{INK}" stroke-width="0.5" stroke-linecap="round" d="{"".join(outline)}"/>
<ellipse cx="55" cy="25" rx="7.2" ry="7.8" transform="rotate(-12 55 25)" fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>
<ellipse cx="55.4" cy="25.6" rx="4.6" ry="5.2" transform="rotate(-12 55 25)" fill="{PINK}" opacity="0.75"/>
<ellipse cx="30" cy="45.5" rx="3.2" ry="1.9" fill="{PINK}" opacity="{0.5 if not hooded else 0.35}"/>
<circle cx="38" cy="36" r="3.4" fill="{PAPER}" opacity="{0.9 if hooded else 0}"/>
<circle cx="38" cy="36" r="3" fill="{eye}"/>
<circle cx="37" cy="34.9" r="1.1" fill="{PAPER}"/>
<circle cx="39" cy="37.2" r="0.45" fill="{PAPER}"/>
<g class="museau">
<circle cx="19.8" cy="45.8" r="1.6" fill="{PINK}" stroke="{INK}" stroke-width="0.5"/>
<path d="M23 45.5c-6-4-13-6-21-6M23 46c-7-1-14 0-21 2M23.5 46.5c-6 2-11 5-16 9M24 45c-5-5-10-8-15-10" fill="none" stroke="{INK}" stroke-width="0.35"/>
</g>
</svg>
'''


out = Path(__file__).resolve().parent.parent / "static" / "img"
for kind, seed in [("capuchon", 7), ("albinos", 11)]:
    svg = make(kind, seed)
    (out / f"rat-{kind}.svg").write_text(svg)
    print(kind, len(svg) // 1024, "Ko")
