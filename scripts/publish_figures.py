"""Commit exactly the converter's output, using compare-and-swap publication.

Runs in the disposable Actions checkout, not in an author's working tree.
On a push race, return 75 so the orchestrator can use a fresh worktree.
Never rebase generated assets onto different inputs.
"""
import json
import os
from pathlib import Path
import subprocess
import sys


def git(*args, check=True):
    return subprocess.run(["git", *args], check=check, capture_output=True, text=True)


def main():
    if os.environ.get("GITHUB_ACTIONS") != "true" or os.environ.get("GITHUB_REF") != "refs/heads/main":
        raise RuntimeError("Publication is restricted to the main-branch GitHub Action")
    report = json.loads(Path(".figure-build/report.json").read_text())
    if report["status"] != "passed":
        raise RuntimeError("Cannot publish a failed conversion batch")
    paths = report["changed_paths"]
    if any(p != "figures/svg-manifest.json" and not (p.startswith("notes/Images/") and p.endswith(".svg")) for p in paths):
        raise RuntimeError("Unexpected generated path")
    if not paths:
        print("No generated changes to commit")
        return
    if git("diff", "--cached", "--name-only").stdout.strip():
        raise RuntimeError("Unexpected pre-existing staged changes")
    source = git("rev-parse", "HEAD").stdout.strip()
    remote = git("ls-remote", "origin", "refs/heads/main").stdout.split()[0]
    if remote != source:
        print("Main advanced; recompute from the latest sources in a fresh worktree.")
        return 75
    git("add", "--", *paths)
    git("diff", "--cached", "--check")
    if not git("diff", "--cached", "--quiet", check=False).returncode:
        return
    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    git("commit", "-m", f"Generate SVG figures from PDFs\n\nSource: {source}")
    pushed = git("push", "origin", "HEAD:refs/heads/main", check=False)
    if pushed.returncode:
        remote = git("ls-remote", "origin", "refs/heads/main").stdout.split()[0]
        if remote != source:
            print("Main advanced during publication. No force push performed.")
            return 75
        raise RuntimeError(f"Generated commit could not be pushed (check branch permissions):\n{pushed.stderr}")
    print(pushed.stdout + pushed.stderr)


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except (RuntimeError, subprocess.SubprocessError, OSError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
