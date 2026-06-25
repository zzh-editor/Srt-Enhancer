#!/usr/bin/env python3
"""
Verify standard casing of English terms via web lookup and heuristics.

Accepts terms from CLI args or from --check-casing output,
attempts web verification, and outputs suggested map entries.

Usage:
  python3 scripts/casing_verify.py obj OBJ FBX fbx  # check these terms
  python3 scripts/casing_verify.py --from-file terms.txt
  python3 casing_verify.py --interactive  # paste terms manually
"""

import argparse
import json
import re
import sys
import textwrap
import urllib.request
import urllib.parse


# ── Heuristic patterns ─────────────────────────────────────────────

EXTENSION_PATTERN = re.compile(r'^\.?[a-z0-9]{2,6}$', re.IGNORECASE)

# File extensions that are conventionally lowercase
LOWERCASE_EXTENSIONS = {
    "obj", "fbx", "gltf", "glb", "usd", "usdz", "dae", "stl", "abc",
    "ma", "mb", "exr", "hdr", "tga", "tiff", "tif", "png", "jpeg",
    "jpg", "bmp", "psd", "svg", "webp", "wav", "mp3", "mp4", "mov",
    "avi", "mxf", "iges", "step", "step", "iges",
    "py", "js", "ts", "json", "xml", "yaml", "yml", "toml",
    "md", "txt", "csv", "log", "cfg", "ini", "conf",
    "zip", "tar", "gz", "rar", "7z",
    "dll", "exe", "app", "dmg", "pkg",
    "ttf", "otf", "woff", "woff2", "eot",
}

# Terms that are conventionally all-uppercase
UPPERCASE_TERMS = {
    "AI", "API", "SDK", "UI", "UX", "GUI", "CLI", "IDE",
    "HTML", "CSS", "JS", "TS", "JSON", "SQL", "HTTP", "HTTPS",
    "TCP", "IP", "DNS", "DHCP", "FTP", "SSH", "SSL", "TLS",
    "PNG", "JPEG", "GIF", "SVG", "XML", "YAML", "TOML",
    "GPU", "CPU", "RAM", "VRAM", "SSD", "HDD", "USB", "HDMI",
    "PBR", "LOD", "UV", "UVW", "FOV", "DOF", "HDR", "SDR",
    "AAA", "3D", "2D", "4K", "8K",
    "RGB", "RGBA", "CMYK", "HSV", "HSL",
    "IK", "FK", "NURBS", "MEL", "PY",
    "DXF", "DWG", "PDF", "ZIP", "RAR",
}


def heuristic_suggestion(term: str) -> str | None:
    """Return a heuristic casing suggestion or None if uncertain."""
    lower = term.lower()

    # If it's a file extension, it's lowercase
    if EXTENSION_PATTERN.match(term):
        if lower in LOWERCASE_EXTENSIONS:
            return lower

    # If it's a known uppercase term
    if lower in {t.lower() for t in UPPERCASE_TERMS}:
        for t in UPPERCASE_TERMS:
            if t.lower() == lower:
                return t

    return None


# ── Wikipedia lookup ───────────────────────────────────────────────

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"


def wikipedia_lookup(term: str) -> str | None:
    """Check Wikipedia for the standard casing of a term."""
    params = {
        "action": "query",
        "format": "json",
        "titles": term,
        "redirects": "1",
    }
    url = f"{WIKIPEDIA_API}?{urllib.parse.urlencode(params)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "opencode-casing-verify/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        pages = data.get("query", {}).get("pages", {})
        for pid, page in pages.items():
            if pid == "-1":
                continue
            title = page.get("title", "")
            if title.lower() == term.lower():
                return title
    except Exception:
        pass
    return None


# ── Main ───────────────────────────────────────────────────────────

def check_term(term: str, verbose: bool = False) -> dict:
    """Check a single term and return results."""
    result = {
        "term": term,
        "heuristic": heuristic_suggestion(term),
        "wikipedia": None,
        "suggested": None,
    }

    # Heuristic
    heuristic = heuristic_suggestion(term)
    if heuristic:
        result["heuristic"] = heuristic
    else:
        result["heuristic"] = None

    # Wikipedia
    wiki = wikipedia_lookup(term)
    result["wikipedia"] = wiki

    # Confidence-based suggestion
    if heuristic and wiki:
        if heuristic.lower() == wiki.lower():
            result["suggested"] = heuristic
            result["confidence"] = "high"
        else:
            # Conflict — show both, let user decide
            result["suggested"] = f"[heuristic:{heuristic}] [wiki:{wiki}]"
            result["confidence"] = "conflict"
    elif wiki:
        result["suggested"] = wiki
        result["confidence"] = "medium"
    elif heuristic:
        result["suggested"] = heuristic
        result["confidence"] = "low"
    else:
        result["suggested"] = term.lower()  # fallback: lowercase
        result["confidence"] = "none"

    return result


def main():
    parser = argparse.ArgumentParser(description="Verify standard casing of English terms")
    parser.add_argument("terms", nargs="*", help="terms to check")
    parser.add_argument("--from-file", "-f", help="read terms from file (one per line)")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="paste terms interactively")
    parser.add_argument("--verbose", "-v", action="store_true", help="show web lookup details")
    parser.add_argument("--output", "-o", choices=["table", "json", "map"], default="table",
                        help="output format")

    args = parser.parse_args()

    # Collect terms
    terms: list[str] = []
    if args.terms:
        terms.extend(args.terms)
    if args.from_file:
        with open(args.from_file, "r", encoding="utf-8") as f:
            for line in f:
                t = line.strip()
                if t:
                    terms.append(t)
    if args.interactive:
        print("粘贴术语（每行一个，Ctrl+D 结束）：", file=sys.stderr)
        for line in sys.stdin:
            t = line.strip()
            if t:
                terms.append(t)

    if not terms:
        # If no terms provided, try reading from stdin
        terms = [t.strip() for t in sys.stdin if t.strip()]
    if not terms:
        print("用法: python3 casing_verify.py obj OBJ FBX", file=sys.stderr)
        print("  或: python3 casing_verify.py --interactive", file=sys.stderr)
        sys.exit(1)

    # Deduplicate and sort by lowercase
    seen: set[str] = set()
    deduped: list[str] = []
    for t in terms:
        key = t.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(t)
    terms = sorted(deduped, key=str.lower)

    # Check each term
    results = [check_term(t, verbose=args.verbose) for t in terms]

    # Output
    if args.output == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif args.output == "map":
        for r in results:
            if r["suggested"]:
                if r["confidence"] == "conflict":
                    print(f"    # CONFLICT: heuristic={r['heuristic']}, wiki={r['wikipedia']}")
                    print(f"    # PICK ONE:")
                    print(f"    #   '{r['term'].lower()}': '{r['heuristic']}',  # file-format group")
                    print(f"    #   '{r['term'].lower()}': '{r['wikipedia']}',  # generic_acronym group")
                else:
                    print(f"    '{r['term'].lower()}': '{r['suggested']}',  # {r['confidence']}")
    else:
        # Table output
        print(f"{'Term':<20} {'Suggested':<20} {'Heuristic':<14} {'Wikipedia':<20} {'Confidence':<10}")
        print("-" * 84)
        for r in results:
            heur = r["heuristic"] or "-"
            wiki = r["wikipedia"] or "-"
            conf = r["confidence"] or "-"
            sug = r["suggested"] or "-"
            print(f"{r['term']:<20} {sug:<20} {heur:<14} {wiki:<20} {conf:<10}")

        print()
        print(f"{len(results)} term(s) checked")
        print()
        print("复制到 CAPITALIZATION_MAP 或 CASE_GROUPS（根据 domain 分组）:")


if __name__ == "__main__":
    main()
