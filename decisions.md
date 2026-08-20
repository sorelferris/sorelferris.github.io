---
title: "Decisions"
layout: single
permalink: /decisions/
author_profile: true
---

## Decision Log

A running record of explicit decisions made during our conversations.
The goal is **durable memory**: 3 months from now, when you've forgotten why
you chose X over Y, this page answers it.

*Auto-generated monthly. Last refreshed: 2026-08-20*

_15 explicit decisions recorded in the current window._

## Recent decisions

### 2026-08-18 - [用户画像建立](https://github.com/sorelferris/research)

- **我的决定（按你授权）**：

### 2026-08-14 - [分散顺延飞书积压任务](https://github.com/sorelferris/research)

- 我倾向 **方案 A**(AI 自动读每日工作 → 总结成 emoji 列表写入),**但写到文档后立即发飞书卡片给你看**,不满意可以让我重写/手工改。

### 2026-08-05 - [飞书任务制定与论文研读](https://github.com/sorelferris/research)

- - 选 1:先做方法论综述(#1)
- - 选 2:直接跳到 MVP(#3)
- - 选 3:先调研再选
- - 选 4:先和我对话把 4 个关键问题聊清楚
- 你选了"选 1:先做方法论综述"。我直接出了一稿,放在飞书文档里回链到任务评论,然后给你卡片式摘要。

### 2026-06-11 - [归档文档标签与摘要修复](https://github.com/sorelferris/research)

- **方案 A**：把"中文摘要"放到 `<li>` 内部（用 `<br/>` 分隔）
- **方案 B**：把 `<ul>` 拆开成多个 `<p>` 块（每篇一篇用单独段落 + 列表项）
- 方案 A 最简单：
- 现在试试用 `<br/>` 在 `<li>` 内部分隔。同时为防万一（lark 服务端可能对 `<br/>` 在 li 内部也挑剔），我同时准备个**方案 C**：每篇论文用一个**独立 `<p>` 块**包标题+摘要（不用 `<ul>`）。让我用方案 A 试一下，先看 lark 接受不接受：
- **方案 A 完美**：

### 2026-06-10 - [Cronjob集成飞书文档](https://github.com/sorelferris/research)

- 💡 默认推荐 A。回复 A / B / C / D 选一个,或贴文档 URL(方案 D)。"]
- ✅ 任务复盘 cron job 优化完成 · 方案 A 已落地

### 2026-06-08 - [飞书任务默认负责人设置](https://github.com/sorelferris/research)

- 如果要"看起来立即"——**方案 B（PLD 残差 + 蒸馏）** 是最成熟的工程化路径；或 **方案 C（adapter）** 速度快但管理复杂



### How decisions get here

Pattern matchers scan assistant turns for explicit decision language:
"我决定 X" / "decided X" / "going with X" / "选择 X". Conservative on
purpose: false negatives (missed decisions) are preferred over false
positives (false claims of "decided").

If a decision is missing, you can either:
1. Edit this page directly (it'll be re-checked next sync)
2. Make the language more explicit in your next session
