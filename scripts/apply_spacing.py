"""
Deterministic CJK-Latin spacing and proper noun capitalization for mixed-language text.

Applies script boundary spacing (Han-Latin, Han-Digit, Latin-Digit),
proper noun capitalization via case-insensitive matching,
and number-unit compact formatting per the srt-enhancer mixed-typesetting spec.

Usage:
  python apply_spacing.py < input.txt > output.txt
  python apply_spacing.py --inline "Python3.9新功能"

Rules:
  - Capitalization: case-insensitive match of known proper nouns (ue5 → UE5, maya → Maya, ...)
  - Han ↔ Latin: add space (Python编程 → Python 编程)
  - Han ↔ Digit: add space (3个场景 → 3 个场景)
   - Latin ↔ Digit: add space (Python3.9 → Python 3.9; compact units like 5GB re-compacted afterward)
  - Protection zones (inline code `...`, math $...$, URLs) are preserved.
  - Number-unit compact: GB, MB, KB, TB, fps, FPS, etc.
"""

import re
import sys

# -- Protection zone patterns --
PROTECTION_PATTERNS = [
    (re.compile(r'`[^`]+`'), '__CODE__'),
    (re.compile(r'\$[^$]+?\$'), '__MATH__'),
    (re.compile(r'https?://[^\s,;:!?）)"\']+'), '__URL__'),
    (re.compile(r'/[^\s,;:!?）)"\']+(?=[\s,;:!?）)"\']|$)'), '__PATH__'),
    (re.compile(r'[A-Za-z]:\\[^\s,;:!?）)"\']+'), '__WPATH__'),
]

# -- Units that stay compact with preceding digits --
COMPACT_UNITS = [
    'GB', 'MB', 'KB', 'TB', 'PB',
    'G', 'K', 'M',  # standalone prefixes: 5G (gigabytes/generation), 4K (resolution)
    'fps', 'FPS',
    'GHz', 'MHz', 'kHz', 'Hz',
    'cm', 'mm', 'm', 'km', 'px',
    'W', 'kW',
    'h', 'min', 's', 'ms',
    '°C', '°F',
    '%',
]

COMPACT_UNITS_SORTED = sorted(COMPACT_UNITS, key=len, reverse=True)
COMPACT_PATTERN = re.compile(r'(\d+)\s*({})'.format('|'.join(re.escape(u) for u in COMPACT_UNITS_SORTED)))

# -- Capitalization map (case-insensitive matching → standard casing) --
CAPITALIZATION_MAP: dict[str, str] = {
    # Technical acronyms (all caps)
    'pcie': 'PCIe',
    'gpu': 'GPU', 'cpu': 'CPU', 'api': 'API', 'sdk': 'SDK',
    'ai': 'AI',
    'html': 'HTML', 'css': 'CSS', 'js': 'JS', 'ts': 'TS',
    'json': 'JSON', 'sql': 'SQL', 'http': 'HTTP', 'rest': 'REST',
    'tcp': 'TCP', 'ip': 'IP', 'usb': 'USB', 'hdmi': 'HDMI',
    'ssd': 'SSD', 'hdd': 'HDD', 'ram': 'RAM', 'vram': 'VRAM',
    'dns': 'DNS', 'dhcp': 'DHCP', 'ftp': 'FTP', 'ssh': 'SSH',
    'ssl': 'SSL', 'tls': 'TLS',
    'png': 'PNG', 'jpeg': 'JPEG', 'gif': 'GIF', 'svg': 'SVG',
    'xml': 'XML', 'yaml': 'YAML', 'toml': 'TOML',
    'cli': 'CLI', 'gui': 'GUI', 'ui': 'UI', 'ux': 'UX',
    'ide': 'IDE', 'db': 'DB', 'vm': 'VM', 'os': 'OS', 'bios': 'BIOS',
    # Domain-specific acronyms
    'ue5': 'UE5', 'ps': 'PS', 'hdr': 'HDR',
    # Brand/tool names
    'pureref': 'PureRef', 'perforce': 'Perforce', 'tapnow': 'TapNow',
    'claude': 'Claude', 'maya': 'Maya', 'blender': 'Blender',
    'photoshop': 'Photoshop', 'xcode': 'Xcode', 'github': 'GitHub',
    'nanite': 'Nanite', 'lumen': 'Lumen', 'megascans': 'Megascans',
    # Discipline-specific terms
    'rookies': 'Rookies', 'lightbox': 'LightBox', 'overwatch': 'Overwatch',
    'keyframe': 'Keyframe', 'playblast': 'Playblast',
    'hypergraph': 'Hypergraph', 'hypershade': 'Hypershade',
    # Multi-word terms (sorted by length, matched before single-word terms)
    'unreal engine': 'Unreal Engine',
    'tripo 3d ai': 'Tripo 3D AI',
    'concept artist': 'Concept Artist',
    'world partition': 'World Partition',
    'concept art': 'Concept Art',
    'art center': 'Art Center',
    'paint over': 'Paint Over',
}

# Generate Ctrl shortcut variants
for key_char in ('v', 'c', 'z', 's', 'a', 'x', 'p'):
    upper = key_char.upper()
    CAPITALIZATION_MAP[f'ctrl+{key_char}'] = f'Ctrl+{upper}'
    CAPITALIZATION_MAP[f'ctrl {key_char}'] = f'Ctrl+{upper}'
    CAPITALIZATION_MAP[f'ctrl{key_char}'] = f'Ctrl+{upper}'

# Build case-insensitive regex, multi-word terms first (longer → higher priority)
_CAP_TERMS_SORTED = sorted(CAPITALIZATION_MAP, key=len, reverse=True)
CAP_PATTERN = re.compile(
    '|'.join(r'\b' + re.escape(t) + r'\b' for t in _CAP_TERMS_SORTED),
    re.IGNORECASE | re.ASCII,
)


def _apply_capitalization(text: str) -> str:
    """Capitalize known proper nouns using case-insensitive word-boundary matching."""
    return CAP_PATTERN.sub(lambda m: CAPITALIZATION_MAP[m.group(0).lower()], text)


def _protect(text):
    """Replace protection zones with placeholders, return (processed, map)."""
    mapping = {}
    for idx, (pattern, tag) in enumerate(PROTECTION_PATTERNS):
        def replacer(m, tag=tag, idx=idx):
            placeholder = f'{tag}_{idx}_'
            mapping[placeholder] = m.group(0)
            return placeholder
        text = pattern.sub(replacer, text)
    return text, mapping


def _restore(text, mapping):
    """Restore protection zones from placeholders."""
    for placeholder, original in mapping.items():
        text = text.replace(placeholder, original)
    return text


def _apply_number_unit_compact(text):
    """Keep number+unit compact: 5GB → 5GB (not 5 GB)."""
    return COMPACT_PATTERN.sub(r'\1\2', text)


def _apply_script_spacing(text):
    """
    Insert space at every Han ↔ Latin, Han ↔ Digit, and Latin ↔ Digit boundary.
    Compact units are re-joined by _apply_number_unit_compact running afterward.
    """
    result = []
    prev_is_han = False
    prev_is_latin = False
    prev_is_digit = False

    for ch in text:
        cur_is_han = '\u4e00' <= ch <= '\u9fff' or '\u3400' <= ch <= '\u4dbf'
        cur_is_latin = 'a' <= ch <= 'z' or 'A' <= ch <= 'Z'
        cur_is_digit = '0' <= ch <= '9'

        if prev_is_han and (cur_is_latin or cur_is_digit):
            result.append(' ')
        elif prev_is_latin and cur_is_han:
            result.append(' ')
        elif prev_is_digit and cur_is_han:
            result.append(' ')
        elif prev_is_latin and cur_is_digit:
            result.append(' ')
        elif prev_is_digit and cur_is_latin:
            result.append(' ')

        result.append(ch)
        prev_is_han = cur_is_han
        prev_is_latin = cur_is_latin
        prev_is_digit = cur_is_digit

    return ''.join(result)


def apply_spacing(line):
    """Apply full spacing + capitalization pipeline to a single text line."""
    line = line.rstrip('\n')
    text, mapping = _protect(line)
    text = _apply_capitalization(text)
    text = _apply_script_spacing(text)
    text = _apply_number_unit_compact(text)
    text = _restore(text, mapping)
    return text


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--inline':
        print(apply_spacing(sys.argv[2]))
        return

    for line in sys.stdin:
        sys.stdout.write(apply_spacing(line))
        sys.stdout.write('\n')


if __name__ == '__main__':
    main()
