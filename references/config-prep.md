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
  "capitalization_overrides": {"mytool": "MyTool"}
}
```

Priority order:

1. User/CLI `terminology_overrides` (exact → casefold → normalized).
2. Static `correction-table.md` matches using the lookup procedure in `references/term-lookup.md` (same matching semantics as the pipeline).
3. Domain-aware web calibration for unmatched candidate terms only.
4. AI contextual inference, lowest confidence and always flagged.

Do not read `correction-table.md` into model context. The script reads it locally for both lookup and the normal enhancement run. Search only candidates returned as `unmatched`, use `"{term}" + "{search_context}"`, inspect the top results, and add only authoritative spellings to `terminology_overrides`.

作品名标记由 `title_marker.py` 自己扫描，不写入 config（`title_candidates`、`split_avoid`、`custom_spacing_rule` 都不是 `enhance.py` 的配置键，传进去会被忽略）。

config 不落盘：`--config` 只接受文件路径，而按 `SKILL.md` 约束不得写中间 config。改用 `--lang`、`--domain`、`--overrides`（JSON 字符串）逐项传值。不需要单独的 config 确认环节，所有文字改动在最终 diff 里审。
