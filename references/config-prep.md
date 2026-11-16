# Domain and Config Preparation

Load this reference before running the deterministic enhancement pipeline.

## Domain

Run `scripts/domain_scanner.py` on subtitle text to detect a domain:

```bash
cat input.srt | grep -v '^[0-9]*$' | grep -v '\-\->' | \
    python3 scripts/domain_scanner.py
```

`domain_policy=override` uses the user's `domain_override`. Otherwise apply this decision tree:

| Condition | Action |
|---|---|
| Scanner returns `general`, but ≥3 keywords match another domain | Use the matched domain and report the keywords |
| Scanner returns a domain with <3 matching keywords, but context clearly points elsewhere | Use the context-supported domain and explain the correction |
| Neither applies | Trust the scanner result |

Use the selected domain's `search_context` for web calibration. Report routine results without asking the user to reconfirm; ask only if the detection remains ambiguous or conflicts with an explicit user override.

## Config and Terminology

Detect the primary language, collect domain, and build the config for `scripts/enhance.py`:

```json
{
  "lang": "zh",
  "domain": "ai-3d",
  "match_mode": "auto",
  "terminology_overrides": {"EK": "1K"},
  "capitalization_overrides": {"mytool": "MyTool"},
  "title_candidates": ["艾尔登法环", "霍格沃茨之遗"],
  "split_avoid": ["的"]
}
```

Priority order:

1. User/CLI `terminology_overrides` (exact → casefold → normalized).
2. Static `correction-table.md` matches using the lookup procedure in `references/term-lookup.md` (same matching semantics as the pipeline).
3. Domain-aware web calibration for unmatched candidate terms only.
4. AI contextual inference, lowest confidence and always flagged.

Do not read `correction-table.md` into model context. The script reads it locally for both lookup and the normal enhancement run. Search only candidates returned as `unmatched`, use `"{term}" + "{search_context}"`, inspect the top results, and add only authoritative spellings to `terminology_overrides`.

Scan the full SRT for likely game/media titles while building config. Add confirmed names to `title_candidates`; `review-workflow.md` specifies when title-marker results may be overridden.

After config is ready, pass it directly to `enhance.py`; do not stop for a separate config confirmation. All proposed text changes are reviewed in the final diff.
