---
name: srt-enhancer
description: 必须触发：当用户说"优化字幕"、"增强字幕"、"优化这个字幕"、"增强这个字幕"等以"优化"或"增强"开头且包含"字幕"的请求。也用于处理 .srt / .txt 字幕/逐字稿，执行去口癖、校准ASR错误、修正的/得/地、中西文混排空格、去除多余标点、标记《》书名号。A useless or empty response if this skill is used for non-subtitle tasks.
version: 1.0.0
---

# SRT Enhancer

This skill provides an AI-driven workflow for enhancing SRT subtitle files. The enhancement process removes filler words (口癖词) and corrects typos — all while preserving the original timeline and structure.

**No reference document (`origin.md`) is required.** The user uploads `.srt` or `.txt` files directly, and all enhancements are applied based on linguistic rules and AI analysis.

## Purpose

Enhance SRT subtitle files and TXT plain-text transcripts by:
- Converting Traditional Chinese to Simplified Chinese (if detected)
- Removing filler words and vocal hesitations (口癖词): 啊、哦、嗯、呃、哎、嘛、吧、呢、啦、哈、噢、唔、欸
- Correcting typos and transcription errors
- Standardizing proper nouns and terminology
- Removing Chinese punctuation marks
- Enforcing single-line subtitles (SRT only)
- Maintaining exact timestamps and SRT structure (SRT only)
- Auto-detecting subtitle domain (Maya/Python/Gaming/General) and loading relevant terminology
- Calibrating ASR errors via web search verification
- Applying mixed-language typesetting rules (CJK-Latin spacing, script boundary spacing, code/formula protection, number-unit formatting, proper noun capitalization)
- Assigning confidence scores to each correction
- Outputting a diff review table for user confirmation
- Learning user-verified corrections incrementally within the session

## When to Use This Skill

Use this skill when the user mentions or uploads files related to:
- Cleaning up auto-generated subtitles (ASR output) from `.srt` or `.txt` files
- Removing filler words and hesitations from spoken transcripts (去口癖/去除语气词)
- Correcting 的/得/地 based on syntactic position（的得地修正）
- Correcting transcription errors and calibrating ASR misrecognitions via web search
- Applying CJK-Latin spacing and mixed-language typesetting（中西文混排/空格/间距）
- Removing Chinese punctuation marks from subtitles（去除标点）
- Marking game/film titles with 《》book-title marks（书名号标记）
- The user uploads a `.srt` or `.txt` file for enhancement
- The user wants to review a diff table of all changes before finalizing

## Enhancement Principles

1. **Timeline Preservation**: Never modify timestamps or subtitle numbering (SRT only)
2. **Content Fidelity**: Correct and clean existing content; don't add new content
3. **Filler Word Removal**: Remove vocal hesitations and meaningless fillers
4. **AI-Driven**: Use semantic understanding, not just regex patterns
5. **Web-Verified**: Use web search to verify suspected ASR errors before correction
6. **Confidence-Aware**: Assign confidence levels to every change; flag low-confidence corrections for user review
7. **Session Learning**: Remember user-verified corrections within the session to avoid repeated confirmations
8. **Mixed-Language Typesetting**: Apply consistent spacing, capitalization, and punctuation rules for multilingual content while protecting code, formulas, and file paths

## Core Workflow

### 1. Receive File

The user uploads a file (`.srt` or `.txt`) directly via the dialog:
- Accept the uploaded file
- No reference document (`origin.md`) is needed
- If `.srt`: Parse the SRT file structure (index, timestamp, text)
- If `.txt`: Treat as plain-text transcript; split by paragraphs or speaker turns; no timestamps

### 1.5. Confirm Mixed-Language Typesetting

**At the very start**, before any processing, notify the user about mixed-language typesetting:

> "中西文混排规范默认开启（如 Python 编程、5GB、GPU 驱动），是否需要调整？"

- Default: **ON** (CJK-Latin spacing, code protection, number-unit compact, capitalization)
- User can say `不需要空格` to disable, or adjust later with `中日文之间不加空格`
- Typesetting is applied during step 7 (Mixed-Language Typesetting)
🔴 **CHECKPOINT** — 等用户回答后再继续。未回答时不得默认进入处理流程。

### 2. Parse SRT File

Load and parse the input SRT file:
- Extract subtitle number
- Extract timestamp (start → end)
- Extract subtitle text
- Preserve exact formatting and structure
- 🔴 解析失败 → 查 Failure Handling 表「SRT 文件解析失败」

### 2.5. Auto Domain Detection

Analyze the content to automatically detect the domain and load the most relevant terminology reference:

1. Scan all subtitle text for domain-specific keywords:
   - **Maya domain**: `make`, `polyCube`, `Hypershade`, `rigging`, `joint`, `blend shape`, `NURBS`, `paint weights`, `keyframe`
   - **Python domain**: `import`, `def`, `class`, `PySide`, `PyQt`, `numpy`, `pandas`, `dataclass`, `lambda`
   - **Gaming domain**: `Rookies`, `Concept Art`, `Keyframe`, `Paint Over`, `game`, `player`, `texture`, `shader`
2. If multiple domains detected, load all matching terminology tables
3. If no domain matches, use the general terminology table only
4. Report detected domain(s) to the user: `检测到领域: Maya + Python`

### 2.6. Convert Traditional Chinese to Simplified Chinese

ASR models may output Traditional Chinese characters. Detect and convert all Traditional Chinese to Simplified Chinese:

- AI-based conversion (no external library required)
- Only convert Chinese characters; English, numbers, and code remain unchanged
- Apply as the very first text processing step (before filler removal)
- Example: `這個功能很好` → `这个功能很好`

### 3. Apply Filler Word Removal

Scan each subtitle segment and remove filler words (口癖词):

**Common filler words to remove:**
- Hesitation sounds: 啊、哦、嗯、呃、哎、噢、唔、欸、嘿
- Sentence-final particles (when meaningless): 嘛、吧、呢、啦、哈、哟、喔
- Filler phrases: 那个、就是、你知道吗、怎么说呢

**Rules:**
- Remove the filler word and its adjacent space/punctuation if it becomes redundant
- Preserve sentence meaning and natural flow
- Don't remove particles that carry grammatical meaning (e.g., 吗 for questions, 的 for possession)
- When a filler word is between two words, merge smoothly without double spaces
- **不要将自然话语标记（Discourse Markers）视为口癖：** 也就是说、然后、那么、那（句首）、说白了、这边的话、对吧、好吧 等是中文口语中的惯用连接手段和过渡词，不会干扰理解，不应删减

Reference `references/enhancement-rules.md` for detailed filler word handling strategies.

### 3.5. Apply 的/得/地 Correction

Correct the most common ASR misrecognition — 的/得/地 — based on syntactic position.

**Critical ASR behavior**: ASR models default to outputting "的" for weak syllables, causing it to appear far more frequently than correct Chinese text. Every occurrence of "的" must be syntactically examined — do not assume it's correct.

**Decision Tree** (examine the word AFTER 的/得/地):

| Position | Character | Rule | Example |
|----------|-----------|------|---------|
| Before noun/noun phrase | **的** | 定语/所属标记 | 美丽的`花`、我的`书`、新`功能` |
| Before verb phrase (adverbial) | **地** | 状语标记，修饰动作 | 慢慢`地走`、认真`地学`、反复`地调` |
| After verb/adj, before degree/result | **得** | 补语标记，连接程度/结果 | 跑`得快`、做`得好`、画`得非常漂亮` |

**Quick Check**: If the word after is a noun → **的**. If the word before is a verb/adj AND the word after is a complement (程度/结果/状态) → **得**. If the word after is a verb AND modifies how it's done → **地**.

**High-Frequency Fixed Patterns** (apply directly, no context analysis needed):

| Pattern | Correct | Reason |
|---------|---------|--------|
| 变得、懂得、觉得、记得、显得 | **得** (fixed) | 固定搭配 |
| 值得、免得、取得、获得、认得 | **得** (fixed) | 固定搭配 |
| V/A + 得 + 很好/很漂亮/很快/要命 | **得** | 程度补语 |
| 做得、跑得、画得、说得、长得、玩得 | **得** | 补语结构 |
| 慢慢地、快快地、认真地、反复地 | **地** | 副词后缀 |
| 自动地、逐渐地、不断地、持续地 | **地** | 副词后缀 |

**Common ASR Misrecognition Table**:

| ASR Output | Correct | Clue |
|-----------|---------|------|
| 做的非常好 | 做得非常好 | "做"+得+程度补语 |
| 做的很棒 | 做得很棒 | 同上 |
| 做的对 | 做得对 | "做"+得+结果 |
| 慢慢的走 | 慢慢地走 | 状语修饰"走" |
| 认真做 | （不变） | "认真"本身就是副词，无需改 |
| 累的够呛 | 累得够呛 | 形容词+得+程度 |
| 累的不行 | 累得不行 | 同上 |
| 变的更好 | 变得更好 | 固定搭配"变得" |
| 变的更差 | 变得更差 | 同上 |
| 学的很快 | 学得很快 | 动词+得+程度 |
| 我的东西 | 我的东西 | 定语，不变 |
| 你的看法 | 你的看法 | 定语，不变 |
| 跑的快 | 跑得快 | 补语结构 |
| 干的不错 | 干得不错 | 动词+得+程度 |
| 懂的 | 懂得 (if verb) / or 懂的 (if noun) | 需分辨：懂得(动词)vs 懂的(定语) |

**Preserved cases** (ASR usually gets these right, but do not over-correct):
- 定语"的": 我的、你的、新的、好的、漂亮的、之前的
- 句末"的": 是我做的、他会来的

This step runs after filler word removal, before terminology correction. Reference `references/enhancement-rules.md` §2.1 for detailed rules.

### 4. Apply Typo and Terminology Correction

Correct common transcription errors using AI analysis and the terminology reference table:

- **Similar character errors**: 工具/工俱, 功能/公能
- **ASR misrecognition of technical terms**: Use `references/terminology.md` to match and correct (case-sensitive, only fixes clear misrecognitions)
  - Maya 术语: `make` → `Maya`, `mayor` → `Maya`, `maya` → `Maya` 等
  - Python 术语: `bison` → `Python`, `pie thon` → `Python`, `piethon` → `Python` 等
  - 编程术语: `key frame` → `Keyframe`, `poly cube` → `polyCube` 等
  - **普通英文单词保持原样**（如 `import`, `none`, `callback` 等不强制大写）
- Missing or extra characters
- Use contextual understanding to determine correct form

Reference `references/terminology.md` for the complete Maya/Python terminology mapping table.

### 5. Web-Based ASR Calibration

After terminology correction, perform web search verification for suspected ASR errors that don't match any entry in the static terminology tables:

**When to trigger a web search:**
- A proper noun (person name, company, product, place) sounds plausible but is not in any terminology table
- An English word appears in an unusual form that could be an ASR hallucination
- A Chinese word doesn't make sense in context and looks like a homophone error
- The confidence in a term's correctness is below 70% (see Confidence Scoring)

**Web search workflow:**
1. Extract the suspect term and its surrounding context (2-3 words before and after)
2. Use `websearch` tool with query format: `"suspect term" + "domain" + "correct spelling"` or `"suspect term" 术语 正确写法`
3. Evaluate search results:
   - If a clear authoritative result confirms a different spelling → correct to that spelling (confidence: high)
   - If multiple plausible spellings exist → flag for user review (confidence: medium)
   - If search confirms the current spelling is correct → skip correction (confidence: high)
4. Record the web-verified correction in the session's incremental terminology table
🔴 web search 超时或无结果 → 查 Failure Handling 表「联网 web search 失败」

**Examples:**
| Suspect Term | Search Query | Likely Correction | Confidence |
|-------------|-------------|-------------------|------------|
| `Owatch` | `Owatch game company` | Overwatch | High |
| `R Center` | `R Center art school` | Art Center | High |
| `pie thon 3.9` | `pie thon programming language` | Python 3.9 | High |

**Important:**
- Only search when confidence is low enough to warrant verification
- Don't search common words (`import`, `function`, `class`)
- Don't search Chinese daily vocabulary
- Cache search results during the session to avoid redundant queries

### 6. Mixed-Language Typesetting

Apply consistent mixed-language formatting rules before punctuation removal.

**Scope:** Applied after ASR calibration, before punctuation removal.

**Execution**: Run `scripts/apply_spacing.py` on the line-by-line subtitle text for deterministic CJK-Latin spacing. Then AI-review the output for protection zones, edge cases, and custom terminology.
🔴 脚本执行报错 → 查 Failure Handling 表「spacing 脚本执行失败」

**Rules:**

1. **Script Boundary Spacing** (enabled by default, handled by `scripts/apply_spacing.py`):
   - Add space between Han (CJK) and Latin scripts: `Python编程` → `Python 编程`
   - Add space between Han and Hiragana/Katakana/Hangul (Chinese-dominant text only)
   - Add space between Hangul and Latin/Han (Chinese-dominant text only)
   - No space between same-script characters (Latin-Latin, Han-Han)
   - **Note**: If a subtitle segment is primarily Japanese or Korean (no Chinese content), skip Han-Kana/Han-Hangul spacing to avoid breaking native text. This rule only applies when Chinese is the dominant language.

2. **Protection Zones** (preserved from spacing/punctuation changes, applied FIRST before any other rule):
   - Inline code: `` `code` ``
   - Fenced code blocks: ```code```
   - Inline math: `$...$`, `\(...\)`
   - Display math: `$$...$$`, `\[...\]`
   - File paths: `/path/to/file`, `C:\path`
   - URLs: `https://...`

3. **Number-Unit Formatting** (default: compact):
   - `5GB` (compact) — no space between number and unit
   - Version numbers: `v1.0`, `v2.3.1` (compact)

4. **Proper Noun Capitalization** (heuristic + terminology table):
   - Known acronyms: GPU, CPU, API, SDK, AI, HTML, CSS, JS, TS, JSON, SQL, HTTP, REST, etc.
   - CamelCase/PascalCase preserved: `polyCube`, `Keyframe`
   - Terminology table entries override heuristic

**User Configuration** (optional, via natural language):
- `中日文之间不加空格` → disable CJK-CJK spacing
- `数字单位加空格` → `5 GB` (spaced)
- `保护代码块` → enable code protection (default on)
- `显示混排配置` / `重置混排配置`

Reference `references/mixed-typesetting.md` for complete specification.

### 7. Apply Punctuation Removal

Remove all Chinese and English punctuation marks from subtitle text (after mixed-language typesetting):

**Punctuation to remove:**
- Chinese: ，。！？、；：""''【】（）—…·～
- English: ,!?;:'"()[]{}<>/-_=+|\\@#$%^&*~`
- **Note**: `.` (dot) is preserved because it appears in filenames (e.g., `Visuals.py`) and technical identifiers

**Preserved punctuation:**
- `《》` (U+300A/U+300B) — book-title marks added by the game/film title marking step are preserved

**Rules:**
- Remove all listed punctuation characters from subtitle text
- Do not modify timestamps (which contain `:` and `,`)
- Do not remove punctuation inside protection zones (code, math, paths, URLs)
- Apply punctuation removal after mixed-language typesetting
- Ensure no empty subtitles remain after punctuation removal

### 8. Game/Media Title Marking

Apply Chinese book-title marks 《》 for known game/film/TV series titles. This step runs **after** punctuation removal to avoid the marks being deleted.

**Rules:**
- Add 《》 only for confirmed game/film/TV series titles
- Engines/tools/companies/platforms: no 《》 (e.g., `Unreal Engine 5`, `Bungie`, `Steam`, `Photoshop`)
- Use context cues: gaming verbs (玩、打、通关), film verbs (看、上映), review language (推荐、评测)

**Examples:**
- `黑神话：悟空` → 《黑神话：悟空》
- `对马岛之魂` → 《对马岛之魂》
- NOT: `Unreal Engine 5` → `Unreal Engine 5` (unchanged)
- NOT: `Bungie` → `Bungie` (unchanged)

Reference `references/mixed-typesetting.md` §6 for complete title list and context cue rules.

### 9. Enforce Single-Line Subtitles (SRT only)

Every SRT subtitle block must contain exactly one line of text.

> **TXT files**: Skip this step. Preserve paragraph structure as-is.

**Rules:**
- If a subtitle block has multiple text lines, merge them into a single line
- If the merged line exceeds 40 characters, split it into multiple subtitle blocks at semantic boundaries
- Semantic break points: conjunctions (然后、所以、但是), topic shifts (接下来、另外), examples (比如说、举个例子)
- If no semantic break point is found, split at spaces (Chinese-English boundary) or between Chinese characters
- Never split in the middle of an English word
- Each split subtitle block inherits the same timestamp as the original
- Re-number all subtitle blocks sequentially after splitting

Before finalizing each correction:
- Ensure the subtitle remains grammatically correct
- Verify no new content is added
- Confirm timestamps remain unchanged (SRT only)
- Check subtitle numbering is preserved (SRT only)

### 10. Confidence Scoring & Diff Output

Assign a confidence score to every modification and present a diff table for user review.

**Confidence Levels:**

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

**Diff Output Format:**

After processing, present a review table before generating the final file:

```
## 修改预览 (Diff Review)

| # | 原文 | 修改后 | 置信度 | 类型 |
|---|------|--------|--------|------|
| 1 | 嗯今天我们要 | 今天我们要 | 高(95%) | 去口癖 |
| 5 | match case 工俱 | match case 工具 | 高(100%) | 错别字 |
| 8 | Owatch 游戏 | Overwatch 游戏 | 高(90%) | 联网校准 |

❗ = 需要用户确认
```

**User Review Workflow:**
1. Present the diff table
2. Ask: `以上修改是否全部确认？(y/n) 或输入编号单独确认/拒绝`
🔴 **CHECKPOINT** — 必须等待用户输入。未确认不得进入输出生成。
3. If user rejects specific items, revert those changes
4. If user confirms, apply all changes and generate output
5. Record user-verified corrections into the session's incremental terminology table

### 11. Generate Output File

Save the enhanced result:
- **SRT input** → `enhanced.srt` (maintain all original timestamps, numbering, formatting)
- **TXT input** → `enhanced.txt` (plain text, cleaned, one sentence per line recommended)
- Apply all validated (user-confirmed) corrections
- Include a summary of changes at the end of the output

## Incremental Terminology Learning

During a session, maintain a **session terminology table** that grows as the user reviews corrections.

### How It Works

1. Start of session: Load the static references (`references/terminology.md`, `references/asr-corrections-gaming.md`)
2. During processing: When a correction is made (typ fix, web-calibrated term, terminology match), record it in the session table
3. User review: When the user confirms a correction in the diff review, promote it to the session table
4. Subsequent blocks: Before making any terminology decision, first check the session table (highest priority), then the static references, then fall back to web search

### Session Table Format

```
session_terminology.jsonc (in-memory, not persisted to disk):
{
  "entries": [
    { "asr": "Owatch", "correct": "Overwatch", "confidence": "web-verified", "source": "user-confirmed" },
    { "asr": "R Center", "correct": "Art Center", "confidence": "web-verified", "source": "user-confirmed" }
  ]
}
```

### Priority Order

When encountering a potentially incorrect term:
1. **Session table** (user-confirmed this session) → apply immediately (high confidence)
2. **Static terminology.md / asr-corrections-gaming.md** → apply (high confidence)
3. **Web search verification** → apply with medium-high confidence
4. **AI contextual guess** → apply with low confidence, always flag for review

### Session Lifecycle

- Session table is **reset** when the skill is re-loaded in a new conversation
- User can manually add entries by saying: `记住：XXX 的正确写法是 YYY`
- User can clear session table: `清除本次学习的术语`

## Implementation Guidelines

### Enhancement Order

Apply corrections in this priority order:
1. **Traditional → Simplified Chinese** (convert Traditional Chinese if detected)
2. **Auto Domain Detection** (identify domain, load relevant terminology)
3. **Filler word removal** (clean up meaningless content)
4. **的/得/地 Correction** (fix based on syntactic position: 定语→的, 状语→地, 补语→得)
5. **Typo and terminology correction** (fix transcription errors using terminology table)
6. **Web-Based ASR Calibration** (verify suspected errors via web search)
7. **Mixed-Language Typesetting** (apply spacing, code protection, number-unit format, capitalization)
8. **Punctuation removal** (remove punctuation; preserve 《》 and protection zones)
9. **Game/Media Title Marking** (add 《》 for known game/film titles)
10. **Single-line enforcement** (SRT only — merge multi-line blocks, split long lines at semantic boundaries)
11. **Confidence Scoring & Diff Output** (assign confidence, present diff table, collect user feedback)
12. **Output generation** (enhanced.srt or enhanced.txt)

### Quality Checks

Before generating output:
- Verify all timestamps are unchanged (SRT only)
- Confirm subtitle/block count matches original
- Validate no content was added
- Check filler words properly removed
- Ensure proper nouns are standardized
- Verify web-calibrated terms against search results
- Verify mixed-language typesetting applied correctly (spacing, capitalization, title marks, protection zones)
- Validate output filename is `enhanced.srt` or `enhanced.txt`
- Ensure no low-confidence corrections were applied without user confirmation

## Example Enhancement

See `references/example.md` for a complete worked example (input → processing steps → diff table → output).

## Important Constraints

### Must NOT:
- Modify timestamps or subtitle numbering (SRT only)
- Add new content that wasn't in the original file
- Change the meaning or intent of subtitles
- Remove meaningful content (only fillers)
- Alter SRT structure or formatting (SRT only)
- Remove grammatical particles (的, 了, 吗, etc.) that carry meaning
- Apply low-confidence corrections without user approval
- Use scripts for tasks requiring semantic understanding (filler removal, 的/得/地 correction, terminology lookup, ASR calibration)

### Must DO:
- Use AI to analyze and apply semantic enhancements
- Remove filler words and vocal hesitations
- Correct obvious typos
- Perform web search verification for suspected ASR errors
- Apply 的/得/地 correction based on syntactic position (定语→的, 状语→地, 补语→得)
- Apply mixed-language typesetting rules (CJK-Latin spacing, protection zones, number-unit formatting, capitalization)
- **Use `scripts/apply_spacing.py` for CJK-Latin spacing (deterministic)**, then AI-review the output for protection zones and edge cases
- Apply game/film title 《》book-title marks for known game/film titles only (not for engines/tools/companies)
- Assign confidence scores to every modification
- Present a diff review table to the user
- Output to `enhanced.srt` (SRT input) or `enhanced.txt` (TXT input)
- Preserve exact timestamps and structure (SRT only)
- Remember user-verified corrections during the session

## Failure Handling

Each workflow step has an explicit failure branch. Follow this table when any step does not produce the expected result.

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| SRT 文件解析失败（格式无效/时间戳错误/编号不连续） | 提示用户并提供行号 | 回退为 TXT 逐行处理，不做时间轴保证 |
| 领域检测无匹配 | 使用通用术语表 | 跳过术语校准，仅执行其他步骤 |
| 繁转简后文本无变化（输入已为简体） | 跳过本步，继续下一步 | — |
| 口癖去除后字幕变空 | 保留最小有意义的词组 | 保留原始文本并标记 `#unmodified` |
| 的/得/地修正后语法不通 | 回退到原始版本，标记 `#uncertain` | 保留原始，在 diff 中标记 ❗ |
| 术语表查找无匹配 | 回退到 AI 上下文猜测 | 标记为低置信度（50-69%）提交用户确认 |
| 联网 web search 失败（超时/无结果） | 跳过联网校准，使用本地术语表 | 标记该词为低置信度（50-69%），在 diff 中提示用户自行确认 |
| spacing 脚本执行失败 | 回退到纯 AI 混排处理 | 跳过混排步骤，记录警告 |
| 标点去除后字幕变空 | 保留原始文本的骨干部分 | 保留原始并标记 `#punctuation_removed_failed` |
| 游戏书名号标记过泛（误标工具名） | 撤销该条标记 | 保留不做书名号标记 |
| 单行合并后超过 40 字无法拆分（无语义断点） | 在空格/标点处硬拆分 | 保持现状，标记 `#overflow` |
| 用户拒绝所有修改 | 直接输出原始文件 | 输出原始文件并附加提示「已跳过所有修改」 |
| 增量术语表冲突（session 表与静态表不一致） | session 表优先 | 在 diff 中展示两条记录供用户选择 |

## Additional Resources

### Reference Files
- **`references/example.md`** - Complete worked example with input, processing steps, diff table, and output
- **`references/enhancement-rules.md`** - Detailed rules for filler word removal, typo detection, semantic analysis strategies, web-based ASR verification, confidence scoring, and incremental learning
- **`references/terminology.md`** - Maya and Python terminology mapping table for correcting ASR misrecognition of technical terms
- **`references/asr-corrections-gaming.md`** - Gaming industry (Rookies, Concept Art, etc.) ASR correction table
- **`references/mixed-typesetting.md`** - Complete specification for mixed-language typesetting (CJK-Latin spacing, protection zones, number formats, capitalization, game title marking, user configuration)

### Scripts
- **`scripts/apply_spacing.py`** - Deterministic CJK-Latin spacing tool. Run on subtitle text before AI review of protection zones and edge cases.

## Workflow Summary

To enhance an SRT or TXT file:

1. Receive the uploaded `.srt` or `.txt` file from the user
2. Parse the file structure (SRT: index + timestamp + text; TXT: plain paragraphs)
3. Auto-detect domain and load relevant terminology tables
4. For each subtitle/paragraph segment, apply in order:
   - Convert Traditional Chinese → Simplified Chinese
   - Remove filler words (口癖词)
   - Correct 的/得/地 usage based on syntactic position (定语→的, 状语→地, 补语→得)
   - Correct typos using terminology tables (session table > static references > web search > AI guess)
   - Calibrate suspected ASR errors via web search (low-confidence items flagged with ❗)
   - Apply mixed-language typesetting (CJK-Latin spacing, code/path protection, number-unit formatting, capitalization)
   - Remove punctuation (preserve 《》 and protection zones)
   - Mark known game/film titles with 《》book-title marks
   - Enforce single-line (SRT only)
5. Assign confidence scores to every modification
6. Present diff review table to the user for confirmation (include confidence %, change type)
7. Apply user-confirmed corrections
8. Save output as `enhanced.srt` or `enhanced.txt`
9. Remember user-verified corrections in session table for the remainder of the session

Focus on semantic understanding and conservative corrections. The goal is to clean up spoken-language artifacts while preserving the original meaning and structure of the subtitles. Use web search to verify uncertain ASR output, and always present a diff for user review before finalizing.
