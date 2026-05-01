# Daily Paint

A tiny heartbeat repository that appends one dated line to `heartbeat.log`
every day and commits it. The point is to keep my GitHub contribution
graph reflecting that I'm still actively maintaining things.

## How it works

A scheduled GitHub Actions workflow runs [`daily_paint.py`](daily_paint.py)
once per day. The script:

1. Computes today's UTC date.
2. Skips out if `heartbeat.log` already has an entry for today
   (idempotent, so manual re-runs don't pile up junk commits).
3. Otherwise appends one line and commits with a message of the form
   `chore: daily activity update - YYYY-MM-DD`.
4. The workflow then pushes if and only if a new commit exists.

## Setup

1. **Create the repo.** Private is fine and recommended.

2. **Pick the email that will count toward your graph.** Either:
   - any verified email on <https://github.com/settings/emails>, or
   - your no-reply address, shown on the same page, of the form
     `12345678+yourusername@users.noreply.github.com`.

3. **Add repository variables** under
   *Settings -> Secrets and variables -> Actions -> Variables*:
   - `GIT_AUTHOR_NAME` -- the name you want on the commits.
   - `GIT_AUTHOR_EMAIL` -- the email from step 2.

4. **(Private repo only)** Turn on
   *Profile -> Settings -> Profile -> Contributions & activity ->
   Include private contributions on my profile*. Without this, the
   squares only appear when you're signed in as yourself.

5. **Push these three files** to `master`:
   - `daily_paint.py`
   - `.github/workflows/daily-paint.yml`
   - `README.md`

6. **Smoke test.** Open *Actions -> Daily Paint -> Run workflow*. A new
   commit should appear authored by the email you configured.

## Notes on the contribution graph

- Commits only count when they are on the **default branch** and the
  **author email** is one GitHub recognises as yours.
- The cron fires at `00:17 UTC`. GitHub may delay scheduled workflows
  during peak load, so an off-the-hour minute is more reliable than
  `00:00`. If your contribution day is off by one in your timezone,
  shift the cron earlier or later as needed.
- If the workflow doesn't run for a while (long inactivity periods),
  GitHub may auto-disable it. Re-enable from the Actions tab.

## Customization

`daily_paint.py` reads three optional environment variables:

| Variable             | Default                                       | Purpose                            |
|----------------------|-----------------------------------------------|------------------------------------|
| `HEARTBEAT_FILE`     | `heartbeat.log`                               | Path of the log file.              |
| `COMMIT_MESSAGE_FMT` | `chore: daily activity update - {date}`      | `str.format` template.             |
| `TIMEZONE_LABEL`     | `UTC`                                         | Label written into each log line.  |

Set them in the workflow's `env:` block if you want to change them.
