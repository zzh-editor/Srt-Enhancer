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


def detect_domain(texts: list[str],
                  domains_data: dict | None = None) -> str:
    """Score each domain by keyword frequency. Return highest-scoring domain key."""
    if domains_data is None:
        domains_data = load_domains()
    domains = domains_data.get("domains", {})
    if not domains:
        return "general"

    scores: dict[str, int] = {}
    domain_keywords: dict[str, list[str]] = {}
    for key, cfg in domains.items():
        kws = cfg.get("keywords", [])
        domain_keywords[key] = kws
        scores[key] = 0

    for text in texts:
        text_lower = text.lower()
        for domain, kws in domain_keywords.items():
            for kw in kws:
                if kw.lower() in text_lower:
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
