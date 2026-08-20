# -*- coding: utf-8 -*-
"""Multi-source data fetcher: research/ GitHub repo + hermes session DB.

No external deps (except urllib/requests, both stdlib). Cron-friendly.
"""
import json
import urllib.request
import urllib.error
import datetime as dt
from pathlib import Path
from typing import Optional

from .config import GH_TOKEN, GH_USER, RESEARCH_REPO


def _gh_api(path: str, method: str = "GET", body: Optional[dict] = None) -> Optional[dict]:
    """Call GitHub API. Returns parsed JSON or None on error."""
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"token {GH_TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "sorelferris-site-sync")
    data = json.dumps(body).encode() if body else None
    try:
        with urllib.request.urlopen(req, data=data, timeout=20) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"[GH API {e.code}] {path}: {e.reason}")
        return None
    except Exception as e:
        print(f"[GH API error] {path}: {e}")
        return None


def get_research_tree(path: str = "") -> list:
    """Recursively get research repo tree via /contents/{path}.
    Returns list of {name, type, path, size, sha} dicts.
    """
    data = _gh_api(f"/repos/{RESEARCH_REPO}/contents/{path}")
    if not isinstance(data, list):
        return []
    return [
        {
            "name": x["name"],
            "type": x["type"],
            "path": x["path"],
            "size": x.get("size", 0),
            "sha": x.get("sha"),
        }
        for x in data
    ]


def get_research_file(path: str) -> Optional[str]:
    """Read raw file content from research repo. Returns decoded utf-8 string."""
    url = f"https://raw.githubusercontent.com/{GH_USER}/{RESEARCH_REPO}/main/{path}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "sorelferris-site-sync")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"[research raw {e.code}] {path}: {e.reason}")
        return None
    except Exception as e:
        print(f"[research raw error] {path}: {e}")
        return None


def list_research_papers() -> list:
    """List all subdirectories under research/papers/, each a paper notebook.
    Returns: [{name, path, has_readme, first_note}, ...]
    """
    items = get_research_tree("papers")
    papers = []
    for it in items:
        if it["type"] != "dir":
            continue
        sub = get_research_tree(f"papers/{it['name']}")
        has_readme = any(s["name"].lower() in ("readme.md", "index.md", "notes.md") for s in sub)
        first_md = next((s for s in sub if s["name"].endswith(".md")), None)
        papers.append({
            "name": it["name"],
            "path": it["path"],
            "has_readme": has_readme,
            "first_note": first_md["name"] if first_md else None,
        })
    return papers


def list_research_roadmap() -> list:
    """List all .md files under research/roadmap/, each a quarterly plan.
    Returns: [{name, path, size, content}, ...]
    """
    items = get_research_tree("roadmap")
    out = []
    for it in items:
        if not it["name"].endswith(".md"):
            continue
        content = get_research_file(f"roadmap/{it['name']}")
        out.append({
            "name": it["name"],
            "path": it["path"],
            "size": it["size"],
            "content": content or "",
        })
    return out


if __name__ == "__main__":
    print("=== research/papers ===")
    papers = list_research_papers()
    for p in papers:
        print(f"  {p['name']:<30} has_readme={p['has_readme']} first_note={p.get('first_note')}")

    print("\n=== research/roadmap ===")
    rm = list_research_roadmap()
    for r in rm:
        print(f"  {r['name']:<30} size={r['size']} content_len={len(r['content'])}")