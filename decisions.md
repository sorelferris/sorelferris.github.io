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

### 2026-08-20 - [优化每日 arXiv 飞书定时推送](https://github.com/sorelferris/research)

- 关于优化 Daily arXiv 定时推送(加"代码开源/模型权重开源"标注),我有方案 — 但有几个决策需要你拍板,因为会影响 cron prompt 写法、卡片版式、归档 markdown 模板:
- hermes/skills/lark/lark-cron-scheduled-cards/references/prompt-template-arxiv-digest
- com/
- **标注图标**:`💻 Code` `🤗 Weights` (两个状态各一:`✅ 有 / ❌ 无 / ❓ 未明`)
- **写入归档**:当日 callout 旁边加一行 `**代码/权重**:` + 每篇 `- [1]
- com/xxx | 🤗✅ hf
- co/yyy`
- patch canonical prompt-template-arxiv-digest
- 把这次改动同步进 cron job `05a56bb7dcbf` 的 prompt 字段
- 在 himalaya skill 下补一份新 baseline reference (今天 8/20 之后下次跑的记录会写在这里,含 pitfall #55/56)
- - Code 命中: **0/10** ❌
- co/docs/hub/spaces` — arxiv 站点"如何上传模型"文档,不是论文自己的权重) ❌
- x 重设计后,abs 页底部**不再有** `<a name="Code">` 这种老锚点 (老 regex 全部失效)
- abs 页**完全没有**论文自己的 GitHub 链接 — 只有侧栏的 CatalyzeX 代码搜索 + HuggingFace 模型搜索通用锚点
- 除非作者在 abstract 文本里主动写 "Code: https://github



### How decisions get here

Pattern matchers scan assistant turns for explicit decision language:
"我决定 X" / "decided X" / "going with X" / "选择 X". Conservative on
purpose: false negatives (missed decisions) are preferred over false
positives (false claims of "decided").

If a decision is missing, you can either:
1. Edit this page directly (it'll be re-checked next sync)
2. Make the language more explicit in your next session
