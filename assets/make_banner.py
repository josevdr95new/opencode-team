# -*- coding: utf-8 -*-
"""Genera el banner / social preview del repo OpenCode Team (1280x640).
Uso: python make_banner.py  ->  crea social-preview.png junto a este script.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1280, 640
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "social-preview.png")

PURPLE = (124, 58, 237)
AGENTS = [
    ("designer", (236, 72, 153)),
    ("frontend", (6, 182, 212)),
    ("backend", (16, 185, 129)),
    ("developer", (139, 92, 246)),
    ("debugger", (245, 158, 11)),
    ("security", (239, 68, 68)),
]


def font(bold, size):
    names = ["segoeuib.ttf" if bold else "segoeui.ttf",
             "arialbd.ttf" if bold else "arial.ttf"]
    for n in names:
        p = os.path.join("C:/Windows/Fonts", n)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default(size)


def main():
    # Fondo con degradado vertical
    img = Image.new("RGB", (W, H), (13, 17, 23))
    top, bottom = (13, 17, 23), (24, 30, 40)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)

    # Resplandor morado tras la red de la derecha
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([780, 60, 1300, 580], fill=PURPLE + (55,))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    d = ImageDraw.Draw(img)

    # --- Red del orquestador (derecha) ---
    cx, cy = 985, 315
    import math
    R = 185
    positions = []
    for i in range(6):
        ang = math.radians(-90 + i * 60)
        positions.append((cx + R * math.cos(ang), cy + R * math.sin(ang)))

    for (px, py), (_, color) in zip(positions, AGENTS):
        d.line([(cx, cy), (px, py)], fill=color + (0,) if False else tuple(
            int((color[i] + 40) / 2) for i in range(3)), width=4)

    for (px, py), (_, color) in zip(positions, AGENTS):
        r = 36
        soft = tuple(min(255, c + 40) for c in color)
        d.ellipse([px - r, py - r, px + r, py + r],
                  fill=tuple(c // 4 for c in color), outline=soft, width=3)
        d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=color)

    # Hexágono central = orquestador
    hr = 74
    hexpts = [(cx + hr * math.cos(math.radians(a)),
               cy + hr * math.sin(math.radians(a))) for a in
              [30, 90, 150, 210, 270, 330]]
    d.polygon(hexpts, fill=(30, 22, 58), outline=PURPLE)
    d.polygon([(cx + hr * 0.55 * math.cos(math.radians(a)),
                cy + hr * 0.55 * math.sin(math.radians(a))) for a in
               [30, 90, 150, 210, 270, 330]], outline=(167, 139, 250))
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=PURPLE)

    # --- Texto (izquierda) ---
    f_title = font(True, 96)
    f_sub = font(False, 34)
    f_chip = font(True, 21)
    f_small = font(False, 24)

    x0, y_title = 80, 150
    d.text((x0, y_title), "OpenCode", font=f_title, fill=(240, 246, 252))
    w_open = d.textlength("OpenCode ", font=f_title)
    d.text((x0 + w_open, y_title), "Team", font=f_title, fill=(167, 139, 250))

    d.text((x0 + 4, y_title + 128),
           "Equipo multi-agente · Spec-Driven Development",
           font=f_sub, fill=(139, 148, 158))

    # Pills de agentes
    x, y = x0, y_title + 210
    for name, color in AGENTS[:4]:
        tw = d.textlength(name, font=f_chip)
        d.rounded_rectangle([x, y, x + tw + 26, y + 38], radius=19,
                            fill=(23, 28, 36), outline=color, width=2)
        d.text((x + 13, y + 8), name, font=f_chip, fill=color)
        x += tw + 26 + 12
    x = x0
    y += 48
    for name, color in AGENTS[4:]:
        tw = d.textlength(name, font=f_chip)
        d.rounded_rectangle([x, y, x + tw + 26, y + 38], radius=19,
                            fill=(23, 28, 36), outline=color, width=2)
        d.text((x + 13, y + 8), name, font=f_chip, fill=color)
        x += tw + 26 + 12

    # Pie
    d.text((x0, H - 62), "github.com/josevdr95new/opencode-team",
           font=f_small, fill=(110, 118, 129))
    d.rectangle([x0, H - 84, x0 + 190, H - 80], fill=PURPLE)

    img.save(OUT, "PNG")
    print("OK ->", OUT)


if __name__ == "__main__":
    main()
