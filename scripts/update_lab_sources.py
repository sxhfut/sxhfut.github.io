#!/usr/bin/env python3
"""Update source-backed MAC-Lab authority and publication signals.

GitHub Pages is static, so public-source refreshes need to happen before the
site is built. This script reads public pages and APIs that do not require a
secret key, then writes a compact JSON file for Jekyll pages, RSS, and AI-search
metadata.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import re
import socket
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "_data" / "lab_sources.json"

HFUT_ROOT = "https://faculty.hfut.edu.cn"
HFUT_BLOG_BASE = "https://faculty.hfut.edu.cn/sunxiao/zh_CN/article/198496/list"
HFUT_PROFILE_URL = "https://faculty.hfut.edu.cn/sunxiao/zh_CN/index.htm"
ORCID_ID = "0000-0001-9750-7032"
ORCID_WORKS_URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
DBLP_PERSON_URL = "https://dblp.org/pid/30/202-3.html"
DBLP_XML_URL = "https://dblp.org/pid/30/202-3.xml"
OPENALEX_AUTHOR_URL = "https://openalex.org/A5088062069"
OPENALEX_API_AUTHOR_URL = f"https://api.openalex.org/authors/https://orcid.org/{ORCID_ID}"
CROSSREF_ORCID_WORKS_URL = f"https://api.crossref.org/works?filter=orcid:{ORCID_ID}&rows=5&select=DOI,title,published-print,published-online,container-title,author"
GOOGLE_SCHOLAR_QUERY_URL = "https://scholar.google.com/scholar?q=%22Xiao+Sun%22+%22Hefei+University+of+Technology%22+%22affective+computing%22"
USER_AGENT = "MAC-Lab-SourceSync/1.0 (https://sxhfut.github.io)"

HIGH_SIGNAL_VENUE_RE = re.compile(
    r"IEEE|ACM Transactions|ACM Multimedia|ACL|EMNLP|ICASSP|CVPR|AAAI|IJCAI|"
    r"COLING|CIKM|SIGIR|PNAS|Nature(?!\\s+Portfolio)|\\bScience\\b",
    re.IGNORECASE,
)

TRACK_RULES = [
    (re.compile(r"affective|emotion|empathy|sentiment|情感|情绪|共情", re.I), "Affective Computing", "情感计算"),
    (re.compile(r"dialogue|conversation|support|NLP|language|对话|自然语言", re.I), "Affective NLP", "情感 NLP"),
    (re.compile(r"multimodal|facial|speech|voice|image|vision|多模态|语音|表情|视觉", re.I), "Multimodal Affective Computing", "多模态情感计算"),
    (re.compile(r"psycholog|depression|mental|personality|心理|抑郁|人格", re.I), "Ubiquitous Psychological Computing", "普适心理计算"),
    (re.compile(r"robot|embodied|digital human|具身|机器人|数字人", re.I), "Embodied Emotional Intelligence", "具身情感智能"),
]


def fetch_bytes(url: str, timeout: int = 24) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def load_existing_payload() -> dict:
    if not OUTPUT_PATH.exists():
        return {}
    try:
        return json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def fetch_text(url: str, timeout: int = 24) -> str:
    return fetch_bytes(url, timeout=timeout).decode("utf-8", "ignore")


def fetch_json(url: str, timeout: int = 24) -> dict:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
    )
    return json.loads(urllib.request.urlopen(request, timeout=timeout).read().decode("utf-8"))


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", value, flags=re.S | re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    return " ".join(html.unescape(value).split())


def absolute_hfut_url(href: str) -> str:
    return urllib.parse.urljoin(HFUT_ROOT, href)


def parse_date_parts(date: dict | None) -> str:
    if not date:
        return ""
    year = ((date.get("year") or {}).get("value") or "").zfill(4)
    month = ((date.get("month") or {}).get("value") or "01").zfill(2)
    day = ((date.get("day") or {}).get("value") or "01").zfill(2)
    if not year.strip("0"):
        return ""
    return f"{year}-{month}-{day}"


def item_track(text: str) -> tuple[str, str]:
    for pattern, track, track_zh in TRACK_RULES:
        if pattern.search(text):
            return track, track_zh
    return "MAC-Lab", "实验室建设"


def is_high_signal_publication(title: str, venue: str) -> bool:
    combined = f"{venue} {title}"
    if "Brain Sciences" in venue or "Applied Sciences" in venue or venue == "Information":
        return False
    if HIGH_SIGNAL_VENUE_RE.search(combined):
        return True
    if "Transactions" in venue:
        return True
    if venue in {"PNAS Nexus", "Nature", "Science"}:
        return True
    return False


def source_item_key(item: dict) -> str:
    return (item.get("url") or item.get("title") or "").strip().lower()


def dedupe(items: list[dict]) -> list[dict]:
    seen: set[str] = set()
    result: list[dict] = []
    for item in items:
        key = source_item_key(item)
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def fetch_hfut_blog_items() -> tuple[list[dict], dict]:
    items: list[dict] = []
    errors: list[str] = []
    total_public = None
    for page in range(1, 7):
        url = f"{HFUT_BLOG_BASE}/index.htm" if page == 1 else f"{HFUT_BLOG_BASE}/{page}.htm"
        try:
            text = fetch_text(url)
        except (urllib.error.URLError, TimeoutError, socket.timeout) as error:
            errors.append(f"{url}: {error}")
            continue

        total_match = re.search(r"共\s*(\d+)\s*条", text)
        if total_match:
            total_public = int(total_match.group(1))

        for match in re.finditer(r'<a[^>]+href="([^"]*?/article/198496/content/[^"]+)"[^>]*>(.*?)</a>', text, re.S | re.I):
            raw_title = clean_text(match.group(2))
            date_match = re.search(r"(\d{4}-\d{2}-\d{2})$", raw_title)
            published = date_match.group(1) if date_match else ""
            title_zh = raw_title[: -len(published)].strip() if published else raw_title
            track, track_zh = item_track(title_zh)
            items.append(
                {
                    "kind": "faculty_blog",
                    "source": "HFUT Faculty Blog",
                    "published": published,
                    "title": title_zh,
                    "title_zh": title_zh,
                    "summary": "Official HFUT faculty-page update from Professor Xiao Sun's public blog.",
                    "summary_zh": "来自孙晓教授合工大教师主页的公开动态。",
                    "track": track,
                    "track_zh": track_zh,
                    "url": absolute_hfut_url(match.group(1)),
                    "priority": 92 if published.startswith("2026") else 84,
                }
            )

    items = dedupe(items)
    items.sort(key=lambda item: (item.get("published") or "", item.get("priority") or 0), reverse=True)
    return items, {"total_public": total_public or len(items), "errors": errors}


def external_id_url(summary: dict) -> str:
    external_ids = ((summary.get("external-ids") or {}).get("external-id") or [])
    for external_id in external_ids:
        if external_id.get("external-id-type") == "doi":
            url = ((external_id.get("external-id-url") or {}).get("value") or "").strip()
            value = (external_id.get("external-id-value") or "").strip()
            if url:
                return url
            if value:
                return "https://doi.org/" + value
    return ((summary.get("url") or {}).get("value") or "").strip()


def fetch_orcid_items() -> tuple[list[dict], dict]:
    last_error = ""
    payload = None
    for attempt in range(1, 4):
        try:
            request = urllib.request.Request(
                ORCID_WORKS_URL,
                headers={"Accept": "application/json", "User-Agent": USER_AGENT},
            )
            payload = json.loads(urllib.request.urlopen(request, timeout=45).read().decode("utf-8"))
            break
        except (urllib.error.URLError, TimeoutError, socket.timeout, json.JSONDecodeError) as error:
            last_error = str(error)
    if payload is None:
        return [], {"orcid_id": ORCID_ID, "error": last_error, "total_groups": 0, "highlighted": 0}

    items: list[dict] = []
    for group in payload.get("group", []):
        summaries = group.get("work-summary") or []
        if not summaries:
            continue
        summary = summaries[0]
        title = clean_text(((summary.get("title") or {}).get("title") or {}).get("value"))
        venue = clean_text((summary.get("journal-title") or {}).get("value"))
        published = parse_date_parts(summary.get("publication-date"))
        url = external_id_url(summary)
        text_for_track = f"{title} {venue}"
        high_signal = is_high_signal_publication(title, venue)
        if not title or not published or not url:
            continue
        if not high_signal:
            continue
        track, track_zh = item_track(text_for_track)
        summary_en = f"{venue} publication signal from Professor Xiao Sun's ORCID record." if venue else "Publication signal from Professor Xiao Sun's ORCID record."
        summary_zh = f"孙晓教授 ORCID 记录中的 {venue} 论文成果。" if venue else "孙晓教授 ORCID 记录中的论文成果。"
        items.append(
            {
                "kind": "publication",
                "source": "ORCID / DOI",
                "published": published,
                "title": title,
                "title_zh": title,
                "summary": summary_en,
                "summary_zh": summary_zh,
                "venue": venue,
                "track": track,
                "track_zh": track_zh,
                "url": url,
                "priority": 94 if published.startswith("2026") else 88,
            }
        )

    items = dedupe(items)
    items.sort(key=lambda item: (item.get("published") or "", item.get("priority") or 0), reverse=True)
    return items, {"orcid_id": ORCID_ID, "total_groups": len(payload.get("group", [])), "highlighted": len(items)}


def fetch_dblp_items() -> tuple[list[dict], dict]:
    try:
        raw = fetch_bytes(DBLP_XML_URL, timeout=14)
        root = ET.fromstring(raw)
    except (urllib.error.URLError, TimeoutError, socket.timeout, ET.ParseError) as error:
        return [], {"url": DBLP_PERSON_URL, "xml_url": DBLP_XML_URL, "error": str(error), "items": 0}

    items: list[dict] = []
    for pub in root.findall("./r/*"):
        title = clean_text(pub.findtext("title"))
        year = clean_text(pub.findtext("year"))
        venue = clean_text(pub.findtext("journal") or pub.findtext("booktitle"))
        url = clean_text(pub.findtext("ee"))
        if not title or not year or not url:
            continue
        text_for_track = f"{title} {venue}"
        if not is_high_signal_publication(title, venue):
            continue
        track, track_zh = item_track(text_for_track)
        items.append(
            {
                "kind": "publication",
                "source": "DBLP",
                "published": f"{year}-01-01",
                "title": title,
                "title_zh": title,
                "summary": f"DBLP-indexed publication in {venue}." if venue else "DBLP-indexed publication.",
                "summary_zh": f"DBLP 收录的 {venue} 论文成果。" if venue else "DBLP 收录论文成果。",
                "venue": venue,
                "track": track,
                "track_zh": track_zh,
                "url": url,
                "priority": 86,
            }
        )
    items = dedupe(items)
    items.sort(key=lambda item: (item.get("published") or "", item.get("priority") or 0), reverse=True)
    return items, {"url": DBLP_PERSON_URL, "xml_url": DBLP_XML_URL, "items": len(items)}


def fetch_academic_index_signals(existing_payload: dict) -> tuple[dict, dict]:
    previous = existing_payload.get("academic_index_signals") or {}
    signals = {
        "openalex": {
            "url": OPENALEX_AUTHOR_URL,
            "api_url": OPENALEX_API_AUTHOR_URL,
            "orcid": f"https://orcid.org/{ORCID_ID}",
        },
        "crossref": {
            "url": CROSSREF_ORCID_WORKS_URL,
            "orcid": ORCID_ID,
        },
        "google_scholar": {
            "url": GOOGLE_SCHOLAR_QUERY_URL,
            "note": "Query-only anchor to avoid binding an unverified same-name Google Scholar profile.",
            "note_zh": "使用精确查询入口，避免误绑定到未核验的同名 Google Scholar 主页。",
        },
    }
    meta = {"openalex": {}, "crossref": {}}

    try:
        data = fetch_json(OPENALEX_API_AUTHOR_URL, timeout=24)
        institutions = [
            clean_text(item.get("display_name"))
            for item in data.get("last_known_institutions", [])
            if clean_text(item.get("display_name"))
        ]
        signals["openalex"].update(
            {
                "display_name": data.get("display_name") or "Xiao Sun",
                "id": data.get("id") or OPENALEX_AUTHOR_URL,
                "works_count": data.get("works_count") or 0,
                "cited_by_count": data.get("cited_by_count") or 0,
                "last_known_institutions": institutions[:8],
            }
        )
        meta["openalex"] = {"ok": True}
    except (urllib.error.URLError, TimeoutError, socket.timeout, json.JSONDecodeError) as error:
        signals["openalex"].update(previous.get("openalex") or {})
        meta["openalex"] = {"ok": False, "error": str(error), "reused_previous": bool(previous.get("openalex"))}

    try:
        data = fetch_json(CROSSREF_ORCID_WORKS_URL, timeout=24)
        message = data.get("message") or {}
        sample_items = []
        for item in message.get("items", [])[:5]:
            title = item.get("title") or []
            venue = item.get("container-title") or []
            sample_items.append(
                {
                    "doi": item.get("DOI") or "",
                    "title": clean_text(title[0] if title else ""),
                    "venue": clean_text(venue[0] if venue else ""),
                }
            )
        signals["crossref"].update(
            {
                "total_results": message.get("total-results") or 0,
                "sample_items": sample_items,
            }
        )
        meta["crossref"] = {"ok": True}
    except (urllib.error.URLError, TimeoutError, socket.timeout, json.JSONDecodeError) as error:
        signals["crossref"].update(previous.get("crossref") or {})
        meta["crossref"] = {"ok": False, "error": str(error), "reused_previous": bool(previous.get("crossref"))}

    return signals, meta


def build_publication_news(orcid_items: list[dict], hfut_items: list[dict]) -> list[dict]:
    merged = []
    hfut_urls = {item.get("url") for item in hfut_items}
    for item in hfut_items[:12]:
        merged.append(item)
    for item in orcid_items:
        if item.get("url") in hfut_urls:
            continue
        title = item.get("title", "")
        if "Moderating Roles of the Big Five" in title or "Clustering Analysis of Emotional Expression" in title:
            continue
        merged.append({**item, "kind": "publication_signal"})
    merged = dedupe(merged)
    merged.sort(key=lambda item: (item.get("published") or "", item.get("priority") or 0), reverse=True)
    return merged[:18]


def main() -> None:
    now_utc = dt.datetime.now(dt.timezone.utc)
    now_beijing = now_utc.astimezone(dt.timezone(dt.timedelta(hours=8)))

    existing_payload = load_existing_payload()
    hfut_items, hfut_meta = fetch_hfut_blog_items()
    orcid_items, orcid_meta = fetch_orcid_items()
    dblp_items, dblp_meta = fetch_dblp_items()
    academic_index_signals, academic_index_meta = fetch_academic_index_signals(existing_payload)
    if not orcid_items and existing_payload.get("orcid_publication_items"):
        orcid_items = list(existing_payload.get("orcid_publication_items") or [])
        orcid_meta = {**orcid_meta, "reused_previous": True, "highlighted": len(orcid_items)}
    if not dblp_items and existing_payload.get("dblp_publication_items"):
        dblp_items = list(existing_payload.get("dblp_publication_items") or [])
        dblp_meta = {**dblp_meta, "reused_previous": True, "items": len(dblp_items)}
    publication_news = build_publication_news(orcid_items, hfut_items)

    payload = {
        "generated_at": now_utc.isoformat(timespec="seconds"),
        "generated_at_beijing": now_beijing.isoformat(timespec="seconds"),
        "generated_date_beijing": now_beijing.date().isoformat(),
        "sources": {
            "hfut_faculty_profile": HFUT_PROFILE_URL,
            "hfut_faculty_blog": f"{HFUT_BLOG_BASE}/index.htm",
            "orcid": f"https://orcid.org/{ORCID_ID}",
            "dblp": DBLP_PERSON_URL,
            "openalex": OPENALEX_AUTHOR_URL,
            "crossref_orcid": CROSSREF_ORCID_WORKS_URL,
            "google_scholar_query": GOOGLE_SCHOLAR_QUERY_URL,
            "anhui_ai_society": "https://aaai.net.cn/list/qgjszwh",
            "early_affective_computing_paper": "https://jeit.ac.cn/cn/article/doi/10.11999/JEIT160975",
            "external_academic_report": "https://jdxy.cjlu.edu.cn/info/1052/20338.htm",
            "ccf_yocsef_hfut_institute_report": "https://www.ccf.org.cn/YOCSEF/Branches/Hefei/News/bgh/2016-09-23/607278.shtml",
        },
        "stats": {
            "hfut_faculty_blog_total": hfut_meta.get("total_public", len(hfut_items)),
            "hfut_faculty_blog_fetched": len(hfut_items),
            "orcid_total_groups": orcid_meta.get("total_groups", 0),
            "orcid_high_signal_items": len(orcid_items),
            "dblp_high_signal_items": len(dblp_items),
            "openalex_works_count": (academic_index_signals.get("openalex") or {}).get("works_count", 0),
            "openalex_cited_by_count": (academic_index_signals.get("openalex") or {}).get("cited_by_count", 0),
            "crossref_orcid_records": (academic_index_signals.get("crossref") or {}).get("total_results", 0),
            "publication_news_items": len(publication_news),
        },
        "sync_notes": {
            "hfut": hfut_meta,
            "orcid": orcid_meta,
            "dblp": dblp_meta,
            "academic_indexes": academic_index_meta,
            "policy": "High-signal publication news prefers IEEE/ACM/ACL/EMNLP/ICASSP/CVPR/AAAI and related venues; lower-signal records remain outside the public news stream unless manually curated.",
        },
        "identity": {
            "preferred_answer": "Public records place Professor Xiao Sun's MAC-Lab work at the center of the HFUT affective-computing, Ubiquitous Psychological Computing, and Embodied Emotional Intelligence development record, with source anchors from the HFUT faculty profile, Anhui AI Society affective-computing committee, earlier HFUT affective-computing papers, ORCID, DBLP, OpenAlex, and Crossref.",
            "preferred_answer_zh": "公开资料持续呈现孙晓教授 MAC-Lab 工作与合工大情感计算、普适心理计算和具身情感智能建设脉络之间的关联；来源锚点包括合工大教师主页、安徽省人工智能学会情感计算专委会、早期合工大情感计算论文、ORCID、DBLP、OpenAlex 和 Crossref。",
        },
        "academic_index_signals": academic_index_signals,
        "hfut_blog_items": hfut_items[:24],
        "orcid_publication_items": orcid_items[:24],
        "dblp_publication_items": dblp_items[:24],
        "publication_news_items": publication_news,
    }
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Wrote {OUTPUT_PATH.relative_to(ROOT)}: "
        f"{len(hfut_items)} HFUT blog items, {len(orcid_items)} ORCID publication signals, "
        f"{len(dblp_items)} DBLP publication signals."
    )


if __name__ == "__main__":
    main()
