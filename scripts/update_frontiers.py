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
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUAL_PATH = ROOT / "_data" / "frontiers_manual.json"
OUTPUT_PATH = ROOT / "_data" / "frontiers.json"

MAX_ITEMS = 60
MAX_RESULTS_PER_QUERY = 12
USER_AGENT = "MAC-Lab-FrontierRadar/1.0 (https://sxhfut.github.io)"

LAST30DAYS_DEFAULT_TOPICS = [
    ("AI + Psychology", "AI psychology mental health"),
    ("AI + Mind-Body Health", "AI mental health digital wellbeing"),
    ("Affective Computing", "affective computing emotion AI"),
    ("Multimodal Affective Computing", "multimodal affective computing speech emotion"),
    ("Empathetic Dialogue", "empathetic dialogue emotional support chatbot"),
    ("Embodied Emotional Intelligence", "embodied emotional intelligence robot emotion"),
    ("Ubiquitous Psychological Computing", "ubiquitous psychological computing psychological assessment"),
]
LAST30DAYS_DEFAULT_SOURCES = "reddit,hn,polymarket,github"

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


def parse_bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def parse_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


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


def last30days_skill_root() -> Path | None:
    configured = os.getenv("LAST30DAYS_SKILL_ROOT", "").strip()
    candidates = []
    if configured:
        candidates.append(Path(configured).expanduser())
    candidates.extend(
        [
            Path.home() / ".codex" / "skills" / "last30days",
            Path.home() / ".agents" / "skills" / "last30days",
            Path.home() / ".claude" / "skills" / "last30days",
        ]
    )
    for candidate in candidates:
        if (candidate / "scripts" / "last30days.py").exists():
            return candidate
    return None


def last30days_topics() -> list[tuple[str, str]]:
    configured = os.getenv("LAST30DAYS_TOPICS", "").strip()
    if not configured:
        return LAST30DAYS_DEFAULT_TOPICS

    topics: list[tuple[str, str]] = []
    for raw_topic in configured.split(";"):
        raw_topic = raw_topic.strip()
        if not raw_topic:
            continue
        if "::" in raw_topic:
            track, topic = raw_topic.split("::", 1)
            topics.append((track.strip() or "Last 30 Days", topic.strip()))
        else:
            topics.append(("Last 30 Days", raw_topic))
    return topics or LAST30DAYS_DEFAULT_TOPICS


def build_last30days_plan(topic: str, sources: list[str]) -> dict:
    source_weights = {source: round(1 / len(sources), 4) for source in sources}
    return {
        "intent": "concept",
        "freshness_mode": "last_30_days",
        "cluster_mode": "theme",
        "raw_topic": topic,
        "source_weights": source_weights,
        "notes": [
            "MAC-Lab frontier radar scheduled enrichment",
            "Prioritize public discourse, application signals, open-source activity, and community concerns.",
        ],
        "subqueries": [
            {
                "label": "research",
                "search_query": topic,
                "ranking_query": f"Recent high-signal discussion, deployment evidence, and open-source activity about {topic}",
                "sources": sources,
                "weight": 1.0,
            }
        ],
    }


def extract_json_payload(raw_output: str) -> dict | None:
    start = raw_output.find("{")
    end = raw_output.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(raw_output[start : end + 1])
    except json.JSONDecodeError:
        return None


def first_source_item(candidate: dict) -> dict:
    source_items = candidate.get("source_items") or []
    if source_items and isinstance(source_items[0], dict):
        return source_items[0]
    return {}


def source_label(source: str) -> str:
    labels = {
        "reddit": "Reddit",
        "hackernews": "Hacker News",
        "github": "GitHub",
        "polymarket": "Polymarket",
        "youtube": "YouTube",
        "x": "X",
        "xiaohongshu": "Xiaohongshu",
    }
    return labels.get(source, source.title())


def last30days_item_from_candidate(candidate: dict, track: str, topic: str, range_to: str) -> dict | None:
    url = clean_text(candidate.get("url"))
    title = clean_text(candidate.get("title"))
    if not url or not title:
        return None

    primary = first_source_item(candidate)
    source = clean_text(candidate.get("source") or primary.get("source") or "last30days")
    published = clean_text(primary.get("published_at") or range_to)
    snippet = clean_text(candidate.get("snippet") or primary.get("snippet") or primary.get("body") or "")
    container = clean_text(primary.get("container") or "")
    author = clean_text(primary.get("author") or "")
    authors = [value for value in (author, container) if value]
    score = float(candidate.get("final_score") or candidate.get("rerank_score") or 45)
    summary_parts = []
    if snippet:
        summary_parts.append(summarize(snippet, 360))
    summary_parts.append(
        f"Last30Days signal for {topic}, surfaced from {source_label(source)} public activity in the latest 30-day window."
    )

    return {
        "kind": "community",
        "track": track,
        "published": published,
        "title": title,
        "summary": " ".join(summary_parts),
        "source": f"Last30Days · {source_label(source)}",
        "authors": authors[:3],
        "categories": [source_label(value) for value in candidate.get("sources", [])[:4]],
        "url": url,
        "priority": min(75, 54 + int(score // 8)),
    }


def fetch_last30days_items() -> list[dict]:
    if parse_bool_env("LAST30DAYS_DISABLE"):
        print("Last30Days: disabled by LAST30DAYS_DISABLE.")
        return []

    skill_root = last30days_skill_root()
    if not skill_root:
        print("Last30Days: skill root not found; skipping community radar enrichment.")
        return []

    python = os.getenv("LAST30DAYS_PYTHON") or sys.executable
    sources_flag = os.getenv("LAST30DAYS_SOURCES", LAST30DAYS_DEFAULT_SOURCES)
    sources = [source.strip() for source in sources_flag.split(",") if source.strip()]
    max_topics = parse_int_env("LAST30DAYS_MAX_TOPICS", 4)
    per_topic = parse_int_env("LAST30DAYS_ITEMS_PER_TOPIC", 2)
    timeout = parse_int_env("LAST30DAYS_TIMEOUT", 180)
    use_mock = parse_bool_env("LAST30DAYS_MOCK")
    items: list[dict] = []

    for track, topic in last30days_topics()[:max_topics]:
        plan = build_last30days_plan(topic, sources)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as plan_file:
            json.dump(plan, plan_file, ensure_ascii=False)
            plan_path = plan_file.name
        command = [
            python,
            str(skill_root / "scripts" / "last30days.py"),
            "--emit=json",
            "--quick",
            "--days",
            "30",
            "--search",
            sources_flag,
            "--web-backend",
            "none",
            "--plan",
            plan_path,
            topic,
        ]
        if use_mock:
            command.insert(2, "--mock")
        try:
            completed = subprocess.run(
                command,
                cwd=skill_root,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            print(f"Last30Days: skipped {topic} after runtime error: {error}")
            Path(plan_path).unlink(missing_ok=True)
            continue
        finally:
            Path(plan_path).unlink(missing_ok=True)

        if completed.returncode != 0:
            error_text = summarize(completed.stderr or completed.stdout, 280)
            print(f"Last30Days: skipped {topic} after exit {completed.returncode}: {error_text}")
            continue

        payload = extract_json_payload(completed.stdout)
        if not payload:
            print(f"Last30Days: skipped {topic}; JSON payload not found.")
            continue

        range_to = payload.get("range_to") or dt.datetime.now(dt.timezone.utc).date().isoformat()
        candidates = payload.get("ranked_candidates") or []
        added_for_topic = 0
        for candidate in candidates:
            item = last30days_item_from_candidate(candidate, track, topic, range_to)
            if not item:
                continue
            items.append(enrich_item(item))
            added_for_topic += 1
            if added_for_topic >= per_topic:
                break
        print(f"Last30Days: added {added_for_topic} items for {topic}.")

    return items


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
    if parse_bool_env("ARXIV_DISABLE"):
        print("arXiv: disabled by ARXIV_DISABLE.")
        return []

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


def dedupe_items(items: list[dict]) -> list[dict]:
    seen: set[str] = set()
    deduped: list[dict] = []
    for item in items:
        key = item.get("url") or item.get("title", "")
        key = re.sub(r"v\d+$", "", key)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def item_sort_key(item: dict) -> tuple[str, int]:
    return (f"{int(item.get('priority', 0)):03d}", item.get("published", ""))


def main() -> None:
    existing_items = load_existing_items()
    manual_items = [enrich_item(item) for item in load_manual_items()]
    last30days_items = fetch_last30days_items()
    arxiv_items = [enrich_item(item) for item in fetch_arxiv_items(existing_items)]

    merged = dedupe_items(manual_items + last30days_items + arxiv_items)
    merged.sort(key=item_sort_key, reverse=True)
    merged = merged[:MAX_ITEMS]

    payload = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "sources": {
            "papers": "arXiv open metadata API",
            "last30days": "Recent public discourse, open-source, and market signals via last30days-skill",
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
