class Box:  # 宝箱类
    def __init__(self, things, setting):
        self.things = things  # 宝箱内的物品对象列表
        self.things_num = len(things)  # 宝箱内物品数量
        self.selecting = 0  # 宝箱选中物品标号
        self.space = setting.bag_space  # 宝箱空间
        self.image = self.load_image()  # 宝箱基本图像，如空格，说明、拾取按钮等

    def load_image(self):  # 加载图像
        pass

    def draw(self):  # 绘制宝箱
        pass

    def select(self, event):  # 选中宝箱物品
        pass

    def explain(self):  # 对宝箱选中物品展开说明
        pass

    def pick(self):  # 拾取宝箱选中物品
        pass

    def move(self):  # 移动宝箱物品
        pass
