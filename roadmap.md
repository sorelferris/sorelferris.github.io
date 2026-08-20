---
title: "Roadmap"
layout: single
permalink: /roadmap/
author_profile: true
---

## Personal Roadmap — Q3 2026 → Q2 2029

This page tracks the **3-year Industrial PI arc**: technical depth first,
then architecture, then leadership. Updated monthly from
[`sorelferris/research/roadmap`](https://github.com/sorelferris/research/tree/main/roadmap).

### Current quarter (Q3 2026)

| Track | Goal | Status |
|-------|------|--------|
| VLA inference latency | Push reactive-policy latency below 40ms on a single 4090 | 🟡 In progress — see `lingbot-va` & camera-stream combo |
| Multi-brand arm support | One LeRobot workflow across Piper / PiPER / SO-101 | 🟢 Done for 2/3 |
| ZMQ async inference | Decouple camera → policy → control so backpressure doesn't stall | 🟢 Prototype stable, prod-hardening next |
| Isaac Teleop integration | Standard data-collection pipeline across lab arms | 🟡 Blocked on Isaac Lab 0.12 release |

### Medium term (Q4 2026 → Q2 2027)

- **On-robot continual learning.** Today we still pre-train off-robot then
  fine-tune in lab. The next 12 months: enough on-robot experience that a
  robot gets *better at its specific job* the more it's deployed.
- **Long-horizon manipulation benchmark.** Existing benchmarks reward
  short-horizon success; the real world rewards the robot that finishes
  the multi-step task without intervention.
- **Sim-to-real at 1/1000 the cost.** Currently every real-robot hour costs
  ~$300 in supervision + wear. Target: 10x cheaper by sharing learned
  corrections across arm instances.

### Long term (2027 → 2029)

- **Industrial PI.** A small team (5–8 engineers + researchers) shipping
  robots that someone pays for because the robot does the job, not because
  it's a research demo.
- **Open-source halo.** Every shipped robot has a public research twin.
  Real-world robotics is starved of public data; my bet is the team that
  ships data wins the next decade.

### How this page is built

The source of truth is [`sorelferris/research/roadmap`](https://github.com/sorelferris/research/tree/main/roadmap).
A weekly cron pulls that directory, parses each `*.md`, and rebuilds this
page. The page itself is a Jekyll static file — no server, no JavaScript
hydration, just Markdown.
