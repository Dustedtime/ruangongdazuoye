import json
import os

import pygame

from game_equipment import Weapon


class Bag:  # 背包类
    def __init__(self, setting, archival, width, rect):  # 初始化背包，width为人物大小，rect为人物坐标，用于初始化武器
        self.things = []  # 背包内的物品对象列表
        self.things_kind = None  # 背包各种物品依次的种类
        self.things_num = 0  # 背包内物品数量
        self.equip_wear = 0  # 装备中的物品标号
        self.selecting = 0  # 背包选中物品标号
        self.space = setting.bag_space  # 背包空间
        self.images = []  # 背包图像
        self.item_edge = 0  # 背包格子框架宽度
        self.item_width = 0  # 背包格子内宽度
        self.things_images = []  # 背包中物品图像
        self.things_rects = []  # 背包各个格子中物品图像位置
        self.load_data(setting.screen_width, setting.screen_height, archival, width, rect)  # 背包基本图像，如空格，说明、使用按钮等

    def load_data(self, screen_width, screen_height, archival, width, rect):  # 加载背包信息
        # 加载背包基本图像
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
        # 实例化背包内的物品
        with open(os.path.join('page', archival, 'page4', 'bag', 'bag_data.json'), 'r') as f:
            data = json.load(f)
        self.things_num = len(data['things'])
        self.selecting = data['selecting']
        self.equip_wear = data['equip_wear']
        self.things_kind = data['things']
        self.item_edge = data['item_edge']
        self.item_width = data['item_width']
        for thing in data['things']:
            if thing[0] == 1:  # 武器
                self.things.append(Weapon(thing[1], thing[2], width, rect))
        # 加载物品在背包内显示的图像信息
        bag_width = self.images[1][2][0] - self.images[1][1][0]  # 游戏中加载的背包栏（不含标题）的像素宽度
        bag_height = self.images[1][2][1] - self.images[1][1][1]  # 游戏中加载的背包栏（不含标题）的像素高度
        bag_width_true = self.item_width * 5 + self.item_edge * 6  # 原图像背包栏（不含标题）的像素宽度
        bag_height_true = self.item_width * 7 + self.item_edge * 8  # 原图像背包栏（不含标题）的像素高度
        for i in range(35):  # 计算背包内各个格子的物品图像的位置
            row = i // 5
            col = i % 5
            x_left = self.item_edge + col * (self.item_edge + self.item_width)
            x_right = x_left + self.item_width
            dx_left = x_left * bag_width / bag_width_true
            dx_right = x_right * bag_width / bag_width_true
            rect_left = self.images[1][1][0] + dx_left
            rect_right = self.images[1][1][0] + dx_right
            y_top = self.item_edge + row * (self.item_edge + self.item_width)
            y_bottom = y_top + self.item_width
            dy_top = y_top * bag_height / bag_height_true
            dy_bottom = y_bottom * bag_height / bag_height_true
            rect_top = self.images[1][1][1] + dy_top
            rect_bottom = self.images[1][1][1] + dy_bottom
            self.things_rects.append([(rect_left, rect_top), (rect_right, rect_bottom)])
        picture_size = (self.things_rects[0][1][0] - self.things_rects[0][0][0],
                        self.things_rects[0][1][1] - self.things_rects[0][0][1])  # 物品图像尺寸
        path = os.path.join('image', 'page4', 'thing')
        for i in range(self.things_num):
            path1 = path
            for num in self.things_kind[i][:-1]:
                path1 = os.path.join(path1, str(num))
            path1 = os.path.join(path1, str(self.things_kind[i][-1]) + '.bmp')
            image = pygame.image.load(path1)
            self.things_images.append(pygame.transform.scale(image, picture_size))

    def draw(self, screen):  # 绘制背包
        for image in self.images:
            screen.blit(image[0], image[1])
        for i in range(self.things_num):
            screen.blit(self.things_images[i], self.things_rects[i][0])

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
