# sync/ — Monthly auto-sync pipeline

## What it does

Pulls from 3 sources, generates 4 site pages, commits + pushes to GitHub.

**Sources:**
1. `sorelferris/research` GitHub repo (papers/ + roadmap/)
2. `~/.hermes/state.db` SQLite (recent user sessions)

**Pages generated:**
| file | data source | time window |
|------|------------|-------------|
| `roadmap.md` | research/roadmap/*.md | latest |
| `reading.md` | research/papers/*/ | latest |
| `now.md` | user sessions | last 7 days |
| `decisions.md` | user sessions | last 90 days |

## Trigger

Monthly cron — 1st of month, 00:00 Asia/Shanghai.

## Manual run

```bash
cd ~/workspace/sorelferris.github.io
python3 -m sync.main                # run + commit + push
python3 -m sync.main --dry-run       # preview only
```

## State

`sync_state.json` keeps last 20 runs (timestamps + updated files + status).

## Extending

To add a 5th data source:

1. Add fetcher in `sources.py` (return list/dict of records)
2. Add 5-dim classifier in `extract.py` if extracting from sessions
3. Add generator function in `generators.py` (return markdown string)
4. Wire into `run_all()` and add to `pages` dict

## Limitations (2026-08-20)

- Pattern matchers for session extraction are conservative (false-neg biased)
- Only English + Chinese; no other languages
- Decision matcher looks for assistant turns only (user phrasings get missed)
- arXiv digest cross-link with `zotero-arxiv-daily` is hand-rolled; could
  automate but not yet (waiting on user feedback)
