# Srt-Enhancer 最终优化方案（定稿）

> 基于 `srt-enhancer-audit.md`（实测复现 P0×3）与《针对审计优化方案的分析》（二审复核）综合形成。已对 `SKILL.md 579行 / enhance.py 828行 / vertical.py 228行 / domain_scanner.py 64行 / title_marker.py 205行 / apply_spacing.py 186行 / casing_verify.py 228行 / correction-table.md 1067行 / domains.yaml 398行` 逐行核验。二审结论：审计核心发现可靠，但部分表述夸大、部分修复需重定义边界。本方案以二审为准，落地时以本文件为准。

## 现状判定

流水线 `normalize → terminology → spacing → capitalization → terminology → finalize` 本身成立，外围有 domain 检测、title 标记、vertical 竖屏。问题不在架构，而在**确定性层的静默失败与模块间 contract 缺失**。零自动化测试导致 P0 长期潜伏。本轮目标：不改变增强方向，只修静默丢内容、规则未生效、错误领域识别与术语不一致，并建立回归体系。

## 审计准确性校正

| 审计点 | 原结论 | 复核结果 |
|---|---|---|
| SKILL 640-706 附录 | 清洗算法附录缺失 | 夸大：SKILL 仅 579 行，无该附录，细节在 `enhancement-rules.md` |
| vertical 保真校验 | 仅分配前校验 | 准确但强度被夸大：`_norm` 去空格弱校验，空格增删可绕过 |
| casing_verify 引用常量 | 引用不存在常量致错 | 夸大：仅文案提示 `CAPITALIZATION_MAP/CASE_GROUPS` 与实名 `cap_map/case_groups` 不一致，未致 ImportError |
| 其余 P0-1/P0-3/P1-1/P1-3 等 | 实测复现 | 均准确 |

## 最终等级与处理方式

| ID | 问题 | 最终等级 | 处理方式 |
|---|---|---|---|
| **P0-1** | 中文去口癖对句中/句尾无效（`enhance.py:274-308`） | **P0** | 重写为三级语用检测，非简单去空格正则 |
| **P0-2** | `vertical.py:134-168` 短时长多 chunk 静默丢字 | **P0** | 分配后保真校验 + min_ms 柔性，失败回退整段 |
| **P0-3** | 领域感知大小写组全部塌缩 `generic`（`enhance.py:190-255`） | **P0** | 改按列解析，不依赖 2 组 regex |
| **P1-1** | `domain_scanner.py:35-40` 子串误判 `ue` 等 | **P1** | 英文按类型设边界，短缩写专项，非全局 `\b` |
| **P1-2** | `title_marker.py:186-205` 逐行+强 cue 窗口过小 | **P1/P2** | 先明确 deterministic/AI 契约，二阶段再扩全文上下文 |
| **P1-3** | `apply_spacing.py:38 vs 161` MultiViewReference 大小写分叉 | **P1** | 建 canonical source 统一两处 |
| **P2-1** | `enhance.py:146` 分隔行被当术语 | **P2** | 统一 Markdown table parser 跳过 `---|---` |
| **P2-2** | `casing_verify.py` 未被文档提及且文案过时 | **P2** | 确认维护用途后更新或删除 |
| **P2-3** | `enhance.py:13-19` docstring 缺 capitalization/二轮术语且编号跳 6 | **P2** | 同步 6 步 |
| **P2-4** | `DOMAIN_CASE_GROUPS_MAP:477-484` 缺 6 域回退 generic | **P2** | 补齐 6 域 |
| 测试 | 零单测 `find *test*` 仅 `test-prompts.json` | **基础设施** | 随每个 P0/P1 同步补，非最后集中补 |
| 联网校准 / references 内容质量 | 未实测 | **待验证** | 本轮不假设 |

## 执行顺序（测试先行）

```
Phase 0  测试骨架（与 P0 同步建）
  ├─ test_defiller.py
  ├─ test_vertical.py
  ├─ test_capitalization.py
  └─ test_domain_scanner.py
        ↓
Phase 1  P0 修复
  ├─ P0-3  capitalization 按列解析
  ├─ P0-2  vertical 完整性不变式
  └─ P0-1  三级 filler 检测
        ↓
Phase 2  P1 语义准确性
  ├─ P1-1  关键词类型化边界
  ├─ P1-3  canonical 术语源
  └─ P1-2  title_marker 契约明确
        ↓
Phase 3  Parser/文档健壮性
  ├─ P2-1  Markdown parser
  ├─ P2-3  docstring
  ├─ P2-4  补域映射
  └─ P2-2  casing_verify
        ↓
Phase 4  回归与联调
  └─  全链路语料回归 + video-transcribe 联调（连续无空格中文 SRT → enhance → vertical 保真）
```

## Phase 0 — 测试脚手架（先建）

采用 `修一个 bug 立即写回归`，非全部修完再补。

- `test_defiller.py`：矩阵 句首/句中/句尾/正常语义（`好吧/对吧/知道吗/怎么办呢/是啊` 必须保留）。断言宁可少删不误删。
- `test_vertical.py`：`1s×8chunk` 复现用例，断言 `normalize("".join(out)) == normalize(original)` 且 `out` 非空；`chunk×min_ms > total_dur` 时回退整段非丢后半。
- `test_capitalization.py`：断言 `case_groups` 含 `file_format/generic_acronym/os_term/brand_tool/ai_3d` 全量，非仅 `generic`。
- `test_domain_scanner.py`：含 `blue/value/issue/continue/true/argue/queue` 等的纯英文教学文本不得判 `unreal`。
- 后续：`test_title_marker.py / test_spacing.py / test_terminology.py / test_pipeline.py`

运行：`./venv/bin/python -m unittest discover -s scripts/tests -v` 需毫秒级，零外部依赖。

## Phase 1 — P0

### P0-3：领域感知大小写组解析

**根因**：`table_pattern = re.compile(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|")` 仅 2 组，`group(3)` 永 fall back `generic`；4 列表 `小写|标准|领域组|说明` 第 3 列被丢弃。

**方案**：不再依赖列数敏感的 regex capture，统一 `cells = [c.strip() for c in line.strip("|").split("|")]` 按列取：
- `专有名词大写(3列)`：`cells[0]=low, cells[1]=std`
- `领域感知(4列)`：`cells[0]=low, cells[1]=std, cells[2]=group`

同时支持未来扩列。验证 `case_groups.keys()` 含 5 组。

### P0-2：vertical 静默丢字

**根因**：保真仅在分配前做；`min_ms=300` 硬下限在 `chunks×min_ms > total_dur` 时使后段 `end==cursor` 被 `if end>cursor` 丢弃。`_norm` 去空格弱校验可绕过空格增删。

**不变式**：`文本完整性 > 时间合法性 > 最短时长偏好`。任何 split 不得静默丢字。

**方案**：
```
split_segment(seg, chunks, min_ms=300)
  ├─ 候选 chunks 数量 × min_ms ≤ total_dur → 正常按 min_ms 分配
  └─ 否则 → 按比例压缩 min_ms' = total_dur / len(chunks) 再分配
  → 时间合法性检查（start<end 且在原区间内且有序）
  → 分配后保真检查：normalize("".join(o["text"] for o in out)) == normalize(seg["text"])
  → 失败 → return [dict(seg)] 整段回退，不输出前半
```
需同时保留分配前快速 reject 与分配后最终 invariant 双重检查。提升为全局原则：所有增强允许“不增强”，不允许丢内容。

### P0-1：中文口癖清理

**根因**：仅处理 `^f` 与 `\s+f\s+`，中文无空格句中/句尾不生效；句尾仅 7 词且需前字为标点；`_is_discourse_marker` 整段回滚过度保守。

**分级策略**（非全局 replace）：
- **A 高置信独立口癖**：`嗯/呃/噢/唔/欸/哎/嘿` 等——句首/句中/句尾积极清理
- **B 语气词**：`啊/哦/嘛/吧/呢/啦/哈/哟/喔`——需位置+上下文（前字是否标点、是否句尾、后文是否衔接）
- **C 尾缀保护**：`好吧/是吧/对吧/怎么办呢/是啊/知道吗`——不得删

**流程**：`原始文本 → 识别 filler candidate → 位置判断 → 上下文判断 → 删除/保留 → 重新规范空白`。SKILL Purpose 口癖集合与代码集合强制一致。

**测试矩阵**已列于 Phase 0，新增中文连续无空格真实 ASR 用例（来自 video-transcribe 输出）。

## Phase 2 — P1

### P1-1：domain_scanner 边界

**根因**：`kw.lower() in text_lower` 子串，`ue` 命中 `value/issue/true` 等。

**方案**：关键词分型，非统一 `\b`：
- 普通英文单词 → `\bkw\b`
- 短英文缩写 ≤3（含 `ue/uv/sop/vop/dop/cop/rbd/hda/vdb/vex/goz`） → `(?<![A-Za-z])kw(?![A-Za-z])`（前后不能接字母，允许 `UE5/UE Engine`）
- 中文词（含 `可灵/蓝图/拓扑`）→ 保留子串或自定义中文边界
- 混合术语 → 按 token 结构处理

并对 `domains.yaml` 全量 ≤3 英文短词做 review，`P0-3` 修复后联动验收（域检测→大小写组激活）。

### P1-3：canonical 术语源

**根因**：`PROTECTION_PATTERNS` 护 `MultiViewReference`，`FIXUP_COMPOUNDS` 修 `MultiviewReference` 并存。

**方案**：建 `CANONICAL_COMPOUNDS = {"multiviewreference": "MultiViewReference", ...}`，`PROTECTION` 与 `FIXUP` 均由此派生。
```
CANONICAL_COMPOUNDS
   ├─ PROTECTION_PATTERNS
   ├─ FIXUP_COMPOUNDS
   ├─ capitalization
   └─ terminology
```
原则：一个术语唯一规范写法。

### P1-2：title_marker 契约

**现状**：`grep -v` 管线逐行 `mark_titles`，要求标题与 `GAME_CUES/FILM_CUES` 同行才加《》，跨行 `原神/游戏` 漏标；`KNOWN_TITLES` 148 项但强 cue 低召回。

**分两阶段**：
1. **本轮**：SKILL 明确 contract：`title_marker.py = deterministic first-pass 行级/高 precision 不保证 recall；AI systematic scan = document-level 补全最终 override`，避免误作独立诊断工具。
2. **后续**（视 AI 兜底负载）：重做为全文上下文 `完整 SRT → 建立上下文 → 识别 candidate → 定位 index → 只改对应字幕`，非简单 `_has_cue(full_text)` 全局替换。

## Phase 3 — P2

- **P2-1**：抽 `parse_markdown_table()` 统一处理 `header/separator/data/empty/escaped |`，跳过 `^[\s|:-]+$` 分隔行，`load_terminology` 与 `load_capitalization_table` 复用。
- **P2-3**：同步 `enhance.py:13-19` docstring 为 `normalize,terminology,spacing,capitalization,terminology,finalize + write` 6 步，与 `PIPELINE_STEPS`/`--steps`/`SKILL 表` 同源；考虑由 `PIPELINE_STEPS` 生成 help/docstring。
- **P2-4**：补 `DOMAIN_CASE_GROUPS_MAP` 缺失 6 域（`substance/blender/unreal/houdini/zbrush/photoshop`），或显式回退策略并在注释中说明。
- **P2-2**：核实 `casing_verify.py` 是否为维护者扩表工具：若在用，更新提示为“追加到 `correction-table.md` 大小写表格”并加入 SKILL Resources；若无调用，删除。

## Phase 4 — 全局不变式与联调

**Enhancer 契约**：
```
Enhance(input) = 合法 SRT + 允许的文本变换（口癖删除/术语标准化） + 不丢内容 + 不造新术语 + 不破时间轴
```

**Validation 层**（pipeline 末）：
- 内容完整性：非逐字符相等，但结构性内容受 `normalize` 保真与 segment 数量守恒约束；vertical 专检
- 时间完整性：`start<end, start≥orig.start, end≤orig.end, 有序, 无异常重叠`
- 数量守恒：异常不致字幕消失

**联调**：与 `video-transcribe` 已修复版本做 integration test：连续无空格中文 SRT → enhancer → vertical，验文本/术语/时间轴/vertical 保真。

## 验收标准

- `test_defiller` 中文矩阵通过且 `好吧/对吧` 等保护用例不误删
- `test_vertical` 1s×8chunk 不丢字，分配后保真 invariant 常驻
- `case_groups.keys()` 含 5 领域组
- `domain_scanner` 含 `value/issue` 的英文文本不判 `unreal`
- `MultiViewReference` 两路径一致
- 全量单测 + 联调语料回归通过
- `SKILL.md/README/CLI help/docstring` 四处流水线描述同源

## 不在本轮

- 联网 Web 校准真实效果与 `references` 条目详实度逐条复核（需联网与语料 review）
- 大规模语料人工精校对比
