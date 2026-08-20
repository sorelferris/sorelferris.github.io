# -*- coding: utf-8 -*-
"""4 个区块的 markdown 生成器.
每个 generator 接受 sources 数据 + 写文件到 site_dir.
"""
import datetime as dt
from pathlib import Path
from typing import Optional

from .config import SITE_DIR, NOW_WINDOW_DAYS, READING_WINDOW_DAYS, DECISIONS_WINDOW_DAYS
from . import extract, sources


def _fmt_date(d) -> str:
    if isinstance(d, str):
        return d[:10]
    if isinstance(d, dt.datetime):
        return d.date().isoformat()
    return "?"


def _titlecase(s: str) -> str:
    if not s:
        return ""
    return s[0].upper() + s[1:]


# ---------- /roadmap/ ----------
def generate_roadmap(roadmap_items: list[dict]) -> str:
    """读取 research/roadmap/*.md 内容, 拼成 Jekyll 页面.
    若 research/roadmap/ 空, 用静态 fallback (来自 index.md 的 roadmap 部分).
    """
    today = dt.date.today().isoformat()

    # 静态骨架
    head = """---
title: "Roadmap"
layout: single
permalink: /roadmap/
author_profile: true
---

## Personal Roadmap - Quarterly View

This page tracks the **3-year Industrial PI arc** (technical depth first,
then architecture, then leadership). Updated monthly from
[`sorelferris/research/roadmap`](https://github.com/sorelferris/research/tree/main/roadmap).

*Last refreshed: {today}*

""".format(today=today)

    if not roadmap_items:
        body = """
> 📭 `research/roadmap/` is currently empty - drop your quarterly `.md` files there
> and they'll show up here on the next sync.

### Static overview (preserved from initial site)

**Q3 2026 - Current quarter**

| Track | Goal | Status |
|-------|------|--------|
| VLA inference latency | Push reactive-policy latency below 40ms on a single 4090 | 🟡 In progress |
| Multi-brand arm support | One LeRobot workflow across Piper / PiPER / SO-101 | 🟢 2/3 done |
| ZMQ async inference | Decouple camera → policy → control so backpressure doesn't stall | 🟢 Prototype stable |
| Isaac Teleop integration | Standard data-collection pipeline across lab arms | 🟡 Blocked on Isaac Lab 0.12 |

**Medium term (Q4 2026 → Q2 2027)**

- On-robot continual learning
- Long-horizon manipulation benchmark
- Sim-to-real at 1/1000 the cost

**Long term (2027 → 2029)**

- Industrial PI - small team shipping robots that someone pays for
- Open-source halo - every shipped robot has a public research twin
"""
        return head + body

    # 动态从 research/roadmap/*.md 拉
    body = "## Quarterly Notes (auto-generated from `research/roadmap/`)\n\n"
    for item in sorted(roadmap_items, key=lambda x: x["name"]):
        body += f"### {item['name'].replace('.md', '').replace('_', ' ').title()}\n\n"
        # 提 front-matter 之后的内容 (去掉 --- 包裹的 yaml)
        content = item["content"]
        # 简单剥离 frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[2].strip()
        # 截断太长
        if len(content) > 4000:
            content = content[:4000] + "\n\n*[truncated; see source file]*"
        body += content + "\n\n---\n\n"

    body += """
### How this page is built

Source of truth: [`sorelferris/research/roadmap`](https://github.com/sorelferris/research/tree/main/roadmap).
Monthly cron (1st of month, 00:00 Asia/Shanghai) pulls that directory and
regenerates this page. To update: drop a `.md` file in `research/roadmap/`
and push to main.
"""
    return head + body


# ---------- /reading/ ----------
def generate_reading(papers: list[dict], skim_items: list[dict]) -> str:
    today = dt.date.today().isoformat()
    head = """---
title: "Reading Queue"
layout: single
permalink: /reading/
author_profile: true
---

## Reading Queue & Paper Notes

The running log of papers I'm reading, ranked by depth of engagement.
Source: [`sorelferris/research/papers`](https://github.com/sorelferris/research/tree/main/papers)
+ daily digest from [`zotero-arxiv-daily`](https://github.com/sorelferris/zotero-arxiv-daily).

*Last refreshed: {today}*

""".format(today=today)

    if not papers and not skim_items:
        body = """
> 📭 No paper notes found in `research/papers/`. Create a subdirectory per
> paper (e.g. `papers/<arxiv-id>-<slug>/`) with a `README.md` to track reading.

### This week's arXiv digest

See [zotero-arxiv-daily](https://github.com/sorelferris/zotero-arxiv-daily)
for the daily recommendations filtered by your Zotero library.
"""
        return head + body

    body = "## Deep-read ({n} papers)\n\n".format(n=len(papers))
    for p in papers:
        body += f"### [{p['name']}](https://github.com/sorelferris/research/tree/main/papers/{p['name']})\n\n"
        body += f"- Path: `papers/{p['name']}/`\n"
        if p.get("first_note"):
            body += f"- First note: `{p['first_note']}`\n"
        if p.get("has_readme"):
            body += f"- Has README: ✅\n"
        body += "\n"

    body += "\n## Skimmed\n\n"
    if skim_items:
        body += "These surfaced from recent daily arXiv digests (auto-curated).\n\n"
        for s in skim_items[:10]:
            body += f"- {s}\n"
    else:
        body += "_No recent skims this period._\n"

    body += """
\n### Why this is public

1. **Forcing function.** Writing a TLDR in public is the cheapest way to find
   out whether I actually understood the paper.
2. **Signal for collaborators.** If you find a paper interesting, you can
   tell - and that loop is what my best collaborations have come from.
3. **Lies-to-children disclaimer.** Skim-grade takes are often wrong.

### Maintenance

Monthly cron (1st of month, 00:00) regenerates this page from
[`research/papers/`](https://github.com/sorelferris/research/tree/main/papers).
"""
    return head + body


# ---------- /now/ ----------
def generate_now(extract_data: dict) -> str:
    today = dt.date.today().isoformat()
    head = """---
title: "Now"
layout: single
permalink: /now/
author_profile: true
---

## What I'm Focused On Right Now

*Auto-generated monthly from your recent conversation sessions.
Last refreshed: {today}*

> 💡 This page is **not** aspirations - it's operational. Long-horizon ideas
> live on the [Roadmap](/roadmap/) page. Inspired by
> [Derek Sivers' /now page](https://nownownow.com/about).

""".format(today=today)

    sessions_used = extract_data.get("sessions_used", 0)
    body = f"_Scanned {sessions_used} recent user sessions._\n\n"

    # 5 个维度
    sections = [
        ("shipped", "🟢 Shipped / Completed", "What got done in this period."),
        ("in_flight", "🟡 In flight / Investigating", "Active threads that aren't done yet."),
        ("blocked", "🔴 Blocked / Waiting on", "Things that need input from you or others."),
        ("decision", "💡 Decisions made", "Choices that were explicit, with context."),
        ("bookmark", "📚 New bookmarks / Reading", "Things added to your watch list."),
    ]

    for cat, title, blurb in sections:
        items = extract_data.get(cat, [])
        body += f"## {title}\n\n_{blurb}_\n\n"
        if not items:
            body += "_Nothing recorded this period._\n\n"
            continue
        body += "| Date | From session | Snippet |\n"
        body += "|------|-------------|---------|\n"
        for it in items[:10]:
            date = _fmt_date(it.get("started_at", ""))
            title_short = (it.get("title") or "(no title)")[:40]
            text_short = it["text"][:100].replace("|", "\\|").replace("\n", " ")
            body += f"| {date} | {title_short} | {text_short} |\n"
        body += "\n"

    body += """
### What's *not* on this page

- Aspirations - see [/roadmap/](/roadmap/)
- Long-horizon ideas - see [/roadmap/](/roadmap/)
- Already-decided-and-executed items - see commits + closed PRs on GitHub

### Methodology

The pattern matchers are intentionally conservative - false negatives
(missed) are preferred over false positives (false claims of "completed").
If you find something missing, edit the source markdown directly; the next
monthly sync will pick it up.
"""
    return head + body


# ---------- /decisions/ ----------
def generate_decisions(extract_data: dict) -> str:
    today = dt.date.today().isoformat()
    head = """---
title: "Decisions"
layout: single
permalink: /decisions/
author_profile: true
---

## Decision Log

A running record of explicit decisions made during our conversations.
The goal is **durable memory**: 3 months from now, when you've forgotten why
you chose X over Y, this page answers it.

*Auto-generated monthly. Last refreshed: {today}*

""".format(today=today)

    decisions = extract_data.get("decision", [])
    body = f"_{len(decisions)} explicit decisions recorded in the current window._\n\n"

    if not decisions:
        body += """
> 📭 No explicit decisions recorded in this period.

If you want a decision to show up here, phrase it as "我决定 X" / "decided X"
/ "going with X" - the pattern matcher is conservative on purpose.
"""
        return head + body

    # 按 session 分组, 同一 session 的决定聚在一起
    by_session = {}
    for d in decisions:
        sid = d.get("session_id", "?")
        by_session.setdefault(sid, {"title": d.get("title", ""), "items": [], "started_at": d.get("started_at")})
        by_session[sid]["items"].append(d["text"])

    body += "## Recent decisions\n\n"
    for sid, info in sorted(by_session.items(), key=lambda kv: kv[1]["started_at"] or dt.datetime.min, reverse=True):
        date = _fmt_date(info["started_at"])
        title = info["title"] or "(no title)"
        body += f"### {date} - [{title}](https://github.com/sorelferris/research)\n\n"
        for txt in info["items"]:
            body += f"- {txt[:200]}\n"
        body += "\n"

    body += """
\n### How decisions get here

Pattern matchers scan assistant turns for explicit decision language:
"我决定 X" / "decided X" / "going with X" / "选择 X". Conservative on
purpose: false negatives (missed decisions) are preferred over false
positives (false claims of "decided").

If a decision is missing, you can either:
1. Edit this page directly (it'll be re-checked next sync)
2. Make the language more explicit in your next session
"""
    return head + body


# ---------- Driver ----------
def run_all(extract_data: Optional[dict] = None) -> dict:
    """主入口: 生成 4 个区块 + 返回写入路径 + 字节数."""
    if extract_data is None:
        now = dt.datetime.now()
        extract_data = extract.extract_all(now - dt.timedelta(days=max(READING_WINDOW_DAYS, DECISIONS_WINDOW_DAYS)))

    # 拉 research 数据
    papers = sources.list_research_papers()
    roadmap = sources.list_research_roadmap()

    pages = {
        "roadmap.md": generate_roadmap(roadmap),
        "reading.md": generate_reading(papers, []),
        "now.md": generate_now(extract_data),
        "decisions.md": generate_decisions(extract_data),
    }

    out = {}
    for filename, content in pages.items():
        path = SITE_DIR / filename
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        if old.strip() == content.strip():
            out[filename] = {"path": str(path), "status": "unchanged", "bytes": len(content)}
            continue
        path.write_text(content, encoding="utf-8")
        out[filename] = {"path": str(path), "status": "updated", "bytes": len(content)}

    return out


if __name__ == "__main__":
    import json
    result = run_all()
    print(json.dumps(result, indent=2))
