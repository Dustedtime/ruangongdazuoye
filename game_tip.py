import json
import os

import pygame


class Tip:  # 游戏提示类
    def __init__(self, screen_width, screen_height):
        self.words = []  # 提示文本
        self.font = None  # 提示字体
        self.font_color = None  # 提示字体颜色
        self.images = []  # 基本图像
        self.last_time = 0  # 提示窗口开始出现的时间
        self.exist_time = 0  # 提示窗口存在时间

        self.init_data(screen_width, screen_height)

    def init_data(self, screen_width, screen_height):  # 初始化信息
        path = os.path.join('page', 'tip.json')
        with open(path, 'r', encoding='utf-8') as f:
            dictionary = json.load(f)
        # 背景图像
        for image in dictionary['images']:
            path = ''
            for directory in image[0]:
                path = os.path.join(path, directory)
            img = pygame.image.load(path)
            img_size = (image[2][0] * screen_width, image[2][1] * screen_height)
            img_left_top = (image[1][0] * screen_width, image[1][1] * screen_height)
            img_right_bottom = (img_left_top[0] + img_size[0], img_left_top[1] + img_size[1])
            img = pygame.transform.scale(img, img_size)
            self.images.append([img, img_left_top, img_right_bottom])
        # 提示的字体属性
        self.font = pygame.font.SysFont('SimSun', int(dictionary['font_size'] * screen_height))
        self.font_color = tuple(dictionary['font_color'])
        self.exist_time = dictionary['exist_time']

    def update(self):  # 更新提示窗口状态（提示窗口显示时间到达后取消显示）
        if self.words:
            if self.last_time + self.exist_time <= pygame.time.get_ticks():
                self.words.clear()

    def draw(self, screen):  # 绘制提示窗口
        if self.words:
            for image in self.images:
                screen.blit(image[0], image[1])
            screen.blit(self.words[0], self.words[1])

    def create_tip(self, text):  # 添加提示文本
        word = self.font.render(text, True, self.font_color)
        rect = word.get_rect()
        rect.centerx = (self.images[0][1][0] + self.images[0][2][0]) / 2
        rect.centery = (self.images[0][1][1] + self.images[0][2][1]) / 2
        self.words.clear()
        self.words.append(word)
        self.words.append(rect)
        self.last_time = pygame.time.get_ticks()
