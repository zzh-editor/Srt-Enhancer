# SRT Enhancement Example

## Minimal Example

**Input:**
```srt
1
00:00:00,100 --> 00:00:05,000
嗯今天我们要看一下Python3.9的新功能啊
```

**Processing:**
1. Detect `zh` and Python domain; resolve only candidate terminology from the local table lookup.
2. Run `enhance.py --lang zh --domain python --steps normalize,terminology,spacing,capitalization,terminology,finalize`.
3. Review title marking and the diff; wait for user approval before writing.

**Output:** `input_Enhancer.srt`; removes fillers, fixes 的/得/地 and ratios, normalizes Python terms, spacing and casing, applies the second terminology pass, then punctuation and hotkey normalization.

See the full worked example below for a multi-cue input, diff table and output.

**Input SRT**:
```
1
00:00:00,000 --> 00:00:05,000
嗯今天要介绍Python3.9的新功能

2
00:00:05,000 --> 00:00:10,000
首先就是就是match case语句这是一个强大的模式匹配工俱

3
00:00:10,000 --> 00:00:15,000
我我们来看看啊啊这个功能Owatch得的Concept2

4
00:00:15,000 --> 00:00:20,000
玩黑神话：悟空的时候一定要装GPU驱动

5
00:00:20,000 --> 00:00:25,000
他3个场景做的非常好一个5G的纹理包
```

**实际输出**（2026-11-25 用 `python3 scripts/enhance.py in.srt -o out.srt --lang zh --domain python --overrides '{"Owatch":"Overwatch"}'` 实测）:

```
1
00:00:00,000 --> 00:00:05,000
今天要介绍 Python3.9 的新功能

2
00:00:05,000 --> 00:00:10,000
首先就是就是 match case 语句这是一个强大的模式匹配工俱

3
00:00:10,000 --> 00:00:15,000
我我们来看看这个功能 Overwatch 得的 Concept Art

4
00:00:15,000 --> 00:00:20,000
玩黑神话 悟空的时候一定要装 GPU 驱动

5
00:00:20,000 --> 00:00:25,000
他 3 个场景做的非常好一个 5G 的纹理包
```

**脚本实际做了什么**（其余一律不动）:

| 项 | 结果 |
|---|---|
| 去口癖 | 去掉句首「嗯」「啊啊」；`我我们`、`就是就是` 这类叠词不处理 |
| 中英混排 | CJK 与拉丁字母之间加空格；`Python3.9` 词内数字不加空格 |
| 术语 | `Owatch → Overwatch`（`--overrides`）、`Concept2 → Concept Art`（对照表命中） |
| 标点 | 中文标点被移除：`黑神话：悟空 → 黑神话 悟空` |
| 书名号 | 不自动加；`title_marker.py` 只在本条命中作品名时处理，本例未命中 |
| 的/得/地 | `得的` 不在规则内，保持原样 |
| 对照表未收录 | `工俱`、`5G→5GB`、`他3个` 的数量单位均不处理 |

**模型仍需在 diff 审核阶段补的**：`工俱 → 工具`（无表项，凭上下文低置信度提出）、`5G → 5GB`（单位规范要人确认）、`我我们 → 我们`、`得的 → 的`。这些若写进 SRT 必须走审批，不能当成脚本已完成的步骤。

**约束提醒**：以上输出与原稿的条目数、编号、时间轴逐条一致；时间戳永不由本流水线改动。
