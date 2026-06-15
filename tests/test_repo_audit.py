from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import repo_audit  # noqa: E402

import llm_gateway  # noqa: E402
import scout_leads  # noqa: E402
import scout_big_repos  # noqa: E402
import mission_control  # noqa: E402
import llm_coworker  # noqa: E402
import prepare_subagent_brief  # noqa: E402


class RepoAuditTests(unittest.TestCase):
    def write_minimal_launch_files(self, root: Path) -> None:
        workflow_dir = root / ".github" / "workflows"
        workflow_dir.mkdir(parents=True)
        (root / "README.md").write_text("# Demo\n", encoding="utf-8")
        (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
        (root / "SECURITY.md").write_text("# Security\n", encoding="utf-8")
        (root / ".gitignore").write_text(".env\n", encoding="utf-8")
        (root / ".env.example").write_text("APP_ENV=local\n", encoding="utf-8")
        (root / "package.json").write_text('{"scripts":{"test":"echo ok"}}\n', encoding="utf-8")
        (workflow_dir / "ci.yml").write_text("name: CI\non: [push]\n", encoding="utf-8")

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

    def test_static_headers_missing_csp_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_minimal_launch_files(root)
            public_dir = root / "public"
            public_dir.mkdir()
            (public_dir / "_headers").write_text(
                "/*\n"
                "  X-Frame-Options: DENY\n"
                "  X-Content-Type-Options: nosniff\n",
                encoding="utf-8",
            )

            findings = repo_audit.audit_path(root)

            self.assertTrue(
                any(
                    finding.title == "Static hosting header/config file detected without obvious Content-Security-Policy"
                    and finding.path == "public/_headers"
                    for finding in findings
                )
            )

    def test_static_headers_with_csp_are_not_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_minimal_launch_files(root)
            public_dir = root / "public"
            public_dir.mkdir()
            (public_dir / "_headers").write_text(
                "/*\n"
                "  Content-Security-Policy: default-src 'self'; frame-ancestors 'none'\n",
                encoding="utf-8",
            )

            findings = repo_audit.audit_path(root)

            self.assertFalse(
                any("Content-Security-Policy" in finding.title for finding in findings)
            )

    def test_static_headers_csp_comment_does_not_suppress_finding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_minimal_launch_files(root)
            public_dir = root / "public"
            public_dir.mkdir()
            (public_dir / "_headers").write_text(
                "/*\n"
                "  # Content-Security-Policy: TODO\n"
                "  X-Content-Type-Options: nosniff\n",
                encoding="utf-8",
            )

            findings = repo_audit.audit_path(root)

            self.assertTrue(
                any("without obvious Content-Security-Policy" in finding.title for finding in findings)
            )

    def test_block_commented_csp_does_not_suppress_static_header_finding(self) -> None:
        config_cases = {
            "public/_headers": (
                "/*\n"
                "  Content-Security-Policy: default-src 'self'\n"
                "*/\n"
                "/*\n"
                "  X-Content-Type-Options: nosniff\n"
            ),
            "netlify.toml": (
                "[[headers]]\n"
                "  for = \"/*\"\n"
                "  /*\n"
                "  Content-Security-Policy = \"default-src 'self'\"\n"
                "  */\n"
                "  [headers.values]\n"
                "    X-Frame-Options = \"DENY\"\n"
            ),
            "vercel.json": (
                "{\"headers\":[{\"source\":\"/(.*)\",\"headers\":["
                "/* {\"key\":\"Content-Security-Policy\",\"value\":\"default-src self\"}, */"
                "{\"key\":\"X-Frame-Options\",\"value\":\"DENY\"}]}]}\n"
            ),
        }
        for name, content in config_cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.write_minimal_launch_files(root)
                config_path = root / name
                config_path.parent.mkdir(parents=True, exist_ok=True)
                config_path.write_text(content, encoding="utf-8")

                findings = repo_audit.audit_path(root)

                self.assertTrue(
                    any("without obvious Content-Security-Policy" in finding.title for finding in findings)
                )

    def test_frontend_without_static_header_config_has_no_csp_finding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_minimal_launch_files(root)
            (root / "index.html").write_text("<main>Demo</main>\n", encoding="utf-8")
            src_dir = root / "src"
            src_dir.mkdir()
            (src_dir / "main.ts").write_text("console.log('demo')\n", encoding="utf-8")

            findings = repo_audit.audit_path(root)

            self.assertFalse(
                any("Content-Security-Policy" in finding.title for finding in findings)
            )

    def test_static_deploy_configs_missing_csp_are_reported(self) -> None:
        config_cases = {
            "netlify.toml": (
                "[[headers]]\n"
                "  for = \"/*\"\n"
                "  [headers.values]\n"
                "    X-Frame-Options = \"DENY\"\n"
            ),
            "vercel.json": (
                "{\"headers\":[{\"source\":\"/(.*)\",\"headers\":["
                "{\"key\":\"X-Frame-Options\",\"value\":\"DENY\"}]}]}\n"
            ),
        }
        for name, content in config_cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.write_minimal_launch_files(root)
                (root / name).write_text(content, encoding="utf-8")

                findings = repo_audit.audit_path(root)

                self.assertTrue(
                    any(
                        finding.title
                        == "Static hosting header/config file detected without obvious Content-Security-Policy"
                        and finding.path == name
                        for finding in findings
                    )
                )

    def test_deploy_configs_without_header_blocks_do_not_trigger_csp_finding(self) -> None:
        config_cases = {
            "netlify.toml": "[build]\n  command = \"npm run build\"\n",
            "vercel.json": "{\"rewrites\":[]}\n",
        }
        for name, content in config_cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.write_minimal_launch_files(root)
                (root / name).write_text(content, encoding="utf-8")

                findings = repo_audit.audit_path(root)

                self.assertFalse(
                    any("Content-Security-Policy" in finding.title for finding in findings)
                )

    def test_static_csp_finding_does_not_leak_header_file_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_minimal_launch_files(root)
            public_dir = root / "public"
            public_dir.mkdir()
            fake_secret = "sk-" + "test" + "B" * 32
            (public_dir / "_headers").write_text(
                "/*\n"
                f"  X-Debug-Token: {fake_secret}\n",
                encoding="utf-8",
            )

            findings = repo_audit.audit_path(root)
            report = repo_audit.render_report(root, findings)
            csp_findings = [
                finding
                for finding in findings
                if "without obvious Content-Security-Policy" in finding.title
            ]

            self.assertEqual(csp_findings[0].evidence, "_headers")
            self.assertNotIn(fake_secret, csp_findings[0].evidence)
            self.assertNotIn(fake_secret, report)

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

    def test_big_repo_candidate_compact_includes_scale(self) -> None:
        candidate = scout_big_repos.BigCandidate(
            repo="example/project",
            repo_url="https://github.com/example/project",
            stars=12000,
            forks=1500,
            pushed_at="2026-06-01T00:00:00Z",
            security_policy_enabled=True,
            description="AI workflow platform",
            issue_title="Add security headers",
            issue_url="https://github.com/example/project/issues/1",
            updated_at="2026-06-02T00:00:00Z",
            labels=["security"],
            query="example/project:security headers",
            body="Please add Content-Security-Policy.",
        )

        compact = candidate.compact()

        self.assertEqual(compact["stars"], 12000)
        self.assertEqual(compact["forks"], 1500)
        self.assertEqual(compact["security_policy_enabled"], True)
        self.assertEqual(compact["body_excerpt"], "")

    def test_big_repo_run_json_wraps_invalid_json(self) -> None:
        completed = mock.Mock(stdout="not-json")

        with mock.patch.object(scout_big_repos.subprocess, "run", return_value=completed):
            with self.assertRaises(scout_big_repos.CommandError):
                scout_big_repos.run_json(["gh", "issue", "list"], timeout=1)

    def test_big_repo_skips_contacted_repo_case_insensitive(self) -> None:
        args = mock.Mock()
        args.sent_dir = Path("leads/sent")
        args.include_contacted_repos = False
        args.repo = ["flowiseai/flowise"]
        args.command_timeout = 1
        args.min_stars = 0
        args.min_forks = 0
        args.min_watchers = 0
        args.term = ["security"]
        args.per_term = 1
        args.include_sensitive_hints = False
        args.max_candidates = 10

        with (
            mock.patch.object(scout_big_repos.scout_leads, "sent_urls", return_value=set()),
            mock.patch.object(
                scout_big_repos.scout_leads,
                "sent_repos",
                return_value={"FlowiseAI/Flowise"},
            ),
            mock.patch.object(scout_big_repos, "run_json") as run_json,
        ):
            candidates, warnings = scout_big_repos.search_big_candidates(args)

        self.assertEqual(candidates, [])
        self.assertEqual(warnings, [])
        run_json.assert_not_called()

    def test_big_repo_sort_prefers_security_keyword_and_scale(self) -> None:
        smaller_security = scout_big_repos.BigCandidate(
            repo="example/smaller",
            repo_url="https://github.com/example/smaller",
            stars=11000,
            forks=1000,
            pushed_at="",
            security_policy_enabled=True,
            description="",
            issue_title="Security headers",
            issue_url="https://github.com/example/smaller/issues/1",
            updated_at="2026-06-02T00:00:00Z",
            labels=[],
            query="security",
            body="Add CSP and CORS hardening.",
        )
        bigger_vague = scout_big_repos.BigCandidate(
            repo="example/bigger",
            repo_url="https://github.com/example/bigger",
            stars=90000,
            forks=9000,
            pushed_at="",
            security_policy_enabled=True,
            description="",
            issue_title="UI polish",
            issue_url="https://github.com/example/bigger/issues/2",
            updated_at="2026-06-03T00:00:00Z",
            labels=[],
            query="security",
            body="Make the page nicer.",
        )

        ordered = scout_big_repos.sort_candidates([bigger_vague, smaller_security])

        self.assertEqual(ordered[0].repo, "example/smaller")

    def test_big_repo_prompt_includes_large_repo_policy(self) -> None:
        prompt = scout_big_repos.build_prompt([], top_n=3)

        self.assertIn("Large active repos are preferred", prompt)
        self.assertIn("No outreach to minors", prompt)

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
                "Payment https://ko-fi.com/freecodex\n",
                encoding="utf-8",
            )

            excerpt = mission_control.read_local_scout_excerpt(path)

            self.assertEqual(excerpt, ["Fit - safe", 'Curly "quote" and dash - ok'])

    def test_mission_control_counts_kofi_payment_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sent_dir = Path(tmp)
            (sent_dir / "run.md").write_text(
                "Public URL: https://github.com/example/app/issues/1#issuecomment-123\n"
                "Payment https://ko-fi.com/freecodex\n",
                encoding="utf-8",
            )

            summary = mission_control.collect_sent_logs(sent_dir)

            self.assertEqual(summary.payment_mentions, 1)

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

    def test_prepare_subagent_brief_includes_policy_and_report_template(self) -> None:
        brief = prepare_subagent_brief.render_brief(
            "proof-worker",
            "Find one bounded useful public contribution.",
            "https://github.com/example/app/issues/1",
            max_chars_per_file=1200,
        )

        self.assertIn("# Sub-Agent Brief", brief)
        self.assertIn("- Name: proof-worker", brief)
        self.assertIn("Do not include payment links", brief)
        self.assertIn("templates/subagent-run-report.md", brief)
        self.assertIn("https://github.com/example/app/issues/1", brief)

    def test_prepare_subagent_brief_writes_output_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "brief.md"

            with mock.patch(
                "sys.argv",
                [
                    "prepare_subagent_brief.py",
                    "--role",
                    "evolution-distiller",
                    "--objective",
                    "Distill one repeated pattern.",
                    "--output",
                    str(output),
                ],
            ):
                self.assertEqual(prepare_subagent_brief.main(), 0)

            text = output.read_text(encoding="utf-8")
            self.assertIn("- Name: evolution-distiller", text)
            self.assertIn("Distill one repeated pattern.", text)


if __name__ == "__main__":
    unittest.main()
