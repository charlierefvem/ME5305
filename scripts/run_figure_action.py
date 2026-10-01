"""Run the CI batch in fresh, project-local worktrees with bounded push retries."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def command(args, cwd=ROOT, check=True):
    return subprocess.run(args, cwd=cwd, check=check)


def main():
    if os.environ.get("GITHUB_ACTIONS") != "true" or os.environ.get("GITHUB_REF") != "refs/heads/main":
        raise RuntimeError("This orchestrator is only for the main-branch GitHub Action")
    report = ROOT / ".figure-build/report.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, 4):
        command(["git", "fetch", "origin", "main"])
        checkout = ROOT / f".figure-build/attempt-{attempt}"
        command(["git", "worktree", "add", "--detach", str(checkout), "origin/main"])
        home = checkout / ".figure-build/home"
        home.mkdir(parents=True)
        # Mount the enclosing checkout at its original path so Git worktree
        # metadata remains accessible. All generated files stay inside it.
        docker = ["docker", "run", "--rm", "--user", f"{os.getuid()}:{os.getgid()}",
                  "-e", f"HOME={home}", "-v", f"{ROOT}:{ROOT}", "-w", str(checkout), "me5305-figures"]
        try:
            # Rebuild when a racing source commit changes the locked toolchain.
            command(["docker", "build", "-t", "me5305-figures", "scripts/figure-toolchain"], cwd=checkout)
            command([*docker, "python", "-B", "-m", "unittest", "discover", "-s", "tests", "-v"])
            flags = ["--force"] if os.environ.get("FORCE") == "true" else []
            command([*docker, "python", "-B", "scripts/convert_figures.py", "--visual-check", *flags])
            result = command([sys.executable, "-B", "scripts/publish_figures.py"], cwd=checkout, check=False)
        finally:
            candidate = checkout / ".figure-build/report.json"
            if candidate.exists():
                shutil.copyfile(candidate, report)
            else:
                report.write_text(json.dumps({"status": "failed", "error": f"Toolchain or tests failed on attempt {attempt}"}))
        if result.returncode == 75:
            continue
        data = json.loads(report.read_text())
        data["publication"] = "completed" if result.returncode == 0 else "failed"
        data["attempts"] = attempt
        report.write_text(json.dumps(data, indent=2) + "\n")
        result.check_returncode()
        return
    data = json.loads(report.read_text())
    data["publication"] = "superseded after three attempts; rerun on current main"
    report.write_text(json.dumps(data, indent=2) + "\n")
    raise RuntimeError("Main changed during all three attempts; no stale result was pushed")


if __name__ == "__main__":
    main()
