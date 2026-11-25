import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from enhance import step_defiller, write_srt
from vertical import attach_word_timestamps, split_segment, write_srt as write_vertical_srt


class TestMillisecondSerialization(unittest.TestCase):
    def test_enhancer_writer_rounds_milliseconds(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "out.srt"
            write_srt([{"start": 12.019, "end": 13.021, "text": "字幕"}], str(path))
            self.assertIn("00:00:12,019 --> 00:00:13,021", path.read_text())

    def test_vertical_writer_rounds_milliseconds(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "out.srt"
            write_vertical_srt([{"start": 12.019, "end": 13.021, "text": "字幕"}], str(path))
            self.assertIn("00:00:12,019 --> 00:00:13,021", path.read_text())


class TestWordAlignedVerticalSplit(unittest.TestCase):
    def test_short_cue_splits_every_chunk_without_dropping_text(self):
        seg = {"idx": 1, "start": 0.0, "end": 0.1, "text": "甲乙丙丁"}
        out = split_segment(seg, ["甲", "乙", "丙", "丁"])

        self.assertEqual([item["text"] for item in out], ["甲", "乙", "丙", "丁"])
        self.assertEqual((out[0]["start"], out[-1]["end"]), (0.0, 0.1))
        self.assertTrue(all(item["start"] < item["end"] for item in out))

    def test_nonmatching_chunks_fall_back_to_original(self):
        seg = {"idx": 1, "start": 0.0, "end": 1.0, "text": "原字幕"}
        self.assertEqual(split_segment(seg, ["其他文本"]), [seg])

    def test_attaches_matching_words_and_uses_word_boundaries(self):
        segments = [{"idx": 1, "start": 0.0, "end": 1.0, "text": "今天我们"}]
        words = [{"start": 0.0, "end": 1.0, "words": [
            {"word": "今天", "start": 0.0, "end": 0.4},
            {"word": "我们", "start": 0.5, "end": 1.0},
        ]}]
        attach_word_timestamps(segments, words)
        out = split_segment(segments[0], ["今天", "我们"])
        self.assertEqual([(item["start"], item["end"]) for item in out],
                         [(0.0, 0.4), (0.4, 1.0)])

    def test_mismatch_falls_back_to_proportional_timing(self):
        seg = {"idx": 1, "start": 0.0, "end": 1.0, "text": "今天我们",
               "words": [{"word": "今天你们", "start": 0.0, "end": 1.0}]}
        out = split_segment(seg, ["今天", "我们"])
        self.assertEqual(len(out), 2)
        self.assertAlmostEqual(out[0]["end"], 0.5)

    def test_word_timing_preserves_original_cue_bounds(self):
        seg = {"idx": 1, "start": 0.0, "end": 1.0, "text": "今天我们",
               "words": [
                   {"word": "今天", "start": 0.1, "end": 0.4},
                   {"word": "我们", "start": 0.6, "end": 0.9},
               ]}
        out = split_segment(seg, ["今天", "我们"])
        self.assertEqual((out[0]["start"], out[-1]["end"]), (0.0, 1.0))


class TestConservativeDefiller(unittest.TestCase):
    def _clean(self, text):
        segments = [{"text": text}]
        step_defiller(segments, {"discourse_markers": []})
        return segments[0]["text"]

    def test_removes_leading_filler_but_preserves_interjection(self):
        self.assertEqual(self._clean("嗯今天开始"), "今天开始")
        self.assertEqual(self._clean("哎呀今天开始"), "哎呀今天开始")

    def test_removes_isolated_filler_but_not_cjk_embedded_sound(self):
        self.assertEqual(self._clean("我们 嗯 继续"), "我们 继续")
        self.assertEqual(self._clean("我们嗯继续"), "我们嗯继续")


if __name__ == "__main__":
    unittest.main()


class TestHotkeyProtection(unittest.TestCase):
    def test_spacing_keeps_hotkey_glued(self):
        from apply_spacing import apply_spacing
        self.assertEqual(apply_spacing("hit ctrl+e to export"), "hit ctrl+e to export")
        self.assertEqual(apply_spacing("按ctrl+shift+z回退"), "按ctrl+shift+z回退")

    def test_hotkey_step_still_normalizes(self):
        from enhance import step_hotkeys
        segs = [{"start": 0.0, "end": 1.0, "text": "hit ctrl+e to export"}]
        self.assertEqual(step_hotkeys(segs, {})[0]["text"], "hit Ctrl+E to export")


class TestVerticalMinDuration(unittest.TestCase):
    def test_chunks_get_min_duration_when_it_fits(self):
        seg = {"idx": 1, "start": 0.0, "end": 4.0, "text": "一二三四五六七八九十十一"}
        out = split_segment(seg, ["一二三", "四五六", "七八九", "十十一"], min_ms=800)
        self.assertEqual(len(out), 4)
        self.assertTrue(all(b["end"] - b["start"] >= 0.799 for b in out), out)
        self.assertEqual("".join(b["text"] for b in out), "一二三四五六七八九十十一")
