import json
import os
import pygame

from game_equipment import Weapon
from game_thing import Key


class Merchant(pygame.sprite.Sprite):  # 商人类
    def __init__(self, dictionary, setting, hero_size, hero_rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = dictionary['image']  # 图像
        self.size = (setting.screen_height * dictionary['size'], setting.screen_height * dictionary['size'])
        self.rect = None
        self.load_image(setting.screen_width, setting.screen_height, dictionary)

        self.font_height = int(dictionary['font_height'] * setting.screen_height)
        self.font_gap = dictionary['font_gap'] * setting.screen_height  # 字体行间距
        self.color = tuple(dictionary['color'])
        self.font = None
        self.words_tip = "让我们来做单交易吧"
        self.load_word_init()

        self.trade_time = 0
        self.trade_enable = 0  # 是否处于可交易状态
        self.trading = 0  # 是否与角色进行交易中
        self.store = Store(setting, hero_size, hero_rect, dictionary)

    def load_image(self, screen_width, screen_height, dictionary):  # 初始化图像
        path = ''
        for directory in self.image:
            path = os.path.join(path, directory)
        self.image = pygame.transform.scale(pygame.image.load(path), self.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (screen_width * dictionary['rect'][0], screen_height * dictionary['rect'][1])

    def load_word_init(self):  # 初始化字体
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

    def draw(self, screen):  # 绘制商人及可能存在的谈话
        screen.blit(self.image, self.rect)
        if self.trade_enable:
            screen.blit(self.words_tip[0], self.words_tip[1])

    def trade_enable_check(self, hero):  # 判断能否进行交谈
        # noinspection PyTypeChecker
        if pygame.sprite.collide_rect(self, hero):
            self.trade_enable = 1
        else:
            self.trade_enable = 0
            self.trading = 0

    def trade(self):  # 进入交易窗口
        self.trading = 1

    def trading_return(self, monsters, hero):  # 退出商店
        self.trading = 0
        self.store.showing = -1
        hero.bag.showing_return(monsters, hero, None, None)


class Store:  # 商店类
    def __init__(self, setting, hero_size, hero_rect, dictionary):
        self.space = setting.store_space  # 商店空间大小
        self.things_num = 0  # 商店内物品数量
        self.things = []
        self.things_kind = []  # 商店各种物品依次的种类
        self.things_images = []  # 商店中物品图像
        self.things_rects = []  # 商店各个格子中物品图像位置

        self.showing = -1  # 是否正在查看物品详细信息的标志
        self.show_image_size = ()  # 物品详细信息界面的物品图像大小
        self.background = []  # 物品详细信息查看的背景图
        self.show_image = []  # 详细信息中的物品图像
        self.show_words = []  # 详细信息中的物品文字描述等
        self.show_click_word = None  # 详细信息界面可以点击的按钮的文本设置属性

        self.images = []  # 商店基本图像
        self.item_edge = 0  # 原图像商店格子框架宽度
        self.item_width = 0  # 原图像商店格子内宽度加框架宽度
        self.store_width_true = 0  # 原图像商店栏（不含标题）的像素宽度
        self.store_height_true = 0  # 原图像商店栏（不含标题）的像素高度
        self.store_width = 0  # 游戏中加载的商店栏（不含标题）的像素宽度
        self.store_height = 0  # 游戏中加载的商店栏（不含标题）的像素高度

        # 背包基本图像，如空格，说明、使用按钮等
        self.load_data(setting.screen_width, setting.screen_height, hero_size, hero_rect, dictionary)

    def load_data(self, screen_width, screen_height, hero_size, hero_rect, dictionary):  # 加载数据
        with open(os.path.join('page', 'page4', 'store.json'), 'r', encoding='utf-8') as f:
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
        # 初始化商店属性
        self.things_kind = dictionary['things_kind']
        self.item_edge = dictionary['item_edge']
        self.item_width = dictionary['item_width']
        self.store_width_true = self.item_width * 7 + self.item_edge
        self.store_height_true = self.item_width * 5 + self.item_edge
        self.store_width = self.images[1][2][0] - self.images[1][1][0]
        self.store_height = self.images[1][2][1] - self.images[1][1][1]
        # 加载物品详细信息查看的图像信息
        path = ''
        for directory in dictionary['background'][0]:
            path = os.path.join(path, directory)
        size = (dictionary['background'][2][0] * screen_width, dictionary['background'][2][1] * screen_height)
        image = pygame.image.load(path)
        self.background.append(pygame.transform.scale(image, size))
        self.background.append(
            (dictionary['background'][1][0] * screen_width, dictionary['background'][1][1] * screen_height))
        self.background.append((self.background[1][0] + size[0], self.background[1][1] + size[1]))
        self.show_image.append(None)
        size = dictionary['show_image'][1] * screen_height
        self.show_image.append(
            (dictionary['show_image'][0][0] * screen_width - size / 2, dictionary['show_image'][0][1] * screen_height))
        self.show_image_size = (size, size)
        # 加载物品在商店内显示的图像信息
        x_div = self.store_width / self.store_width_true
        y_div = self.store_height / self.store_height_true
        for i in range(self.space):  # 计算商店内各个格子的物品图像的位置
            row = i // 7
            col = i % 7
            x_left = col * self.item_width + self.item_edge
            x_right = (col + 1) * self.item_width
            rect_left = self.images[1][1][0] + x_left * x_div
            rect_right = self.images[1][1][0] + x_right * x_div
            y_top = row * self.item_width + self.item_edge
            y_bottom = (row + 1) * self.item_width
            rect_top = self.images[1][1][1] + y_top * y_div
            rect_bottom = self.images[1][1][1] + y_bottom * y_div
            self.things_rects.append([(rect_left, rect_top), (rect_right, rect_bottom), [rect_left, rect_top]])
        size1 = ((self.item_width - self.item_edge) * x_div, (self.item_width - self.item_edge) * y_div)
        path = os.path.join('image', 'page4', 'thing')
        for i in range(len(self.things_kind)):  # 加载商店所有物品图像
            path1 = path
            if self.things_kind[i]:
                for num in self.things_kind[i][:-2]:
                    path1 = os.path.join(path1, str(num))
                path1 = os.path.join(path1, '1.bmp')
                image = pygame.image.load(path1)
                self.things_images.append(pygame.transform.scale(image, size1))
                self.things_num += 1
            else:
                self.things_images.append(None)
        if len(self.things_images) < self.space:  # 商店物品不足商店空间大小
            for i in range(len(self.things_images), self.space):
                self.things_images.append(None)
        # 实例化商店内的物品
        for thing in dictionary['things_kind']:
            if not thing:
                self.things.append(None)
            elif thing[0] == 1:  # 武器
                self.things.append(Weapon(thing[1], thing[2], hero_size, hero_rect))
            elif thing[0] == 4:  # 道具
                if thing[1] == 1:  # 钥匙
                    self.things.append(Key())

    def draw(self, screen):  # 绘制商店以及商店内物品等图像
        for image in self.images:
            screen.blit(image[0], image[1])
        for i in range(self.space):
            if self.things_images[i]:
                screen.blit(self.things_images[i], tuple(self.things_rects[i][2]))
        if self.showing >= 0:
            screen.blit(self.background[0], self.background[1])
            screen.blit(self.show_image[0], self.show_image[1])
            for word in self.show_words:
                screen.blit(word[0], word[1])

    def click(self, pos, screen_width, screen_height, bag):  # 选中商店物品
        bag.selecting = -1
        bag.showing = -1
        bag.showing_enable = 0
        selecting = -1
        for i in range(self.space):
            if self.things_rects[i][0][0] <= pos[0] < self.things_rects[i][1][0] and self.things_rects[i][0][1] <= \
                    pos[1] < self.things_rects[i][1][1]:
                selecting = i
                break
        # 查看选中物品的详细信息
        if selecting >= 0 and self.things[selecting]:
            self.explain(screen_width, screen_height, selecting)

    def explain(self, screen_width, screen_height, selecting):  # 对商店选中物品展开说明
        self.show_words = []
        # 查看的物品图像的加载
        self.show_image[0] = pygame.transform.scale(self.things_images[selecting], self.show_image_size)
        self.showing = selecting
        path = os.path.join('page', 'page4', 'thing')
        for i in self.things_kind[self.showing][:-2]:
            path = os.path.join(path, str(i))
        path = os.path.join(path, 'word.json')
        # 打开存储物品信息的json文件读取信息
        with open(path, 'r', encoding='utf-8') as f:
            datas = json.load(f)
        datas[-3][-1] = "购买价格："
        datas[-2][-1] = "购买"
        # 物品详细的文本描述信息
        for data in datas:
            font = pygame.font.SysFont('SimSun', int(data[0] * screen_height))
            info = data[-1]
            if data[4] == 1:
                info += str(self.things[selecting].strength)
            elif data[4] == 2:
                info += str(self.things[selecting].defence)
            elif data[4] == 3:
                pass
            elif data[4] == 4:
                info += str(self.things_kind[selecting][-1])
            elif data[4] == 5:
                info += str(self.things[selecting].buy_price)
            words = font.render(info, True, tuple(data[2]))
            rect = words.get_rect()
            if data[3]:
                rect.topleft = (data[1][0] * screen_width, data[1][1] * screen_height)
            else:
                rect.center = (data[1][0] * screen_width, data[1][1] * screen_height)
            self.show_words.append([words, rect])

    def purchase(self, hero, screen_width, screen_height, tip):  # 购买商品
        if hero.money < self.things[self.showing].buy_price:  # 提示金币不足
            tip.create_tip("金币不足！")
            return
        target = -1
        if self.things_kind[self.showing][-2]:  # 物品可以叠放，优先查找背包重复物品位置，叠放存储
            for i in range(hero.bag.space):
                if hero.bag.things_kind[i] and len(hero.bag.things_kind[i]) == len(self.things_kind[self.showing]):
                    same = True
                    for j in range(len(self.things_kind[self.showing]) - 2):
                        if self.things_kind[self.showing][j] != hero.bag.things_kind[i][j]:
                            same = False
                            break
                    if same:
                        target = i
                        break
        if target >= 0:  # 物品可以叠放，且查找重复物品成功
            hero.money -= self.things[self.showing].buy_price
            self.move_to_bag_not_empty(hero.bag, target)
        else:  # 物品只能存放到背包空格中
            if hero.bag.things_num >= hero.bag.space:  # 背包空间已满
                return
            else:  # 背包空间未满，查找空格位置并移动物品
                for i in range(hero.bag.space):
                    if not hero.bag.things[i]:
                        target = i
                        break
                hero.money -= self.things[self.showing].buy_price
                self.move_to_bag_empty(hero.bag, target)
        # 更新英雄金币数量显示
        hero.status.update(hero, screen_height, screen_width)

    def move_to_bag_not_empty(self, bag, target):  # 将购买的物品与背包目标格子的物品重叠存放
        bag.things_kind[target][-1] += 1
        bag.change_things_num_text(target)
        self.after_purchase()

    def move_to_bag_empty(self, bag, target):  # 将购买的物品存放至背包的目标空格中
        bag.things_num += 1
        bag.things[target] = self.things[self.showing]
        bag.things_kind[target] = self.things_kind[self.showing].copy()
        size = (bag.things_rects[target][1][0] - bag.things_rects[target][0][0],
                bag.things_rects[target][1][1] - bag.things_rects[target][0][1])
        bag.things_images[target] = pygame.transform.scale(self.things_images[self.showing], size)
        bag.change_things_num_text(target)
        self.after_purchase()

    def after_purchase(self):  # 购买之后商店的善后工作（攒积货物上架等）
        self.things_num -= 1
        if self.things_num >= self.space:  # 存在攒积货物，将其更新到货架上
            self.things[self.showing] = self.things[self.space]
            self.things_images[self.showing] = self.things_images[self.space]
            self.things_kind[self.showing] = self.things_kind[self.space].copy()
            self.things.pop(self.space)
            self.things_images.pop(self.space)
            self.things_kind.pop(self.space)
        else:  # 删除该格子货物
            self.things[self.showing] = None
            self.things_images[self.showing] = None
            self.things_kind[self.showing] = []
        self.showing = -1

    def showing_cancel(self):  # 从物品详细信息界面返回游戏
        self.showing = -1
