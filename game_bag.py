import json
import os

import pygame


class Bag:  # 背包类
    def __init__(self, setting):
        self.things = []  # 背包内的物品对象列表
        self.things_num = 0  # 背包内物品数量
        self.selecting = 0  # 背包选中物品标号
        self.space = setting.bag_space  # 背包空间
        self.images = []
        self.load_image(setting.screen_width, setting.screen_height)  # 背包基本图像，如空格，说明、使用按钮等

    def load_image(self, screen_width, screen_height):  # 加载背包栏图像
        with open(os.path.join('page', 'page4', 'bag.json'), 'r') as f:
            images = json.load(f)
        for image in images:
            path = ''
            for directory in image[0]:
                path = os.path.join(path, directory)
            size = (screen_width * image[2][0], screen_height * image[2][1])  # 图像大小
            img = pygame.transform.scale(pygame.image.load(path), size)  # 加载图像并转换大小
            img_left_top = (screen_width * image[1][0], screen_height * image[1][1])
            img_right_bottom = (img_left_top[0] + size[0], img_left_top[1] + size[1])
            self.images.append([img, img_left_top, img_right_bottom])  # 将图像及相关信息存入列表

    def draw(self, screen):  # 绘制背包
        for image in self.images:
            screen.blit(image[0], image[1])

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
