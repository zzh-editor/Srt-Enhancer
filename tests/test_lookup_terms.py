import base64
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import enhance


class TestLookupTerms(unittest.TestCase):
    def setUp(self):
        self.mapping = {
            "Owatch": "Overwatch",
            "MultiViewReference": "Multi View Ref",
            "eve": "EV",
        }

    def test_reports_matches_known_correct_and_unmatched_terms(self):
        results = enhance.lookup_terms(
            ["Owatch", "Overwatch", "Multi View Reference", "Rodin"], self.mapping
        )

        self.assertEqual(
            [item["status"] for item in results],
            ["asr_match", "known_correct", "asr_match", "unmatched"],
        )
        self.assertEqual(results[2]["resolved"], "Multi View Ref")

    def test_lookup_uses_the_same_word_boundary_rule_as_enhancement(self):
        self.assertEqual(
            enhance.lookup_terms(["whatever"], {"eve": "EV"})[0]["status"],
            "unmatched",
        )

        output = enhance.step_terminology(
            [{"text": "whatever"}], {"terminology_overrides": {"eve": "EV"}}
        )
        self.assertEqual(output[0]["text"], "whatever")

    def test_context_only_conflict_is_reported_without_becoming_auto_mapping(self):
        with tempfile.TemporaryDirectory() as directory:
            table = Path(directory) / "correction-table.md"
            table.write_text(
                "| ASR 误识别 | 正确术语 | 说明 |\n|---|---|---|\n"
                "| TabDown / TypeNode | TypeNow ⚠️仅上下文判断 | 另一工具名候选 |\n",
                encoding="utf-8",
            )
            contextual = enhance.load_contextual_terminology(table)

        results = enhance.lookup_terms(
            ["TabDown"], {"TabDown": "TapNow"}, contextual_terms=contextual,
        )
        self.assertEqual(results[0]["resolved"], "TapNow")
        self.assertEqual(results[0]["contextual_matches"][0]["correct"], "TypeNow")
        self.assertEqual(
            enhance.load_terminology(table), {},
        )

    def test_real_context_only_rows_are_available_to_candidate_lookup(self):
        contexts = enhance.load_contextual_terminology()

        self.assertIn("TypeNode", contexts)
        self.assertEqual(contexts["TypeNode"][0]["correct"], "TypeNow")
        self.assertIn("Cloud", contexts)
        self.assertIn("width", contexts)

        width = enhance.lookup_terms(
            ["width"], enhance.load_terminology(), contextual_terms=contexts,
        )[0]
        self.assertEqual(width["status"], "unmatched")
        self.assertEqual(width["contextual_matches"][0]["correct"], "weights")

    def test_cli_lookup_accepts_base64_without_srt_input(self):
        output = io.StringIO()
        terms_json = json.dumps(["Owatch", "Rodin"], ensure_ascii=False)
        terms_b64 = base64.b64encode(terms_json.encode("utf-8")).decode("ascii")
        with patch.object(sys, "argv", ["enhance.py", "--lookup-terms-base64", terms_b64]), \
                patch("enhance.load_terminology", return_value=self.mapping), \
                contextlib.redirect_stdout(output):
            enhance.main()

        results = json.loads(output.getvalue())
        self.assertEqual([item["status"] for item in results], ["asr_match", "unmatched"])


if __name__ == "__main__":
    unittest.main()
