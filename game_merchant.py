import json
import os
import pygame


class Merchant(pygame.sprite.Sprite):
    def __init__(self, dictionary, setting, archival):
        pygame.sprite.Sprite.__init__(self)
        self.image = dictionary['image']  # 图像
        self.size = (setting.screen_height * dictionary['size'], setting.screen_height * dictionary['size'])
        self.load_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (
            setting.screen_width * dictionary['rect'][0], setting.screen_height * dictionary['rect'][1])
        self.font_height = int(dictionary['font_height'] * setting.screen_height)
        self.font_gap = dictionary['font_gap'] * setting.screen_height  # 字体行间距
        self.color = tuple(dictionary['color'])
        self.trade_time = 0
        self.trade_enable = 0  # 是否处于可交易状态
        self.trading = 0  # 是否与角色进行交易中
        self.font = None
        self.words_tip = dictionary['words_tip']
        self.load_word_init()
        self.things = dictionary['things']
        self.store = Store(setting, archival, self.things)

    def load_image(self):  # 初始化图像
        path = ''
        for directory in self.image:
            path = os.path.join(path, directory)
        self.image = pygame.transform.scale(pygame.image.load(path), self.size)

    def load_word_init(self):
        self.font = pygame.font.SysFont('SimSun', self.font_height)
        # 加载可谈话标志
        word = self.font.render(self.words_tip, True, self.color)
        rect = word.get_rect()
        rect.centerx = self.rect.centerx
        rect.y = self.rect.y - self.font_gap
        self.words_tip = [word, rect]

    def update(self, x, y, hero):  # 更新商人位置及可能存在的交易的位置，以及更新交易状态
        self.rect.x += x
        self.rect.y += y
        self.words_tip[1].x += x
        self.words_tip[1].y += y
        self.trade_enable_check(hero)

    def draw(self, screen):  # 绘制npc及可能存在的谈话
        screen.blit(self.image, self.rect)
        if self.trade_enable:
            screen.blit(self.words_tip[0], self.words_tip[1])
        if self.trading:
            self.store.draw(screen)

    def trade_enable_check(self, hero):  # 判断能否进行交谈
        if pygame.sprite.collide_rect(self, hero):
            self.trade_enable = 1
        else:
            self.trade_enable = 0
            self.trading = 0

    def trade(self):
        self.trading = 1


class Store:
    def __init__(self, setting, archival, things):
        self.space = setting.store_space

        self.things = things
        self.things_kind = None  # 商店各种物品依次的种类
        self.things_images = []  # 商店中物品图像
        self.things_rects = []  # 商店各个格子中物品图像位置

        self.images = []  # 商店基本图像
        self.item_edge = 0  # 原图像商店格子框架宽度
        self.item_width = 0  # 原图像商店格子内宽度加框架宽度
        self.store_width_true = 0  # 原图像商店栏（不含标题）的像素宽度
        self.store_height_true = 0  # 原图像商店栏（不含标题）的像素高度
        self.store_width = 0  # 游戏中加载的商店栏（不含标题）的像素宽度
        self.store_height = 0  # 游戏中加载的商店栏（不含标题）的像素高度

        self.load_data(setting.screen_width, setting.screen_height, archival, things)  # 背包基本图像，如空格，说明、使用按钮等

    def load_data(self, screen_width, screen_height, archival, merchant_things):
        with open(os.path.join('page', 'page4', 'store.json'), 'r') as f:
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
        pass

    def draw(self, screen):
        for image in self.images:
            screen.blit(image[0], image[1])
        pass
