import json
import os

import pygame

from game_equipment import Weapon


class Bag:  # 背包类
    def __init__(self, setting, archival, width, rect):  # 初始化背包，width为人物大小，rect为人物坐标，用于初始化武器
        self.space = setting.bag_space  # 背包空间大小
        self.things_num = 0  # 背包内物品数量
        self.things = []  # 背包内的物品对象列表
        self.things_kind = None  # 背包各种物品依次的种类
        self.things_images = []  # 背包中物品图像
        self.things_rects = []  # 背包各个格子中物品图像位置

        self.equip_wear = []  # 装备中的物品标号
        self.equip_image = []  # 装备中图标
        self.selecting = 0  # 背包选中物品标号
        self.selecting_image = []  # 背包选中物品时的边框图像

        self.showing = -1  # 是否正在查看物品详细信息的标志
        self.show_image_size = ()  # 物品详细信息界面的物品图像大小
        self.background = []  # 物品详细信息查看的背景图
        self.show_image = []  # 详细信息中的物品图像
        self.show_words = []  # 详细信息中的物品文字描述等
        self.show_click_word = None  # 详细信息界面可以点击的按钮的文本设置属性

        self.images = []  # 背包基本图像
        self.item_edge = 0  # 原图像背包格子框架宽度
        self.item_width = 0  # 原图像背包格子内宽度加框架宽度
        self.bag_width_true = 0  # 原图像背包栏（不含标题）的像素宽度
        self.bag_height_true = 0  # 原图像背包栏（不含标题）的像素高度
        self.bag_width = 0  # 游戏中加载的背包栏（不含标题）的像素宽度
        self.bag_height = 0  # 游戏中加载的背包栏（不含标题）的像素高度

        self.load_data(setting.screen_width, setting.screen_height, archival, width, rect)  # 背包基本图像，如空格，说明、使用按钮等

    def load_data(self, screen_width, screen_height, archival, hero_size, hero_rect):  # 加载背包信息
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
        # 初始化背包属性
        with open(os.path.join('page', archival, 'page4', 'bag', 'bag_data.json'), 'r') as f:
            data = json.load(f)
        self.things_num = len(data['things'])
        self.selecting = data['selecting']
        self.equip_wear = data['equip_wear']
        self.things_kind = data['things']
        self.item_edge = data['item_edge']
        self.item_width = data['item_width']
        self.bag_width_true = self.item_width * 5 + self.item_edge
        self.bag_height_true = self.item_width * 7 + self.item_edge
        self.bag_width = self.images[1][2][0] - self.images[1][1][0]
        self.bag_height = self.images[1][2][1] - self.images[1][1][1]
        # 加载物品在背包内显示的图像信息
        for i in range(35):  # 计算背包内各个格子的物品图像的位置
            row = i // 5
            col = i % 5
            x_left = col * self.item_width + self.item_edge
            x_right = (col + 1) * self.item_width
            rect_left = self.images[1][1][0] + x_left * self.bag_width / self.bag_width_true
            rect_right = self.images[1][1][0] + x_right * self.bag_width / self.bag_width_true
            y_top = row * self.item_width + self.item_edge
            y_bottom = (row + 1) * self.item_width
            rect_top = self.images[1][1][1] + y_top * self.bag_height / self.bag_height_true
            rect_bottom = self.images[1][1][1] + y_bottom * self.bag_height / self.bag_height_true
            self.things_rects.append([(rect_left, rect_top), (rect_right, rect_bottom)])
        size1 = ((self.item_width - self.item_edge) * self.bag_width / self.bag_width_true,
                 (self.item_width - self.item_edge) * self.bag_height / self.bag_height_true)
        path = os.path.join('image', 'page4', 'thing')
        for i in range(self.things_num):
            path1 = path
            if self.things_kind[i]:
                for num in self.things_kind[i][:-1]:
                    path1 = os.path.join(path1, str(num))
                path1 = os.path.join(path1, str(self.things_kind[i][-1]) + '.bmp')
                image = pygame.image.load(path1)
                self.things_images.append(pygame.transform.scale(image, size1))
            else:
                self.things_images.append(None)
        # 加载装备被穿戴图标
        path = ''
        for directory in data['equip_image']:
            path = os.path.join(path, directory)
        image1 = pygame.image.load(path)  # 武器被穿戴图标
        image2 = pygame.image.load(path)  # 盾牌被穿戴图标
        image1 = pygame.transform.scale(image1, size1)
        image2 = pygame.transform.scale(image2, size1)
        self.equip_image.append([image1])
        self.equip_image.append([image2])
        for i in range(len(self.equip_image)):
            if self.equip_wear[i] >= 0:
                self.equip_image[i].append(
                    (self.things_rects[self.equip_wear[i]][0][0], self.things_rects[self.equip_wear[i]][0][1]))
            else:
                self.equip_image[i].append(None)
        # 加载背包物品被选中图标
        path = ''
        for directory in data['selecting_image']:
            path = os.path.join(path, directory)
        image = pygame.image.load(path)
        size = ((self.item_edge + self.item_width) * self.bag_width / self.bag_width_true,
                (self.item_edge + self.item_width) * self.bag_height / self.bag_height_true)
        self.selecting_image.append(pygame.transform.scale(image, size))
        self.selecting_image.append(None)
        if self.selecting >= 0:
            row = self.selecting // 5
            col = self.selecting % 5
            rect = self.selecting_image[0].get_rect()
            rect.x = self.images[1][1][0] + (self.item_width * col) * self.bag_width / self.bag_width_true
            rect.y = self.images[1][1][1] + (self.item_width * row) * self.bag_height / self.bag_height_true
            self.selecting_image[1] = rect
        # 加载物品详细信息查看的图像信息
        path = ''
        for directory in data['background'][0]:
            path = os.path.join(path, directory)
        size = (data['background'][2][0] * screen_width, data['background'][2][1] * screen_height)
        image = pygame.image.load(path)
        self.background.append(pygame.transform.scale(image, size))
        self.background.append((data['background'][1][0] * screen_width, data['background'][1][1] * screen_height))
        self.background.append((self.background[1][0] + size[0], self.background[1][1] + size[1]))
        self.show_image.append(None)
        size = data['show_image'][1] * screen_height
        self.show_image_size = (size, size)
        self.show_image.append(
            (data['show_image'][0][0] * screen_width - size / 2, data['show_image'][0][1] * screen_height))
        # 实例化背包内的物品
        for thing in data['things']:
            if not thing:
                self.things.append(None)
            elif thing[0] == 1:  # 武器
                self.things.append(Weapon(thing[1], thing[2], hero_size, hero_rect))

    def change_weapon_wear(self, pos):  # 更换穿戴中武器图标位置
        if pos == self.equip_wear[0]:
            return
        self.equip_wear[0] = pos
        if pos < 0:
            self.equip_image[0][1] = None
        else:
            self.equip_image[0][1] = (self.things_rects[pos][0][0], self.things_rects[pos][0][1])

    def click_select(self, pos, screen_width, screen_height):  # 选中背包物品
        selecting = -1
        for i in range(self.space):
            if self.things_rects[i][0][0] <= pos[0] < self.things_rects[i][1][0] and self.things_rects[i][0][1] <= \
                    pos[1] < self.things_rects[i][1][1]:
                selecting = i
                break
        if selecting < 0:
            self.selecting = -1
        elif self.selecting == selecting:  # 展示详细信息
            if self.showing != self.selecting and self.things_kind[self.selecting]:
                self.explain(screen_width, screen_height)
        else:  # 更新选中边框位置
            self.selecting = selecting
            row = selecting // 5
            col = selecting % 5
            x = col * self.item_width * self.bag_width / self.bag_width_true + self.images[1][1][0]
            y = row * self.item_width * self.bag_height / self.bag_height_true + self.images[1][1][1]
            self.selecting_image[1] = (x, y)

    def draw(self, screen):  # 绘制背包
        for image in self.images:
            screen.blit(image[0], image[1])
        for i in range(self.things_num):
            if self.things_images[i]:
                screen.blit(self.things_images[i], self.things_rects[i][0])
        if self.selecting >= 0:
            screen.blit(self.selecting_image[0], self.selecting_image[1])
        for equip in self.equip_image:
            if equip[1]:
                screen.blit(equip[0], equip[1])
        if self.showing >= 0:
            screen.blit(self.background[0], self.background[1])
            screen.blit(self.show_image[0], self.show_image[1])
            for word in self.show_words:
                screen.blit(word[0], word[1])

    def explain(self, screen_width, screen_height):  # 对背包选中物品展开说明
        self.show_words = []
        # 查看的物品图像的加载
        self.show_image[0] = pygame.transform.scale(self.things_images[self.selecting], self.show_image_size)
        self.showing = self.selecting
        path = os.path.join('page', 'page4', 'thing', str(self.things_kind[self.selecting][0]),
                            str(self.things_kind[self.selecting][1]), str(self.things_kind[self.selecting][2]))
        # 打开存储物品信息的txt文本读取信息
        path1 = os.path.join(path, 'detail.txt')
        information = []
        with open(path1, 'r', encoding='utf-8') as f:
            data = f.readline()
            while data:
                information.append(data[:-1])
                data = f.readline()
        if self.things_kind[self.selecting][0] <= 2:  # 查看物品为装备
            if self.equip_wear[0] == self.selecting:
                information[-2] = "取消装备"
            else:
                information[-2] = "装备"
        elif self.things_kind[self.selecting][0] == 3:
            pass
        # 读取字体设置的信息
        path2 = os.path.join(path, 'word.json')
        with open(path2, 'r') as f:
            datas = json.load(f)
        self.show_click_word = datas[-2]
        # 物品详细的文本描述信息
        for i in range(len(information)):
            font = pygame.font.SysFont('SimSun', int(datas[i][0] * screen_height))
            info = information[i]
            if datas[i][4] == 1:
                info += str(self.things[self.selecting].strength)
            elif datas[i][4] == 2:
                info += str(self.things[self.selecting].defence)
            elif datas[i][4] == 3:
                pass
            elif datas[i][4] == 4:
                pass
            elif datas[i][4] == 5:
                info += str(self.things[self.selecting].sell_price)
            elif datas[i][4] == 6:
                info += str(self.things[self.selecting].buy_price)
            words = font.render(info, True, tuple(datas[i][2]))
            rect = words.get_rect()
            if datas[i][3]:
                rect.x = datas[i][1][0] * screen_width
                rect.y = datas[i][1][1] * screen_height
            else:
                rect.center = (datas[i][1][0] * screen_width, datas[i][1][1] * screen_height)
            self.show_words.append([words, rect])

    def throw(self):  # 丢弃背包选中物品
        pass

    def move(self):  # 移动背包物品
        pass

    def sell(self):  # 出售背包物品
        pass
