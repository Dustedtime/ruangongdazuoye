import json
import os


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


class Key:  # 钥匙类
    def __init__(self):
        self.sell_price = None
        self.buy_price = None
        self.load_data()

    def load_data(self):  # 初始化
        with open(os.path.join('page', 'page4', 'item', '1.json'), 'r') as f:
            dictionary = json.load(f)
        self.buy_price = dictionary["buy_price"]
        self.sell_price = dictionary["sell_price"]


class LifePotion:  # 生命药水类
    def __init__(self, dictionary):
        self.recovery = dictionary['recovery']  # 恢复量
        self.image = dictionary['image']  # 图像

    def use(self):  # 使用
        pass
