import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import audit


class TestAuditExitStatus(unittest.TestCase):
    def _write_srt(self, path: Path, text: str) -> None:
        path.write_text(
            f"1\n00:00:00,000 --> 00:00:01,000\n{text}\n",
            encoding="utf-8",
        )

    def test_warning_only_dot_chain_does_not_fail_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory) / "raw.srt"
            enhanced = Path(directory) / "enhanced.srt"
            self._write_srt(raw, "foo.bar.baz")
            self._write_srt(enhanced, "foo.bar.qux")
            with patch.object(sys, "argv", [
                "audit.py", str(enhanced), "--raw", str(raw),
            ]), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(audit.main(), 0)

    def test_error_signal_fails_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            enhanced = Path(directory) / "enhanced.srt"
            self._write_srt(enhanced, "whatEVr")
            with patch.object(sys, "argv", ["audit.py", str(enhanced)]), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(audit.main(), 1)


if __name__ == "__main__":
    unittest.main()
