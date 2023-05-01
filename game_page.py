import json
import sys

import pygame


class Page:  # 定义页面类
    def __init__(self):
        self.hero = None
        self.monster = None
        self.npc = None
        self.merchant = None
        self.map = None
        self.box = None
        self.bullet = None
        self.page_kind = 0  # 页面类别
        self.archival = ''  # 存档
        self.directory = None
        self.images = None  # 页面的基本图像
        self.images_pos = None  # 页面的基本图像的位置
        self.images_num = None  # 页面的基本图像的数量
        self.update_page_info()

    def update_page_info(self):  # 根据页面类别更新页面信息
        self.images_num = 0
        self.images = []
        self.images_pos = []
        route = 'page/' + self.archival + 'page' + str(self.page_kind) + '/'  # 更新数据存放的目录
        with open(route + 'images.json', 'r') as f:  # 读取图像数据并更新页面图像信息
            images = json.load(f)
            images_num = len(images)
            for i in range(images_num):
                self.images.append(pygame.image.load(images[i][0]))
                self.images_pos.append(tuple(images[i][1]))
                self.images_num += 1

    def update_page_type(self, page_kind):
        self.page_kind = page_kind
        self.update_page_info()

    def update_page(self, screen):
        for i in range(self.images_num):
            screen.blit(self.images[i], self.images_pos[i])

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button_down_page(event)

    def mouse_button_down_page(self, event):
        if self.page_kind == 0:
            self.mouse_button_down_page0(event)
        elif self.page_kind == 1:
            self.mouse_button_down_page1(event)

    def mouse_button_down_page0(self, event):
        if 800 <= event.pos[0] < 1000 and 175 <= event.pos[1] < 225:
            self.update_page_type(1)
        elif 800 <= event.pos[0] < 1000 and 275 <= event.pos[1] < 325:
            self.update_page_type(5)
        elif 800 <= event.pos[0] < 1000 and 375 <= event.pos[1] < 425:
            self.update_page_type(6)
        elif 800 <= event.pos[0] < 1000 and 475 <= event.pos[1] < 525:
            pygame.quit()
            sys.exit()

    @staticmethod
    def mouse_button_down_page1(event):
        if 550 <= event.pos[0] < 650 and 338 <= event.pos[1] <= 362:
            pygame.quit()
            sys.exit()
