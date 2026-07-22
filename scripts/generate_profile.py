#!/usr/bin/env python3
"""Generate deterministic, repository-owned Profile visuals from reviewed data."""

from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "profile.yml"
OUTPUT_DIR = ROOT / "assets" / "generated"


def load_config() -> dict[str, str]:
    # JSON is a valid subset of YAML; keeping this file JSON-shaped avoids a
    # runtime dependency while preserving the profile.yml interface.
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
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")

    try:
        with urlopen(request, timeout=15) as response:
            payload = json.load(response)
        tag = str(payload.get("tag_name", "")).strip()
        project = repo.rsplit("/", 1)[-1]
        return f"{project} · {tag}" if tag else fallback
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return fallback


def render_pulse(config: dict[str, str], theme: str, release: str) -> str:
    if theme == "dark":
        colors = {
            "bg": "#07111f",
            "panel": "#0b1827",
            "border": "#294156",
            "text": "#e6eef4",
            "muted": "#91a7b9",
            "cyan": "#41c6dc",
            "violet": "#9b8cff",
            "amber": "#efb45e",
            "grid": "#7890a5",
        }
    else:
        colors = {
            "bg": "#f8fafc",
            "panel": "#ffffff",
            "border": "#cfdae3",
            "text": "#173044",
            "muted": "#667d8f",
            "cyan": "#168da4",
            "violet": "#6656c7",
            "amber": "#d18a2c",
            "grid": "#7890a5",
        }

    values = {
        "focus": escape(config["current_focus"]),
        "systems": escape(config["featured_systems"]),
        "lens_primary": escape(config["engineering_lens_primary"]),
        "lens_secondary": escape(config["engineering_lens_secondary"]),
        "principle": escape(config["operating_principle"]),
        "release": escape(release),
    }

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-labelledby="title desc">
  <title id="title">System pulse</title>
  <desc id="desc">Current engineering focus and latest public project signal.</desc>
  <defs>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="{colors['grid']}" stroke-opacity=".07" />
    </pattern>
    <linearGradient id="line" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{colors['cyan']}" />
      <stop offset=".55" stop-color="{colors['violet']}" />
      <stop offset="1" stop-color="{colors['amber']}" />
    </linearGradient>
  </defs>
  <rect width="1200" height="300" rx="20" fill="{colors['bg']}" />
  <rect width="1200" height="300" rx="20" fill="url(#grid)" />
  <g font-family="Segoe UI, Inter, Arial, sans-serif">
    <text x="48" y="48" fill="{colors['text']}" font-size="17" font-weight="750" letter-spacing="2.4">SYSTEM PULSE</text>
    <circle cx="1025" cy="42" r="5" fill="{colors['cyan']}" />
    <text x="1039" y="47" fill="{colors['muted']}" font-family="Consolas, monospace" font-size="10" letter-spacing="1">PUBLIC SIGNALS</text>
    <rect x="48" y="67" width="1104" height="3" rx="1.5" fill="url(#line)" />

    <g transform="translate(48 91)">
      <rect width="1104" height="66" rx="13" fill="{colors['panel']}" stroke="{colors['border']}" />
      <text x="22" y="25" fill="{colors['cyan']}" font-family="Consolas, monospace" font-size="10" font-weight="700" letter-spacing="1.2">CURRENT FOCUS</text>
      <text x="22" y="49" fill="{colors['text']}" font-size="16" font-weight="600">{values['focus']}</text>
    </g>

    <g transform="translate(48 177)">
      <g>
        <rect width="258" height="76" rx="13" fill="{colors['panel']}" stroke="{colors['border']}" />
        <text x="18" y="25" fill="{colors['violet']}" font-family="Consolas, monospace" font-size="9" font-weight="700" letter-spacing="1">FEATURED SYSTEMS</text>
        <text x="18" y="53" fill="{colors['text']}" font-size="14" font-weight="600">{values['systems']}</text>
      </g>
      <g transform="translate(282)">
        <rect width="258" height="76" rx="13" fill="{colors['panel']}" stroke="{colors['border']}" />
        <text x="18" y="25" fill="{colors['cyan']}" font-family="Consolas, monospace" font-size="9" font-weight="700" letter-spacing="1">ENGINEERING LENS</text>
        <text x="18" y="48" fill="{colors['text']}" font-size="12" font-weight="600">{values['lens_primary']}</text>
        <text x="18" y="64" fill="{colors['muted']}" font-size="11">{values['lens_secondary']}</text>
      </g>
      <g transform="translate(564)">
        <rect width="258" height="76" rx="13" fill="{colors['panel']}" stroke="{colors['border']}" />
        <text x="18" y="25" fill="{colors['amber']}" font-family="Consolas, monospace" font-size="9" font-weight="700" letter-spacing="1">OPERATING PRINCIPLE</text>
        <text x="18" y="53" fill="{colors['text']}" font-size="14" font-weight="600">{values['principle']}</text>
      </g>
      <g transform="translate(846)">
        <rect width="258" height="76" rx="13" fill="{colors['panel']}" stroke="{colors['border']}" />
        <text x="18" y="25" fill="{colors['cyan']}" font-family="Consolas, monospace" font-size="9" font-weight="700" letter-spacing="1">LATEST PUBLIC RELEASE</text>
        <text x="18" y="53" fill="{colors['text']}" font-size="14" font-weight="600">{values['release']}</text>
      </g>
    </g>
  </g>
  <text x="48" y="280" fill="{colors['muted']}" font-family="Consolas, monospace" font-size="9" letter-spacing="1">REVIEWED CONFIGURATION + GITHUB RELEASE API</text>
  <rect x=".5" y=".5" width="1199" height="299" rx="19.5" fill="none" stroke="{colors['border']}" />
</svg>
'''


def main() -> None:
    config = load_config()
    release = latest_release(config["release_repo"], config["release_fallback"])
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for theme in ("light", "dark"):
        output = OUTPUT_DIR / f"system-pulse-{theme}.svg"
        output.write_text(render_pulse(config, theme, release), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
