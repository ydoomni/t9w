from __future__ import annotations

import argparse
import collections
import math
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_NAMESPACES = {
    ".gst": "http://www.battlescribe.net/schema/gameSystemSchema",
    ".cat": "http://www.battlescribe.net/schema/catalogueSchema",
}
RESERVED_FIELDS = {"selections", "category", "hidden", "name", "sortIndex", "collective", "defaultAmount"}
RESERVED_CHILD_IDS = {"any", "model", "unit", "upgrade", "force", "roster"}


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def namespace(tag: str) -> str:
    return tag[1:].split("}", 1)[0] if tag.startswith("{") else ""


@dataclass
class Document:
    path: Path
    root: ET.Element


class Validator:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.documents: list[Document] = []
        self.ids: dict[str, tuple[Path, str]] = {}
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, path: Path, message: str) -> None:
        self.errors.append(f"{path.name}: {message}")

    def warning(self, path: Path, message: str) -> None:
        self.warnings.append(f"{path.name}: {message}")

    def load(self) -> None:
        paths = sorted([*self.root.glob("*.gst"), *self.root.glob("*.cat")])
        if not paths:
            self.errors.append("No .gst or .cat files found in the repository root")
            return
        for path in paths:
            try:
                root = ET.parse(path).getroot()
            except ET.ParseError as exc:
                self.error(path, f"XML parse failure: {exc}")
                continue
            expected = EXPECTED_NAMESPACES[path.suffix]
            if namespace(root.tag) != expected:
                self.error(path, f"wrong XML namespace: {namespace(root.tag)!r}; expected {expected!r}")
            expected_root = "gameSystem" if path.suffix == ".gst" else "catalogue"
            if local(root.tag) != expected_root:
                self.error(path, f"root element is {local(root.tag)!r}; expected {expected_root!r}")
            self.documents.append(Document(path, root))

    def collect_ids(self) -> None:
        for document in self.documents:
            for node in document.root.iter():
                node_id = node.get("id")
                if not node_id:
                    continue
                if node_id in self.ids:
                    previous_path, previous_tag = self.ids[node_id]
                    self.error(document.path, f"duplicate ID {node_id!r} on <{local(node.tag)}>; first used by <{previous_tag}> in {previous_path.name}")
                else:
                    self.ids[node_id] = (document.path, local(node.tag))

    def check_game_system_links(self) -> None:
        systems = {document.root.get("id") for document in self.documents if local(document.root.tag) == "gameSystem"}
        catalogues = {document.root.get("id") for document in self.documents if local(document.root.tag) == "catalogue"}
        if len(systems) != 1:
            self.errors.append(f"Expected exactly one game system, found {len(systems)}")
        for document in self.documents:
            if local(document.root.tag) != "catalogue":
                continue
            game_system_id = document.root.get("gameSystemId")
            if game_system_id not in systems:
                self.error(document.path, f"gameSystemId {game_system_id!r} does not resolve to the repository game system")
            for node in document.root.iter():
                if local(node.tag) == "catalogueLink" and node.get("targetId") not in catalogues:
                    self.error(document.path, f"catalogueLink targetId {node.get('targetId')!r} does not resolve")

    def check_references(self) -> None:
        for document in self.documents:
            for node in document.root.iter():
                tag = local(node.tag)
                for attribute in ("targetId", "publicationId", "typeId"):
                    value = node.get(attribute)
                    if value and value not in self.ids:
                        self.error(document.path, f"<{tag}> {attribute}={value!r} does not resolve")
                child_id = node.get("childId")
                if child_id and child_id not in RESERVED_CHILD_IDS and child_id not in self.ids:
                    self.error(document.path, f"<{tag}> childId={child_id!r} does not resolve")
                field = node.get("field")
                if field:
                    if field.startswith("limit::"):
                        referenced = field.split("::", 1)[1]
                        if referenced not in self.ids:
                            self.error(document.path, f"<{tag}> field={field!r} uses an unknown cost type")
                    elif field not in RESERVED_FIELDS and field not in self.ids:
                        self.error(document.path, f"<{tag}> field={field!r} does not resolve to an ID or supported field")
                if tag == "modifier" and node.get("field") == "category" and node.get("type") in {"add", "remove", "set-primary"}:
                    value = node.get("value")
                    if value not in self.ids:
                        self.error(document.path, f"category modifier value={value!r} does not resolve")

    def check_numbers(self) -> None:
        for document in self.documents:
            for node in document.root.iter():
                tag = local(node.tag)
                if tag not in {"cost", "constraint", "repeat"}:
                    continue
                raw = node.get("value")
                if raw is None:
                    self.error(document.path, f"<{tag}> is missing value")
                    continue
                try:
                    value = float(raw)
                except ValueError:
                    self.error(document.path, f"<{tag}> value {raw!r} is not numeric")
                    continue
                if not math.isfinite(value):
                    self.error(document.path, f"<{tag}> value {raw!r} is not finite")
                if tag == "cost" and value < 0:
                    self.error(document.path, f"negative point cost {raw!r}")

    def check_constraint_conflicts(self) -> None:
        for document in self.documents:
            for parent in document.root.iter():
                constraints = [child for container in parent if local(container.tag) == "constraints" for child in container if local(child.tag) == "constraint"]
                grouped: dict[tuple[str | None, str | None], dict[str, list[float]]] = collections.defaultdict(lambda: collections.defaultdict(list))
                for constraint in constraints:
                    try:
                        value = float(constraint.get("value", "nan"))
                    except ValueError:
                        continue
                    grouped[(constraint.get("field"), constraint.get("scope"))][constraint.get("type", "")].append(value)
                for (field, scope), values in grouped.items():
                    if values.get("min") and values.get("max") and max(values["min"]) > min(values["max"]):
                        self.error(document.path, f"obvious constraint conflict on <{local(parent.tag)}> {parent.get('name', parent.get('id', ''))!r}: min {max(values['min'])} > max {min(values['max'])} for field={field!r}, scope={scope!r}")

    def run(self) -> int:
        self.load()
        self.collect_ids()
        self.check_game_system_links()
        self.check_references()
        self.check_numbers()
        self.check_constraint_conflicts()
        for warning in self.warnings:
            print(f"WARNING: {warning}")
        for error in self.errors:
            print(f"ERROR: {error}")
        if self.errors:
            print(f"Validation failed: {len(self.errors)} error(s), {len(self.warnings)} warning(s).")
            return 1
        print(f"Validation passed: {len(self.documents)} file(s), {len(self.ids)} unique ID(s), 0 errors.")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate BattleScribe/New Recruit .gst and .cat data files.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root to scan")
    args = parser.parse_args()
    return Validator(args.root.resolve()).run()


if __name__ == "__main__":
    sys.exit(main())
