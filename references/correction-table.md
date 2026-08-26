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

### 1.7 Maya 新特性与工作流

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| arnold / aarnold | Arnold | 渲染器名称 |
| mtoa / m to a | MtoA | Maya to Arnold 桥接 |
| by frost / bifrost | Bifrost | 视觉编程/BFX 环境 |
| lookdev / look dev | LookdevX | 外观开发工具 |
| motion maker / motionmaker | MotionMaker | Maya 2026 AI 动画工具 |
| retopo / retopology | Retopology | 拓扑重算 |
| pymel / pi mel | PyMEL | Python 在 Maya 中的库 |
| outliner / outliner | Outliner | 大纲视图面板 |
| deform / deformer | Deformer | 变形器系统总称 |
| skin cluster | Skin Cluster | 蒙皮簇 |
| skin weight / width | Skin Weight / Weights | 蒙皮权重 |
| constraint / constrain | Constraint | 约束系统 |
| camera sequencer | Camera Sequencer | 镜头序列器 |
| channel box | Channel Box | 通道栏属性编辑 |
| animation curve | Animation Curve | 动画曲线编辑 |
| graph editor | Graph Editor | 曲线图编辑器 |
| openpbr | OpenPBR | Maya 2026 新默认材质标准 |

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

### 2.3 编程工具与库

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| py charm / pychram / pycharm | PyCharm | Python IDE |
| jupyter / jupiter / jupiter notebook | Jupyter | 交互式笔记本 |
| anaconda / anna conda | Anaconda | Python 发行版 |
| pie test / p test | pytest | Python 测试框架 |
| unit test | unittest | Python 内置测试框架 |
| pie pi / p ip | pip | Python 包管理器 |
| asyncio / async io | asyncio | 异步 I/O 库 |
| type hint / typehint | Type Hint | 类型注解 |
| decorator / decoration | Decorator | 装饰器模式 |
| context manager / contextmanager | Context Manager | 上下文管理器 |
| list comp / comprehension | List Comprehension | 列表推导式 |
| generator / yield | Generator | 生成器函数 |
| virtual env / venv | Virtual Environment | 虚拟环境 |
| 变量 / 变亮 | 变量 | variable 的同音误识 |
| 推导式 / 推算 | 推导式 | comprehension |

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

### 5.3 游戏设计流程

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| game jam / game jam | Game Jam | 游戏开发节 |
| prototype / pro type | Prototype | 原型制作 |
| play test / plate test | Playtest | 游戏测试 |
| mood board / move board | Mood Board | 情绪板/视觉调性板 |
| design document / GDD | Game Design Document | 游戏设计文档 |
| turn around / 转面 | Turnaround | 角色转面设计 |
| silhouette / 剪影/减影 | Silhouette | 人物轮廓设计 |
| color palette / palette | Color Palette | 调色盘/配色方案 |
| world building | World Building | 世界观构建 |
| tech art / 技术美术 | Technical Artist | 技术美术师岗位 |
| asset pipeline / pipeline | Asset Pipeline | 资产制作管线 |
| polygon budget / poly count | Polygon Budget | 面数预算优化 |
| concept design / 概念设计 | Concept Design | 概念设计阶段 |

### 5.4 公司与工作室

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

## 6. AI 3D 生成

### 6.1 工具与平台

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| TertReference / preference / pure ref | PureRef | 参考图管理面板 |
| triple 3d AI | Tripo 3D AI | AI 3D 模型生成平台 |
| triple / tripa | Tripo | 缩写 |
| ProForce / profiles | Perforce | 版本控制系统 |
| Cloud | Claude | Anthropic AI 模型 |
| TabDown / TypeNode / type now / typenow | TypeNow | AI 生图工具 |
| TapNow / type now / typenow | TapNow | AI 生图工具（与 TypeNow 关联） |
| 麦克斯 / 麦壳思 | MAXs | 课程配套插件名称 |
| messy / meshy | Meshy | AI 3D 模型生成平台 |
| luma / lumen / luminous | Luma AI | AI 3D/视频生成平台 |
| genie / jenny | Genie | Luma AI 的 3D 生成工具 |
| dream machine / dream machine | Dream Machine | Luma AI 视频生成模型 |
| nerd / nerf | NeRF | 神经辐射场 3D 重建 |
| omni verse / omnyverse | Omniverse | NVIDIA 3D 协作平台 |
| sloyd / sloid | Sloyd | 参数化 3D 资产生成 |
| sloyed / sloide | Sloyd | 参数化 3D 资产生成 |
| gaussian splat / gauss splat | Gaussian Splatting | 3D 高斯泼溅重建 |
| photo gram / photo grammetry | Photogrammetry | 摄影测量 3D 重建 |
| wonder dynamics / wonder | Wonder Dynamics | AI 3D 动画工具 |
| stable cascade / SC | Stable Cascade | Stability AI 3D 生成模型 |
| control net / control net 3D | ControlNet 3D | 3D ControlNet 控制网络 |
| spline / spline 3D | Spline | 交互式 3D 设计工具 |
| point e / point E | Point-E | OpenAI 3D 点云生成 |

### 6.2 3D 建模流程

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| 30图 / 40图 | 三视图 / 四视图 | 多视图参考图 |
| 白提无影影 | 白盒无阴影 | white box no shadow |
| 左侧打 | 左侧图 | 左侧参考图 |
| 兵器器 | 编辑器 | editor |
| 提词词 / 骑士词 | 提示词 | prompt |
| 收尾帧 | 首尾帧 | 帧动画起止标记 |
| 偏激的格式 | PNG 格式 | 发音相似 |
| 点心面 | 点线面 | 发音相似 |
| 面素 | 面数 | 发音不完整 |
| 文理生成 | 纹理生成 | 同音字混淆 |
| 穿束 | 参数 | 发音相似 |
| 空 VUI / confi / kungfu | ComfyUI | 发音相似，已知多种变体 |

### 6.3 界面操作

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| 接下号 | 加号 | 点击 + 按钮 |
| ctrlv / ctrl+v / ctrl v | Ctrl+V | 快捷键（同理 ctrl+c/ctrl+z/ctrl+s 等） |
| Facebook | 消耗 | token/credit consumption |

### 6.4 AI 术语常见误识别

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| 大模型 | Large Model | AI 大语言模型 |
| 模型 | 模型 | AI 模型的通用称呼（"模"是正确写法，"摸型"是误写） |
| 声程 | 生成 | generation，同音字混淆 |
| 训练 / 讯练 | 训练 | training，同音字混淆 |
| 推理 / 退离 | 推理 | inference，AI 推理阶段 |
| 微调 / 味调 | 微调 | fine-tuning |
| 权重 / 权证 | 权重 | weights，模型权重参数 |
| 扩散 / 扩展 | 扩散 | diffusion，图像生成扩散模型 |
| 嵌布 | embedding | 嵌入，AI 特征表示 |
| 对器 | 对齐 | alignment，训练中对齐（RLHF 等） |

---

## 7. Substance Painter / 材质贴图

### 7.1 软件与工作流

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| substance / sub stance | Substance 3D | 发音相似 |
| sample / sampler | Sampler | Substance 3D Sampler 材质采集工具 |
| designer / desiner | Designer | Substance 3D Designer 节点材质工具 |
| stager / stage | Stager | Substance 3D Stager 场景布景 |
| alchemist / alchemy | Alchemist | Substance Alchemist 材质生成器 |

### 7.2 贴图与材质

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| anchor / anger point | Anchor Point | Substance Painter 锚点系统 |
| smart mask / smart mass | Smart Mask | 智能蒙版（发音相似） |
| fill layer / feel layer | Fill Layer | 填充图层 |
| texture set / texture set | Texture Set | 纹理集 |
| export template | Export Template | 导出模板 |
| channel pack / channel pack | Channel Pack | 通道打包 |
| paint mesh / pain mesh | Paint Mesh | 网格绘制模式 |
| dynamic material / dynamic | Dynamic Material | 动态材质 |

### 7.3 贴图类型与烘焙

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| mesh map / mesh map | Mesh Map | 网格贴图（法线/曲率/位置/厚度） |
| curvature / curvy ture | Curvature Map | 曲率贴图 |
| position map / position | Position Map | 位置贴图 |
| thickness / thickness map | Thickness Map | 厚度贴图 |
| udim / u dim / u dim | UDIM | UV 瓷砖编号工作流 |
| baking / bagging | Baking | 低模→高模烘焙通道 |
| normal map / norm map | Normal Map | 法线贴图 |
| height map / hight map | Height Map | 高度贴图 |
| 烘焙 / 哄培 / 烘培 | 烘焙 | baking，常见同音字混淆 |
| 曲率 / 曲律 / 曲力 | 曲率 | curvature map，同音字混淆 |
| 法线贴图 / 法形贴图 | 法线贴图 | normal map，常见误写 |

---

## 8. Blender 术语

### 8.1 软件与渲染引擎

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| blender / blend her | Blender | 发音相似，大小写修正 |
| blend her | Blender | 发音相似 |
| eevee / e v / e vee | Eevee | 实时渲染引擎 |
| cycles / cycles render | Cycles | 基于物理的路径追踪渲染器 |
| workbench / work beach | Workbench | 视口显示引擎 |

### 8.2 建模与修改器

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| modifier / modifi er | Modifier | 修改器系统 |
| sub division / sub divis | Subdivision Surface | 细分曲面修改器 |
| solidify / solify / solid | Solidify | 实体化修改器 |
| bevel / beval / bev | Bevel | 倒角修改器 |
| boolean / boole an | Boolean | 布尔运算修改器 |
| mirror / miror | Mirror | 镜像修改器 |
| geometry nodes / geo nodes | Geometry Nodes | 几何节点系统 |
| goo nodes / geo | Geometry Nodes | 发音相似 |
| node group / node group | Node Group | 节点组，可封装复用 |

### 8.3 雕刻与纹理

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| sculpt / sculp | Sculpt Mode | 雕刻模式 |
| grease pencil / grease | Grease Pencil | 蜡笔 2D/3D 动画工具 |
| texture paint / tex paint | Texture Paint | 纹理绘制模式 |
| shader editor / shader | Shader Editor | 着色器节点编辑器 |
| compositor / compositer | Compositor | 合成器节点编辑器 |
| uv editing / u v | UV Editing | UV 编辑工作区 |
| armature / armature | Armature | 骨架绑定系统 |
| rigify / rigi fy | Rigify | 自动角色绑定插件 |

### 8.4 中文常用术语

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| 修改器 / 修改气 | 修改器 | Modifier |
| 细分曲面 / 细分区面 | 细分曲面 | Subdivision Surface |
| 着色器 / 设色器/射器 | 着色器 | Shader |
| 粒子系统 / 粒子系 | 粒子系统 | Particle System |
| 雕刻模式 / 调动雕刻 | 雕刻模式 | Sculpt Mode |
| 骨骼绑定 / 骨骼绑 | 骨骼绑定 | Rigging / Armature |
| 蜡笔 / 拉笔 | Grease Pencil | 2D 动画工具 |
| 几何节点 / 集合节点 | 几何节点 | Geometry Nodes |

---

## 9. Unreal Engine 术语

### 9.1 引擎与核心系统

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| unreal / 虚幻 | Unreal Engine | 虚幻引擎 |
| ue5 / u15 / u e 5 | UE5 | Unreal Engine 5，数字误识别 |
| blue print / blue print | Blueprint | 蓝图可视化脚本系统 |
| blueprint / blue print | Blueprint | 空格修正 |
| nanite / night / na nite | Nanite | 虚拟化微多边形几何系统 |
| lumen / luminous / lu men | Lumen | 动态全局光照和反射系统 |
| niagara / ni agra / nigara | Niagara | 视觉特效粒子系统 |
| chaos / chaos physics | Chaos Physics | 物理破坏系统 |
| metahuman / meta human | MetaHuman | 高保真数字人框架 |
| world partition / world part | World Partition | 世界分区流式加载 |

### 9.2 关卡与动画

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| sequencer / sequence | Sequencer | 过场动画/关卡序列编辑器 |
| control rig / control rig | Control Rig | 控制绑定系统 |
| animation blueprint / anim bp | Animation Blueprint | 动画蓝图 |
| behavior tree / behavior | Behavior Tree | 行为树 AI 系统 |
| game mode / game mode | Game Mode | 游戏模式规则类 |
| level blueprint / level bp | Level Blueprint | 关卡蓝图 |
| landscape / land scape | Landscape | 地形系统 |
| material instance / mat instance | Material Instance | 材质实例 |
| skeletal mesh / skeleton mesh | Skeletal Mesh | 骨架网格体 |
| virtual shadow map / vsm | Virtual Shadow Map | 虚拟阴影贴图 |
| render target / render | Render Target | 渲染目标 |
| post process / poster | Post Process | 后处理体积 |

### 9.3 中文 UE 术语

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| 蓝图 / 蓝图系统 | Blueprint | 中文术语 |
| 虚幻物引擎 / 虚幻物 | 虚幻5引擎 / UE5 | 发音相似 |
| 关卡蓝图 / 关卡 | Level Blueprint | 关卡脚本系统 |
| 动画蓝图 / 动画蓝 | Animation Blueprint | 动画状态机 |
| 材质蓝图 / 材质 | Material Blueprint | 材质编辑器 |
| 行为树 / 行为数 | Behavior Tree | AI 行为决策系统 |
| 世界分区 / 世界分割 | World Partition | 大型世界加载方案 |
| 序列器 / 序列气 | Sequencer | 过场动画编辑器 |
| 混沌物理 / 混乱物理 | Chaos Physics | 物理破坏与模拟 |

---

## 10. Houdini FX 术语

### 10.1 软件与脚本

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| houdini | Houdini | 大小写修正 |
| side fx / side effects | SideFX | 发音相似（SideFX 是 Houdini 开发商） |
| vex / vecks / vx | VEX | Houdini 内置脚本语言（发音相似） |
| hda / digital asset | HDA / Digital Asset | Houdini 数字资产封装 |
| attribute wrangle / wrangler | Attribute Wrangle | 属性编辑节点（发音相似/拼写错误） |

### 10.2 节点系统

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| sop / s o p | SOP | Surface Operator，几何体操作节点 |
| vop / v o p | VOP | VEX Operator，着色器节点 |
| dop / d o p | DOP | Dynamics Operator，动力学节点 |
| pop net / pop net | POP Net | Particle Operator 粒子网络 |
| cop / c o p | COP | Compositing Operator，合成节点 |
| solver / solver node | Solver | 解算器节点（循环递进计算） |
| group / group node | Group | 几何体组（发音不完整） |
| for each / for each | For Each | 循环节点 |

### 10.3 特效与仿真

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| pyro / pie ro | Pyro | 火焰/烟雾仿真（发音相似） |
| flip / flew / flup | FLIP | 流体仿真（Liquid Simulation） |
| rbd / r b d | RBD | 刚体动力学（Rigid Body Dynamics） |
| vellum / velum | Vellum | 布料/柔体/毛发仿真 |
| volumes / volume | Volume | 体积（VDB 格式） |
| point cloud / point | Point Cloud | 点云数据 |
| vdb / v d b | VDB | OpenVDB 体积数据格式 |

### 10.4 中文术语

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| 数字资产 / 数码资产 | HDA / Digital Asset | 可复用的 Houdini 节点封装 |
| 解算器 / 计算器 | Solver | 发音相似，物理求解引擎 |
| 属性 / 属型 / 属心 | Attribute | 同音字，几何体数据 |
| 粒子 / 力子 | Particle | 同音字区别 |
| 体积 / 体极 | Volume | 3D 体素数据 |
| 爆炸 / 报炸 | 爆炸 | explosion 同音字 |

---

## 11. ZBrush 术语

### 11.1 软件名称

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| z brush / Z brush / zee brush | ZBrush | 空格/发音修正 |
| zee brush | ZBrush | 发音相似 |
| zb / z b | ZBrush | 缩写 |
| brush / z brush | ZBrush | 软件名（不是笔刷） |

### 11.2 核心功能

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| dynamesh / dynamic mesh | DynaMesh | 动态网格，实时重构拓扑 |
| dynamic mesh | DynaMesh | 发音相似含义相同 |
| z remesher / re-mesher | ZRemesher | 自动拓扑重构工具 |
| sub tool | Subtool | 子工具，ZBrush 中的独立模型层 |
| poly group | Polygroup | 多边形组，类似光滑组的集合 |
| fibermesh / fiber mesh | FiberMesh | 纤维网格系统（头发/毛发） |
| fiber / fiber | FiberMesh | 缩写 |
| zsphere / z sphere | ZSphere | Z 球，自适应骨架系统 |
| goz / go z | GoZ | ZBrush ↔ 其他软件桥接传输 |

### 11.3 笔刷与渲染

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| clay buildup / clay build | Clay Buildup | 粘土堆积笔刷 |
| standard brush / standard | Standard Brush | 标准笔刷（ZBrush 基础笔刷） |
| mask / masking | Mask | 遮罩，保护不受笔刷影响 |
| poly paint / poly paint | PolyPaint | 多边形顶点着色 |
| spotlight / spot light | Spotlight | 聚光灯投影贴图工具 |
| gizmo / gyzmo | Gizmo 3D | 变形操作器（移动/旋转/缩放） |
| hd geometry / h d geo | HD Geometry | 高分辨率细分几何体 |
| zmodeler / z modeler | ZModeler | 多边形直接建模系统 |
| insert mesh / insert | Insert Mesh | 插入网格笔刷 |
| live boolean / live | Live Boolean | 实时布尔运算 |
| bpr render / bpr | BPR | 最佳预览渲染（Best Preview Render） |
| alphas / alpha | Alpha | 笔刷灰度图/纹理贴图 |

### 11.4 中文术语

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| 动态网格 / 动感网格 | DynaMesh | 发音相似 |
| 子工具 / 子工具栏 | Subtool | 模型层级管理 |
| 多边形组 / 多边组 | Polygroup | 多边形分组 |
| 纤维 / 纤维网格 | FiberMesh | 发丝/纤维生成 |
| 拓扑 / 拓补 / 拓朴 | 拓扑 | Topology，常见错字 |
| 遮罩 / 遮照 / 遮造 | 遮罩 | Mask，保护区域的覆盖层 |
| 笔刷 / 臂刷 | 笔刷 | Brush |

---

## 12. Photoshop / 数字绘画术语

### 12.1 软件名称

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| photoshop / photo shop | Photoshop | 空格修正 |
| ps | Photoshop | 常见缩写 |
| photo shop | Photoshop | 空格修正 |
| camera raw / camera row | Camera Raw | 原始照片处理插件 |

### 12.2 图层与蒙版

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| layer mask / layer mask | Layer Mask | 图层蒙版，大小写修正 |
| adjustment layer / adjust | Adjustment Layer | 调整图层 |
| blending mode / blend mode | Blending Mode | 混合模式 |
| smart object / smart | Smart Object | 智能对象，非破坏性编辑 |
| layer style / layer style | Layer Style | 图层样式（阴影/发光/浮雕） |
| fill layer / fill | Fill Layer | 纯色/渐变/图案填充图层 |

### 12.3 选择与工具

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| selection / select | Selection | 选区工具 |
| pen tool / pen | Pen Tool | 钢笔路径工具 |
| brush tool / brush | Brush Tool | 画笔工具 |
| clone stamp / clone | Clone Stamp | 仿制图章工具 |
| dodge and burn / dodge | Dodge & Burn | 加深减淡局部调整技术 |
| content aware / content | Content-Aware | 内容识别填充 |
| gradient / gradiant | Gradient | 渐变工具（拼写错误） |

### 12.4 色彩与调整

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| hue saturation / hue | Hue/Saturation | 色相/饱和度调整 |
| curves / curve | Curves | 曲线调色工具 |
| levels / level | Levels | 色阶调整 |
| color balance / colour | Color Balance | 色彩平衡 |
| channel / channels | Channel | 通道面板（RGB/Alpha） |
| filter / filter | Filter | 滤镜效果 |

### 12.5 中文术语

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| 蒙版 / 蒙板 / 朦版 | 蒙版 | Mask，常见错字 |
| 图层 / 曾 / 图曾 | 图层 | Layer，同音字混淆 |
| 笔刷 / 臂刷 / 逼刷 | 笔刷 | Brush |
| 曲线 / 区线 | Curves | 同音字混淆 |
| 色相 / 色像 / 涉相 | Hue | 同音字混淆 |
| 饱和度 / 包合度 / 报合度 | Saturation | 发音/同音字混淆 |
| 色彩平衡 / 色彩平横 | Color Balance | 同音字混淆 |
| 色调 / 色掉 | Tone | 同音字混淆 |
| 滤镜 / 虑镜 | Filter | 同音字混淆 |

---

## 大小写校准

### 专有名词大写（通用，不依赖领域）

| 小写形式 | 标准写法 | 说明 |
|---------|---------|------|
| pcie | PCIe | Technical acronym |
| gpu | GPU | Technical acronym |
| cpu | CPU | Technical acronym |
| api | API | Technical acronym |
| sdk | SDK | Technical acronym |
| ai | AI | Technical acronym |
| html | HTML | Technical acronym |
| css | CSS | Technical acronym |
| js | JS | Technical acronym |
| ts | TS | Technical acronym |
| json | JSON | Technical acronym |
| sql | SQL | Technical acronym |
| http | HTTP | Technical acronym |
| rest | REST | Technical acronym |
| tcp | TCP | Technical acronym |
| ip | IP | Technical acronym |
| usb | USB | Technical acronym |
| hdmi | HDMI | Technical acronym |
| ssd | SSD | Technical acronym |
| hdd | HDD | Technical acronym |
| ram | RAM | Technical acronym |
| vram | VRAM | Technical acronym |
| dns | DNS | Technical acronym |
| dhcp | DHCP | Technical acronym |
| ftp | FTP | Technical acronym |
| ssh | SSH | Technical acronym |
| ssl | SSL | Technical acronym |
| tls | TLS | Technical acronym |
| png | PNG | Technical acronym |
| jpeg | JPEG | Technical acronym |
| gif | GIF | Technical acronym |
| svg | SVG | Technical acronym |
| xml | XML | Technical acronym |
| yaml | YAML | Technical acronym |
| toml | TOML | Technical acronym |
| cli | CLI | Technical acronym |
| gui | GUI | Technical acronym |
| ui | UI | Technical acronym |
| ux | UX | Technical acronym |
| ide | IDE | Technical acronym |
| db | DB | Technical acronym |
| vm | VM | Technical acronym |
| os | OS | Technical acronym |
| bios | BIOS | Technical acronym |
| ue5 | UE5 | Domain-specific acronym |
| ps | PS | Domain-specific acronym |
| hdr | HDR | Domain-specific acronym |
| pureref | PureRef | Brand/tool name |
| perforce | Perforce | Brand/tool name |
| tapnow | TapNow | Brand/tool name |
| claude | Claude | Brand/tool name |
| maya | Maya | Brand/tool name |
| blender | Blender | Brand/tool name |
| photoshop | Photoshop | Brand/tool name |
| xcode | Xcode | Brand/tool name |
| github | GitHub | Brand/tool name |
| nanite | Nanite | Brand/tool name |
| lumen | Lumen | Brand/tool name |
| megascans | Megascans | Brand/tool name |
| rookies | Rookies | Discipline-specific |
| lightbox | LightBox | Discipline-specific |
| overwatch | Overwatch | Discipline-specific |
| keyframe | Keyframe | Discipline-specific |
| playblast | Playblast | Discipline-specific |
| hypergraph | Hypergraph | Discipline-specific |
| hypershade | Hypershade | Discipline-specific |
| unreal engine | Unreal Engine | Multi-word term |
| tripo 3d ai | Tripo 3D AI | Multi-word term |
| concept artist | Concept Artist | Multi-word term |
| world partition | World Partition | Multi-word term |
| concept art | Concept Art | Multi-word term |
| art center | Art Center | Multi-word term |
| paint over | Paint Over | Multi-word term |

### 领域感知大小写组（按领域组激活）

| 小写形式 | 标准写法 | 领域组 | 说明 |
|---------|---------|--------|------|
| obj | obj | file_format | File extension |
| fbx | fbx | file_format | File extension |
| gltf | gltf | file_format | File extension |
| glb | glb | file_format | File extension |
| usd | usd | file_format | File extension |
| usdz | usdz | file_format | File extension |
| dae | dae | file_format | File extension |
| stl | stl | file_format | File extension |
| abc | abc | file_format | File extension |
| ma | ma | file_format | File extension |
| mb | mb | file_format | File extension |
| exr | exr | file_format | File extension |
| tga | tga | file_format | File extension |
| tiff | tiff | file_format | File extension |
| bmp | bmp | file_format | File extension |
| psd | psd | file_format | File extension |
| webp | webp | file_format | File extension |
| wav | wav | file_format | File extension |
| mp3 | mp3 | file_format | File extension |
| mp4 | mp4 | file_format | File extension |
| mov | mov | file_format | File extension |
| avi | avi | file_format | File extension |
| mxf | mxf | file_format | File extension |
| iges | iges | file_format | File extension |
| step | step | file_format | File extension |
| pbr | PBR | generic_acronym | Shading/standard term |
| lod | LOD | generic_acronym | Level of Detail |
| uv | UV | generic_acronym | UV coordinate |
| nx | NX | generic_acronym | Normal X |
| fov | FOV | generic_acronym | Field of View |
| dof | DOF | generic_acronym | Depth of Field |
| sss | SSS | generic_acronym | Subsurface Scattering |
| ldr | LDR | generic_acronym | Low Dynamic Range |
| sdr | SDR | generic_acronym | Standard Dynamic Range |
| sbsar | SBSAR | generic_acronym | Substance package format |
| sbs | SBS | generic_acronym | Substance graph format |
| nd | ND | generic_acronym | Normal Direction |
| ae | AE | generic_acronym | After Effects |
| pr | PR | generic_acronym | Premiere Pro |
| bake | Bake | generic_acronym | Baking process |
| unfold | Unfold | generic_acronym | UV unfolding |
| macos | macOS | os_term | Apple OS |
| ios | iOS | os_term | Apple mobile OS |
| ipados | iPadOS | os_term | Apple tablet OS |
| watchos | watchOS | os_term | Apple watch OS |
| tvos | tvOS | os_term | Apple TV OS |
| windows | Windows | os_term | Microsoft OS |
| linux | Linux | os_term | Open-source OS |
| android | Android | os_term | Google mobile OS |
| substance | Substance | brand_tool | Substance 3D suite |
| painter | Painter | brand_tool | Substance 3D Painter |
| designer | Designer | brand_tool | Substance 3D Designer |
| sampler | Sampler | brand_tool | Substance 3D Sampler |
| zbrush | ZBrush | brand_tool | Digital sculpting |
| marmoset | Marmoset | brand_tool | Marmoset Toolbag |
| toolbag | Toolbag | brand_tool | Marmoset Toolbag |
| speedtree | SpeedTree | brand_tool | Procedural vegetation |
| world machine | World Machine | brand_tool | Terrain generation |
| gaea | Gaea | brand_tool | Terrain generation |
| unreal | Unreal | brand_tool | Unreal Engine |
| unity | Unity | brand_tool | Unity Engine |
| godot | Godot | brand_tool | Godot Engine |
| houdini | Houdini | brand_tool | Houdini FX |
| nuke | Nuke | brand_tool | Compositing |
| fusion | Fusion | brand_tool | Compositing |
| rodin | Rodin | ai_3d | AI 3D generation |
| tripo | Tripo | ai_3d | AI 3D generation |
| meshy | Meshy | ai_3d | AI 3D generation |
| gen | Gen | ai_3d | Generation model |
| legacy | Legacy | ai_3d | Legacy model |
| native | Native | ai_3d | Native model |
| point | Point | ai_3d | Point cloud |

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

---

## 7. 用户确认持久化（自动追加）

以下条目由用户在使用过程中确认的修正自动追加。每次会话生成一条新记录。

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| 展门课 | 这门课 | 用户确认修正 |
| 光于 | 关于 | 用户确认修正 |
| 大肠都在用 | 大厂都在用 | 用户确认修正 |
| 十几个遍体 | 十几个变体 | 用户确认修正 |
| 事业观 | 世界观 | 用户确认修正 |
| 全波A | AAA | Triple-A，统一写 AAA；用户确认修正 |
| 跑费 | 跑废 | AI 跑废（运行损坏的版本）；用户确认修正 |
| 出版 | 出图 | 概念图出图；用户确认修正 |
| 规档 | 归档 | 用户确认修正 |
| 入屏 | 入门 | 用户确认修正 |
| 聊天光 | 聊天框 | 用户确认修正 |
| move board | mood board | 情绪板；用户确认修正 |
| cloud skills | Claude skills | 用户确认修正 |
| force（上传 context） | Perforce | 用户确认修正 |
| 建我自己存在的 | 存在我自己 | 用户确认修正 |
| 亲眼的 | 亲眼 | 亲眼看到；用户确认修正 |
| TypeNode | TapNow | AI 生图工具；用户确认修正 |
| 防射霜 | 防晒霜 | UV 类比用语；用户确认修正 |
| 钢箔 | 高模 | 高面数模型；用户确认修正 |
| 法形贴图 | 法线贴图 | 用户确认修正 |
| 一万司机 / 一万停电 | 死机 / 停电 | 电脑崩溃；用户确认修正 |
| 拍屏 / 拍平 | 展平 | UV 展开操作；用户确认修正 |
| 原著体 | 圆柱体 | 基本几何体；用户确认修正 |
| 起初 | 挤出 | extrude 操作；用户确认修正 |
| 解面 | 减面 | 减少面数；用户确认修正 |
| 金格 | 晶格 | Lattice 变形器；用户确认修正 |
| 带功耗组 | 光滑组 | Smoothing Group；用户确认修正 |
| 光折 / 光学 | 光照 | lighting；用户确认修正 |
| 烘培 | 烘焙 | baking；用户确认修正 |
| 散热面 | 三角面 | triangle face；用户确认修正 |
| 反线 / 法性 | 法线 | normal 方向；用户确认修正 |
| Hyper3D Routing / Hyper3D loading | Hyper3D Rodin | AI 3D 生成工具；用户确认修正 |
| 蚂蚁2026 | Maya 2026 | 3D 软件；用户确认修正 |
| CLS | 该 | 应当；用户确认修正 |
| outline | Outliner | Maya 大纲面板；用户确认修正 |
| p cube 1 | pCube1 | Maya 多边形立方体命名；用户确认修正 |
| p cube1 | pCube1 | Maya 多边形立方体命名；用户确认修正 |
| 式口 | 视口 | viewport；用户确认修正 |
| 试口 | 视口 | viewport；用户确认修正 |
| ctrle | Ctrl+E | 快捷键；用户确认修正 |
| ctrl+e | Ctrl+E | 快捷键；用户确认修正 |
| ctrl e | Ctrl+E | 快捷键；用户确认修正 |
| ctrl+c | Ctrl+C | 快捷键；用户确认修正 |
| ctrl c | Ctrl+C | 快捷键；用户确认修正 |
| ctrl+v | Ctrl+V | 快捷键；用户确认修正 |
| ctrl v | Ctrl+V | 快捷键；用户确认修正 |
| controld | Ctrl+D | 快捷键；用户确认修正 |
| 玛雅 | Maya | ASR 校准；用户确认修正 |
| 虚幻无影前 | 虚幻5引擎 | UE5 Unreal Engine 5；用户确认修正 |
| 运从围一下 | 另存为一下 | Hyper3D Rodin 工作流操作；用户确认修正 |
| 两把外面的这个 | 然后把外面的这个 | ASR 误识别；用户确认修正 |
| Hyper 3D Routing | Hyper3D Rodin | 带空格的 ASR 形式；用户确认修正 |
| Image 2 3D | Image To 3D | AI 3D 工具；用户确认修正 |
| next | Legacy | Rodin Gen 材质模式；用户确认修正 |
| negative | Native | Rodin Gen 材质模式；用户确认修正 |
| 点心面 | 点线面 | 发音相似；用户确认修正 |
| 面素 | 面数 | 发音不完整；用户确认修正 |
| 文理生成 | 纹理生成 | 同音字混淆；用户确认修正 |
| 穿束 | 参数 | 发音相似；用户确认修正 |
| 空 VUI | ComfyUI | 发音相似；用户确认修正 |
| confi | ComfyUI | 文件夹名；用户确认修正 |
| KungfuUI | ComfyUI | 用户自定义名称，统一写法；用户确认修正 |
| type down | TapNow | 剩余未匹配项；用户确认修正 |
| PBI | PBR | 单处遗漏；用户确认修正 |
| 偏激的格式 | PNG 格式 | 发音相似；用户确认修正 |
| 循环5（非 Maya 语境） | 虚幻5 | 单处"循环5→虚幻5"在材质语境中；用户确认修正 |
| 瓦那 | 华纳 | Warner Bros 发音相似；用户确认修正 |
| 霍格沃兹之一 | 霍格沃兹之遗 | Hogwarts Legacy 发音不完整；用户确认修正 |
| 物气 | 雾气 | 同音字混淆；用户确认修正 |
| 阻次 | 层次 | 发音相似；用户确认修正 |
| 插线 | 插件 | 发音相似；用户确认修正 |
| 地边 / DBN / DBA | 地编 | 场景地编 Level Design；用户确认修正 |
| Titan光 | 天光 | Skylight ASR 错误；用户确认修正 |
| lex | lux | 光照单位 lux；用户确认修正 |
| eve | EV | 曝光值 EV；用户确认修正 |
| Retracing Shadow | Ray Tracing Shadow | 光线追踪阴影；用户确认修正 |
| Post-Positive Volume | Post Process Volume | 后处理体积；用户确认修正 |
| 丁达尔效果 / 叮答儿 | 丁达尔效应 | Tyndall effect；用户确认修正 |
| color nuts | Color LUTs | 调色 LUT；用户确认修正 |
| 蓝推街 | 蓝图 | Blueprint 发音相似；用户确认修正 |
| 调成雷 | 调为0 | 数值归零，发音相似；用户确认修正 |
| 打分器 | 达芬奇 | DaVinci Resolve；用户确认修正 |
| 不懂时代 | 不同时代 | 场景 critique，发音相似；用户确认修正 |
| 下招 | 校招 | 校园招聘 ASR 误识别；用户确认修正 |
| 岸厂 | 校招 | 校园招聘 ASR 误识别；用户确认修正 |
| 现役（游戏大厂） | 心仪 | 心仪的游戏大厂；用户确认修正 |
| 地边港 | 地编岗 | 地编岗位 ASR 误识别；用户确认修正 |

---

## 用户确认修正（通用/文学播客）

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| 王欧行 | 王鸥行 | Ocean Vuong 越南裔美国作家；联网校准确认 |
| Billy Eilish | Billie Eilish | 美国歌手；联网校准确认 |
| 村上村树 | 村上春树 | Haruki Murakami 日本作家；联网校准确认 |
| 金安亮 | 金安岚 | 语境一致性修正（与前文金安岚统一） |
| 月晚 | 明亮的夜晚 | 崔恩荣韩国小说；联网校准确认 |

---

## 用户确认修正（Maya/刚体物理录播课）

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| OLA / Ola method / orla method | Euler / Euler method | 欧拉积分法；Euler 发音 ASR 误识别 |
| semi-implicit OLA / Semi-Implaced OLA | semi-implicit Euler | 半隐式欧拉积分 |
| Overline Integrator | Euler Integrator | 欧拉积分器误识别 |
| stevenness / stickness | stiffness | 刚度（弹簧系数） |
| gigaboint / gigaboint update | jiggle joint / jiggle joint update | Maya 动力学 Joint |
| people joint | pivot joint | Maya 枢轴关节 |
| join chain / john | joint chain / joint | 关节链误识别 |
| room matrix / rule matrix | root matrix | 根矩阵误识别 |
| Claw Simulation | Cloth Simulation | 布料模拟 |
| data t / data time / delatime | delta t / delta time | delta 时间步长 |
| giggle / giggle amount / calculateGiggo | jiggle / jiggle amount / calculateJiggle | jiggle 抖动效果 |
| damp spring simple motion / damaged spring harmonic | damped spring simple motion / damped spring harmonic | 阻尼弹簧简谐运动 |
| envegage target point / envavage target point | initial target point | 初始目标点误识别 |
| sackling | setClean | Maya API setClean 方法 |
| attribute effects | attribute affects | Maya API attributeAffects |
| target of that matrix | target offset matrix | 目标偏移矩阵 |
| inlinear | linear | 线性插值 |
| protab | prototype | 原型 |
| 钢体 | 刚体 | 刚体物理标准术语 |
| 角约数 | 角约束 | 角度约束 |
| 影视 / 引式 | 隐式 | 隐式积分法 |
| 半显示 / 半影视 / 半影式 / 半隐性 / 半引式 / 半隐士 | 半隐式 | 半隐式欧拉 |
| 胡和定律 / 虎克定律 | 胡克定律 | Hooke's Law |
| 弹簧光度 | 弹簧刚度 | spring stiffness |
| 阻尼吸水 | 阻尼系数 | damping coefficient |
| 祖尼系统 / 促尼 | 阻尼系统 | damping system |
| 祖尼系数 / 减斜 | 阻尼系数 | damping coefficient |
| 检学运动 | 简谐运动 | simple harmonic motion |
| 协律 | 斜率 | slope |
| 奥米卡 / 奥米卡0 | 欧米伽 / 欧米伽0 | omega / omega0 |
| 片面方程 | 偏微分方程 | partial differential equation |
| 步传 | 步长 | step size |
| 接盘没电了 | 键盘没电了 | keyboard battery dead |
| M乘A平方 | M乘A (F=ma) | 牛顿第二定律 |
| 风光震动 | 疯狂振荡 | 剧烈振荡 |
| linear的interplay | linear的插值(lerp) | linear interpolation|
| omega | omega | 角频率归一化 |
| 二阶导数用lambda平方 | 二阶导得lambda平方 | 二阶导特征方程 |
| 通解是ce乘x1t加上cr乘x2t | 通解是c1乘x1t加上c2乘x2t | 通解系数修正 |

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| 就打个表 | 就打个比方 | 用户确认修正 |
| 抱他这个伴 | 报他这个班 | 用户确认修正 |

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| Corker | Claude | 用户确认修正 |
| Coworker | Claude | 用户确认修正 |
| Bstorming | Brainstorming | 用户确认修正 |
| GHub | GitHub | 用户确认修正 |
| keychain | Keyframe | 用户确认修正 |
| 五几天 | 我这几天 | 用户确认修正 |
| 说人语语不如说人语语 | 说人话 | 用户确认修正 |
| 马尔 | Maya | 用户确认修正 |
| 比说 | 比如说 | 用户确认修正 |
| 优异 | 游戏 | 用户确认修正 |
| 讹厂 | 鹅厂 | 用户确认修正 |
| 拓产 | 脱产 | 用户确认修正 |
| 低编 | 地编 | 用户确认修正 |
| 科学学 | 本科学 | 用户确认修正 |
| 正式效章 | 正式上岗 | 用户确认修正 |
| 国内的一天大厂 | 国内的一家大厂 | 用户确认修正 |
| 度曾经 | 镀金 | 用户确认修正 |
| 作品级 | 作品集 | 用户确认修正 |
| 一本亏本 | 一笔亏本 | 用户确认修正 |
| 投币院校 | 欧美院校 | 用户确认修正 |

## 用户确认修正（Unreal 水材质教程）

| ASR 误识别 | 正确术语 | 说明 |
|-----------|---------|------|
| 虚妄 | 虚幻 | Unreal 引擎中文名；用户确认修正 |
| 虚幻无引擎 / UE无引擎 | 虚幻5引擎 / UE5引擎 | UE5 发音误识别；用户确认修正 |
| 虚幻五字带 | 虚幻5自带 | UE5 内置；用户确认修正 |
| 交散 | 焦散 | caustics；用户确认修正 |
| 足射 | 折射 | refraction；用户确认修正 |
| 发现 / 发线 / 发型 / 仿星 / 仿线 | 法线 | normal，法线贴图语境；用户确认修正 |
| 下滑线 / 向滑线 | 下划线 | underscore；用户确认修正 |
| text coordinate | Texture Coordinate | 材质节点名；用户确认修正 |
| nomal tiling | Normal Tiling | 材质节点名；用户确认修正 |
| Twater Normal | T_Water Normal | 贴图命名；用户确认修正 |
| UBI | UV | 坐标误识别；用户确认修正 |
| panel / PAN / panelpan | Panner | 材质节点 Panner；用户确认修正（注意不匹配 panner 全词） |
| primiton | Parameter | 材质节点 Parameter；用户确认修正 |
| speedxspeedy | SpeedX SpeedY | 参数名；用户确认修正 |
| BlendingAngleCorrectNomals | BlendAngleCorrectedNormals | UE 官方节点；联网校准确认 |
| Flat and Noble | Flatten Normal | UE 官方节点；联网校准确认 |
| flattenness | flatness | 材质节点属性；用户确认修正 |
| normalintensity | Normal Intensity | 材质节点属性；用户确认修正 |
| cloudshadowopacity | Cloud Shadow Opacity | 材质节点属性；用户确认修正 |
| blendblend | Blend | 发音重叠；用户确认修正 |
| smooth step | SmoothStep | 材质节点；用户确认修正 |
| mean | Min | 材质节点 Min，发音误识别；用户确认修正 |
| 安卓s / 安卓L | 按S / 按L | 键盘快捷键 ASR 误识别；用户确认修正 |
| t-noise | T_Noise | 贴图命名；用户确认修正 |
| 接点图 | 节点图 | 材质节点图；用户确认修正 |
| entcomponent mask / maskcompon | ComponentMask | UE 官方节点；用户确认修正 |
| Cloud | Cloud | 注意：Cloud Shadow/Cloud Color 等 Unreal 术语不可误改为 Claude；用户确认修正 |
| 人事 | 人生 | ASR 误识别；用户确认修正 |
| Cloud Code | Claude Code | ASR 误识别；用户确认修正 |
| 马海 | Maya | 发音相似；用户确认修正 |
| 马眼 | Maya | 发音相似；用户确认修正 |
| 面书 | 面数 | ASR 误识别；用户确认修正 |
| 简讯 | 简历 | ASR 误识别；用户确认修正 |
| 解面 | 减面 | ASR 误识别；用户确认修正 |
| XGBT | ChatGPT | ASR 误识别；用户确认修正 |
| chatpdt | ChatGPT | ASR 误识别；用户确认修正 |
| Chad GPD | ChatGPT | ASR 误识别；用户确认修正 |
| 拆GPT | ChatGPT | ASR 误识别；用户确认修正 |
| Brain Storing | Brainstorming | ASR 误识别；用户确认修正 |
| 原住期 | 圆柱体 | ASR 误识别；用户确认修正 |
| 原柱体 | 圆柱体 | ASR 误识别；用户确认修正 |
| 玛雅 | Maya | 大小写修正；用户确认修正 |
