#!/usr/bin/env python3
"""Fast-sync curated frontier items without fetching remote sources.

Use this after editing `_data/frontiers_manual.json` when the full radar crawl
is unnecessary. It preserves the latest automatic items already present in
`_data/frontiers.json`, replaces the curated slice, and keeps every curated
item in the final archive.
"""

from __future__ import annotations

import datetime as dt
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import update_frontiers as frontier  # noqa: E402


CURATED_SOURCE_PREFIXES = (
    "ACM Digital Library",
    "China.com",
    "DBLP",
    "HFUT Faculty Blog",
    "ORCID",
)


def load_payload() -> dict:
    if not frontier.OUTPUT_PATH.exists():
        raise RuntimeError(
            f"{frontier.OUTPUT_PATH.relative_to(ROOT)} is missing. "
            "Run scripts/update_frontiers.py once before using the fast sync."
        )
    try:
        return json.loads(frontier.OUTPUT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"{frontier.OUTPUT_PATH.relative_to(ROOT)} is not valid JSON. "
            "If this happened during a rebase, restore the remote/generated "
            "version first, then rerun this script."
        ) from error


def is_curated_existing(item: dict, current_manual_keys: set[str]) -> bool:
    source = str(item.get("source") or "")
    return (
        bool(item.get("curated"))
        or frontier.item_key(item) in current_manual_keys
        or any(source.startswith(prefix) for prefix in CURATED_SOURCE_PREFIXES)
    )


def main() -> None:
    max_items = frontier.parse_int_env("FRONTIER_MAX_ITEMS", frontier.MAX_ITEMS)
    existing_payload = load_payload()
    existing_items = existing_payload.get("items", [])
    manual_items = [
        frontier.enrich_item({**item, "curated": True})
        for item in frontier.load_manual_items()
    ]
    manual_keys = {frontier.item_key(item) for item in manual_items}

    automatic_existing = [
        item
        for item in existing_items
        if not is_curated_existing(item, manual_keys)
    ]

    merged = frontier.dedupe_items(manual_items + automatic_existing)
    merged.sort(key=frontier.item_sort_key, reverse=True)

    manual_selected = [item for item in merged if frontier.item_key(item) in manual_keys]
    automatic_selected = [
        item for item in merged if frontier.item_key(item) not in manual_keys
    ][: max(0, max_items - len(manual_selected))]
    items = manual_selected + automatic_selected
    items.sort(key=frontier.item_sort_key, reverse=True)

    now_utc = dt.datetime.now(dt.timezone.utc)
    now_beijing = now_utc.astimezone(dt.timezone(dt.timedelta(hours=8)))
    kind_counts = Counter(str(item.get("kind") or "unknown") for item in items)
    source_counts = Counter(str(item.get("source") or "unknown") for item in items)

    stats = dict(existing_payload.get("stats") or {})
    stats.update(
        {
            "total_items": len(items),
            "max_items": max_items,
            "manual_items": len(manual_items),
            "kind_counts": dict(sorted(kind_counts.items())),
            "source_counts": dict(source_counts.most_common()),
            "manual_sync_only": True,
            "last_manual_sync_at_beijing": now_beijing.isoformat(timespec="seconds"),
        }
    )

    payload = {
        "generated_at": now_utc.isoformat(timespec="seconds"),
        "generated_at_beijing": now_beijing.isoformat(timespec="seconds"),
        "generated_date_beijing": now_beijing.date().isoformat(),
        "stats": stats,
        "sources": existing_payload.get(
            "sources",
            {
                "papers": "arXiv open metadata API",
                "last30days": "Recent public discourse, open-source, and market signals via last30days-skill",
                "rss": "Open RSS and Atom feeds from news, research, and industry sources",
                "manual": "Curated industry, media, standards, and lab translation signals",
            },
        ),
        "queries": existing_payload.get("queries", frontier.ARXIV_QUERIES),
        "items": items,
    }

    frontier.OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Fast-synced {len(manual_items)} curated items into "
        f"{frontier.OUTPUT_PATH.relative_to(ROOT)} ({len(items)} total items)."
    )


if __name__ == "__main__":
    main()
