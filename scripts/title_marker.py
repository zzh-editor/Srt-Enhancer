#!/usr/bin/env python3
"""Deterministic game/media title marking with 《》.

Contract (P1-2): This script is a deterministic first-pass with HIGH precision, NO recall guarantee.
- Operates strictly line-local: title + GAME_CUES/FILM_CUES must co-occur on the SAME subtitle line to mark.
- KNOWN_TITLES (148 entries) filtered by TOOL_BLACKLIST; strong cue +逐行 ⇒ low recall by design.
- Full-document semantic title detection is handled by the AI systematic scan in SKILL §7a,
  which builds `title_candidates` via web verification and overrides this script's output.
Do NOT use this script as a standalone recall diagnostic.
"""

import re

KNOWN_TITLES = {
    # AAA 大作
    "黑神话：悟空": "《黑神话：悟空》",
    "黑神话悟空":    "《黑神话悟空》",
    "对马岛之魂":    "《对马岛之魂》",
    "原神":          "《原神》",
    "赛博朋克2077":  "《赛博朋克2077》",
    "艾尔登法环":    "《艾尔登法环》",
    "只狼":          "《只狼》",
    "战神":          "《战神》",
    "最后生还者":    "《最后生还者》",
    "荒野大镖客":    "《荒野大镖客》",
    "巫师3":         "《巫师3》",
    "死亡搁浅":      "《死亡搁浅》",
    "集合啦动物森友会": "《集合啦动物森友会》",
    "动物森友会":    "《动物森友会》",
    "宝可梦":        "《宝可梦》",
    "塞尔达传说":    "《塞尔达传说》",
    "塞尔达":        "《塞尔达传说》",
    "马里奥":        "《超级马里奥》",
    "最终幻想":      "《最终幻想》",
    "怪物猎人":      "《怪物猎人》",
    "街头霸王":      "《街头霸王》",
    "拳皇":          "《拳皇》",
    "星际争霸":      "《星际争霸》",
    "魔兽世界":      "《魔兽世界》",
    "英雄联盟":      "《英雄联盟》",
    "DOTA2":         "《DOTA2》",
    "守望先锋":      "《守望先锋》",
    "APEX":          "《APEX英雄》",
    "堡垒之夜":      "《堡垒之夜》",
    "绝地求生":      "《绝地求生》",
    # 新增 AAA/独立游戏
    "博德之门3":     "《博德之门3》",
    "博德之门三":    "《博德之门三》",
    "星空":          "《星空》",
    "霍格沃茨之遗":  "《霍格沃茨之遗》",
    "霍格沃兹之遗":  "《霍格沃兹之遗》",
    "霍格沃茨":      "《霍格沃茨之遗》",
    "漫威蜘蛛侠":    "《漫威蜘蛛侠》",
    "漫威金刚狼":    "《漫威金刚狼》",
    "心灵杀手2":     "《心灵杀手2》",
    "心灵杀手二":    "《心灵杀手二》",
    "地狱之刃2":     "《地狱之刃2》",
    "地狱之刃二":    "《地狱之刃二》",
    "黑帝斯":        "《黑帝斯》",
    "黑帝斯2":       "《黑帝斯2》",
    "空洞骑士":      "《空洞骑士》",
    "丝之歌":        "《丝之歌》",
    "茶杯头":        "《茶杯头》",
    "死亡细胞":      "《死亡细胞》",
    "以撒的结合":    "《以撒的结合》",
    "哈迪斯":        "《哈迪斯》",
    "蔚蓝":          "《蔚蓝》",
    "星露谷物语":    "《星露谷物语》",
    "暗黑破坏神":    "《暗黑破坏神》",
    "暗黑破坏神4":   "《暗黑破坏神4》",
    "辐射4":         "《辐射4》",
    "辐射四":        "《辐射四》",
    "上古卷轴":      "《上古卷轴》",
    "上古卷轴5":     "《上古卷轴5》",
    "侠盗猎车手":    "《侠盗猎车手》",
    "给他爱":        "《给他爱》",
    "给她爱":        "《给她爱》",
    "GTA5":          "《GTA5》",
    "GTA V":         "《GTA V》",
    "我的世界":      "《我的世界》",
    "Minecraft":     "《Minecraft》",
    # Nintendo
    "王国之泪":      "《王国之泪》",
    "旷野之息":      "《旷野之息》",
    "异度之刃":      "《异度之刃》",
    "斯普拉遁":      "《斯普拉遁》",
    "喷射战士":      "《喷射战士》",
    "星之卡比":      "《星之卡比》",
    "皮克敏":        "《皮克敏》",
    "火焰纹章":      "《火焰纹章》",
    "密特罗德":      "《密特罗德》",
    "银河战士":      "《银河战士》",
    "大乱斗":        "《任天堂明星大乱斗》",
    "马车":          "《马里奥赛车》",
    "马车8":         "《马里奥赛车8》",
    "健身环大冒险":  "《健身环大冒险》",
    # 影视IP改编
    "哈利波特":      "《哈利波特》",
    "指环王":        "《指环王》",
    "力量之戒":      "《力量之戒》",
    "权力的游戏":    "《权力的游戏》",
    "龙之家族":      "《龙之家族》",
    "最后生还者剧版":"《最后生还者》",
    "赛博朋克边缘行者": "《赛博朋克边缘行者》",
    "英雄联盟双城之战": "《英雄联盟双城之战》",
    "双城之战":      "《双城之战》",
    "奥术":          "《奥术》",
    # 国产/亚洲游戏
    "永劫无间":      "《永劫无间》",
    "崩坏星穹铁道":  "《崩坏星穹铁道》",
    "星穹铁道":      "《星穹铁道》",
    "崩坏3":         "《崩坏3》",
    "绝区零":        "《绝区零》",
    "鸣潮":          "《鸣潮》",
    "幻塔":          "《幻塔》",
    "剑网3":         "《剑网3》",
    "最终幻想14":    "《最终幻想14》",
    "ff14":          "《FF14》",
    "失落之魂":      "《失落之魂》",
    "影之刃":        "《影之刃》",
    "百面千相":      "《百面千相》",
    "燕云十六声":    "《燕云十六声》",
    # 通用英文名
    "Elden Ring":    "《Elden Ring》",
    "Sekiro":        "《Sekiro》",
    "God of War":    "《God of War》",
    "The Last of Us":"《The Last of Us》",
    "Red Dead":      "《Red Dead》",
    "Cyberpunk 2077":"《Cyberpunk 2077》",
    "Baldur's Gate": "《Baldur's Gate》",
    "Starfield":     "《Starfield》",
    "Hogwarts Legacy":"《Hogwarts Legacy》",
    "Spider-Man":    "《Spider-Man》",
    "Alan Wake":     "《Alan Wake》",
    "Hellblade":     "《Hellblade》",
    "Hades":         "《Hades》",
    "Hollow Knight": "《Hollow Knight》",
    "Cuphead":       "《Cuphead》",
    "Dead Cells":    "《Dead Cells》",
    "Stardew Valley":"《Stardew Valley》",
    "Zelda":         "《Zelda》",
    "Mario":         "《Mario》",
    "Final Fantasy": "《Final Fantasy》",
    "Monster Hunter":"《Monster Hunter》",
    "Street Fighter":"《Street Fighter》",
    "World of Warcraft": "《World of Warcraft》",
    "League of Legends": "《League of Legends》",
    "Overwatch":     "《Overwatch》",
    "Fortnite":      "《Fortnite》",
    "PUBG":          "《PUBG》",
    "Apex Legends":  "《Apex Legends》",
    "Wuthering Waves":"《Wuthering Waves》",
    "Genshin Impact":"《Genshin Impact》",
    "Honkai Star Rail":"《Honkai Star Rail》",
    "Zenless Zone Zero":"《Zenless Zone Zero》",
}

# Context cues suggesting a game/film title
GAME_CUES = [
    "玩", "打", "通关", "攻略", "评测", "推荐",
    "下载", "安装", "联机", "单机", "游戏",
    "角色", "关卡", "boss", "BOSS", "Boss",
    "存档", "MOD", "mod", "DLC", "dlc",
]

FILM_CUES = [
    "看", "上映", "导演", "演员", "剧情",
    "豆瓣", "IMDB", "imdb", "观影",
]

TOOL_BLACKLIST = [
    "unreal", "虚幻", "maya", "photoshop", "substance",
    "blender", "zbrush", "unity", "max", "c4d",
    "after effects", "premiere", "final cut",
]


def _has_cue(text: str, cues: list[str]) -> bool:
    text_lower = text.lower()
    for cue in cues:
        if cue.lower() in text_lower:
            return True
    return False


def _is_tool(name: str) -> bool:
    name_lower = name.lower()
    for t in TOOL_BLACKLIST:
        if t in name_lower:
            return True
    return False


def mark_titles(text: str) -> str:
    """Add 《》 book-title marks to known game/film titles.

    Contract: line-local high-precision first-pass. Requires title and cue on same line.
    Full recall is provided by AI title_candidates override (see module docstring).
    """
    for title, marked in sorted(KNOWN_TITLES.items(), key=lambda x: -len(x[0])):
        if title not in text:
            continue
        if _is_tool(title):
            continue
        if _has_cue(text, GAME_CUES + FILM_CUES):
            text = text.replace(title, marked)
    return text


if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        line = line.strip()
        if line:
            print(mark_titles(line))
        else:
            print()
