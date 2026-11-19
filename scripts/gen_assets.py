#!/usr/bin/env python3
"""
Generates the SVGs used by the profile README (stdlib only).

Edit CONTENT, run `python scripts/gen_assets.py`, commit assets/.
"""
import math
import random
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# --------------------------------------------------------------------------- #
# CONTENT
# --------------------------------------------------------------------------- #
NAME = "Marc-Antoine Gaumond"
SUBTITLE = "Software Engineering · Polytechnique Montréal"

PROJECTS = [
    {
        "file": "project-moisson.svg",
        "title": "Moisson Montréal Tax Receipt Platform",
        "tag": "Hack4Impact",
        "accent": "#22c55e",
        "desc": [
            "Desktop app that issues CRA-compliant tax receipts for a food bank. I work on the",
            "backend: database schema, EF Core migrations and xUnit tests against real PostgreSQL.",
        ],
        "stack": "C# · ASP.NET Core · EF Core · PostgreSQL · Azure",
        "seed": 23,
    },
    {
        "file": "project-solfege.svg",
        "title": "Solfege",
        "tag": "AI DJ Transition Engine",
        "accent": "#a78bfa",
        "desc": [
            "Turns a playlist into a continuous DJ mix, ordered by Camelot key and energy, with",
            "downbeat-aligned transitions, EQ sweeps, stem-based bass swaps and a learned ranker.",
        ],
        "stack": "Python · scikit-learn · FastAPI · React · Redis",
        "seed": 5,
    },
    {
        "file": "project-fitfolio.svg",
        "title": "Fitfolio",
        "tag": "Multi-Agent Investment Copilot",
        "accent": "#ef4444",
        "desc": [
            "Built at the PolyFinances Datathon (National Bank × AWS). Six Claude sub-agents analyze",
            "520 assets, and every number in an answer must match a stored tool-call record.",
        ],
        "stack": "Python · FastAPI · AWS Bedrock · Strands · Neptune",
        "seed": 11,
    },
    {
        "file": "project-robot.svg",
        "title": "Autonomous Inspection Robot",
        "tag": "Course project",
        "accent": "#3b82f6",
        "desc": [
            "Runs floor-damage, item-count and person-detection inspections across 6 rooms, self-docks,",
            "and executes missions from EEPROM through an on-robot bytecode interpreter.",
        ],
        "stack": "Bare-metal C++17 · AVR · UART · I2C",
        "seed": 41,
    },
]

# --------------------------------------------------------------------------- #
# STYLE
# --------------------------------------------------------------------------- #
FONT = ("ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, "
        "'Liberation Mono', 'DejaVu Sans Mono', monospace")
BG = "#000000"
INK = "#ffffff"
MUTED = "#9a9a9a"
LINE = "#2a2a2a"
WAVE_A, WAVE_B = "#ffffff", "#5a5a5a"
CHAR = 0.6
BEAT = 60 / 128

CSS = (
    ".bar{transform-box:fill-box;transform-origin:center;"
    f"animation:pump {BEAT * 2:.3f}s ease-in-out infinite alternate}}"
    "@keyframes pump{from{transform:scaleY(.6)}to{transform:scaleY(1)}}"
    "@keyframes spin{to{transform:rotate(360deg)}}"
    "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"
)


def tw(text, size):
    return len(text) * size * CHAR


def t(x, y, text, size=14, fill=INK, weight=400, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" {extra}>{escape(text)}</text>')


def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}" '
            f'font-family="{FONT}">\n<style>{CSS}</style>\n{body}\n</svg>\n')


def envelope(n, seed, lo=0.15):
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, math.tau) for _ in range(3)]
    vals = [0.5 * math.sin(i / n * 6 + ph[0]) + 0.3 * math.sin(i / n * 17 + ph[1])
            + 0.2 * math.sin(i / n * 41 + ph[2]) + 0.3 * rnd.random()
            + (0.3 if i % 4 == 0 else 0) for i in range(n)]
    mn, mx = min(vals), max(vals)
    return [lo + (1 - lo) * (v - mn) / (mx - mn) for v in vals]


def waveform(x0, x1, cy, maxh, n, seed, fill, bar_w):
    step = (x1 - x0) / n
    out = []
    for i, a in enumerate(envelope(n, seed)):
        h = max(2.0, a * maxh)
        x = x0 + i * step + (step - bar_w) / 2
        out.append(f'<rect class="bar" x="{x:.1f}" y="{cy - h / 2:.1f}" width="{bar_w}" '
                   f'height="{h:.1f}" rx="{bar_w / 2}" fill="{fill}" '
                   f'style="animation-delay:-{(i * 0.04) % (BEAT * 4):.2f}s"/>')
    return "\n".join(out)


def frame(w, h):
    return (f'<rect width="{w}" height="{h}" rx="12" fill="{BG}"/>'
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" '
            f'fill="none" stroke="{LINE}"/>')


def cd(cx, cy, r, period=1.8):
    """Spinning disc, black and white."""
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#050505" stroke="{LINE}" stroke-width="2"/>']
    for rr in range(r - 8, 22, -7):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="#1c1c1c"/>')
    out.append(
        f'<g style="transform-origin:{cx}px {cy}px;animation:spin {period}s linear infinite">'
        f'<circle cx="{cx}" cy="{cy}" r="17" fill="{INK}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="3" fill="#050505"/>'
        f'<line x1="{cx}" y1="{cy - 19}" x2="{cx}" y2="{cy - r + 4}" stroke="{INK}" '
        f'stroke-width="2.5" stroke-linecap="round"/></g>')
    return "\n".join(out)


def header():
    W, H = 1200, 230
    x0, x1 = 56, 1144
    body = [
        f'<defs><linearGradient id="wf" gradientUnits="userSpaceOnUse" x1="{x0}" y1="0" '
        f'x2="{x1}" y2="0"><stop offset="0" stop-color="{WAVE_A}"/>'
        f'<stop offset="1" stop-color="{WAVE_B}"/></linearGradient></defs>',
        frame(W, H),
        t(x0, 92, NAME, 48, INK, 700, 'letter-spacing="-1"'),
        t(x0, 126, SUBTITLE, 18, MUTED),
        waveform(x0, x1, 180, 34, 136, 7, "url(#wf)", 3.5),
        cd(1074, 88, 58),
    ]
    return svg(W, H, "\n".join(body), f"{NAME}, {SUBTITLE}")


def project(p):
    W, H = 1200, 150
    acc = p["accent"]
    x = 40
    body = [
        frame(W, H),
        # tag is a tspan inside the title so the gap is font-independent
        f'<text x="{x}" y="50" font-size="22" fill="{INK}" font-weight="700">{escape(p["title"])}'
        f'<tspan dx="18" font-size="13" font-weight="400" fill="{acc}">{escape(p["tag"])}</tspan></text>',
    ]
    for i, line in enumerate(p["desc"]):
        assert tw(line, 13) <= 860 - x, f"too long: {line}"
        body.append(t(x, 82 + i * 20, line, 13, MUTED))
    body.append(t(x, 128, p["stack"], 12, INK, 400, 'fill-opacity=".7"'))
    body.append(waveform(900, W - 40, 75, 46, 52, p["seed"], acc, 3))
    return svg(W, H, "\n".join(body), f'{p["title"]}: {" ".join(p["desc"])}')


def main():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    files = {"header.svg": header()}
    for p in PROJECTS:
        files[p["file"]] = project(p)
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"wrote assets/{name}")


if __name__ == "__main__":
    main()
