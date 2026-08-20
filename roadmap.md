---
title: "Roadmap"
layout: single
permalink: /roadmap/
author_profile: true
---

## Personal Roadmap - Quarterly View

This page tracks the **3-year Industrial PI arc** (technical depth first,
then architecture, then leadership). Updated monthly from
[`sorelferris/research/roadmap`](https://github.com/sorelferris/research/tree/main/roadmap).

*Last refreshed: 2026-08-20*


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
