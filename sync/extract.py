# -*- coding: utf-8 -*-
"""从 session messages 中提取 5 类信息:
- 🟢 完成什么 (shipped)
- 🟡 卡在什么 (in-flight)
- 🔴 阻塞 / 风险
- 💡 关键决策
- 📚 新收藏 / 调研
"""
import re
import datetime as dt
from typing import Iterator

# Pattern design - 双向匹配 user 提问 (用户表达意图) + assistant 复述
# 优先级: assistant 消息中"我决定/我做了/我设置" = decision shipped
#          user 消息中"我想要 / 帮我 X / 怎么 Y" = in-flight
PATTERNS = {
    "shipped": [
        # Chinese - 完成/已经/已 push
        r"\b(?:已完成|已 push|已提交|已发送|完成(?:了)?|刚刚完成)\b",
        r"\b(?:已上线|已 merge|已部署|已创建|已修复|已更新)\b",
        r"\b(?:改动|修改|patch|fix)(?:了|完成|好了)\b",
        # English
        r"\b(?:shipped|deployed|merged|pushed|submitted|fixed|implemented)\b",
        # 我做了
        r"\b我(?:做了|完成了|设置了|建了|创建了|提交了)\b",
    ],
    "in_flight": [
        # Chinese - 正在/调研/卡
        r"\b(?:正在|还在|仍然|调研|实验|测试|调试|排错|追踪)\b",
        r"\b(?:待办|TODO|待完成|未完成)\b",
        r"\b(?:纠结|没想清楚|不确定|不知道该不该)\b",
        # English
        r"\b(?:investigating|debugging|exploring|still working on|WIP|TBD)\b",
        # 卡点
        r"(?:卡在|卡住了|遇到|碰到)(?:.{0,20})(?:问题|坑|错误|错误码)",
    ],
    "blocked": [
        # Chinese - 等/需要/依赖
        r"\b(?:等(?:待|你|对方)|需要你|等你回复|取决于)\b",
        r"\b(?:阻塞|拦着|卡住)\b",
        r"\b(?:等你拍板|等你决策|等你决定)\b",
        # English
        r"\b(?:blocked|waiting on|need (?:you|user|input))\b",
    ],
    "decision": [
        # Chinese - 决定/选择
        r"\b(?:我决定|我选了|我选择|决定用|决定不|选定)\b",
        r"\b(?:方案 A|B|C):?(?:.{0,40})\b",
        r"\b(?:最终用|最终选择|改用|换成|切换到)\b",
        # English
        r"\b(?:decided|chose|going with|will use|switched to)\b",
        # 选择题
        r"\b选(?:择)?[1-4]\b",
        r"\bdecision:",
    ],
    "bookmark": [
        # Chinese - 收藏/感兴趣/想看
        r"\b(?:收藏|加入收藏|加入书签|加个书签|想看|想读)\b",
        r"\b(?:已收藏|已在收藏)\b",
        r"\b(?:调研|研读)(?:这篇|这个|这个 repo|这论文)\b",
        # English
        r"\b(?:bookmarked|added to collection|want to read)\b",
    ],
}


def classify_sentences(messages: Iterator[dict]) -> dict:
    """对每条 message 做 sentence-level 模式匹配.
    Returns: {category: [sentence, sentence, ...]}
    """
    out = {k: [] for k in PATTERNS}
    for msg in messages:
        content = msg["content"]
        # 分句 (按 . 或 .)
        sentences = re.split(r"[..!?\n]+", content)
        for sent in sentences:
            sent = sent.strip()
            if len(sent) < 4 or len(sent) > 300:
                continue  # 跳过太短/太长
            for cat, patterns in PATTERNS.items():
                for pat in patterns:
                    if re.search(pat, sent, re.IGNORECASE):
                        out[cat].append({
                            "text": sent,
                            "session_id": msg.get("session_id"),
                            "title": msg.get("title"),
                            "started_at": msg.get("started_at"),
                            "role": msg.get("role"),
                        })
                        break  # 每句话只归一类
    return out


def dedupe_by_text(items: list[dict], max_keep: int = 20) -> list[dict]:
    """按 text 去重 + 按 session_id 保持时序."""
    seen = set()
    out = []
    for it in items:
        key = it["text"][:80]  # 取前 80 字符作 key
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
        if len(out) >= max_keep:
            break
    return out


def extract_all(since: dt.datetime) -> dict:
    """顶层: 聚合过去 N 天的 5 类信息.
    Returns: {category: [items], 'sessions_used': int, 'since': iso, 'until': iso}
    """
    from .state import session_messages_iter
    msgs = session_messages_iter(since)
    classified = classify_sentences(msgs)
    sessions_used = len({m.get("session_id") for cat in classified.values() for m in cat})

    out = {}
    for cat, items in classified.items():
        out[cat] = dedupe_by_text(items, max_keep=15)
    out["sessions_used"] = sessions_used
    out["since"] = since.isoformat()
    out["until"] = dt.datetime.now().isoformat()
    return out


if __name__ == "__main__":
    import datetime as dt
    week_ago = dt.datetime.now() - dt.timedelta(days=7)
    result = extract_all(week_ago)
    print(f"Sessions scanned: {result['sessions_used']}")
    print(f"Window: {result['since'][:10]} → {result['until'][:10]}")
    print()
    for cat in ("shipped", "in_flight", "blocked", "decision", "bookmark"):
        items = result[cat]
        print(f"--- {cat} ({len(items)}) ---")
        for it in items[:5]:
            d = it.get("started_at") or ""
            print(f"  [{d[:10]}] {it['text'][:90]}")
        print()
