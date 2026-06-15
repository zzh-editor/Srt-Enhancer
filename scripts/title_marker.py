#!/usr/bin/env python3
"""Deterministic game/media title marking with 《》."""

import re

KNOWN_TITLES = {
    "黑神话：悟空": "《黑神话：悟空》",
    "黑神话悟空":    "《黑神话悟空》",
    "对马岛之魂":    "《对马岛之魂》",
    "原神":          "《原神》",
    "赛博朋克2077":  "《赛博朋克2077》",
    "赛博朋克":      "《赛博朋克》",
    "艾尔登法环":    "《艾尔登法环》",
    "只狼":          "《只狼》",
    "战神":          "《战神》",
    "最后生还者":    "《最后生还者》",
    "荒野大镖客":    "《荒野大镖客》",
    "巫师3":         "《巫师3》",
    "巫师三":        "《巫师三》",
    "死亡搁浅":      "《死亡搁浅》",
    "集合啦动物森友会": "《集合啦动物森友会》",
    "动物森友会":    "《动物森友会》",
    "宝可梦":        "《宝可梦》",
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
    """Add 《》 book-title marks to known game/film titles."""
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
