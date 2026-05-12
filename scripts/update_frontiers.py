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
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUAL_PATH = ROOT / "_data" / "frontiers_manual.json"
OUTPUT_PATH = ROOT / "_data" / "frontiers.json"

MAX_ITEMS = 48
MAX_RESULTS_PER_QUERY = 12
USER_AGENT = "MAC-Lab-FrontierRadar/1.0 (https://sxhfut.github.io)"

ARXIV_QUERIES = [
    {
        "track": "AI + Psychology",
        "query": 'all:"mental health" AND (all:"large language model" OR all:"artificial intelligence" OR all:"machine learning")',
    },
    {
        "track": "AI + Mind-Body Health",
        "query": 'all:"digital mental health" OR all:"AI mental health" OR all:"mental health chatbot"',
    },
    {
        "track": "Affective Computing",
        "query": 'all:"affective computing" OR all:"emotion recognition" OR all:"emotion understanding"',
    },
    {
        "track": "Multimodal Affective Computing",
        "query": 'all:"multimodal emotion recognition" OR all:"multimodal affective" OR all:"speech emotion recognition"',
    },
    {
        "track": "Empathetic Dialogue",
        "query": 'all:"emotional support conversation" OR all:"empathetic dialogue" OR all:"counseling dialogue"',
    },
    {
        "track": "Embodied Emotional Intelligence",
        "query": '(all:"embodied intelligence" OR all:"human robot interaction" OR all:"digital human") AND (all:"emotion" OR all:"affective" OR all:"empathy" OR all:"human interaction")',
    },
    {
        "track": "Ubiquitous Psychological Computing",
        "query": 'all:"psychological computing" OR all:"psychological assessment" OR all:"depression detection"',
    },
]

TRACK_LENSES = {
    "AI + Psychology": {
        "lens": "Relevant to MAC-Lab's psychological computing route: it connects AI models with assessment, risk identification, and human-centered support.",
        "lens_zh": "对应 MAC-Lab 的心理计算路线：把 AI 模型与评估、风险识别和以人为中心的支持连接起来。",
    },
    "AI + Mind-Body Health": {
        "lens": "Relevant to mind-body health platforms: it can inform screening, monitoring, intervention, and deployable mental-care systems.",
        "lens_zh": "对应 AI 身心健康平台：可为筛查、监测、干预和可部署心理关护系统提供参考。",
    },
    "Affective Computing": {
        "lens": "Relevant to the lab's affective-computing foundation: it strengthens emotion perception, affective semantics, and interaction understanding.",
        "lens_zh": "对应实验室情感计算根基：强化情绪感知、情感语义和交互理解能力。",
    },
    "Multimodal Affective Computing": {
        "lens": "Relevant to MAC-Lab's original multimedia affective computing identity: it connects speech, vision, behavior, physiology, and context.",
        "lens_zh": "对应 MAC-Lab 多模态情感计算本源：连接语音、视觉、行为、生理与场景信息。",
    },
    "Empathetic Dialogue": {
        "lens": "Relevant to emotional support agents: it connects affective NLP, dialogue safety, counseling interaction, and long-term companionship.",
        "lens_zh": "对应情感支持智能体：连接情感 NLP、对话安全、咨询交互和长期陪伴能力。",
    },
    "Embodied Emotional Intelligence": {
        "lens": "Relevant to embodied emotional intelligence: it informs robots, digital humans, smart cockpits, and situated emotional interaction.",
        "lens_zh": "对应具身情感智能：服务机器人、数字人、智能座舱和场景化情感交互。",
    },
    "Ubiquitous Psychological Computing": {
        "lens": "Relevant to ubiquitous psychological computing: it supports continuous sensing, psychological profiling, early warning, and real-world intervention.",
        "lens_zh": "对应普适心理计算：支撑连续感知、心理画像、早期预警和真实场景干预。",
    },
}

CAPABILITY_RULES = [
    (r"large language model|llm|foundation model|agent", "Affective LLMs", "情感大模型"),
    (r"multimodal|speech|voice|facial|vision|gait|physiolog|eeg|sensor", "Multimodal Sensing", "多模态感知"),
    (r"depression|anxiety|mental health|psychological|crisis|counsel", "Psychological Assessment", "心理评估"),
    (r"intervention|support|therapy|well-being|wellbeing|care", "Mind-Body Support", "身心支持"),
    (r"robot|embodied|digital human|human-robot|cockpit|companion", "Embodied Interaction", "具身交互"),
    (r"safety|privacy|risk|trust|temporal evidence|benchmark", "Trustworthy Evaluation", "可信评测"),
    (r"emotion recognition|affective|emotion understanding|empathy", "Affective Understanding", "情感理解"),
]


def fetch_url(url: str, retries: int = 3) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError, socket.timeout) as error:
            last_error = error
            if attempt < retries:
                time.sleep(8 * attempt)
    raise RuntimeError(f"Unable to fetch {url}: {last_error}") from last_error


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


def arxiv_feed_url(query: str, max_results: int = MAX_RESULTS_PER_QUERY) -> str:
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


def infer_capability_tags(item: dict) -> tuple[list[str], list[str]]:
    text = " ".join(
        str(item.get(field, ""))
        for field in ("track", "title", "title_zh", "summary", "summary_zh")
    ).lower()
    tags: list[str] = []
    tags_zh: list[str] = []
    for pattern, tag, tag_zh in CAPABILITY_RULES:
        if re.search(pattern, text) and tag not in tags:
            tags.append(tag)
            tags_zh.append(tag_zh)
    if not tags:
        tags.append(item.get("track", "Frontier Signal"))
        tags_zh.append(item.get("track", "前沿信号"))
    return tags[:5], tags_zh[:5]


def relevance_score(item: dict, tags: list[str]) -> int:
    score = int(item.get("priority", 50))
    score += min(len(tags), 5) * 6
    if item.get("kind") != "paper":
        score += 12
    text = " ".join(str(item.get(field, "")) for field in ("title", "summary")).lower()
    for phrase in ("mental health", "affective", "emotion", "psychological", "embodied", "multimodal"):
        if phrase in text:
            score += 3
    return min(score, 100)


def enrich_item(item: dict) -> dict:
    item = dict(item)
    lens = TRACK_LENSES.get(item.get("track", ""), TRACK_LENSES["Affective Computing"])
    tags, tags_zh = infer_capability_tags(item)
    item.setdefault("lens", lens["lens"])
    item.setdefault("lens_zh", lens["lens_zh"])
    item["capability_tags"] = tags
    item["capability_tags_zh"] = tags_zh
    item["relevance_score"] = relevance_score(item, tags)
    return item


def load_existing_items() -> list[dict]:
    if not OUTPUT_PATH.exists():
        return []
    try:
        payload = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return payload.get("items", [])


def fetch_arxiv_items(existing_items: list[dict] | None = None) -> list[dict]:
    namespace = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    seen: set[str] = set()
    items: list[dict] = []
    existing_by_track: dict[str, list[dict]] = {}
    for item in existing_items or []:
        if item.get("kind") == "paper" and item.get("source") == "arXiv":
            existing_by_track.setdefault(item.get("track", ""), []).append(item)

    for source in ARXIV_QUERIES:
        track = source["track"]
        try:
            data = fetch_url(arxiv_feed_url(source["query"]))
        except RuntimeError as error:
            fallback = existing_by_track.get(track, [])[:MAX_RESULTS_PER_QUERY]
            if fallback:
                print(
                    f"Warning: reused {len(fallback)} existing {track} items after fetch failure: {error}"
                )
                for item in fallback:
                    canonical_url = re.sub(r"v\d+$", "", item.get("url", ""))
                    if canonical_url and canonical_url not in seen:
                        seen.add(canonical_url)
                        items.append(item)
            else:
                print(f"Warning: skipped {track} after fetch failure: {error}")
            continue
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
        time.sleep(10)
    return items


def load_manual_items() -> list[dict]:
    if not MANUAL_PATH.exists():
        return []
    return json.loads(MANUAL_PATH.read_text(encoding="utf-8"))


def item_sort_key(item: dict) -> tuple[str, int]:
    return (f"{int(item.get('priority', 0)):03d}", item.get("published", ""))


def main() -> None:
    existing_items = load_existing_items()
    manual_items = [enrich_item(item) for item in load_manual_items()]
    arxiv_items = [enrich_item(item) for item in fetch_arxiv_items(existing_items)]

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
