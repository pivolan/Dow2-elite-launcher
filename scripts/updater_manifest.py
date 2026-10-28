"""updater.json for the launcher self-update (tauri-plugin-updater, static JSON), next to the installers:
on a GitHub Release or in the download folder on the server.

  updater_manifest.py <version> <download url base> <dist folder>

Each installer in <dist folder> needs its .sig next to it (made by `cargo tauri build` with the updater key) and
becomes the platform entries below, pointing to <download url base>/<file>. A kind of installer that is not there
(e.g. no Mac build on a Linux server) is left out. The notes are changelog/<version>/en.md.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

CHANGELOG = Path(__file__).resolve().parent.parent / "changelog"

# file name ending → updater targets; the plugin looks up {os}-{arch}-{installer} first, then {os}-{arch}
TARGETS = [
    ("-setup.exe", ["windows-x86_64-nsis", "windows-x86_64"]),
    (".AppImage", ["linux-x86_64-appimage", "linux-x86_64"]),
    ("_amd64.deb", ["linux-x86_64-deb"]),
    # one universal .app for both Mac architectures
    ("-mac.app.tar.gz", ["darwin-x86_64-app", "darwin-aarch64-app", "darwin-x86_64", "darwin-aarch64"]),
]


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    version, base, dist = sys.argv[1], sys.argv[2].rstrip("/"), Path(sys.argv[3])
    platforms = {}
    for suffix, targets in TARGETS:
        files = sorted(f for f in dist.iterdir() if f.name.endswith(suffix))
        if not files:
            print(f"no *{suffix} in {dist}: left out", file=sys.stderr)
            continue
        if len(files) > 1:
            sys.exit(f"expected one *{suffix} in {dist}, found {[f.name for f in files]}")
        sig = files[0].with_name(files[0].name + ".sig")
        if not sig.is_file():
            sys.exit(f"{sig.name} is missing: was the launcher built with the updater key?")
        # Tauri names its installers with a space ("Elite Launcher_1.3.0_x64-setup.exe")
        entry = {"signature": sig.read_text(encoding="utf-8").strip(), "url": f"{base}/{quote(files[0].name)}"}
        for target in targets:
            platforms[target] = entry
    if not platforms:
        sys.exit(f"no installers in {dist}")
    notes = CHANGELOG / version / "en.md"
    manifest = {
        "version": version,
        "notes": notes.read_text(encoding="utf-8").strip() if notes.is_file() else "",
        "pub_date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "platforms": platforms,
    }
    json.dump(manifest, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
