import json
import math
import os

import pygame


class Bullet(pygame.sprite.Sprite):
    # rect:人物位置，确认子弹发射方向以及绘制的起始坐标
    # pos:鼠标点击坐标，确认子弹发射方向
    # strength:子弹攻击力
    # kind:子弹种类
    def __init__(self, rect, pos, strength, kind, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.direction = None  # 方向
        self.strength = strength  # 攻击力
        self.speed = 0  # 子弹速度
        self.size = 0  # 子弹大小
        self.kind = kind  # 种类
        self.image = None  # 子弹图像
        self.rect = None  # 子弹图像位置
        self.rect_temp = []
        self.load_image(rect, screen_height)
        self.load_direction(pos, rect)

    def load_image(self, rect, screen_height):  # 根据种类读取文档信息获取子弹图像
        path = os.path.join('image', 'page4', 'bullet', str(self.kind) + '.bmp')
        image = pygame.image.load(path)
        file = os.path.join('page', 'page4', 'bullet', str(self.kind) + '.json')
        with open(file, 'r') as f:
            data = json.load(f)
        self.speed = data['speed'] * screen_height
        self.size = (data['size'] * screen_height, data['size'] * screen_height)
        self.image = pygame.transform.scale(image, self.size)
        self.rect = self.image.get_rect()
        self.rect.center = (rect.centerx, rect.centery)  # 将计算得出的坐标赋给子弹图像的中心
        self.rect_temp = [float(rect.centerx), float(rect.centery)]

    def load_direction(self, pos, rect):
        direction_x = pos[0] - rect.centerx
        direction_y = pos[1] - rect.centery
        length = math.sqrt(float(direction_x ** 2) + float(direction_y ** 2))
        if length == 0:
            self.direction = [1, 0]
        else:
            self.direction = [direction_x / length, direction_y / length]

    def update(self, x_change, y_change):  # 更新子弹位置
        self.rect_temp[0] += self.speed * self.direction[0] + x_change
        self.rect_temp[1] += self.speed * self.direction[1] + y_change
        self.rect.centerx = self.rect_temp[0]
        self.rect.centery = self.rect_temp[1]

    def move(self, game_map):  # 根据子弹属性以及地图进行子弹移动
        pass

    def draw(self, screen):  # 在屏幕上绘制子弹
        screen.blit(self.image, self.rect)
