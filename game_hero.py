from game_creature import Creature


class Hero(Creature):  # 角色类
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.level = dictionary['level']  # 等级
        self.max_health = dictionary['max_health']  # 最大生命值
        self.shield = dictionary['shield']  # 盾牌
        self.jewel = dictionary['jewel']  # 宝石
        self.weapon = dictionary['weapon']  # 武器
        self.bag = dictionary['bag']  # 背包

    def defense(self, status, kind):  # 防御，kind只有两种值：-1和1，-1表示取消防御，1表示开始防御
        self.defence += kind * status * self.shield.defence  # 修改防御力

    def stairs(self, game_map):  # 上下楼梯
        pass

    def talk(self, npc):  # 与npc交谈
        pass

    def door(self, game_map):  # 开门
        pass
