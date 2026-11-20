import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from enhance import step_depunct


def run(*texts):
    segs = [{"text": t} for t in texts]
    out = step_depunct(segs, {})
    return [s["text"] for s in out]


def test_latin_punct_cjk():
    """英文语气词后的逗号接中文时必须清理：OK,我们 → OK 我们。"""
    assert run("OK,我们这个时候先把这个模型") == ["OK 我们这个时候先把这个模型"]
    assert run("OK,把 Tool") == ["OK 把 Tool"]
    # 英文词后其他半角标点同样清理
    assert run("yes!好的") == ["yes 好的"]


def test_number_thousand_separator_kept():
    """数字千分位逗号不能被误删：3,500 个。"""
    assert run("大概有3,500 个") == ["大概有3,500 个"]


def test_latin_to_latin_untouched():
    """纯拉丁之间的标点不受影响：C++, A/B。"""
    assert run("A/B test") == ["A/B test"]


def test_cjk_trailing_punct_stripped():
    """中文后尾随逗号仍清理（回归既有行为）。"""
    assert run("OK,基本上,") == ["OK 基本上"]


def test_ok_trailing_punct_latin_only():
    """拉丁词尾的逗号（无中文跟随）保持不变，depunct 只处理 CJK 邻接。"""
    assert run("OK,") == ["OK,"]
