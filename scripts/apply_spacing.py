"""
Deterministic CJK-Latin spacing for mixed-language text.

Applies script boundary spacing (Han-Latin, Han-Digit, Latin-Digit)
and number-unit compact formatting per the srt-enhancer mixed-typesetting spec.

Usage:
  python apply_spacing.py < input.txt > output.txt
  python apply_spacing.py --inline "Python3.9新功能"

Rules:
  - Han ↔ Latin: add space (Python编程 → Python 编程)
  - Han ↔ Digit: add space (3个场景 → 3 个场景)
  - Latin ↔ Digit: preserved compact (2K, 3A, Python3.9 unchanged)
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
    Insert space at every Han ↔ Latin and Han ↔ Digit boundary.
    Latin ↔ Digit boundary: add space (compact units are re-joined
    by _apply_number_unit_compact running afterward).
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

        result.append(ch)
        prev_is_han = cur_is_han
        prev_is_latin = cur_is_latin
        prev_is_digit = cur_is_digit

    return ''.join(result)


def apply_spacing(line):
    """Apply full spacing pipeline to a single text line."""
    line = line.rstrip('\n')
    text, mapping = _protect(line)
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
