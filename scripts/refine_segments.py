#!/usr/bin/env python3
"""
Refine SRT segments using multi-level cascading semantic split rules.

Pipeline:
  1. For each segment, find candidate split positions across 6 confidence levels
  2. Recursively split at balanced positions, proportionally allocate time
  3. Merge back very short fragments (< 3 chars) unless protected response words

Usage:
    python3 scripts/refine_segments.py <input.srt> [output.srt]
"""

import argparse
import re
import sys
from pathlib import Path

# ── Constants ────────────────────────────────────────────────────────

SENTENCE_END_PUNCT = frozenset(".?!。？！…")

STRONG_CONJUNCTIONS = [
    "但是", "但", "所以", "不过", "然而", "可是", "因此", "因而",
]

DISCOURSE_MARKERS = [
    "首先", "其次", "然后", "接着",
    "另外", "还有", "此外", "同样",
    "比如说", "举个例子", "比方说",
]

TEMP_MARKERS = [
    "等你", "等到", "当你", "到时候", "有时候", "接下来",
]

TIME_WORDS = ["今天", "现在", "目前"]

TOPIC_NA_BLOCK_PREFIX = frozenset(
    "是有的了在和跟与到从把被让给为对向于"
)

TOPIC_NA_BLOCK_SUFFIX = frozenset(
    "个些种时天年月点次级位名里边儿本条张"
)

PROTECTED_WORDS = frozenset({
    "好", "对", "嗯", "是", "不", "行", "哦", "啊", "呀", "喏", "嗯哼",
    "好的", "对的", "明白", "知道", "可以", "没错", "是的", "不行",
    "好吧", "对了", "对哦", "对啊", "嗯嗯", "好啦", "行了", "可以啊",
    "没问题", "没事", "知道了", "明白了", "没关系",
    "ok", "okay", "okay", "yes", "no", "right", "sure", "yeah", "yep",
    "nope", "nah", "alright", "indeed",
})


# ── SRT I/O ─────────────────────────────────────────────────────────

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


# ── Helpers ─────────────────────────────────────────────────────────

def _strip_punct(text: str) -> str:
    return text.strip().lower().rstrip(",.?!。？！，、；:\"'").strip()


def _is_protected(text: str) -> bool:
    return _strip_punct(text) in PROTECTED_WORDS


def _has_sentence_end(text: str) -> bool:
    return any(c in SENTENCE_END_PUNCT for c in text[-3:])


# ── Split point detection ───────────────────────────────────────────

def _is_topic_shift_na(text: str, pos: int) -> bool:
    """Check if \\u90a3 (那) at pos is a topic shift (not a determiner)."""
    if pos <= 0 or pos >= len(text) - 1:
        return False

    if pos > 0 and text[pos - 1] in TOPIC_NA_BLOCK_PREFIX:
        return False

    if pos >= 2:
        prev2 = text[pos - 2:pos]
        if prev2 in ("就是", "这是", "那是", "可是", "而是", "但是", "还是", "或是"):
            return False

    nxt = text[pos + 1] if pos + 1 < len(text) else ""
    if nxt in TOPIC_NA_BLOCK_SUFFIX:
        return False
    nxt2 = text[pos + 1:pos + 3]
    if nxt2 in ("就是", "还是", "也是", "算是", "的话", "这么", "那么"):
        return False

    return True


def _is_split_viable(text: str, pos: int) -> bool:
    if pos < 2 or pos >= len(text) - 2:
        return False
    if text[pos - 1] in SENTENCE_END_PUNCT:
        return False
    return True





def _find_split_points(text: str) -> tuple[list[int], list[int]]:
    """Return (strong_split_positions, all_split_positions) sorted."""
    strong = set()
    all_pts = set()

    if not text:
        return [], []

    n = len(text)

    # Level 1: Sentence-ending punctuation (STRONG)
    for i, c in enumerate(text):
        if c in SENTENCE_END_PUNCT:
            p = i + 1
            if p < n:
                strong.add(p)
                all_pts.add(p)

    # Level 2: Strong conjunctions mid-text (STRONG)
    for conj in STRONG_CONJUNCTIONS:
        idx = text.find(conj, 1)
        while idx > 0:
            if _is_split_viable(text, idx):
                strong.add(idx)
                all_pts.add(idx)
            idx = text.find(conj, idx + 1)

    # Level 3: Topic shift 那 (STRONG, with context check)
    idx = text.find("那", 1)
    while idx > 0:
        if _is_split_viable(text, idx) and _is_topic_shift_na(text, idx):
            strong.add(idx)
            all_pts.add(idx)
        idx = text.find("那", idx + 1)

    # Level 4: Discourse markers (STRONG)
    for marker in DISCOURSE_MARKERS:
        idx = text.find(marker, 1)
        while idx > 0:
            if _is_split_viable(text, idx):
                strong.add(idx)
                all_pts.add(idx)
            idx = text.find(marker, idx + 1)

    # Level 5: Temporal markers (STRONG)
    for marker in TEMP_MARKERS:
        idx = text.find(marker, 1)
        while idx > 0:
            if _is_split_viable(text, idx):
                strong.add(idx)
                all_pts.add(idx)
            idx = text.find(marker, idx + 1)

    # Level 6: Time words mid-text (MEDIUM)
    for marker in TIME_WORDS:
        idx = text.find(marker, 1)
        while idx > 0:
            if _is_split_viable(text, idx):
                all_pts.add(idx)
            idx = text.find(marker, idx + 1)

    # Level 7: OK isolation (MEDIUM)
    for ok_word in ("OK", "ok", "Okay", "Ok"):
        idx = text.find(ok_word)
        while idx >= 0:
            ok_end = idx + len(ok_word)
            right = text[ok_end:ok_end + 1]
            if ok_end <= n and (ok_end >= n or right in "，。？！\n "):
                if ok_end < n:
                    all_pts.add(ok_end)
                elif idx > 2:
                    all_pts.add(idx)
            idx = text.find(ok_word, idx + 1)

    min_left = 2
    min_right = 2  # allow short right chunks (protected words like OK)
    strong_sorted = sorted(p for p in strong if min_left <= p <= n - min_right)
    all_sorted = sorted(p for p in all_pts if min_left <= p <= n - min_right)

    return strong_sorted, all_sorted


# ── Recursive splitting ─────────────────────────────────────────────

def _split_recursive(seg: dict, max_chars: int) -> list[dict]:
    """Recursively split segment at the best balanced split point."""
    text = seg["text"].strip()
    if not text:
        return [seg]

    text_len = len(text)
    strong_pts, all_pts = _find_split_points(text)

    should_split = False
    if text_len >= max_chars and all_pts:
        should_split = True
    elif text_len < max_chars and strong_pts:
        should_split = True

    if not should_split:
        return [seg]

    candidates = list(strong_pts) if text_len < max_chars else list(all_pts)
    if not candidates:
        return [seg]

    viable = []
    for p in candidates:
        right_text = text[p:].strip()
        left_text = text[:p].strip()
        left_ok = len(left_text) >= 2
        right_ok = len(right_text) >= 3 or _is_protected(right_text)
        if left_ok and right_ok:
            viable.append(p)

    if not viable:
        return [seg]

    mid = text_len // 2
    best = min(viable, key=lambda p: abs(p - mid))

    left_text = text[:best].strip()
    right_text = text[best:].strip()
    if not left_text or not right_text:
        return [seg]

    ratio = len(left_text) / text_len if text_len > 0 else 0.5
    duration = seg["end"] - seg["start"]
    split_time = seg["start"] + duration * ratio

    left_seg = {"text": left_text, "start": seg["start"], "end": split_time}
    right_seg = {"text": right_text, "start": split_time, "end": seg["end"]}

    result = []
    result.extend(_split_recursive(left_seg, max_chars))
    result.extend(_split_recursive(right_seg, max_chars))
    return result


# ── Merging ──────────────────────────────────────────────────────────

def _merge_short_fragments(segments: list[dict]) -> list[dict]:
    """Merge very short fragments into the previous segment."""
    if not segments:
        return []

    result = [segments[0]]
    for seg in segments[1:]:
        text = seg["text"].strip()
        prev = result[-1]

        if len(text) <= 3 and not _is_protected(text):
            sep = "" if text[0] in "，、。？！" else ""
            prev["text"] = prev["text"].rstrip("，、；：") + sep + text
            prev["end"] = seg["end"]
        else:
            result.append(seg)

    return result


# ── Main refine pipeline ────────────────────────────────────────────

def refine(segments: list[dict], max_chars: int = 30) -> list[dict]:
    if not segments:
        return []

    split_segs = []
    for seg in segments:
        sub = _split_recursive(seg, max_chars)
        split_segs.extend(sub)

    return _merge_short_fragments(split_segs)


# ── CLI ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Refine SRT segments using content-based semantic analysis"
    )
    parser.add_argument("input", help="input SRT file path")
    parser.add_argument("output", nargs="?", help="output SRT file path (default: overwrite input)")
    parser.add_argument("--max-chars", type=int, default=30, help="max chars per subtitle block")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    segs = parse_srt(str(input_path))
    if not segs:
        print(f"error: no valid segments in {input_path}", file=sys.stderr)
        sys.exit(1)

    out = refine(segs, max_chars=args.max_chars)
    output_path = args.output or str(input_path)
    write_srt(out, output_path)
    print(f"refined {len(segs)} \u2192 {len(out)} segments \u2192 {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
