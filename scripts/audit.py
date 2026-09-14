#!/usr/bin/env python3
"""
防复发审计：检查 enhanced SRT 中的过度替换 / 点链丢失信号。

背景（week8 课程发现）：
- 子串无界替换曾把 whatever→whatEVr、flex→Flux、psphere1→Photoshopphere1、
  jointt4→jointt、width(宽度语义)→weights。
- dot_re 无差别删点曾把 MC.skinweight.io→MC skinweight.io。
enhance.py 已加词边界 + CJK 邻接点保护，本脚本用于回归防复发。

检测分两档：
  ERROR  明确错误产物（点链丢失、jointt、Photoshopphere…）
  WARN   基于 correction-table asr 词条的「词内中招」，供人工复核

用法:
  python3 scripts/audit.py enhanced.srt                  # 误伤产物扫描
  python3 scripts/audit.py enhanced.srt --raw raw.srt    # 附带点链保留检查
  python3 scripts/audit.py enhanced.srt --list           # 列出由表导出的 WARN 信号
退出码: 0=无 ERROR, 1=存在 ERROR
"""

import argparse
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from enhance import load_terminology, parse_srt  # noqa: E402

CJK = r'[\u4e00-\u9fff\u3400-\u4dbf\uff00-\uffef\u3000-\u303f]'

# ── ERROR：明确错误产物 ────────────────────────────────────────────
ERROR_SIGNALS: list[tuple[str, str]] = [
    (r'jointt(?!|ait)', "joint 多加 t（原 jointt→jointtt 类误伤产物）"),
    (r'Photoshopphere', "ps→Photoshop 子串误伤产物"),
    (r'whatEVr', "eve→EV 子串误伤产物（whatever→whatEVr）"),
    (r'Fl[uU]x', "flex→lux 子串误伤产物"),
    (r'\b[eE]v[eE][rR]\b', "EV 残留（复核）"),
]

# ── WARN：由 correction-table 自动导出的词内中招──────────────────
def build_word_inside_signals() -> list[tuple[str, str]]:
    """对单 token 拉丁 asr 词条（3-5 字符），检测增强文本中「非独立词出现」。

    即词条两侧被拉丁字母/数字包围（无词边界）——这是原无界子串替换的
    命中形态，若该词条仍需要全局替换，此处会提示复核。
    """
    signals = []
    skip = {"ps", "width"}  # 保留词的独立词条太常见，降噪
    for asr in load_terminology().keys():
        if any(ch in asr for ch in " /."):
            continue
        s = asr.lower()
        if not re.fullmatch(r'[a-z0-9]{3,5}', s):
            continue
        if s in skip:
            continue
        pat = re.compile(
            r'[A-Za-z0-9_]' + re.escape(asr) + r'[A-Za-z0-9_]*'
            r'|[A-Za-z0-9_]*' + re.escape(asr) + r'[A-Za-z0-9_]',
            re.IGNORECASE,
        )
        signals.append((pat.pattern, f"asr 词条 {asr} 词内出现（复核词边界是否漏替换）"))
    return signals


def audit(texts: list[str], signals: list[tuple[str, str]],
          verdict: str) -> list[dict]:
    hits = []
    for i, text in enumerate(texts, 1):
        for pat, desc in signals:
            if re.search(pat, text):
                hits.append({"index": i, "verdict": verdict, "desc": desc,
                             "text": text})
    return hits


def audit_dot_chains(raw_texts: list[str], out_texts: list[str]) -> list[dict]:
    """Compare dot chains case-insensitively and segment-wise.

    A chain is considered preserved when every raw segment still appears
    (case-insensitive) in the output joined by dots, even if capitalization
    changed (depth.gen → depth.Gen) or a segment was legitimately replaced
    by terminology (ArcData → MArgData). Only report ERROR when a segment
    or the dot structure itself is missing.
    """
    chain_re = re.compile(
        r'(?<![A-Za-z0-9.])[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)+(?![A-Za-z0-9])',
        re.IGNORECASE)
    out_chains = [m.group(0) for t in out_texts for m in chain_re.finditer(t)]
    out_lower_set = {c.lower() for c in out_chains}
    out_seg_tokens = {seg.lower() for c in out_lower_set for seg in c.split(".")}

    results: list[dict] = []
    for t in raw_texts:
        for m in re.finditer(
                r'(?<![A-Za-z0-9.])[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)+(?![A-Za-z0-9])',
                t, re.IGNORECASE):
            raw_chain = m.group(0)
            if raw_chain.lower() in out_lower_set:
                continue
            # Segments may differ by terminology replacement; verify the dot
            # structure survives by checking each raw segment still appears.
            segs = raw_chain.split(".")
            n_segs = len(segs)
            # Only ERROR when point structure breaks (fewer segments in output
            # or segment missing). Segment content changes from terminology
            # replacement (ArcData→MArgData, join→joint) are downgraded to WARN.
            if any(s.lower() not in out_seg_tokens for s in segs):
                # Check if ANY output chain has same segment count (structure preserved)
                has_same_len = any(
                    len(c.split(".")) == n_segs for c in out_lower_set)
                results.append({
                    "chain": raw_chain,
                    "verdict": "WARN" if has_same_len else "ERROR",
                    "desc": ("点链段被术语替换（复核是否合理）"
                             if has_same_len
                             else "raw 点链结构在 enhanced 中断裂（点可能丢失）"),
                })
    return results


def main():
    parser = argparse.ArgumentParser(description="SRT 防复发审计")
    parser.add_argument("input", help="enhanced SRT 路径")
    parser.add_argument("--raw", default=None, help="原始 SRT 路径（点链检查）")
    parser.add_argument("--list", action="store_true", help="列出 WARN 信号")
    parser.add_argument("--quiet", "-q", action="store_true", help="仅摘要")
    parser.add_argument("--max", type=int, default=40, help="最多打印条数")
    args = parser.parse_args()

    warn_signals = build_word_inside_signals()

    if args.list:
        for pat, desc in warn_signals:
            print(f"  {pat}\n      {desc}")
        sys.exit(0)

    texts = [seg["text"] for seg in parse_srt(args.input)]
    raw_texts = ([seg["text"] for seg in parse_srt(args.raw)]
                 if args.raw else [])

    errors = audit(texts, ERROR_SIGNALS, "ERROR")
    warns = audit(texts, warn_signals, "WARN")
    dot = audit_dot_chains(raw_texts, texts) if raw_texts else []

    all_hits = dot + errors + warns
    dot_error = sum(1 for d in dot if d.get("verdict") == "ERROR")
    print(f"audit: {len(errors)} ERROR(s), {len(warns)} WARN(s), "
          f"{len(dot)} 点链审计（{dot_error} 结构断裂）",
          file=sys.stderr if args.quiet else sys.stdout)

    if not args.quiet:
        for p in all_hits[:args.max]:
            if "chain" in p:
                print(f"  [{p['verdict']}] 点链 {p['chain']} — {p['desc']}")
            else:
                print(f"  [{p['verdict']}] #{p['index']}: {p['desc']}")
                print(f"        {p['text'][:120]}")
        if len(all_hits) > args.max:
            print(f"  … 剩余 {len(all_hits) - args.max} 项，用 --max 查看更多")

    sys.exit(1 if errors or dot else 0)


if __name__ == "__main__":
    main()