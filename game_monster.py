from game_creature import Creature


class Monster(Creature):  # 怪物类
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.kind = dictionary['kind']  # 怪物种类

    def patrol(self, game_map):  # 怪物巡逻
        pass
