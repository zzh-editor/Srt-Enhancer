---
name: srt-enhancer
description: 优化或校正已有 SRT 字幕，或将字幕重断句为 9:16 竖屏短行。用于去口癖、ASR 纠错、术语与混排规范化；不用于音视频转录或字幕翻译。
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, WebFetch, Question]
version: 1.0.0
---

# SRT Enhancer

## When to Use This Skill

Use it when a user uploads or names an existing `.srt` and asks to optimize, enhance, clean, correct, or re-segment it for vertical 9:16 subtitles. This skill does not transcribe media or translate subtitles.

English triggers include `optimize subtitles`, `enhance SRT`, `vertical subtitles`, and `9:16 subtitles`.

## Outcome

Deliver a reviewed, valid SRT as a separate file.

## Fixed Workflow

Keep this order; later stages depend on earlier evidence:

1. **Collect preferences before parsing.** Standalone calls read `references/preflight.md`; `video-transcribe` calls read and validate `references/caller-mode.md`. Do not run setup, parse or scan before the applicable preferences are complete.
2. **Prepare environment and parse input.** Run `scripts/setup.sh`, validate the SRT and retain its input path. On parse failure, report the line and stop.
3. **Detect domain and prepare config.** Read `references/config-prep.md`; report the selected domain and use its `search_context`.
4. **Resolve terms and run the deterministic pipeline.** Use `references/term-lookup.md` to query suspect terms; web-search only returned `unmatched` terms. Read `references/script-usage.md` to run the normal pipeline once and write a candidate SRT under the task's scratch directory: `normalize → terminology → spacing → capitalization → terminology → finalize`. The script reads `correction-table.md` locally; never load the full table into model context.
5. **Review and approve.** Read `references/review-workflow.md`; show a confidence-scored text diff, then wait for the user's decision. Do not write the final output path before approval.
6. **Write and report.** After approval, standalone output is `{原始文件名}_Enhancer.srt` beside the input; caller mode writes only to its specified output path. Delete the candidate after the decision. Persist only user-confirmed terminology.

For a vertical-only request on an already prepared SRT, skip the normal preference questionnaire and read `references/vertical-workflow.md` plus `references/vertical-rules.md`. For a new subtitle request that also asks for vertical output, complete normal enhancement first. Run `scripts/vertical.py` as a separate stage; never change or overwrite the regular SRT.

## Non-Negotiable Constraints

- Do not change timestamps, numbering, cue count, SRT structure or meaning; add no source-absent content and remove no meaningful speech.
- Do not apply low-confidence corrections or write changed output before user approval.
- Keep diffs in chat. Delete a temporary diff preview after the decision; do not write an intermediate config JSON.
- Run deterministic transforms once through `enhance.py`; AI must not redo configured steps.
- For a caller, return the status block and output behavior in `references/caller-mode.md`. Never append a change summary to SRT text.

## Completion Criteria

- `enhance.py` succeeds; the result is valid SRT with the original cue count, numbering, timestamps and meaning. Add no source-absent content or remove meaningful speech.
- Every applied edit appears in the diff. Spot-check 5–10 cues; preserve low-confidence edits until approved.
- Write changed output only after user approval; persist only user-confirmed terminology.
- Use a tight, factual summary, not report language.

**NO:** “本次优化显著提升字幕质量，彰显整体表达效果。”

**OK:** “改正 3 处术语，去掉 2 个句首口癖；4 处低置信度原文保留。”

## On-demand References

| Need | Read |
|---|---|
| Run the normal deterministic pipeline | `references/script-usage.md` |
| Standalone preference questions | `references/preflight.md` |
| `video-transcribe` caller contract | `references/caller-mode.md` |
| Domain decision and config | `references/config-prep.md` |
| Candidate-term lookup | `references/term-lookup.md` |
| Final review and diff approval | `references/review-workflow.md` |
| Remember/reject/persist terms | `references/terminology-learning.md` |
| Known pitfalls | `references/anti-patterns.md` during review |
| Explicit 9:16 vertical output | `references/vertical-workflow.md`, `references/vertical-rules.md` and `scripts/vertical.py` |
| Candidate false-positive audit | `scripts/audit.py` during final review |
| Failure branch | `references/failure-handling.md` only when a step fails |
| Worked example | `references/example.md` when requested |
| Custom mixed typesetting | `references/mixed-typesetting.md` only for custom rules |
| Ambiguous ASR decisions | `references/enhancement-rules.md` only when needed |

`correction-table.md` and `domains.yaml` are script inputs, not model references. Treat them as script-owned data; do not load them wholesale.
