import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from vertical import invalid_split_keys


class TestSplitsSchemaGuard(unittest.TestCase):
    def test_chunk_lists_are_accepted(self):
        self.assertEqual(invalid_split_keys({"1": ["大家好", "今天"], "2": ["流程"]}), [])

    def test_video_transcribe_splits_json_is_rejected(self):
        splits = {
            "1": {"text": "大家好", "safe_cuts": [{"char": 2}], "selected_cuts": []},
            "_merge_candidates": [{"segments": [1, 2]}],
        }
        self.assertEqual(invalid_split_keys(splits), ["1"])

    def test_mixed_chunk_types_are_rejected(self):
        self.assertEqual(invalid_split_keys({"3": ["a", 2]}), ["3"])

    def test_non_dict_root_is_rejected(self):
        self.assertEqual(invalid_split_keys(["1"]), ["<root>"])


if __name__ == "__main__":
    unittest.main()


class TestHeuristicBalance(unittest.TestCase):
    def test_split_is_balanced_not_wide_plus_orphan(self):
        from vertical import _heuristic_split
        chunks = _heuristic_split("公司其实都很饱和的不招人了", 12)
        self.assertTrue(all(len(c) <= 12 for c in chunks), chunks)
        self.assertTrue(all(len(c) >= 4 for c in chunks), chunks)
        self.assertEqual("".join(chunks), "公司其实都很饱和的不招人了")

    def test_orphan_tail_is_folded(self):
        from vertical import _heuristic_split
        chunks = _heuristic_split("一二三四五六七八九十十一十二十三", 12)
        self.assertTrue(all(len(c) > 2 for c in chunks), chunks)
        self.assertEqual("".join(chunks), "一二三四五六七八九十十一十二十三")


class TestBoundarySpaceAndWidth(unittest.TestCase):
    def test_cjk_latin_space_survives_split(self):
        from vertical import split_segment
        seg = {"idx": 1, "start": 0.0, "end": 2.0,
               "text": "所以你在 LinkedIn 和官网上看到"}
        out = split_segment(seg, ["所以你在", "LinkedIn", "和官网上看到"])
        self.assertEqual("".join(i["text"] for i in out), "所以你在 LinkedIn 和官网上看到")

    def test_overflow_line_warns(self):
        import contextlib
        import io
        from vertical import apply_splits
        seg = {"idx": 1, "start": 0.0, "end": 4.0, "text": "所以你在 LinkedInX 和官网上看到"}
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            out = apply_splits([seg], {"1": ["所以你在 LinkedInX", "和官网上看到"]}, 12, 800)
        self.assertEqual(len(out), 2)
        self.assertIn("warning: cue 1 is 13 chars", err.getvalue())
