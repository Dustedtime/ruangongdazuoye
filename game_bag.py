class Bag:  # 背包类
    def __init__(self, things, setting):
        self.things = things  # 背包内的物品对象列表
        self.things_num = len(things)  # 背包内物品数量
        self.selecting = 0  # 背包选中物品标号
        self.space = setting.bag_space  # 背包空间
        self.image = self.load_image()  # 背包基本图像，如空格，说明、使用按钮等

    def load_image(self):  # 加载图像
        pass

    def draw(self):  # 绘制背包
        pass

    def select(self, event):  # 选中背包物品
        pass

    def explain(self):  # 对背包选中物品展开说明
        pass

    def throw(self):  # 丢弃背包选中物品
        pass

    def move(self):  # 移动背包物品
        pass

    def sell(self):  # 出售背包物品
        pass
