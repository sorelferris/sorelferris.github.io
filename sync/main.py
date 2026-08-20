# -*- coding: utf-8 -*-
"""Cron entry point - 每月 1 号 00:00 触发.

用法 (手动):
    python3 sync/main.py [--dry-run] [--message "custom commit msg"]

行为:
1. 拉 research/ + hermes session 5 维数据
2. 生成 4 个区块 (roadmap / reading / now / decisions)
3. 比较 hash, 没变化就跳过 commit
4. 有变化 → git add + commit + push
5. 失败 → 把错误写到 sync_state.json + 发飞书 alert (TODO)
"""
import argparse
import json
import datetime as dt
import hashlib
import subprocess
import sys
from pathlib import Path

from .config import SITE_DIR, SYNC_DIR, STATE_FILE
from . import generators


def _hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def _git(args: list[str], cwd: Path = SITE_DIR) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git"] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )


def _load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {"runs": []}


def _save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="don't commit/push")
    parser.add_argument("--message", default=None, help="git commit message")
    args = parser.parse_args()

    now = dt.datetime.now()
    print(f"[sync] start {now.isoformat()}", file=sys.stderr)

    # 1. 跑 generators
    results = generators.run_all()
    for fname, info in results.items():
        marker = "✨" if info["status"] == "updated" else "⏸️"
        print(f"  {marker} {fname:<20} {info['status']:<10} {info['bytes']:>6} bytes")

    # 2. 决定是否 commit
    updated = [f for f, info in results.items() if info["status"] == "updated"]
    if not updated:
        print("[sync] no changes → skip git", file=sys.stderr)
        return 0

    if args.dry_run:
        print(f"[sync] DRY RUN - would commit: {updated}", file=sys.stderr)
        return 0

    # 3. git add + commit + push
    msg = args.message or f"chore(sync): monthly site sync @ {now.strftime('%Y-%m-%d')}"
    add = _git(["add"] + updated + ["sync_state.json"])
    if add.returncode != 0:
        print(f"[sync] git add failed: {add.stderr}", file=sys.stderr)
        return 1

    commit = _git(["commit", "-m", msg, "-m", f"Updated: {', '.join(updated)}"])
    if commit.returncode != 0:
        print(f"[sync] git commit failed: {commit.stderr}", file=sys.stderr)
        return 1

    push = _git(["push", "origin", "main"])
    if push.returncode != 0:
        print(f"[sync] git push failed: {push.stderr}", file=sys.stderr)
        return 1

    print(f"[sync] ✅ pushed {len(updated)} files", file=sys.stderr)

    # 4. 更新 state
    state = _load_state()
    state["runs"].append({
        "ts": now.isoformat(),
        "updated": updated,
        "results": results,
    })
    state["runs"] = state["runs"][-20:]  # 保留最近 20 次
    _save_state(state)

    return 0


if __name__ == "__main__":
    sys.exit(main())
