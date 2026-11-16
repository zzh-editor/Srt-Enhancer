import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from domain_scanner import detect_domain, load_domains


class TestDomainKeywordBoundaries(unittest.TestCase):
    def setUp(self):
        self.domains = {
            "domains": {
                "general": {"keywords": [], "search_context": ""},
                "unreal": {"keywords": ["ue"], "search_context": "Unreal Engine"},
            },
        }

    def test_abbreviation_matches_version_suffix(self):
        self.assertEqual(detect_domain(["UE5 material"], self.domains), "unreal")

    def test_abbreviation_does_not_match_inside_english_words(self):
        self.assertEqual(
            detect_domain(["value, issue, true"], self.domains), "general"
        )

    def test_camelcase_tool_alias_remains_an_ai_3d_keyword(self):
        self.assertEqual(detect_domain(["typenow"], load_domains()), "ai-3d")


if __name__ == "__main__":
    unittest.main()
