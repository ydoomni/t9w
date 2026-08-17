from __future__ import annotations

import hashlib
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    from tools.faction_books import FACTIONS
except ModuleNotFoundError:  # Support direct execution: python tools/build_data.py
    from faction_books import FACTIONS


ROOT = Path(__file__).resolve().parents[1]
GST_NS = "http://www.battlescribe.net/schema/gameSystemSchema"
CAT_NS = "http://www.battlescribe.net/schema/catalogueSchema"
POINTS = "5d8a-7c3f-2026-0001"
GAME_SYSTEM_ID = "9e00-2026-0000-0001"


def stable_id(key: str) -> str:
    """Return a stable BattleScribe ID from a permanent, non-display key."""
    raw = hashlib.sha256(f"t9w-custom:{key}".encode("utf-8")).hexdigest()[:16]
    return "-".join(raw[index : index + 4] for index in range(0, 16, 4))


def q(namespace: str, tag: str) -> str:
    return f"{{{namespace}}}{tag}"


def sub(parent: ET.Element, namespace: str, tag: str, **attrs: object) -> ET.Element:
    clean = {name: str(value).lower() if isinstance(value, bool) else str(value) for name, value in attrs.items()}
    return ET.SubElement(parent, q(namespace, tag), clean)


def add_constraint(
    parent: ET.Element,
    namespace: str,
    key: str,
    constraint_type: str,
    value: int | float,
    *,
    field: str = "selections",
    scope: str = "parent",
    percent: bool = False,
    include_children: bool = False,
    include_forces: bool = False,
) -> str:
    container = next((child for child in parent if child.tag == q(namespace, "constraints")), None)
    if container is None:
        container = sub(parent, namespace, "constraints")
    constraint_id = stable_id(f"constraint:{key}")
    sub(
        container,
        namespace,
        "constraint",
        id=constraint_id,
        type=constraint_type,
        value=value,
        field=field,
        scope=scope,
        shared=True,
        percentValue=percent,
        includeChildSelections=include_children,
        includeChildForces=include_forces,
    )
    return constraint_id


def add_cost(parent: ET.Element, namespace: str, value: int | float) -> None:
    costs = sub(parent, namespace, "costs")
    sub(costs, namespace, "cost", name="分", typeId=POINTS, value=value)


PROFILE_TYPES = {
    "global": ("全局", ["Adv", "Mar", "Dis", "高度", "类型", "底盘", "模型规则"]),
    "defence": ("防御", ["HP", "Def", "Res", "Arm", "装备与规则"]),
    "offence": ("进攻", ["Att", "Off", "Str", "AP", "Agi", "武器与规则"]),
    "weapon": ("武器", ["射程", "射数", "力量", "AP", "瞄准", "规则"]),
    "spell": ("法术", ["施法值", "射程", "类型", "持续时间", "效果摘要"]),
}


def profile_type_id(kind: str) -> str:
    return stable_id(f"profile-type:{kind}")


def characteristic_id(kind: str, name: str) -> str:
    return stable_id(f"characteristic:{kind}:{name}")


def add_profile(
    parent: ET.Element,
    namespace: str,
    key: str,
    kind: str,
    name: str,
    values: dict[str, object],
) -> None:
    profiles = next((child for child in parent if child.tag == q(namespace, "profiles")), None)
    if profiles is None:
        profiles = sub(parent, namespace, "profiles")
    type_name, characteristics = PROFILE_TYPES[kind]
    profile = sub(
        profiles,
        namespace,
        "profile",
        id=stable_id(f"profile:{key}"),
        name=name,
        hidden=False,
        typeId=profile_type_id(kind),
        typeName=type_name,
    )
    rows = sub(profile, namespace, "characteristics")
    for characteristic in characteristics:
        node = sub(
            rows,
            namespace,
            "characteristic",
            name=characteristic,
            typeId=characteristic_id(kind, characteristic),
        )
        node.text = str(values.get(characteristic, "-"))


def add_embedded_rule(
    parent: ET.Element,
    namespace: str,
    key: str,
    name: str,
    description: str,
) -> None:
    rules = next((child for child in parent if child.tag == q(namespace, "rules")), None)
    if rules is None:
        rules = sub(parent, namespace, "rules")
    rule = sub(rules, namespace, "rule", id=stable_id(f"rule:{key}"), name=name, hidden=False)
    sub(rule, namespace, "description").text = description


def add_info_link(
    parent: ET.Element,
    namespace: str,
    key: str,
    name: str,
    target_id: str,
    link_type: str = "rule",
) -> None:
    links = next((child for child in parent if child.tag == q(namespace, "infoLinks")), None)
    if links is None:
        links = sub(parent, namespace, "infoLinks")
    sub(
        links,
        namespace,
        "infoLink",
        id=stable_id(f"info-link:{key}"),
        name=name,
        hidden=False,
        targetId=target_id,
        type=link_type,
    )


def add_category_link(
    parent: ET.Element,
    namespace: str,
    key: str,
    name: str,
    target_id: str,
    *,
    primary: bool = False,
) -> ET.Element:
    links = next((child for child in parent if child.tag == q(namespace, "categoryLinks")), None)
    if links is None:
        links = sub(parent, namespace, "categoryLinks")
    return sub(
        links,
        namespace,
        "categoryLink",
        id=stable_id(f"category-link:{key}"),
        name=name,
        hidden=False,
        targetId=target_id,
        primary=primary,
    )


CATEGORIES = {
    "characters": "人物",
    "core": "核心",
    "special": "特殊",
    "raiders": "劫掠者",
    "menagerie": "兽栏",
    "legendary": "传奇人物",
    "general": "将军",
    "bsb": "军旗手",
    "non_character": "非人物单位",
    "wizard": "法师",
    "goddess": "祈求女神",
    "hidden-arrows": "暗箭难防",
    "true-dragon": "真龙血裔",
    "celestial-craft": "天工开物",
    "engines-destruction": "毁灭装置",
    "clan-thunder": "氏族雷霆",
    "war-engines": "战争引擎",
}


def category_id(key: str) -> str:
    return stable_id(f"category:{key}")


CORE_RULES = [
    ("army-points", "军队分值", "军队总分不得超过约定上限；总规则第 9.A 节同时要求不得低于上限超过 10 分。"),
    ("army-composition", "军队组成", "军表必须包含人物和核心；人物通常至多 40%，核心通常至少 25%，阵营特有分类按种族规则。"),
    ("unit-minimum", "最小军队规模", "除人物外，军队至少包含 4 个单位；战争机器按总规则处理。"),
    ("scale-limits", "战团、野战军与军团", "1500-2999 分为战团，3000-7999 分为野战军，8000 分及以上为军团。0-X 上限在战团减半并向上取整，在军团翻倍；全军唯一不变。"),
    ("special-items", "特殊物品", "除非另有说明，特殊物品全军唯一；每个模型最多一个武器附魔、每件护甲最多一个护甲附魔、一般每面旗帜一个附魔、最多两件魔法奇物和一件至尊物品。"),
]


EQUIPMENT = {
    "hand-weapon": ("单手武器", "近战", "-", "使用者", "使用者", "-", "步行模型与盾牌同用时获得格挡。"),
    "great-weapon": ("大型武器", "近战", "-", "+2", "+2", "-", "双手持用；主动性顺序 0 攻击。"),
    "halberd": ("戟", "近战", "-", "+1", "+1", "-", "双手持用。"),
    "lance": ("骑枪", "近战", "-", "+2", "+2", "-", "正面目标时毁灭冲锋（+2 力量、+2 AP、+1 敏捷）；步兵不可用。"),
    "light-lance": ("轻骑枪", "近战", "-", "+1", "+1", "-", "正面目标时毁灭冲锋（+1 力量、+1 AP）；步兵不可用。"),
    "paired-weapons": ("成对武器", "近战", "-", "使用者", "使用者", "-", "双手持用；+1 攻击次数与+1 进攻技巧；无视格挡。"),
    "spear": ("长矛", "近战", "-", "使用者", "+1", "-", "额外排面攻击；符合条件时首轮再+2 敏捷与+1 AP；仅步兵。"),
    "light-armour": ("轻甲", "-", "-", "-", "-", "-", "+1 护甲。"),
    "heavy-armour": ("重甲", "-", "-", "-", "-", "-", "+2 护甲。"),
    "plate-armour": ("板甲", "-", "-", "-", "-", "-", "+3 护甲。"),
    "shield": ("盾牌", "-", "-", "-", "-", "-", "+1 护甲；双手武器对抗近战时不能同时使用。"),
}


LORES = [
    "火焰系", "野兽系", "光明系", "金属系", "生命系", "天堂系", "阴影系", "死亡系",
    "高等系", "黑暗系", "吸血鬼系", "大Waaagh!!!", "小Waaaagh!!!", "斯卡文毁灭法术",
    "斯卡文瘟疫法术", "奸奇系", "纳垢系", "色孽系", "天劫法术",
]


COMMON_ITEMS = {
    "weapon": [
        ("khaine-sword", "凯恩神剑", 200, 1, "至尊；精灵限定。攻击属性设为 10，并具有强力的特殊伤害与反噬规则。"),
        ("elemental-binding", "元素束缚", 60, 1, "对该武器攻击成功的护甲保护与特殊保护必须重投。"),
        ("dragon-slayer", "屠龙刃", 55, 1, "对伟岸获得多重伤害(D3)与闪电反应。"),
        ("hero-heart", "勇士之心", 50, 1, "+1 攻击次数，力量至少 5，AP 至少 2。"),
        ("sky-staff", "天杖", 45, 1, "骑枪附魔；毁灭冲锋效果改为首轮攻击。"),
        ("executioner", "行刑者", 35, 1, "+6 AP，造伤不优于 3+。"),
        ("killing-essence", "杀戮精华", 25, 1, "一次性；一轮近战中+2 Off、+2 Str、+2 AP。"),
        ("hero-bane", "英雄克星", 20, 1, "分配给人物或队长的命中+1 力量与+1 AP。"),
        ("swift-agility", "神速敏捷", 20, 1, "+2 进攻技巧与+2 敏捷。"),
        ("sharp-sting", "锋锐针刺", 10, 1, "+1 AP。"),
        ("titan-bowstring", "天空泰坦弓弦", 30, 1, "弓类射击+6 英寸射程、多重命中(D3+1)、装弹。"),
    ],
    "armour": [
        ("cheat-death", "死亡欺诈", 90, 1, "伟岸不可选；重生(4+)并+1 护甲。"),
        ("call-destiny", "命运召唤", 70, 1, "大型构装体或伟岸不可选；魔盾(4+)，护甲设为 3。"),
        ("dazzling-barrier", "炫目壁障", 60, 1, "伟岸不可选；对手重投对穿戴者成功的普通攻击命中。"),
        ("mithril", "秘银精华", 50, 1, "大型构装体或伟岸不可选；护甲设为 5。"),
        ("basalt", "玄武灌注", 40, 1, "+1 护甲，魔盾(3+ 对火焰)，重生自动失败。"),
        ("integrated", "一体防护", 40, 1, "标准模型限定；获得附属与抵抗(近战攻击)。"),
        ("ghost-guard", "幽灵守卫", 30, 1, "重甲或板甲限定；对非魔法攻击+2 护甲。"),
        ("smelted-alloy", "冶炼合金", 15, 1, "+1 护甲，-2 进攻技巧。"),
        ("dawn-dusk", "晨昏铸造", 55, 1, "盾牌附魔；可重投护甲保护，但该伤害的特殊保护失败。"),
        ("arcane-ring", "奥法之环", 45, 1, "盾牌附魔；对魔法攻击提升魔盾，至多 3+。"),
        ("wicker", "藤条守护", 15, 1, "步行限定；不能格挡，额外+1 护甲。"),
    ],
    "banner": [
        ("speed-banner", "急速战棋", 50, 3, "+1 移动、+2 行军。"),
        ("razor-banner", "剃刀战旗", 50, 3, "一次性；近战中普通模型普通攻击+1 AP。"),
        ("fury-banner", "暴怒战旗", 40, 3, "一次性；步兵行军速度设为 15 英寸并受相应限制。"),
        ("distortion", "失真徽记", 40, 2, "一次性；单位获得难以瞄准(2)一回合。"),
        ("ranger-banner", "游侠战旗", 35, 3, "单位获得行者。"),
        ("protection-banner", "保护旗", 30, 2, "轻甲限定；AP≤2 的攻击不能令护甲差于 6+。"),
        ("eternal-flame", "永恒烈焰战旗", 25, 3, "一次性；单位获得火焰攻击。"),
        ("discipline-banner", "纪律战旗", 25, 3, "重投恐慌；有将军或军旗手时自动通过。"),
        ("beast-hunter", "猎兽者织锦", 20, 2, "单位获得不能被践踏。"),
        ("witch-bone", "巫骨之旗", 10, 3, "获得或提升魔法抗性。"),
    ],
    "curio": [
        ("seal-scroll", "封印卷轴", 65, 2, "一次性；令指定敌方法术在该魔法阶段不能施放。"),
        ("power-scroll", "能量卷轴", 40, 1, "一次性；为一次施法或破法结果加入一颗法术骰。"),
        ("healing-potion", "治疗药剂", 40, 1, "伟岸不可选；一次性恢复 1 HP。"),
        ("haste-potion", "急速药剂", 20, 1, "一次性；一回合+3 敏捷。"),
        ("strength-potion", "力量药剂", 10, 1, "伟岸不可选；一次性获得粉碎攻击。"),
        ("lucky-coin", "幸运币", 10, 1, "一次性；重投一次失败护甲保护。"),
        ("oak-book", "奥木力量之书", 50, 1, "至尊；魔法学徒/专家限定，调整已学法术选择。"),
        ("gambler-staff", "赌徒法杖", 50, 1, "至尊；法师限定，随机法术选择。"),
        ("forbidden-staff", "禁断法杖", 50, 1, "至尊；法师限定，允许选择两个种族法术。"),
        ("defence-amulet", "防身护符", 50, 1, "获得魔盾(5+)。"),
        ("power-stone", "能量石", 50, 1, "获得传导(1)。"),
        ("crystal-ball", "水晶球", 45, 1, "至尊；敌方魔法阶段首次破法获得+2。"),
        ("wizard-hat", "巫师帽", 40, 1, "非法师限定；随机八风派系并成为魔法学徒。"),
        ("dragon-staff", "龙之法杖", 40, 1, "获得力量4、AP1、火焰吐息。"),
        ("mystic-servant", "神秘仆从", 35, 1, "法师限定；可记录两个派系，不能选择 5、6 号法术。"),
        ("war-wand", "战争短杖", 35, 1, "获得法力强度(4/8)的增益充能法术。"),
        ("despot-crown", "独裁皇冠", 30, 1, "不当头儿不可选；提升或获得鼓舞人心。"),
        ("ruby-ring", "毁灭的红宝石之戒", 30, 1, "获得火球术充能法术，法力强度(4/8)。"),
        ("ranger-boots", "游侠之靴", 30, 1, "步行标准步兵限定；获得行者并提升非飞行移动。"),
        ("obsidian", "黑曜石护符", 20, 1, "获得魔法抗性(2)。"),
    ],
}


DE_RULES = {
    "military-training": ("军事训练", "满足步兵与友军距离条件时，首次冲锋获得移动加成，并在坚定与打乱排面时视为多一个完整排面。"),
    "coastal-predator": ("海岸猎食者", "获得行者(水域)；在水域内满足多数模型条件时获得难以瞄准与冲锋移动加成。"),
    "scent-of-blood": ("血之芬芳", "接战时获得狂暴与无畏；对已损失生命值的目标冲锋时获得移动加成。"),
    "hekatis-blessing": ("赫卡提之佑", "法师施放黑暗系法术的施法值-1。"),
    "eternal-hatred": ("永恒仇恨", "对高等精灵获得首轮攻击(憎恨)；已有该规则时改为憎恨。"),
    "killing-prowess": ("杀戮造诣", "普通攻击获得首轮攻击(+1 造伤)。"),
    "killing-mastery": ("杀戮专精", "普通攻击获得+1 造伤。"),
    "venom-breath": ("毒性吐息", "力量4、AP0 的吐息；造成未保护伤害后令目标 Off 与 Def -1 一回合。"),
    "dark-blades": ("黑暗双刃", "成对魔法武器；满足友方法术条件时攻击力量设为5；不能附魔。"),
    "repeater-crossbow": ("连弩", "射程18英寸、射数2、力量3、AP0；近距射击+1 AP。"),
    "repeater-handbow": ("连发手弩[X]", "射程12英寸、射数X、力量3、AP0、快速射击、精准；近距射击+1 AP。"),
    "darksteel": ("陨钢黑甲", "视为板甲并可附魔；穿戴者获得无畏。"),
    "sea-cloak": ("海龙披风", "+1 护甲并获得海岸猎食者。"),
}


DE_ITEMS = {
    "weapon": [
        ("crippling-frost", "致残寒霜", 35, 1, "大型武器附魔；接触敌军-2 Def。"),
        ("transcendence", "超绝", 50, 1, "骑枪附魔；造成伤害后永久提升力量与 AP，至多各+2。"),
        ("rending-touch", "撕裂之触", 65, 1, "成对武器附魔；+2 Att、+2 AP，并获得恐惧。"),
        ("slaughter-master", "屠杀大师", 40, 1, "长矛附魔；获得杀戮专精、战斗专注、致命一击与多重伤害(2)。"),
        ("crimson-death", "深红死亡", 30, 1, "戟附魔；+2 Att 并获得神圣攻击。"),
    ],
    "armour": [
        ("blood-armour", "血浴护甲", 45, 1, "步行限定；造成普通攻击伤害后永久+1 护甲。"),
        ("ghrond-shield", "戈隆德之盾", 35, 1, "盾牌附魔；接触敌人的近战命中力量-1，最低1。"),
    ],
    "banner": [
        ("naggarond-banner", "纳伽隆德之旗", 80, 1, "单位获得孤傲与永不战败。"),
        ("assault-banner", "突击旗", 85, 1, "单位内步兵获得血之芬芳与快速移动。"),
        ("executioner-mark", "刽子手印记", 65, 1, "具有杀戮造诣的模型获得杀戮专精。"),
        ("medusa-eye", "美杜莎之眼", 50, 1, "核心不可选；持有者获得石化凝视，接触敌军重投成功领导力测试。"),
    ],
    "curio": [
        ("twilight-cloak", "暮光披风", 40, 1, "对近战魔盾(5+)；受近战攻击时在主动性0造成反击命中。"),
        ("death-mask", "死亡面具", 60, 1, "单位获得恐惧，并强化附近友军对恐惧目标的造伤。"),
        ("black-tower-ring", "黑塔之戒", 40, 1, "高阶女术士不可选；附近友军战败与恐慌测试取小。"),
        ("ninth-fleet-seal", "第九舰队印鉴", 45, 1, "黑色方舟舰队司令限定；纯步兵单位获得军事训练。"),
        ("guiding-eye", "引导之眼", 60, 1, "法师限定；获得奥卡姆意志剃刀充能法术。"),
        ("beast-whistle", "驯兽师口哨", 25, 1, "高阶驯兽师限定；一次性提升附近指定野兽冲锋距离骰。"),
        ("black-dragon-egg", "黑龙卵", 25, 1, "获得毒性吐息。"),
    ],
}


DE_TITLES = [
    ("dread-lord", "恐惧之主", 80, 1, "全军唯一；获得冷蜥坐骑，并可令0-1冷蜥骑士计入核心。"),
    ("life-ender", "熄命者", 60, 99, "单位内黑暗双刃+1 AP。"),
    ("shadow-dart", "影镖", 40, 99, "单位内连发手弩或连弩最大射程+6英寸。"),
    ("beast-binder", "缚兽者", 50, 99, "单位获得无畏与憎恨(野兽)。"),
    ("dark-road", "暗路", 40, 99, "单位获得行者与+2英寸行军速度。"),
    ("poison-blade", "毒刃", 30, 99, "单位获得毒性攻击。"),
    ("thorn-whip", "棘鞭", 30, 99, "可加入核心掳掠奴隶，并改变相应规则。"),
    ("fate-shield", "天命盾", 70, 99, "魔盾提升，至多4+。"),
    ("hydra-blood", "多头蛇之血", 55, 99, "伟岸不可选；获得重生(5+)与愤怒。"),
    ("spine-storm", "刺岚", 40, 99, "6英寸内友军射击武器射程+1英寸。"),
    ("dragon-scale", "龙鳞", 35, 99, "+1护甲与魔法抗性(2)。"),
    ("blood-bane", "血祸", 25, 99, "+1攻击次数；单位获得血之芬芳。"),
    ("soul-flame", "魂焰", 25, 99, "攻击获得火焰与魔法；对火焰获得魔盾(3+)。"),
    ("leviathan-wrath", "利维坦之怒", 20, 99, "+2 Off、Def 与 Agi。"),
]


MOUNTS = {
    "dark-steed": {
        "name": "黑暗骏马", "global": ("9\"", "18\"", "C", "标准", "骑兵", "25x50mm", "-"),
        "defence": ("C", "C", "C", "C+1", "-"), "offence": [("黑暗骏马", "1", "3", "3", "0", "4", "驾驭")],
    },
    "cold-one": {
        "name": "冷蜥", "global": ("7\"", "14\"", "C", "标准", "骑兵", "25x50mm", "血之芬芳"),
        "defence": ("C", "C", "4", "C+2", "-"), "offence": [("冷蜥", "2", "3", "4", "1", "3", "驾驭，致命一击")],
    },
    "dark-pegasus": {
        "name": "黑暗飞马", "global": ("地面7\" / 飞行8\"", "地面14\" / 飞行16\"", "C", "大型", "骑兵", "40x40mm", "飞行，轻型部队"),
        "defence": ("C", "C", "4", "C+1", "难以瞄准(1)"), "offence": [("黑暗飞马", "2", "4", "4", "1", "4", "驾驭，毁灭冲锋(+1力量，+1AP)")],
        "limit": 2,
    },
    "cold-one-chariot": {
        "name": "冷蜥战车", "global": ("7\"", "7\"", "C", "大型", "构装体", "50x100mm", "血之芬芳，快速移动"),
        "defence": ("4", "C", "4", "C+2", "-"), "offence": [("冷蜥(2)", "2", "3", "4", "1", "3", "驾驭，致命一击"), ("车体", "-", "-", "5", "2", "-", "撞击(D6+1)，不可活动")],
        "limit": 2,
    },
    "manticore": {
        "name": "蝎尾狮", "global": ("地面6\" / 飞行8\"", "地面12\" / 飞行16\"", "C", "大型", "骑兵", "50x50mm", "恐惧，飞行，血之芬芳，孤傲，轻型部队"),
        "defence": ("5", "C", "5", "4", "-"), "offence": [("蝎尾狮", "4", "5", "5", "2", "5", "驾驭，致命一击")],
        "limit": 2, "menagerie": True,
    },
    "black-dragon": {
        "name": "黑龙", "global": ("地面7\" / 飞行7\"", "地面14\" / 飞行14\"", "C", "巨型", "野兽", "50x100mm", "飞行，统御意志"),
        "defence": ("7", "5", "6", "4", "-"), "offence": [("黑龙", "5", "5", "6", "3", "3", "驾驭，毒性吐息")],
        "limit": 1, "menagerie": True,
    },
}


UNITS: list[dict[str, object]] = [
    {
        "key": "dread-prince", "name": "恐惧领主", "page": 6, "category": "characters", "cost": 215,
        "global": ("5\"", "10\"", "9", "标准", "步兵", "20x20mm", "-"),
        "defence": ("3", "7", "3", "0", "重甲"),
        "offence": [("恐惧领主", "5", "8", "4", "1", "8", "致命还击，永恒仇恨，闪电反应，杀戮专精")],
        "details": [("致命还击", "分配给该模型且自然命中为1的敌方普通攻击，会令恐惧领主在主动性0对来源进行一次普通攻击。")],
        "general": True, "item_budget": 200, "titles": True,
        "options": [("海龙披风（步行限定）", 20), ("陨钢黑甲", 10), ("盾牌", 10)],
        "option_groups": [("普通攻击武器（仅限一项）", 0, 1, [("成对武器", 5), ("戟", 10), ("大型武器", 10), ("骑枪", 15)])],
        "mounts": [("dark-steed", 45), ("cold-one", 50), ("cold-one-chariot", 90), ("manticore", 190), ("black-dragon", 390)],
    },
    {
        "key": "beastmaster-lord", "name": "高阶驯兽师", "page": 7, "category": "characters", "cost": 140,
        "global": ("5\"", "10\"", "9", "标准", "步兵", "20x20mm", "野兽奴主"),
        "defence": ("3", "5", "3", "0", "无法被践踏，重甲"),
        "offence": [("高阶驯兽师", "4", "5", "4", "1", "7", "永恒仇恨，闪电反应，杀戮造诣")],
        "details": [("野兽奴主", "12英寸内影响友方伟岸与践踏攻击骰，具体按种族规则第7页。")],
        "general": True, "item_budget": 150, "titles": True,
        "options": [("盾牌", 5)],
        "option_groups": [("普通攻击武器（仅限一项）", 0, 1, [("成对武器", 10), ("戟", 10), ("骑枪", 15), ("大型武器", 15)])],
        "mounts": [("dark-steed", 45), ("cold-one", 50), ("cold-one-chariot", 90), ("dark-pegasus", 90), ("manticore", 220), ("black-dragon", 500)],
    },
    {
        "key": "khaine-assassin", "name": "凯恩刺客", "page": 7, "category": "characters", "cost": 150, "limit": 2,
        "global": ("5\"", "10\"", "9", "标准", "步兵", "20x20mm", "不当头儿，隐藏，轻型部队，职业素养"),
        "defence": ("3", "7", "3", "0", "-"),
        "offence": [("凯恩刺客", "3", "7", "4", "3", "9", "连发手弩[3](2+)，成对武器，永恒仇恨，杀戮专精，多重伤害(2，对人物)，闪电反应，毒性攻击")],
        "details": [("职业素养", "不能加入已经包含相同模型的单位。")],
    },
    {
        "key": "black-ark-admiral", "name": "黑色方舟舰队司令", "page": 8, "category": "characters", "cost": 160,
        "global": ("5\"", "10\"", "10", "标准", "步兵", "20x20mm", "军事训练，战术家"),
        "defence": ("3", "6", "3", "0", "重甲"),
        "offence": [("黑色方舟舰队司令", "3", "6", "4", "1", "7", "永恒仇恨，闪电反应，杀戮造诣")],
        "details": [("战术家", "满足条件的纯步兵单位视为在另一友方军事训练单位8英寸内。")],
        "general": True, "bsb_option": 50, "item_budget": 100, "general_item_budget": 150, "titles": True,
        "options": [("陨钢黑甲", 5), ("盾牌", 5), ("海龙披风（步行限定）", 15)],
        "option_groups": [("普通攻击武器（仅限一项）", 0, 1, [("成对武器", 5), ("戟", 5), ("长矛", 5), ("骑枪", 10), ("大型武器", 10)])],
        "mounts": [("dark-steed", 35), ("cold-one", 40), ("cold-one-chariot", 65), ("dark-pegasus", 70), ("manticore", 200)],
    },
    {
        "key": "high-sorceress", "name": "高阶女术士", "page": 9, "category": "characters", "cost": 240,
        "global": ("5\"", "10\"", "9", "标准", "步兵", "20x20mm", "魔法专家，赫卡提之佑，猜疑，摄人心魄"),
        "defence": ("3", "4", "3", "0", "-"),
        "offence": [("高阶女术士", "1", "4", "3", "0", "5", "永恒仇恨，闪电反应，杀戮造诣")],
        "details": [("摄人心魄", "使用4颗或更多魔法骰施法时，破法结果-2。"), ("猜疑", "作为将军时，使用其鼓舞人心的领导力-1。")],
        "general": True, "wizard": True, "item_budget": 100, "master_option": 170, "master_item_budget": 200, "titles": True,
        "lores": ["火焰系", "野兽系", "阴影系", "死亡系"],
        "options": [("黑暗双刃", 10), ("成对武器", 10), ("轻甲", 5)],
        "mounts": [("dark-steed", 20), ("cold-one", 25), ("dark-pegasus", 35), ("manticore", 75, "魔法大师限定"), ("black-dragon", 400, "魔法大师限定")],
    },
    {
        "key": "death-witch", "name": "死亡魔女", "page": 10, "category": "characters", "cost": 250,
        "global": ("5\"", "10\"", "9", "标准", "步兵", "20x20mm", "无畏"),
        "defence": ("3", "5", "3", "0", "魔盾(4+，对近战攻击)，重甲"),
        "offence": [("死亡魔女", "3", "5", "4", "1", "6", "永恒仇恨，闪电反应，战斗专注，杀戮造诣")],
        "general": True, "wizard": True, "item_budget": 100, "titles": True, "lores": ["金属系", "黑暗系"],
        "option_groups": [
            ("道路（必须选择一项）", 1, 1, [("军旗手", 0, "bsb"), ("征战先知", 65), ("末日先知", 35)]),
            ("普通攻击武器（仅限一项）", 1, 1, [("黑暗双刃", 0), ("戟", 10), ("大型武器", 10), ("成对武器", 10), ("长矛", 10)]),
        ],
    },
    {
        "key": "dread-guard", "name": "恐惧守卫", "page": 13, "category": "core", "cost": 210, "min": 15, "max": 40, "extra_cost": 14,
        "global": ("5\"", "10\"", "8", "标准", "步兵", "20x20mm", "军事训练，得分"), "defence": ("1", "4", "3", "0", "重甲，盾牌"),
        "offence": [("恐惧矛手", "1", "4", "3", "0", "5", "永恒仇恨，杀戮造诣，闪电反应")],
        "options": [("长矛", 1, "per_model")], "command": True, "banner": True,
    },
    {
        "key": "witch-elves", "name": "巫灵", "page": 13, "category": "core", "cost": 150, "min": 10, "max": 30, "extra_cost": 14,
        "global": ("5\"", "10\"", "8", "标准", "步兵", "20x20mm", "无畏，得分"), "defence": ("1", "3", "3", "0", "-"),
        "offence": [("巫灵", "1", "4", "3", "0", "5", "永恒仇恨，黑暗双刃，闪电反应，杀戮造诣")], "command": True, "banner": True,
    },
    {
        "key": "black-repeater-crossbows", "name": "黑锐连弩手", "page": 14, "category": "core", "extra_categories": ["raiders"], "cost": 210, "min": 10, "max": 25, "extra_cost": 13,
        "global": ("5\"", "10\"", "8", "标准", "步兵", "20x20mm", "军事训练，得分，集火压制"), "defence": ("1", "4", "3", "0", "重甲"),
        "offence": [("黑锐连弩手", "1", "4", "3", "0", "5", "永恒仇恨，闪电反应，连弩(3+)，行军和射击，杀戮造诣")],
        "details": [("集火压制", "冲锋阶段可指定18英寸内目标进行领导力测试；失败后对受训单位攻击命中-1，并限制本单位当回合冲锋和射击。")],
        "options": [("盾牌", 1, "per_model")], "command": True, "banner": True,
    },
    {
        "key": "dark-riders", "name": "黑暗骑手", "page": 14, "category": "core", "cost": 185, "min": 5, "max": 10, "extra_cost": 16, "limit": 4,
        "global": ("9\"", "18\"", "8", "标准", "骑兵", "25x50mm", "诈败，轻型部队，先锋"), "defence": ("1", "4", "3", "1", "轻甲，盾牌"),
        "offence": [("黑暗骑手", "1", "4", "3", "0", "5", "轻骑枪，永恒仇恨，闪电反应，杀戮造诣"), ("精灵战马", "1", "3", "3", "0", "4", "驾驭")],
        "options": [("连弩(3+) [R]", 0, "raider_replace")], "command": True,
    },
    {
        "key": "black-ark-corsairs", "name": "黑色方舟海盗", "page": 15, "category": "core", "cost": 165, "min": 10, "max": 30, "extra_cost": 15,
        "global": ("5\"", "10\"", "8", "标准", "步兵", "20x20mm", "轻型部队，残忍奴贩"), "defence": ("1", "4", "3", "0", "海龙披风，重甲"),
        "offence": [("黑色方舟海盗", "1", "4", "3", "0", "5", "永恒仇恨，杀戮造诣，闪电反应，成对武器")],
        "details": [("残忍奴贩", "与海盗底盘接触且不免疫恐惧的敌方模型领导力-1。")],
        "options": [("连发手弩[2](4+)", 3, "raider_add_per_model")], "command": True,
    },
    {
        "key": "beastmaster-team", "name": "驯兽小队", "page": 15, "category": "core", "cost": 150, "min": 10, "max": 30, "extra_cost": 14,
        "global": ("5\"", "10\"", "8", "标准", "步兵", "20x20mm", "得分，抽刺"), "defence": ("1", "4", "3", "0", "轻甲，盾牌"),
        "offence": [("驯兽小队", "1", "4", "3", "0", "5", "永恒仇恨，杀戮造诣，闪电反应")],
        "details": [("抽刺", "单位获得无法被践踏，并可在回合开始提升附近友方骑乘模型移动。")], "command": True,
    },
    {
        "key": "raiding-slaves", "name": "掳掠奴隶", "page": 16, "category": "core", "cost": 110, "min": 20, "max": 40, "extra_cost": 3,
        "global": ("3\"", "12\"", "4", "标准", "步兵", "20x20mm", "炮灰，不稳定，锁链捆缚"), "defence": ("1", "2", "3", "0", "-"),
        "offence": [("掳掠奴隶", "1", "2", "3", "0", "3", "-")],
        "details": [("锁链捆缚", "单位不能主动改变列数；行军后受到D6次自动造伤命中且不能保护。")],
        "options": [("乐手", 10)],
    },
    {
        "key": "naggarond-black-guard", "name": "纳迦隆德黑守卫", "page": 17, "category": "special", "cost": 240, "min": 10, "max": 25, "extra_cost": 23, "limit": 3,
        "global": ("5\"", "10\"", "9", "标准", "步兵", "20x20mm", "军事训练，得分，督战，无畏，坚毅"), "defence": ("1", "6", "3", "0", "陨钢黑甲"),
        "offence": [("纳迦隆德黑守卫", "2", "6", "3", "1", "6", "戟，永恒仇恨，杀戮专精，闪电反应")], "command": True, "banner": True,
    },
    {
        "key": "har-ganeth-executioners", "name": "哈尔·冈西刽子手", "page": 17, "category": "special", "cost": 190, "min": 10, "max": 30, "extra_cost": 20, "limit": 5,
        "global": ("5\"", "10\"", "8", "标准", "步兵", "20x20mm", "得分"), "defence": ("1", "5", "3", "0", "重甲"),
        "offence": [("哈尔·冈西刽子手", "1", "5", "3", "2", "5", "大型武器，杀戮专精，首轮攻击(憎恨)，闪电反应，致命一击")], "command": True, "banner": True,
    },
    {
        "key": "cold-one-knights", "name": "冷蜥骑士", "page": 18, "category": "special", "cost": 255, "min": 5, "max": 10, "extra_cost": 29, "limit": 4,
        "global": ("7\"", "14\"", "9", "标准", "骑兵", "25x50mm", "得分，血之芬芳"), "defence": ("1", "5", "4", "2", "重甲，盾牌"),
        "offence": [("恐惧骑士", "2", "5", "4", "1", "6", "永恒仇恨，杀戮造诣，闪电反应"), ("冷蜥", "2", "3", "4", "1", "3", "驾驭，致命一击")],
        "options": [("冷蜥恐惧骑士（0-1单位/军队）", 10, "per_model_unique_unit")],
        "option_groups": [("武器（仅限一项）", 0, 1, [("骑枪", 8, "per_model"), ("大型武器", 5, "per_model")])],
        "command": True, "banner": True, "dread_title_core": True,
    },
    {
        "key": "cold-one-chariot-unit", "name": "冷蜥战车", "page": 18, "category": "special", "cost": 210, "limit": 3,
        "global": ("7\"", "7\"", "9", "大型", "构装体", "50x100mm", "快速移动，血之芬芳"), "defence": ("4", "5", "4", "2", "重甲"),
        "offence": [("乘员(2)", "2", "5", "4", "1", "6", "永恒仇恨，杀戮造诣，闪电反应"), ("冷蜥(2)", "2", "3", "4", "1", "3", "驾驭，致命一击"), ("战车", "-", "-", "5", "2", "-", "不可活动，撞击(D6+1)")],
        "option_groups": [("乘员武器（必须选择一项）", 1, 1, [("骑枪", 0), ("戟", 0)])],
    },
    {
        "key": "harpies", "name": "鹰身女妖", "page": 19, "category": "special", "cost": 165, "min": 5, "max": 12, "extra_cost": 10, "limit": 3,
        "global": ("地面5\" / 飞行8\"", "地面10\" / 飞行16\"", "6", "标准", "野兽", "20x20mm", "飞行，炮灰，散兵，轻型部队，血之芬芳"), "defence": ("1", "3", "3", "0", "难以瞄准(1)"),
        "offence": [("鹰身女妖", "1", "3", "4", "0", "4", "飞掠打击(1)，毁灭冲锋(+1攻击次数)")],
    },
    {
        "key": "bloodwrack-medusa", "name": "血骸美杜莎", "page": 19, "category": "special", "cost": 150, "min": 1, "max": 3, "extra_cost": 110, "limit": 2, "model_limit": 3,
        "global": ("7\"", "14\"", "8", "大型", "野兽", "40x40mm", "无畏，恐惧，行者，超自然，血之芬芳"), "defence": ("3", "5", "4", "0", "魔盾(5+)"),
        "offence": [("血骸美杜莎", "3", "5", "4", "1", "5", "石化凝视，闪电反应，杀戮造诣")],
        "details": [("石化凝视", "主动性10时对每个接触敌军造成2次AP10魔法命中，按目标高度4+/5+/6+造伤。")],
        "option_groups": [("普通攻击武器（仅限一项）", 0, 1, [("戟", 15, "per_model"), ("成对武器", 0)])],
    },
    {
        "key": "thunder-pack", "name": "雷兽群", "page": 20, "category": "special", "cost": 270, "min": 3, "max": 6, "extra_cost": 70, "shared_pool": "beast-packs",
        "global": ("6\"", "12\"", "8", "大型", "野兽", "40x60mm", "血之芬芳，快速变阵，狂暴"), "defence": ("3", "3", "5", "1", "轻甲"),
        "offence": [("驯兽师", "1", "4", "3", "0", "5", "永恒仇恨，闪电反应，杀戮造诣"), ("雷兽", "4", "3", "6", "1", "3", "毁灭冲锋(+1AP，惊骇)，首轮攻击(憎恨)，驾驭")],
    },
    {
        "key": "ambush-pack", "name": "潜兽群", "page": 20, "category": "special", "cost": 200, "min": 3, "max": 6, "extra_cost": 50, "shared_pool": "beast-packs",
        "global": ("地面2\" / 飞行7\"", "地面4\" / 飞行14\"", "8", "大型", "野兽", "40x60mm", "飞行，血之芬芳，海岸猎食者"), "defence": ("3", "4", "4", "0", "轻甲，盾牌"),
        "offence": [("驯兽师", "1", "4", "3", "0", "5", "永恒仇恨，闪电反应，杀戮造诣"), ("潜兽", "3", "5", "4", "3", "5", "驾驭")],
        "option_groups": [("普通攻击武器（仅限一项）", 0, 1, [("戟", 0), ("骑枪", 2, "per_model")])],
    },
    {
        "key": "doomfire-warlocks", "name": "末日火术士", "page": 21, "category": "special", "cost": 190, "min": 5, "max": 12, "extra_cost": 32, "limit": 2,
        "global": ("9\"", "18\"", "8", "标准", "骑兵", "25x50mm", "轻型部队，秘会法师"), "defence": ("1", "4", "3", "1", "魔盾(5+)，轻甲"),
        "offence": [("末日火术士", "1", "4", "4", "1", "5", "永恒仇恨，杀戮造诣，闪电反应，黑暗双刃"), ("黑暗骏马", "1", "3", "3", "0", "4", "驾驭")],
        "spell_choices": ["彻骨寒风（黑暗系）", "虚弱术（阴影系）", "灵魂枯萎（死亡系）", "毁灭魔矢（黑暗系）"], "spell_count": 2,
        "options": [("队长", 110)],
    },
    {
        "key": "sisters-of-slaughter", "name": "杀戮姐妹", "page": 21, "category": "special", "cost": 250, "min": 10, "max": 30, "extra_cost": 22, "limit": 2,
        "global": ("5\"", "10\"", "8", "标准", "步兵", "20x20mm", "狂暴，无畏，轻型部队"), "defence": ("1", "5", "3", "0", "盾牌，魔盾(5+)"),
        "offence": [("巫灵", "2", "5", "3", "1", "5", "永恒仇恨，战斗专注，毒性攻击，闪电反应，杀戮造诣，首轮攻击(憎恨)")], "command": True, "banner": True,
    },
    {
        "key": "bloodwrack-shrine", "name": "血腥神龛", "page": 22, "category": "special", "cost": 300, "limit": 1,
        "global": ("5\"", "10\"", "8", "大型", "构装体", "60x100mm", "传导(3)，伟岸"), "defence": ("5", "5", "5", "2", "魔盾(5+)"),
        "offence": [("高阶巫灵(3)", "2", "5", "3", "1", "5", "永恒仇恨，战斗专注，闪电反应，杀戮造诣，黑暗双刃"), ("神龛", "-", "-", "5", "2", "1", "不可活动，撞击(D6+1)")],
        "option_groups": [("形态（必须选择一项）", 1, 1, [("沸腾血池", 0), ("血骸神龛", 50)])],
        "details": [("沸腾血池", "获得附属、孤傲、狂暴、战争平台和不当头儿并改变光环效果。"), ("血骸神龛", "获得坚毅、无畏、不战败，改变攻击并提供恐惧光环。")],
    },
    {
        "key": "ravager-chariot", "name": "灾行者战车", "page": 23, "category": "special", "cost": 205, "limit": 2,
        "global": ("9\"", "9\"", "8", "大型", "构装体", "50x100mm", "快速移动"), "defence": ("4", "4", "4", "2", "轻甲"),
        "offence": [("乘员(2)", "1", "4", "3", "0", "5", "轻骑枪，永恒仇恨，杀戮造诣，闪电反应"), ("黑暗骏马(2)", "1", "3", "3", "0", "4", "驾驭"), ("战车", "-", "-", "5", "2", "-", "刺网发射器(3+)，不可活动，撞击(D6)")],
        "details": [("刺网发射器", "射程18、射数3、力量6、AP3、精准、快速射击、装填；命中令目标暂失快速移动。")],
    },
    {
        "key": "reaper-ballista", "name": "收割者弩炮", "page": 23, "category": "special", "cost": 210, "limit": 3, "reduced_by": "ravager-chariot",
        "global": ("5\"", "5\"", "8", "标准", "构装体", "60mm圆", "战争机器"), "defence": ("4", "1", "4", "0", "重甲"),
        "offence": [("操作员", "2", "4", "3", "0", "5", "收割者弩炮(3+)，永恒仇恨，杀戮造诣，闪电反应")],
        "details": [("收割者弩炮", "炮兵武器：射程24、射数8、力量5、AP2；可以移动后射击。")],
    },
    {
        "key": "shades", "name": "黯影", "page": 24, "category": "raiders", "cost": 150, "min": 5, "max": 10, "extra_cost": 30, "limit": 2,
        "global": ("5\"", "10\"", "8", "标准", "步兵", "20x20mm", "侦察兵，散兵，轻型部队"), "defence": ("1", "4", "3", "0", "轻甲，难以瞄准(1)"),
        "offence": [("黯影", "1", "4", "4", "1", "6", "连发手弩[2](4+)，永恒仇恨，杀戮造诣，闪电反应，毒性攻击")],
        "options": [("将连发手弩替换为连弩(3+)", 0), ("队长", 10)],
        "option_groups": [("普通攻击武器（仅限一项）", 0, 1, [("大型武器", 2, "per_model"), ("成对武器", 0)])],
    },
    {
        "key": "abyssal-kraken", "name": "深渊海妖", "page": 25, "category": "menagerie", "cost": 375, "limit": 3,
        "global": ("6\"", "12\"", "8", "巨型", "野兽", "50x100mm", "血之芬芳，海岸猎食者"), "defence": ("5", "5", "5", "3", "干扰，难以瞄准(1)"),
        "offence": [("深渊海妖", "4", "5", "7", "3", "3", "驾驭，憎恨(大型、巨型)，多重伤害(D3)"), ("驯兽师(2)", "1", "4", "3", "0", "5", "永恒仇恨，闪电反应，杀戮造诣")],
        "options": [("巨型海怪（需高阶驯兽师，0-1单位/军队）", 35, "requires_beastmaster_unique")],
    },
    {
        "key": "war-hydra", "name": "战争多头蛇", "page": 25, "category": "menagerie", "cost": 395, "limit": 3,
        "global": ("6\"", "12\"", "8", "巨型", "野兽", "50x100mm", "血之芬芳，多头备用"), "defence": ("6", "4", "5", "3", "重生(5+)"),
        "offence": [("战争多头蛇", "5", "4", "5", "2", "2", "吐息攻击(力量3，AP2)，驾驭，毒性攻击，愤怒"), ("驯兽师(2)", "1", "4", "3", "0", "5", "永恒仇恨，闪电反应，杀戮造诣")],
        "details": [("多头备用", "每个自然6的成功重生可额外无视一个同时伤害；无伤害可无视时恢复1 HP。")],
    },
    {
        "key": "mist-leviathan", "name": "迷雾利维坦", "page": 26, "category": "menagerie", "cost": 230, "limit": 2,
        "global": ("地面2\" / 飞行7\"", "地面4\" / 飞行14\"", "8", "巨型", "野兽", "100x100mm", "飞行，轻型部队，血之芬芳，迷雾之下"), "defence": ("8", "3", "5", "0", "干扰"),
        "offence": [("迷雾利维坦", "4", "3", "4", "3", "3", "驾驭"), ("操作员(4)", "1", "4", "3", "0", "5", "永恒仇恨，闪电反应，杀戮造诣")],
        "details": [("迷雾之下", "8英寸内敌军射击命中-1；第一回合附近友方步兵获得难以瞄准(1)。")],
    },
]


LEGENDARY_UNITS: list[dict[str, object]] = [
    {"key": "malekith", "name": "马雷基斯", "page": 72, "cost": 1100, "categories": ["characters", "menagerie", "legendary"], "forced_general": True,
     "global": ("地面7\" / 飞行7\"", "地面14\" / 飞行14\"", "10", "巨型", "野兽", "50x100mm", "飞行，无畏，魔法大师，统御意志，赫卡提之佑，绝对力量"),
     "defence": ("7", "6", "6", "4", "午夜护甲"), "offence": [("马雷基斯", "5", "8", "5", "2", "8", "毁灭者，永恒仇恨，闪电反应，杀戮专精"), ("塞拉芬(黑龙)", "6", "7", "6", "3", "3", "驾驭，毒性吐息")], "lores": ["黑暗系"]},
    {"key": "morathi", "name": "莫拉斯", "page": 73, "cost": 655, "categories": ["characters", "legendary"], "general": True,
     "global": ("5\"", "10\"", "10", "标准", "步兵", "20x20mm", "魔法大师，赫卡提之佑，首席女巫，魅惑之美"),
     "defence": ("3", "5", "3", "0", "琥珀护符"), "offence": [("莫拉斯", "3", "5", "3", "0", "6", "碎心者与暗黑剑，永恒仇恨，闪电反应，杀戮造诣")], "lores": ["阴影系", "死亡系", "黑暗系"],
     "options": [("苏勒菲特(黑暗飞马)", 45), ("替换为“暗影女王”莫拉斯", 345, "morathi-shadow")]},
    {"key": "hellebron", "name": "妖婆赫莉本", "page": 75, "cost": 590, "categories": ["characters", "legendary"], "general": True,
     "global": ("5\"", "10\"", "10", "标准", "步兵", "20x20mm", "狂暴，无畏，血腥女王，凯恩冠军"),
     "defence": ("3", "7", "3", "0", "黑火护身符"), "offence": [("妖婆赫莉本", "4", "7", "4", "1", "9", "死亡之剑与诅咒之刃，永恒仇恨，闪电反应，杀戮造诣，毒性攻击")]},
    {"key": "malus-darkblade", "name": "马鲁斯·黑刃", "page": 76, "cost": 350, "categories": ["characters", "legendary"], "general": True, "item_budget": 100,
     "global": ("7\"", "14\"", "10", "标准", "步兵", "20x20mm", "扎坎附身，寒冷的心"), "defence": ("3", "7", "4", "0", "陨钢黑甲"),
     "offence": [("马鲁斯·黑刃", "5", "7", "4", "1", "8", "凯恩次元剑，永恒仇恨，闪电反应，杀戮专精")], "options": [("怨毒(冷蜥)", 100)]},
    {"key": "lokhir-fellheart", "name": "洛克西亚·堕落之心", "page": 77, "cost": 400, "categories": ["characters", "legendary"], "general": True,
     "global": ("5\"", "10\"", "9", "标准", "步兵", "20x20mm", "军事训练，战术家，弄潮儿，奴隶贩子，施虐狂"), "defence": ("3", "6", "3", "0", "克拉肯巨妖头盔，重甲，海龙披风"),
     "offence": [("洛克西亚·堕落之心", "3", "6", "4", "1", "7", "红色双剑，永恒仇恨，闪电反应，杀戮专精")]},
    {"key": "shadowblade", "name": "影刃", "page": 77, "cost": 350, "categories": ["characters", "legendary"],
     "global": ("5\"", "10\"", "9", "标准", "步兵", "20x20mm", "不当头儿，无畏，隐藏，悲恸之心，恶魔之力药剂"), "defence": ("3", "9", "3", "0", "轻甲，魔盾(5+)"),
     "offence": [("影刃", "3", "10", "4", "3", "10", "成对武器，永恒仇恨，杀戮专精，多重伤害(2，对人物)，闪电反应，毒性攻击，致命一击，黑莲花，黑暗剧毒")]},
    {"key": "rakarth", "name": "拉卡斯", "page": 78, "cost": 720, "categories": ["characters", "menagerie", "legendary"], "general": True,
     "global": ("地面7\" / 飞行7\"", "地面14\" / 飞行14\"", "9", "巨型", "野兽", "50x100mm", "飞行，无畏，统御意志，野兽奴主，野兽领主的凝视"), "defence": ("7", "5", "6", "4", "卡隆德·卡尔野兽护甲"),
     "offence": [("拉卡斯", "4", "5", "4", "1", "7", "痛苦之鞭，永恒仇恨，闪电反应，杀戮造诣"), ("巴绰斯(黑龙)", "5", "6", "6", "3", "3", "驾驭，毒性吐息")]},
]


def write_xml(root: ET.Element, path: Path) -> None:
    ET.indent(root, space="  ")
    body = ET.tostring(root, encoding="unicode", short_empty_elements=True)
    path.write_text('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + body + "\n", encoding="utf-8")


def child_container(parent: ET.Element, namespace: str, tag: str) -> ET.Element:
    existing = next((child for child in parent if child.tag == q(namespace, tag)), None)
    return existing if existing is not None else sub(parent, namespace, tag)


def add_condition(
    modifier: ET.Element,
    namespace: str,
    *,
    condition_type: str,
    value: int | float,
    field: str,
    scope: str,
    child_id: str,
    include_children: bool = True,
    include_forces: bool = True,
) -> None:
    conditions = child_container(modifier, namespace, "conditions")
    sub(
        conditions,
        namespace,
        "condition",
        type=condition_type,
        value=value,
        field=field,
        scope=scope,
        childId=child_id,
        shared=True,
        includeChildSelections=include_children,
        includeChildForces=include_forces,
    )


def add_scaled_limit(
    parent: ET.Element,
    namespace: str,
    key: str,
    limit: int,
    *,
    scope: str = "roster",
) -> str:
    constraint_id = add_constraint(
        parent,
        namespace,
        f"{key}:limit",
        "max",
        limit,
        scope=scope,
        include_children=True,
        include_forces=True,
    )
    modifiers = child_container(parent, namespace, "modifiers")
    warband = sub(modifiers, namespace, "modifier", type="set", value=(limit + 1) // 2, field=constraint_id)
    add_condition(
        warband,
        namespace,
        condition_type="lessThan",
        value=3000,
        field=f"limit::{POINTS}",
        scope="roster",
        child_id="any",
    )
    legion = sub(modifiers, namespace, "modifier", type="set", value=limit * 2, field=constraint_id)
    add_condition(
        legion,
        namespace,
        condition_type="atLeast",
        value=8000,
        field=f"limit::{POINTS}",
        scope="roster",
        child_id="any",
    )
    return constraint_id


def new_selection_entry(
    parent: ET.Element,
    namespace: str,
    key: str,
    name: str,
    entry_type: str,
    *,
    publication_id: str | None = None,
    page: int | str | None = None,
    hidden: bool = False,
) -> ET.Element:
    attrs: dict[str, object] = {
        "id": stable_id(key),
        "name": name,
        "hidden": hidden,
        "collective": False,
        "import_": True,
        "type": entry_type,
    }
    if publication_id:
        attrs["publicationId"] = publication_id
    if page is not None:
        attrs["page"] = page
    entry = sub(parent, namespace, "selectionEntry", **attrs)
    entry.attrib["import"] = entry.attrib.pop("import_")
    return entry


def add_entry_link(
    parent: ET.Element,
    namespace: str,
    key: str,
    name: str,
    target_id: str,
    target_type: str,
    *,
    cost: int | None = None,
    hidden: bool = False,
) -> ET.Element:
    links = child_container(parent, namespace, "entryLinks")
    link = sub(
        links,
        namespace,
        "entryLink",
        id=stable_id(f"entry-link:{key}"),
        name=name,
        hidden=hidden,
        collective=False,
        import_=True,
        targetId=target_id,
        type=target_type,
    )
    link.attrib["import"] = link.attrib.pop("import_")
    if cost is not None:
        add_cost(link, namespace, cost)
    return link


def add_visibility_modifier(
    parent: ET.Element,
    namespace: str,
    key: str,
    required_id: str,
    *,
    scope: str = "ancestor",
) -> None:
    modifiers = child_container(parent, namespace, "modifiers")
    modifier = sub(modifiers, namespace, "modifier", type="set", value=False, field="hidden")
    add_condition(
        modifier,
        namespace,
        condition_type="atLeast",
        value=1,
        field="selections",
        scope=scope,
        child_id=required_id,
    )


def add_per_model_cost(option: ET.Element, namespace: str, key: str, value: int, model_id: str) -> None:
    modifiers = child_container(option, namespace, "modifiers")
    modifier = sub(modifiers, namespace, "modifier", type="increment", value=value, field=POINTS)
    repeats = sub(modifier, namespace, "repeats")
    sub(
        repeats,
        namespace,
        "repeat",
        field="selections",
        scope="parent",
        value=1,
        percentValue=False,
        shared=True,
        includeChildSelections=False,
        includeChildForces=False,
        childId=model_id,
        repeats=1,
        roundUp=False,
    )
    add_cost(option, namespace, 0)


def add_banner_choices(parent: ET.Element, namespace: str, key: str, maximum: int) -> None:
    groups = child_container(parent, namespace, "selectionEntryGroups")
    group = sub(groups, namespace, "selectionEntryGroup", id=stable_id(f"group:{key}:banner-items"), name=f"旗帜附魔（至多{maximum}件）", hidden=False, collective=False, import_="true")
    group.attrib["import"] = group.attrib.pop("import_")
    add_constraint(group, namespace, f"{key}:banner-items:max", "max", maximum, include_children=True)
    add_entry_link(group, namespace, f"{key}:common-banners", "通用旗帜附魔", stable_id("group:common-items:banner"), "selectionEntryGroup")
    add_entry_link(group, namespace, f"{key}:de-banners", "黑暗精灵旗帜附魔", stable_id("group:de-items:banner"), "selectionEntryGroup")


def add_option_entry(
    parent: ET.Element,
    namespace: str,
    unit_key: str,
    option_data: tuple,
    model_id: str | None,
) -> tuple[ET.Element, str | None]:
    name, cost, *rest = option_data
    tag = rest[0] if rest else None
    key = f"option:{unit_key}:{name}"
    option = new_selection_entry(parent, namespace, key, str(name), "upgrade")
    add_constraint(option, namespace, f"{key}:parent", "max", 1)
    if tag in {"per_model", "raider_add_per_model", "per_model_unique_unit"}:
        if model_id is None:
            raise ValueError(f"Per-model option without a model entry: {unit_key}/{name}")
        add_per_model_cost(option, namespace, key, int(cost), model_id)
    else:
        add_cost(option, namespace, int(cost))
    if tag == "per_model_unique_unit":
        add_scaled_limit(option, namespace, f"{key}:roster", 1)
    if tag == "bsb":
        add_category_link(option, namespace, f"{key}:bsb", CATEGORIES["bsb"], category_id("bsb"), primary=False)
        add_banner_choices(option, namespace, key, 2)
    if tag == "requires_beastmaster_unique":
        option.set("hidden", "true")
        add_visibility_modifier(option, namespace, key, stable_id("unit:beastmaster-lord"), scope="roster")
        add_scaled_limit(option, namespace, f"{key}:roster", 1)
    return option, tag


def add_item_wrapper(
    unit: ET.Element,
    namespace: str,
    unit_key: str,
    budget: int,
    *,
    general_id: str | None = None,
    general_budget: int | None = None,
    master_id: str | None = None,
    master_budget: int | None = None,
) -> None:
    entries = child_container(unit, namespace, "selectionEntries")
    wrapper_key = f"items:{unit_key}"
    wrapper = new_selection_entry(entries, namespace, wrapper_key, f"特殊物品（至多{budget}分）", "upgrade")
    add_constraint(wrapper, namespace, f"{wrapper_key}:selected", "max", 1)
    budget_constraint = add_constraint(wrapper, namespace, f"{wrapper_key}:budget", "max", budget, field=POINTS, include_children=True)
    groups = child_container(wrapper, namespace, "selectionEntryGroups")
    group = sub(groups, namespace, "selectionEntryGroup", id=stable_id(f"group:{wrapper_key}"), name="特殊物品选择", hidden=False, collective=False, import_="true")
    group.attrib["import"] = group.attrib.pop("import_")
    for kind, label in [("weapon", "武器附魔"), ("armour", "护甲附魔"), ("curio", "魔法奇物")]:
        add_entry_link(group, namespace, f"{wrapper_key}:common:{kind}", f"通用{label}", stable_id(f"group:common-items:{kind}"), "selectionEntryGroup")
        add_entry_link(group, namespace, f"{wrapper_key}:de:{kind}", f"黑暗精灵{label}", stable_id(f"group:de-items:{kind}"), "selectionEntryGroup")
    modifiers = child_container(wrapper, namespace, "modifiers")
    if general_id and general_budget is not None:
        modifier = sub(modifiers, namespace, "modifier", type="set", value=general_budget, field=budget_constraint)
        add_condition(modifier, namespace, condition_type="atLeast", value=1, field="selections", scope="ancestor", child_id=general_id)
    if master_id and master_budget is not None:
        modifier = sub(modifiers, namespace, "modifier", type="set", value=master_budget, field=budget_constraint)
        add_condition(modifier, namespace, condition_type="atLeast", value=1, field="selections", scope="ancestor", child_id=master_id)
    add_cost(wrapper, namespace, 0)


def add_category_change(
    unit: ET.Element,
    namespace: str,
    key: str,
    option_id: str,
    *,
    add: list[str] | None = None,
    remove: list[str] | None = None,
    primary: str | None = None,
) -> None:
    modifiers = child_container(unit, namespace, "modifiers")
    for action, categories in (("add", add or []), ("remove", remove or [])):
        for category in categories:
            modifier = sub(modifiers, namespace, "modifier", type=action, value=category_id(category), field="category")
            add_condition(modifier, namespace, condition_type="atLeast", value=1, field="selections", scope="self", child_id=option_id)
    if primary:
        modifier = sub(modifiers, namespace, "modifier", type="set-primary", value=category_id(primary), field="category")
        add_condition(modifier, namespace, condition_type="atLeast", value=1, field="selections", scope="self", child_id=option_id)


def add_unit(
    parent: ET.Element,
    namespace: str,
    data: dict[str, object],
    publication_id: str,
    *,
    legendary: bool,
) -> None:
    key = str(data["key"])
    unit_id = stable_id(f"unit:{key}")
    unit = new_selection_entry(parent, namespace, f"unit:{key}", str(data["name"]), "unit", publication_id=publication_id, page=data.get("page"))

    add_profile(unit, namespace, f"unit:{key}:global", "global", str(data["name"]), dict(zip(PROFILE_TYPES["global"][1], data["global"])))
    add_profile(unit, namespace, f"unit:{key}:defence", "defence", str(data["name"]), dict(zip(PROFILE_TYPES["defence"][1], data["defence"])))
    for index, attack in enumerate(data["offence"]):
        add_profile(unit, namespace, f"unit:{key}:offence:{index}", "offence", attack[0], dict(zip(PROFILE_TYPES["offence"][1], attack[1:])))
    for detail_name, description in data.get("details", []):
        add_embedded_rule(unit, namespace, f"unit:{key}:{detail_name}", detail_name, description)

    searchable = str(data)
    for rule_key, (rule_name, _description) in DE_RULES.items():
        if rule_name in searchable:
            add_info_link(unit, namespace, f"unit:{key}:{rule_key}", rule_name, stable_id(f"de-rule:{rule_key}"))

    categories = list(data.get("categories", [])) if legendary else [str(data["category"]), *data.get("extra_categories", [])]
    for index, category in enumerate(categories):
        add_category_link(unit, namespace, f"unit:{key}:{category}", CATEGORIES[category], category_id(category), primary=index == 0)
    if not legendary and data.get("category") != "characters":
        add_category_link(unit, namespace, f"unit:{key}:non-character", CATEGORIES["non_character"], category_id("non_character"), primary=False)
    if data.get("wizard") or data.get("lores"):
        add_category_link(unit, namespace, f"unit:{key}:wizard", CATEGORIES["wizard"], category_id("wizard"), primary=False)
    if data.get("shared_pool"):
        add_category_link(unit, namespace, f"unit:{key}:shared-pool", "雷兽群与潜兽群共享池", stable_id("category:beast-packs"), primary=False)

    model_id: str | None = None
    if data.get("min") is not None:
        entries = child_container(unit, namespace, "selectionEntries")
        model_key = f"model:{key}"
        model_id = stable_id(model_key)
        model = new_selection_entry(entries, namespace, model_key, str(data["name"]), "model")
        adjustment = int(data["cost"]) - int(data["min"]) * int(data["extra_cost"])
        if adjustment >= 0:
            add_constraint(model, namespace, f"{model_key}:min", "min", int(data["min"]))
            add_constraint(model, namespace, f"{model_key}:max", "max", int(data["max"]))
            if data.get("model_limit"):
                add_scaled_limit(model, namespace, f"{model_key}:roster", int(data["model_limit"]))
            add_cost(model, namespace, int(data["extra_cost"]))
            add_cost(unit, namespace, adjustment)
        else:
            if "per_model" in str(data.get("options", [])) + str(data.get("option_groups", [])):
                raise ValueError(f"Split model pricing needs multi-pool per-model option support: {key}")
            add_constraint(model, namespace, f"{model_key}:min", "min", int(data["min"]))
            add_constraint(model, namespace, f"{model_key}:max", "max", int(data["min"]))
            add_cost(model, namespace, 0)
            extra_key = f"model:{key}:additional"
            extra = new_selection_entry(entries, namespace, extra_key, f"额外{data['name']}", "model")
            add_constraint(extra, namespace, f"{extra_key}:max", "max", int(data["max"]) - int(data["min"]))
            add_cost(extra, namespace, int(data["extra_cost"]))
            add_cost(unit, namespace, int(data["cost"]))
    else:
        add_cost(unit, namespace, int(data["cost"]))

    limit_constraint: str | None = None
    if legendary:
        add_constraint(unit, namespace, f"unit:{key}:unique", "max", 1, scope="roster", include_children=True, include_forces=True)
    elif data.get("limit"):
        limit_constraint = add_scaled_limit(unit, namespace, f"unit:{key}", int(data["limit"]))

    entries = child_container(unit, namespace, "selectionEntries")
    general_id: str | None = None
    bsb_ids: list[str] = []
    if data.get("forced_general"):
        add_category_link(unit, namespace, f"unit:{key}:forced-general", CATEGORIES["general"], category_id("general"), primary=False)
    elif data.get("general"):
        general = new_selection_entry(entries, namespace, f"option:{key}:general", "任命为将军", "upgrade")
        general_id = general.get("id")
        add_constraint(general, namespace, f"option:{key}:general:parent", "max", 1)
        add_category_link(general, namespace, f"option:{key}:general:category", CATEGORIES["general"], category_id("general"), primary=False)
        add_cost(general, namespace, 0)

    master_id: str | None = None
    if data.get("master_option") is not None:
        master = new_selection_entry(entries, namespace, f"option:{key}:magic-master", "魔法大师", "upgrade")
        master_id = master.get("id")
        add_constraint(master, namespace, f"option:{key}:magic-master:parent", "max", 1)
        add_cost(master, namespace, int(data["master_option"]))

    if data.get("bsb_option") is not None:
        bsb = new_selection_entry(entries, namespace, f"option:{key}:bsb", "军旗手", "upgrade")
        bsb_ids.append(bsb.get("id"))
        add_constraint(bsb, namespace, f"option:{key}:bsb:parent", "max", 1)
        add_category_link(bsb, namespace, f"option:{key}:bsb:category", CATEGORIES["bsb"], category_id("bsb"), primary=False)
        add_banner_choices(bsb, namespace, f"option:{key}:bsb", 2)
        add_cost(bsb, namespace, int(data["bsb_option"]))

    option_effects: list[tuple[str, str | None]] = []
    for option_data in data.get("options", []):
        option, tag = add_option_entry(entries, namespace, key, option_data, model_id)
        option_effects.append((option.get("id"), tag))

    groups = child_container(unit, namespace, "selectionEntryGroups")
    for group_index, (group_name, minimum, maximum, options) in enumerate(data.get("option_groups", [])):
        group_key = f"unit:{key}:group:{group_index}"
        group = sub(groups, namespace, "selectionEntryGroup", id=stable_id(group_key), name=group_name, hidden=False, collective=False, import_="true")
        group.attrib["import"] = group.attrib.pop("import_")
        if minimum:
            add_constraint(group, namespace, f"{group_key}:min", "min", int(minimum), include_children=True)
        if maximum:
            add_constraint(group, namespace, f"{group_key}:max", "max", int(maximum), include_children=True)
        group_entries = sub(group, namespace, "selectionEntries")
        for option_data in options:
            option, tag = add_option_entry(group_entries, namespace, key, option_data, model_id)
            option_effects.append((option.get("id"), tag))
            if tag == "bsb":
                bsb_ids.append(option.get("id"))

    if data.get("command"):
        command = sub(groups, namespace, "selectionEntryGroup", id=stable_id(f"unit:{key}:command"), name="指挥组", hidden=False, collective=False, import_="true")
        command.attrib["import"] = command.attrib.pop("import_")
        command_entries = sub(command, namespace, "selectionEntries")
        for role in ["队长", "乐手", "旗手"]:
            upgrade = new_selection_entry(command_entries, namespace, f"option:{key}:command:{role}", role, "upgrade")
            add_constraint(upgrade, namespace, f"option:{key}:command:{role}:max", "max", 1)
            add_cost(upgrade, namespace, 10)
            if role == "旗手" and data.get("banner"):
                add_banner_choices(upgrade, namespace, f"option:{key}:command:{role}", 1)

    if data.get("mounts"):
        mount_group = sub(groups, namespace, "selectionEntryGroup", id=stable_id(f"unit:{key}:mounts"), name="坐骑（仅限一项）", hidden=False, collective=False, import_="true")
        mount_group.attrib["import"] = mount_group.attrib.pop("import_")
        add_constraint(mount_group, namespace, f"unit:{key}:mounts:max", "max", 1, include_children=True)
        for mount_data in data["mounts"]:
            mount_key, cost, *restriction = mount_data
            link = add_entry_link(mount_group, namespace, f"unit:{key}:mount:{mount_key}", MOUNTS[mount_key]["name"], stable_id(f"mount:{mount_key}"), "selectionEntry", cost=int(cost), hidden=bool(restriction))
            if restriction and master_id:
                add_visibility_modifier(link, namespace, f"unit:{key}:mount:{mount_key}", master_id)

    if data.get("lores"):
        lore_group = sub(groups, namespace, "selectionEntryGroup", id=stable_id(f"unit:{key}:lores"), name="魔法派系（必须选择一项）", hidden=False, collective=False, import_="true")
        lore_group.attrib["import"] = lore_group.attrib.pop("import_")
        add_constraint(lore_group, namespace, f"unit:{key}:lores:min", "min", 1, include_children=True)
        add_constraint(lore_group, namespace, f"unit:{key}:lores:max", "max", 1, include_children=True)
        for lore in data["lores"]:
            add_entry_link(lore_group, namespace, f"unit:{key}:lore:{lore}", lore, stable_id(f"lore:{lore}"), "selectionEntry")

    if data.get("spell_choices"):
        spell_group = sub(groups, namespace, "selectionEntryGroup", id=stable_id(f"unit:{key}:spells"), name=f"秘会法术（必须选择{data['spell_count']}项）", hidden=False, collective=False, import_="true")
        spell_group.attrib["import"] = spell_group.attrib.pop("import_")
        add_constraint(spell_group, namespace, f"unit:{key}:spells:min", "min", int(data["spell_count"]), include_children=True)
        add_constraint(spell_group, namespace, f"unit:{key}:spells:max", "max", int(data["spell_count"]), include_children=True)
        spell_entries = sub(spell_group, namespace, "selectionEntries")
        for spell in data["spell_choices"]:
            choice = new_selection_entry(spell_entries, namespace, f"spell-choice:{key}:{spell}", spell, "upgrade")
            add_constraint(choice, namespace, f"spell-choice:{key}:{spell}:max", "max", 1)
            add_cost(choice, namespace, 0)

    if data.get("titles"):
        title_outer = sub(groups, namespace, "selectionEntryGroup", id=stable_id(f"unit:{key}:titles"), name="异名（至多一项）", hidden=False, collective=False, import_="true")
        title_outer.attrib["import"] = title_outer.attrib.pop("import_")
        add_constraint(title_outer, namespace, f"unit:{key}:titles:max", "max", 1, include_children=True)
        add_entry_link(title_outer, namespace, f"unit:{key}:titles", "异名", stable_id("group:de-titles"), "selectionEntryGroup")

    if data.get("item_budget") is not None:
        add_item_wrapper(
            unit,
            namespace,
            key,
            int(data["item_budget"]),
            general_id=general_id,
            general_budget=int(data["general_item_budget"]) if data.get("general_item_budget") is not None else None,
            master_id=master_id,
            master_budget=int(data["master_item_budget"]) if data.get("master_item_budget") is not None else None,
        )

    if data.get("dread_title_core"):
        convert_key = f"option:{key}:dread-title-core"
        convert = new_selection_entry(entries, namespace, convert_key, "计入核心（需要异名：恐惧之主）", "upgrade", hidden=True)
        add_constraint(convert, namespace, f"{convert_key}:parent", "max", 1)
        add_scaled_limit(convert, namespace, f"{convert_key}:roster", 1)
        add_visibility_modifier(convert, namespace, convert_key, stable_id("de-title:dread-lord"), scope="roster")
        add_cost(convert, namespace, 0)
        add_category_change(unit, namespace, convert_key, convert.get("id"), add=["core"], remove=["special"], primary="core")

    for option_id, tag in option_effects:
        if tag == "raider_replace":
            add_category_change(unit, namespace, f"unit:{key}:raider-replace", option_id, add=["raiders"], remove=["core"], primary="raiders")
        elif tag == "raider_add_per_model":
            add_category_change(unit, namespace, f"unit:{key}:raider-add", option_id, add=["raiders"])
        elif tag == "morathi-shadow":
            add_category_change(unit, namespace, f"unit:{key}:shadow-form", option_id, add=["menagerie"])

    if general_id and bsb_ids:
        for bsb_id in bsb_ids:
            general = next((node for node in unit.iter() if node.get("id") == general_id), None)
            bsb = next((node for node in unit.iter() if node.get("id") == bsb_id), None)
            if general is not None:
                modifiers = child_container(general, namespace, "modifiers")
                hide = sub(modifiers, namespace, "modifier", type="set", value=True, field="hidden")
                add_condition(hide, namespace, condition_type="atLeast", value=1, field="selections", scope="ancestor", child_id=bsb_id)
            if bsb is not None:
                modifiers = child_container(bsb, namespace, "modifiers")
                hide = sub(modifiers, namespace, "modifier", type="set", value=True, field="hidden")
                add_condition(hide, namespace, condition_type="atLeast", value=1, field="selections", scope="ancestor", child_id=general_id)

    if data.get("reduced_by") and limit_constraint:
        modifiers = child_container(unit, namespace, "modifiers")
        modifier = sub(modifiers, namespace, "modifier", type="decrement", value=1, field=limit_constraint)
        repeats = sub(modifier, namespace, "repeats")
        sub(repeats, namespace, "repeat", field="selections", scope="roster", value=1, percentValue=False, shared=True, includeChildSelections=True, includeChildForces=True, childId=stable_id(f"unit:{data['reduced_by']}"), repeats=1, roundUp=False)


def faction_object_key(faction_key: str, kind: str, object_key: str) -> str:
    return f"{kind}:{faction_key}:{object_key}"


def add_faction_banner_choices(
    parent: ET.Element,
    namespace: str,
    faction: dict[str, object],
    key: str,
    maximum: int = 1,
) -> None:
    faction_key = str(faction["key"])
    groups = child_container(parent, namespace, "selectionEntryGroups")
    group = sub(
        groups,
        namespace,
        "selectionEntryGroup",
        id=stable_id(f"group:{faction_key}:{key}:banner-items"),
        name=f"旗帜附魔（至多{maximum}件）",
        hidden=False,
        collective=False,
        import_="true",
    )
    group.attrib["import"] = group.attrib.pop("import_")
    add_constraint(group, namespace, f"{faction_key}:{key}:banner-items:max", "max", maximum, include_children=True)
    add_entry_link(
        group,
        namespace,
        f"{faction_key}:{key}:common-banners",
        "通用旗帜附魔",
        stable_id("group:common-items:banner"),
        "selectionEntryGroup",
    )
    banner_kinds = ["banner", *faction.get("banner_kinds", [])]
    for kind in banner_kinds:
        if kind in dict(faction.get("items", {})):
            add_entry_link(
                group,
                namespace,
                f"{faction_key}:{key}:faction-banners:{kind}",
                f"{faction['name']}旗帜附魔",
                stable_id(f"group:{faction_key}:items:{kind}"),
                "selectionEntryGroup",
            )


def add_faction_item_wrapper(
    unit_entry: ET.Element,
    namespace: str,
    faction: dict[str, object],
    data: dict[str, object],
    general_id: str | None,
) -> None:
    faction_key = str(faction["key"])
    unit_key = str(data["key"])
    budget = int(data["item_budget"])
    entries = child_container(unit_entry, namespace, "selectionEntries")
    wrapper_key = f"{faction_key}:items:{unit_key}"
    wrapper = new_selection_entry(entries, namespace, wrapper_key, f"特殊物品（至多{budget}分）", "upgrade")
    add_constraint(wrapper, namespace, f"{wrapper_key}:selected", "max", 1)
    budget_constraint = add_constraint(
        wrapper,
        namespace,
        f"{wrapper_key}:budget",
        "max",
        budget,
        field=POINTS,
        include_children=True,
    )
    groups = child_container(wrapper, namespace, "selectionEntryGroups")
    group = sub(
        groups,
        namespace,
        "selectionEntryGroup",
        id=stable_id(f"group:{wrapper_key}"),
        name="特殊物品选择",
        hidden=False,
        collective=False,
        import_="true",
    )
    group.attrib["import"] = group.attrib.pop("import_")
    if not faction.get("no_common_items"):
        for kind, label in [("weapon", "武器附魔"), ("armour", "护甲附魔"), ("curio", "魔法奇物")]:
            add_entry_link(
                group,
                namespace,
                f"{wrapper_key}:common:{kind}",
                f"通用{label}",
                stable_id(f"group:common-items:{kind}"),
                "selectionEntryGroup",
            )
    faction_kinds = ["weapon", "armour", "curio", *data.get("faction_item_kinds", [])]
    for kind in dict.fromkeys(faction_kinds):
        if kind not in dict(faction.get("items", {})):
            continue
        add_entry_link(
            group,
            namespace,
            f"{wrapper_key}:faction:{kind}",
            f"{faction['name']}：{kind}",
            stable_id(f"group:{faction_key}:items:{kind}"),
            "selectionEntryGroup",
        )
    if general_id and data.get("item_budget_general") is not None:
        modifiers = child_container(wrapper, namespace, "modifiers")
        modifier = sub(
            modifiers,
            namespace,
            "modifier",
            type="set",
            value=int(data["item_budget_general"]),
            field=budget_constraint,
        )
        add_condition(
            modifier,
            namespace,
            condition_type="atLeast",
            value=1,
            field="selections",
            scope="ancestor",
            child_id=general_id,
        )
    add_cost(wrapper, namespace, 0)


def add_faction_option(
    parent: ET.Element,
    namespace: str,
    faction_key: str,
    unit_key: str,
    option_data: tuple,
    model_id: str | None,
) -> tuple[ET.Element, str | None]:
    name, cost, *rest = option_data
    tag = str(rest[0]) if rest else None
    key = f"{faction_key}:option:{unit_key}:{name}"
    option = new_selection_entry(parent, namespace, key, str(name), "upgrade")
    add_constraint(option, namespace, f"{key}:parent", "max", 1)
    if tag and tag.startswith("per_model"):
        if model_id is None:
            raise ValueError(f"Per-model option without a model entry: {faction_key}/{unit_key}/{name}")
        add_per_model_cost(option, namespace, key, int(cost), model_id)
    else:
        add_cost(option, namespace, int(cost))
    if tag == "bsb":
        add_category_link(option, namespace, f"{key}:bsb", CATEGORIES["bsb"], category_id("bsb"))
        add_faction_banner_choices(option, namespace, next(f for f in FACTIONS if f["key"] == faction_key), key, 2)
    return option, tag


def add_faction_unit(
    parent: ET.Element,
    namespace: str,
    faction: dict[str, object],
    data: dict[str, object],
    publication_id: str,
) -> None:
    faction_key = str(faction["key"])
    unit_key = str(data["key"])
    key = f"{faction_key}:{unit_key}"
    entry = new_selection_entry(
        parent,
        namespace,
        faction_object_key(faction_key, "unit", unit_key),
        str(data["name"]),
        "unit",
        publication_id=publication_id,
        page=data.get("page"),
    )
    add_profile(entry, namespace, f"{key}:global", "global", str(data["name"]), dict(zip(PROFILE_TYPES["global"][1], data["global"])))
    add_profile(entry, namespace, f"{key}:defence", "defence", str(data["name"]), dict(zip(PROFILE_TYPES["defence"][1], data["defence"])))
    for index, attack in enumerate(data["offence"]):
        add_profile(entry, namespace, f"{key}:offence:{index}", "offence", str(attack[0]), dict(zip(PROFILE_TYPES["offence"][1], attack[1:])))
    for detail_name, description in data.get("details", []):
        add_embedded_rule(entry, namespace, f"{key}:detail:{detail_name}", str(detail_name), str(description))

    categories = [str(data["category"]), *[str(value) for value in data.get("extra_categories", [])]]
    for index, category in enumerate(categories):
        add_category_link(entry, namespace, f"{key}:category:{category}", CATEGORIES[category], category_id(category), primary=index == 0)
    if data["category"] != "characters":
        add_category_link(entry, namespace, f"{key}:non-character", CATEGORIES["non_character"], category_id("non_character"))
    if data.get("wizard") or data.get("lores"):
        add_category_link(entry, namespace, f"{key}:wizard", CATEGORIES["wizard"], category_id("wizard"))
    if data.get("shared_pool"):
        pool_key = str(data["shared_pool"])
        add_category_link(
            entry,
            namespace,
            f"{key}:pool:{pool_key}",
            next(name for pool, name, _limit in faction.get("shared_pools", []) if pool == pool_key),
            stable_id(f"category:{faction_key}:pool:{pool_key}"),
        )

    model_id: str | None = None
    if data.get("min") is not None:
        entries = child_container(entry, namespace, "selectionEntries")
        model_key = faction_object_key(faction_key, "model", unit_key)
        model_id = stable_id(model_key)
        minimum = int(data["min"])
        maximum = int(data["max"])
        extra_cost = int(data["extra_cost"])
        adjustment = int(data["cost"]) - minimum * extra_cost
        if adjustment >= 0:
            model = new_selection_entry(entries, namespace, model_key, str(data["name"]), "model")
            add_constraint(model, namespace, f"{model_key}:min", "min", minimum)
            add_constraint(model, namespace, f"{model_key}:max", "max", maximum)
            if data.get("model_limit"):
                add_scaled_limit(model, namespace, f"{model_key}:roster", int(data["model_limit"]))
            add_cost(model, namespace, extra_cost)
            add_cost(entry, namespace, adjustment)
        else:
            model = new_selection_entry(entries, namespace, model_key, str(data["name"]), "model")
            add_constraint(model, namespace, f"{model_key}:min", "min", minimum)
            add_constraint(model, namespace, f"{model_key}:max", "max", minimum)
            add_cost(model, namespace, 0)
            additional_key = faction_object_key(faction_key, "model-extra", unit_key)
            additional = new_selection_entry(entries, namespace, additional_key, f"额外{data['name']}", "model")
            add_constraint(additional, namespace, f"{additional_key}:max", "max", maximum - minimum)
            add_cost(additional, namespace, extra_cost)
            add_cost(entry, namespace, int(data["cost"]))
    else:
        add_cost(entry, namespace, int(data["cost"]))

    if data.get("unique"):
        add_constraint(entry, namespace, f"{key}:unique", "max", 1, scope="roster", include_children=True, include_forces=True)
    elif data.get("limit"):
        add_scaled_limit(entry, namespace, key, int(data["limit"]))

    entries = child_container(entry, namespace, "selectionEntries")
    general_id: str | None = None
    bsb_ids: list[str] = []
    if data.get("general"):
        general_key = f"{faction_key}:option:{unit_key}:general"
        general = new_selection_entry(entries, namespace, general_key, "任命为将军", "upgrade")
        general_id = general.get("id")
        add_constraint(general, namespace, f"{general_key}:max", "max", 1)
        add_category_link(general, namespace, f"{general_key}:category", CATEGORIES["general"], category_id("general"))
        add_cost(general, namespace, 0)
    if data.get("bsb") is not None:
        bsb_key = f"{faction_key}:option:{unit_key}:bsb"
        bsb = new_selection_entry(entries, namespace, bsb_key, "军旗手", "upgrade")
        bsb_ids.append(bsb.get("id", ""))
        add_constraint(bsb, namespace, f"{bsb_key}:max", "max", 1)
        add_category_link(bsb, namespace, f"{bsb_key}:category", CATEGORIES["bsb"], category_id("bsb"))
        add_faction_banner_choices(bsb, namespace, faction, bsb_key, 2)
        add_cost(bsb, namespace, int(data["bsb"]))

    option_effects: list[tuple[str, str | None]] = []
    for option_data in data.get("options", []):
        option, tag = add_faction_option(entries, namespace, faction_key, unit_key, option_data, model_id)
        option_effects.append((option.get("id", ""), tag))

    groups = child_container(entry, namespace, "selectionEntryGroups")
    for index, (group_name, minimum, maximum, options) in enumerate(data.get("option_groups", [])):
        group_key = f"{faction_key}:unit:{unit_key}:group:{index}"
        group = sub(groups, namespace, "selectionEntryGroup", id=stable_id(group_key), name=group_name, hidden=False, collective=False, import_="true")
        group.attrib["import"] = group.attrib.pop("import_")
        if minimum:
            add_constraint(group, namespace, f"{group_key}:min", "min", int(minimum), include_children=True)
        if maximum:
            add_constraint(group, namespace, f"{group_key}:max", "max", int(maximum), include_children=True)
        group_entries = sub(group, namespace, "selectionEntries")
        for option_data in options:
            option, tag = add_faction_option(group_entries, namespace, faction_key, unit_key, option_data, model_id)
            option_effects.append((option.get("id", ""), tag))
            if tag == "bsb":
                bsb_ids.append(option.get("id", ""))

    command_data = data.get("command")
    if command_data:
        command = sub(groups, namespace, "selectionEntryGroup", id=stable_id(f"{faction_key}:unit:{unit_key}:command"), name="指挥组", hidden=False, collective=False, import_="true")
        command.attrib["import"] = command.attrib.pop("import_")
        command_entries = sub(command, namespace, "selectionEntries")
        roles = [("队长", 10), ("乐手", 10), ("旗手", 10)] if command_data is True else list(command_data)
        for role, cost in roles:
            role_key = f"{faction_key}:option:{unit_key}:command:{role}"
            upgrade = new_selection_entry(command_entries, namespace, role_key, str(role), "upgrade")
            add_constraint(upgrade, namespace, f"{role_key}:max", "max", 1)
            add_cost(upgrade, namespace, int(cost))
            if role in {"旗手", "方旗骑士"}:
                add_faction_banner_choices(upgrade, namespace, faction, role_key)

    if data.get("mounts"):
        mount_group = sub(groups, namespace, "selectionEntryGroup", id=stable_id(f"{faction_key}:unit:{unit_key}:mounts"), name="坐骑（至多一项）", hidden=False, collective=False, import_="true")
        mount_group.attrib["import"] = mount_group.attrib.pop("import_")
        add_constraint(mount_group, namespace, f"{faction_key}:unit:{unit_key}:mounts:max", "max", 1, include_children=True)
        mounts_by_key = {str(mount["key"]): mount for mount in faction.get("mounts", [])}
        for mount_key, cost, *_rest in data["mounts"]:
            mount = mounts_by_key[str(mount_key)]
            add_entry_link(
                mount_group,
                namespace,
                f"{faction_key}:unit:{unit_key}:mount:{mount_key}",
                str(mount["name"]),
                stable_id(faction_object_key(faction_key, "mount", str(mount_key))),
                "selectionEntry",
                cost=int(cost),
            )

    if data.get("lores"):
        lore_group = sub(groups, namespace, "selectionEntryGroup", id=stable_id(f"{faction_key}:unit:{unit_key}:lores"), name="魔法派系（必须选择一项）", hidden=False, collective=False, import_="true")
        lore_group.attrib["import"] = lore_group.attrib.pop("import_")
        add_constraint(lore_group, namespace, f"{faction_key}:unit:{unit_key}:lores:min", "min", 1, include_children=True)
        add_constraint(lore_group, namespace, f"{faction_key}:unit:{unit_key}:lores:max", "max", 1, include_children=True)
        for lore in data["lores"]:
            add_entry_link(lore_group, namespace, f"{faction_key}:unit:{unit_key}:lore:{lore}", str(lore), stable_id(f"lore:{lore}"), "selectionEntry")

    if data.get("spell_choices"):
        spell_group = sub(groups, namespace, "selectionEntryGroup", id=stable_id(f"{faction_key}:unit:{unit_key}:spells"), name=f"法术（选择{data['spell_count']}项）", hidden=False, collective=False, import_="true")
        spell_group.attrib["import"] = spell_group.attrib.pop("import_")
        add_constraint(spell_group, namespace, f"{faction_key}:unit:{unit_key}:spells:min", "min", int(data["spell_count"]), include_children=True)
        add_constraint(spell_group, namespace, f"{faction_key}:unit:{unit_key}:spells:max", "max", int(data["spell_count"]), include_children=True)
        spell_entries = sub(spell_group, namespace, "selectionEntries")
        for spell in data["spell_choices"]:
            spell_key = f"{faction_key}:spell-choice:{unit_key}:{spell}"
            choice = new_selection_entry(spell_entries, namespace, spell_key, str(spell), "upgrade")
            add_constraint(choice, namespace, f"{spell_key}:max", "max", 1)
            add_cost(choice, namespace, 0)

    if data.get("item_budget") is not None:
        add_faction_item_wrapper(entry, namespace, faction, data, general_id)

    for option_id, tag in option_effects:
        if tag == "per_model_category_special":
            add_category_change(entry, namespace, f"{key}:to-special", option_id, add=["special"], remove=["core"], primary="special")
        elif tag == "per_model_add_hidden_arrows":
            add_category_change(entry, namespace, f"{key}:add-hidden-arrows", option_id, add=["hidden-arrows"])
        elif tag == "per_model_add_clan_thunder":
            add_category_change(entry, namespace, f"{key}:add-clan-thunder", option_id, add=["clan-thunder"])
        elif tag == "add_clan_thunder":
            add_category_change(entry, namespace, f"{key}:add-clan-thunder", option_id, add=["clan-thunder"])

    if general_id and bsb_ids:
        for bsb_id in bsb_ids:
            general = next((node for node in entry.iter() if node.get("id") == general_id), None)
            bsb = next((node for node in entry.iter() if node.get("id") == bsb_id), None)
            if general is not None:
                modifiers = child_container(general, namespace, "modifiers")
                hide = sub(modifiers, namespace, "modifier", type="set", value=True, field="hidden")
                add_condition(hide, namespace, condition_type="atLeast", value=1, field="selections", scope="ancestor", child_id=bsb_id)
            if bsb is not None:
                modifiers = child_container(bsb, namespace, "modifiers")
                hide = sub(modifiers, namespace, "modifier", type="set", value=True, field="hidden")
                add_condition(hide, namespace, condition_type="atLeast", value=1, field="selections", scope="ancestor", child_id=general_id)


def build_faction_catalogue(faction: dict[str, object]) -> None:
    ns = CAT_NS
    ET.register_namespace("", ns)
    faction_key = str(faction["key"])
    root = ET.Element(
        q(ns, "catalogue"),
        {
            "id": stable_id(f"catalogue:{faction_key}"),
            "name": str(faction["name"]),
            "revision": "1",
            "battleScribeVersion": "2.03",
            "authorName": "Custom Rules Data Team",
            "library": "false",
            "gameSystemId": GAME_SYSTEM_ID,
            "gameSystemRevision": "1",
            "type": "catalogue",
        },
    )
    publications = sub(root, ns, "publications")
    publication_id = stable_id(f"publication:{faction_key}")
    sub(
        publications,
        ns,
        "publication",
        id=publication_id,
        name=faction["publication"],
        shortName=faction["short_name"],
        publicationDate=faction["publication_date"],
    )

    shared_rules = sub(root, ns, "sharedRules")
    for rule_key, rule_name, description, page in faction.get("rules", []):
        rule = sub(shared_rules, ns, "rule", id=stable_id(f"faction-rule:{faction_key}:{rule_key}"), name=rule_name, hidden=False, publicationId=publication_id, page=page)
        sub(rule, ns, "description").text = description

    shared_entries = sub(root, ns, "sharedSelectionEntries")
    for mount in faction.get("mounts", []):
        mount_key = str(mount["key"])
        entry = sub(shared_entries, ns, "selectionEntry", id=stable_id(faction_object_key(faction_key, "mount", mount_key)), name=mount["name"], hidden=False, collective=False, type="upgrade", import_="true", publicationId=publication_id, page=mount["page"])
        entry.attrib["import"] = entry.attrib.pop("import_")
        add_profile(entry, ns, f"{faction_key}:mount:{mount_key}:global", "global", str(mount["name"]), dict(zip(PROFILE_TYPES["global"][1], mount["global"])))
        add_profile(entry, ns, f"{faction_key}:mount:{mount_key}:defence", "defence", str(mount["name"]), dict(zip(PROFILE_TYPES["defence"][1], mount["defence"])))
        for index, attack in enumerate(mount["offence"]):
            add_profile(entry, ns, f"{faction_key}:mount:{mount_key}:offence:{index}", "offence", str(attack[0]), dict(zip(PROFILE_TYPES["offence"][1], attack[1:])))
        for category in mount.get("extra_categories", []):
            add_category_link(entry, ns, f"{faction_key}:mount:{mount_key}:category:{category}", CATEGORIES[str(category)], category_id(str(category)))
        if mount.get("unique"):
            add_constraint(entry, ns, f"{faction_key}:mount:{mount_key}:unique", "max", 1, scope="roster", include_children=True, include_forces=True)
        elif mount.get("limit"):
            add_scaled_limit(entry, ns, f"{faction_key}:mount:{mount_key}", int(mount["limit"]))
        add_constraint(entry, ns, f"{faction_key}:mount:{mount_key}:parent", "max", 1)
        add_cost(entry, ns, 0)

    shared_groups = sub(root, ns, "sharedSelectionEntryGroups")
    for kind, items in dict(faction.get("items", {})).items():
        group = sub(shared_groups, ns, "selectionEntryGroup", id=stable_id(f"group:{faction_key}:items:{kind}"), name=f"{faction['name']}：{kind}", hidden=False, collective=False, import_="true")
        group.attrib["import"] = group.attrib.pop("import_")
        item_entries = sub(group, ns, "selectionEntries")
        for item_data in items:
            item_key, item_name, cost, description, page, *limits = item_data
            parent_max = int(limits[0]) if limits else 1
            roster_limit = int(limits[1]) if len(limits) > 1 else 1
            item = sub(item_entries, ns, "selectionEntry", id=stable_id(f"faction-item:{faction_key}:{kind}:{item_key}"), name=item_name, hidden=False, collective=False, import_="true", type="upgrade", publicationId=publication_id, page=page)
            item.attrib["import"] = item.attrib.pop("import_")
            add_constraint(item, ns, f"faction-item:{faction_key}:{kind}:{item_key}:parent", "max", parent_max)
            if roster_limit < 99:
                add_constraint(item, ns, f"faction-item:{faction_key}:{kind}:{item_key}:roster", "max", roster_limit, scope="roster", include_children=True, include_forces=True)
            add_embedded_rule(item, ns, f"faction-item:{faction_key}:{kind}:{item_key}", str(item_name), str(description))
            add_cost(item, ns, int(cost))

    selection_entries = sub(root, ns, "selectionEntries")
    for data in faction["units"]:
        add_faction_unit(selection_entries, ns, faction, data, publication_id)

    local_categories = sub(root, ns, "categoryEntries")
    for pool_key, pool_name, limit in faction.get("shared_pools", []):
        pool = sub(local_categories, ns, "categoryEntry", id=stable_id(f"category:{faction_key}:pool:{pool_key}"), name=pool_name, hidden=True)
        add_scaled_limit(pool, ns, f"category:{faction_key}:pool:{pool_key}", int(limit), scope="force")

    force_entries = sub(root, ns, "forceEntries")
    force = sub(force_entries, ns, "forceEntry", id=stable_id(f"force:{faction_key}:standard"), name="标准军队", hidden=False, publicationId=publication_id, page=faction["force_page"])
    for category_key, category_name, constraint_type, value in faction["categories"]:
        link = add_category_link(force, ns, f"force:{faction_key}:{category_key}", str(category_name), category_id(str(category_key)), primary=True)
        if constraint_type:
            add_constraint(link, ns, f"force:{faction_key}:{category_key}:{constraint_type}-points", str(constraint_type), int(value), field=POINTS, scope="roster", percent=True, include_children=True, include_forces=True)
    for hidden_key in ["general", "bsb", "non_character", "wizard"]:
        add_category_link(force, ns, f"force:{faction_key}:{hidden_key}", CATEGORIES[hidden_key], category_id(hidden_key))
    for pool_key, pool_name, _limit in faction.get("shared_pools", []):
        add_category_link(force, ns, f"force:{faction_key}:pool:{pool_key}", pool_name, stable_id(f"category:{faction_key}:pool:{pool_key}"))
    for rule_key, rule_name, _description, _page in faction.get("rules", []):
        add_info_link(force, ns, f"force:{faction_key}:rule:{rule_key}", rule_name, stable_id(f"faction-rule:{faction_key}:{rule_key}"))

    write_xml(root, ROOT / str(faction["filename"]))


def build_game_system() -> None:
    ns = GST_NS
    ET.register_namespace("", ns)
    root = ET.Element(
        q(ns, "gameSystem"),
        {
            "id": GAME_SYSTEM_ID,
            "name": "第九纪元：中古战锤",
            "revision": "1",
            "battleScribeVersion": "2.03",
            "authorName": "Custom Rules Data Team",
            "type": "gameSystem",
        },
    )
    publications = sub(root, ns, "publications")
    sub(publications, ns, "publication", id=stable_id("publication:core"), name="总规则 2026 beta3", shortName="CR-2026β3", publicationDate="2026-06-26")
    sub(publications, ns, "publication", id=stable_id("publication:arcane"), name="奥法宝典 2026 beta2", shortName="AC-2026β2", publicationDate="2026")
    sub(publications, ns, "publication", id=stable_id("publication:legendary"), name="传奇人物 2026 beta3", shortName="LC-2026β3", publicationDate="2026")

    cost_types = sub(root, ns, "costTypes")
    sub(cost_types, ns, "costType", id=POINTS, name="分", defaultCostLimit=-1, hidden=False)

    profile_types = sub(root, ns, "profileTypes")
    for key, (name, characteristics) in PROFILE_TYPES.items():
        profile_type = sub(profile_types, ns, "profileType", id=profile_type_id(key), name=name)
        rows = sub(profile_type, ns, "characteristicTypes")
        for characteristic in characteristics:
            sub(rows, ns, "characteristicType", id=characteristic_id(key, characteristic), name=characteristic)

    categories = sub(root, ns, "categoryEntries")
    for key, name in CATEGORIES.items():
        category = sub(categories, ns, "categoryEntry", id=category_id(key), name=name, hidden=key in {"general", "bsb", "non_character", "wizard"})
        if key == "general":
            add_constraint(category, ns, "general-min", "min", 1, scope="force", include_children=True)
            add_constraint(category, ns, "general-max", "max", 1, scope="force", include_children=True)
        if key == "non_character":
            add_constraint(category, ns, "non-character-min", "min", 4, scope="force", include_children=False)
        if key == "bsb":
            add_constraint(category, ns, "bsb-max", "max", 1, scope="force", include_children=True)

    shared_rules = sub(root, ns, "sharedRules")
    for key, name, description in CORE_RULES:
        rule = sub(shared_rules, ns, "rule", id=stable_id(f"core-rule:{key}"), name=name, hidden=False, publicationId=stable_id("publication:core"))
        sub(rule, ns, "description").text = description

    shared_profiles = sub(root, ns, "sharedProfiles")
    for key, (name, attack_range, shots, strength, ap, aim, rules) in EQUIPMENT.items():
        profile = sub(shared_profiles, ns, "profile", id=stable_id(f"equipment-profile:{key}"), name=name, hidden=False, typeId=profile_type_id("weapon"), typeName=PROFILE_TYPES["weapon"][0], publicationId=stable_id("publication:core"), page="114-116")
        rows = sub(profile, ns, "characteristics")
        values = {"射程": attack_range, "射数": shots, "力量": strength, "AP": ap, "瞄准": aim, "规则": rules}
        for characteristic in PROFILE_TYPES["weapon"][1]:
            node = sub(rows, ns, "characteristic", name=characteristic, typeId=characteristic_id("weapon", characteristic))
            node.text = values[characteristic]

    shared_entries = sub(root, ns, "sharedSelectionEntries")
    for key, (name, *_rest) in EQUIPMENT.items():
        entry = sub(shared_entries, ns, "selectionEntry", id=stable_id(f"equipment-entry:{key}"), name=name, hidden=False, collective=False, import_=True, type="upgrade")
        entry.attrib["import"] = entry.attrib.pop("import_")
        add_info_link(entry, ns, f"equipment:{key}", name, stable_id(f"equipment-profile:{key}"), "profile")

    shared_groups = sub(root, ns, "sharedSelectionEntryGroups")
    lore_group = sub(shared_groups, ns, "selectionEntryGroup", id=stable_id("group:lores"), name="魔法派系", hidden=False, collective=False, import_=True)
    lore_group.attrib["import"] = lore_group.attrib.pop("import_")
    lore_entries = sub(lore_group, ns, "selectionEntries")
    for lore in LORES:
        entry = sub(lore_entries, ns, "selectionEntry", id=stable_id(f"lore:{lore}"), name=lore, hidden=False, collective=False, import_=True, type="upgrade", publicationId=stable_id("publication:arcane"))
        entry.attrib["import"] = entry.attrib.pop("import_")
        add_constraint(entry, ns, f"lore:{lore}:max", "max", 1)
        add_cost(entry, ns, 0)

    for kind, items in COMMON_ITEMS.items():
        group = sub(shared_groups, ns, "selectionEntryGroup", id=stable_id(f"group:common-items:{kind}"), name={"weapon": "通用武器附魔", "armour": "通用护甲附魔", "banner": "通用旗帜附魔", "curio": "通用魔法奇物"}[kind], hidden=False, collective=False, import_=True)
        group.attrib["import"] = group.attrib.pop("import_")
        entries = sub(group, ns, "selectionEntries")
        for key, name, cost, limit, description in items:
            item = sub(entries, ns, "selectionEntry", id=stable_id(f"common-item:{key}"), name=name, hidden=False, collective=False, import_=True, type="upgrade", publicationId=stable_id("publication:arcane"), page={"weapon": 23, "armour": 24, "banner": 25, "curio": "26-27"}[kind])
            item.attrib["import"] = item.attrib.pop("import_")
            add_constraint(item, ns, f"common-item:{key}:parent", "max", 1)
            add_constraint(item, ns, f"common-item:{key}:roster", "max", limit, scope="roster", include_children=True, include_forces=True)
            add_embedded_rule(item, ns, f"common-item:{key}", name, description)
            add_cost(item, ns, cost)

    write_xml(root, ROOT / "第九纪元：中古战锤.gst")


def build_catalogue() -> None:
    ns = CAT_NS
    ET.register_namespace("", ns)
    root = ET.Element(
        q(ns, "catalogue"),
        {
            "id": stable_id("catalogue:dark-elves"),
            "name": "黑暗精灵",
            "revision": "1",
            "battleScribeVersion": "2.03",
            "authorName": "Custom Rules Data Team",
            "library": "false",
            "gameSystemId": GAME_SYSTEM_ID,
            "gameSystemRevision": "1",
            "type": "catalogue",
        },
    )
    publications = sub(root, ns, "publications")
    de_publication = stable_id("publication:dark-elves")
    legendary_publication = stable_id("publication:legendary")
    sub(publications, ns, "publication", id=de_publication, name="黑暗精灵种族规则 2026 beta1", shortName="DE-2026β1", publicationDate="2026-05-01")

    shared_rules = sub(root, ns, "sharedRules")
    for key, (name, description) in DE_RULES.items():
        rule = sub(shared_rules, ns, "rule", id=stable_id(f"de-rule:{key}"), name=name, hidden=False, publicationId=de_publication, page="2-3")
        sub(rule, ns, "description").text = description

    shared_entries = sub(root, ns, "sharedSelectionEntries")
    for key, mount in MOUNTS.items():
        entry = sub(shared_entries, ns, "selectionEntry", id=stable_id(f"mount:{key}"), name=mount["name"], hidden=False, collective=False, type="upgrade", import_="true", publicationId=de_publication, page="11-12")
        entry.attrib["import"] = entry.attrib.pop("import_")
        global_values = mount["global"]
        add_profile(entry, ns, f"mount:{key}:global", "global", mount["name"], dict(zip(PROFILE_TYPES["global"][1], global_values)))
        add_profile(entry, ns, f"mount:{key}:defence", "defence", mount["name"], dict(zip(PROFILE_TYPES["defence"][1], mount["defence"])))
        for index, attack in enumerate(mount["offence"]):
            add_profile(entry, ns, f"mount:{key}:offence:{index}", "offence", attack[0], dict(zip(PROFILE_TYPES["offence"][1], attack[1:])))
        if mount.get("menagerie"):
            add_category_link(entry, ns, f"mount:{key}:menagerie", CATEGORIES["menagerie"], category_id("menagerie"), primary=False)
        if mount.get("limit"):
            add_scaled_limit(entry, ns, f"mount:{key}", int(mount["limit"]))
        add_constraint(entry, ns, f"mount:{key}:parent", "max", 1)
        add_cost(entry, ns, 0)

    shared_groups = sub(root, ns, "sharedSelectionEntryGroups")
    for kind, items in DE_ITEMS.items():
        group = sub(shared_groups, ns, "selectionEntryGroup", id=stable_id(f"group:de-items:{kind}"), name={"weapon": "黑暗精灵武器附魔", "armour": "黑暗精灵护甲附魔", "banner": "黑暗精灵旗帜附魔", "curio": "黑暗精灵魔法奇物"}[kind], hidden=False, collective=False, import_="true")
        group.attrib["import"] = group.attrib.pop("import_")
        entries = sub(group, ns, "selectionEntries")
        for key, name, cost, limit, description in items:
            item = sub(entries, ns, "selectionEntry", id=stable_id(f"de-item:{key}"), name=name, hidden=False, collective=False, import_="true", type="upgrade", publicationId=de_publication, page=5)
            item.attrib["import"] = item.attrib.pop("import_")
            add_constraint(item, ns, f"de-item:{key}:parent", "max", 1)
            add_constraint(item, ns, f"de-item:{key}:roster", "max", limit, scope="roster", include_children=True, include_forces=True)
            add_embedded_rule(item, ns, f"de-item:{key}", name, description)
            add_cost(item, ns, cost)

    title_group = sub(shared_groups, ns, "selectionEntryGroup", id=stable_id("group:de-titles"), name="异名", hidden=False, collective=False, import_="true")
    title_group.attrib["import"] = title_group.attrib.pop("import_")
    title_entries = sub(title_group, ns, "selectionEntries")
    for key, name, cost, limit, description in DE_TITLES:
        title = sub(title_entries, ns, "selectionEntry", id=stable_id(f"de-title:{key}"), name=name, hidden=False, collective=False, import_="true", type="upgrade", publicationId=de_publication, page=4)
        title.attrib["import"] = title.attrib.pop("import_")
        add_constraint(title, ns, f"de-title:{key}:parent", "max", 1)
        if limit != 99:
            add_constraint(title, ns, f"de-title:{key}:roster", "max", limit, scope="roster", include_children=True, include_forces=True)
        add_embedded_rule(title, ns, f"de-title:{key}", name, description)
        add_cost(title, ns, cost)

    selection_entries = sub(root, ns, "selectionEntries")
    for unit in UNITS:
        add_unit(selection_entries, ns, unit, de_publication, legendary=False)
    for unit in LEGENDARY_UNITS:
        add_unit(selection_entries, ns, unit, legendary_publication, legendary=True)

    local_categories = sub(root, ns, "categoryEntries")
    pool = sub(local_categories, ns, "categoryEntry", id=stable_id("category:beast-packs"), name="雷兽群与潜兽群共享池", hidden=True)
    add_scaled_limit(pool, ns, "category:beast-packs", 3, scope="force")

    force_entries = sub(root, ns, "forceEntries")
    force = sub(force_entries, ns, "forceEntry", id=stable_id("force:dark-elves-standard"), name="标准军队", hidden=False, publicationId=de_publication, page=6)
    for key in ["characters", "core", "special", "raiders", "menagerie", "legendary", "general", "bsb", "non_character", "wizard"]:
        link = add_category_link(force, ns, f"force:{key}", CATEGORIES[key], category_id(key), primary=key in {"characters", "core", "special", "raiders", "menagerie", "legendary"})
        if key == "characters":
            add_constraint(link, ns, "force:characters:max-points", "max", 40, field=POINTS, scope="roster", percent=True, include_children=True, include_forces=True)
        elif key == "core":
            add_constraint(link, ns, "force:core:min-points", "min", 25, field=POINTS, scope="roster", percent=True, include_children=True, include_forces=True)
        elif key == "raiders":
            add_constraint(link, ns, "force:raiders:max-points", "max", 20, field=POINTS, scope="roster", percent=True, include_children=True, include_forces=True)
        elif key == "menagerie":
            add_constraint(link, ns, "force:menagerie:max-points", "max", 30, field=POINTS, scope="roster", percent=True, include_children=True, include_forces=True)
    add_category_link(force, ns, "force:beast-packs", "雷兽群与潜兽群共享池", stable_id("category:beast-packs"), primary=False)

    write_xml(root, ROOT / "黑暗精灵.cat")


def main() -> None:
    build_game_system()
    build_catalogue()
    for faction in FACTIONS:
        build_faction_catalogue(faction)


if __name__ == "__main__":
    main()
