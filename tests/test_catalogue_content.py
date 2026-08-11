from __future__ import annotations

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import build_data  # noqa: E402


class CatalogueContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        build_data.build_game_system()
        build_data.build_catalogue()
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


if __name__ == "__main__":
    unittest.main()
