from __future__ import annotations

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import build_data  # noqa: E402
from tools.faction_books import FACTIONS  # noqa: E402
from tools.faction_books_batch2 import FACTIONS as BATCH_TWO_FACTIONS  # noqa: E402


class CatalogueContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        build_data.main()
        cls.catalogue = ET.parse(ROOT / "黑暗精灵.cat").getroot()

    def test_source_keys_are_unique(self) -> None:
        all_units = [*build_data.UNITS, *build_data.LEGENDARY_UNITS]
        keys = [unit["key"] for unit in all_units]
        self.assertEqual(len(keys), len(set(keys)))

    def test_pilot_faction_has_expected_scope(self) -> None:
        self.assertEqual(len(build_data.UNITS), 30)
        self.assertEqual(len(build_data.LEGENDARY_UNITS), 7)
        self.assertEqual(sum(map(len, build_data.COMMON_ITEMS.values())), 52)
        self.assertEqual(sum(map(len, build_data.DE_ITEMS.values())), 18)

    def test_all_top_level_units_are_generated(self) -> None:
        namespace = {"cat": build_data.CAT_NS}
        generated = self.catalogue.findall("./cat:selectionEntries/cat:selectionEntry", namespace)
        self.assertEqual(len(generated), len(build_data.UNITS) + len(build_data.LEGENDARY_UNITS))

    def test_force_percentage_constraints(self) -> None:
        namespace = {"cat": build_data.CAT_NS}
        values: dict[str, tuple[str, str]] = {}
        for link in self.catalogue.findall("./cat:forceEntries/cat:forceEntry/cat:categoryLinks/cat:categoryLink", namespace):
            constraint = link.find("./cat:constraints/cat:constraint", namespace)
            if constraint is not None and constraint.get("field") == build_data.POINTS:
                values[link.get("name", "")] = (constraint.get("type", ""), constraint.get("value", ""))
        self.assertEqual(values["人物"], ("max", "40"))
        self.assertEqual(values["核心"], ("min", "25"))
        self.assertEqual(values["劫掠者"], ("max", "20"))
        self.assertEqual(values["兽栏"], ("max", "30"))

    def test_key_conditional_rules_remain_present(self) -> None:
        by_key = {unit["key"]: unit for unit in build_data.UNITS}
        self.assertTrue(by_key["cold-one-knights"]["dread_title_core"])
        self.assertEqual(by_key["reaper-ballista"]["reduced_by"], "ravager-chariot")
        self.assertEqual(by_key["thunder-pack"]["shared_pool"], "beast-packs")
        self.assertEqual(by_key["ambush-pack"]["shared_pool"], "beast-packs")

    def test_expansion_source_keys_and_profiles_are_valid(self) -> None:
        seen: set[tuple[str, str]] = set()
        for faction in FACTIONS:
            faction_key = str(faction["key"])
            for record in [*faction["mounts"], *faction["units"]]:
                identity = (faction_key, str(record["key"]))
                self.assertNotIn(identity, seen)
                seen.add(identity)
                self.assertEqual(len(record["global"]), 7, identity)
                self.assertEqual(len(record["defence"]), 5, identity)
                self.assertTrue(record["offence"], identity)
                self.assertTrue(all(len(attack) == 7 for attack in record["offence"]), identity)
                self.assertGreaterEqual(int(record["cost"]), 0, identity)
                if record.get("min") is not None:
                    self.assertGreaterEqual(int(record["min"]), 1, identity)
                    self.assertGreaterEqual(int(record["max"]), int(record["min"]), identity)
                    self.assertGreaterEqual(int(record["extra_cost"]), 0, identity)

    def test_all_expansion_catalogues_are_generated(self) -> None:
        namespace = {"cat": build_data.CAT_NS}
        for faction in FACTIONS:
            path = ROOT / str(faction["filename"])
            self.assertTrue(path.exists(), path)
            root = ET.parse(path).getroot()
            self.assertEqual(root.get("name"), faction["name"])
            self.assertEqual(root.get("gameSystemId"), build_data.GAME_SYSTEM_ID)
            generated = root.findall("./cat:selectionEntries/cat:selectionEntry", namespace)
            self.assertEqual(len(generated), len(faction["units"]), faction["name"])
            self.assertEqual(
                {entry.get("name") for entry in generated},
                {record["name"] for record in faction["units"]},
                faction["name"],
            )

    def test_expansion_force_percentage_constraints(self) -> None:
        namespace = {"cat": build_data.CAT_NS}
        for faction in FACTIONS:
            root = ET.parse(ROOT / str(faction["filename"])).getroot()
            actual: dict[str, tuple[str, str]] = {}
            for link in root.findall("./cat:forceEntries/cat:forceEntry/cat:categoryLinks/cat:categoryLink", namespace):
                constraint = link.find("./cat:constraints/cat:constraint", namespace)
                if constraint is not None and constraint.get("field") == build_data.POINTS:
                    actual[link.get("name", "")] = (constraint.get("type", ""), constraint.get("value", ""))
            expected = {
                str(name): (str(constraint_type), str(value))
                for _key, name, constraint_type, value in faction["categories"]
                if constraint_type
            }
            self.assertEqual(actual, expected, faction["name"])

    def test_expansion_expected_scope(self) -> None:
        expected = {
            "巴托尼亚": (23, 5, 15),
            "木精灵": (23, 5, 30),
            "震旦天朝": (26, 4, 16),
            "混沌矮人": (29, 6, 4),
            "矮人群山王国": (25, 2, 36),
            "混沌勇士": (28, 16, 7),
        }
        for faction in FACTIONS:
            if faction["name"] not in expected:
                continue
            self.assertEqual(
                (len(faction["units"]), len(faction["mounts"]), sum(map(len, faction["items"].values()))),
                expected[faction["name"]],
            )

    def test_second_pdf_batch_has_catalogues_and_records(self) -> None:
        self.assertEqual(len(BATCH_TWO_FACTIONS), 18)
        self.assertGreaterEqual(sum(len(faction["units"]) for faction in BATCH_TWO_FACTIONS), 430)
        for faction in BATCH_TWO_FACTIONS:
            self.assertGreaterEqual(len(faction["units"]), 12, faction["name"])
            self.assertTrue(all(int(unit["cost"]) > 0 for unit in faction["units"]), faction["name"])
            self.assertTrue(
                all(
                    unit.get("min") is None or int(unit["max"]) >= int(unit["min"])
                    for unit in faction["units"]
                ),
                faction["name"],
            )
            self.assertTrue((ROOT / faction["filename"]).exists(), faction["filename"])

    def test_expansion_conditional_constraints_are_generated(self) -> None:
        namespace = {"cat": build_data.CAT_NS}

        warriors = ET.parse(ROOT / "混沌勇士.cat").getroot()
        emperor_dragon = next(
            entry
            for entry in warriors.findall("./cat:sharedSelectionEntries/cat:selectionEntry", namespace)
            if entry.get("name") == "混沌帝王龙"
        )
        self.assertTrue(
            any(
                constraint.get("type") == "max"
                and constraint.get("scope") == "roster"
                and constraint.get("value") == "1"
                for constraint in emperor_dragon.findall("./cat:constraints/cat:constraint", namespace)
            )
        )

        bretonnia = ET.parse(ROOT / "巴托尼亚.cat").getroot()
        paladin = next(
            entry
            for entry in bretonnia.findall("./cat:selectionEntries/cat:selectionEntry", namespace)
            if entry.get("name") == "圣骑士"
        )
        roles = {
            entry.get("name"): entry
            for entry in paladin.findall("./cat:selectionEntries/cat:selectionEntry", namespace)
        }
        self.assertIn("任命为将军", roles)
        self.assertIn("军旗手", roles)
        for role_name in ("任命为将军", "军旗手"):
            self.assertIsNotNone(roles[role_name].find("./cat:modifiers/cat:modifier/cat:conditions/cat:condition", namespace))

        dwarfs = ET.parse(ROOT / "矮人群山王国.cat").getroot()
        cart = next(
            entry
            for entry in dwarfs.findall("./cat:selectionEntries/cat:selectionEntry", namespace)
            if entry.get("name") == "矮人推车"
        )
        miner_cart = next(entry for entry in cart.iter() if entry.get("name") == "矿工推车（额外计入氏族雷霆）")
        self.assertTrue(
            any(
                modifier.get("type") == "add"
                and modifier.get("field") == "category"
                and modifier.get("value") == build_data.category_id("clan-thunder")
                and any(condition.get("childId") == miner_cart.get("id") for condition in modifier.iter())
                for modifier in cart.findall("./cat:modifiers/cat:modifier", namespace)
            )
        )


if __name__ == "__main__":
    unittest.main()
