# -*- coding: utf-8 -*-
"""Hermes session DB 读取 + 对话总结辅助."""
import sqlite3, json
import datetime as dt
from pathlib import Path
from typing import Iterator

from .config import HERMES_STATE_DB, USER_SESSION_SOURCES


def _conn():
    if not HERMES_STATE_DB.exists():
        raise FileNotFoundError(f"Hermes state DB not found: {HERMES_STATE_DB}")
    return sqlite3.connect(str(HERMES_STATE_DB))


def recent_user_sessions(since: dt.datetime, limit: int = 50) -> list[dict]:
    """列出指定时间之后, 用户驱动的 sessions (source in USER_SESSION_SOURCES).
    Returns list of dicts with keys: id, source, started_at, ended_at,
    message_count, tool_call_count, title.
    """
    since_ts = since.timestamp()
    sql = """
        SELECT id, source, started_at, ended_at, message_count,
               tool_call_count, title
        FROM sessions
        WHERE started_at >= ?
          AND source IN ({})
        ORDER BY started_at DESC
        LIMIT ?
    """.format(",".join("?" * len(USER_SESSION_SOURCES)))
    with _conn() as db:
        cur = db.execute(sql, [since_ts, *USER_SESSION_SOURCES, limit])
        out = []
        for row in cur.fetchall():
            sid, src, started, ended, msg_cnt, tool_cnt, title = row
            out.append({
                "id": sid,
                "source": src,
                "started_at": dt.datetime.fromtimestamp(started) if started else None,
                "ended_at": dt.datetime.fromtimestamp(ended) if ended else None,
                "message_count": msg_cnt or 0,
                "tool_call_count": tool_cnt or 0,
                "title": title or "",
            })
        return out


def session_user_messages(session_id: str) -> list[dict]:
    """提取某 session 里 role='user' 的消息内容 (用于决策/总结扫描)."""
    sql = """
        SELECT id, content, created_at
        FROM messages
        WHERE session_id = ? AND role = 'user' AND content IS NOT NULL
        ORDER BY id ASC
    """
    with _conn() as db:
        cur = db.execute(sql, [session_id])
        out = []
        for row in cur.fetchall():
            mid, content, created_at = row
            out.append({
                "id": mid,
                "content": content,
                "created_at": created_at,
            })
        return out


def session_assistant_messages(session_id: str) -> list[dict]:
    sql = """
        SELECT id, content, created_at
        FROM messages
        WHERE session_id = ? AND role = 'assistant' AND content IS NOT NULL
        ORDER BY id ASC
    """
    with _conn() as db:
        cur = db.execute(sql, [session_id])
        return [{"id": r[0], "content": r[1], "created_at": r[2]} for r in cur.fetchall()]


def session_messages_iter(since: dt.datetime, source_filter=None) -> Iterator[dict]:
    """生成器: 迭代最近 user sessions 里的所有 user/assistant 文本.
    用于聚合关键词扫描 (决策/卡点/完成 等).
    Yields dict: {session_id, source, title, started_at, role, content}.
    """
    sessions = recent_user_sessions(since, limit=200)
    with _conn() as db:
        for s in sessions:
            if source_filter and s["source"] not in source_filter:
                continue
            sid = s["id"]
            sql = """
                SELECT role, content FROM messages
                WHERE session_id = ? AND role IN ('user','assistant')
                  AND content IS NOT NULL AND length(content) > 5
                ORDER BY id ASC
            """
            cur = db.execute(sql, [sid])
            for role, content in cur.fetchall():
                yield {
                    "session_id": sid,
                    "source": s["source"],
                    "title": s["title"],
                    "started_at": s["started_at"],
                    "role": role,
                    "content": content,
                }


if __name__ == "__main__":
    # Sanity check
    week_ago = dt.datetime.now() - dt.timedelta(days=7)
    sessions = recent_user_sessions(week_ago)
    print(f"Recent user sessions (7d): {len(sessions)}")
    for s in sessions[:3]:
        print(f"  {s['started_at']} {s['source']:<10} msgs={s['message_count']:>3}  {s['title'][:60]}")
