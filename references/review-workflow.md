# AI Review and Diff Approval

Load this reference after `enhance.py` writes a temporary candidate under the task scratch directory. Keep the order: AI review → confidence scoring → show diff → wait for user decision → write the final SRT with only approved changes. The caller's `output_srt` or standalone `_Enhancer.srt` path must not exist before approval.

## Title and ASR Review

AI reviews the enhance.py output and applies remaining semantic steps:

**a. Game/Media Title Marking:**
Run `scripts/title_marker.py` for known titles:

```bash
cat output.srt | grep -v '^[0-9]*$' | grep -v '\-\->' | \
    python3 scripts/title_marker.py
```

**AI systematic scan** (并行于 Config 阶段，不增加轮次)：

在 §3 AI 构建 config 时，AI 需扫描输入全文，提取疑似作品名的 token（≥2个中文字或≥2个英文大写词），联网验证后：
- 将确认的作品名写入 JSON config 的 `title_candidates` 数组
- `title_marker.py` 执行后，AI 遍历 `title_candidates` 检查是否已加《》，未加则 override

AI overrides only when **all** conditions met:
- title_marker.py returned no match for a token
- Token matches a known game/media title pattern (≥2 words, capitalized, common title suffix like `2`/`3`/`World`/`War`/`Craft`)
- Web search confirms it's a game/media title (top-1 result is a title page or database entry)
- If any condition fails → keep original text, do not override

**Web-based ASR calibration (remaining unmatched terms only):**
- Read candidate lookup results produced with the procedure in `references/term-lookup.md`.
- Search only candidates with `status=unmatched`, using `"{term}" + "{search_context}"`; inspect the top 2 results.
- If an authoritative source is found, add the verified spelling to `terminology_overrides` with confidence ≥ 90%.
- If no authoritative result is found, leave the original unchanged and mark it ❗ in the diff.
- Never web-search a candidate reported as `asr_match` or `known_correct`.

**English remnant scan:**
- Scan candidate cues for pure-English captions of at most 4 characters. A cue of at most 3 letters and under 500ms is only a remnant candidate, not an automatic deletion.
- Confirm from neighboring text and timing before joining a split word to the previous cue or removing a meaningless isolated fragment. If the joined line is too long, split again at a semantic boundary without changing unrelated cues.
- Mark each accepted change as `英文残片合并` and include it in the diff with confidence ≥ 90%.

**Optional English-term annotation:**
- Run only when `enhancer_preferences.terminology_annotation=true` or the user explicitly requests it. Otherwise leave subtitle text unannotated.
- In Chinese subtitles, append `(<中文释义>)` without a space after an English technical term. Annotate every occurrence; prefer the correction table's Chinese meaning, then the domain glossary, then the general meaning.
- Consider multiword phrases and substantive single terms of at least four letters. Skip single-letter variables, abbreviations such as `AI`/`UE`/`OK`, and protected code, formula or path spans.
- Mark changes as `术语括注`; keep them in the final diff for user approval. This is semantic AI review, not a deterministic script step.

**Confidence Scoring:**
Use `scripts/confidence_scorer.py` for deterministic scoring:

```python
from confidence_scorer import score, format_diff
val, reason = score("table", "casefold")      # 95%
val, reason = score("web", "authoritative")    # 90%
val, reason = score("ai_context_guess", "exact")  # 55%
```

## Diff Review

Assign a confidence score to every modification and present a diff table for user review.

| Level | Label | Meaning |
|-------|-------|---------|
| ≥ 90% | High | Clear correction — terminology match, web-verified, or obvious typo |
| 70-89% | Medium | Likely correct but minor ambiguity — e.g., homophone in context |
| 50-69% | Low | Uncertain — flag for user review |
| < 50% | Skip | Don't apply; preserve original |

**Confidence Guidelines by Change Type:**
- **Filler word removal**: High (≥90%) for hesitation sounds; Medium (70-89%) for context-dependent particles like `呢`/`吧`
- **Terminology correction (table match)**: High (≥90%) for exact table match; Medium (70-89%) for fuzzy match
- **Web-verified correction**: High (≥90%) if authoritative source confirms; Medium (70-89%) if ambiguous
- **Homophone/spelling correction without web verification**: Low (50-69%) — always flag

When comparing the original SRT and enhanced output, diff text lines only. Skip numbering and timestamp lines because rewriting may introduce ±1ms floating-point differences.

- Up to 20 changes: show the full table in chat.
- More than 20: show the first 20 and write the complete diff preview next to the input SRT.
- Do not write any changed SRT to the final output path before the user confirms. Keep any candidate only in the current task's temporary directory.

Before presenting the diff, run the regression audit on the final candidate after all semantic edits:

```bash
python3 scripts/audit.py "<scratch_dir>/candidate.srt" --raw "<input_srt>"
```

- `ERROR` or a nonzero exit blocks the final output. Keep the source, report the affected cue, and ask for correction or leave the original unchanged.
- `WARN` remains reviewable: show it with the related diff entry and let the user decide. A warning alone does not fail the audit command.

最终决定通过当前 Agent 提供的交互确认方式收集：

- `全部确认`: apply all changes.
- `逐条审核`: apply only the approved entries.
- `全部拒绝`: apply nothing.

After approval, write the approved candidate to the final output path, then delete the candidate and temporary diff preview. Persist only user-confirmed corrections to `references/correction-table.md`. If the user rejects every change, delete the candidate and diff preview and leave the final output path absent.
