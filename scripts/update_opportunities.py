#!/usr/bin/env python3
"""Refresh MAC-Lab calls and academic opportunities.

GitHub Pages is static, so the website cannot crawl opportunity sources when a
visitor opens the page. This script runs in GitHub Actions, gathers public CFP
signals, merges manual lab selections, and writes a Jekyll data file.
"""

from __future__ import annotations

import datetime as dt
import email.utils
import html
import json
import os
import re
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUAL_PATH = ROOT / "_data" / "opportunities_manual.json"
OUTPUT_PATH = ROOT / "_data" / "opportunities.json"

USER_AGENT = "MAC-Lab-OpportunityRadar/1.0 (https://sxhfut.github.io)"
MAX_ITEMS = 80
MAX_AI_DEADLINES_ITEMS = 45
MAX_WIKICFP_ITEMS = 28
DEFAULT_TIMEOUT = 24

AI_DEADLINES_URL = "https://raw.githubusercontent.com/paperswithcode/ai-deadlines/gh-pages/_data/conferences.yml"

WIKICFP_QUERIES = [
    "affective computing",
    "emotion recognition",
    "multimodal emotion",
    "speech emotion recognition",
    "sentiment analysis",
    "empathetic dialogue",
    "AI mental health",
    "digital mental health",
    "psychological assessment artificial intelligence",
    "human computer interaction AI",
    "computing education mental health",
    "learning analytics wellbeing",
    "social computing emotion",
    "computational social science emotion",
    "digital human emotion",
    "human robot interaction emotion",
    "embodied artificial intelligence",
    "wearable sensing mental health",
    "ubiquitous computing mental health",
    "human factors artificial intelligence",
    "cognitive workload artificial intelligence",
    "trustworthy AI human factors",
    "smart cockpit driver monitoring",
]

RELEVANT_SUBJECTS = {
    "AI",
    "ML",
    "NLP",
    "CV",
    "HCI",
    "RO",
    "SP",
    "DM",
    "KR",
}

STRONG_RELEVANCE = re.compile(
    r"affective|emotion|empathy|sentiment|mental health|psycholog|wellbeing|well-being|"
    r"multimodal|speech|voice|facial|expression|gesture|gaze|eye[- ]tracking|wearable|sensor|"
    r"human[- ]computer|hci|human[- ]robot|"
    r"embodied|robot|digital human|agent|dialogue|conversation|counsel|therapy|"
    r"human factors|cognitive|workload|personality|social computing|computational social|"
    r"learning analytics|educational technology|digital health|mhealth|smart cockpit|driver monitoring|"
    r"trustworthy ai|safety|privacy|fairness|explainable|"
    r"情感|心理|身心|多模态|具身|数字人|机器人|人机交互|认知|人因",
    re.IGNORECASE,
)

CORE_RELEVANCE = re.compile(
    r"affective|emotion|empathy|sentiment|mental health|psycholog|wellbeing|well-being|"
    r"multimodal|speech emotion|facial expression|human[- ]computer|hci|human[- ]robot|"
    r"embodied|digital human|dialogue system|conversational|counsel|therapy|"
    r"human factors|cognitive workload|learning analytics|digital health|smart cockpit|"
    r"情感|心理|身心|多模态|具身|数字人|机器人|人机交互|认知|人因",
    re.IGNORECASE,
)

WEAK_ONLY_RELEVANCE = re.compile(
    r"\b(agent|dialogue|voice|sensor|safety|privacy|evidence|education|ai)\b",
    re.IGNORECASE,
)

EXCLUDE_RELEVANCE = re.compile(
    r"cybersecurity|religion|religious|sovereign ai|digital sovereignty|theology|"
    r"cloud computing|parallel and distributed systems|information science",
    re.IGNORECASE,
)

VENUE_HINTS = {
    "ACII": ("Affective Computing", "情感计算", 96),
    "ICMI": ("Multimodal Affective Computing", "多模态情感计算", 92),
    "IVA": ("Embodied Emotional Intelligence", "具身情感智能", 88),
    "HRI": ("Embodied Emotional Intelligence", "具身情感智能", 87),
    "CHI": ("Human-Computer Interaction", "人机交互", 82),
    "CSCW": ("Human-Computer Interaction", "人机交互", 79),
    "IUI": ("Human-Computer Interaction", "人机交互", 78),
    "ACL": ("Affective NLP and Dialogue", "情感 NLP 与对话", 82),
    "EMNLP": ("Affective NLP and Dialogue", "情感 NLP 与对话", 84),
    "NAACL": ("Affective NLP and Dialogue", "情感 NLP 与对话", 80),
    "COLING": ("Affective NLP and Dialogue", "情感 NLP 与对话", 76),
    "INTERSPEECH": ("Speech Emotion and Multimodal Sensing", "语音情感与多模态感知", 83),
    "ICASSP": ("Speech Emotion and Multimodal Sensing", "语音情感与多模态感知", 80),
    "ACM MM": ("Multimodal Affective Computing", "多模态情感计算", 84),
    "MM": ("Multimodal Affective Computing", "多模态情感计算", 72),
    "CVPR": ("Multimodal Affective Computing", "多模态情感计算", 75),
    "ICCV": ("Multimodal Affective Computing", "多模态情感计算", 74),
    "ECCV": ("Multimodal Affective Computing", "多模态情感计算", 74),
    "AAAI": ("AI + Psychology", "AI + 心理", 75),
    "IJCAI": ("AI + Psychology", "AI + 心理", 74),
    "ICLR": ("AI + Psychology", "AI + 心理", 74),
    "ICML": ("AI + Psychology", "AI + 心理", 72),
    "NEURIPS": ("AI + Psychology", "AI + 心理", 73),
    "IROS": ("Embodied Emotional Intelligence", "具身情感智能", 75),
    "ICRA": ("Embodied Emotional Intelligence", "具身情感智能", 75),
    "UBICOMP": ("Ubiquitous Psychological Computing", "普适心理计算", 82),
    "IMWUT": ("Ubiquitous Psychological Computing", "普适心理计算", 80),
    "PERCOM": ("Ubiquitous Psychological Computing", "普适心理计算", 74),
    "ISWC": ("Ubiquitous Psychological Computing", "普适心理计算", 72),
    "CUI": ("Affective NLP and Dialogue", "情感 NLP 与对话", 72),
    "EDM": ("AI + Psychology", "AI + 心理", 70),
    "LAK": ("AI + Psychology", "AI + 心理", 70),
    "AAAI AIES": ("Trustworthy Human-Centered AI", "可信以人为中心 AI", 72),
    "AIES": ("Trustworthy Human-Centered AI", "可信以人为中心 AI", 72),
    "FAccT": ("Trustworthy Human-Centered AI", "可信以人为中心 AI", 72),
}

SUBJECT_TRACKS = {
    "HCI": ("Human-Computer Interaction", "人机交互", 78),
    "NLP": ("Affective NLP and Dialogue", "情感 NLP 与对话", 78),
    "SP": ("Speech Emotion and Multimodal Sensing", "语音情感与多模态感知", 76),
    "RO": ("Embodied Emotional Intelligence", "具身情感智能", 76),
    "CV": ("Multimodal Affective Computing", "多模态情感计算", 70),
    "AI": ("AI + Psychology", "AI + 心理", 69),
    "ML": ("AI + Psychology", "AI + 心理", 66),
    "DM": ("Ubiquitous Psychological Computing", "普适心理计算", 66),
    "KR": ("AI + Psychology", "AI + 心理", 64),
    "SOC": ("Social and Psychological Computing", "社会与心理计算", 66),
    "SE": ("Deployable AI Systems", "可部署 AI 系统", 62),
}

FIT_RULES = [
    (r"affective|emotion|empathy|sentiment", "Affective computing", "情感计算"),
    (r"mental health|psycholog|wellbeing|therapy|counsel", "AI + psychology", "AI + 心理"),
    (r"multimodal|speech|voice|facial|vision|expression", "Multimodal sensing", "多模态感知"),
    (r"dialogue|conversation|language|nlp|acl|emnlp|naacl", "Affective NLP", "情感 NLP"),
    (r"robot|embodied|hri|digital human|agent", "Embodied interaction", "具身交互"),
    (r"hci|human-computer|cscw|iui|chi", "Human-computer interaction", "人机交互"),
    (r"human factors|cognitive|workload|performance", "Human factors", "人因与认知"),
    (r"learning analytics|education|student|school", "Education and student wellbeing", "教育与学生发展"),
    (r"digital health|mhealth|healthcare|clinical", "Digital health", "数字健康"),
    (r"social computing|computational social|group|collective", "Social computing", "社会计算"),
    (r"trustworthy|privacy|safety|fairness|explainable", "Trustworthy AI", "可信 AI"),
    (r"smart cockpit|driver|vehicle|mobility", "Smart cockpit", "智能座舱"),
]


def parse_int_env(name: str, default: int) -> int:
    value = os.getenv(name, "").strip()
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def fetch_url(url: str, retries: int = 2) -> str:
    timeout = parse_int_env("OPPORTUNITY_FETCH_TIMEOUT", DEFAULT_TIMEOUT)
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml,text/plain,*/*",
    }
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=timeout) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read().decode(charset, errors="ignore")
        except (urllib.error.URLError, TimeoutError, socket.timeout) as error:
            last_error = error
            if attempt < retries:
                time.sleep(5 * attempt)
    raise RuntimeError(f"Unable to fetch {url}: {last_error}") from last_error


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = html.unescape(value)
    value = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", value, flags=re.IGNORECASE | re.DOTALL)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def clean_url(value: str | None) -> str:
    if not value:
        return ""
    value = value.replace("&amp;", "&")
    value = re.sub(r"\s+", "", value)
    value = value.replace("©ownerid", "&copyownerid")
    return value.strip()


def unquote_yaml(value: str) -> str:
    value = value.strip()
    if value in {"", "null", "None", "~"}:
        return ""
    if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
        value = value[1:-1]
    return clean_text(value)


def parse_ai_deadlines_records(text: str) -> list[dict]:
    records: list[dict] = []
    current: dict[str, str] | None = None

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        if raw_line.startswith("- "):
            if current:
                records.append(current)
            current = {}
            line = raw_line[2:]
        elif current is not None:
            line = raw_line
        else:
            continue

        match = re.match(r"\s*([A-Za-z0-9_]+):\s*(.*)$", line)
        if match and current is not None:
            key, value = match.groups()
            current[key] = unquote_yaml(value)

    if current:
        records.append(current)
    return records


def parse_date(value: str | None) -> dt.date | None:
    value = clean_text(value)
    if not value or value.upper() in {"TBD", "TBA", "N/A"}:
        return None

    iso_match = re.search(r"(\d{4}-\d{2}-\d{2})", value)
    if iso_match:
        try:
            return dt.date.fromisoformat(iso_match.group(1))
        except ValueError:
            return None

    for fmt in ("%b %d, %Y", "%B %d, %Y", "%d %b %Y", "%d %B %Y"):
        try:
            return dt.datetime.strptime(value, fmt).date()
        except ValueError:
            continue

    try:
        parsed = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError, IndexError):
        return None
    return parsed.date() if parsed else None


def beijing_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).astimezone(dt.timezone(dt.timedelta(hours=8)))


def item_key(item: dict) -> str:
    url = clean_url(item.get("url"))
    title = clean_text(item.get("title")).lower()
    deadline = clean_text(item.get("deadline"))
    return re.sub(r"\W+", "", f"{url}|{title}|{deadline}".lower())


def infer_track(title: str, sub: str = "", text: str = "") -> tuple[str, str, int]:
    haystack = f"{title} {text}".upper()
    for hint, track in VENUE_HINTS.items():
        if hint in haystack:
            return track
    return SUBJECT_TRACKS.get(sub.upper(), ("AI + Psychology", "AI + 心理", 60))


def infer_kind(title: str, source_type: str = "") -> str:
    lowered = title.lower()
    if "workshop" in lowered:
        return "workshop"
    if "challenge" in lowered or "shared task" in lowered:
        return "challenge"
    if "journal" in lowered or "transactions" in lowered or "special issue" in lowered:
        return "journal"
    if source_type == "wikicfp" and ("workshop" in lowered or "cfp" in lowered):
        return "workshop"
    return "conference"


def fit_tags(title: str, summary: str = "") -> tuple[list[str], list[str]]:
    haystack = f"{title} {summary}"
    fits: list[str] = []
    fits_zh: list[str] = []
    for pattern, label, label_zh in FIT_RULES:
        if re.search(pattern, haystack, flags=re.IGNORECASE):
            fits.append(label)
            fits_zh.append(label_zh)
    if not fits:
        fits = ["Research training"]
        fits_zh = ["科研训练"]
    return fits[:4], fits_zh[:4]


def deadline_state(deadline: str, today: dt.date) -> tuple[str, int | None]:
    deadline_lower = clean_text(deadline).lower()
    if deadline_lower in {"rolling", "rolling submissions", "open", "continuous", "year-round"}:
        return "open", None

    parsed = parse_date(deadline)
    if not parsed:
        return "watch", None
    days = (parsed - today).days
    if days < 0:
        return "closed", days
    if days <= 21:
        return "closing_soon", days
    if days <= 90:
        return "open", days
    return "future", days


def build_summary(title: str, track: str, track_zh: str, kind: str, source_type: str) -> tuple[str, str]:
    kind_label = {
        "conference": "conference",
        "workshop": "workshop",
        "journal": "journal or special issue",
        "challenge": "challenge or shared task",
    }.get(kind, "academic opportunity")
    source_note = "official page" if source_type == "official" else "public CFP source"
    summary = (
        f"{title} is tracked as a {kind_label} opportunity around {track}. "
        f"The original {source_note} should be checked before submission planning."
    )
    summary_zh = (
        f"该条目与{track_zh}相关，适合作为论文投稿、专题交流、学生训练或合作选题的时间窗口。"
        "正式准备前请以原始页面的最新要求为准。"
    )
    return summary, summary_zh


def normalize_item(item: dict, today: dt.date) -> dict | None:
    title = clean_text(item.get("title"))
    url = clean_url(item.get("url"))
    if not title or not url:
        return None

    title_zh = clean_text(item.get("title_zh"))
    deadline = clean_text(item.get("deadline"))
    state, days_left = deadline_state(deadline, today)
    if state == "closed" and not item.get("keep_closed"):
        return None

    source_type = clean_text(item.get("source_type")) or "aggregator"
    sub = clean_text(item.get("sub"))
    track = clean_text(item.get("track"))
    track_zh = clean_text(item.get("track_zh"))
    inferred_track, inferred_track_zh, base_score = infer_track(title, sub, clean_text(item.get("summary")))
    track = track or inferred_track
    track_zh = track_zh or inferred_track_zh
    kind = clean_text(item.get("kind")) or infer_kind(title, clean_text(item.get("source")))
    summary = clean_text(item.get("summary"))
    summary_zh = clean_text(item.get("summary_zh"))
    if not summary or not summary_zh:
        fallback, fallback_zh = build_summary(title, track, track_zh, kind, source_type)
        summary = summary or fallback
        summary_zh = summary_zh or fallback_zh

    fits, fits_zh = fit_tags(title, summary)
    relevance = parse_int_env("OPPORTUNITY_DEFAULT_RELEVANCE", base_score)
    if item.get("relevance_score"):
        try:
            relevance = int(item["relevance_score"])
        except (ValueError, TypeError):
            pass
    if STRONG_RELEVANCE.search(f"{title} {summary} {track}"):
        relevance += 8
    if state == "closing_soon":
        relevance += 4
    if source_type == "official":
        relevance += 5
    relevance = max(1, min(100, relevance))

    return {
        "kind": kind,
        "track": track,
        "track_zh": track_zh,
        "title": title,
        "title_zh": title_zh or title,
        "venue": clean_text(item.get("venue")) or title,
        "deadline": deadline,
        "deadline_label": clean_text(item.get("deadline_label")) or "Submission deadline",
        "deadline_tz": clean_text(item.get("deadline_tz") or item.get("timezone")),
        "days_left": days_left,
        "status": state,
        "date": clean_text(item.get("date")),
        "place": clean_text(item.get("place")),
        "source": clean_text(item.get("source")) or ("Official page" if source_type == "official" else "Public CFP index"),
        "source_type": source_type,
        "relevance_score": relevance,
        "summary": summary,
        "summary_zh": summary_zh,
        "fit": item.get("fit") or fits,
        "fit_zh": item.get("fit_zh") or fits_zh,
        "url": url,
    }


def fetch_ai_deadlines_items(today: dt.date) -> list[dict]:
    try:
        records = parse_ai_deadlines_records(fetch_url(AI_DEADLINES_URL))
    except RuntimeError as error:
        print(f"AI Deadlines: {error}")
        return []

    items: list[dict] = []
    horizon = today + dt.timedelta(days=parse_int_env("OPPORTUNITY_HORIZON_DAYS", 540))

    for record in records:
        title = clean_text(record.get("title"))
        year = clean_text(record.get("year"))
        sub = clean_text(record.get("sub")).upper()
        deadline = clean_text(record.get("deadline"))
        parsed_deadline = parse_date(deadline)
        if not title or not parsed_deadline:
            continue
        if parsed_deadline < today or parsed_deadline > horizon:
            continue
        if sub not in RELEVANT_SUBJECTS and not STRONG_RELEVANCE.search(title):
            continue

        display_title = f"{title} {year}".strip()
        track, track_zh, score = infer_track(display_title, sub)
        kind = infer_kind(display_title)
        summary, summary_zh = build_summary(display_title, track, track_zh, kind, "aggregator")
        item = normalize_item(
            {
                "title": display_title,
                "venue": title,
                "deadline": parsed_deadline.isoformat(),
                "deadline_label": "Paper deadline",
                "deadline_tz": clean_text(record.get("timezone")),
                "date": clean_text(record.get("date")),
                "place": clean_text(record.get("place")),
                "sub": sub,
                "track": track,
                "track_zh": track_zh,
                "kind": kind,
                "summary": summary,
                "summary_zh": summary_zh,
                "source": "AI Deadlines",
                "source_type": "aggregator",
                "relevance_score": score,
                "url": clean_text(record.get("link")),
            },
            today,
        )
        if item:
            items.append(item)

    items.sort(key=lambda item: (item.get("deadline") or "9999-12-31", -int(item.get("relevance_score") or 0)))
    return items[: parse_int_env("OPPORTUNITY_AI_DEADLINES_MAX", MAX_AI_DEADLINES_ITEMS)]


def wikicfp_url(query: str) -> str:
    return "http://www.wikicfp.com/cfp/servlet/tool.search?q=" + urllib.parse.quote(query)


def parse_wikicfp_rows(markup: str) -> list[dict]:
    rows: list[dict] = []
    pattern = re.compile(
        r'<tr[^>]*>\s*<td[^>]*rowspan="2"[^>]*>\s*<a href="(?P<href>[^"]+)">(?P<title>.*?)</a>\s*</td>\s*'
        r'<td[^>]*colspan="3"[^>]*>(?P<description>.*?)</td>\s*</tr>\s*'
        r'<tr[^>]*>\s*<td[^>]*>(?P<when>.*?)</td>\s*'
        r'<td[^>]*>(?P<where>.*?)</td>\s*'
        r'<td[^>]*>(?P<deadline>.*?)</td>\s*</tr>',
        re.IGNORECASE | re.DOTALL,
    )
    for match in pattern.finditer(markup):
        href = match.group("href").replace("&amp;", "&")
        if href.startswith("/"):
            href = "http://www.wikicfp.com" + href
        rows.append(
            {
                "title": clean_text(match.group("title")),
                "summary": clean_text(match.group("description")),
                "date": clean_text(match.group("when")),
                "place": clean_text(match.group("where")),
                "deadline": clean_text(match.group("deadline")),
                "url": href,
            }
        )
    return rows


def fetch_wikicfp_items(today: dt.date) -> list[dict]:
    if os.getenv("WIKICFP_DISABLE", "").strip().lower() in {"1", "true", "yes"}:
        return []

    items: list[dict] = []
    seen: set[str] = set()
    horizon = today + dt.timedelta(days=parse_int_env("OPPORTUNITY_HORIZON_DAYS", 540))
    per_query = parse_int_env("WIKICFP_MAX_PER_QUERY", 4)

    for query in WIKICFP_QUERIES:
        try:
            markup = fetch_url(wikicfp_url(query), retries=1)
        except RuntimeError as error:
            print(f"WikiCFP {query}: {error}")
            continue

        kept = 0
        for row in parse_wikicfp_rows(markup):
            parsed_deadline = parse_date(row.get("deadline"))
            if not parsed_deadline or parsed_deadline < today or parsed_deadline > horizon:
                continue
            haystack = f"{row.get('title')} {row.get('summary')}"
            if EXCLUDE_RELEVANCE.search(haystack):
                continue
            if not CORE_RELEVANCE.search(haystack):
                continue
            row["deadline"] = parsed_deadline.isoformat()
            track, track_zh, score = infer_track(clean_text(row.get("title")), text=haystack)
            kind = infer_kind(clean_text(row.get("title")), "wikicfp")
            row.update(
                {
                    "track": track,
                    "track_zh": track_zh,
                    "kind": kind,
                    "source": f"WikiCFP · {query}",
                    "source_type": "aggregator",
                    "deadline_label": "CFP deadline",
                    "relevance_score": score - 2,
                }
            )
            item = normalize_item(row, today)
            if not item:
                continue
            key = item_key(item)
            if key in seen:
                continue
            seen.add(key)
            items.append(item)
            kept += 1
            if kept >= per_query:
                break

    items.sort(key=lambda item: (item.get("deadline") or "9999-12-31", -int(item.get("relevance_score") or 0)))
    return items[: parse_int_env("WIKICFP_MAX_ITEMS", MAX_WIKICFP_ITEMS)]


def load_manual_items(today: dt.date) -> list[dict]:
    if not MANUAL_PATH.exists():
        return []
    try:
        payload = json.loads(MANUAL_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        print(f"Manual opportunities JSON error: {error}")
        return []

    raw_items = payload.get("items", payload if isinstance(payload, list) else [])
    items = []
    for raw_item in raw_items:
        if not isinstance(raw_item, dict):
            continue
        item = normalize_item({**raw_item, "source_type": raw_item.get("source_type") or "official"}, today)
        if item:
            item["manual"] = True
            items.append(item)
    return items


def dedupe_items(items: list[dict]) -> list[dict]:
    merged: dict[str, dict] = {}
    for item in items:
        key = item_key(item)
        if not key:
            continue
        existing = merged.get(key)
        if not existing:
            merged[key] = item
            continue
        existing_score = int(existing.get("relevance_score") or 0)
        item_score = int(item.get("relevance_score") or 0)
        if item.get("manual") or item_score > existing_score:
            merged[key] = item
    return list(merged.values())


def sort_key(item: dict) -> tuple[int, str, int]:
    status_order = {
        "closing_soon": 0,
        "open": 1,
        "future": 2,
        "watch": 3,
        "closed": 4,
    }
    status = status_order.get(clean_text(item.get("status")), 9)
    deadline = clean_text(item.get("deadline")) or "9999-12-31"
    return (status, deadline, -int(item.get("relevance_score") or 0))


def main() -> None:
    now = beijing_now()
    today = now.date()
    max_items = parse_int_env("OPPORTUNITY_MAX_ITEMS", MAX_ITEMS)

    manual_items = load_manual_items(today)
    ai_deadline_items = fetch_ai_deadlines_items(today)
    wikicfp_items = fetch_wikicfp_items(today)

    items = dedupe_items(manual_items + ai_deadline_items + wikicfp_items)
    items.sort(key=sort_key)
    items = items[:max_items]

    stats = {
        "items": len(items),
        "manual_items": len([item for item in items if item.get("manual")]),
        "ai_deadlines_items": len([item for item in items if item.get("source") == "AI Deadlines"]),
        "wikicfp_items": len([item for item in items if str(item.get("source", "")).startswith("WikiCFP")]),
        "official_items": len([item for item in items if item.get("source_type") == "official"]),
        "closing_soon_items": len([item for item in items if item.get("status") == "closing_soon"]),
        "open_items": len([item for item in items if item.get("status") in {"closing_soon", "open"}]),
    }

    payload = {
        "generated_at": now.isoformat(),
        "generated_date_beijing": today.isoformat(),
        "refresh_cadence": "daily",
        "stats": stats,
        "sources": [
            {
                "name": "AI Deadlines",
                "url": "https://aideadlin.es/",
                "type": "aggregator",
            },
            {
                "name": "WikiCFP",
                "url": "http://www.wikicfp.com/cfp/",
                "type": "aggregator",
            },
            {
                "name": "Manual MAC-Lab selections",
                "url": "_data/opportunities_manual.json",
                "type": "curated",
            },
        ],
        "items": items,
    }

    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)} with {len(items)} opportunity items.")


if __name__ == "__main__":
    main()
