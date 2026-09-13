#!/usr/bin/env python3
"""Build api/v1/equip.json from api/v1/equips.txt.

equips.txt is a tab-separated file with a header row:

    code    title    level    energyFlag    linkParentId

- code: unique identifier for the category/item. No numeric pattern is
  required (level1/level2 no longer need a trailing-zero code).
- title: display name.
- level: 1, 2, or 3. Level1 rows start a new top category, level2 rows
  attach to the most recent level1 row, level3 rows attach to the most
  recent level2 row.
- energyFlag: "1" or "2". Required for level1. Optional for level2/3 -
  if blank, it is inherited from the enclosing level2 row (or level1
  row for a level2 row without its own value).
- linkParentId: optional, comma-separated list of other codes this
  level2/level3 row should also be listed under, in addition to its
  primary parent. Level1 rows must leave this blank.

Blank lines (no code) are ignored and may be used as spacing/placeholders.

Usage:
    python3 scripts/build_equip.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TXT_PATH = ROOT / "api/v1/equips.txt"
JSON_PATH = ROOT / "api/v1/equip.json"

EXPECTED_HEADER = ["code", "title", "level", "energyFlag", "linkParentId"]


class BuildError(Exception):
    pass


def parse_link_parent_id(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def build(txt_path: Path) -> list[dict]:
    lines = txt_path.read_text(encoding="utf-8").splitlines()
    if not lines:
        raise BuildError("equips.txt is empty")

    header = lines[0].split("\t")
    if header != EXPECTED_HEADER:
        raise BuildError(
            f"unexpected header {header!r}, expected {EXPECTED_HEADER!r}"
        )

    nodes: list[dict] = []
    nodes_by_id: dict[str, dict] = {}
    current_level1: str | None = None
    current_level2: str | None = None

    for lineno, line in enumerate(lines[1:], start=2):
        fields = line.split("\t")
        fields += [""] * (len(EXPECTED_HEADER) - len(fields))
        code, title, level_str, energy_flag, link_parent_raw = fields[:5]

        if code.strip() == "":
            continue

        if code in nodes_by_id:
            raise BuildError(f"line {lineno}: duplicate code {code!r}")

        if level_str not in ("1", "2", "3"):
            raise BuildError(
                f"line {lineno}: code {code!r} has invalid level {level_str!r}"
            )
        level = int(level_str)

        link_parent_id = parse_link_parent_id(link_parent_raw)
        if level == 1 and link_parent_id:
            raise BuildError(
                f"line {lineno}: level1 code {code!r} must not have linkParentId"
            )

        if level == 1:
            if not energy_flag:
                raise BuildError(f"line {lineno}: level1 code {code!r} needs energyFlag")
            current_level1 = code
            current_level2 = None
            parent_id = None
            level1_id = code
            level2_id = None
        elif level == 2:
            if current_level1 is None:
                raise BuildError(
                    f"line {lineno}: level2 code {code!r} appears before any level1 row"
                )
            if not energy_flag:
                energy_flag = nodes_by_id[current_level1]["energyFlag"]
            current_level2 = code
            parent_id = current_level1
            level1_id = current_level1
            level2_id = code
        else:  # level == 3
            if current_level2 is None:
                raise BuildError(
                    f"line {lineno}: level3 code {code!r} appears before any level2 row"
                )
            if not energy_flag:
                energy_flag = nodes_by_id[current_level2]["energyFlag"]
            parent_id = current_level2
            level1_id = current_level1
            level2_id = current_level2

        node = {
            "id": code,
            "title": title,
            "level": level,
            "parentId": parent_id,
            "level1Id": level1_id,
            "level2Id": level2_id,
            "energyFlag": energy_flag,
            "linkParentId": link_parent_id,
        }
        nodes.append(node)
        nodes_by_id[code] = node

    for node in nodes:
        for linked_id in node["linkParentId"]:
            if linked_id not in nodes_by_id:
                raise BuildError(
                    f"code {node['id']!r} has linkParentId {linked_id!r} "
                    "which does not exist"
                )

    return nodes


def main() -> int:
    try:
        nodes = build(TXT_PATH)
    except BuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    JSON_PATH.write_text(
        json.dumps(nodes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {len(nodes)} nodes to {JSON_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
