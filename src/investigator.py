from diceutils.charactors import Character, Template, Attribute, AttributeGroup
from diceutils.charactors import manager

import random

build_dict = {64: -2, 84: -1, 124: 0, 164: 1, 204: 2, 284: 3, 364: 4, 444: 5, 524: 6}
db_dict = {
    -2: "-2",
    -1: "-1",
    0: "0",
    1: "1d4",
    2: "1d6",
    3: "2d6",
    4: "3d6",
    5: "4d6",
    6: "5d6",
}

attributes = [
    AttributeGroup(
        "meta",
        "元属性",
        [
            Attribute(
                "name",
                str,
                ["姓名", "名字", "名称"],
            ),
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
            Attribute("san", int, ["理智", "精神状态", "san值"]),
            Attribute("mov", int, ["速度", "移动速度"]),
            Attribute("hp", int, ["生命"]),
            Attribute("mhp", int, ["生命上限", "最大生命"]),
        ],
    ),
]
manager.add_template("coc", attributes)


class Investigator(Character):
    def __init__(self) -> None:
        super().__init__(Template("coc", attributes))
        self.set("name", "无名调查员")
        self.set("age", 20)
        self.set("sex", "女")
        self.set("str", "3d6*5")
        self.set("con", "3d6*5")
        self.set("siz", "(2d6+6)*5")
        self.set("dex", "3d6*5")
        self.set("app", "3d6*5")
        self.set("int", "(2d6+6)*5")
        self.set("pow", "3d6*5")
        self.set("edu", "(2d6+6)*5")
        self.set("luc", "3d6*5")
        self.set("san", self.get("pow"))
        self.set("hp", (self.get("con") + self.get("siz")) // 10)
        self.set("mhp", self.get("hp"))

    def body_build(self) -> int:
        build = self.str + self.con
        for i, j in build_dict.items():
            if build <= i:
                return j
        return

    def db(self) -> str:
        return db_dict[self.body_build()]

    def lp_max(self) -> int:
        return (self.con + self.siz) // 10

    def mov(self) -> int:
        r = 8
        age = self.get("age")
        if age >= 80:
            r -= 5
        elif age >= 70:
            r -= 4
        elif age >= 60:
            r -= 3
        elif age >= 50:
            r -= 2
        elif age >= 40:
            r -= 1
        if self.get("str") < self.get("siz") and self.get("dex") < self.get("siz"):
            return r - 1
        elif self.str > self.siz and self.dex > self.siz:
            return r + 1
        else:
            return r

    def edu_up(self) -> str:
        edu_check = random.randint(1, 100)
        if edu_check > self.edu:
            edu_en = random.randint(1, 10)
            self.edu += edu_en
        else:
            return "教育成长检定D100=%d, 小于%d, 无增长。" % (edu_check, self.edu)
        if self.edu > 99:
            self.edu = 99
            return "教育成长检定D100=%d, 成长1D10=%d, 成长到了最高值99！" % (
                edu_check,
                edu_en,
            )
        else:
            return "教育成长检定D100=%d, 成长1D10=%d, 成长到了%d" % (
                edu_check,
                edu_en,
                self.edu,
            )

    def edu_ups(self, times) -> str:
        r = ""
        for _ in range(times):
            r += self.edu_up()
        return r

    def sum_down(self, sum) -> str:
        if self.str + self.con + self.dex - 45 < sum:
            self.str = 15
            self.con = 15
            self.dex = 15
        else:
            str_lost = random.randint(0, min(sum, self.str - 15))
            while sum - str_lost > self.con + self.dex - 30:
                str_lost = random.randint(0, min(sum, self.str - 15))
            self.str -= str_lost
            sum -= str_lost
            con_lost = random.randint(0, min(sum, self.con - 15))
            while sum - con_lost > self.dex - 15:
                con_lost = random.randint(0, min(sum, self.con - 15))
            self.con -= con_lost
            sum -= con_lost
            self.dex -= sum
        return

    def rollcount(self) -> tuple:
        return (self.__count(), self.__count() + self.get("luc"))

    def __count(self):
        return 0
