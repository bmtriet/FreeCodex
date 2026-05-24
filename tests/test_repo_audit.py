from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import repo_audit  # noqa: E402

import llm_gateway  # noqa: E402
import scout_leads  # noqa: E402
import mission_control  # noqa: E402
import llm_coworker  # noqa: E402


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

    def test_local_private_config_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            local_dir = root / "local"
            local_dir.mkdir()
            fake_key = "sk-" + "test" + "A" * 32
            (local_dir / "llmgate.env").write_text(f"LLMGATE_API_KEY={fake_key}\n", encoding="utf-8")
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "SECURITY.md").write_text("# Security\n", encoding="utf-8")
            (root / ".gitignore").write_text("local/\n", encoding="utf-8")

            findings = repo_audit.audit_path(root)

            self.assertFalse(any("local/llmgate.env" in finding.path for finding in findings))
            self.assertFalse(any("OpenAI" in finding.title for finding in findings))

    def test_llm_gateway_env_parser(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env_path = Path(tmp) / "gateway.env"
            env_path.write_text(
                "# comment\n"
                "LLMGATE_BASE_URL=https://example.test/v1\n"
                "LLMGATE_API_KEY=local-demo\n",
                encoding="utf-8",
            )

            values = llm_gateway.parse_env_file(env_path)

            self.assertEqual(values["LLMGATE_BASE_URL"], "https://example.test/v1")
            self.assertEqual(values["LLMGATE_API_KEY"], "local-demo")

    def test_scout_leads_normalizes_comment_urls(self) -> None:
        url = "https://github.com/example/project/issues/12#issuecomment-12345"

        self.assertEqual(
            scout_leads.normalize_github_url(url),
            "https://github.com/example/project/issues/12",
        )

    def test_scout_leads_extracts_repo_from_url(self) -> None:
        url = "https://github.com/example/project/pull/7#discussion_r1"

        self.assertEqual(scout_leads.repo_from_github_url(url), "example/project")

    def test_mission_control_counts_only_sent_threads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sent_dir = Path(tmp)
            (sent_dir / "run.md").write_text(
                "Public URL: https://github.com/example/app/issues/1#issuecomment-123\n"
                "PR opened: https://github.com/example/app/pull/2\n"
                "Held candidate: https://github.com/example/blocked/issues/9\n",
                encoding="utf-8",
            )

            summary = mission_control.collect_sent_logs(sent_dir)

            self.assertEqual(summary.files, 1)
            self.assertEqual(summary.issue_comments, ["https://github.com/example/app/issues/1"])
            self.assertEqual(summary.prs, ["https://github.com/example/app/pull/2"])
            self.assertNotIn("https://github.com/example/blocked/issues/9", summary.threads)

    def test_mission_control_extracts_outcome_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sent_dir = Path(tmp)
            (sent_dir / "run.md").write_text(
                "Public URL: https://github.com/example/app/issues/1#issuecomment-123\n"
                "PR opened: https://github.com/example/app/pull/2\n",
                encoding="utf-8",
            )

            refs = mission_control.extract_outcome_refs(sent_dir)

            self.assertEqual(len(refs), 2)
            self.assertEqual(refs[0].kind, "issue_comment")
            self.assertEqual(refs[0].normalized_url, "https://github.com/example/app/issues/1")
            self.assertEqual(refs[0].comment_id, 123)
            self.assertEqual(refs[1].kind, "pull_request")
            self.assertEqual(refs[1].normalized_url, "https://github.com/example/app/pull/2")

    def test_mission_control_sanitizes_lookup_errors(self) -> None:
        self.assertEqual(mission_control.sanitize_lookup_error("HTTP 404 Not Found /Users/name"), "not_found_or_inaccessible")
        self.assertEqual(mission_control.sanitize_lookup_error("please run gh auth login"), "auth_required_or_forbidden")
        self.assertEqual(mission_control.sanitize_lookup_error("secondary rate limit"), "rate_limited")
        self.assertEqual(mission_control.sanitize_lookup_error("network path /Users/name failed"), "lookup_failed")

    def test_mission_control_sanitizes_local_scout_excerpt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "next-leads.md"
            path.write_text(
                "Fit - safe\n"
                "Curly \u201cquote\u201d and dash \u2014 ok\n"
                "Payment https://www.paypal.com/paypalme/example\n",
                encoding="utf-8",
            )

            excerpt = mission_control.read_local_scout_excerpt(path)

            self.assertEqual(excerpt, ["Fit - safe", 'Curly "quote" and dash - ok'])

    def test_llm_coworker_denies_local_context(self) -> None:
        with self.assertRaises(llm_coworker.PolicyError):
            llm_coworker.read_context_file(Path("local/llmgate.env"))

    def test_llm_coworker_rejects_denied_diff_target(self) -> None:
        diff = "--- a/local/demo.txt\n+++ b/local/demo.txt\n@@ -1 +1 @@\n-old\n+new\n"

        with self.assertRaises(llm_coworker.PolicyError):
            llm_coworker.extract_diff(diff)

    def test_llm_coworker_validates_review_sections(self) -> None:
        review = "# Summary\nOk\n# Findings\nNone\n# Suggested Changes\nNone\n# Risks\nLow\n"

        self.assertEqual(llm_coworker.validate_review(review), review)


if __name__ == "__main__":
    unittest.main()
