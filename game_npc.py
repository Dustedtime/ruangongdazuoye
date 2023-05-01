class NPC:
    def __init__(self, dictionary):
        self.kind = dictionary['kind']  # 种类
        self.image = dictionary['image']  # 图像
        self.position = dictionary['position']  # 位置
        self.status = dictionary['status']  # 状态，决定对话时显示哪些内容

    def talk(self):  # 与角色交谈
        pass

    def draw(self, screen):  # 绘制图像
        screen.blit(self.image, self.position)

    def load_data(self):  # 加载数据
        pass
