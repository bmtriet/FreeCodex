from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import repo_audit  # noqa: E402


class RepoAuditTests(unittest.TestCase):
    def test_redacts_fake_secret_in_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "SECURITY.md").write_text("# Security\n", encoding="utf-8")
            (root / ".gitignore").write_text(".env\n", encoding="utf-8")
            fake_key = "sk-" + "test" + "A" * 32
            (root / "config.py").write_text(f'OPENAI_API_KEY="{fake_key}"\n', encoding="utf-8")

            findings = repo_audit.audit_path(root)
            report = repo_audit.render_report(root, findings)

            self.assertTrue(any("OpenAI" in finding.title for finding in findings))
            self.assertNotIn(fake_key, report)
            self.assertIn("[REDACTED:OpenAI key]", report)

    def test_missing_launch_files_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            findings = repo_audit.audit_path(Path(tmp))
            titles = {finding.title for finding in findings}

            self.assertIn("README is missing", titles)
            self.assertIn("License is missing", titles)
            self.assertIn("Security policy is missing", titles)

    def test_agentic_workflow_prompt_risk_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflow_dir = root / ".github" / "workflows"
            workflow_dir.mkdir(parents=True)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "SECURITY.md").write_text("# Security\n", encoding="utf-8")
            (root / ".gitignore").write_text(".env\n", encoding="utf-8")
            (workflow_dir / "agent.yml").write_text(
                "name: Agent\n"
                "on: issues\n"
                "jobs:\n"
                "  run:\n"
                "    steps:\n"
                "      - run: echo '${{ github.event.issue.body }}' | codex prompt\n",
                encoding="utf-8",
            )

            findings = repo_audit.audit_path(root)

            self.assertTrue(any("untrusted GitHub text" in finding.title for finding in findings))

    def test_hidden_unicode_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "SECURITY.md").write_text("# Security\n", encoding="utf-8")
            (root / ".gitignore").write_text(".env\n", encoding="utf-8")
            hidden = chr(0x202E)
            (root / "SKILL.md").write_text(f"# Skill\n{hidden} hidden control\n", encoding="utf-8")

            findings = repo_audit.audit_path(root)

            self.assertTrue(any("Hidden Unicode" in finding.title for finding in findings))


if __name__ == "__main__":
    unittest.main()

