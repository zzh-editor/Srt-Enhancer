#!/usr/bin/env python3
"""Domain detection by keyword frequency scoring."""

import re
import yaml
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOMAINS_PATH = SKILL_DIR / "references" / "domains.yaml"


def load_domains(path: Path = DOMAINS_PATH) -> dict:
    if not path.exists():
        return {"domains": {"general": {"keywords": [], "search_context": ""}}}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"domains": {}}


def _has_chinese(s: str) -> bool:
    return any('\u4e00' <= ch <= '\u9fff' or '\u3400' <= ch <= '\u4dbf' for ch in s)


def _build_kw_pattern(kw: str) -> re.Pattern | None:
    """Build typed regex for keyword boundary handling. Returns None for pure Chinese (use substring)."""
    if _has_chinese(kw):
        return None  # pure/ mixed Chinese → substring match
    stripped = kw.strip()
    if not stripped:
        return None
    # contains space → multi-word phrase, allow flexible whitespace
    if ' ' in stripped:
        tokens = stripped.split()
        # short phrase with any token ≤3 → more permissive letter-boundary, else word boundary
        has_short = any(len(t) <= 3 and t.isalpha() for t in tokens)
        inner = r'\s+'.join(re.escape(t) for t in tokens)
        if has_short:
            return re.compile(r'(?<![A-Za-z0-9])' + inner + r'(?![A-Za-z0-9])', re.IGNORECASE)
        return re.compile(r'\b' + inner + r'\b', re.IGNORECASE)
    # single token
    if len(stripped) <= 3 and stripped.isalpha():
        # short abbrev like ue/uv/sop/vex/goz → don't require word boundary \b, allow UE5 but not value
        return re.compile(r'(?<![A-Za-z])' + re.escape(stripped) + r'(?![A-Za-z])', re.IGNORECASE)
    # single long token (may contain digits/hyphens)
    # use word boundary for pure alphanumeric
    if re.match(r'^[A-Za-z0-9]+$', stripped):
        return re.compile(r'\b' + re.escape(stripped) + r'\b', re.IGNORECASE)
    # fallback: letter-boundary
    return re.compile(r'(?<![A-Za-z0-9])' + re.escape(stripped) + r'(?![A-Za-z0-9])', re.IGNORECASE)


def detect_domain(texts: list[str],
                  domains_data: dict | None = None) -> str:
    """Score each domain by keyword frequency. Return highest-scoring domain key."""
    if domains_data is None:
        domains_data = load_domains()
    domains = domains_data.get("domains", {})
    if not domains:
        return "general"

    scores: dict[str, int] = {}
    # pre-compile patterns per domain
    domain_patterns: dict[str, list[tuple[str, re.Pattern | None]]] = {}
    for key, cfg in domains.items():
        kws = cfg.get("keywords", [])
        compiled = []
        for kw in kws:
            pat = _build_kw_pattern(kw)
            compiled.append((kw, pat))
        domain_patterns[key] = compiled
        scores[key] = 0

    for text in texts:
        text_lower = text.lower()
        for domain, kw_pats in domain_patterns.items():
            for kw, pat in kw_pats:
                if pat is None:
                    # Chinese substring
                    if kw.lower() in text_lower:
                        scores[domain] += 1
                else:
                    if pat.search(text):
                        scores[domain] += 1

    # Filter out zero scores
    scored = {k: v for k, v in scores.items() if v > 0}
    if not scored:
        return "general"

    return max(scored, key=scored.get)


def get_search_context(domain: str,
                       domains_data: dict | None = None) -> str:
    if domains_data is None:
        domains_data = load_domains()
    entry = domains_data.get("domains", {}).get(domain, {})
    return entry.get("search_context", "")


if __name__ == "__main__":
    import sys
    lines = [line.strip() for line in sys.stdin if line.strip()]
    domain = detect_domain(lines)
    ctx = get_search_context(domain)
    print(f"domain={domain}")
    print(f"search_context={ctx}")
