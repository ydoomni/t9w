"""Generate the second faction-expansion source data from user-supplied PDFs.

This developer utility is intentionally not invoked by the normal catalogue
builder.  It turns the temporary pdfplumber text extraction into a compact,
version-controlled JSON source file that the regular builder can load without
requiring the PDFs to be present on another machine.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pdfplumber


ROOT = Path(__file__).resolve().parents[1]
PDF_TEXT = ROOT / "tmp" / "pdfs"
PDF_SOURCE = Path(r"D:\weixinjilu\xwechat_files\wxid_1gguf0iddhry22_f596\msg\file\2026-08")
OUTPUT = ROOT / "tools" / "faction_books_batch2.json"


SPECS = [
    ("northern-tribes", "北方混沌部落", "北方混沌部落.cat", "第九纪元：中古战锤_北方混沌部落 2026_β2.txt", "北方混沌部落种族规则 2026 beta2", "NT-2026β2", "2026-06-01", {"荒原猛兽": "wasteland-beasts"}),
    ("high-elves", "高等精灵", "高等精灵.cat", "第九纪元：中古战锤_高等精灵 2026_β2.txt", "高等精灵种族规则 2026 beta2", "HE-2026β2", "2026-06-01", {"女王之弓": "queen-bow"}),
    ("tomb-kings", "古墓王", "古墓王.cat", "第九纪元：中古战锤_古墓王 2026_β2.txt", "古墓王种族规则 2026 beta2", "TK-2026β2", "2026-05-01", {"古代城械": "ancient-engines", "构装生物": "constructs", "被埋葬者": "buried"}),
    ("daemons-chaos", "混沌恶魔", "混沌恶魔.cat", "第九纪元：中古战锤_混沌恶魔 2026_β2.txt", "混沌恶魔种族规则 2026 beta2", "DC-2026β2", "2026-06-21", {"圣赞使者": "daemonic-heralds"}),
    ("greenskins", "绿皮", "绿皮.cat", "第九纪元：中古战锤_绿皮 2026_β2.txt", "绿皮种族规则 2026 beta2", "GS-2026β2", "2026-06-01", {"天降大石头": "falling-rocks", "又大又狠": "bigger-and-meaner"}),
    ("legions-nagash", "纳迦什军团", "纳迦什军团.cat", "第九纪元：中古战锤_纳迦什军团 2026_α1.txt", "纳迦什军团种族规则 2026 alpha1", "LN-2026α1", "2026-06-01", {"尸山骨海": "corpse-mountain", "狂啸恶灵": "wailing-wraiths"}),
    ("southern-realms", "南方王国", "南方王国.cat", "第九纪元：中古战锤_南方王国 2026_β1.txt", "南方王国种族规则 2026 beta1", "SR-2026β1", "2026-06-01", {"军火库": "arsenal", "陆行堡垒": "land-fortresses"}),
    ("empire", "人类帝国", "人类帝国.cat", "第九纪元：中古战锤_人类帝国 2026_β3.txt", "人类帝国种族规则 2026 beta3", "EM-2026β3", "2026-06-21", {"帝国助力": "empire-support", "信仰，钢铁和火药": "faith-steel-gunpowder"}),
    ("ogre-kingdoms", "食人魔王国", "食人魔王国.cat", "第九纪元：中古战锤_食人魔王国 2026_β3.txt", "食人魔王国种族规则 2026 beta3", "OK-2026β3", "2026-06-30", {"火药桶": "powder-kegs", "驯化野兽": "tamed-beasts"}),
    ("skaven", "斯卡文鼠人", "斯卡文鼠人.cat", "第九纪元：中古战锤_斯卡文鼠人 2026_β2.txt", "斯卡文鼠人种族规则 2026 beta2", "SK-2026β2", "2026-06-01", {"禁忌工坊": "forbidden-workshop", "肉体实验室": "flesh-laboratory"}),
    ("vampire-counts", "吸血鬼伯爵", "吸血鬼伯爵.cat", "第九纪元：中古战锤_吸血鬼伯爵 2026_β1.txt", "吸血鬼伯爵种族规则 2026 beta1", "VC-2026β1", "2026-06-01", {"苦难者": "sufferers", "疾速亡者": "swift-dead"}),
    ("vampire-coast", "吸血鬼海岸", "吸血鬼海岸.cat", "第九纪元：中古战锤_吸血鬼海岸 2026_β2.txt", "吸血鬼海岸种族规则 2026 beta2", "VP-2026β2", "2026-06-01", {"深渊惧兽": "abyssal-dreadbeasts", "打捞军火": "salvage-arsenal"}),
    ("lizardmen", "蜥蜴人", "蜥蜴人.cat", "第九纪元：中古战锤_蜥蜴人 2026_β2.txt", "蜥蜴人种族规则 2026 beta2", "LZ-2026β2", "2026-06-01", {"游猎战士": "hunter-warriors", "雷霆蜥蜴": "thunder-lizards"}),
    ("beast-herds", "野兽人", "野兽人.cat", "第九纪元：中古战锤_野兽人 2026_β3.txt", "野兽人种族规则 2026 beta3", "BH-2026β3", "2026-06-21", {"荒野恐怖": "wilderness-horrors", "伏击捕食者": "ambush-predators"}),
    ("dogs-war", "战争之犬雇佣兵", "战争之犬雇佣兵.cat", "第九纪元：中古战锤_战争之犬雇佣兵 2026_α7.txt", "战争之犬雇佣兵种族规则 2026 alpha7", "DW-2026α7", "2026-06-01", {}),
    ("araby", "阿拉比", "阿拉比.cat", "第九纪元：中古战争_阿拉比_2026_β2.txt", "阿拉比种族规则 2026 beta2", "AR-2026β2", "2026-06-01", {"狂信徒": "fanatics", "神灯精灵": "lamp-djinn"}),
    ("kislev", "基斯里夫", "基斯里夫.cat", "第九纪元：中古战争_基斯里夫_2026_β2.txt", "基斯里夫种族规则 2026 beta2", "KS-2026β2", "2026-06-01", {"熊神信仰": "bear-faith", "霜原恐惧": "frost-terrors"}),
    ("ind", "印地", "印地.cat", "第九纪元：中古战争_印地_2026_β2.txt", "印地种族规则 2026 beta2", "IN-2026β2", "2026-06-01", {"千神使者": "thousand-gods"}),
]


COMPOSITION = {
    "northern-tribes": (6, [("characters", "人物", "max", 40), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("wasteland-beasts", "荒原猛兽", "max", 25)]),
    "high-elves": (6, [("characters", "人物", "max", 40), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("queen-bow", "女王之弓", "max", 30)]),
    "tomb-kings": (6, [("characters", "人物", "max", 40), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("ancient-engines", "古代城械", "max", 35), ("constructs", "构装生物", "max", 35), ("buried", "被埋葬者", "max", 30)]),
    "daemons-chaos": (7, [("characters", "人物", "max", 45), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("daemonic-heralds", "圣赞使者", "max", 35)]),
    "greenskins": (5, [("characters", "人物", "max", 40), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("falling-rocks", "天降大石头", "max", 15), ("bigger-and-meaner", "又大又狠", "max", 30)]),
    "legions-nagash": (6, [("characters", "人物", "max", 40), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("corpse-mountain", "尸山骨海", "max", 35), ("wailing-wraiths", "狂啸恶灵", "max", 20)]),
    "southern-realms": (8, [("characters", "人物", "max", 40), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("arsenal", "军火库", "max", 30), ("land-fortresses", "陆行堡垒", "max", 25)]),
    "empire": (6, [("characters", "人物", "max", 40), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("empire-support", "帝国助力", "max", 35), ("faith-steel-gunpowder", "信仰，钢铁和火药", "max", 30)]),
    "ogre-kingdoms": (6, [("characters", "人物", "max", 40), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("powder-kegs", "火药桶", "max", 35), ("tamed-beasts", "驯化野兽", "max", 30)]),
    "skaven": (6, [("characters", "人物", "max", 40), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("forbidden-workshop", "禁忌工坊", "max", 30), ("flesh-laboratory", "肉体实验室", "max", 20)]),
    "vampire-counts": (7, [("characters", "人物", "max", 40), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("sufferers", "苦难者", "max", 20), ("swift-dead", "疾速亡者", "max", 30)]),
    "vampire-coast": (7, [("characters", "人物", "max", 40), ("core", "核心", "min", 20), ("special", "特殊", None, None), ("abyssal-dreadbeasts", "深渊惧兽", "max", 25), ("salvage-arsenal", "打捞军火", "max", 40)]),
    "lizardmen": (5, [("characters", "人物", "max", 35), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("hunter-warriors", "游猎战士", "max", 30), ("thunder-lizards", "雷霆蜥蜴", "max", 35)]),
    "beast-herds": (7, [("characters", "人物", "max", 40), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("wilderness-horrors", "荒野恐怖", "max", 40), ("ambush-predators", "伏击捕食者", "max", 60)]),
    "dogs-war": (7, [("characters", "人物", "max", 40), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("arsenal", "军火库", "max", 25), ("land-fortresses", "陆行堡垒", "max", 20)]),
    "araby": (5, [("characters", "人物", "max", 40), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("fanatics", "狂信徒", "max", 35), ("lamp-djinn", "神灯精灵", "max", 25)]),
    "kislev": (6, [("characters", "人物", "max", 40), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("bear-faith", "熊神信仰", "max", 30), ("frost-terrors", "霜原恐惧", "max", 25)]),
    "ind": (4, [("characters", "人物", "max", 40), ("core", "核心", "min", 25), ("special", "特殊", None, None), ("thousand-gods", "千神使者", "max", 35)]),
}

PAGE = re.compile(r"\n===== PDF PAGE (\d+) =====\n")
HEIGHT = re.compile(r"(?:^|\n)高度[^\n]*")
NUMBER = re.compile(r"(?:\d+D\d*|\d+D|\d+|C)(?:[”\"])?")


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip(" ：:")


def stat_tokens(line: str, count: int) -> list[str]:
    values = NUMBER.findall(line)
    return [value.replace("”", "\"") for value in values[:count]]


def value_after(label: str, block: str, count: int) -> tuple[list[str], str]:
    match = re.search(label + r"[^\n]*\n([^\n]+)", block)
    if not match:
        return [], ""
    line = clean(match.group(1))
    values = stat_tokens(line, count)
    remainder = line
    for value in values:
        remainder = remainder.replace(value, "", 1)
    return values, clean(remainder)


def unit_name(block: str) -> str | None:
    lines = [clean(line) for line in block.splitlines() if clean(line)]
    for line in lines[:5]:
        match = re.match(r"(.+?)\s*分(?:\s|$)", line)
        if match:
            name = clean(match.group(1))
            if name and name not in {"分", "模型，可额外增加至多 模型"} and not re.match(r"^\d|^(如果|单位|模型)", name):
                return name
    ignored = ("高度", "核心", "特殊", "人物", "类型", "全局", "防御", "进攻", "选项", "底盘", "分")
    for line in lines[1:5]:
        if not line.startswith(ignored) and "模型" not in line and len(line) <= 24:
            return line
    return None


def unit_cost(block: str) -> int:
    for pattern in (
        r"\n\s*(\d{2,4})\s*:",
        r"\n\s*(\d{2,4})\s*\n",
        r"全\S*\s*(\d{2,4})\s*(?:\+|Adv|/)" ,
        r"\((\d{2,4})\s*分\)",
    ):
        match = re.search(pattern, block)
        if match:
            return int(match.group(1))
    return 0


def word_cost(words: list[dict[str, object]], name: str) -> int | None:
    """Return the price printed beside a unit name, using PDF coordinates.

    Text extraction interleaves columns on these army-book layouts, but the
    price and its `分` label remain close together in the rendered table.
    """
    targets = [
        word for word in words
        if name == str(word["text"]).strip() or (len(name) >= 3 and name in str(word["text"]))
    ]
    for target in sorted(targets, key=lambda word: float(word["top"])):
        top = float(target["top"])
        left = float(target["x0"])
        price_headers = [
            label for label in words
            if str(label["text"]).strip() == "分"
            and top - 8 <= float(label["top"]) <= top + 20
            and left <= float(label["x0"]) <= left + 140
        ]
        for header in price_headers:
            header_top = float(header["top"])
            header_left = float(header["x0"])
            values = [
                int(word["text"])
                for word in words
                if str(word["text"]).strip().isdigit()
                and 2 <= len(str(word["text"]).strip()) <= 4
                and header_top + 6 <= float(word["top"]) <= header_top + 55
                and header_left - 55 <= float(word["x0"]) <= header_left + 55
            ]
            if values:
                return values[0]
        candidates: list[tuple[float, float, int]] = []
        for word in words:
            token = str(word["text"]).strip("()：:")
            if not token.isdigit() or not 2 <= len(token) <= 4:
                continue
            word_top = float(word["top"])
            word_left = float(word["x0"])
            if not top - 12 <= word_top <= top + 150 or not left - 25 <= word_left <= left + 420:
                continue
            if any(
                str(label["text"]).strip() == "分"
                and abs(float(label["top"]) - word_top) <= 4
                and 0 <= float(label["x0"]) - float(word["x1"]) <= 48
                for label in words
            ):
                candidates.append((word_top, word_left, int(token)))
        if candidates:
            return sorted(candidates)[0][2]
    return None


def unit_size(block: str, cost: int) -> dict[str, int]:
    match = re.search(r"(\d+)\s*模型，可额外增加至多\s*(\d+)\s*模型", block)
    if not match:
        return {}
    minimum = int(match.group(1))
    maximum = int(match.group(2))
    if maximum < minimum:
        return {}
    after = block[match.end(): match.end() + 100]
    per_model = re.search(r"(\d{1,3})\s*/", after)
    if not per_model:
        return {}
    extra_cost = int(per_model.group(1))
    return {"min": minimum, "max": maximum, "extra_cost": extra_cost}


def unit_limit(block: str) -> dict[str, object]:
    if "全军唯一" in block or "传奇人物" in block:
        return {"unique": True}
    match = re.search(r"0-(\d+)\s*(?:单位|模型)?\s*/\s*军队", block)
    if match:
        return {"limit": int(match.group(1))}
    return {}


def parse_height(block: str) -> str:
    first = block.splitlines()[0] if block.splitlines() else ""
    for value in ("小型", "标准", "大型", "巨型"):
        if value in first:
            return value
    return "标准"


def parse_type(block: str) -> str:
    match = re.search(r"类型\s*([^\n\s]+)", block)
    return match.group(1) if match else "步兵"


def parse_chassis(block: str) -> str:
    match = re.search(r"(\d+\s*[x×]\s*\d+\s*mm|\d+\s*mm圆|\d+\s*mm)", block)
    if not match:
        return "-"
    return re.sub(r"\s+", "", match.group(1)).replace("×", "x")


def parse_unit(key: str, page: int, category: str, block: str, words: list[dict[str, object]]) -> dict[str, object] | None:
    name = unit_name(block)
    if not name:
        return None
    if any(marker in name for marker in ("类型", "底盘", "( ", " : ")):
        return None
    global_values, global_rules = value_after("全局", block, 3)
    defence_values, defence_rules = value_after("防御", block, 5)
    offence_values, offence_rules = value_after("进攻", block, 5)
    height = parse_height(block)
    unit_type = parse_type(block)
    global_profile = tuple((global_values + ["-", "-", "-"])[:3] + [height, unit_type, parse_chassis(block), global_rules or "-"])
    defence = tuple((defence_values + ["-", "-", "-", "-", "-"])[:5])
    if defence_rules and defence[-1] == "-":
        defence = (*defence[:4], defence_rules)
    offence = [(name, *(offence_values + ["-", "-", "-", "-", "-"])[:5], offence_rules or "-")]
    record: dict[str, object] = {
        "key": key,
        "name": name,
        "page": page,
        "category": category,
        "cost": word_cost(words, name) or unit_cost(block),
        "global": global_profile,
        "defence": defence,
        "offence": offence,
        "details": [("来源", f"用户提供军书第{page}页；复杂装备与条件规则见 IMPLEMENTATION_NOTES.md。")],
    }
    record.update(unit_size(block, int(record["cost"])))
    record.update(unit_limit(block))
    if "魔法学徒" in global_rules or "魔法大师" in global_rules or "秘会法师" in global_rules:
        record["wizard"] = True
    return record


def category_for(context: str, current: str, custom: dict[str, str]) -> str:
    """Return the most recent army-list section heading before a unit.

    The first army-list page contains the complete force-organisation summary
    followed by the first "人物 至多 40%" heading.  Looking for any category
    word in a full page therefore assigns the first character to the final
    category in the summary.  Restrict matches to actual heading lines and use
    the final heading preceding the current unit instead.
    """
    matches: list[tuple[int, str]] = []
    patterns = [
        ("characters", r"(?:^|\n)人物\s*(?:\(|（)?\s*至多"),
        ("core", r"(?:^|\n)核心\s*(?:\(|（)?\s*至少"),
        ("special", r"(?:^|\n)特殊\s*(?:\(|（)?\s*无限制"),
    ]
    patterns.extend(
        (key, rf"(?:^|\n){re.escape(label)}[*＊]?\s*(?:\(|（)?\s*至多")
        for label, key in custom.items()
    )
    for key, pattern in patterns:
        for match in re.finditer(pattern, context):
            matches.append((match.start(), key))
    return max(matches)[1] if matches else current


def parse_book(spec: tuple[object, ...]) -> dict[str, object]:
    key, name, filename, text_file, publication, short_name, publication_date, custom = spec
    content = (PDF_TEXT / str(text_file)).read_text(encoding="utf-8")
    source_pdf = PDF_SOURCE / Path(str(text_file)).with_suffix(".pdf").name
    with pdfplumber.open(source_pdf) as pdf:
        page_words = [page.extract_words(x_tolerance=1, y_tolerance=3) for page in pdf.pages]
    chunks = PAGE.split(content)
    category = "characters"
    units: list[dict[str, object]] = []
    unresolved: list[dict[str, object]] = []
    seen: set[str] = set()
    for index in range(1, len(chunks), 2):
        page = int(chunks[index])
        page_text = chunks[index + 1]
        starts = list(HEIGHT.finditer(page_text))
        for position, match in enumerate(starts):
            end = starts[position + 1].start() if position + 1 < len(starts) else len(page_text)
            start = match.start()
            prefix = page_text[max(0, start - 90):start]
            previous_name = re.search(r"(?:^|\n)([^\n]{1,50}?)\s*分\s*\n\s*$", prefix)
            if previous_name:
                start -= len(previous_name.group(0)) - (1 if previous_name.group(0).startswith("\n") else 0)
            unit_category = category_for(page_text[:start], category, dict(custom))
            if unit_category != category:
                category = unit_category
            block = page_text[start:end]
            candidate = unit_name(block)
            if not candidate:
                continue
            suffix = hashlib.sha1(candidate.encode("utf-8")).hexdigest()[:10]
            if suffix in seen:
                continue
            seen.add(suffix)
            record = parse_unit(f"u-{suffix}", page, unit_category, block, page_words[page - 1])
            if record is not None:
                if int(record["cost"]) <= 0:
                    unresolved.append(
                        {
                            "name": record["name"],
                            "page": record["page"],
                            "reason": "自动提取未能可靠确定成本；保留为待人工核对项，未导出为可选单位。",
                        }
                    )
                else:
                    units.append(record)
    force_page, categories = COMPOSITION[str(key)]
    return {
        "key": key,
        "name": name,
        "filename": filename,
        "publication": publication,
        "short_name": short_name,
        "publication_date": publication_date,
        "force_page": force_page,
        "categories": categories,
        "rules": [],
        "items": {},
        "mounts": [],
        "units": units,
        "unresolved": unresolved,
    }


def main() -> None:
    books = [parse_book(spec) for spec in SPECS]
    OUTPUT.write_text(json.dumps(books, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {OUTPUT.name}: {sum(len(book['units']) for book in books)} units across {len(books)} factions")


if __name__ == "__main__":
    main()
