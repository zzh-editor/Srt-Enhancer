#!/usr/bin/env python3
"""Deterministic confidence scoring for subtitle corrections."""

CONFIDENCE_TABLE = {
    "table_exact":       (100, "对照表精确匹配"),
    "override_exact":    (100, "用户覆盖精确匹配"),
    "table_casefold":    (95,  "对照表大小写折叠"),
    "override_casefold": (95,  "用户覆盖大小写折叠"),
    "table_normalized":  (90,  "对照表归一化匹配"),
    "ratio_regex":       (90,  "比例格式正则"),
    "de_de_pattern":     (90,  "的得地正则模式"),
    "defiller_exact":    (95,  "口癖精确去除"),
    "defiller_context":  (80,  "口癖上下文去除"),
    "web_authoritative": (90,  "联网权威源确认"),
    "web_ambiguous":     (70,  "联网结果有歧义"),
    "web_no_result":     (50,  "联网无明确结果"),
    "ai_context_guess":  (55,  "AI 上下文猜测"),
    "title_known":       (85,  "已知作品名标注"),
    "title_cue":         (75,  "上下文线索标注"),
}


def score(source: str, sub_type: str | None = None) -> tuple[int, str]:
    # Try exact match first
    if sub_type:
        key = f"{source}_{sub_type}"
        if key in CONFIDENCE_TABLE:
            return CONFIDENCE_TABLE[key]
    # Try source only (no subtype, e.g. "ratio_regex")
    if source in CONFIDENCE_TABLE:
        return CONFIDENCE_TABLE[source]
    # Fallback: prefix match
    prefix = source + "_"
    for k, v in CONFIDENCE_TABLE.items():
        if k.startswith(prefix):
            return v
    return (60, "未知来源")


def label(score_value: int) -> str:
    if score_value >= 90:
        return "高"
    if score_value >= 70:
        return "中"
    if score_value >= 50:
        return "低"
    return "跳过"


def format_diff(source: str, sub_type: str = "exact") -> str:
    val, reason = score(source, sub_type)
    return f"{reason}({val}%)"


if __name__ == "__main__":
    for source, sub_type in [
        ("table", "exact"),
        ("table", "casefold"),
        ("table", "normalized"),
        ("ratio_regex", "exact"),
        ("web", "authoritative"),
        ("web", "no_result"),
        ("ai_context_guess", "exact"),
    ]:
        val, reason = score(source, sub_type)
        print(f"{source}/{sub_type}: {reason} ({val}%) → {label(val)}")
