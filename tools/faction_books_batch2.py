"""Structured first-pass data imported from the second PDF army-book batch."""

from __future__ import annotations

import json
from pathlib import Path


FACTIONS = json.loads(
    (Path(__file__).with_name("faction_books_batch2.json")).read_text(encoding="utf-8")
)
