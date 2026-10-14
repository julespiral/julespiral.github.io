"""Génère les deux rats à l'encre du site (static/img/rat-capuchon.svg et rat-albinos.svg).

Le pelage est fait de centaines de petits traits orientés vers l'arrière, plus denses
dans les zones d'ombre, à la manière d'un dessin à la plume. Relancer après modification :
    python3 scripts/rats.py
"""
import math
import random
from pathlib import Path

INK = "#1A1A1A"
PAPER = "#FAFAF8"
W, H = 170, 76

# Formes du corps, vu de côté, tête à gauche : (cx, cy, rx, ry, rotation en degrés)
BODY = (94, 41, 38, 21, -8)
NECK = (68, 39, 16, 14, 0)
HEAD = (46, 40, 22, 12, 16)
SNOUT = (29, 44, 10, 5.5, 22)
HIP = (114, 46, 20, 17, 0)
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


def stroke(x, y, ang, length, bend):
    ex, ey = x + length * math.cos(ang), y + length * math.sin(ang)
    mx = (x + ex) / 2 - bend * math.sin(ang)
    my = (y + ey) / 2 + bend * math.cos(ang)
    return f"M{x:.1f} {y:.1f}Q{mx:.1f} {my:.1f} {ex:.1f} {ey:.1f}"


def fur_angle(x, y):
    # Le poil part vers l'arrière (droite) et retombe sur les flancs.
    cy = 40
    return math.atan2(0.45 * (y - cy) / 20 + 0.05, 1.0)


def in_hood(x, y):
    # Capuchon : tête, cou, épaules, et une bande sur le dos jusqu'à la queue.
    shoulder = 76 - (y - 20) * 0.35
    if x < shoulder:
        return True
    return y < 30 + (x - 76) * 0.06


def make(kind, seed):
    rnd = random.Random(seed)
    hooded = kind == "capuchon"
    dark, light, outline = [], [], []

    # Pelage intérieur
    for _ in range(12000):
        x, y = rnd.uniform(18, 140), rnd.uniform(18, 64)
        if not inside(x, y, 0.92):
            continue
        shade = max(0.0, (y - 44) / 18)          # ombre sous le ventre
        shade += max(0.0, (x - 118) / 25) * 0.5  # ombre sur la croupe
        ang = fur_angle(x, y) + rnd.gauss(0, 0.18)
        length = rnd.uniform(4, 8)
        bend = rnd.gauss(0, 0.5)
        if hooded and in_hood(x, y):
            if rnd.random() < 0.09:
                light.append(stroke(x, y, ang, length * 0.8, bend))
        elif hooded and in_hood(x - 7, y - 4) and rnd.random() < 0.7:
            dark.append(stroke(x - 6, y, ang, length * 1.1, bend))  # bord du capuchon effiloché
        else:
            p = 0.02 + 0.4 * shade * shade + 0.02 * max(0.0, (30 - y) / 6)
            if rnd.random() < p:
                dark.append(stroke(x, y, ang, length, bend))

    # Contour en poils : petits traits tirés vers l'extérieur et l'arrière
    for s in SHAPES:
        for i in range(260):
            t = 2 * math.pi * i / 260 + rnd.uniform(-0.01, 0.01)
            x, y = on_shape(s, t)
            if inside(x, y, 0.97) and any(o is not s and sum(q * q for q in local(o, x, y)) < 0.97 for o in SHAPES):
                continue
            nx, ny = x - s[0], y - s[1]
            n = math.hypot(nx, ny) or 1
            out = math.atan2(ny / n, nx / n)
            back = fur_angle(x, y)
            ang = math.atan2(math.sin(out) * 0.5 + math.sin(back), math.cos(out) * 0.5 + math.cos(back))
            if x < 30:  # museau : contour net
                if rnd.random() < 0.5:
                    outline.append(stroke(x, y, ang, rnd.uniform(1, 2), 0))
                continue
            if rnd.random() < 0.75:
                outline.append(stroke(x - 1.2 * math.cos(ang), y - 1.2 * math.sin(ang), ang, rnd.uniform(1.8, 4), rnd.gauss(0, 0.5)))

    # Couleurs
    eye = "#C8102E" if not hooded else INK
    pink = "#E3A1A1"
    hood_fill = ""
    if hooded:
        hood_fill = (
            f'<clipPath id="corps"><ellipse cx="{BODY[0]}" cy="{BODY[1]}" rx="{BODY[2]}" ry="{BODY[3]}" transform="rotate({BODY[4]} {BODY[0]} {BODY[1]})"/>'
            f'<ellipse cx="{NECK[0]}" cy="{NECK[1]}" rx="{NECK[2]}" ry="{NECK[3]}"/>'
            f'<ellipse cx="{HEAD[0]}" cy="{HEAD[1]}" rx="{HEAD[2]}" ry="{HEAD[3]}" transform="rotate({HEAD[4]} {HEAD[0]} {HEAD[1]})"/>'
            f'<ellipse cx="{SNOUT[0]}" cy="{SNOUT[1]}" rx="{SNOUT[2]}" ry="{SNOUT[3]}" transform="rotate({SNOUT[4]} {SNOUT[0]} {SNOUT[1]})"/>'
            f'<ellipse cx="{HIP[0]}" cy="{HIP[1]}" rx="{HIP[2]}" ry="{HIP[3]}"/></clipPath>'
            f'<path clip-path="url(#corps)" fill="{INK}" d="M0 0H80C90 31 120 33 170 36V0Z"/>'
            f'<path clip-path="url(#corps)" fill="{INK}" d="M0 0H76C74 30 70 50 66 76H0Z"/>'
        )

    def body_fill():
        return "".join(
            f'<ellipse cx="{s[0]}" cy="{s[1]}" rx="{s[2]}" ry="{s[3]}" transform="rotate({s[4]} {s[0]} {s[1]})"/>'
            for s in SHAPES
        )

    leg = f'fill="none" stroke="{INK}" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"'
    toes = lambda x, y: f"M{x} {y}l-4 0.6M{x} {y}l-3.4 2M{x} {y}l-1.2 2.4"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>
.patte{{transform-box:fill-box;transform-origin:50% 0;animation:pas .3s ease-in-out infinite alternate}}
.patte.b{{animation-direction:alternate-reverse}}
@keyframes pas{{from{{transform:rotate(-22deg)}}to{{transform:rotate(22deg)}}}}
</style>
<path d="M128 50C146 62 160 60 169 44" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>
<path d="M128 50C146 62 160 60 169 44" fill="none" stroke="{pink}" stroke-width="1.6" stroke-linecap="round"/>
<path d="M134 54l1-2M140 57l1-2M146 58l0.6-2M152 57l0.4-2M158 54l0.2-2" stroke="{INK}" stroke-width="0.5"/>
<g class="patte a"><path {leg} d="M52 50L49 65L44 66"/><path {leg} d="{toes(44, 66)}"/></g>
<g class="patte b"><path {leg} d="M60 51L60 65L55 66"/><path {leg} d="{toes(55, 66)}"/></g>
<g class="patte b"><path {leg} d="M110 56L104 66L96 67"/><path {leg} d="{toes(96, 67)}"/></g>
<g class="patte a"><path {leg} d="M120 54L117 66L109 67"/><path {leg} d="{toes(109, 67)}"/></g>
<g fill="{PAPER}">{body_fill()}</g>
{hood_fill}
<path fill="none" stroke="{INK}" stroke-width="0.38" stroke-linecap="round" d="{''.join(dark)}"/>
<path fill="none" stroke="{PAPER}" stroke-width="0.5" stroke-linecap="round" opacity="0.85" d="{''.join(light)}"/>
<path fill="none" stroke="{INK}" stroke-width="0.5" stroke-linecap="round" d="{''.join(outline)}"/>
<ellipse cx="55" cy="26" rx="6.5" ry="8" transform="rotate(-18 55 26)" fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>
<path d="M53 22c2 2 3 6 2 10M57 22c1 3 1 6 0 9" fill="none" stroke="{pink if not hooded else INK}" stroke-width="0.6"/>
<circle cx="35" cy="36" r="2.3" fill="{eye}" stroke="{INK}" stroke-width="0.5"/>
<circle cx="34.3" cy="35.2" r="0.7" fill="{PAPER}"/>
<path d="M22.5 45.5c-1.6 0-2.6-1-2.4-2.2c0.3-1.2 1.6-1.6 2.8-1" fill="{pink}" stroke="{INK}" stroke-width="0.6"/>
<path d="M24 45c-6-4-14-6-22-6M24 45.5c-7-1-14 0-21 2M24.5 46c-6 2-11 5-16 9M25 44.5c-5-5-10-8-16-10" fill="none" stroke="{INK}" stroke-width="0.35"/>
</svg>
'''
    return svg


out = Path(__file__).resolve().parent.parent / "static" / "img"
for kind, seed in [("capuchon", 7), ("albinos", 11)]:
    (out / f"rat-{kind}.svg").write_text(make(kind, seed))
    print(kind, len(make(kind, seed)) // 1024, "Ko")
