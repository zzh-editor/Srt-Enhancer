# Maya & Python 术语对照表

本对照表用于修正 ASR（语音识别）对 Maya 和 Python 专业术语的误识别。在优化字幕时，应结合此表修正字幕中的术语错误。

> **匹配规则**：大小写敏感。只修正明确的 ASR 误识别（如 `make` → `Maya`），不影响普通英文单词的原有大小写。

---

## 1. Maya 术语

### 1.1 软件名称

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| make | Maya | 发音相似（注意：不匹配代码中的 My 前缀变量名） |
| mayor | Maya | 发音相似 |
| maya | Maya | 大小写修正 |

### 1.2 Maya 界面与操作

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| hyper graph | Hypergraph | 超级图表 |
| hyper shade | Hypershade | 材质编辑器 |

### 1.3 Maya 建模命令

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| poly cube | polyCube | 多边形立方体 |
| poly sphere | polySphere | 多边形球体 |
| poly cylinder | polyCylinder | 多边形圆柱体 |
| poly cone | polyCone | 多边形圆锥体 |
| poly torus | polyTorus | 多边形圆环 |
| poly plane | polyPlane | 多边形平面 |

### 1.4 Maya 动画术语

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| key frame | Keyframe | 关键帧 |
| set key | Set Key | 设置关键帧 |
| play blast | Playblast | 播放预览 |
| blend shape | Blend Shape | 混合变形 |
| skin cluster | Skin Cluster | 蒙皮簇 |
| bind skin | Bind Skin | 绑定蒙皮 |
| paint weights | Paint Weights | 绘制权重 |
| ik solver | IK Solver | IK 求解器 |
| parent constraint | Parent Constraint | 父级约束 |
| point constraint | Point Constraint | 点约束 |
| orient constraint | Orient Constraint | 方向约束 |
| aim constraint | Aim Constraint | 目标约束 |

### 1.5 Maya 材质与渲染

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| ai standard | aiStandard | Arnold 标准材质 |
| standard surface | Standard Surface | 标准曲面 |
| render view | Render View | 渲染视图 |
| render settings | Render Settings | 渲染设置 |
| batch render | Batch Render | 批量渲染 |
| directional light | Directional Light | 平行光 |
| point light | Point Light | 点光源 |
| spot light | Spot Light | 聚光灯 |
| area light | Area Light | 面光源 |
| ambient light | Ambient Light | 环境光 |

### 1.6 Maya Rigging 术语

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| ik handle | IK Handle | IK 手柄 |
| pole vector | Pole Vector | 极向量 |
| nurbs curve | NURBS Curve | NURBS 曲线 |
| ik rp solver | ikRPsolver | IK 旋转平面求解器 |
| ik sc solver | ikSCSolver | IK 单链求解器 |
| driven key | Driven Key | 驱动关键帧 |
| set driven key | Set Driven Key | 设置驱动关键帧 |
| connection editor | Connection Editor | 连接编辑器 |
| utility node | Utility Node | 工具节点 |

---

## 2. Python 术语

### 2.1 语言名称

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| bison | Python | 发音相似 |
| pie thon | Python | 发音相似 |
| piethon | Python | 发音不完整 |
| path on | Python | 发音相似 |

### 2.2 Python GUI (Qt/PySide)

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| py side | PySide | Qt for Python |
| py side 6 | PySide6 | Qt 6 for Python |
| py qt | PyQt | Qt 绑定 |
| h box layout | QHBoxLayout | 水平布局 |
| v box layout | QVBoxLayout | 垂直布局 |
| grid layout | QGridLayout | 网格布局 |
| data class | dataclass | 数据类 |

---

## 3. 通用编程术语

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| github | GitHub | 代码托管平台 |
| pull request | Pull Request | 拉取请求 |
| stack trace | Stack Trace | 堆栈跟踪 |
| command line | Command Line | 命令行 |
| file path | File Path | 文件路径 |

---

## 4. Rigging / 绑定技术术语

### 4.1 骨骼与权重

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| hyperjoins | helper joints | 辅助骨骼/辅助关节，用于改善变形效果 |
| join | joint | 骨骼/关节，常见拼写错误 |
| helper jointts | helper joints | helper joints 的拼写错误 |
| jointt | joint | joint 的拼写错误（多了一个 t） |
| jointt1 | joint1 | joint1 的拼写错误 |
| jointt2 | joint2 | joint2 的拼写错误 |
| jointt3 | joint3 | joint3 的拼写错误 |
| jointt4 | joint4 | joint4 的拼写错误 |
| join1 | joint1 | joint1 的拼写错误（少了 int） |
| join2 | joint2 | joint2 的拼写错误（少了 int） |
| join3 | joint3 | joint3 的拼写错误（少了 int） |
| mcnewjointt | mcn.newjoint | 代码符号丢失，应为 mcn.newjoint |
| ascend swap | ancestor swap | 祖先交换，将缺失骨骼的权重分配给其父级骨骼 |
| sensor swap | ancestor swap | ancestor 被误识别为 sensor |
| uncensored swap | ancestor swap | ancestor 被误识别为 uncensored |
| an sensor swap | ancestor swap | ancestor 被误识别为 an sensor |
| drawn based | joint-based | 基于关节的（肌肉绑定技术） |
| width | weights | 蒙皮权重，骨骼对顶点的影响权重值 |
| skin width | skin weights | 蒙皮权重，完整写法 |
| pinned | painted | painted weights，Maya中手动绘制权重 |
| inference | influence | 影响（骨骼对顶点的影响范围） |
| ArcData | MArgData | Maya API中解析命令参数的类 |
| mSyntax | MSyntax | Maya API定义命令语法的类 |
| commandSyntax | MSyntax | Maya API定义命令语法的类 |
| new一个thing | new一个scene | Maya脚本操作：新建场景 |

### 4.2 层级关系

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| 子集 | 子级 | child，层级关系中的下级 |
| 父集 | 父级 | parent，层级关系中的上级 |
| 负极 | 父级 | parent，同音字混淆（负极是电池术语） |
| 音响 | 影响 | influence，骨骼对顶点的影响范围 |
| 格子 | 代码 | 发音相似导致误识别 |

---

## 5. 游戏行业术语

### 5.1 比赛与机构

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| RUKIES | Rookies | 大小写错误 |
| Rookie Sim | Rookies | 误识别 |
| rookies | Rookies | 大小写修正 |

### 5.2 赛道与类别

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| Concept2 | Concept Art | 发音相似 |
| concept art | Concept Art | 大小写修正 |
| concept artist | Concept Artist | 大小写修正 |
| keyframe | Keyframe | 大小写修正 |
| paint over | Paint Over | 大小写修正 |
| Paint over | Paint Over | 大小写修正 |

### 5.3 公司与工作室

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| Owatch | Overwatch | 发音不完整 |
| R Center | Art Center | 发音相似 |
| Art Centen | Art Center | 发音相似 |
| Lightbox | LightBox | 大小写修正 |

### 5.4 学校名称

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| ACCD | ACCD | Art Center College of Design 缩写（无需修正） |
| USC | USC | 南加州大学（无需修正） |
| NYU | NYU | 纽约大学（无需修正） |
| CMU | CMU | 卡内基梅隆大学（无需修正） |

### 5.5 已知正确术语（无需修正）

以下术语在 ASR 输出中通常是正确的，无需修改：

| ASR 输出 | 判定 | 说明 |
|---------|------|------|
| Rookies Award | 正确 ✅ | 比赛名称 |
| Keyframe | 正确 ✅ | 赛道类别（注：术语 `keyframe` 需修正为 `Keyframe`） |
| Digital Fashion | 正确 ✅ | 赛道类别 |
| Game Art | 正确 ✅ | 赛道类别 |
| EA | 正确 ✅ | 公司名称 |
| Obsidian Entertainment | 正确 ✅ | 工作室名称 |
| Remedy Entertainment | 正确 ✅ | 工作室名称 |

---

## 6. AI 3D 生成与虚幻引擎

### 6.1 工具与平台

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| TertReference / preference / pure ref | PureRef | 参考图管理面板 |
| triple 3d AI | Tripo 3D AI | AI 3D 模型生成平台 |
| ProForce / profiles | Perforce | 版本控制系统 |
| Cloud | Claude | Anthropic AI 模型 |
| TabDown / TypeNode / type now / typenow | TapNow | AI 生图工具 |
| 麦克斯 / 麦壳思 | MAXs | 课程配套插件名称 |

### 6.2 3D 建模流程

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| 30图 / 40图 | 三视图 / 四视图 | 多视图参考图 |
| 白提无影影 | 白盒无阴影 | white box no shadow |
| 左侧打 | 左侧图 | 左侧参考图 |
| 兵器器 | 编辑器 | editor |
| 提词词 / 骑士词 | 提示词 | prompt |
| 虚幻物引擎 / U15 | 虚幻5引擎 / UE5 | Unreal Engine 5 |

### 6.3 界面操作

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| 接下号 | 加号 | 点击 + 按钮 |
| ctrlv / ctrl+v / ctrl v | Ctrl+V | 快捷键（同理 ctrl+c/ctrl+z/ctrl+s 等） |
| Facebook | 消耗 | token/credit consumption |

---

## 使用说明

### 在字幕优化中的应用

1. **加载术语表**：在开始优化前，读取本术语对照表
2. **大小写敏感匹配**：只匹配大小写完全一致的条目，不影响普通英文单词
3. **上下文验证**：结合上下文确认是否为术语误识别（避免误改正常词汇）
4. **保守原则**：当不确定是否为术语误识别时，保留原文

### 修正优先级

1. **明确匹配**：ASR 误识别词与正确术语完全匹配 → 直接修正
2. **不确定**：无法确认是否为误识别 → 保留原文
