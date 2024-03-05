from diceutils.charactors import Character, Template, Attribute, AttributeGroup, manager
from typing import Tuple

import random


attributes = [
    AttributeGroup(
        "meta",
        "元属性",
        [
            Attribute("name", str, ["姓名", "名字", "名称"]),
            Attribute("sex", str, ["性别"]),
            Attribute("age", int, ["年龄"]),
        ],
    ),
    AttributeGroup(
        "basic",
        "基础属性",
        [
            Attribute("str", int, ["力量", "攻击", "攻击力"]),
            Attribute("con", int, ["体质"]),
            Attribute("siz", int, ["体型"]),
            Attribute("dex", int, ["敏捷"]),
            Attribute("app", int, ["外貌"]),
            Attribute("int", int, ["智力", "灵感"]),
            Attribute("pow", int, ["意志", "精神"]),
            Attribute("edu", int, ["教育"]),
            Attribute("luc", int, ["幸运", "命运"]),
            Attribute("db", str, ["伤害加成"]),
            Attribute("mov", int, ["速度", "移动速度"]),
            Attribute("san", int, ["理智", "精神状态", "san值"]),
            Attribute("hp", int, ["生命"]),
            Attribute("mhp", int, ["生命上限", "最大生命"]),
        ],
    ),
]
manager.add_template("coc", attributes)


def mov(charactor: Character):
    move_value = 8
    age = charactor.get("age")
    str = charactor.get("str")
    siz = charactor.get("siz")
    dex = charactor.get("dex")

    if age >= 40:
        move_value -= min(5, (age - 30) // 10)

    if str < siz and dex < siz:
        return move_value - 1
    elif str > siz and dex > siz:
        return move_value + 1
    else:
        return move_value


def db(charactor: Character) -> str:
    _db_dict = {
        64: "-2",
        84: "-1",
        124: "+0",
        164: "+1d4",
        204: "+1d6",
        284: "+2d6",
        364: "+3d6",
        444: "+4d6",
        524: "+5d6",
    }
    if not charactor.get("str") or not charactor.get("con"):
        return "+0"
    _db_count = charactor.get("str") + charactor.get("con")
    for max_value, db in _db_dict.items():
        if _db_count < max_value:
            return str(db)
    return "+0"


def rollcount(charactor: Character) -> Tuple[int, int]:
    summary = (
        (charactor.get("str") or 0)
        + (charactor.get("con") or 0)
        + (charactor.get("siz") or 0)
        + (charactor.get("dex") or 0)
        + (charactor.get("app") or 0)
        + (charactor.get("int") or 0)
        + (charactor.get("pow") or 0)
        + (charactor.get("edu") or 0)
    )
    return summary, summary + (charactor.get("luc") or 0)


def initialized(charactor: Character) -> Character:
    charactor.set("name", "无名调查员")
    charactor.set("age", 20)
    charactor.set("sex", random.choice(["男", "女"]))
    charactor.set("str", "3d6*5")
    charactor.set("con", "3d6*5")
    charactor.set("siz", "(2d6+6)*5")
    charactor.set("dex", "3d6*5")
    charactor.set("app", "3d6*5")
    charactor.set("int", "(2d6+6)*5")
    charactor.set("pow", "3d6*5")
    charactor.set("edu", "(2d6+6)*5")
    charactor.set("luc", "3d6*5")
    charactor.set("san", charactor.get("pow"))
    charactor.set("hp", (charactor.get("con") + charactor.get("siz")) // 10)
    charactor.set("mhp", charactor.get("hp"))
    charactor.set("mov", mov(charactor))
    charactor.set("db", db(charactor))

    return charactor


# def edu_up(self) -> str:
#     edu_check = random.randint(1, 100)
#     if edu_check > self.edu:
#         edu_en = random.randint(1, 10)
#         self.edu += edu_en
#     else:
#         return "教育成长检定D100=%d, 小于%d, 无增长。" % (edu_check, self.edu)
#     if self.edu > 99:
#         self.edu = 99
#         return "教育成长检定D100=%d, 成长1D10=%d, 成长到了最高值99！" % (
#             edu_check,
#             edu_en,
#         )
#     else:
#         return "教育成长检定D100=%d, 成长1D10=%d, 成长到了%d" % (
#             edu_check,
#             edu_en,
#             self.edu,
#         )

# def edu_ups(self, times) -> str:
#     r = ""
#     for _ in range(times):
#         r += self.edu_up()
#     return r

# def sum_down(self, sum) -> str:
#     if self.str + self.con + self.dex - 45 < sum:
#         self.str = 15
#         self.con = 15
#         self.dex = 15
#     else:
#         str_lost = random.randint(0, min(sum, self.str - 15))
#         while sum - str_lost > self.con + self.dex - 30:
#             str_lost = random.randint(0, min(sum, self.str - 15))
#         self.str -= str_lost
#         sum -= str_lost
#         con_lost = random.randint(0, min(sum, self.con - 15))
#         while sum - con_lost > self.dex - 15:
#             con_lost = random.randint(0, min(sum, self.con - 15))
#         self.con -= con_lost
#         sum -= con_lost
#         self.dex -= sum
#     return
