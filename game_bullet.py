class Bullet:
    def __init__(self, position, direction, strength, kind):
        self.position = position  # 位置
        self.direction = direction  # 方向
        self.strength = strength  # 攻击力
        self.kind = kind  # 种类
        self.image = self.load_image()
        self.speed = self.load_speed()

    def load_image(self):  # 根据种类读取文档信息获取子弹图像
        pass

    def load_speed(self):  # 根据种类读取文档信息获取子弹速度
        pass

    def move(self, game_map):  # 根据子弹属性以及地图进行子弹移动
        pass

    def draw(self, screen):  # 根据子弹种类绘制子弹
        pass
