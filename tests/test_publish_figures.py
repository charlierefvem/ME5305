"""Exercise stale-source and push-race handling without touching a remote."""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import publish_figures as publisher


class PublicationTests(unittest.TestCase):
    def publish(self, remotes, *, push_fails=False, paths=None):
        self.calls = []
        remotes = iter(remotes)
        if paths is None:
            paths = ["notes/Images/nested/a.svg", "figures/svg-manifest.json"]

        def git(*args, **kwargs):
            self.calls.append(args)
            stdout, code = "", 0
            if args[0] == "rev-parse":
                stdout = "source\n"
            elif args[0] == "ls-remote":
                stdout = next(remotes) + "\trefs/heads/main\n"
            elif args == ("diff", "--cached", "--quiet"):
                code = 1
            elif args[0] == "push" and push_fails:
                code = 1
            return subprocess.CompletedProcess(args, code, stdout, "push rejected" if code else "")

        report = json.dumps({"status": "passed", "changed_paths": paths})
        with patch.dict(os.environ, GITHUB_ACTIONS="true", GITHUB_REF="refs/heads/main"), \
                patch.object(publisher.Path, "read_text", return_value=report), \
                patch.object(publisher, "git", side_effect=git):
            return publisher.main()

    def test_stale_source_never_commits_or_pushes(self):
        self.assertEqual(self.publish(["new-source"]), 75)
        self.assertFalse(any(call[0] in ("add", "commit", "push") for call in self.calls))

    def test_push_race_requests_fresh_conversion(self):
        self.assertEqual(self.publish(["source", "new-source"], push_fails=True), 75)
        self.assertEqual([c for c in self.calls if c[0] == "push"],
                         [("push", "origin", "HEAD:refs/heads/main")])

    def test_permission_failure_is_not_retried_as_a_race(self):
        with self.assertRaisesRegex(RuntimeError, "branch permissions"):
            self.publish(["source", "source"], push_fails=True)

    def test_only_reported_generated_paths_are_staged(self):
        self.publish(["source"])
        self.assertIn(("add", "--", "notes/Images/nested/a.svg", "figures/svg-manifest.json"), self.calls)

    def test_unchanged_batch_does_not_commit(self):
        self.publish([], paths=[])
        self.assertEqual(self.calls, [])

    def test_unexpected_path_cannot_be_staged(self):
        with self.assertRaisesRegex(RuntimeError, "Unexpected generated path"):
            self.publish([], paths=["notes/.obsidian/appearance.json"])
        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
