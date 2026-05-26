import json
import tempfile
import unittest
from pathlib import Path

import codex_cost_guard as guard


class CodexCostGuardTests(unittest.TestCase):
    def test_scans_transcript_and_flags_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            transcript = "\n".join(["user: please continue", "assistant: " + ("hello " * 1000)] * 5)
            (root / "session.log").write_text(transcript)
            sessions = guard.scan(root, price_per_million=2.5, max_tokens=100, warn_turns=3)

        self.assertEqual(len(sessions), 1)
        self.assertIn("token budget exceeded", sessions[0].risks)
        self.assertIn("long agent session", sessions[0].risks)

    def test_sarif_serializes(self):
        session = guard.Session("session.log", 1000, 250, 0.001, 2, ["token budget exceeded"])
        data = guard.sarif([session])
        self.assertEqual(data["version"], "2.1.0")
        self.assertEqual(len(data["runs"][0]["results"]), 1)
        json.dumps(data)


if __name__ == "__main__":
    unittest.main()
