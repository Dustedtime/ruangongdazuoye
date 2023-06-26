class Thing:  # 物件基类
    def __init__(self, dictionary):
        self.kind = dictionary['kind']  # 物件种类
        self.image = dictionary['image']  # 物件图像
        self.position = dictionary['position']  # 物件位置
        self.active = dictionary['active']  # 是否活跃（是否绘制）

    def draw(self, screen):  # 绘制物件
        screen.blit(self.image, self.position)

    def sell(self):  # 出售物件
        pass

    def load_data(self):  # 加载数据
        pass


class Weapon(Thing):  # 武器类
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.strength = dictionary['strength']  # 攻击力

    def attack(self):  # 攻击
        pass

    def equip(self):  # 装备
        pass


class Shield(Thing):  # 盾牌类
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.defence = dictionary['defence']  # 防御力

    def equip(self):  # 装备
        pass


class Jewel(Thing):  # 宝石类
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.strength = dictionary['strength']
        self.defence = dictionary['defence']

    def equip(self):  # 装备
        pass


class Key(Thing):  # 钥匙类
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.kind = dictionary['kind']  # 钥匙种类

    def use(self):  # 使用
        pass


class LifePotion:  # 生命药水类
    def __init__(self, dictionary):
        self.recovery = dictionary['recovery']  # 恢复量
        self.image = dictionary['image']  # 图像

    def use(self):  # 使用
        pass
