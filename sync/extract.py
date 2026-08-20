# -*- coding: utf-8 -*-
"""Extract 5 categories from session messages: shipped / in_flight / blocked / decision / bookmark.

Design v2 (2026-08-20 regex tune):
- Stop-word filter: skip meta-discussion of the categories themselves (e.g. "5-dim
  classification" or table rows that list category names).
- Markdown skip: header lines (`## ...`) and table rows (`| ... |`) are noise, not actions.
- Anchored verbs: `已 X` / `I shipped` need a subject + action past tense. Avoid matching
  when keyword appears in a quoted list of patterns or as a parenthetical example.
- Decision: `方案 A` requires literal `A/B/C/D` (single letter), not Chinese 案 char.
"""
import re
import datetime as dt
from typing import Iterator

# --- Layer A: Stop-word patterns (sentence-level filters) ---
# Catch meta-discussion of the categories themselves, false-positive analysis,
# and Design-doc-style category enumerations.
STOP_WORDS = re.compile(
    r"(?:"
    r"5[\-\s]?dim|5\s*维|5\s*个\s*维度"  # category meta-discussion
    r"|分类\s*regex|regex\s*调(?:|更准|优|更精)"
    r"|(?:本对话|本 session|本次|这个对话)\s*(?:任务|记录|摘要)"  # meta about THIS conversation
    r"|消除.{0,30}(?:噪声|误报|false positive)"  # meta-false-positive analysis
    r"|(?:5|categories)\s*:\s*shipped"
    r"|shipped\s*/\s*in_flight\s*/\s*blocked"  # literal category list
    r"|shipped\s*标志"  # "shipped 标志" = "the shipped marker" (meta)
    r"|(?:把|将).{0,15}(?:当|作为|误判为)\s*shipped"  # discussion of mis-classification
    r"|(?:误报|噪声).{0,20}(?:shipped|blocked|decision|in_flight)"  # noise analysis
    r"|(?:describes?|mentions?)\s+(?:shipped|blocked|decision|in_flight|bookmark)"  # English meta
    r")",
    re.IGNORECASE,
)

# --- Layer B: Markdown structural skip (whole sentence) ---
RE_HEADER = re.compile(r"^\s*#+\s")  # # ## ### at start
RE_TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")  # | cell | cell |
RE_LIST_BULLET = re.compile(r"^\s*[-\*]\s+")  # list bullet (could be legit but usually noise)
RE_CODE_FENCE = re.compile(r"^\s*```")

# --- Layer C: Pattern groups (anchored, with context) ---
# All patterns designed to anchor on verb/action, not on bare category name.
PATTERNS = {
    "shipped": [
        # Chinese past-tense + completed action - look for 时态锚 (已 / 了 / 完成 / 推送)
        r"\b(?:我|已经|刚|刚[刚才]|这次)\s*(?:已完成|完成(?:了)?|刚完成|刚 push|刚推|刚跑完|刚 sync|已经 sync)\b",
        r"\b(?:已 push|已提交|已发送|已上线|已 merge|已部署|已创建|已修复|已更新|已写入|已沉淀)\b",
        r"\b(?:已固化|已 patch|已 dry[\-\s]?run|已 dry.{0,3}run)\b",
        r"\b(?:改动|修改|patch|fix|deploy|merge|ship|commit)(?:了|完成|好了|过了)\b",
        r"\b(?:cron\s+(?:已|创建)|job\s+(?:已|创建))\b",
        # English past-tense
        r"\b(?:just (?:shipped|deployed|merged|pushed|submitted|fixed|implemented|synced))\b",
        r"\b(?:shipped|deployed|merged|pushed|submitted|fixed|implemented)[\s,]+",
        r"\b(?:cron\s+job\s+created|cron\s+(?:已|创建))\b",
    ],
    "in_flight": [
        # Chinese - 正在做 / 还在做 / 调研中
        r"\b(?:正在|还在|仍然)\s*(?:调试|排查|跑|调|写|试|测|调研|研究|看|读|部署|设计|实现|测试|训练)\b",
        r"\b(?:调研中|实验中|测试中|调试中|排错中|推进中|打磨中)\b",
        r"\b(?:待完成|未完成|待定|TBD|WIP|TODO)\b",
        r"\b(?:下次|稍后|回头|明天|以后)\s*(?:再|接着|继续|来)\b",
        r"\b(?:纠结|没想清楚|不确定|不知道该不该|有点卡)\b",
        # 卡在 X 上
        r"(?:卡在|卡住了|遇到|碰到|陷在)\s*.{0,20}(?:问题|坑|错误|错误码|循环)",
        # English
        r"\b(?:investigating|debugging|exploring|working on|still TBD|in progress)\b",
        # 待 X (avoid 已 X)
        r"\b待\s*(?:修|补|加|做|写|调|跑|测|验证|verify)\b",
    ],
    "blocked": [
        # Chinese - 等某人 / 等某事
        r"\b等(?:待|你|你拍板|你决策|你决定|你回复|用户|用户回|用户选)\b",
        r"\b(?:需要你|取决于|靠你)\s*.{0,15}\b",
        r"\b(?:等你拍板|等你决策|等你决定|等你回|等你选|等用户)\b",
        r"\b(?:阻塞|拦着|卡住)(?:了|住)?\b",
        # English
        r"\b(?:blocked|waiting on|need (?:you|user|input|decision))\b",
        r"\b(?:blocked by|取决于)\b",
    ],
    "decision": [
        # Chinese - 决定/选定 (with 我 or 已)
        r"\b(?:我决定|我(?:的)?决定|我选了|我选择|我选定|我(?:的)?选择|我(?:的)?选定|决定用|决定改用|决定走)\b",
        r"\b(?:已决定|已选定|已选)\b",
        # 改用/换成 需要主体是"方案/方法/工具/方案/策略/路径", 避免 "用 ASCII 替代" 误中
        r"\b(?:改用|换成|切换到|改走|走)\s*(?:方案|方法|工具|策略|路径|路线|版本|方案)\s*[A-Z0-9一-鿿]",
        r"\b(?:最终用|最终选择)\s*(?:方案|方法|工具|策略|路径|版本|V[0-9]+)\b",
        # 方案选择: 必须 方案 A/B/C/D (单字符)
        r"\b方案\s+[ABCD]\b",
        r"\b选(?:择)?\s*[1-4]\b",
        r"\b(?:倾向|主推|走)\s*(?:方案\s+)?[ABCD]\b",
        r"\b方案\s+(?:已定|定了|选定|定了)\b",
        # English
        r"\b(?:I (?:decided|chose|will use|will go with|going with))\b",
        r"\b(?:decided to|chose to|switched to)\b",
        r"\b(?:final decision|final choice|final call)\b",
        r"\bdecision\s*:\s*",
    ],
    "bookmark": [
        # Chinese - 收藏/想看
        r"\b(?:加入收藏|加入书签|加个书签|已收藏|已在收藏|加入收藏)\b",
        r"\b(?:想看|想读|想研究|想深读)\b",
        r"\b(?:调研|研读)(?:这篇|这个|这论文|这个 repo|这文章)\b",
        # English
        r"\b(?:bookmarked|added to (?:collection|reading list)|want to read|want to deep[- ]?read)\b",
        r"\b(?:deep[- ]?read\s+paper|deep[- ]?dive\s+into)\b",
    ],
}


def _is_noise_sentence(sent: str) -> bool:
    """Layer A/B/C sentence-level filters. Returns True if should skip."""
    s = sent.strip()
    if not s:
        return True
    # Length filter
    if len(s) < 6 or len(s) > 280:
        return True
    # Markdown structural
    if RE_HEADER.match(s):
        return True
    if RE_TABLE_ROW.match(s):
        return True
    if RE_CODE_FENCE.match(s):
        return True
    # Meta discussion of categories themselves
    if STOP_WORDS.search(s):
        return True
    # Pure header / separator
    if re.match(r"^\s*[=\-_]{3,}\s*$", s):
        return True
    return False


def classify_sentences(messages: Iterator[dict]) -> dict:
    """Sentence-level pattern matching with noise filters."""
    out = {k: [] for k in PATTERNS}
    for msg in messages:
        content = msg["content"]
        # Split on punctuation + newlines
        sentences = re.split(r"[.!?\n;]+", content)
        for sent in sentences:
            sent = sent.strip()
            if _is_noise_sentence(sent):
                continue
            # Strip leading list bullet for matching (but keep for display)
            sent_clean = re.sub(r"^\s*[-\*]\s+", "", sent)
            sent_clean = sent_clean.strip()
            if len(sent_clean) < 4:
                continue
            # First match wins - each sentence gets only one category
            for cat, patterns in PATTERNS.items():
                for pat in patterns:
                    if re.search(pat, sent_clean, re.IGNORECASE):
                        out[cat].append({
                            "text": sent,  # keep original with bullet for display
                            "session_id": msg.get("session_id"),
                            "title": msg.get("title"),
                            "started_at": msg.get("started_at"),
                            "role": msg.get("role"),
                        })
                        break  # one category per sentence
                else:
                    continue
                break  # break outer after first category
    return out


def dedupe_by_text(items: list[dict], max_keep: int = 20) -> list[dict]:
    """Dedupe by text prefix (first 80 chars), keep order, cap at max_keep."""
    seen = set()
    out = []
    for it in items:
        key = (it["text"][:80], it.get("session_id"))
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
        if len(out) >= max_keep:
            break
    return out


def extract_all(since: dt.datetime) -> dict:
    """Aggregate 5 categories from sessions since `since`. Returns dict with category lists + metadata."""
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
    week_ago = dt.datetime.now() - dt.timedelta(days=7)
    result = extract_all(week_ago)
    print("Sessions scanned:", result["sessions_used"])
    print("Window:", str(result["since"])[:10], "->", str(result["until"])[:10])
    print()
    for cat in ("shipped", "in_flight", "blocked", "decision", "bookmark"):
        items = result[cat]
        print("--- %s (%d) ---" % (cat, len(items)))
        for it in items[:6]:
            d = str(it.get("started_at") or "")[:10]
            print("  [%s] %s" % (d, it["text"][:130]))
        print()