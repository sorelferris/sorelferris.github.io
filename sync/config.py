# -*- coding: utf-8 -*-
"""Sync config - 修改这里即可调整 4 个区块的生成行为.
集中放一处,避免各 generator 重复硬编码 token / repo / 路径.
"""
import os
from pathlib import Path

# GitHub
GH_TOKEN = os.environ.get("GH_TOKEN") or open(Path.home() / ".git-credentials").read().split(":")[1].split("@")[0]
GH_USER = "sorelferris"
RESEARCH_REPO = f"{GH_USER}/research"
SITE_REPO = f"{GH_USER}/sorelferris.github.io"

# Local paths
SITE_DIR = Path.home() / "workspace" / "sorelferris.github.io"
RESEARCH_LOCAL = Path.home() / "workspace" / "research"  # optional local clone
SYNC_DIR = SITE_DIR / "sync"
STATE_FILE = SYNC_DIR / "sync_state.json"  # 上次 sync 时间戳 + 内容哈希

# Time windows (days)
NOW_WINDOW_DAYS = 7
READING_WINDOW_DAYS = 30
DECISIONS_WINDOW_DAYS = 90

# SQLite (Hermes session DB)
HERMES_STATE_DB = Path.home() / ".hermes" / "state.db"

# Skip cron sessions, only summarise user-driven sessions (feishu / CLI)
USER_SESSION_SOURCES = ("feishu", "cli", "terminal", "manual")
