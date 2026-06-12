# Enhancement Rules

This document provides detailed rules for enhancing SRT subtitles, including filler word removal, typo correction, and semantic analysis strategies.

**Note**: This version does not depend on any reference document (`origin.md`). All enhancements are applied based on linguistic rules and AI contextual analysis.

---

## 1. Filler Word Removal (口癖词去除)

### 1.1 Categories of Filler Words

#### Hesitation Sounds (犹豫声)
These are vocal hesitations with no lexical meaning — always remove.

| Filler | Example Before | Example After |
|--------|---------------|---------------|
| 啊 | 我啊觉得 | 我觉得 |
| 哦 | 这个哦问题 | 这个问题 |
| 嗯 | 嗯今天我们 | 今天我们 |
| 呃 | 那个呃东西 | 那个东西 |
| 哎 | 哎你知道吗 | 你知道吗 |
| 噢 | 噢对了 | 对了 |
| 唔 | 唔我想想 | 我想想 |
| 欸 | 欸不对 | 不对 |
| 嘿 | 嘿你知道吗 | 你知道吗 |

#### Meaningless Sentence-Final Particles (无意义句末语气词)
Remove when they don't carry grammatical or emotional meaning.

| Filler | Remove? | Example |
|--------|---------|---------|
| 嘛 | Usually yes | 就是嘛 → 就是 |
| 啦 | Usually yes | 好啦 → 好 |
| 哈 | Usually yes | 对哈 → 对 |
| 哟 | Usually yes | 快哟 → 快 |
| 喔 | Usually yes | 是喔 → 是 |
| 呢 | Context-dependent | See rules below |
| 吧 | Context-dependent | See rules below |

#### Filler Phrases (口头禅短语)
Common spoken filler phrases that add no meaning:

| Filler Phrase | Example Before | Example After |
|--------------|---------------|---------------|
| 那个 | 我觉得那个就是说 | 我觉得就是说 |
| 就是说 | 就是说我想要 | 我想要 |
| 你知道吗 | 你知道吗这个 | 这个 |
| 怎么说呢 | 怎么说呢这个功能 | 这个功能 |
| 就是说 | 就是说我们可以 | 我们可以 |

**不要视为口癖** — 以下属于自然话语标记（Discourse Markers），是中文口语中的惯用连接和过渡手段，不应删减：
- **也就是说、然后**（表承接/递进）、**那么、那**（句首引入话题）
- **说白了**（换言标记）、**对吧**（确认标记）、**好吧**（让步标记）
- **的话**（话题标记，如"技术美术的话"）

### 1.2 Removal Rules

#### Rule 1: Standalone Filler Removal
When a filler word appears alone (not part of a meaningful word), remove it entirely.

```
Before: 嗯 我觉得这个很好
After:  我觉得这个很好
```

#### Rule 2: Mid-Sentence Filler Removal
When a filler is between two words, remove it and ensure no double spaces remain.

```
Before: 我啊觉得这个很好
After:  我觉得这个很好
```

#### Rule 3: Consecutive Filler Removal
When multiple fillers appear together, remove all of them.

```
Before: 嗯啊那个就是说
After:  (empty — remove entire segment if no meaningful content)
```

#### Rule 4: Filler Before Punctuation
When a filler appears right before punctuation, remove both the filler and adjust spacing.

```
Before: 这个功能很好啊，对吧
After:  这个功能很好，对吧
```

#### Rule 5: Preserve Meaningful Particles
**DO NOT remove** particles that carry grammatical meaning:

- **吗** (question particle): 你去吗？ → Keep
- **的** (possessive/descriptive): 我的 → Keep
- **了** (completed action): 吃了 → Keep
- **呢** when used for questions: 怎么了呢？ → Keep
- **吧** when indicating suggestion: 我们走吧 → Keep
- **呢** when used for comparison: 比昨天好呢 → Keep

#### Rule 6: Never Delete Meaningful Lexical Words

**绝对不删减以下类别——它们是句子的语法或语义组成部分，不是口癖：**

| 类别 | 说明 | 示例 | 不删原因 |
|------|------|------|----------|
| 数量词 | 表示数量、程度 | `一些`、`一个`、`很多`、`一些比较` | 提供数量信息 |
| 人称代词 | 指代人物 | `我`、`你`、`他`、`我们`、`大家` | 句子主语/宾语 |
| 口语动词搭配 | 口语化的动词组合 | `来一个`、`去做`、`给说`、`搞一个` | 体现口语风格 |
| 程度副词 | 修饰程度 | `比较`、`非常`、`很`、`太`、`特别` | 表达程度差异 |
| 结构助词 | 连接修饰语 | `的`、`地`（状语）、`得`（补语） | 语法必需 |
| 时态助词 | 表示时态 | `了`、`着`、`过` | 表达动作状态 |
| 量词短语 | 单位量词 | `一张`、`一个`（高手/画面/古风）、`一种`、`一些`、`一层` | 搭配名词使用 |
| 指示代词 | 指代事物 | `这个`、`那个`、`这些`、`那些`、`这种` | 明确指代关系 |

**常见误判风险** — 以下容易被误判为冗余，实则有语法作用：
- `每屏是不是都是龙曲花点啊`中的"啊" → 句末语气词，赋予句子轻松口语色彩，但与犹豫声"啊"不同，需根据语境判断
- `就是你有中国建筑`中的"就是" → 强调标记，不同于口头禅填充词
- `那这个`、"那这一"中的"那" → 话语标记，引出新话题

**核心原则：如果删除后句子变得不自然、缺失信息、或改变说话者语气，就不要删。**

### 1.3 Context-Aware Decisions

Use AI to determine whether a word is a filler or meaningful:

1. **Position in sentence**: Fillers typically appear at sentence boundaries
2. **Surrounding context**: If removing the word doesn't change meaning, it's a filler
3. **Speech pattern**: Repeated usage of the same sound suggests filler
4. **Sentence completeness**: If the sentence is complete without it, remove it

### 1.4 Examples

#### Example 1: Simple Filler Removal
```
Before: 嗯今天我们来聊聊Python
After:  今天我们来聊聊 Python
```

#### Example 2: Multiple Fillers
```
Before: 嗯啊就是说这个功能很好用
After:  这个功能很好用
```

#### Example 3: Preserve Meaningful Particle
```
Before: 你去过北京吗？
After:  你去过北京吗？  (吗 is a question particle — keep it)
```

#### Example 4: Filler in Middle of Sentence
```
Before: 我们需要哦一个更好的方案
After:  我们需要一个更好的方案
```

#### Example 5: Filler Phrase Removal
```
Before: 就是说我们可以用Python来写
After:  我们可以用 Python 来写
```

---

## 2. Typo Detection and Terminology Correction

### 2.1 Common Transcription Errors

#### Homophone Errors (同音字错误)
- 的/得/地 confusion（ASR 最常误识，根据句法位置修正）：

  **Critical ASR behavior**: ASR models default to outputting "的" for weak syllables, causing it to appear far more frequently than correct Chinese text. Every encounter of "的" must be syntactically examined.

  **Decision Tree**:
  - Word after is a noun/noun phrase → **的** (定语/所属标记)：美丽的花、我的书、新的功能
  - Word after is a verb phrase AND modifies how the action is done → **地** (状语标记)：慢慢地走、认真地学、反复地调
  - Word before is a verb/adj AND word after is degree/result/state → **得** (补语标记)：跑得快、做得好、气得跳、画得非常漂亮

  **High-Frequency Fixed Patterns**:
  | Pattern | Correct | Example |
  |---------|---------|---------|
  | 变得、懂得、觉得、记得、显得 | 得 | 变得更好、懂得很多 |
  | 值得、免得、取得、获得 | 得 | 值得一试、取得进展 |
  | V/A + 得 + 程度补语 | 得 | 做得很好、累得要命、画得漂亮 |
  | 慢慢地、认真地、反复地、自动地 | 地 | 慢慢地走、认真地学 |
  | 定语"的" (不变) | 的 | 我的书、新的功能、之前的效果 |

  **Common ASR Misrecognition Table**:
  | ASR Output | Correct | Clue |
  |-----------|---------|------|
  | 做的非常好 | 做得非常好 | "做"+得+程度补语 |
  | 慢慢走 | （不变） | "慢慢"本身就是副词 |
  | 累的够呛 | 累得够呛 | 形容词+得+程度 |
  | 变的更好 | 变得更好 | 固定搭配"变得" |
  | 学的很快 | 学得很快 | 动词+得+程度 |
  | 跑的快 | 跑得快 | 补语结构 |
  | 懂的 | 懂得 (verb) / 懂的 (det.) | 需上下文判断 |
- 在/再 confusion
- 做/作 confusion
- 他/她/它 confusion
- 打上来/答上来（如"如果你能打上来"→"如果你能答上来"）

#### Similar Character Errors (形近字错误)
- 工具/工俱
- 功能/公能
- 設定/設訂
- 模型/模形

#### ASR Misrecognition of Technical Terms (语音识别术语错误)
ASR 经常将专业术语误识别为发音相似的常见词。使用 `references/terminology.md` 术语对照表进行修正。

常见模式：
- Maya → `make`, `mayor`, `maya` (小写)
- Python → `bison`, `pie thon`, `path on`
- Maya 命令 → `poly cube` → `polyCube`, `group` → `group`
- Python 术语 → `pandas` → `pandas`, `numpy` → `numpy`

#### Missing Characters (漏字)
- Dropped particles (的, 了, 著)
- Incomplete words
- Truncated phrases

#### Extra Characters (多余字符)
- Transcription artifacts

### 2.2 Correction Strategy

1. **Identify Error**: Use AI to detect potential typos based on context
2. **Check Terminology Table**: Consult `references/terminology.md` for known ASR misrecognition patterns
3. **Verify Error**: Confirm it's a typo, not intentional variation or dialect
4. **Apply Correction**: Replace with the correct form from terminology table or context
5. **Validate Context**: Ensure correction makes sense in subtitle context

### 2.3 Conservative Approach

When uncertain:
- Preserve original text
- Don't force corrections
- Only correct clear errors
- Maintain speaker's voice and style

---

## 3. Punctuation Removal (标点符号去除)

### 3.1 Scope

Remove all Chinese and English punctuation marks from subtitle text.

**Chinese punctuation to remove:**
，。！？、；：""''【】（）—…·～

**English punctuation to remove:**
,!?;:'"()[]{}<>/-_=+|\\@#$%^&*~`

**Preserved:**
- `.` (dot) — appears in filenames like `Visuals.py` and technical identifiers
- `《》` (U+300A/U+300B) — book-title marks added by game/film title marking step are preserved

### 3.2 Rules

1. Remove all listed punctuation characters from subtitle text lines
2. **Never** modify timestamps — timestamps contain `:` and `,` which must be preserved
3. Apply punctuation removal **after** mixed-language typesetting, **before** game title marking
4. Do not remove punctuation inside protection zones (code, math, paths, URLs)
5. If removing punctuation results in an empty line, keep the original text

### 3.3 Examples

| Before | After |
|--------|-------|
| 去优化一下，做一些功能 | 去优化一下做一些功能 |
| 这个功能很好，对吧 | 这个功能很好对吧 |
| 我们需要 A=myClass | 我们需要 A=myClass |
| 使用 Python 3.9 版本 | 使用 Python 3.9 版本 |

---

## 4. Proper Noun and Terminology Handling

### 4.1 Categories of Proper Nouns

1. **Personal Names**: 李明, Steve Jobs, 王小華
2. **Company/Organization Names**: Google, Microsoft, WHO
3. **Product Names**: Python, Docker, iPhone, GitHub
4. **Technical Terms**: JavaScript, API, REST, GraphQL
5. **Place Names**: 台北, New York, Singapore

### 4.2 Standardization Rules

1. **Capitalization**: Follow standard conventions (iPhone, macOS, GitHub)
2. **Spacing**: Add spaces around English proper nouns in Chinese text
3. **Consistency**: Use the same form throughout (不要 Python/python 混用)

### 4.3 Application Strategy

1. Identify proper nouns and technical terms in each subtitle
2. Verify correct spelling and capitalization
3. Apply consistent formatting throughout the file
4. Add proper spacing around English terms

---

## 5. Semantic Analysis Guidelines

### 5.1 Context Understanding

When analyzing subtitle content:
- Consider the surrounding subtitles for context
- Identify the topic and domain
- Account for spoken language patterns
- Distinguish between fillers and meaningful content

### 5.2 Decision Framework

For each potential enhancement:

1. **Filler word?** → Will the sentence remain complete and natural without it? → Remove
2. **Typo?** → Is it clearly wrong based on context or terminology table? → Correct

### 5.3 Edge Cases

#### Ambiguous Fillers
- "然后" can be a meaningful connector or a filler — use context
- "就是" can be emphatic or a filler — use context
- "那个" can refer to something specific or be a filler — use context

#### Dialectal Variations
- Don't "correct" dialect-specific expressions
- Preserve regional speech patterns
- Only fix clear ASR transcription errors

#### Technical Content
- Be extra careful with technical terms
- Preserve exact technical terminology

---

## 6. Quality Assurance

### Pre-Enhancement Checks

- [ ] SRT file is valid and parseable
- [ ] File uses consistent encoding (UTF-8)
- [ ] Timestamps are properly formatted

### During Enhancement

- [ ] Each filler removal preserves sentence meaning
- [ ] Timestamps remain unchanged
- [ ] Subtitle numbering preserved
- [ ] No content added that wasn't in original

### Post-Enhancement Validation

- [ ] Output file is `{源文件名}_Enhancer.srt` 或 `{源文件名}_Enhancer.txt`
- [ ] Subtitle count matches original
- [ ] All timestamps identical to original
- [ ] No double spaces introduced
- [ ] English/numbers have proper spacing
- [ ] No semantic meaning changed
- [ ] SRT format is valid
- [ ] No empty subtitle blocks (unless original was empty)

---

## 7. Comprehensive Examples

### Example 1: Full Enhancement Pipeline

**Input**:
```
1
00:00:00,000 --> 00:00:05,000
嗯啊今天我们来聊聊Python3.9的新功能

2
00:00:05,000 --> 00:00:10,000
首先就是就是match case語句這是一個強大的模式匹配工俱

3
00:00:10,000 --> 00:00:15,000
我我我們來看看啊啊這個功能怎麼用
```

**Output**:
```
1
00:00:00,000 --> 00:00:05,000
今天我们来聊聊 Python 3.9 的新功能

2
00:00:05,000 --> 00:00:10,000
首先就是 match case 語句,這是一個強大的模式匹配工具

3
00:00:10,000 --> 00:00:15,000
我們來看看這個功能怎麼用
```

**Changes**:
1. Removed fillers: 嗯, 啊, 啊啊
2. Corrected typo: 工俱 → 工具
3. Added spacing: Python 3.9, match case

### Example 2: Filler Phrase Context Handling

**Input**:
```
1
00:00:00,000 --> 00:00:05,000
关于就是说那个Python3.9的新功能
```

**Output**:
```
1
00:00:00,000 --> 00:00:05,000
关于Python 3.9的新功能
```

**Changes**: Removed filler phrases "就是说" and "那个", added CJK-Latin spacing.

### Example 3: Preserve Meaningful Content

**Input**:
```
1
00:00:00,000 --> 00:00:05,000
你有没有去过北京啊？
```

**Output**:
```
1
00:00:00,000 --> 00:00:05,000
你有没有去过北京啊？
```

**Changes**: None — "啊" here adds a casual tone to the question, not a pure filler. Context-dependent preservation.

---

## 8. Web-Based ASR Verification

### 8.1 When to Trigger a Web Search

Trigger a web search when:
- A proper noun (person/organization/product name) sounds plausible but isn't in terminology tables
- A technical term appears in an unusual form that could be an ASR hallucination
- A Chinese word makes no sense in context and resembles a homophone error
- A named entity appears with unusual capitalization or spacing
- Confidence in a term's correctness is below 70%

Do NOT trigger for:
- Common Chinese vocabulary (日常词汇不需要联网验证)
- Common English words in their standard form (`import`, `function`, `class`, `return`)
- Words that exactly match a terminology table entry
- Clear filler words or repeated characters

### 8.2 Search Strategy

```
1. Extract suspect term + 2-3 words surrounding context
2. Choose search query format:

   For English proper nouns:
     "suspect term" + domain keyword + "spelling"
     Example: "Owatch game company"

   For Chinese suspect terms:
     "suspect term" + domain + "正确写法" / "术语"
     Example: "R Center 美术学校"

   For technical terms:
     "suspect term" + "definition" / "documentation"
     Example: "Concept2 game art category"

3. Evaluate top 3 results:
   - Authoritative source confirms different spelling → use corrected form
   - Multiple plausible forms → flag as medium confidence for user
   - Search confirms current form → skip correction
```

### 8.3 Result Evaluation

| Search Outcome | Action | Confidence |
|---------------|--------|------------|
| Single authoritative result confirming correction | Apply correction | High (≥90%) |
| Multiple plausible results, one dominant | Apply dominant form, flag for review | Medium (75%) |
| No clear result or contradictory results | Skip correction, flag for user | Low (50%) |
| Search confirms current spelling is correct | Skip correction | High (95%) |

### 8.4 Caching

Cache search results in session memory to avoid redundant queries:
```
session_web_cache:
  "Owatch" → { result: "Overwatch", confidence: "high", timestamp: "..." }
  "R Center" → { result: "Art Center", confidence: "high", timestamp: "..." }
```

- Cache hits: Skip web search, use cached result
- Cache expires: Per-session only (no persistent storage)

---

## 9. Confidence Scoring

### 9.1 Scoring Framework

Every modification must be assigned a confidence score and a reason.

| Score Range | Label | Meaning |
|------------|-------|---------|
| ≥ 90% | High | Clear correction — terminology match, web-verified, or obvious typo |
| 70-89% | Medium | Likely correct but minor ambiguity — e.g., homophone in context |
| 50-69% | Low | Uncertain — flag for user review |
| < 50% | Skip | Don't apply; preserve original |

### 9.2 Score by Change Type

**Filler Word Removal:**
- Hesitation sounds (啊、哦、嗯、呃、哎、噢、唔、欸、嘿): 95%
- Sentence-final particles (嘛、啦、哈、哟、喔 at end): 85%
- Context-dependent particles (呢、吧): 70% — requires context analysis
- Filler phrases (就是说、你知道吗、怎么说呢): 80%
- `然后`/`就是`/`那个` as filler: 65% — could be meaningful connector

**Typo/Terminology Correction:**
- Exact match in terminology table: 100%
- Case mismatch in terminology table (e.g., `maya` → `Maya`): 95%
- Fuzzy match to table entry: 80%
- Homophone correction with context support: 75%
- Web-verified with authoritative source: 90-95%
- Web-verified with ambiguous results: 70%
- AI contextual guess without table or web: 55% — always flag

### 9.3 Flagging for Review

Any modification with confidence < 70% must be:
1. Marked with `❗` in the diff review table
2. Presented with the original text and suggested correction
3. Awaiting user approval before being applied

### 9.4 Aggregation

For subtitle blocks with multiple changes, present per-change confidence (not per-block):
```
#12: Owatch游戏行业Concept2比赛

Changes:
  Owatch → Overwatch  90% (联网校准)
  Concept2 → Concept Art  100% (术语修正)
```

---

## 10. Incremental Terminology Learning

### 10.1 Session Table

Maintain an in-memory session terminology table that is checked before any other reference:

```
Priority order when evaluating a term:
1. Session table (highest priority, user-confirmed this session)
2. Static references (terminology.md)
3. Web search cache (if previously searched)
4. Live web search (if confidence < 70% and not in cache)
5. AI contextual inference (lowest priority, flag for review)
```

### 10.2 Populating the Session Table

Entries are added to the session table from three sources:

1. **User-confirmed diff items**: When user accepts a correction in the diff review
2. **User manual entry**: User says `记住：XXX 的正确写法是 YYY`
3. **Web-verified with high confidence**: Auto-add with source = "web-verified"

### 10.3 Session Table Format

In-memory structure:
```
session_terms = {
  "owatch": {
    correct: "Overwatch",
    confidence: "web-verified",
    source: "user-confirmed",
    original: "Owatch",
    context: "...Owatch的Concept2..."
  },
  "rukie": {
    correct: "Rookies",
    confidence: "table-match",
    source: "terminology.md",
    original: "RUKIES"
  }
}
```

### 10.4 Matching Rules

- Case-insensitive matching for session table lookups
- Fuzzy prefix matching: "owatch" also matches "Owatch" and "OWATCH"
- Single-entry per root term (latest user-confirmed version wins)
- If user rejects a suggestion, mark it as `rejected` to avoid re-suggesting

### 10.5 User Commands

The user can control the session table via natural language:

| User says | Action |
|-----------|--------|
| `记住：XXX 的正确写法是 YYY` | Add manual entry |
| `XXX 不应该被改成 YYY` | Mark as rejected |
| `清除本次学习的术语` | Reset session table |
| `显示本次学习的术语` | Print session table contents |

---

## 11. Best Practices

1. **Be Conservative**: When in doubt, preserve original
2. **Context is Key**: Use surrounding content for validation
3. **Respect Speech Patterns**: Don't over-formalize spoken language
4. **Order Matters**: Apply filler removal → 的/得/地 fix → typo fix → web calibration → mixed typesetting → punctuation removal → game title marking
5. **Maintain Flow**: Ensure corrections don't disrupt reading rhythm
6. **Validate Output**: Ensure enhanced SRT is still valid and readable
7. **Search Judiciously**: Only web search when genuinely uncertain; don't waste queries on trivial cases
8. **Show Your Work**: Always present confidence scores and reasoning in the diff table
9. **Learn From Feedback**: Use the session table to avoid repeating corrections

## 12. Common Pitfalls to Avoid

1. **Over-Removal**: Removing words that carry meaning (e.g., removing all 的/了)
2. **Timestamp Modification**: Never change timing
3. **Ignoring Context**: Making changes based on isolated words
4. **Double Spaces**: Introducing spacing artifacts after filler removal
5. **Unnecessary Web Searches**: Searching for common words that don't need verification
6. **Applying Unconfirmed Changes**: Committing low-confidence corrections without user approval
7. **Ignoring Session Table**: Re-asking about terms the user already confirmed

Focus on improving readability while preserving the natural flow and structure of the original subtitles. Use web search as a precision tool — only when the AI's knowledge is genuinely uncertain. Always present a clear diff for user review, and learn from feedback to make the session progressively smoother.

混排规范详见 `references/mixed-typesetting.md`。
