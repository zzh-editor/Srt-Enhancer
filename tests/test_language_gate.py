import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import enhance
from enhance import _has_cjk, step_capitalization, step_terminology


class TestTableLanguageGate(unittest.TestCase):
    """correction-table.md 与「大小写校准」的条目来自中文语境（next→Legacy、
    material→Material），靠周围中文消歧。纯英文段落没有这层上下文，套用会
    误伤普通词，因此表格条目只作用于含中文的段落。"""

    def setUp(self):
        self._orig = (enhance.load_terminology, enhance.load_capitalization_table)
        enhance.load_terminology = lambda *a, **k: {"next": "Legacy", "mean": "Min"}
        enhance.load_capitalization_table = lambda *a, **k: (
            {"material": "Material", "texture": "Texture"},
            {"brand_tool": {"point": "Point"}},
        )

    def tearDown(self):
        (enhance.load_terminology,
         enhance.load_capitalization_table) = self._orig

    def test_english_segment_skips_table_terminology(self):
        segs = [{"text": "So, the next question was how"},
                {"text": "I mean, how you build a sense of space."}]
        out = step_terminology(segs, {"domain": "substance"})
        self.assertEqual([s["text"] for s in out],
                         ["So, the next question was how",
                          "I mean, how you build a sense of space."])

    def test_chinese_segment_still_applies_table_terminology(self):
        out = step_terminology([{"text": "下一个 next 问题"}], {})
        self.assertEqual(out[0]["text"], "下一个 Legacy 问题")

    def test_english_segment_skips_table_capitalization(self):
        segs = [{"text": "the wood material and the texture"}]
        out = step_capitalization(segs, {"domain": "substance"})
        self.assertEqual(out[0]["text"], "the wood material and the texture")

    def test_chinese_segment_applies_table_capitalization(self):
        segs = [{"text": "这个 material 的 point"}]
        out = step_capitalization(segs, {"domain": "substance"})
        self.assertEqual(out[0]["text"], "这个 Material 的 Point")

    def test_terminology_overrides_apply_to_english_segments(self):
        out = step_terminology(
            [{"text": "and the turn sheet"}],
            {"terminology_overrides": {"turn sheet": "trim sheet"}})
        self.assertEqual(out[0]["text"], "and the trim sheet")

    def test_capitalization_overrides_apply_to_english_segments(self):
        out = step_capitalization(
            [{"text": "in substance channels"}],
            {"capitalization_overrides": {"substance": "Substance"}})
        self.assertEqual(out[0]["text"], "in Substance channels")

    def test_has_cjk(self):
        self.assertTrue(_has_cjk("中英 mixed"))
        self.assertFalse(_has_cjk("English only 123"))


if __name__ == "__main__":
    unittest.main()
