---
title: "Home"
layout: single
classes: wide
header:
  overlay_color: "#000"
  overlay_filter: "0.5"
  overlay_image: /assets/images/header-bg.jpg
  caption: "Photo by [Sorel Ferris](https://github.com/sorelferris)"
excerpt: "Robotics × AI × VLA — building the bridge from research papers to real-world robot systems."
---

## About Me

I build **robot systems that actually work in the real world**. My current focus is
**Vision-Language-Action (VLA) models** and the infrastructure that turns research papers
into reproducible robot deployments.

**Career arc (3–5 year horizon):** Founder → **Industrial PI**. I want to lead a small team
that ships — not another paper, but a robot someone is using today. I stay technical (70%)
and grow into architecture/management (30%) deliberately.

**What I work on day-to-day:**

- 🤖 **Custom LeRobot fork** + multi-brand arm integration (Piper / AgileX / SO-101)
- 📡 **ZMQ camera streaming** (`camera-stream`) for low-latency multi-camera pipelines
- 🎮 **Isaac Teleop** workflows for VLA data collection
- 🧠 **VLA training** with FSDP2 + DTensor mixed precision (resolved an earlier
  FSDP2/DTensor interop bug)
- ⚡ **Asynchronous ZMQ inference** so the policy can outrun the control loop

I keep the engineering bar where my brain lives: if it doesn't run on a real robot in
the lab, it doesn't ship.

## 🛠️ Tech Stack

<table>
  <tr>
    <td align="center" width="100"><strong>Robotics</strong></td>
    <td>LeRobot · Isaac Sim · MuJoCo · ROS 2 · Piper SDK · AgileX PiPER · SO-100/101 · phosphobot</td>
  </tr>
  <tr>
    <td align="center"><strong>ML / DL</strong></td>
    <td>PyTorch · FSDP2 · DTensor · HuggingFace Transformers · Diffusion Policy · GRPO · DAgger</td>
  </tr>
  <tr>
    <td align="center"><strong>Infra</strong></td>
    <td>ZMQ (PUB/SUB, async) · Docker · CUDA · Linux (RT-priority) · GitHub Actions</td>
  </tr>
  <tr>
    <td align="center"><strong>Languages</strong></td>
    <td>Python · C++ · Shell · TypeScript · Markdown</td>
  </tr>
</table>

## 🚀 Featured Projects

<div class="grid--container">

<div class="grid__item">
  <a href="https://github.com/sorelferris/VLA-Handbook">
    <strong>VLA-Handbook</strong>
  </a>
  <p>A Chinese-language, practice-oriented handbook for engineers entering the
  VLA (Vision-Language-Action) field. Fills the gap between generic CV/NLP
  interview prep and the robotics-specific challenges that actually trip
  people up — embodiment gaps, sim-to-real, action tokenization.</p>
</div>

<div class="grid__item">
  <a href="https://github.com/sorelferris/lingbot-va">
    <strong>lingbot-va</strong> · <em>RSS 2026</em>
  </a>
  <p>Causal video-action world model for generalist robot control. Built on the
  hypothesis that <em>causal structure</em> in the action stream — not just
  visual fidelity — is what lets a world model transfer across embodiments.</p>
</div>

<div class="grid__item">
  <a href="https://github.com/sorelferris/Evo-RL">
    <strong>Evo-RL</strong>
  </a>
  <p>Open-source real-world offline RL on So-101 and AgileX PiPER. The hard
  part wasn't the algorithm — it was the data pipeline that lets a community
  contributor reproduce results on a $300 arm.</p>
</div>

<div class="grid__item">
  <a href="https://github.com/sorelferris/asimov-1">
    <strong>asimov-1</strong>
  </a>
  <p>v1 of an open-source humanoid robot. Hardware released under CERN-OHL-S-2.0.
  This is the kind of thing that takes 5 years and breaks every assumption you
  had about supply chains. Worth it.</p>
</div>

<div class="grid__item">
  <a href="https://github.com/sorelferris/phosphobot">
    <strong>phosphobot</strong>
  </a>
  <p>Community-driven UI middleware for controlling robots, recording datasets,
  and training action models. Compatible with SO-100 / SO-101. My contribution
  focuses on the recording → training → deployment loop.</p>
</div>

<div class="grid__item">
  <a href="https://github.com/sorelferris/zotero-arxiv-daily">
    <strong>zotero-arxiv-daily</strong>
  </a>
  <p>Daily arXiv recommendations driven by your Zotero library. Built because
  I wanted my own digest to actually reflect my reading list, not generic
  ML trends.</p>
</div>

<div class="grid__item">
  <a href="https://github.com/sorelferris/hiors">
    <strong>hiors</strong>
  </a>
  <p>Human-in-the-loop online rejection sampling for robotic manipulation.
  Cleanest MIT-licensed implementation I could find when I needed it for a
  side project; now it has a paper.</p>
</div>

<div class="grid__item">
  <a href="https://github.com/sorelferris/AmazingHand">
    <strong>AmazingHand</strong>
  </a>
  <p>Code and model for the AH! — a dexterous hand controller. Small, focused,
  and the kind of project that reminds you hardware-software co-design is
  alive and well.</p>
</div>

<div class="grid__item">
  <a href="https://github.com/sorelferris/camera-stream">
    <strong>camera-stream</strong>
  </a>
  <p>Low-latency multi-camera broadcast over ZeroMQ PUB/SUB. Designed for the
  robotics workloads where the newest frame is more valuable than retaining
  every frame — capacity-one queues, latest-frame-wins, on-demand idle.</p>
</div>

<div class="grid__item">
  <a href="https://github.com/sorelferris/lerobot">
    <strong>lerobot</strong> · <em>fork</em>
  </a>
  <p>My working fork of 🤗 LeRobot. Not a re-distribution — a place where I
  experiment with multi-brand arm integrations, custom datasets, and the
  upstream patches I keep meaning to send a PR for.</p>
</div>

</div>

## 📝 Publications

| Year | Venue | Title | Code |
|------|-------|-------|------|
| 2026 | **RSS 2026** | Causal video-action world model for generalist robot control | [lingbot-va](https://github.com/sorelferris/lingbot-va) |
| 2026 | preprint | Real-world offline RL on So-101 / PiPER | [Evo-RL](https://github.com/sorelferris/Evo-RL) |

## 🗺️ Roadmap & Notes

This site doubles as a **personal work log**. Beyond the public projects above,
I keep a working notebook of papers, claims, and unfinished threads in
[`sorelferris/research`](https://github.com/sorelferris/research). Subsections
will appear here as I crystallize them.

- **Active threads:** VLA inference latency budget · ZMQ async pipeline
  · long-horizon manipulation benchmarks · on-robot continual learning
- **Reading queue:** surfaced weekly by my [arxiv daily digest](https://github.com/sorelferris/zotero-arxiv-daily)
- **Build log:** see [research repo](https://github.com/sorelferris/research)
  `papers/`, `claims/`, `syntheses/` for the raw material

## 📫 Contact

- **GitHub:** [sorelferris](https://github.com/sorelferris)
- **Email:** open an issue on any of the repos above — fastest channel

> *This page is generated by Jekyll + Minimal Mistakes, auto-deployed by
> GitHub Pages. The content is refreshed periodically from my active research
> repository.*
