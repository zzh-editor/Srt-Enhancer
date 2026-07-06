#!/usr/bin/env python3
"""
Deterministic SRT enhancement pipeline.

All steps are rule-based and configurable via CLI flags + JSON config.
AI is NOT involved during execution — it prepares the config upfront.

Usage:
    python3 scripts/enhance.py input.srt -o output.srt \\
        --lang zh --domain maya \\
        --config my_overrides.json

Steps (applied in order, all optional):
  1. parse        Parse SRT into internal format
  2. normalize    Text normalization: defiller(去口癖) → de_de(的得地) → ratio_format(16比9→16:9)
  3. terminology  ASR term replacement (from correction-table.md + overrides)
  4. spacing      CJK-Latin spacing (inlined, no subprocess)
   5. finalize     depunct(去标点) → hotkeys(Ctrl+E 标准化), kept last to avoid + stripping
  7. write        Write output SRT
"""

import argparse
import collections
import importlib.util
import json
import os
import re
import sys
from pathlib import Path
from apply_spacing import apply_spacing as _apply_spacing

# ── Paths ──────────────────────────────────────────────────────────

SKILL_DIR = Path(__file__).resolve().parent.parent
REFERENCES_DIR = SKILL_DIR / "references"
TERMINOLOGY_PATH = REFERENCES_DIR / "correction-table.md"


# ── Config defaults ────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "lang": "zh",
    "domain": None,          # auto-detect, or "maya" / "python" / "gaming" / "ai-3d" / "substance" / "blender" / "unreal" / "houdini" / "zbrush" / "photoshop"
    "match_mode": "auto",    # "exact" | "auto" (exact → casefold → normalized)
    "filler_words": [
        "啊", "哦", "嗯", "呃", "哎", "噢", "唔", "欸", "嘿",
        "嘛", "吧", "呢", "啦", "哈", "哟", "喔",
    ],
    "discourse_markers": [
        "也就是说", "说白了", "这边的话", "对吧", "好吧",
        "然后", "那么", "所以", "但是", "不过",
    ],
    "de_de_enabled": True,
    "terminology_enabled": True,
    "ratio_format_enabled": True,
    "spacing_enabled": True,
    "capitalization_enabled": True,
    "depunct_enabled": True,
    "singleline_enabled": True,
    "singleline_max_chars": 40,
    "terminology_overrides": {},   # {asr_text: correct_text}
    "capitalization_overrides": {}, # {lowercase: StandardCasing}
    "punctuation_preserve": ["《》", "`", "$"],
    "dot_preserve": True,          # preserve . in file names/versions
}


# ── SRT I/O ────────────────────────────────────────────────────────

def parse_srt(path: str) -> list[dict]:
    segments: list[dict] = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.isdigit():
            idx = int(line)
            i += 1
            if i >= len(lines):
                break
            ts = lines[i].strip()
            i += 1
            text_lines = []
            while i < len(lines) and lines[i].strip():
                text_lines.append(lines[i].strip())
                i += 1
            text = " ".join(text_lines)
            m = re.match(
                r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*"
                r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})",
                ts,
            )
            if m:
                start = (int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])
                         + int(m[4]) / 1000)
                end = (int(m[5]) * 3600 + int(m[6]) * 60 + int(m[7])
                       + int(m[8]) / 1000)
                segments.append({
                    "idx": idx,
                    "start": start,
                    "end": end,
                    "text": text,
                })
            i += 1
        else:
            i += 1
    return segments


def write_srt(segments: list[dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = seg["start"]
            end = seg["end"]
            sh = int(start // 3600)
            sm = int((start % 3600) // 60)
            ss = int(start % 60)
            sms = int((start - int(start)) * 1000)
            eh = int(end // 3600)
            em = int((end % 3600) // 60)
            es = int(end % 60)
            ems = int((end - int(end)) * 1000)
            f.write(f"{i}\n")
            f.write(f"{sh:02d}:{sm:02d}:{ss:02d},{sms:03d} --> "
                    f"{eh:02d}:{em:02d}:{es:02d},{ems:03d}\n")
            f.write(f"{seg['text']}\n\n")


# ── Terminology loader ─────────────────────────────────────────────

def load_terminology(path: Path = TERMINOLOGY_PATH) -> dict[str, str]:
    """Load ASR → correct mappings from correction-table.md Markdown table."""
    mapping: dict[str, str] = {}
    if not path.exists():
        return mapping

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse Markdown tables: | ASR | correct | ... |
    table_pattern = re.compile(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|", re.MULTILINE)
    skip_correct_markers = ["正确", "✅", "无需修正"]
    for match in table_pattern.finditer(content):
        asr = match.group(1).strip()
        correct = match.group(2).strip()
        if not asr or not correct:
            continue
        asr_lower = asr.lower()
        correct_lower = correct.lower()
        if asr_lower == correct_lower:
            continue
        if any(m in correct for m in skip_correct_markers):
            continue
        if "ASR 误识别" in asr:
            continue
        mapping[asr] = correct

    return mapping


# ── ASR stutter fix ────────────────────────────────────────────────

STUTTER_PATTERN = re.compile(
    r'([\u4e00-\u9fff\u3400-\u4dbf])\1{2,}'    # 这这这, 那那那
)
STUTTER_WORD_PATTERN = re.compile(
    r'\b([A-Za-z]+)(\s+\1\b){2,}',              # no no no, yes yes yes
    re.IGNORECASE,
)
STUTTER_CJK_WORD_PATTERN = re.compile(
    r'([\u4e00-\u9fff])(?:\s*\1){2,}'           # 不 不 不, 对 对 对
)


def _fix_stutter(text: str) -> str:
    """Collapse stuttered/repeated characters and words."""
    text = STUTTER_PATTERN.sub(r'\1', text)
    text = STUTTER_WORD_PATTERN.sub(r'\1', text)
    text = STUTTER_CJK_WORD_PATTERN.sub(r'\1', text)
    return text


# ── Capitalization loader ──────────────────────────────────────────

def load_capitalization_table(path: Path = TERMINOLOGY_PATH) -> tuple[dict[str, str], dict[str, dict[str, str]]]:
    """Load proper noun capitalization + case groups from correction-table.md '大小写校准' section.

    Returns (cap_map, case_groups) where:
      cap_map: lowercase → standard casing (generic, domain-independent)
      case_groups: group_name → {lowercase → standard_casing} (domain-sensitive)
    """
    cap_map: dict[str, str] = {}
    case_groups: dict[str, dict[str, str]] = {}
    if not path.exists():
        return cap_map, case_groups

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_section: str | None = None
    current_subsection: str | None = None
    in_cap_section = False
    table_pattern = re.compile(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|")

    for line in lines:
        stripped = line.strip()
        # Detect sections
        if stripped.startswith("## 大小写校准"):
            in_cap_section = True
            continue
        if in_cap_section and stripped.startswith("## "):
            in_cap_section = False
            continue
        if not in_cap_section:
            continue

        # Subsections: ### 专有名词大写 / ### 领域感知大小写组
        if stripped.startswith("### "):
            current_subsection = stripped[4:].strip()
            continue

        # Skip header rows
        if "---" in stripped or stripped.startswith("| 小写"):
            continue
        if not stripped.startswith("|"):
            continue

        m = table_pattern.match(stripped)
        if not m:
            continue

        if current_subsection and "专有名词" in current_subsection:
            low = m.group(1).strip()
            std = m.group(2).strip()
            if low and std:
                cap_map[low] = std
        elif current_subsection and "领域" in current_subsection:
            low = m.group(1).strip()
            std = m.group(2).strip()
            group_name = m.group(3).strip() if len(m.groups()) >= 3 else "generic"
            if low and std:
                case_groups.setdefault(group_name, {})[low] = std

    # Generate Ctrl shortcut variants
    for key_char in ('v', 'c', 'z', 's', 'a', 'x', 'p'):
        upper = key_char.upper()
        for variant in (f'ctrl+{key_char}', f'ctrl {key_char}', f'ctrl{key_char}'):
            cap_map[variant] = f'Ctrl+{upper}'

    return cap_map, case_groups


# ── Step: de-filler ────────────────────────────────────────────────

def _contains_any(text: str, words: list[str]) -> str | None:
    for w in words:
        if w in text:
            return w
    return None


def _is_discourse_marker(text: str, markers: list[str]) -> bool:
    for m in markers:
        if m in text:
            return True
    return False


def step_defiller(segments: list[dict], config: dict) -> list[dict]:
    fillers = config["filler_words"]
    markers = config["discourse_markers"]

    for seg in segments:
        text = seg["text"]
        original = text

        # ASR stutter: collapse repeated chars/words
        text = _fix_stutter(text)

        # Remove hesitation sounds at start
        for f in fillers:
            while text.startswith(f):
                text = text[len(f):].lstrip()
            # Remove hesitation surrounded by spaces
            pattern = re.compile(r"\s+" + re.escape(f) + r"\s+")
            text = pattern.sub(" ", text)

        # Remove sentence-final particles (when standalone at end)
        for f in ["嘛", "吧", "呢", "啦", "哈", "哟", "喔"]:
            if text.endswith(f) and len(text) > len(f):
                prev_char = text[-len(f) - 1]
                if prev_char in "，。！？；":
                    text = text[:-len(f)].rstrip()

        # Don't remove discourse markers — they're valid connectors
        if text != original and _is_discourse_marker(text, markers):
            text = original

        # Clean up double spaces
        text = re.sub(r" {2,}", " ", text).strip()
        seg["text"] = text

    return segments


# ── Step: 的/得/地 correction ──────────────────────────────────────

DE_DE_PATTERNS = [
    # Fixed compounds (always keep 得)
    (r"\b变得", "变得"),
    (r"\b懂得", "懂得"),
    (r"\b觉得", "觉得"),
    (r"\b记得", "记得"),
    (r"\b显得", "显得"),
    (r"\b值得", "值得"),
    (r"\b免得", "免得"),
    (r"\b取得", "取得"),
    (r"\b获得", "获得"),
    (r"\b认得", "认得"),
    # R1: V+的+比较/越来越/有点/有些/更+Adj → V+得+...
    #   仅限常见动词（单字或双字），避免误改"具体的比较"这类形+名结构
    (r"(["
     r"\u7528\u505a\u8bf4\u770b\u5b66\u6559\u7ec3\u5e72"  # 用做说看学教练干
     r"\u8dd1\u5403\u559d\u73a9\u5199\u753b\u5531\u6253"  # 跑吃喝玩写画唱打
     r"\u8d70\u98de\u6e38\u8bfb\u8bb2\u6f14\u4f4f\u7761"  # 走飞游读讲演住睡
     r"\u7ad9\u5750\u653e\u62ff\u7ed9\u6539\u4fee\u7ba1"  # 站坐放拿给改修管
     r"\u7b49\u627e\u6362\u9009\u529e\u7b97\u4e70\u5356"  # 等找换选办算买卖
     r"\u517b\u79cd\u9020\u5efa\u5f00\u5173\u505c\u641e"  # 养种建造开关停搞
     r"\u5f04\u6574\u62c9\u63a8\u63d0\u4e3e\u80cc\u5e26"  # 弄整拉推提举背带
     r"\u6293\u8d34\u6302\u6446\u88c5\u6309\u538b\u6d82"  # 抓贴挂摆装按压缩涂
     r"\u64e6\u6d17\u5237\u751f\u957f\u53d1\u53d8\u6765"  # 擦洗刷生长发变来
     r"\u53bb\u5012\u60f3\u7b54\u95ee\u8003\u8bd5\u8bc4"  # 去倒想问考试评
     r"]{1,2})的"
     r"(比较|越来越|有点|有些|更|更加|更为|越发|十分|极其)",
     r"\1得\2"),
    # R2: V+的+要命/不行/够呛/不得了/很+单字Adj → V+得+...
    (r"(["
     r"\u7528\u505a\u8bf4\u770b\u5b66\u6559\u7ec3\u5e72"
     r"\u8dd1\u5403\u559d\u73a9\u5199\u753b\u5531\u6253"
     r"\u8d70\u98de\u6e38\u8bfb\u8bb2\u6f14\u4f4f\u7761"
     r"\u7ad9\u5750\u653e\u62ff\u7ed9\u6539\u4fee\u7ba1"
     r"\u7b49\u627e\u6362\u9009\u529e\u7b97\u4e70\u5356"
     r"\u517b\u79cd\u9020\u5efa\u5f00\u5173\u505c\u641e"
     r"\u5f04\u6574\u62c9\u63a8\u63d0\u4e3e\u80cc\u5e26"
     r"\u6293\u8d34\u6302\u6446\u88c5\u6309\u538b\u6d82"
     r"\u64e6\u6d17\u5237\u751f\u957f\u53d1\u53d8\u6765"
     r"\u53bb\u5012\u60f3\u7b54\u95ee\u8003\u8bd5\u8bc4"
     r"]+)的"
     r"(要命|不行|够呛|不得了|很[好快多慢对错早晚久长短大小高矮宽厚深浅轻重难易])",
     r"\1得\2"),
    # R3: 常见副词+的+去/来/做/进行/给予/予以/加以 → 地
    (r"(更好|慢慢|快速|认真|反复|不断|持续|自动|逐渐|逐步|陆续|相继|"
     r"悄悄|默默|故意|特意|拼命|使劲|大力|全力|狠狠|轻轻|稍稍|"
     r"随便|随意|任意|强行|干脆|一直|不停|直接|间接|"
     r"主动|被动|积极|消极|共同|一起|统一|单独|独立)的"
     r"(?=去|来|做|进行|给予|予以|加以|做出|做出|开展|实施|说|讲|谈|"
     r"写|画|看|听|用|玩|学|教|练|处理|解决|完成|安排|准备|考虑|"
     r"讨论|研究|分析|比较|选择|决定|使用|利用|应用|回答|解释|"
     r"介绍|说明|表达|描述|演示|操作|制作|创造|创建|开发|设计|执行)",
     r"\1地"),
]


def step_de_de(segments: list[dict], config: dict) -> list[dict]:
    for seg in segments:
        text = seg["text"]
        for pattern, replacement in DE_DE_PATTERNS:
            text = re.sub(pattern, replacement, text)
        seg["text"] = text
    return segments


# ── Step: ratio format (16比9 → 16:9) ────────────────────────────

RATIO_PATTERN = re.compile(
    r'(?<!这|比|百|占|对|无|可|相|类|综|总|合|加|减|乘|除)'
    r'(\d+)\s*比\s*(\d+)'
    r'(?!例|分|重|赛|武|试|拼|项|类|量|较|喻|如|方|例|准)'
)


def step_ratio_format(segments: list[dict], config: dict) -> list[dict]:
    for seg in segments:
        seg["text"] = RATIO_PATTERN.sub(r'\1:\2', seg["text"])
    return segments


# ── Fuzzy matching helper ─────────────────────────────────────────

def _try_replace(text: str, asr_text: str, correct_text: str,
                 mode: str = "auto") -> str | None:
    """If asr_text matches text at given fuzziness, return corrected text.

    Priority: exact substring → case-insensitive → normalized.
    Returns None if no match.
    """
    # Level 1: exact
    if asr_text in text:
        return text.replace(asr_text, correct_text)

    if mode == "exact":
        return None

    # Level 2: case-insensitive
    pattern = re.compile(re.escape(asr_text), re.IGNORECASE)
    if pattern.search(text):
        return pattern.sub(correct_text, text)

    # Level 3: normalized — multi-word or CamelCase split
    def _norm(s: str) -> str:
        return re.sub(r'[\s\-_.,;:/]', '', s).lower()

    text_norm = _norm(text)
    asr_norm = _norm(asr_text)
    if asr_norm in text_norm:
        # Tokenize: space split then CamelCase split per word
        raw_tokens = asr_text.split()
        tokens: list[str] = []
        for t in raw_tokens:
            parts = re.findall(r'[A-Z]?[a-z]+|[A-Z]+|[0-9]+', t)
            tokens.extend(parts if parts else [t])
        if len(tokens) > 1:
            flexible = re.compile(
                r'\s*'.join(re.escape(t) for t in tokens), re.IGNORECASE
            )
            return flexible.sub(correct_text, text)

    return None


# ── Step: terminology replacement ──────────────────────────────────

def step_terminology(segments: list[dict], config: dict) -> list[dict]:
    mapping = load_terminology()
    mapping.update(config.get("terminology_overrides", {}))

    if not mapping:
        return segments

    match_mode = config.get("match_mode", "auto")
    sorted_terms = sorted(mapping.items(), key=lambda x: -len(x[0]))

    for seg in segments:
        text = seg["text"]
        for asr_text, correct_text in sorted_terms:
            if asr_text.lower() == correct_text.lower():
                continue
            result = _try_replace(text, asr_text, correct_text, match_mode)
            if result is not None:
                text = result
        seg["text"] = text

    return segments


# ── Step: spacing ──────────────────────────────────────────────────

def step_spacing(segments: list[dict], config: dict) -> list[dict]:
    try:
        from apply_spacing import apply_spacing as _do_spacing
    except ImportError:
        print("warning: apply_spacing module not found, skipping spacing",
              file=sys.stderr)
        return segments
    for seg in segments:
        seg["text"] = _do_spacing(seg["text"])
    return segments


# ── Step: capitalization ───────────────────────────────────────────

DOMAIN_CASE_GROUPS_MAP: dict[str, list[str]] = {
    "general": ["generic_acronym", "os_term", "brand_tool", "file_format"],
    "ai-3d": ["generic_acronym", "os_term", "brand_tool", "ai_3d", "file_format"],
    "maya": ["generic_acronym", "os_term", "brand_tool", "ai_3d", "file_format"],
    "python": ["generic_acronym", "os_term", "file_format"],
    "gaming": ["generic_acronym", "os_term", "brand_tool", "file_format"],
}
DEFAULT_CASE_GROUPS = ["generic_acronym", "os_term", "file_format"]


def step_capitalization(segments: list[dict], config: dict) -> list[dict]:
    """Apply proper noun capitalization and domain-aware case normalization.

    Loads from correction-table.md '大小写校准' section + AI overrides.
    """
    cap_map, case_groups = load_capitalization_table()

    overrides = config.get("capitalization_overrides", {})
    cap_map.update(overrides)

    domain = config.get("domain")
    group_names = DOMAIN_CASE_GROUPS_MAP.get(domain, DEFAULT_CASE_GROUPS) if domain else DEFAULT_CASE_GROUPS

    combined: dict[str, str] = {}
    # cap_map has highest priority (don't overwrite)
    for k, v in cap_map.items():
        combined[k] = v
    # Then case groups (lower priority)
    for name in group_names:
        group = case_groups.get(name, {})
        for k, v in group.items():
            if k not in combined:
                combined[k] = v

    if not combined:
        return segments

    sorted_terms = sorted(combined, key=len, reverse=True)
    pattern = re.compile(
        '|'.join(r'\b' + re.escape(t) + r'\b' for t in sorted_terms),
        re.IGNORECASE | re.ASCII,
    )

    for seg in segments:
        seg["text"] = pattern.sub(lambda m: combined[m.group(0).lower()], seg["text"])

    return segments


# ── Step: punctuation removal ──────────────────────────────────────

def step_depunct(segments: list[dict], config: dict) -> list[dict]:
    preserve = config.get("punctuation_preserve", ["《》", "`", "$"])
    preserve_chars: set[str] = set()
    for p in preserve:
        preserve_chars.update(p)

    punct_re = re.compile(
        "["
        "\u3000-\u303f"    # CJK punctuation
        "\uff00-\uffef"    # Fullwidth
        "\\!\"#\\$%&'()*+,\\-./:;<=>?@\\[\\\\\\]^_`\\{|\\}~"  # ASCII
        "]+"
    )

    dot_re = re.compile(r"(?<!\d)\.(?!\d|com|net|org|edu|cn|io|ai|app|dev)")
    colon_re = re.compile(r"(?<!\d):(?!\d)")

    for seg in segments:
        text = seg["text"]
        if not text:
            continue

        # Protect zones: replace with placeholders
        protected: list[tuple[str, str]] = []

        # Protect 数字:数字 patterns (16:9, 4:3, etc.)
        COLON_PH = "PROTECTCOLON"
        text = re.sub(r'(\d):(\d)', rf'\1{COLON_PH}\2', text)

        # Protect 数字.数字 patterns (3.9, 5.0, etc.)
        if config.get("dot_preserve", True):
            DOT_PH = "PROTECTDOT"
            text = re.sub(r'(\d)\.(\d)', rf'\1{DOT_PH}\2', text)

        # Protect 数字% patterns (90%, 50%, etc.)
        PCT_PH = "PROTECTPCT"
        text = re.sub(r'(\d)%', rf'\1{PCT_PH}', text)

        for i, p in enumerate(preserve):
            if len(p) == 2:  # paired like 《》
                placeholder = f"\x00PROTECT_PAIR_{i}\x00"
                pattern = re.escape(p[0]) + r".*?" + re.escape(p[1])
                protected.append((placeholder, p))
                text = re.sub(pattern, lambda m, ph=placeholder: ph, text)
            elif p == "`":
                # Inline code
                placeholder = f"\x00PROTECT_CODE_{i}\x00"
                text = re.sub(r"`[^`]+`", lambda m, ph=placeholder: ph, text)

        # Replace punctuation with space (mid-line) or delete (trailing)
        text = punct_re.sub(" ", text)
        if config.get("dot_preserve", True):
            text = dot_re.sub(" ", text)
        text = re.sub(r'[ \t]+', ' ', text)

        # Fix CJK-Latin boundaries exposed by punctuation removal
        text = re.sub(
            r'([\u4e00-\u9fff\u3400-\u4dbf])([A-Za-z])',
            r'\1 \2', text
        )
        text = re.sub(
            r'([A-Za-z])([\u4e00-\u9fff\u3400-\u4dbf])',
            r'\1 \2', text
        )

        # Restore protected zones
        text = text.replace("PROTECTCOLON", ":")
        text = text.replace("PROTECTDOT", ".")
        text = text.replace("PROTECTPCT", "%")
        for placeholder, orig in protected:
            if len(orig) == 2:
                pattern_ph = re.escape(placeholder)
                # Remove punctuation inside protection too
                text = re.sub(pattern_ph, orig, text)
            elif orig == "`":
                text = text.replace(placeholder, "`code`")

        seg["text"] = text.strip()

    return segments


# ── Step: hotkey normalization ──────────────────────────────────────

HOTKEY_PATTERNS = [
    (r'\b[Cc]trl[\s+\-]?[Ee]\b', 'Ctrl+E'),
    (r'\b[Cc]trl[\s+\-]?[Cc]\b', 'Ctrl+C'),
    (r'\b[Cc]trl[\s+\-]?[Vv]\b', 'Ctrl+V'),
    (r'\b[Cc]trl[\s+\-]?[Zz]\b', 'Ctrl+Z'),
    (r'\b[Cc]trl[\s+\-]?[Ss]\b', 'Ctrl+S'),
    (r'\b[Cc]trl[\s+\-]?[Dd]\b', 'Ctrl+D'),
    (r'\b[Cc]ontrol\s*[Dd]\b', 'Ctrl+D'),
    (r'\b[Cc]ommand[\s+\-]?[Zz]\b', 'Command+Z'),
    (r'\b[Cc]ommand[\s+\-]?[Cc]\b', 'Command+C'),
    (r'\b[Cc]ommand[\s+\-]?[Vv]\b', 'Command+V'),
    (r'\b[Cc]ommand[\s+\-]?[Ss]\b', 'Command+S'),
]


def step_hotkeys(segments: list[dict], config: dict) -> list[dict]:
    for seg in segments:
        text = seg["text"]
        for pattern, replacement in HOTKEY_PATTERNS:
            text = re.sub(pattern, replacement, text)
        seg["text"] = text
    return segments


# ── Step: semantic segment refinement ──────────────────────────────




# ── Pipeline ───────────────────────────────────────────────────────

# Legacy single-step names (defiller, de_de, etc.) still work via --steps

def step_normalize(segments: list[dict], config: dict) -> list[dict]:
    segments = step_defiller(segments, config)
    segments = step_de_de(segments, config)
    segments = step_ratio_format(segments, config)
    return segments


def step_finalize(segments: list[dict], config: dict) -> list[dict]:
    segments = step_depunct(segments, config)
    segments = step_hotkeys(segments, config)
    return segments


PIPELINE_STEPS = {
    "normalize": step_normalize,
    "terminology": step_terminology,
    "spacing": step_spacing,
    "capitalization": step_capitalization,
    "finalize": step_finalize,
    "defiller": step_defiller,
    "de_de": step_de_de,
    "ratio_format": step_ratio_format,
    "depunct": step_depunct,
    "hotkeys": step_hotkeys,
}


def run_pipeline(segments: list[dict], config: dict,
                 enabled_steps: list[str]) -> list[dict]:
    for step_name in enabled_steps:
        if step_name in PIPELINE_STEPS:
            segs = PIPELINE_STEPS[step_name](segments, config)
            n = len(segments)
            if n != len(segs):
                print(f"step '{step_name}': {n} → {len(segs)} segments",
                      file=sys.stderr)
            segments = segs
        else:
            print(f"warning: unknown step '{step_name}', skipping",
                  file=sys.stderr)
    return segments


# ── Casing consistency check ────────────────────────────────────────

ENGLISH_TOKEN = re.compile(r'\b[A-Za-z][A-Za-z0-9]*\b')


def check_casing(segments: list[dict]) -> None:
    """Scan all SRT text for inconsistent English term casing.

    Groups by lowercase form, reports terms with 2+ different casings.
    """
    cap_map, case_groups = load_capitalization_table()

    # Collect all tokens
    variants: dict[str, set[str]] = collections.defaultdict(set)
    for seg in segments:
        for m in ENGLISH_TOKEN.finditer(seg["text"]):
            token = m.group(0)
            if len(token) <= 1:
                continue
            variants[token.lower()].add(token)

    # Build known casing from cap_map + case_groups
    known: dict[str, str] = {}
    for k, v in cap_map.items():
        known[k.lower()] = v
    for group in case_groups.values():
        for k, v in group.items():
            if k not in known:
                known[k] = v

    # Report
    n_issues = 0
    for key in sorted(variants):
        hits = variants[key]
        if len(hits) <= 1:
            continue
        n_issues += 1
        std = known.get(key)
        std_hint = f" → 建议: {std}" if std else ""
        hit_list = ', '.join(sorted(hits))
        print(f"  {hit_list}{std_hint}")

    if n_issues == 0:
        print("  (all consistent — no terms with mixed casing)")
    else:
        print(f"\n  {n_issues} term(s) with inconsistent casing above")

    # Also report known terms that were never found
    n_miss = 0
    for key, std in sorted(known.items()):
        if key not in variants:
            pass  # silent — too noisy
    if n_miss:
        print(f"  {n_miss} known term(s) not found in output")


# ── CLI ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Deterministic SRT enhancement pipeline"
    )
    parser.add_argument("input", help="input SRT file")
    parser.add_argument("-o", "--output", default=None, help="output SRT path")
    parser.add_argument("--match-mode", default="auto",
                        help="term match mode: exact / auto / normalized")
    parser.add_argument("--config", "-c", default=None,
                        help="JSON config file with overrides")
    parser.add_argument("--lang", default="zh",
                        help="language code (zh/en/ja/ko)")
    parser.add_argument("--domain", default=None,
                        help="domain: maya/python/gaming/ai-3d/substance/blender/unreal/houdini/zbrush/photoshop/general")
    parser.add_argument("--steps", default="normalize,terminology,spacing,capitalization,terminology,finalize",
                        help="comma-separated pipeline steps to run")
    parser.add_argument("--skip", default=None,
                        help="comma-separated steps to skip")
    parser.add_argument("--overrides", default=None,
                        help="JSON string for terminology_overrides")
    parser.add_argument("--dry-run", action="store_true",
                        help="parse and print steps without executing")
    parser.add_argument("--check-casing", action="store_true",
                        help="scan output for inconsistent English term casing")

    args = parser.parse_args()

    # Build config from defaults + JSON file + CLI overrides
    config = dict(DEFAULT_CONFIG)
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            file_config = json.load(f)
            config.update(file_config)
    if args.lang:
        config["lang"] = args.lang
    if args.match_mode:
        config["match_mode"] = args.match_mode
    if args.domain:
        config["domain"] = args.domain
    if args.overrides:
        config["terminology_overrides"] = json.loads(args.overrides)

    # Determine enabled steps
    enabled = [s.strip() for s in args.steps.split(",") if s.strip()]
    if args.skip:
        skipped = set(s.strip() for s in args.skip.split(","))
        enabled = [s for s in enabled if s not in skipped]

    # Parse input
    segments = parse_srt(args.input)
    if not segments:
        print(f"error: no valid segments in {args.input}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(f"input: {args.input}", file=sys.stderr)
        print(f"segments: {len(segments)}", file=sys.stderr)
        print(f"steps: {', '.join(enabled)}", file=sys.stderr)
        print(f"config: {json.dumps(config, indent=2, ensure_ascii=False)}",
              file=sys.stderr)
        return

    print(f"pipeline: {', '.join(enabled)} on {len(segments)} segments",
          file=sys.stderr)

    out = run_pipeline(segments, config, enabled)

    if args.check_casing:
        print("casing consistency check:", file=sys.stderr)
        check_casing(out)
        return

    output_path = args.output or args.input.replace(".srt", "_Enhancer.srt")
    if output_path == args.input:
        output_path = args.input.replace(".srt", "_Enhancer.srt")

    write_srt(out, output_path)
    print(f"done! {len(segments)} → {len(out)} segments → {output_path}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
