#!/usr/bin/env python3
"""Writes Casks/<name>.rb from .github/cask-templates for the latest published release of each app.

Drafts and prereleases are ignored (GitHub's "latest release" never points to them), so a cask only
changes once a release is published. A cask that is already on the latest version is left alone.
Fails loudly when a release has no matching DMG, instead of writing a broken cask.
"""
import hashlib
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# cask name -> GitHub repo and one asset pattern per architecture placeholder
APPS = {
    "3d-hoard-deck": {
        "repo": "Ragin-LundF/3d-hoard-deck",
        "assets": {"ARM": r"_aarch64\.dmg$", "INTEL": r"_x64\.dmg$"},
    },
    "ragin-dms": {
        "repo": "Ragin-LundF/ragin-dms",
        "assets": {"ARM": r"\.dmg$"},
    },
    "ruleengine-ui": {
        "repo": "Ragin-LundF/rule-engine",
        "assets": {"ARM": r"\.dmg$"},
    },
}


def get(url: str, accept: str = "application/vnd.github+json") -> bytes:
    request = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": "homebrew-tap-updater"})
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def current_version(cask: Path) -> str | None:
    if not cask.exists():
        return None
    match = re.search(r'^\s*version "([^"]+)"', cask.read_text(), re.MULTILINE)
    return match.group(1) if match else None


def update(name: str, app: dict) -> bool:
    release = json.loads(get(f"https://api.github.com/repos/{app['repo']}/releases/latest"))
    version = release["tag_name"].removeprefix("v")
    cask = ROOT / "Casks" / f"{name}.rb"
    if current_version(cask) == version and not os.environ.get("FORCE"):
        print(f"{name}: {version} is current")
        return False

    text = (ROOT / ".github" / "cask-templates" / f"{name}.rb").read_text().replace("@@VERSION@@", version)
    for placeholder, pattern in app["assets"].items():
        matches = [asset for asset in release["assets"] if re.search(pattern, asset["name"])]
        if len(matches) != 1:
            names = ", ".join(asset["name"] for asset in release["assets"]) or "none"
            sys.exit(f"{name} {version}: expected one asset matching {pattern}, release has: {names}")
        asset = matches[0]
        digest = hashlib.sha256(get(asset["browser_download_url"], "application/octet-stream")).hexdigest()
        url = asset["browser_download_url"].replace(version, "#{version}")
        text = text.replace(f"@@SHA256_{placeholder}@@", digest).replace(f"@@URL_{placeholder}@@", url)

    if "@@" in text:
        sys.exit(f"{name}: template has placeholders without an asset pattern")
    cask.parent.mkdir(exist_ok=True)
    cask.write_text(text)
    print(f"{name}: updated to {version}")
    return True


if __name__ == "__main__":
    only = set(sys.argv[1:])
    changed = [name for name, app in APPS.items() if (not only or name in only) and update(name, app)]
    if out := os.environ.get("GITHUB_OUTPUT"):
        with open(out, "a") as file:
            file.write(f"changed={' '.join(changed)}\n")
