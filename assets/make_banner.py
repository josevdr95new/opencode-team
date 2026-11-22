# -*- coding: utf-8 -*-
"""Banner / social preview del repo OpenCode Team (1280x640) — v2 estilo impeccable.

Principios aplicados: jerarquía clara, ritmo vertical consistente, márgenes
generosos, un solo punto focal por zona, cero solapamientos (verificados
matemáticamente al final).

Uso: python make_banner.py  ->  crea social-preview.png junto a este script.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1280, 640
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "social-preview.png")

BG_TOP, BG_BOTTOM = (13, 17, 23), (24, 30, 40)
PURPLE = (124, 58, 237)
LILAC = (167, 139, 250)
TEXT = (240, 246, 252)
MUTED = (139, 148, 158)
FAINT = (110, 118, 129)

AGENTS = [
    ("designer", (236, 72, 153)),
    ("frontend", (6, 182, 212)),
    ("backend", (16, 185, 129)),
    ("developer", (139, 92, 246)),
    ("debugger", (245, 158, 11)),
    ("security", (239, 68, 68)),
]


def font(bold, size):
    for n in ["segoeuib.ttf" if bold else "segoeui.ttf",
              "arialbd.ttf" if bold else "arial.ttf"]:
        p = os.path.join("C:/Windows/Fonts", n)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default(size)


def main():
    # Degradado vertical de fondo
    img = Image.new("RGB", (W, H), BG_TOP)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)],
               fill=tuple(int(BG_TOP[i] + (BG_BOTTOM[i] - BG_TOP[i]) * t)
                          for i in range(3)))

    # Resplandor morado tras la red (solo mitad derecha, sin invadir el texto)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([860, 90, 1360, 570], fill=PURPLE + (50,))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    d = ImageDraw.Draw(img)

    # ---------- Zona derecha: red del orquestador ----------
    cx, cy, R, r_node = 1000, 318, 158, 34
    positions = [(cx + R * math.cos(math.radians(-90 + i * 60)),
                  cy + R * math.sin(math.radians(-90 + i * 60)))
                 for i in range(6)]

    for (px, py), (_, color) in zip(positions, AGENTS):
        link = tuple((color[i] + 30) // 2 for i in range(3))
        d.line([(cx, cy), (px, py)], fill=link, width=3)

    for (px, py), (_, color) in zip(positions, AGENTS):
        soft = tuple(min(255, c + 45) for c in color)
        d.ellipse([px - r_node, py - r_node, px + r_node, py + r_node],
                  fill=tuple(c // 5 for c in color), outline=soft, width=3)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=color)

    hexpts = lambda hr: [(cx + hr * math.cos(math.radians(a)),
                          cy + hr * math.sin(math.radians(a)))
                         for a in [30, 90, 150, 210, 270, 330]]
    d.polygon(hexpts(66), fill=(28, 21, 54), outline=PURPLE)
    d.polygon(hexpts(36), outline=LILAC)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=PURPLE)

    # ---------- Zona izquierda: texto (x máximo = 800) ----------
    X0 = 88
    f_title, f_sub, f_chip, f_foot = font(True, 82), font(False, 30), font(True, 20), font(False, 22)

    y_title = 128
    d.rectangle([X0 - 26, y_title + 8, X0 - 20, y_title + 96], fill=PURPLE)  # acento
    d.text((X0, y_title), "OpenCode", font=f_title, fill=TEXT)
    w1 = d.textlength("OpenCode ", font=f_title)
    d.text((X0 + w1, y_title), "Team", font=f_title, fill=LILAC)

    y_sub = y_title + 118  # ritmo: 118px bajo el título
    d.text((X0, y_sub), "Equipo multi-agente · Spec-Driven Development",
           font=f_sub, fill=MUTED)

    # Pills en una cuadrícula limpia de 2 filas x 3
    y_pills = y_sub + 64
    col_w = 205
    for i, (name, color) in enumerate(AGENTS):
        px = X0 + (i % 3) * col_w
        py = y_pills + (i // 3) * 50
        tw = d.textlength(name, font=f_chip)
        d.rounded_rectangle([px, py, px + tw + 24, py + 36], radius=18,
                            fill=(23, 28, 36), outline=color, width=2)
        d.text((px + 12, py + 7), name, font=f_chip, fill=color)

    # Pie con regla separadora
    y_foot = H - 66
    d.rectangle([X0, y_foot - 18, X0 + 176, y_foot - 14], fill=PURPLE)
    d.text((X0, y_foot), "github.com/josevdr95new/opencode-team",
           font=f_foot, fill=FAINT)

    # ---------- Verificación anti-solapamiento ----------
    title_w = w1 + d.textlength("Team", font=f_title)
    left_node_x = min(px for px, _ in positions) - r_node
    sub_w = d.textlength("Equipo multi-agente · Spec-Driven Development", font=f_sub)
    pills_end_y = y_pills + 50 + 36
    checks = [
        ("titulo vs red", title_w + X0 < left_node_x - 30),
        ("subtitulo vs red", sub_w + X0 < left_node_x - 30),
        ("pills vs pie", pills_end_y < y_foot - 30),
        ("pills vs ancho", X0 + 2 * col_w + 180 < left_node_x - 30),
        ("red dentro del lienzo", cy + R + r_node < H - 20 and cx + R + r_node < W - 10),
    ]
    ok = True
    for name, passed in checks:
        print(("OK  " if passed else "FALLA ") + name)
        ok = ok and passed

    img.save(OUT, "PNG")
    print("OK ->", OUT)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
