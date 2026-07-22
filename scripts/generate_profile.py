#!/usr/bin/env python3
"""Generate the repository-owned Profile visual system from reviewed data."""

from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "profile.yml"
GENERATED_DIR = ROOT / "assets" / "generated"

THEMES = {
    "light": {
        "bg": "#F6F4EF", "surface": "#F0ECE4", "line": "#C9C4BA",
        "text": "#1B2128", "muted": "#6F7A85", "blue": "#5D7B8A",
        "blue2": "#7B8E9D", "red": "#A55E46", "gold": "#9C7C58",
    },
    "dark": {
        "bg": "#0B0E12", "surface": "#11161C", "line": "#2A323A",
        "text": "#E8ECEF", "muted": "#8E99A3", "blue": "#7FA8B8",
        "blue2": "#6F8F9F", "red": "#B86A4A", "gold": "#C6A96A",
    },
}


def load_config() -> dict[str, str]:
    # JSON is a valid YAML subset, so profile.yml stays dependency-free.
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def latest_release(repo: str, fallback: str) -> str:
    request = Request(
        f"https://api.github.com/repos/{repo}/releases/latest",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "PerrinYong-profile-generator",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    if token := os.environ.get("GITHUB_TOKEN"):
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urlopen(request, timeout=15) as response:
            payload = json.load(response)
        tag = str(payload.get("tag_name", "")).strip()
        return f"{repo.rsplit('/', 1)[-1]} · {tag}" if tag else fallback
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return fallback


def frame(c: dict[str, str], width: int, height: int) -> str:
    return f'''<defs>
    <pattern id="paper" width="36" height="36" patternUnits="userSpaceOnUse">
      <path d="M0 35.5H36M35.5 0V36" fill="none" stroke="{c['line']}" stroke-opacity=".11" stroke-width=".6"/>
      <circle cx="6" cy="8" r=".65" fill="{c['muted']}" fill-opacity=".08"/>
    </pattern>
  </defs>
  <rect width="{width}" height="{height}" rx="18" fill="{c['bg']}"/>
  <rect width="{width}" height="{height}" rx="18" fill="url(#paper)"/>
  <rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="17.5" fill="none" stroke="{c['line']}"/>'''


def render_hero(c: dict[str, str]) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="380" viewBox="0 0 1200 380" role="img" aria-labelledby="title desc">
  <title id="title">Yong — Engineering Across Boundaries</title>
  <desc id="desc">A quiet ink-line engineering topology connects languages, runtimes, platforms, and products.</desc>
  {frame(c, 1200, 380)}
  <path d="M0 319C176 291 286 336 438 310S730 264 904 292s198 5 296-20v108H0Z" fill="{c['surface']}" fill-opacity=".72"/>
  <g font-family="IBM Plex Sans, Inter, Segoe UI, Arial, sans-serif">
    <text x="64" y="66" fill="{c['blue']}" font-size="12" font-weight="650" letter-spacing="3.2">YONG / ENGINEERING ACROSS BOUNDARIES</text>
    <text x="64" y="132" fill="{c['text']}" font-size="43" font-weight="650" letter-spacing="-.8">Turning complex workflows</text>
    <text x="64" y="183" fill="{c['text']}" font-size="43" font-weight="650" letter-spacing="-.8">into reliable software.</text>
    <text x="65" y="226" fill="{c['muted']}" font-size="16">Cross-Platform Software Engineer &amp; Product Builder</text>
    <line x1="65" y1="254" x2="286" y2="254" stroke="{c['line']}"/>
    <circle cx="65" cy="254" r="3.5" fill="{c['red']}"/>
    <text x="65" y="282" fill="{c['muted']}" font-family="IBM Plex Mono, Consolas, monospace" font-size="10" letter-spacing="1.2">QUIET SYSTEMS · CLEAR STRUCTURE · RELIABLE OUTCOMES</text>
  </g>

  <g transform="translate(695 38)" fill="none" stroke-linecap="round">
    <path d="M2 270C96 241 113 193 188 184s113-52 164-92 86-50 143-64" stroke="{c['blue']}" stroke-width="1.5"/>
    <path d="M0 292C72 268 132 268 201 224s133-41 194-66 86-20 110-19" stroke="{c['blue2']}" stroke-opacity=".58" stroke-width="1"/>
    <path d="M41 120C106 145 151 136 221 91s124-40 181-14 86 20 111 7" stroke="{c['line']}" stroke-width="1"/>
    <path d="M88 62C137 77 192 64 253 35s111-22 176-2" stroke="{c['line']}" stroke-opacity=".72" stroke-width=".8"/>
    <path d="M57 236C105 224 143 227 188 184" stroke="{c['line']}" stroke-dasharray="3 8"/>
    <path d="M352 92C392 80 441 69 491 32" stroke="{c['gold']}" stroke-opacity=".62" stroke-dasharray="3 8"/>
  </g>

  <g font-family="IBM Plex Mono, Consolas, monospace" font-size="9" letter-spacing="1.1">
    <g transform="translate(716 296)"><circle r="5" fill="{c['bg']}" stroke="{c['blue']}" stroke-width="1.6"/><text x="14" y="4" fill="{c['muted']}">LANGUAGE</text></g>
    <g transform="translate(883 222)"><circle r="5" fill="{c['bg']}" stroke="{c['blue']}" stroke-width="1.6"/><text x="14" y="4" fill="{c['muted']}">RUNTIME</text></g>
    <g transform="translate(1047 130)"><circle r="5" fill="{c['bg']}" stroke="{c['blue2']}" stroke-width="1.6"/><text x="14" y="4" fill="{c['muted']}">PLATFORM</text></g>
    <g transform="translate(1173 66)"><circle r="5" fill="{c['red']}"/><text x="-14" y="-12" text-anchor="end" fill="{c['gold']}">PRODUCT</text></g>
  </g>

  <line x1="64" y1="332" x2="1136" y2="332" stroke="{c['line']}"/>
  <text x="64" y="354" fill="{c['muted']}" font-family="IBM Plex Mono, Consolas, monospace" font-size="9" letter-spacing="1.2">LANGUAGES / PLATFORMS / ENGINES / PRODUCTS</text>
  <text x="1136" y="354" text-anchor="end" fill="{c['muted']}" font-family="IBM Plex Mono, Consolas, monospace" font-size="9" letter-spacing="1.2">AI: MULTIPLIER, NOT FOUNDATION</text>
</svg>'''


def render_capability_map(c: dict[str, str]) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="330" viewBox="0 0 1200 330" role="img" aria-labelledby="title desc">
  <title id="title">Capability topology</title>
  <desc id="desc">Five engineering capabilities converge on reliable software through restrained ink-like lines.</desc>
  {frame(c, 1200, 330)}
  <g fill="none" stroke="{c['line']}" stroke-width="1.15">
    <path d="M295 92C401 92 442 144 518 154"/><path d="M295 238C400 238 439 190 518 176"/>
    <path d="M905 92C798 92 756 144 682 154"/><path d="M905 238C798 238 757 190 682 176"/>
    <path d="M600 76V132" stroke="{c['gold']}" stroke-opacity=".7"/>
  </g>
  <g font-family="IBM Plex Sans, Inter, Segoe UI, Arial, sans-serif">
    <g transform="translate(56 57)"><text y="14" fill="{c['text']}" font-size="13" font-weight="650" letter-spacing="1.2">CROSS-LANGUAGE</text><line y1="28" x2="184" y2="28" stroke="{c['line']}"/><text y="50" fill="{c['muted']}" font-size="12">C# · C++ · Java · Python</text><text y="69" fill="{c['muted']}" font-size="10">Native bridges · SDK contracts</text></g>
    <g transform="translate(56 203)"><text y="14" fill="{c['text']}" font-size="13" font-weight="650" letter-spacing="1.2">CROSS-PLATFORM</text><line y1="28" x2="184" y2="28" stroke="{c['line']}"/><text y="50" fill="{c['muted']}" font-size="12">Windows · Android · iOS · WebGL</text><text y="69" fill="{c['muted']}" font-size="10">Compatibility · Delivery constraints</text></g>
    <g transform="translate(944 57)"><text y="14" fill="{c['text']}" font-size="13" font-weight="650" letter-spacing="1.2">DELIVERY SYSTEMS</text><line y1="28" x2="184" y2="28" stroke="{c['line']}"/><text y="50" fill="{c['muted']}" font-size="12">CI/CD · Testing · Diagnostics</text><text y="69" fill="{c['muted']}" font-size="10">Observability · Verifiable completion</text></g>
    <g transform="translate(944 203)"><text y="14" fill="{c['text']}" font-size="13" font-weight="650" letter-spacing="1.2">AGENT WORKFLOWS</text><line y1="28" x2="184" y2="28" stroke="{c['line']}"/><text y="50" fill="{c['muted']}" font-size="12">Responsibilities · Tools · Review</text><text y="69" fill="{c['muted']}" font-size="10">Governance · Durable context</text></g>
    <g transform="translate(477 25)"><text x="123" y="14" text-anchor="middle" fill="{c['text']}" font-size="13" font-weight="650" letter-spacing="1.2">ENGINE &amp; RUNTIME</text><line y1="28" x2="246" y2="28" stroke="{c['gold']}"/><text x="123" y="50" text-anchor="middle" fill="{c['muted']}" font-size="11">Unity · Unreal · Cocos · Native · Web</text></g>
  </g>
  <g transform="translate(518 132)" font-family="IBM Plex Sans, Inter, Segoe UI, Arial, sans-serif">
    <rect width="164" height="66" rx="33" fill="{c['surface']}" stroke="{c['blue']}" stroke-width="1.2"/>
    <circle cx="18" cy="33" r="3.5" fill="{c['red']}"/>
    <text x="92" y="30" text-anchor="middle" fill="{c['text']}" font-size="13" font-weight="650" letter-spacing="1.2">RELIABLE SOFTWARE</text>
    <text x="92" y="48" text-anchor="middle" fill="{c['muted']}" font-family="IBM Plex Mono, Consolas, monospace" font-size="8.5">UNDERSTAND · TEST · REVIEW</text>
  </g>
  <text x="600" y="303" text-anchor="middle" fill="{c['muted']}" font-family="IBM Plex Mono, Consolas, monospace" font-size="9" letter-spacing="1.5">BOUNDARIES BECOME EXPLICIT INTERFACES</text>
</svg>'''


def render_featured_systems(c: dict[str, str]) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="330" viewBox="0 0 1200 330" role="img" aria-labelledby="title desc">
  <title id="title">Featured systems</title>
  <desc id="desc">CrewBee and PilotDeck presented as two complementary engineering systems.</desc>
  {frame(c, 1200, 330)}
  <text x="52" y="48" fill="{c['blue']}" font-family="IBM Plex Mono, Consolas, monospace" font-size="10" letter-spacing="2.4">FEATURED SYSTEMS / 02</text>
  <line x1="600" y1="72" x2="600" y2="278" stroke="{c['line']}"/>
  <g font-family="IBM Plex Sans, Inter, Segoe UI, Arial, sans-serif">
    <g transform="translate(54 82)">
      <text x="0" y="32" fill="{c['line']}" font-size="48" font-weight="300">01</text>
      <circle cx="492" cy="22" r="4" fill="{c['blue']}"/>
      <text x="0" y="78" fill="{c['text']}" font-size="25" font-weight="650">CrewBee</text>
      <text x="0" y="108" fill="{c['blue']}" font-size="11" font-weight="650" letter-spacing="1.5">MAINTAINABLE AGENT TEAMS</text>
      <text x="0" y="147" fill="{c['muted']}" font-size="13">Prompts, roles, review, and completion criteria</text>
      <text x="0" y="169" fill="{c['muted']}" font-size="13">shaped into reusable engineering assets.</text>
      <line x1="0" y1="199" x2="492" y2="199" stroke="{c['line']}"/>
      <text x="0" y="224" fill="{c['muted']}" font-family="IBM Plex Mono, Consolas, monospace" font-size="9" letter-spacing="1.2">ASSET LAYER · REVIEW · VERIFIABLE COMPLETION</text>
    </g>
    <g transform="translate(654 82)">
      <text x="0" y="32" fill="{c['line']}" font-size="48" font-weight="300">02</text>
      <circle cx="492" cy="22" r="4" fill="{c['red']}"/>
      <text x="0" y="78" fill="{c['text']}" font-size="25" font-weight="650">PilotDeck</text>
      <text x="0" y="108" fill="{c['gold']}" font-size="11" font-weight="650" letter-spacing="1.5">OBSERVABLE AGENT WORK</text>
      <text x="0" y="147" fill="{c['muted']}" font-size="13">Projects, runs, events, audit trails, and costs</text>
      <text x="0" y="169" fill="{c['muted']}" font-size="13">shaped into a lightweight operating layer.</text>
      <line x1="0" y1="199" x2="492" y2="199" stroke="{c['line']}"/>
      <text x="0" y="224" fill="{c['muted']}" font-family="IBM Plex Mono, Consolas, monospace" font-size="9" letter-spacing="1.2">PROJECTOPS × AGENTOPS · AUDIT · COST VISIBILITY</text>
    </g>
  </g>
</svg>'''


def render_pulse(c: dict[str, str], config: dict[str, str], release: str) -> str:
    focus = escape(config["current_focus"])
    systems = escape(config["featured_systems"])
    principle = escape(config["operating_principle"])
    release = escape(release)
    lens = escape(f"{config['engineering_lens_primary']} · {config['engineering_lens_secondary']}")
    rows = [
        ("CURRENT FOCUS", focus, c["blue"]),
        ("FEATURED SYSTEMS", systems, c["blue2"]),
        ("LATEST PUBLIC RELEASE", release, c["red"]),
        ("OPERATING PRINCIPLE", principle, c["gold"]),
    ]
    row_svg = []
    for index, (label, value, accent) in enumerate(rows):
        y = 80 + index * 48
        row_svg.append(f'''<line x1="48" y1="{y + 30}" x2="1152" y2="{y + 30}" stroke="{c['line']}"/>
    <circle cx="53" cy="{y}" r="3" fill="{accent}"/>
    <text x="70" y="{y + 4}" fill="{c['muted']}" font-family="IBM Plex Mono, Consolas, monospace" font-size="9" letter-spacing="1.4">{label}</text>
    <text x="286" y="{y + 5}" fill="{c['text']}" font-family="IBM Plex Sans, Inter, Segoe UI, Arial, sans-serif" font-size="13" font-weight="550">{value}</text>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="310" viewBox="0 0 1200 310" role="img" aria-labelledby="title desc">
  <title id="title">System pulse</title>
  <desc id="desc">A restrained status panel showing current engineering focus and the latest public release.</desc>
  {frame(c, 1200, 310)}
  <text x="48" y="48" fill="{c['text']}" font-family="IBM Plex Sans, Inter, Segoe UI, Arial, sans-serif" font-size="16" font-weight="650" letter-spacing="2">SYSTEM PULSE</text>
  <circle cx="1024" cy="43" r="3.5" fill="{c['red']}"/>
  <text x="1038" y="47" fill="{c['muted']}" font-family="IBM Plex Mono, Consolas, monospace" font-size="9" letter-spacing="1.2">QUIETLY RUNNING</text>
  {''.join(row_svg)}
  <text x="48" y="291" fill="{c['muted']}" font-family="IBM Plex Mono, Consolas, monospace" font-size="8.5" letter-spacing="1.1">ENGINEERING LENS / {lens}</text>
</svg>'''


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> None:
    config = load_config()
    release = latest_release(config["release_repo"], config["release_fallback"])
    for name, colors in THEMES.items():
        write(ROOT / "assets" / f"hero-{name}.svg", render_hero(colors))
        write(ROOT / "assets" / f"capability-map-{name}.svg", render_capability_map(colors))
        write(ROOT / "assets" / f"featured-systems-{name}.svg", render_featured_systems(colors))
        write(GENERATED_DIR / f"system-pulse-{name}.svg", render_pulse(colors, config, release))


if __name__ == "__main__":
    main()
