#!/usr/bin/env python3
"""Update MAC-Lab frontier radar data.

The site is hosted on GitHub Pages, so it cannot run server-side crawlers at
request time. This script fetches open metadata from arXiv, merges it with
curated industry/translation signals, and writes a static JSON file for Jekyll.
"""

from __future__ import annotations

import datetime as dt
import email.utils
import html
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUAL_PATH = ROOT / "_data" / "frontiers_manual.json"
OUTPUT_PATH = ROOT / "_data" / "frontiers.json"

MAX_ITEMS = 36
USER_AGENT = "MAC-Lab-FrontierRadar/1.0 (https://sxhfut.github.io)"

ARXIV_QUERIES = [
    {
        "track": "AI + Psychology",
        "query": 'all:"mental health" AND (all:"large language model" OR all:"artificial intelligence" OR all:"machine learning")',
    },
    {
        "track": "Affective Computing",
        "query": 'all:"affective computing" OR all:"emotion recognition" OR all:"emotion understanding"',
    },
    {
        "track": "Empathetic Dialogue",
        "query": 'all:"emotional support conversation" OR all:"empathetic dialogue" OR all:"counseling dialogue"',
    },
    {
        "track": "Embodied Emotional Intelligence",
        "query": 'all:"embodied intelligence" AND (all:"emotion" OR all:"affective" OR all:"human interaction")',
    },
    {
        "track": "Ubiquitous Psychological Computing",
        "query": 'all:"psychological computing" OR all:"psychological assessment" OR all:"depression detection"',
    },
]


def fetch_url(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def iso_date(value: str | None) -> str:
    if not value:
        return ""
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        parsed = email.utils.parsedate_to_datetime(value)
        return parsed.date().isoformat()


def summarize(text: str, limit: int = 430) -> str:
    text = clean_text(text)
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return f"{cut}..."


def arxiv_feed_url(query: str, max_results: int = 12) -> str:
    params = urllib.parse.urlencode(
        {
            "search_query": query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    return f"https://export.arxiv.org/api/query?{params}"


def fetch_arxiv_items() -> list[dict]:
    namespace = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    seen: set[str] = set()
    items: list[dict] = []

    for source in ARXIV_QUERIES:
        data = fetch_url(arxiv_feed_url(source["query"]))
        root = ET.fromstring(data)
        for entry in root.findall("atom:entry", namespace):
            url = clean_text(entry.findtext("atom:id", namespaces=namespace))
            canonical_url = re.sub(r"v\d+$", "", url)
            if canonical_url in seen:
                continue
            seen.add(canonical_url)

            authors = [
                clean_text(author.findtext("atom:name", namespaces=namespace))
                for author in entry.findall("atom:author", namespace)
            ]
            categories = [
                category.attrib.get("term", "")
                for category in entry.findall("atom:category", namespace)
                if category.attrib.get("term")
            ]
            title = clean_text(entry.findtext("atom:title", namespaces=namespace))
            summary = summarize(entry.findtext("atom:summary", namespaces=namespace) or "")
            published = iso_date(entry.findtext("atom:published", namespaces=namespace))
            items.append(
                {
                    "kind": "paper",
                    "track": source["track"],
                    "published": published,
                    "title": title,
                    "summary": summary,
                    "source": "arXiv",
                    "authors": authors[:6],
                    "categories": categories[:4],
                    "url": canonical_url,
                    "priority": 50,
                }
            )
        time.sleep(3)
    return items


def load_manual_items() -> list[dict]:
    if not MANUAL_PATH.exists():
        return []
    return json.loads(MANUAL_PATH.read_text(encoding="utf-8"))


def item_sort_key(item: dict) -> tuple[str, int]:
    return (f"{int(item.get('priority', 0)):03d}", item.get("published", ""))


def main() -> None:
    manual_items = load_manual_items()
    arxiv_items = fetch_arxiv_items()

    merged = manual_items + arxiv_items
    merged.sort(key=item_sort_key, reverse=True)
    merged = merged[:MAX_ITEMS]

    payload = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "sources": {
            "papers": "arXiv open metadata API",
            "manual": "Curated industry, media, standards, and lab translation signals",
        },
        "queries": ARXIV_QUERIES,
        "items": merged,
    }
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(merged)} items to {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
