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
        self.things_num_words = []  # 背包每个格子内该物品数量的文本
        self.things_num_font = None  # 背包每个格子内该物品数量的文字字体
        self.things_num_color = None  # 背包每个格子内该物品数量的文本颜色

        self.moving = 0  # 移动背包物品位置的标志
        self.move_enable = 0  # 能否开始移动的标志
        self.move_gap = 0  # 开始移动的距离
        self.moving_start = None  # 移动物品开始是鼠标坐标
        self.moving_now = None  # 移动物品目前鼠标所在坐标

        self.equip_wear = []  # 装备中的物品标号
        self.equip_image = []  # 装备中图标
        self.selecting = -1  # 背包选中物品标号
        self.selecting_image = []  # 背包选中物品时的边框图像
        self.selecting_num = 0  # 选中物品的数量（某些物品可以堆叠存放）
        self.selecting_num_moving = 0  # 使用拖动刻度方法改变选中物品数量的标志
        self.selecting_num_image = []  # 选中物品数量的进度条（拖动调节选中数量）
        self.selecting_words = []  # 描述选中物品数量的文字

        self.showing = -1  # 是否正在查看物品详细信息的标志
        self.showing_enable = 0  # 是否可查看物品详细信息
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
        self.move_gap = data['move_gap']
        self.equip_wear = data['equip_wear']
        self.things_kind = data['things_kind']
        self.item_edge = data['item_edge']
        self.item_width = data['item_width']
        self.things_num_font = pygame.font.SysFont('SimSun', int(data['things_num_font'][0] * screen_height))
        self.things_num_color = tuple(data['things_num_font'][1])
        self.bag_width_true = self.item_width * 5 + self.item_edge
        self.bag_height_true = self.item_width * 7 + self.item_edge
        self.bag_width = self.images[1][2][0] - self.images[1][1][0]
        self.bag_height = self.images[1][2][1] - self.images[1][1][1]
        # 加载物品在背包内显示的图像信息
        x_div = self.bag_width / self.bag_width_true
        y_div = self.bag_height / self.bag_height_true
        for i in range(self.space):  # 计算背包内各个格子的物品图像的位置
            row = i // 5
            col = i % 5
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
        for i in range(self.space):
            path1 = path
            if self.things_kind[i]:
                for num in self.things_kind[i][:-3]:
                    path1 = os.path.join(path1, str(num))
                path1 = os.path.join(path1, str(self.things_kind[i][-3]) + '.bmp')
                image = pygame.image.load(path1)
                self.things_images.append(pygame.transform.scale(image, size1))
                self.things_num += 1  # 背包内物品数量加一
            else:
                self.things_images.append(None)
        # 加载背包每个格子内该物品数量的文本
        for i in range(self.space):
            if self.things_kind[i] and self.things_kind[i][-2]:
                word = self.things_num_font.render(str(self.things_kind[i][-1]), True, self.things_num_color)
                rect = word.get_rect()
                rect.right = self.things_rects[i][1][0] - 3
                rect.bottom = self.things_rects[i][1][1] - 3
                self.things_num_words.append([word, rect])
            else:
                self.things_num_words.append(None)
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
        size = ((self.item_edge + self.item_width) * x_div, (self.item_edge + self.item_width) * y_div)
        self.selecting_image.append(pygame.transform.scale(image, size))
        self.selecting_image.append(None)
        # 加载描述选中物品数量的图像和文本
        for image in data['selecting_num_image']:
            path = ''
            for directory in image[0]:
                path = os.path.join(path, directory)
            img = pygame.image.load(path)
            size = (image[2][0] * screen_width, image[2][1] * screen_height)
            img = pygame.transform.scale(img, size)
            img_left_top = (image[1][0] * screen_width, image[1][1] * screen_height)
            img_right_bottom = (img_left_top[0] + size[0], img_left_top[1] + size[1])
            self.selecting_num_image.append([img, img_left_top, img_right_bottom])
        centery = (self.selecting_num_image[3][1][1] + self.selecting_num_image[3][2][1]) / 2
        self.selecting_num_image[3][1] = self.selecting_num_image[3][0].get_rect()
        self.selecting_num_image[3][1].centery = centery
        with open(os.path.join('page', 'page4', 'bag_words.json'), 'r') as f:
            words_data = json.load(f)
        for words in words_data:
            font = pygame.font.SysFont('SimSun', int(screen_height * words[0]))
            rect_left_top = (screen_width * words[2][0], screen_height * words[2][1])
            color = tuple(words[3])
            self.selecting_words.append([font, color, rect_left_top, None])
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
        img_left_top = (data['show_image'][0][0] * screen_width - size / 2, data['show_image'][0][1] * screen_height)
        self.show_image.append(img_left_top)
        # 实例化背包内的物品
        for thing in data['things_kind']:
            if not thing:
                self.things.append(None)
            elif thing[0] == 1:  # 武器
                self.things.append(Weapon(thing[1], thing[2], hero_size, hero_rect))

    def draw(self, screen):  # 绘制背包
        for image in self.images:
            screen.blit(image[0], image[1])
        for equip in self.equip_image:
            if equip[1]:
                screen.blit(equip[0], equip[1])
        if self.selecting >= 0:
            screen.blit(self.selecting_image[0], self.selecting_image[1])
            if self.things[self.selecting]:
                for words in self.selecting_words:
                    screen.blit(words[3], words[2])
                for image in self.selecting_num_image:
                    screen.blit(image[0], image[1])
        if self.showing >= 0:
            screen.blit(self.background[0], self.background[1])
            screen.blit(self.show_image[0], self.show_image[1])
            for word in self.show_words:
                screen.blit(word[0], word[1])

    def change_weapon_wear(self, showing):  # 更换穿戴中武器图标位置
        if showing == self.equip_wear[0]:
            return
        self.equip_wear[0] = showing
        if showing < 0:
            self.equip_image[0][1] = None
        else:
            self.equip_image[0][1] = self.things_rects[showing][0]

    def click_select(self, pos, box, merchant):  # 选中背包物品
        selecting = -1
        for i in range(self.space):
            if self.things_rects[i][0][0] <= pos[0] < self.things_rects[i][1][0] and self.things_rects[i][0][1] <= \
                    pos[1] < self.things_rects[i][1][1]:
                selecting = i
                break
        if selecting < 0:  # 选择无效（点击到边框）
            self.selecting = -1
            self.showing_enable = 0
        elif self.selecting == selecting:  # 重复点击同意物品，将可展示详细信息标志置一
            if self.showing != self.selecting and self.things[self.selecting]:
                self.showing_enable = 1
        else:  # 首次点击该物品
            self.click_select_first(selecting)
        if self.selecting >= 0 and self.things[self.selecting]:  # 选择有效，将可移动标志置一
            self.move_enable = 1
            self.moving_start = pos  # 将当前鼠标位置置为移动起始坐标
        if box:  # 修改宝箱选中物品标志
            box.selecting = -1
            box.showing = -1
            box.showing_enable = 0
        if merchant:  # 修改商店选中物品标志
            merchant.store.showing = -1

    def click_select_first(self, selecting):  # 首次点击该物品，更新选中边框位置以及选中数量信息
        self.showing_enable = 0
        self.selecting = selecting
        row = selecting // 5
        col = selecting % 5
        x = col * self.item_width * self.bag_width / self.bag_width_true + self.images[1][1][0]
        y = row * self.item_width * self.bag_height / self.bag_height_true + self.images[1][1][1]
        self.selecting_image[1] = (x, y)
        if self.things[selecting]:  # 若选中格子不为空，更新选中物品数量为1
            self.selecting_num = 1
            text = self.selecting_words[0][0].render("选中：" + str(self.selecting_num), True,
                                                     self.selecting_words[0][1])
            self.selecting_words[0][3] = text
            text = self.selecting_words[1][0].render("拥有：" + str(self.things_kind[selecting][-1]), True,
                                                     self.selecting_words[1][1])
            self.selecting_words[1][3] = text
            # 重新调整选中数量进度条刻度位置
            length = self.selecting_num_image[0][2][0] - self.selecting_num_image[0][1][0] - 1
            rect_x = self.selecting_num_image[0][1][0] + self.selecting_num * length / self.things_kind[self.selecting][
                -1]
            self.selecting_num_image[3][1].centerx = rect_x

    def change_selecting_num_text(self):  # 修改选中物品数量的文本显示
        text = self.selecting_words[0][0].render("选中：" + str(self.selecting_num), True, self.selecting_words[0][1])
        self.selecting_words[0][3] = text
        text = self.selecting_words[1][0].render("拥有：" + str(self.things_kind[self.selecting][-1]), True,
                                                 self.selecting_words[1][1])
        self.selecting_words[1][3] = text

    def change_things_num_text(self, target):  # 修改格子内物品数量显示文本
        if self.things_kind[target] and self.things_kind[target][-2] and self.things_kind[target][-1]:
            word = self.things_num_font.render(str(self.things_kind[target][-1]), True, self.things_num_color)
            rect = word.get_rect()
            rect.right = self.things_rects[target][1][0] - 3
            rect.bottom = self.things_rects[target][1][1] - 3
            self.things_num_words[target] = [word, rect]
        else:
            self.things_num_words[target] = None

    def change_selecting_num(self, num):  # 改变选中的物品数量
        if not self.things[self.selecting]:
            return
        if self.selecting_num + num <= 0 or self.selecting_num + num > self.things_kind[self.selecting][-1]:
            return
        self.selecting_num += num
        # 重新调整选中数量进度条刻度位置
        length = self.selecting_num_image[0][2][0] - self.selecting_num_image[0][1][0] - 1
        rect_x = self.selecting_num_image[0][1][0] + self.selecting_num * length / self.things_kind[self.selecting][-1]
        self.selecting_num_image[3][1].centerx = rect_x
        # 修改选中物品数量的文本显示
        self.change_selecting_num_text()

    def change_selecting_num_tick(self, x, method):  # 通过点击数量进度条改变选中物品数量
        # 防止点击坐标过界
        if x < self.selecting_num_image[0][1][0]:
            x = self.selecting_num_image[0][1][0]
        elif x >= self.selecting_num_image[0][2][0]:
            x = self.selecting_num_image[0][2][0] - 1
        self.selecting_num_moving = method  # 判断拖动还是点击
        length = self.selecting_num_image[0][2][0] - self.selecting_num_image[0][1][0] - 1
        num = self.things_kind[self.selecting][-1] * (x - self.selecting_num_image[0][1][0]) / length
        # 调整选中数量（四舍五入）
        if num - int(num) > 0.5:
            num = int(num) + 1
        else:
            num = int(num)
        if not num:
            num = 1
        # 更新选中数量和拥有数量文本
        if self.selecting_num != num:
            self.selecting_num = num
            self.change_selecting_num_text()
        # 根据改变数量方式更改刻度坐标
        if method:
            self.selecting_num_image[3][1].centerx = x
        else:
            rect_x = self.selecting_num_image[0][1][0] + num * length / self.things_kind[self.selecting][-1]
            self.selecting_num_image[3][1].centerx = rect_x

    def change_selecting_num_moving(self, x, end):  # 通过拖动刻度改变选中物品数量
        # 限制拖动有效范围
        if x < self.selecting_num_image[0][1][0]:
            x = self.selecting_num_image[0][1][0]
        elif x >= self.selecting_num_image[0][2][0]:
            x = self.selecting_num_image[0][2][0] - 1
        # 计算相关数据
        length = self.selecting_num_image[0][2][0] - self.selecting_num_image[0][1][0] - 1
        num = self.things_kind[self.selecting][-1] * (x - self.selecting_num_image[0][1][0]) / length
        # 调整选中数量（四舍五入）
        if num - int(num) > 0.5:
            num = int(num) + 1
        else:
            num = int(num)
        if not num:
            num = 1
        # 更新选中数量和拥有数量文本
        if self.selecting_num != num:
            self.selecting_num = num
            self.change_selecting_num_text()
        # 更改数量刻度坐标
        self.selecting_num_image[3][1].centerx = x
        # 拖动结束标志为1，改变物品数量结束，重新调整刻度坐标（即选中数量只能为整数）
        if end:
            self.selecting_num_moving = 0
            rect_x = self.selecting_num_image[0][1][0] + num * length / self.things_kind[self.selecting][-1]
            self.selecting_num_image[3][1].centerx = rect_x
        pass

    def explain(self, screen_width, screen_height, box, merchant):  # 对背包选中物品展开说明
        self.showing_enable = 0
        self.show_words = []
        # 查看的物品图像的加载
        self.show_image[0] = pygame.transform.scale(self.things_images[self.selecting], self.show_image_size)
        self.showing = self.selecting
        path = os.path.join('page', 'page4', 'thing')
        for i in self.things_kind[self.showing][:-2]:
            path = os.path.join(path, str(i))
        # 打开存储物品信息的txt文本读取信息
        path1 = os.path.join(path, 'detail.txt')
        information = []
        with open(path1, 'r', encoding='utf-8') as f:
            data = f.readline()
            while data:
                information.append(data[:-1])
                data = f.readline()
        information.append("出售价格：")
        if box:
            information.append("丢弃")
        elif merchant:
            information.append("出售")
        else:
            if self.things_kind[self.selecting][0] <= 2:  # 查看物品为装备
                if self.equip_wear[0] == self.selecting:
                    information.append("脱除")
                else:
                    information.append("装备")
            elif self.things_kind[self.selecting][0] == 3:
                pass
        information.append("取消")
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
            words = font.render(info, True, tuple(datas[i][2]))
            rect = words.get_rect()
            if datas[i][3]:
                rect.x = datas[i][1][0] * screen_width
                rect.y = datas[i][1][1] * screen_height
            else:
                rect.center = (datas[i][1][0] * screen_width, datas[i][1][1] * screen_height)
            self.show_words.append([words, rect])

    def showing_click_left(self, screen_width, screen_height, box, merchant, hero):  # 查看物品详细信息时点击了操作键
        if box:  # 宝箱打开中，左键显示为丢弃
            self.throw(box)
        elif merchant:
            self.sell(merchant, hero, screen_width, screen_height)
        elif self.things_kind[self.showing][0] == 1:  # 查看物品为武器
            if self.equip_wear[0] == self.showing:  # 该武器正被装备，点击后取消装备该武器
                self.showing_weapon_off(screen_width, screen_height)
            else:  # 该武器未被装备，点击后装备该武器
                self.showing_weapon_on(screen_width, screen_height)

    def throw(self, box):  # 丢弃背包选中物品到宝箱中
        # 穿戴中物品不可直接丢弃
        for i in self.equip_wear:
            if i == self.selecting:
                return
        target = -1
        # 物品可以叠放，优先查找宝箱重复物品位置，叠放存储
        if self.things_kind[self.selecting][-2]:
            for i in range(box.space):
                if box.things[i] and len(box.things_kind[i]) == len(self.things_kind[self.selecting]):
                    same = True
                    for j in range(len(self.things_kind[self.selecting]) - 2):
                        if self.things_kind[self.selecting][j] != box.things_kind[i][j]:
                            same = False
                            break
                    if same:
                        target = i
                        break
        if target >= 0:  # 物品可以叠放，且查找重复物品成功
            self.move_to_box_not_empty_same(box, target)
        else:  # 物品只能存放到宝箱空格中
            if box.things_num >= box.space:  # 背包空间已满
                return
            else:  # 宝箱空间未满，查找空格位置并移动物品
                for i in range(box.space):
                    if not box.things[i]:
                        target = i
                        break
                self.move_to_box_empty(box, target)

    def sell(self, merchant, hero, screen_width, screen_height):  # 出售背包物品
        size = (merchant.store.things_rects[0][1][0] - merchant.store.things_rects[0][0][0],
                merchant.store.things_rects[0][1][1] - merchant.store.things_rects[0][0][1])
        for i in range(self.selecting_num):
            # 商店货架未满，直接出售到商店货架上（可见）
            if merchant.store.things_num < merchant.store.space:
                for j in range(merchant.store.space):
                    if not merchant.store.things[j]:
                        merchant.store.things[j] = self.things[self.selecting]
                        merchant.store.things_kind[j] = self.things_kind[self.selecting].copy()
                        merchant.store.things_kind[j][-1] = 1
                        merchant.store.things_images[j] = pygame.transform.scale(self.things_images[self.selecting],
                                                                                 size)
                        merchant.store.things_num += 1
                        break
            # 商店货架已满，囤积到商店中（不可见）
            else:
                merchant.store.things.append(self.things[self.selecting])
                merchant.store.things_kind.append(self.things_kind[self.selecting].copy())
                merchant.store.things_kind[-1][-1] = 1
                image = pygame.transform.scale(self.things_images[self.selecting], size)
                merchant.store.things_images.append(image)
                merchant.store.things_num += 1
        self.things_kind[self.selecting][-1] -= self.selecting_num
        # 更新英雄金币数量
        hero.money += self.things[self.selecting].sell_price * self.selecting_num
        hero.status.update(hero, screen_height, screen_width)
        # 背包内该物品售空
        if not self.things_kind[self.selecting][-1]:
            self.things[self.selecting] = None
            self.things_images[self.selecting] = None
            self.things_kind[self.selecting] = []
        # 更改该格子显示的物品数量
        self.change_things_num_text(self.selecting)
        self.selecting = -1
        self.showing = -1

    def showing_weapon_off(self, screen_width, screen_height):  # 取消装备选中的武器
        info = "装备"
        font = pygame.font.SysFont('SimSun', int(self.show_click_word[0] * screen_height))
        words = font.render(info, True, tuple(self.show_click_word[2]))
        rect = words.get_rect()
        rect.center = (self.show_click_word[1][0] * screen_width, self.show_click_word[1][1] * screen_height)
        self.show_words[-2] = [words, rect]
        self.change_weapon_wear(-1)  # 更新背包中装备中武器

    def showing_weapon_on(self, screen_width, screen_height):  # 装备选中的武器
        info = "脱除"
        font = pygame.font.SysFont('SimSun', int(self.show_click_word[0] * screen_height))
        words = font.render(info, True, tuple(self.show_click_word[2]))
        rect = words.get_rect()
        rect.center = (self.show_click_word[1][0] * screen_width, self.show_click_word[1][1] * screen_height)
        self.show_words[-2] = [words, rect]
        self.change_weapon_wear(self.showing)  # 更新背包中装备中武器

    def showing_return(self, monsters, hero, box, merchant):  # 从物品详细信息界面返回游戏
        self.showing = -1
        if box or merchant:
            return
        time_now = pygame.time.get_ticks()
        for monster in monsters:
            monster.attack_time = time_now  # 更新怪物上次攻击时间
        hero.attack_time = time_now  # 更新英雄上次攻击时间

    def move(self, pos):  # 移动背包物品
        self.moving_now = [pos[0], pos[1]]
        # 计算物品被拖动的偏移量
        x_change = self.moving_now[0] - self.moving_start[0]
        y_change = self.moving_now[1] - self.moving_start[1]
        if abs(x_change) >= self.move_gap or abs(y_change) >= self.move_gap:
            self.moving = 1
            self.showing_enable = 0
        # 根据偏移量更新物品图像坐标
        if self.moving:
            self.things_rects[self.selecting][2][0] = self.things_rects[self.selecting][0][0] + x_change
            self.things_rects[self.selecting][2][1] = self.things_rects[self.selecting][0][1] + y_change

    def move_to_bag_empty(self, target):  # 移动物品到背包的某个空格中
        # 获取目标位置行数和列数（从零开始）
        row = target // 5
        col = target % 5
        self.things[target] = self.things[self.selecting]  # 复制物品对象
        self.things_images[target] = self.things_images[self.selecting]  # 复制物品图像
        # 修改数量信息
        self.things_kind[target] = self.things_kind[self.selecting].copy()
        self.things_kind[target][-1] = self.selecting_num
        self.things_kind[self.selecting][-1] -= self.selecting_num
        # 修改显示的格子内物品数量信息
        self.change_things_num_text(self.selecting)
        self.change_things_num_text(target)
        # 修改其他信息
        if self.things_kind[self.selecting][-1]:  # 仅移动选中物品的一部分
            self.things_num += 1
            # 调节显示的选中数量文本信息
            self.selecting_num = 1
            self.change_selecting_num_text()
            length = self.selecting_num_image[0][2][0] - self.selecting_num_image[0][1][0] - 1
            num = self.things_kind[self.selecting][-1]
            self.selecting_num_image[3][1].centerx = self.selecting_num_image[0][1][0] + length / num
        else:  # 移动选中物品的全部
            for i in range(len(self.equip_wear)):  # 修改佩戴装备
                if self.equip_wear[i] == self.selecting:
                    self.equip_image[i][1] = (self.things_rects[target][0][0], self.things_rects[target][0][1])
                    self.equip_wear[i] = target
                    break
            self.things[self.selecting] = None
            self.things_images[self.selecting] = None
            self.things_kind[self.selecting] = []
            if self.showing == self.selecting:
                self.showing = target
            self.selecting = target
            x = col * self.item_width * self.bag_width / self.bag_width_true + self.images[1][1][0]
            y = row * self.item_width * self.bag_height / self.bag_height_true + self.images[1][1][1]
            self.selecting_image[1] = (x, y)

    def move_to_bag_not_empty_not_same(self, target):  # 目标格子不为空，且物品种类不一致
        if self.things_kind[self.selecting][-1] != self.selecting_num:  # 无效移动
            return
        # 修改佩戴装备
        for i in range(len(self.equip_wear)):
            if self.equip_wear[i] == self.selecting:
                self.equip_image[i][1] = (self.things_rects[target][0][0], self.things_rects[target][0][1])
                self.equip_wear[i] = target
                break
            elif self.equip_wear[i] == target:
                self.equip_image[i][1] = (
                    self.things_rects[self.selecting][0][0], self.things_rects[self.selecting][0][1])
                self.equip_wear[i] = self.selecting
                break
        # 获取目标位置行数和列数（从零开始）
        row = target // 5
        col = target % 5
        # 交换两个格子的物品
        thing = self.things[self.selecting]
        self.things[self.selecting] = self.things[target]
        self.things[target] = thing
        # 交换图像
        image = self.things_images[self.selecting]
        self.things_images[self.selecting] = self.things_images[target]
        self.things_images[target] = image
        # 修改正在展示物品的编号
        if self.showing == self.selecting:
            self.showing = target
        elif self.showing == target:
            self.showing = self.selecting
        # 修改物品种类
        kind = self.things_kind[self.selecting].copy()
        self.things_kind[self.selecting] = self.things_kind[target].copy()
        self.things_kind[target] = kind
        # 修改格子内物品数量显示文本
        self.change_things_num_text(self.selecting)
        self.change_things_num_text(target)
        # 修改选中边框的坐标
        self.selecting = target
        x = col * self.item_width * self.bag_width / self.bag_width_true + self.images[1][1][0]
        y = row * self.item_width * self.bag_height / self.bag_height_true + self.images[1][1][1]
        self.selecting_image[1] = (x, y)

    def move_to_bag_not_empty_same(self, target):  # 目标格子不为空，且物品种类一致
        # 获取目标位置行数和列数（从零开始）
        row = target // 5
        col = target % 5
        # 物品可以叠放
        if self.things_kind[target][-2]:
            # 修改两处物品的数量
            self.things_kind[self.selecting][-1] -= self.selecting_num
            self.things_kind[target][-1] += self.selecting_num
            self.selecting_num = 1
            # 修改两处格子内物品显示数量文本
            self.change_things_num_text(self.selecting)
            self.change_things_num_text(target)
            # 物品全部移过去的情况
            if not self.things_kind[self.selecting][-1]:
                self.things_num -= 1
                self.things[self.selecting] = None
                self.things_images[self.selecting] = None
                self.things_kind[self.selecting] = []
                if self.showing == self.selecting:
                    self.showing = target
                self.selecting = target
                # 修改选中边框的坐标
                x = col * self.item_width * self.bag_width / self.bag_width_true + self.images[1][1][0]
                y = row * self.item_width * self.bag_height / self.bag_height_true + self.images[1][1][1]
                self.selecting_image[1] = (x, y)
            # 调节显示的选中数量文本信息
            self.change_selecting_num_text()
            length = self.selecting_num_image[0][2][0] - self.selecting_num_image[0][1][0] - 1
            num = self.things_kind[self.selecting][-1]
            self.selecting_num_image[3][1].centerx = self.selecting_num_image[0][1][0] + length / num
        # 物品不可以叠放
        else:
            # 修改佩戴装备
            for i in range(len(self.equip_wear)):
                if self.equip_wear[i] == self.selecting:
                    self.equip_image[i][1] = (self.things_rects[target][0][0], self.things_rects[target][0][1])
                    self.equip_wear[i] = target
                    break
                elif self.equip_wear[i] == target:
                    self.equip_image[i][1] = (
                        self.things_rects[self.selecting][0][0], self.things_rects[self.selecting][0][1])
                    self.equip_wear[i] = self.selecting
                    break
            # 修改展示详细信息物品的下标以及选中物品下标
            if self.showing == self.selecting:
                self.showing = target
            self.selecting = target
            # 修改选中边框的坐标
            x = col * self.item_width * self.bag_width / self.bag_width_true + self.images[1][1][0]
            y = row * self.item_width * self.bag_height / self.bag_height_true + self.images[1][1][1]
            self.selecting_image[1] = (x, y)

    def move_to_box_empty(self, box, target):  # 移动物品到宝箱的某个空格中
        # 将数据复制或移动过去
        box.things_kind[target] = self.things_kind[self.selecting].copy()
        box.things_kind[target][-1] = self.selecting_num
        box.things[target] = self.things[self.selecting]
        box.things_num += 1
        size = (box.things_rects[target][1][0] - box.things_rects[target][0][0],
                box.things_rects[target][1][1] - box.things_rects[target][0][1])
        box.things_images[target] = pygame.transform.scale(self.things_images[self.selecting], size)
        box.change_things_num_text(target)
        # 修改移动后的背包属性
        self.things_kind[self.selecting][-1] -= self.selecting_num
        if not self.things_kind[self.selecting][-1]:
            self.things[self.selecting] = None
            self.things_images[self.selecting] = None
            self.things_kind[self.selecting] = []
            self.things_num -= 1
            self.things_num_words[self.selecting] = None
        self.change_things_num_text(self.selecting)
        if self.showing == self.selecting:
            self.showing = -1
        self.selecting = -1

    def move_to_box_not_empty_not_same(self, box, target):  # 移动到宝箱，目标格子不为空，且物品种类不一致
        if self.things_kind[self.selecting][-1] != self.selecting_num:  # 无效移动
            return
        # 交换物品数据
        thing = self.things[self.selecting]
        self.things[self.selecting] = box.things[target]
        box.things[target] = thing
        thing_kind = self.things_kind[self.selecting].copy()
        self.things_kind[self.selecting] = box.things_kind[target].copy()
        box.things_kind[target] = thing_kind
        size_bag = (self.things_rects[self.selecting][1][0] - self.things_rects[self.selecting][0][0],
                    self.things_rects[self.selecting][1][1] - self.things_rects[self.selecting][0][1])
        size_box = (box.things_rects[target][1][0] - box.things_rects[target][0][0],
                    box.things_rects[target][1][1] - box.things_rects[target][0][1])
        image = pygame.transform.scale(self.things_images[self.selecting], size_box)
        self.things_images[self.selecting] = pygame.transform.scale(box.things_images[target], size_bag)
        box.things_images[target] = image
        # 更改背包的格子内物品数量显示文本
        self.change_things_num_text(self.selecting)
        # 更改宝箱的格子内物品数量显示文本
        box.change_things_num_text(target)
        # 更新背包属性
        if self.showing == self.selecting:
            self.showing = -1
        self.selecting = -1

    def move_to_box_not_empty_same(self, box, target):  # 移动到宝箱，目标格子不为空，且物品种类一致
        if not self.things_kind[self.selecting][-2]:  # 物品不可以叠放
            if self.showing == self.selecting:
                self.showing = -1
            self.selecting = -1
        else:  # 物品可以叠放
            box.things_kind[target][-1] += self.selecting_num
            self.things_kind[self.selecting][-1] -= self.selecting_num
            # 更改宝箱的格子内物品数量显示文本
            box.change_things_num_text(target)
            # 更改背包的格子内物品数量显示文本
            self.change_things_num_text(self.selecting)
            # 仅移动一部分
            if self.things_kind[self.selecting][-1]:
                # 调节显示的选中数量文本信息
                self.selecting_num = 1
                self.change_selecting_num_text()
                length = self.selecting_num_image[0][2][0] - self.selecting_num_image[0][1][0] - 1
                num = self.things_kind[self.selecting][-1]
                self.selecting_num_image[3][1].centerx = self.selecting_num_image[0][1][0] + length / num
            # 全部移动过去
            else:
                self.things[self.selecting] = None
                self.things_images[self.selecting] = None
                self.things_kind[self.selecting] = []
                self.things_num -= 1
                if self.showing == self.selecting:
                    self.showing = -1
                self.selecting = -1

    def move_end(self, box):  # 移动物品结束
        self.move_enable = 0
        if not self.moving:
            return
        self.moving = 0
        target = -1
        # 求被移动物品图像中心位置
        thing_width_half = (self.things_rects[self.selecting][1][0] - self.things_rects[self.selecting][0][0]) // 2
        thing_height_half = (self.things_rects[self.selecting][1][1] - self.things_rects[self.selecting][0][1]) // 2
        x = self.things_rects[self.selecting][2][0] + thing_width_half
        y = self.things_rects[self.selecting][2][1] + thing_height_half
        self.things_rects[self.selecting][2] = list(self.things_rects[self.selecting][0])
        # 确定移动的目的地格子在背包中的位置
        for i in range(self.space):
            if i != self.selecting:
                if self.things_rects[i][0][0] <= x < self.things_rects[i][1][0]:
                    if self.things_rects[i][0][1] <= y < self.things_rects[i][1][1]:
                        target = i
                        break
        if target == self.selecting:  # 移动目的格子为原格子，相当于没有移动
            return
        if target >= 0:  # 移动到背包内其他格子的情况
            if not self.things[target]:  # 目标格子为空
                self.move_to_bag_empty(target)
            else:  # 目标格子不为空
                same = len(self.things_kind[self.selecting]) == len(self.things_kind[target])
                if same:  # 判断两个格子的物品种类是否一致
                    for i in range(len(self.things_kind[target]) - 2):
                        if self.things_kind[self.selecting][i] != self.things_kind[target][i]:
                            same = False
                            break
                if not same:  # 物品种类不一致
                    self.move_to_bag_not_empty_not_same(target)
                else:  # 物品种类一致
                    self.move_to_bag_not_empty_same(target)
        elif box:  # 检测是否移动到宝箱中
            # 穿戴中的装备不能直接丢弃到宝箱中
            for i in self.equip_wear:
                if self.selecting == i:
                    return
            # 确定移动的目的地格子在宝箱中的位置
            for i in range(box.space):
                if box.things_rects[i][0][0] <= x < box.things_rects[i][1][0]:
                    if box.things_rects[i][0][1] <= y < box.things_rects[i][1][1]:
                        target = i
                        break
            if target < 0:  # 移动无效
                return
            else:
                if not box.things[target]:  # 该宝箱格子为空
                    self.move_to_box_empty(box, target)
                else:  # 该宝箱格子不为空
                    same = len(self.things_kind[self.selecting]) == len(box.things_kind[target])
                    if same:  # 判断两个格子的物品种类是否一致
                        for i in range(len(self.things_kind[self.selecting]) - 2):
                            if self.things_kind[self.selecting][i] != box.things_kind[target][i]:
                                same = False
                                break
                    if not same:  # 物品种类不一致
                        self.move_to_box_not_empty_not_same(box, target)
                    else:  # 物品种类一致
                        self.move_to_box_not_empty_same(box, target)
