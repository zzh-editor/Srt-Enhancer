"""
Deterministic CJK-Latin spacing and proper noun capitalization for mixed-language text.

Applies script boundary spacing (Han-Latin, Han-Digit, Latin-Digit),
proper noun capitalization via case-insensitive matching,
domain-aware case group normalization,
and number-unit compact formatting per the srt-enhancer mixed-typesetting spec.

Usage:
  python apply_spacing.py < input.txt > output.txt
  python apply_spacing.py --inline "Python3.9新功能"
  python apply_spacing.py --domain ai-3d < input.txt > output.txt

Rules:
  - Capitalization: case-insensitive match of known proper nouns (ue5 → UE5, maya → Maya, ...)
  - Case groups: domain-aware normalization (obj/OBJ/Obj → obj, HDR/hdr → HDR, ...)
  - Han ↔ Latin: add space (Python编程 → Python 编程)
  - Han ↔ Digit: add space (3个场景 → 3 个场景)
  - Latin ↔ Digit: add space (Python3.9 → Python 3.9; compact units re-compacted)
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
    (re.compile(r'(?<![A-Za-z0-9_])[pP](?:Cube|Sphere|Cylinder|Cone|Torus|Plane|Prism|Pipe)\d+(?![A-Za-z0-9_])'), '__MAYA_OBJ__'),
    # Protected compound terms — prevent script-spacing from splitting them
    (re.compile(
        r'\b(?:Hyper3D|ComfyUI|TapNow|NanoBanana|BananaPro|ContentAware|'
        r'TextureDelight|PureRef|FrontRight|MultiViewReference|'
        r'ShiftF5|ShiftF4|ShiftF6|CtrlV|CtrlC|CtrlZ|CtrlX|CtrlS|CtrlD|CtrlP|CtrlA|'
        r'Gen1\.5|Gen2\.5|Gen2|Gen1|'
        r'ImageTo3D|TextTo3D|AssetsBreakdown|AssetBreakdown|'
        r'QuickSort|OpenModelDB|FormRight)\b'
    ), '__COMPOUND__'),
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

# -- Domain-aware case normalization groups --
# Each group maps lowercase term → its standard casing in that context.
# Groups are activated based on --domain.
# CAPITALIZATION_MAP entries always take priority over these groups.

CASE_GROUPS: dict[str, dict[str, str]] = {
    "file_format": {
        "obj": "obj", "fbx": "fbx", "gltf": "gltf",
        "glb": "glb", "usd": "usd", "usdz": "usdz",
        "dae": "dae", "stl": "stl", "abc": "abc",
        "ma": "ma", "mb": "mb",
        "exr": "exr", "hdr": "hdr", "tga": "tga",
        "png": "png", "jpeg": "jpeg", "jpg": "jpg",
        "tiff": "tiff", "bmp": "bmp", "psd": "psd",
        "svg": "svg", "webp": "webp",
        "wav": "wav", "mp3": "mp3", "mp4": "mp4",
        "mov": "mov", "avi": "avi", "mxf": "mxf",
        "fbx": "fbx", "iges": "iges", "step": "step",
    },
    "generic_acronym": {
        "pbr": "PBR", "lod": "LOD", "uv": "UV", "nx": "NX",
        "fov": "FOV", "dof": "DOF", "sss": "SSS",
        "hdr": "HDR", "ldr": "LDR", "sdr": "SDR",
        "sbsar": "SBSAR", "sbs": "SBS",
        "nd": "ND", "ae": "AE", "pr": "PR",
        "bake": "Bake", "unfold": "Unfold",
    },
    "os_term": {
        "macos": "macOS", "ios": "iOS", "ipados": "iPadOS",
        "watchos": "watchOS", "tvos": "tvOS",
        "windows": "Windows", "linux": "Linux",
        "android": "Android",
    },
    "brand_tool": {
        "substance": "Substance", "painter": "Painter",
        "designer": "Designer", "sampler": "Sampler",
        "zbrush": "ZBrush", "marmoset": "Marmoset",
        "toolbag": "Toolbag", "speedtree": "SpeedTree",
        "worldmachine": "World Machine", "gaea": "Gaea",
        "unreal": "Unreal", "unity": "Unity", "godot": "Godot",
        "blender": "Blender", "houdini": "Houdini",
        "nuke": "Nuke", "fusion": "Fusion",
    },
    "ai_3d": {
        "rodin": "Rodin", "tripo": "Tripo", "meshy": "Meshy",
        "gen": "Gen", "legacy": "Legacy", "native": "Native",
        "point": "Point", "unfold": "Unfold",
    },
}

# Map domain → active case groups
DOMAIN_CASE_GROUPS: dict[str, list[str]] = {
    # generic_acronym first so it wins over file_format on conflicts like hdr
    # file_format is universal — file extension casing applies everywhere
    "general": ["generic_acronym", "os_term", "brand_tool", "file_format"],
    "ai-3d": ["generic_acronym", "os_term", "brand_tool", "ai_3d", "file_format"],
    "maya": ["generic_acronym", "os_term", "brand_tool", "ai_3d", "file_format"],
    "python": ["generic_acronym", "os_term", "file_format"],
    "gaming": ["generic_acronym", "os_term", "brand_tool", "file_format"],
}

DEFAULT_CASE_GROUPS = ["generic_acronym", "os_term", "file_format"]


def _get_active_case_groups(domain: str | None = None) -> list[str]:
    if domain and domain in DOMAIN_CASE_GROUPS:
        return DOMAIN_CASE_GROUPS[domain]
    return DEFAULT_CASE_GROUPS


def _build_case_group_pattern(group_names: list[str]) -> re.Pattern | None:
    """Build a single combined case-insensitive regex from selected groups."""
    all_terms: list[str] = []
    for name in group_names:
        group = CASE_GROUPS.get(name)
        if group:
            all_terms.extend(sorted(group, key=len, reverse=True))
    if not all_terms:
        return None
    return re.compile(
        '|'.join(r'\b' + re.escape(t) + r'\b' for t in all_terms),
        re.IGNORECASE | re.ASCII,
    )


def _apply_case_normalization(text: str, domain: str | None = None) -> str:
    """Apply domain-aware casing normalization to known terms."""
    groups = _get_active_case_groups(domain)
    pattern = _build_case_group_pattern(groups)
    if not pattern:
        return text

    # Build combined lookup: earlier group = higher priority (don't overwrite)
    lookup: dict[str, str] = {}
    for name in groups:
        group = CASE_GROUPS.get(name)
        if group:
            for k, v in group.items():
                if k not in lookup:
                    lookup[k] = v

    return pattern.sub(lambda m: lookup[m.group(0).lower()], text)


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
    prev_is_pct = False

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
        elif prev_is_han and ch == '%':
            result.append(' ')
        elif prev_is_pct and cur_is_han:
            result.append(' ')

        result.append(ch)
        prev_is_han = cur_is_han
        prev_is_latin = cur_is_latin
        prev_is_digit = cur_is_digit
        prev_is_pct = (ch == '%')

    text = ''.join(result)
    return text


def apply_spacing(line, domain=None):
    """Apply full spacing + capitalization pipeline to a single text line."""
    line = line.rstrip('\n')
    text, mapping = _protect(line)
    text = _apply_capitalization(text)
    text = _apply_case_normalization(text, domain=domain)
    text = _apply_script_spacing(text)
    text = _apply_number_unit_compact(text)
    # Post-spacing fixup: re-glue known multi-word compounds that spacing may have split
    FIXUP_COMPOUNDS = {
        r'\bHyper 3D\b': 'Hyper3D',
        r'\bImage 2 3D\b': 'Image To 3D',
        r'\bGen 1\.5\b': 'Gen1.5',
        r'\bGen 2\.5\b': 'Gen2.5',
        r'\bNano Banana\b': 'NanoBanana',
        r'\bNano Banana Pro\b': 'NanoBanana Pro',
        r'\bFront Right\b': 'FrontRight',
        r'\bTexture Delight\b': 'TextureDelight',
        r'\bMulti View Reference\b': 'MultiviewReference',
        r'\bShift F 5\b': 'Shift F5',
        r'\bShift F 4\b': 'Shift F4',
        r'\bAssets Breakdown\b': 'AssetsBreakdown',
        r'\bOpen Model DB\b': 'OpenModelDB',
    }
    for pattern, replacement in FIXUP_COMPOUNDS.items():
        text = re.sub(pattern, replacement, text)
    text = _restore(text, mapping)
    return text


def main():
    domain = None
    args = sys.argv[1:]

    if args and args[0] == '--domain' and len(args) >= 2:
        domain = args[1]
        args = args[2:]

    if args and args[0] == '--inline':
        print(apply_spacing(args[1], domain=domain))
        return

    for line in sys.stdin:
        sys.stdout.write(apply_spacing(line, domain=domain))
        sys.stdout.write('\n')


if __name__ == '__main__':
    main()
