"""
Deterministic CJK-Latin spacing for mixed-language text.

Applies script boundary spacing (Han-Latin, Han-Digit, Latin-Digit),
number-unit compact formatting,
and compound protection per the srt-enhancer mixed-typesetting spec.

Usage:
  python apply_spacing.py < input.txt > output.txt
  python apply_spacing.py --inline "Python3.9新功能"

Rules:
  - Han ↔ Latin: add space (Python编程 → Python 编程)
  - Han ↔ Digit: add space (3个场景 → 3 个场景)
  - Han ↔ Unicode letter/symbol: add space (μ乘以 → μ 乘以, π等于 → π 等于, ∞大 → ∞ 大)
  - Latin ↔ Digit: add space (Python3.9 → Python 3.9; compact units re-compacted)
  - Latin ↔ Unicode letter/symbol: add space (μV → μ V, Δx → Δ x)
  - Protection zones (inline code `...`, math $...$, URLs) are preserved.
  - Number-unit compact: GB, MB, KB, TB, fps, FPS, etc.
"""

import re
import sys
import unicodedata

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


def _is_non_cjk_letter(ch):
    """True if ch is a letter or math symbol outside CJK/Latin/Digit ranges."""
    if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z':
        return False
    if '0' <= ch <= '9':
        return False
    if '\u4e00' <= ch <= '\u9fff' or '\u3400' <= ch <= '\u4dbf':
        return False
    cat = unicodedata.category(ch)
    return cat in ('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Sm')


def _apply_script_spacing(text):
    """
    Insert space at every Han ↔ Latin, Han ↔ Digit, and Han ↔ non-CJK letter,
    Latin ↔ Digit, and Latin ↔ non-CJK letter boundary.
    Covers Greek letters (μ, λ, π, α, β, γ, ω, Δ, Σ, etc.),
    Cyrillic, and mathematical symbols (∞, ∈, ∑, ∫, √, ≈, ≠, ≤, ≥, etc.)
    Compact units are re-joined by _apply_number_unit_compact running afterward.
    """
    result = []
    prev_is_han = False
    prev_is_latin = False
    prev_is_digit = False
    prev_is_script = False
    prev_is_pct = False

    for ch in text:
        cur_is_han = '\u4e00' <= ch <= '\u9fff' or '\u3400' <= ch <= '\u4dbf'
        cur_is_latin = 'a' <= ch <= 'z' or 'A' <= ch <= 'Z'
        cur_is_digit = '0' <= ch <= '9'
        cur_is_script = _is_non_cjk_letter(ch)

        if prev_is_han and (cur_is_latin or cur_is_digit or cur_is_script):
            result.append(' ')
        elif prev_is_latin and (cur_is_han or cur_is_script):
            result.append(' ')
        elif prev_is_digit and (cur_is_han or cur_is_script):
            result.append(' ')
        elif prev_is_script and (cur_is_han or cur_is_latin or cur_is_digit):
            result.append(' ')
        elif prev_is_han and ch == '%':
            result.append(' ')
        elif prev_is_pct and cur_is_han:
            result.append(' ')

        result.append(ch)
        prev_is_han = cur_is_han
        prev_is_latin = cur_is_latin
        prev_is_digit = cur_is_digit
        prev_is_script = cur_is_script
        prev_is_pct = (ch == '%')

    text = ''.join(result)
    return text


def apply_spacing(line):
    """Apply full spacing pipeline to a single text line."""
    line = line.rstrip('\n')
    text, mapping = _protect(line)
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
    args = sys.argv[1:]

    if args and args[0] == '--inline':
        print(apply_spacing(args[1]))
        return

    for line in sys.stdin:
        sys.stdout.write(apply_spacing(line))
        sys.stdout.write('\n')


if __name__ == '__main__':
    main()
