<div align="center">

<h1>🎨 painter</h1>

<p><strong>Keep your GitHub contribution graph alive — a tiny Python + GitHub Actions cron bot that commits one dated heartbeat line every day, automatically.</strong></p>

[![Last commit](https://img.shields.io/github/last-commit/aashir-athar/painter/master?style=for-the-badge&logo=github)](https://github.com/aashir-athar/painter/commits/master)
[![Top language](https://img.shields.io/github/languages/top/aashir-athar/painter?style=for-the-badge&logo=python&logoColor=white)](https://github.com/aashir-athar/painter)
[![Workflow](https://img.shields.io/badge/GitHub_Actions-cron-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](./.github/workflows/daily-paint.yml)
[![Repo size](https://img.shields.io/github/repo-size/aashir-athar/painter?style=for-the-badge&logo=github)](https://github.com/aashir-athar/painter)
[![Stars](https://img.shields.io/github/stars/aashir-athar/painter?style=for-the-badge&logo=github&color=FFD33D)](https://github.com/aashir-athar/painter/stargazers)

<a href="#-getting-started"><strong>Get Started</strong></a> ·
<a href="#️-how-it-works"><strong>How It Works</strong></a> ·
<a href="https://github.com/aashir-athar/painter/issues"><strong>Report Bug</strong></a> ·
<a href="https://github.com/aashir-athar/painter/issues"><strong>Request Feature</strong></a>

</div>

---

**painter** is a minimal **GitHub contribution graph automation** tool. A scheduled **GitHub Actions** workflow runs a small **Python** script once per day that appends a single dated line to `heartbeat.log` and commits it to the default branch — so your contribution graph keeps reflecting that you're actively maintaining your repos. It's idempotent and configurable, making it a clean, no-nonsense daily-commit bot.

> A self-hosted "daily paint" for your GitHub contribution graph. One Python script, one cron workflow, one commit a day.

## ✨ Features

| | Feature | Description |
|---|---|---|
| 🐍 | **Single Python script** | All the logic lives in one small `daily_paint.py` file. |
| ⏰ | **Scheduled via GitHub Actions** | A cron-triggered workflow fires daily at `00:17 UTC` (off-the-hour for reliability under peak load). |
| 🔁 | **Idempotent by design** | Skips out if `heartbeat.log` already has today's entry, so manual re-runs never pile up junk commits. |
| 🚦 | **Commits only when needed** | Pushes if and only if a new commit was actually created — no empty noise. |
| 🪪 | **Counts toward your graph** | Commits are authored with your configured name/email so they register on the contribution graph. |
| ⚙️ | **Configurable** | Tune the log file path, commit-message template, and timezone label via environment variables. |

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Cron](https://img.shields.io/badge/Cron-Scheduled-4B5563?style=flat-square)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)

| Layer | Technology |
|---|---|
| Script | Python |
| Scheduler | GitHub Actions (`schedule` / cron + `workflow_dispatch`) |
| Storage | Plain-text append-only `heartbeat.log` |
| VCS | Git commit + conditional push |

## ⚙️ How It Works

The workflow (`.github/workflows/daily-paint.yml`) runs `daily_paint.py` once per day. The script:

1. Computes today's UTC date.
2. **Skips** if `heartbeat.log` already contains an entry for today (idempotent).
3. Otherwise appends one dated line and commits with a message like `chore: daily activity update - YYYY-MM-DD`.
4. The workflow then pushes **only if** a new commit exists.

## 🚀 Getting Started

### Prerequisites
- A GitHub account (a **private** repo is fine and recommended)
- Python 3 — only needed if you want to run the script locally; the workflow provides it in CI

### 1. Use this repo
Clone it, or fork/copy the core files into your own repository:

```bash
git clone https://github.com/aashir-athar/painter.git
cd painter
```

You need `daily_paint.py`, `.github/workflows/daily-paint.yml`, and `README.md`, pushed to your default branch (`master`).

### 2. Pick the email that counts toward your graph
Use either:
- any **verified** email on <https://github.com/settings/emails>, or
- your **no-reply** address from that page, e.g. `12345678+yourusername@users.noreply.github.com`.

### 3. Add repository variables
Under **Settings → Secrets and variables → Actions → Variables**:

| Variable | Value |
|---|---|
| `GIT_AUTHOR_NAME` | The name you want on the commits |
| `GIT_AUTHOR_EMAIL` | The email from step 2 |

### 4. (Private repos only) Show private contributions
Enable **Profile → Settings → Profile → Contributions & activity → Include private contributions on my profile**. Without this, the squares only appear when you're signed in as yourself.

### 5. Smoke test
Open **Actions → Daily Paint → Run workflow**. A new commit should appear, authored by the email you configured.

## 📖 Usage

Once set up, painter runs itself — no further action needed. To run the script locally for testing:

```bash
python daily_paint.py
```

### Customization

`daily_paint.py` reads three optional environment variables. Set them in the workflow's `env:` block to override the defaults:

| Variable | Default | Purpose |
|---|---|---|
| `HEARTBEAT_FILE` | `heartbeat.log` | Path of the log file. |
| `COMMIT_MESSAGE_FMT` | `chore: daily activity update - {date}` | `str.format` template (receives `{date}`). |
| `TIMEZONE_LABEL` | `UTC` | Label written into each log line. |

<details>
<summary><strong>Notes on the contribution graph</strong></summary>

- Commits only count when they are on the **default branch** and the **author email** is one GitHub recognises as yours.
- The cron fires at `00:17 UTC`. GitHub may delay scheduled workflows during peak load, so an off-the-hour minute is more reliable than `00:00`. If your contribution day is off by one in your timezone, shift the cron earlier or later.
- During long inactivity periods, GitHub may auto-disable scheduled workflows. Re-enable from the **Actions** tab.

</details>

## 🗺️ Roadmap

- [x] Idempotent daily heartbeat script
- [x] Scheduled GitHub Actions workflow
- [x] Configurable file, message, and timezone label
- [ ] Optional weekday-only / random-skip scheduling
- [ ] Add a `LICENSE` file

> 🚧 **Active development** — this is a small, focused utility. Suggestions and improvements are welcome.

## 🤝 Contributing

Contributions are welcome. For larger changes, please open an issue first to discuss what you'd like to change.

1. Fork the repo
2. Create a branch (`git checkout -b feat/thing`)
3. Commit, push, and open a Pull Request

## 📄 License

No license file has been added to this repository yet, so all rights are reserved by default. If you'd like to reuse this project, please open an issue — adding a permissive license (e.g. MIT) is on the [roadmap](#️-roadmap).

## 👤 Author

**Aashir Athar**

[![GitHub](https://img.shields.io/badge/GitHub-aashir--athar-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/aashir-athar)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-aashirathar-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/aashirathar/)
[![X](https://img.shields.io/badge/X_(Twitter)-aashirathar-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/aashirathar)

---

<div align="center">

<sub>If painter helped keep your contribution graph green, consider leaving a ⭐</sub>

<br/>

<sub><strong>Keywords:</strong> github contribution graph automation · daily commit bot · github actions cron · python automation script · keep contribution graph green · scheduled github workflow · heartbeat commit bot</sub>

</div>
