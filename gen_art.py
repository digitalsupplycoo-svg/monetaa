#!/usr/bin/env python3
"""Generates all original money-themed SVG artwork for the Moneta site."""
import math, os, random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(OUT, exist_ok=True)
random.seed(2611)

INK = "#0C0C0C"
FONT = "Kanit, 'Segoe UI', system-ui, sans-serif"

CURRENCIES = [
    ("$",  "USD", "#7CE0A6"), ("\u20ac", "EUR", "#E9C25C"), ("\u00a3", "GBP", "#8FD9F0"),
    ("\u00a5", "JPY", "#F0A8B8"), ("\u20b9", "INR", "#F5C77E"), ("\u20a9", "KRW", "#A9E5C8"),
    ("\u20ba", "TRY", "#EFA26A"), ("\u20bd", "RUB", "#9FB4F2"), ("\u20a6", "NGN", "#7CE0A6"),
    ("\u0e3f", "THB", "#E9C25C"), ("\u20bf", "BTC", "#F5A623"), ("R$", "BRL", "#8FD9F0"),
    ("Fr",  "CHF", "#D9E3EA"), ("kr", "SEK", "#A9E5C8"), ("\u20b1", "PHP", "#F0A8B8"),
    ("\u20aa", "ILS", "#9FB4F2"), ("Rp", "IDR", "#EFA26A"), ("\u20ab", "VND", "#7CE0A6"),
    ("zl", "PLN", "#E9C25C"), ("AED", "AED", "#8FD9F0"), ("SAR", "SAR", "#A9E5C8"),
]


def guilloche(cx, cy, rings, r0, dr, color, opacity=0.16, wobble=6, pts=180):
    """Engraved banknote-style concentric rosettes."""
    out = []
    for k in range(rings):
        r = r0 + k * dr
        lobes = 5 + (k % 3)
        d = []
        for i in range(pts + 1):
            a = 2 * math.pi * i / pts
            rr = r + wobble * math.sin(lobes * a + k * 0.7)
            d.append(f"{cx + rr*math.cos(a):.1f},{cy + rr*math.sin(a)*0.92:.1f}")
        out.append(
            f'<polyline points="{" ".join(d)}" fill="none" stroke="{color}" '
            f'stroke-width="0.7" opacity="{opacity:.2f}"/>'
        )
    return "".join(out)


def coin(cx, cy, r, hue, glyph, tilt=0.42, stack=0, gap=0):
    """A tilted coin, optionally with a stack of coins beneath it."""
    s = []
    for i in range(stack, 0, -1):
        oy = cy + i * gap
        s.append(
            f'<ellipse cx="{cx}" cy="{oy}" rx="{r}" ry="{r*tilt}" fill="url(#edge{hue[1:]})"/>'
        )
    s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r*tilt}" fill="url(#face{hue[1:]})"/>')
    s.append(
        f'<ellipse cx="{cx}" cy="{cy}" rx="{r*0.82}" ry="{r*tilt*0.82}" fill="none" '
        f'stroke="{INK}" stroke-opacity="0.35" stroke-width="1.5"/>'
    )
    s.append(
        f'<text x="{cx}" y="{cy + r*tilt*0.34}" text-anchor="middle" font-family="{FONT}" '
        f'font-weight="900" font-size="{r*0.82:.0f}" fill="{INK}" fill-opacity="0.72" '
        f'transform="scale(1,{tilt*1.55:.2f})" transform-origin="{cx} {cy}">{glyph}</text>'
    )
    return "".join(s)


def coin_defs(hue):
    h = hue[1:]
    return (
        f'<linearGradient id="face{h}" x1="0" y1="0" x2="0.4" y2="1">'
        f'<stop offset="0" stop-color="{hue}"/><stop offset="0.55" stop-color="{hue}" stop-opacity="0.75"/>'
        f'<stop offset="1" stop-color="#ffffff" stop-opacity="0.35"/></linearGradient>'
        f'<linearGradient id="edge{h}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{hue}" stop-opacity="0.5"/>'
        f'<stop offset="1" stop-color="{hue}" stop-opacity="0.15"/></linearGradient>'
    )


def wrap(w, h, body, defs="", bg=INK):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
        f"<defs>{defs}</defs>"
        f'<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>'
    )


# ---------------------------------------------------------------- marquee tiles
def tile(glyph, code, hue, idx):
    w, h = 420, 270
    defs = (
        f'<radialGradient id="g{idx}" cx="0.3" cy="0.35" r="0.85">'
        f'<stop offset="0" stop-color="{hue}" stop-opacity="0.30"/>'
        f'<stop offset="1" stop-color="{INK}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="t{idx}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#ffffff" stop-opacity="0.92"/>'
        f'<stop offset="1" stop-color="{hue}"/></linearGradient>' + coin_defs(hue)
    )
    fs = 168 if len(glyph) == 1 else (104 if len(glyph) == 2 else 78)
    body = [
        f'<rect width="{w}" height="{h}" fill="url(#g{idx})"/>',
        guilloche(300, 135, 9, 26, 13, hue, 0.20),
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22" fill="none" stroke="{hue}" stroke-opacity="0.28"/>',
        f'<text x="46" y="{135 + fs*0.34:.0f}" font-family="{FONT}" font-weight="900" '
        f'font-size="{fs}" fill="url(#t{idx})">{glyph}</text>',
        f'<text x="48" y="44" font-family="{FONT}" font-weight="300" font-size="17" '
        f'letter-spacing="6" fill="{hue}" fill-opacity="0.85">{code}</text>',
        coin(352, 214, 34, hue, glyph if len(glyph) == 1 else "", 0.40, 2, 9),
    ]
    for i in range(7):
        y = 250 - i * 5
        body.append(f'<rect x="46" y="{y}" width="{18 + i*9}" height="2" fill="{hue}" opacity="0.25"/>')
    return wrap(w, h, "".join(body), defs)


for i, (g, c, hue) in enumerate(CURRENCIES):
    open(f"{OUT}/cur-{i:02d}.svg", "w").write(tile(g, c, hue, i))

# ---------------------------------------------------------------- hero artwork
def hero():
    w, h = 620, 720
    defs = coin_defs("#7CE0A6") + coin_defs("#E9C25C") + coin_defs("#8FD9F0") + (
        '<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">'
        '<stop offset="0" stop-color="#7CE0A6" stop-opacity="0.42"/>'
        '<stop offset="0.6" stop-color="#12A85F" stop-opacity="0.12"/>'
        '<stop offset="1" stop-color="#0C0C0C" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="orb" x1="0.2" y1="0" x2="0.8" y2="1">'
        '<stop offset="0" stop-color="#F4FFF7"/><stop offset="0.45" stop-color="#7CE0A6"/>'
        '<stop offset="1" stop-color="#116B41"/></linearGradient>'
        '<linearGradient id="note" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#CFE8C4" stop-opacity="0.95"/>'
        '<stop offset="1" stop-color="#5E8F72" stop-opacity="0.85"/></linearGradient>'
    )
    b = [f'<ellipse cx="310" cy="330" rx="300" ry="300" fill="url(#halo)"/>']
    # floating banknotes behind the orb
    for x, y, r, o in ((78, 214, -17, 0.5), (470, 176, 13, 0.42), (516, 430, -9, 0.34), (46, 452, 8, 0.3)):
        b.append(
            f'<g transform="translate({x} {y}) rotate({r})" opacity="{o}">'
            f'<rect width="150" height="76" rx="9" fill="url(#note)"/>'
            f'<circle cx="75" cy="38" r="22" fill="none" stroke="{INK}" stroke-opacity="0.4"/>'
            f'<circle cx="75" cy="38" r="15" fill="none" stroke="{INK}" stroke-opacity="0.25"/>'
            f'<rect x="12" y="12" width="126" height="52" rx="5" fill="none" stroke="{INK}" stroke-opacity="0.3"/></g>'
        )
    b.append(guilloche(310, 316, 14, 62, 11, "#7CE0A6", 0.22, 9))
    # the orb
    b.append('<circle cx="310" cy="316" r="132" fill="url(#orb)"/>')
    b.append('<circle cx="310" cy="316" r="132" fill="none" stroke="#0C0C0C" stroke-opacity="0.25" stroke-width="6"/>')
    b.append('<ellipse cx="266" cy="266" rx="52" ry="34" fill="#ffffff" opacity="0.35" transform="rotate(-28 266 266)"/>')
    b.append(
        f'<text x="310" y="388" text-anchor="middle" font-family="{FONT}" font-weight="900" '
        f'font-size="196" fill="{INK}" fill-opacity="0.78">$</text>'
    )
    # coin stacks at the base
    b.append(coin(150, 588, 66, "#E9C25C", "\u20ac", 0.4, 5, 15))
    b.append(coin(470, 604, 60, "#8FD9F0", "\u00a5", 0.4, 3, 15))
    b.append(coin(310, 640, 78, "#7CE0A6", "\u00a3", 0.4, 4, 16))
    return wrap(w, h, "".join(b), defs, "none")


open(f"{OUT}/hero-orb.svg", "w").write(hero())

# ---------------------------------------------------------------- decor objects
def decor_stack():
    d = coin_defs("#E9C25C") + coin_defs("#7CE0A6")
    b = [coin(150, 220, 96, "#E9C25C", "$", 0.4, 6, 22), coin(150, 96, 70, "#7CE0A6", "", 0.4, 0, 0)]
    return wrap(300, 300, "".join(b), d, "none")


def decor_vault():
    d = ('<linearGradient id="v" x1="0" y1="0" x2="1" y2="1">'
         '<stop offset="0" stop-color="#CFE8C4"/><stop offset="1" stop-color="#3E6650"/></linearGradient>'
         + coin_defs("#E9C25C"))
    b = [
        '<rect x="34" y="54" width="232" height="200" rx="26" fill="url(#v)"/>',
        f'<rect x="52" y="72" width="196" height="164" rx="18" fill="{INK}" fill-opacity="0.18"/>',
        '<circle cx="150" cy="154" r="58" fill="none" stroke="#0C0C0C" stroke-opacity="0.55" stroke-width="9"/>',
        '<circle cx="150" cy="154" r="30" fill="#0C0C0C" fill-opacity="0.5"/>',
    ]
    for a in range(0, 360, 45):
        r = math.radians(a)
        b.append(
            f'<rect x="146" y="80" width="8" height="26" rx="4" fill="{INK}" fill-opacity="0.55" '
            f'transform="rotate({a} 150 154)"/>'
        )
    b.append(coin(238, 258, 40, "#E9C25C", "$", 0.4, 2, 11))
    return wrap(300, 300, "".join(b), d, "none")


def decor_chart():
    d = ('<linearGradient id="bar" x1="0" y1="1" x2="0" y2="0">'
         '<stop offset="0" stop-color="#116B41"/><stop offset="1" stop-color="#7CE0A6"/></linearGradient>'
         + coin_defs("#7CE0A6"))
    b = []
    for i, hgt in enumerate((70, 116, 158, 214)):
        b.append(f'<rect x="{34 + i*62}" y="{262 - hgt}" width="44" height="{hgt}" rx="12" fill="url(#bar)"/>')
    b.append('<path d="M40 190 L102 152 L164 106 L232 48" fill="none" stroke="#E9C25C" stroke-width="7" stroke-linecap="round"/>')
    b.append(coin(240, 44, 40, "#7CE0A6", "$", 0.4, 0, 0))
    return wrap(300, 300, "".join(b), d, "none")


def decor_piggy():
    d = ('<linearGradient id="p" x1="0.2" y1="0" x2="0.8" y2="1">'
         '<stop offset="0" stop-color="#F4FFF7"/><stop offset="1" stop-color="#5E8F72"/></linearGradient>'
         + coin_defs("#E9C25C"))
    b = [
        '<ellipse cx="150" cy="180" rx="112" ry="86" fill="url(#p)"/>',
        '<ellipse cx="252" cy="166" rx="34" ry="30" fill="url(#p)"/>',
        f'<circle cx="262" cy="166" r="6" fill="{INK}" fill-opacity="0.5"/>',
        f'<circle cx="246" cy="166" r="6" fill="{INK}" fill-opacity="0.5"/>',
        f'<circle cx="196" cy="150" r="9" fill="{INK}" fill-opacity="0.7"/>',
        f'<path d="M104 108 L136 74 L152 118 Z" fill="url(#p)"/>',
        f'<rect x="112" y="96" width="76" height="11" rx="6" fill="{INK}" fill-opacity="0.55"/>',
        f'<rect x="86" y="248" width="30" height="34" rx="10" fill="url(#p)"/>',
        f'<rect x="182" y="248" width="30" height="34" rx="10" fill="url(#p)"/>',
        coin(150, 66, 40, "#E9C25C", "$", 0.4, 0, 0),
    ]
    return wrap(300, 300, "".join(b), d, "none")


open(f"{OUT}/decor-stack.svg", "w").write(decor_stack())
open(f"{OUT}/decor-vault.svg", "w").write(decor_vault())
open(f"{OUT}/decor-chart.svg", "w").write(decor_chart())
open(f"{OUT}/decor-piggy.svg", "w").write(decor_piggy())

# ---------------------------------------------------------------- guide art
def art(idx, hue, glyph, mode, w=800, h=600):
    d = (f'<radialGradient id="a{idx}" cx="0.4" cy="0.3" r="0.9">'
         f'<stop offset="0" stop-color="{hue}" stop-opacity="0.34"/>'
         f'<stop offset="1" stop-color="{INK}" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="b{idx}" x1="0" y1="1" x2="0" y2="0">'
         f'<stop offset="0" stop-color="{hue}" stop-opacity="0.25"/>'
         f'<stop offset="1" stop-color="{hue}"/></linearGradient>' + coin_defs(hue))
    b = [f'<rect width="{w}" height="{h}" fill="url(#a{idx})"/>']
    cx, cy = w / 2, h / 2
    if mode == "rings":
        b.append(guilloche(cx, cy, 16, 40, 16, hue, 0.28, 12))
        b.append(coin(cx, cy, min(w, h) * 0.21, hue, glyph, 0.4, 3, 16))
    elif mode == "bars":
        n = 7
        bw = w / (n * 1.8)
        for i in range(n):
            hh = h * (0.16 + 0.1 * i)
            b.append(f'<rect x="{w*0.08 + i*bw*1.7:.0f}" y="{h*0.86 - hh:.0f}" width="{bw:.0f}" height="{hh:.0f}" rx="{bw*0.3:.0f}" fill="url(#b{idx})"/>')
        b.append(coin(w * 0.78, h * 0.24, min(w, h) * 0.14, hue, glyph, 0.4, 2, 12))
    elif mode == "notes":
        for i, (x, y, r) in enumerate(((0.14, 0.2, -14), (0.5, 0.12, 7), (0.3, 0.55, -6), (0.66, 0.5, 12))):
            b.append(
                f'<g transform="translate({w*x:.0f} {h*y:.0f}) rotate({r})" opacity="0.75">'
                f'<rect width="{w*0.3:.0f}" height="{h*0.2:.0f}" rx="12" fill="{hue}" fill-opacity="0.3" stroke="{hue}" stroke-opacity="0.6"/>'
                f'<circle cx="{w*0.15:.0f}" cy="{h*0.1:.0f}" r="{h*0.06:.0f}" fill="none" stroke="{hue}" stroke-opacity="0.7"/></g>'
            )
        b.append(coin(w * 0.5, h * 0.78, min(w, h) * 0.15, hue, glyph, 0.4, 3, 13))
    elif mode == "spiral":
        pts = []
        for i in range(260):
            t = i / 26
            rr = 6 * t
            pts.append(f"{cx + rr*math.cos(t)*1.5:.1f},{cy + rr*math.sin(t):.1f}")
        b.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{hue}" stroke-opacity="0.55" stroke-width="3"/>')
        b.append(coin(cx, cy, min(w, h) * 0.16, hue, glyph, 0.4, 4, 14))
    return wrap(w, h, "".join(b), d)


GUIDE_ART = [
    ("g1a", "#7CE0A6", "$", "rings", 800, 460), ("g1b", "#E9C25C", "\u20ac", "bars", 800, 620),
    ("g1c", "#8FD9F0", "\u00a3", "notes", 900, 1100),
    ("g2a", "#E9C25C", "$", "notes", 800, 460), ("g2b", "#7CE0A6", "\u00a5", "spiral", 800, 620),
    ("g2c", "#F5A623", "\u20bf", "rings", 900, 1100),
    ("g3a", "#8FD9F0", "\u20b9", "bars", 800, 460), ("g3b", "#7CE0A6", "$", "rings", 800, 620),
    ("g3c", "#E9C25C", "\u20ac", "spiral", 900, 1100),
]
for i, (n, hue, g, m, w, h) in enumerate(GUIDE_ART):
    open(f"{OUT}/{n}.svg", "w").write(art(i + 40, hue, g, m, w, h))

# article headers
for i, (n, hue, g, m) in enumerate([
    ("art-emergency", "#7CE0A6", "$", "rings"), ("art-budget", "#E9C25C", "\u20ac", "bars"),
    ("art-debt", "#8FD9F0", "\u00a3", "spiral"), ("art-compound", "#F5A623", "\u20bf", "spiral"),
    ("art-income", "#7CE0A6", "\u00a5", "bars"), ("art-loan", "#E9C25C", "$", "rings"),
]):
    open(f"{OUT}/{n}.svg", "w").write(art(i + 60, hue, g, m, 1200, 500))

# ---------------------------------------------------------------- favicon
fav = wrap(64, 64,
    '<circle cx="32" cy="32" r="30" fill="url(#fg)"/>'
    f'<text x="32" y="47" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="42" fill="{INK}">$</text>',
    '<linearGradient id="fg" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#F4FFF7"/><stop offset="0.5" stop-color="#7CE0A6"/>'
    '<stop offset="1" stop-color="#E9C25C"/></linearGradient>', "none")
open(f"{OUT}/favicon.svg", "w").write(fav)

print("generated", len(os.listdir(OUT)), "svg files")
