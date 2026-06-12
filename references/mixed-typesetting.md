# Mixed-Language Typesetting Specification

Complete reference for applying consistent mixed-language typesetting in SRT/TXT subtitle output.

**Version**: 1.0.0
**Applied**: After ASR calibration, before punctuation removal

---

## 1. Overview

Mixed-language typesetting ensures consistent formatting when Chinese (Han) and Latin/RTL scripts appear in the same subtitle line. It covers:

- Script boundary spacing (CJK-Latin, CJK-digit)
- Protection zones (code, math, paths, URLs)
- Number and unit formatting (compact vs spaced)
- Proper noun capitalization heuristics
- Game/film title 《》 marking
- Sentence-level spacing

---

## 2. Script Boundary Spacing

### 2.1 General Rule

Insert a single ASCII space (U+0020) at any boundary between Han (CJK Unified Ideographs) and non-Han scripts.

**Scope of "Han" characters**:
- CJK Unified Ideographs (U+4E00–U+9FFF)
- CJK Unified Ideographs Extension A/B (U+3400–U+4DBF)
- CJK Compatibility Ideographs (U+F900–U+FAFF)
- CJK Radicals/Strokes (U+2E80–U+2EFF)

**Scope of "non-Han" adjacent characters**:
- Latin letters (A-Z, a-z)
- Digits (0-9)
- Greek/Cyrillic (U+0370–U+03FF etc.)
- Any script that is not CJK Han

### 2.2 Detailed Patterns

| Context | Before | After | Rule |
|---------|--------|-------|------|
| Latin → Han | `Python编程` | `Python 编程` | Add space after Latin |
| Han → Latin | `编程Python` | `编程 Python` | Add space before Latin |
| Digit → Han | `3个场景` | `3 个场景` | Add space after digit |
| Han → Digit | `场景3` | `场景 3` | Add space before digit |
| Acronym → Han | `GPU驱动` | `GPU 驱动` | Add space after acronym |
| Han → Acronym | `驱动GPU` | `驱动 GPU` | Add space before acronym |
| Latin → Digit | `Python3.9` | `Python 3.9` | Add space (word boundary) |
| Digit → Latin | `5GB` | `5GB` | Keep compact (unit, see §3) |
| Han → Latin → Han | `他说OK了` | `他说 OK 了` | Space before and after Latin |
| Version → Han | `v1.0版本` | `v1.0 版本` | Add space after version |

### 2.3 Same-Script Exceptions

No space added between characters of the same script:
- Latin-Latin: `GPU driver`, `match case`, `Unreal Engine`
- Han-Han: `编程语言`, `场景美术`, `黑神话：悟空`
- Digit-Digit: `3.9`, `1920`, `5.0`
- Han-Japanese Kana: `プログラミング言語` (in Chinese-dominant text: spaced; in Japanese-dominant text: same-script, no space)

### 2.4 Edge Cases

| Edge Case | Input | Output | Explanation |
|-----------|-------|--------|-------------|
| Empty line | `` | `` | No change |
| All Latin | `Hello World` | `Hello World` | No CJK boundaries |
| All Han | `你好世界` | `你好世界` | No non-CJK boundaries |
| Mixed punctuation | `你好,world.` | `你好, world.` | Space after comma before Latin |
| Multiple boundaries | `Python3.9新功能` | `Python 3.9 新功能` | Space at each boundary |
| Email addresses | `联系info@example.com` | `联系 info@example.com` | Space before email (email is protection zone) |
| Parenthetical | `Python(编程)` | `Python (编程)` | Space before parenthesis |

---

## 3. Protection Zones

### 3.1 Zone Types and Patterns

| Zone Type | Pattern | Example |
|-----------|---------|---------|
| Inline code | `` `code` `` | `` Use `print()` to output `` |
| Fenced code block | ```` ``` ``` ```` | ```` ```python\nprint("hello")\n``` ```` |
| Inline math | `$...$` | `Formula $E=mc^2$` |
| Display math | `$$...$$` | `$$\sum_{i=1}^n i$$` |
| LaTeX inline | `\(...\)` | `\(\alpha + \beta\)` |
| LaTeX display | `\[...\]` | `\[\int_0^\infty\]` |
| File path (Unix) | `/path/to/file` | `/usr/local/bin/python3` |
| File path (Windows) | `C:\path` | `C:\Users\name\file.py` |
| URL | `https://...` | `https://example.com/page` |
| Email | `user@host` | `foo@bar.com` |

### 3.2 Protection Algorithm

For each subtitle line:

1. **Scan** for protection zone boundaries using regex patterns
2. **Replace** each zone with a `__PROTECT_N__` placeholder and store the original
3. **Apply** spacing and punctuation rules on the placeholder-substituted string
4. **Restore** original content from placeholders

**Regex patterns** (pseudocode):
```
inline_code: `[^`]+`
fenced_code: ```[\s\S]*?```
inline_math: \$[^$]+?\$
display_math: \$\$[\s\S]*?\$\$
latex_inline: \\\([\s\S]*?\\\)
latex_display: \\\[[\s\S]*?\\\]
unix_path: \/[^\s,;:!?）)]+
windows_path: [A-Za-z]:\\[^\s,;:!?）)]+
url: https?:\/\/[^\s,;:!?）)]+
email: [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
```

### 3.3 Protection Priority

When zones overlap, inner zones take precedence:
- `` `print($x)` `` → inner `$x$` is a math zone, outer is code — protect both
- `` Path `/usr/local/$NAME` `` → `$NAME` is math (higher priority than path)

---

## 4. Number and Unit Formatting

### 4.1 Default: Compact Mode

| Type | Example |
|------|---------|
| Storage | `5GB`, `500MB`, `2TB` |
| Version | `v1.0`, `v2.3.1`, `v2026.0.1` |
| Resolution | `1920×1080`, `4K`, `8K` |
| FPS | `30fps`, `60fps`, `120fps` |
| Dimensions | `16:9`, `4:3` |
| Percentage | `50%`, `100%` |
| Temperature | `30°C`, `100°F` |
| Time | `3s`, `5min`, `2h` |

### 4.2 User Override: Spaced Mode

If user says `数字单位加空格`:

| Type | Before | After |
|------|--------|-------|
| Storage | `5GB` | `5 GB` |
| Version | `v1.0` | `v1.0` (unchanged — version always compact) |
| FPS | `30fps` | `30 fps` |
| Temperature | `30°C` | `30 °C` |

### 4.3 Priority: Compact Over Spacing

**Rule**: Number-unit compact formatting takes precedence over the general script-boundary spacing rule.

For example:
- `5GB`: The `5` (Digit) and `G` (Latin) boundary would normally get a space, but because `GB` is a recognized unit, the compact form wins → `5GB` (not `5 G B`)
- `v1.0`: Version numbers are always compact, even when adjacent to Han → `v1.0版本` (already compact before boundary spacing)
- `30fps` → `30fps` (compact), not `30 fps` unless user overrides with `数字单位加空格`

**User override**: `数字单位加空格` switches to spaced mode for non-version units (see §4.2).

### 4.4 Non-Unit Numbers

Numbers that are part of a word or identifier should NOT be split:
- `Python3.9` → `Python 3.9` (version boundary — this IS split because "Python" is a word)
- `polyCube4` → `polyCube 4` (identifier split)
- `4K` → `4K` (resolution standard, kept compact)
- `第3个` → `第 3 个` (ordinal, split per CJK-digit rule)
- `match case` → `match case` (no change, all Latin)

---

## 5. Capitalization Heuristics

### 5.1 Known Technical Acronyms

Always preserve/replace in uppercase:

GPU, CPU, API, SDK, AI, HTML, CSS, JS, TS, JSON, SQL, HTTP, REST, TCP, IP, USB, HDMI, SSD, HDD, RAM, VRAM, DNS, DHCP, FTP, SSH, SSL, TLS, PNG, JPEG, GIF, SVG, XML, YAML, TOML, CLI, GUI, UI, UX, IDE, DB, VM, OS, BIOS, PCIe

### 5.2 Brand Names

Standard capitalization from terminology table:
- `Unreal Engine`, `Unity`, `Maya`, `Blender`, `Photoshop`, `Visual Studio Code`
- `Visual Studio`, `Xcode`, `Android Studio`

### 5.3 CamelCase/PascalCase

Preserve original casing:
- `polyCube`, `pCube1`, `Keyframe`, `VertexBuffer`
- `RenderPipeline`, `ShaderGraph`, `MaterialInstance`

### 5.4 Terminology Table Override

Entries in `terminology.md` take priority over heuristics.

### 5.5 Lowercase Exceptions

Common English function words remain lowercase in Chinese context:
- Articles: `the`, `a`, `an`
- Prepositions: `in`, `on`, `at`, `for`, `to`, `with`, `by`, `of`, `from`
- Conjunctions: `and`, `or`, `but`, `if`, `so`

---

## 6. Game/Media Title Marking

### 6.1 Scope

Add 《》（U+300A/U+300B）only for confirmed game/film/TV series titles. Do NOT add for engines, tools, companies, platforms, or other proper nouns.

### 6.2 Curated Title List

Known game titles (examples):
- 黑神话：悟空, 对马岛之魂, 最后生还者, 战神, 塞尔达传说, 原神, 王者荣耀, 英雄联盟, 绝地求生, 堡垒之夜, 使命召唤, 艾尔登法环, 巫师3, 荒野大镖客, 赛博朋克2077, 最终幻想, 生化危机, 只狼, 黑暗之魂

Known film titles (examples):
- 流浪地球, 哪吒, 战狼, 长津湖, 你好李焕英, 满江红, 孤注一掷, 消失的她

### 6.3 Context Cues for Detection

Increase likelihood of game/film title when adjacent to:
- Gaming verbs: 玩(游戏), 打(游戏), 通关, 下载(游戏)
- Film verbs: 看(电影), 上映, 票房
- Review language: 推荐, 评测, 测评

### 6.4 Negative Examples (no 《》)

- **Engines**: `Unreal Engine 5`, `Unity 6`, `CryEngine`
- **Tools**: `Photoshop`, `Substance Painter`, `Maya`, `Blender`, `ZBrush`
- **Companies**: `Bungie`, `Epic Games`, `NVIDIA`, `AMD`, `Intel`, `Microsoft`
- **Platforms**: `Steam`, `PS5`, `Xbox`, `Nintendo Switch`, `Epic Games Store`
- **Technologies**: `DirectX 12`, `Vulkan`, `OpenGL`, `CUDA`, `RTX`

---

## 7. Sentence-Level Spacing

Preserve single space after sentence-ending punctuation when the next character is from a different script:

| Input | Output |
|-------|--------|
| `look at this.下一个` | `look at this. 下一个` |
| `就是这个。Then` | `就是这个。 Then` |
| `Hello world.你好` | `Hello world. 你好` |
| `等一下。Next` | `等一下。 Next` |

Sentence-ending punctuation: `.`, `。`, `!`, `！`, `?`, `？`

---

## 8. Pipeline Integration

### 8.1 Position in Enhancement Order

Mixed-language typesetting is step 7 in the pipeline:
1. 领域检测
2. 去口癖
3. 空格清理
4. 的/得/地修正
5. 术语修正
6. ASR联网校准
7. **混排规范** ← here
8. 标点去除
9. 书名号标记
10. 单行强制
11. 置信度评分 + Diff输出
12. 输出生成

### 8.2 Interaction with Other Steps

- **After ASR calibration** (step 6): Typesetting works on already-corrected text
- **Before punctuation removal** (step 8): Spacing decisions are made first, then punctuation is cleaned up
- **Protection zones survive punctuation removal**: Code, math, paths, URLs are preserved through both steps
- **Game title marking (step 9)**: Game/film title 《》 is added AFTER punctuation removal, so it won't be deleted. The title detection logic (identifying potential titles) runs during the mixed typesetting step, but the actual insertion of 《》 is deferred to step 9.

---

## 9. User Configuration

### 9.1 Commands

| Command | Effect |
|---------|--------|
| `中日文之间不加空格` | Disable all CJK-Latin spacing |
| `数字单位加空格` | Switch to spaced number-unit format |
| `保护代码块` | Enable code protection (default: on) |
| `禁用代码保护` | Disable code protection (not recommended) |
| `显示混排配置` | Show current typesetting configuration |
| `重置混排配置` | Reset to default settings |
| `版本号紧凑` | Keep version numbers compact (default) |
| `显示混排详情` | Show per-subtitle typesetting changes in diff |

### 9.2 Default Configuration

```jsonc
{
  "cjk_latin_spacing": true,
  "number_unit_compact": true,
  "version_compact": true,
  "code_protection": true,
  "math_protection": true,
  "path_protection": true,
  "url_protection": true,
  "game_title_marking": true,
  "capitalization": true,
  "sentence_spacing": true
}
```
