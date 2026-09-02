import math, cairosvg, sys
sys.path.insert(0, '.')
import gen_art as ga
from gen_art import guilloche, coin, coin_defs, FONT, INK
KANIT = FONT

W, H = 1200, 630
RING = ["\u20ac","\u00a3","\u00a5","\u20b9","\u20a9","\u20ba","\u20bd","\u20a6","\u0e3f","\u20ab","\u20aa","\u20b1"]
HUES = ["#E9C25C","#8FD9F0","#F0A8B8","#F5C77E","#A9E5C8","#EFA26A","#9FB4F2","#7CE0A6","#E9C25C","#F5A623","#8FD9F0","#F0A8B8"]

defs = (
 '<radialGradient id="bgh" cx="0.5" cy="0.46" r="0.62">'
 '<stop offset="0" stop-color="#12A85F" stop-opacity="0.34"/>'
 '<stop offset="1" stop-color="#0C0C0C" stop-opacity="0"/></radialGradient>'
 '<linearGradient id="orb" x1="0.2" y1="0" x2="0.8" y2="1">'
 '<stop offset="0" stop-color="#F4FFF7"/><stop offset="0.45" stop-color="#7CE0A6"/>'
 '<stop offset="1" stop-color="#116B41"/></linearGradient>'
 '<linearGradient id="wm" x1="0" y1="0" x2="0" y2="1">'
 '<stop offset="0" stop-color="#DCEBE0"/><stop offset="1" stop-color="#E9C25C"/></linearGradient>'
) + "".join(coin_defs(h) for h in set(HUES))

b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>', f'<rect width="{W}" height="{H}" fill="url(#bgh)"/>']
b.append(guilloche(W/2, 282, 18, 148, 16, "#7CE0A6", 0.22, 16, 240))
# currency ring
for i, (g, hue) in enumerate(zip(RING, HUES)):
    a = -math.pi/2 + 2*math.pi*i/len(RING)
    x, y = W/2 + 402*math.cos(a), 282 + 196*math.sin(a)
    ga.FONT = "DejaVu Sans"
    b.append(coin(x, y, 44, hue, g, 0.42, 2, 11))
    ga.FONT = KANIT
# center orb
b.append('<circle cx="600" cy="276" r="146" fill="url(#orb)"/>')
b.append('<circle cx="600" cy="276" r="146" fill="none" stroke="#0C0C0C" stroke-opacity="0.28" stroke-width="7"/>')
b.append('<ellipse cx="553" cy="224" rx="56" ry="35" fill="#fff" opacity="0.34" transform="rotate(-28 553 224)"/>')
b.append(f'<text x="600" y="356" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="214" fill="{INK}" fill-opacity="0.8">$</text>')
b.append(f'<text x="600" y="556" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="84" letter-spacing="3" fill="url(#wm)">MONETA</text>')
b.append(f'<text x="600" y="600" text-anchor="middle" font-family="{FONT}" font-weight="300" font-size="21" letter-spacing="4" fill="#D7E2EA" fill-opacity="0.8">LOAN AND INCOME CALCULATORS, PLAIN-ENGLISH MONEY GUIDES</text>')

svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs>{defs}</defs>{"".join(b)}</svg>'
open('img/og.svg','w').write(svg)
cairosvg.svg2png(url='img/og.svg', write_to='img/og.png', output_width=1200, output_height=630)
print('og done')
