import json
import os

import pygame


class Harm:  # 伤害数值的显示
    def __init__(self, screen_height):
        self.font = None
        self.font_height = None
        self.harm = []
        self.color = None  # 字体颜色
        self.speed = 0  # 字体上升速度
        self.time_existing = 0  # 字体存在时间
        self.init_data(screen_height)

    def init_data(self, screen_height):  # 初始化固定数值
        # 获取伤害显示的相关信息
        with open(os.path.join('page', 'page4', 'harm.json'), 'r') as f:
            dictionary = json.load(f)
        self.speed = dictionary['speed'] * screen_height  # 伤害在屏幕中上升的速度
        self.time_existing = dictionary['time_existing']  # 伤害在屏幕中存在的时间
        self.color = tuple(dictionary['color'])  # 伤害显示的颜色
        self.font = pygame.font.SysFont('SimSun', int(dictionary['font_size'] * screen_height))
        self.font_height = self.font.get_height()

    def add_harm(self, value, rect_harm):
        harm = self.font.render('-' + str(value), True, self.color)  # 生成显示的文字
        rect = harm.get_rect()  # 获取文本坐标
        rect.center = (rect_harm.centerx, rect_harm.y - self.font_height / 2)
        self.harm.append([harm, rect, [rect.x, rect.y], pygame.time.get_ticks()])

    def update(self, x_change, y_change):  # 伤害数值在屏幕上的更新
        # 英雄受到的伤害在屏幕上的更新
        num = len(self.harm)
        i = 0
        time_now = pygame.time.get_ticks()
        while i < num:
            self.harm[i][2][0] += x_change  # 更新位置，使用临时浮点数变量使坐标显示更为精准
            self.harm[i][2][1] += y_change - self.speed
            self.harm[i][1].x = self.harm[i][2][0]
            self.harm[i][1].y = self.harm[i][2][1]
            if self.harm[i][3] + self.time_existing <= time_now:  # 判断存在时间受否已达上限
                self.harm.pop(i)
                num -= 1
            else:
                i += 1

    def draw(self, screen):  # 绘制伤害值
        for harm in self.harm:
            screen.blit(harm[0], harm[1])
