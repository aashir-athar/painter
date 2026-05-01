"""
daily_paint.py
==============

A small, well-behaved "heartbeat" script that keeps a GitHub contribution
graph active by appending a single dated line to a log file and committing
it to the default branch via GitHub Actions.

Why this works
--------------
GitHub counts a commit toward your contribution graph when ALL of:
  1. The commit is on the repository's default branch (here: ``master``).
  2. The commit's author email matches an email verified on your GitHub
     account, OR matches your GitHub no-reply address
     (``<id>+<username>@users.noreply.github.com``).
  3. For PRIVATE repos: "Include private contributions on my profile" must
     be enabled in your GitHub profile settings, otherwise the squares only
     show up to you when signed in.

This script is intentionally minimal. It writes one human-readable line
per run to ``heartbeat.log`` and commits it. It is idempotent within a
single UTC day: if today's date already has an entry, no new commit is
made (so manual re-runs don't pile up junk commits).

------------------------------------------------------------------------
SETUP (one-time)
------------------------------------------------------------------------

1. Create a new repository on GitHub.
   - PRIVATE is recommended (nothing here needs to be public).
   - Default branch: ``master`` (the workflow assumes this; change it in
     ``.github/workflows/daily-paint.yml`` if you use ``main``).

2. Configure your contribution-counting email.
   Pick ONE of:
     (a) A verified email on https://github.com/settings/emails, OR
     (b) Your GitHub no-reply email, found at the same page. It looks
         like:  12345678+yourusername@users.noreply.github.com
   Set it as a repository variable named ``GIT_AUTHOR_EMAIL`` under:
     Settings -> Secrets and variables -> Actions -> Variables -> New
   Also set ``GIT_AUTHOR_NAME`` to the name you want on commits.

3. (Private repo only) Enable contribution counting:
   Profile -> Settings -> Profile ->
     "Contributions & activity" -> tick
     "Include private contributions on my profile".

4. Add these three files to the repo root:
       daily_paint.py
       .github/workflows/daily-paint.yml
       README.md
   Commit and push to ``master``.

5. Verify it works:
   - Go to the repo's "Actions" tab.
   - Open the "Daily Paint" workflow and click "Run workflow".
   - Confirm a new commit appears authored by you.

------------------------------------------------------------------------
CUSTOMIZATION
------------------------------------------------------------------------

Environment variables (all optional):

  HEARTBEAT_FILE      Path to the log file. Default: ``heartbeat.log``.
  COMMIT_MESSAGE_FMT  ``str.format`` template; receives ``date`` and
                      ``time``. Default:
                      ``"chore: daily activity update - {date}"``.
  TIMEZONE_LABEL      Free-form label written into the log line for
                      human readers. Default: ``"UTC"``.

The script always uses UTC internally so behavior is deterministic
regardless of where the runner is hosted.
"""

from __future__ import annotations

import logging
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("daily-paint")


@dataclass(frozen=True)
class Config:
    heartbeat_file: Path
    commit_message_fmt: str
    timezone_label: str

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            heartbeat_file=Path(os.environ.get("HEARTBEAT_FILE", "heartbeat.log")),
            commit_message_fmt=os.environ.get(
                "COMMIT_MESSAGE_FMT", "chore: daily activity update - {date}"
            ),
            timezone_label=os.environ.get("TIMEZONE_LABEL", "UTC"),
        )


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a git command and capture its output."""
    result = subprocess.run(
        ["git", *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        log.error("git %s failed (exit %d)", " ".join(args), result.returncode)
        if result.stdout:
            log.error("stdout: %s", result.stdout.strip())
        if result.stderr:
            log.error("stderr: %s", result.stderr.strip())
        raise SystemExit(result.returncode)
    return result


def already_logged_today(path: Path, today_iso: str) -> bool:
    """Return True if the heartbeat file already has an entry for today."""
    if not path.exists():
        return False
    # Read in binary then decode to tolerate stray bytes; file is small.
    text = path.read_text(encoding="utf-8", errors="replace")
    # Each line begins with the ISO date, so a substring check at line
    # start is sufficient and fast.
    return any(line.startswith(today_iso) for line in text.splitlines())


def append_heartbeat(path: Path, now: datetime, tz_label: str) -> str:
    """Append a single dated line to the heartbeat file. Returns the line."""
    header = (
        "# heartbeat.log\n"
        "# One line per day. Maintained by daily_paint.py.\n\n"
    )
    line = f"{now.strftime('%Y-%m-%d')}  {now.strftime('%H:%M:%S')} {tz_label}\n"

    if not path.exists():
        path.write_text(header + line, encoding="utf-8")
    else:
        with path.open("a", encoding="utf-8") as fh:
            fh.write(line)
    return line.rstrip()


def has_staged_changes() -> bool:
    """True if there is anything staged for commit."""
    # `git diff --cached --quiet` exits 1 when there ARE staged changes.
    result = run_git("diff", "--cached", "--quiet", check=False)
    return result.returncode == 1


def main() -> int:
    cfg = Config.from_env()
    now = datetime.now(timezone.utc)
    today_iso = now.strftime("%Y-%m-%d")

    log.info("Heartbeat file: %s", cfg.heartbeat_file)
    log.info("UTC date: %s", today_iso)

    if already_logged_today(cfg.heartbeat_file, today_iso):
        log.info("Today's entry already present. Nothing to do.")
        return 0

    line = append_heartbeat(cfg.heartbeat_file, now, cfg.timezone_label)
    log.info("Appended: %s", line)

    run_git("add", "--", str(cfg.heartbeat_file))

    if not has_staged_changes():
        # Possible if the file's only delta was whitespace already
        # normalized by a hook. Treat as success without committing.
        log.info("No staged changes after add; skipping commit.")
        return 0

    message = cfg.commit_message_fmt.format(
        date=today_iso,
        time=now.strftime("%H:%M:%S"),
    )
    run_git("commit", "-m", message)
    log.info("Committed: %s", message)
    return 0


if __name__ == "__main__":
    sys.exit(main())
