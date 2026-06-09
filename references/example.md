# SRT Enhancement Example

**Input SRT**:
```
1
00:00:00,000 --> 00:00:05,000
嗯今天要介紹Python3.9的新功能

2
00:00:05,000 --> 00:00:10,000
首先就是就是match case語句這是一個強大的模式匹配工俱

3
00:00:10,000 --> 00:00:15,000
我我我們來看看啊啊這個功能Owatch得的Concept2

4
00:00:15,000 --> 00:00:20,000
玩黑神话：悟空的時后一定要装GPU驱动

5
00:00:20,000 --> 00:00:25,000
他3个场景做的非常好一个5G的纹理包
```

**Processing**:
1. **繁转简**: 介紹 → 介绍, 語句 → 语句, 時后 → 时候
2. **领域检测**: 检测到 Python + Gaming 领域
3. **去口癖**: 嗯/啊啊
4. **的/得/地**: `得` → `的`（"Owatch 的 Concept2" 是所属关系，定语需用"的"）
5. **术语修正**: 工俱 → 工具（对照表匹配）, Concept2 → Concept Art（对照表匹配）
6. **联网校准**: `Owatch` → 搜索 `Owatch game` → 确认正确写法为 `Overwatch`（高置信度）
7. **中英文混排**: `Python3.9` → `Python 3.9`, `5G的纹理包` → `5GB 纹理包`（数字单位紧凑 + CJK-Latin 空格）
8. **标点去除**: 移除中文标点（保留《》书名字）
9. **书名号**: `黑神话：悟空` → 《黑神话：悟空》

**Diff Review Table**:

| # | 原文 | 修改后 | 置信度 | 类型 |
|---|------|--------|--------|------|
| 1 | 嗯今天要介紹 | 今天要介绍 | 高(95%) | 去口癖+繁转简 |
| 2 | 首先就是就是 match case 語句 | 首先就是 match case 语句 | 高(90%) | 去口癖(就是)+繁转简 |
| 2 | 模式匹配工俱 | 模式匹配工具 | 高(100%) | 错别字(术语表) |
| 3 | 我們來看看啊啊 | 我们来看看 | 高(95%) | 去口癖+繁转简 |
| 3 | Owatch | Overwatch | 高(90%) | 联网校准 |
| 3 | Concept2 | Concept Art | 高(100%) | 术语修正(游戏行业) |
| 3 | Owatch 得 的 Concept2 | Owatch 的 Concept Art | 高(95%) | 的/得/地修正 |
| 4 | 黑神话：悟空 | 《黑神话：悟空》 | 高(100%) | 书名号标记 |
| 4 | GPU驱动 | GPU 驱动 | 高(95%) | 混排空格 |
| 5 | 5G的纹理包 | 5GB 纹理包 | 高(90%) | 单位规范+空格 |

**Output SRT (`enhanced.srt`)**:
```
1
00:00:00,000 --> 00:00:05,000
今天要介绍 Python 3.9 的新功能

2
00:00:05,000 --> 00:00:10,000
首先就是 match case 语句这是一个强大的模式匹配工具

3
00:00:10,000 --> 00:00:15,000
我们来看看这个功能 Overwatch 的 Concept Art

4
00:00:15,000 --> 00:00:20,000
玩《黑神话：悟空》的时候一定要装 GPU 驱动

5
00:00:20,000 --> 00:00:25,000
他 3 个场景做得非常好一个 5GB 的纹理包
```

**Changes Made**:
- **Subtitle 1**: Removed filler `嗯`, 繁转简 `介紹` → `介绍`, CJK-Latin spacing: `Python3.9` → `Python 3.9`
- **Subtitle 2**: Removed filler `就是`, corrected `工俱` → `工具`, 繁转简 `語句` → `语句`
- **Subtitle 3**: Removed filler `啊啊`, 繁转简 `我們` → `我们`, web-calibrated `Owatch` → `Overwatch`, corrected `Concept2` → `Concept Art`, 的/得/地: `得` → `的`
- **Subtitle 4**: 书名号 `黑神话：悟空` → 《黑神话：悟空》, 繁转简 `時后` → `时候`, CJK-Latin spacing: `GPU驱动` → `GPU 驱动`
- **Subtitle 5**: 的/得/地: `做的` → `做得`, Unit formatting: `5G` → `5GB`, CJK-Latin spacing: `他3个` → `他 3 个`, `5GB的` → `5GB 的`
- All timestamps and numbering preserved
