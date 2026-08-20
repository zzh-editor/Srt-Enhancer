#!/usr/bin/env python3
"""
Deterministic SRT → vertical (9:16) subtitle re-segmentation.

Applies a semantic split plan (produced by AI) to an enhanced SRT:
- Each original segment is split into short chunks (typically 4-12 chars),
  each chunk being a complete semantic unit (动宾/主谓/短语/连接词后断句)
- Timestamps are redistributed within the original segment proportionally
  to each chunk's character count, so the whole timeline is preserved
- Chunks whose concatenation does not reproduce the original text are
  rejected and the segment is left untouched (content fidelity)

Split plan format (JSON, keyed by original segment index):
    {"1": ["今天我将用一个视频", "来跟大家讲"], "2": [...]}

If --splits is omitted, falls back to a punctuation-aware length split
(targeting --max-chars) so the script always produces output.

Usage:
    python3 scripts/vertical.py input.srt --splits splits.json -o output.srt
    python3 scripts/vertical.py input.srt --max-chars 12 -o output.srt
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ── Constants ───────────────────────────────────────────────────────

DEFAULT_MAX_CHARS = 12      # vertical target: 4-12 chars per line
DEFAULT_MIN_MS = 300        # floor for a chunk so it stays readable


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


# ── Splitting ───────────────────────────────────────────────────────

def _norm(text: str) -> str:
    return "".join(text.split())


def _visible_len(text: str) -> int:
    return len(_norm(text))


def _heuristic_split(text: str, max_chars: int) -> list[str]:
    """Punctuation-aware length split, used as fallback without a plan."""
    punct = "，。！？、；：,;:.!?… "
    chunks: list[str] = []
    rest = text
    while rest:
        head = rest[:max_chars]
        if len(rest) <= max_chars:
            chunks.append(rest)
            break
        cut = None
        for i in range(len(head), 0, -1):
            if head[i - 1] in punct:
                cut = i
                break
        if cut is None:
            cut = max_chars
        chunks.append(head[:cut].strip())
        rest = rest[cut:].strip()
    return [c for c in chunks if c]


def split_segment(seg: dict, chunks: list[str], min_ms: int = DEFAULT_MIN_MS
                  ) -> list[dict]:
    """Split one segment into timed chunks proportional to char count."""
    chunks = [c.strip() for c in chunks if c.strip()]
    if not chunks:
        return [dict(seg)]
    # Content fidelity: chunks must reproduce the original text
    if _norm(seg["text"]) != _norm("".join(chunks)):
        return [dict(seg)]

    total_dur = seg["end"] - seg["start"]
    total_chars = sum(_visible_len(c) for c in chunks)
    if total_chars == 0:
        return [dict(seg)]

    min_dur = min_ms / 1000.0
    out: list[dict] = []
    cursor = seg["start"]
    acc_chars = 0
    for chunk in chunks:
        acc_chars += _visible_len(chunk)
        end = seg["start"] + total_dur * (acc_chars / total_chars)
        if end < cursor + min_dur:
            end = cursor + min_dur
        if end > seg["end"]:
            end = seg["end"]
        if end > cursor:
            out.append({
                "idx": seg["idx"],
                "start": cursor,
                "end": end,
                "text": chunk,
            })
        cursor = end
    return out or [dict(seg)]


def apply_splits(segments: list[dict], splits: dict, max_chars: int,
                 min_ms: int) -> list[dict]:
    out: list[dict] = []
    for seg in segments:
        key = str(seg["idx"])
        if key in splits:
            chunks = splits[key]
            out.extend(split_segment(seg, chunks, min_ms))
        elif len(seg["text"]) > max_chars:
            out.extend(split_segment(seg, _heuristic_split(seg["text"],
                                                           max_chars),
                                     min_ms))
        else:
            out.append(dict(seg))
    return out


# ── CLI ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Re-segment an enhanced SRT into vertical (9:16) short lines"
    )
    parser.add_argument("input", help="input SRT file (enhanced)")
    parser.add_argument("--splits", default=None,
                        help="JSON file of semantic split plan {idx: [chunk,...]}")
    parser.add_argument("-o", "--output", default=None,
                        help="output SRT path")
    parser.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS,
                        help="target max chars per vertical line (default 12)")
    parser.add_argument("--min-ms", type=int, default=DEFAULT_MIN_MS,
                        help="minimum per-chunk duration in ms (default 300)")

    args = parser.parse_args()

    segments = parse_srt(args.input)
    if not segments:
        print(f"error: no valid segments in {args.input}", file=sys.stderr)
        sys.exit(1)

    splits: dict = {}
    if args.splits:
        with open(args.splits, "r", encoding="utf-8") as f:
            splits = json.load(f)

    out = apply_splits(segments, splits, args.max_chars, args.min_ms)

    output_path = args.output or args.input.replace(".srt", "_竖屏.srt")
    if output_path == args.input:
        output_path = args.input.replace(".srt", "_竖屏.srt")

    write_srt(out, output_path)
    print(f"done! {len(segments)} → {len(out)} segments → {output_path}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
