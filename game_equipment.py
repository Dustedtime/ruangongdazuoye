import json
import math
import os

import pygame


class Bullet(pygame.sprite.Sprite):  # 子弹类
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
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.speed = data['speed'] * screen_height
        self.size = (data['size'] * screen_height, data['size'] * screen_height)
        self.image = pygame.transform.scale(image, self.size)
        self.rect = self.image.get_rect()
        self.rect.center = (rect.centerx, rect.centery)  # 将计算得出的坐标赋给子弹图像的中心
        self.rect_temp = [float(rect.centerx), float(rect.centery)]

    def load_direction(self, pos, rect):  # 子弹射击方向
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


class SwordAttack(pygame.sprite.Sprite):  # 剑气类
    # rect:人物位置，确认攻击方向以及绘制的起始坐标
    # pos:鼠标点击坐标，确认攻击方向
    # strength:攻击力
    def __init__(self, rect, pos, strength, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.strength = strength  # 攻击力
        self.image = None
        self.rect = None
        self.start = pygame.time.get_ticks()  # 剑气发出开始的时间，配合self.end完成剑气的存在周期
        self.end = 0
        self.load_image(pos, screen_height, rect)  # 加载图像

    def load_image(self, pos, screen_height, rect):  # 加载剑气图像
        path = os.path.join('page', 'page4', 'sword_attack', 'image.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        path = ''
        for directory in data[0]:
            path = os.path.join(path, directory)
        image = pygame.image.load(path)
        size = (data[1] * screen_height, data[1] * screen_height)
        image = pygame.transform.scale(image, size)
        # 鼠标点击坐标与人物坐标的差
        dy = rect.centery - pos[1]
        dx = pos[0] - rect.centerx
        # 鼠标点击坐标与人物坐标连线与横坐标轴之间的弧度以及角度
        radian = math.atan2(dy, dx)
        angle = (radian * 180) / math.pi
        # 上面求出的弧度对应的sin和cos
        dy = -math.sin(radian)
        dx = math.sqrt(1 - dy ** 2)
        if angle >= 90 or angle <= -90:
            dx = -dx
        self.image = pygame.transform.rotate(image, angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = rect.centerx + dx * data[3] * screen_height
        self.rect.centery = rect.centery + dy * data[3] * screen_height
        self.end = self.start + data[2]  # 设置剑气消失时间

    def update(self, x_change, y_change):  # 剑气位置的更新
        self.rect.x += x_change
        self.rect.y += y_change


class Weapon:  # 武器类
    # kind:武器种类，分近战和远战
    # num:该种类下武器编号
    # width:使用者大小
    # rect:使用者位置
    def __init__(self, kind, num, width, rect):
        self.strength = 0  # 攻击力
        self.kind = kind  # 种类
        self.num = num  # 编号
        self.backshake = 0  # 武器后摇时间
        self.choose = 0  # 帧数定位
        self.sell_price = 0  # 出售价格
        self.buy_price = 0  # 购买价格
        self.images = []
        self.rects = []
        self.load_data(rect, width)
        self.image = None  # 当前选中要绘制的图像
        self.rect = None

    def load_data(self, rect, width):  # 根据种类读取文档信息获取武器图像等信息
        path = os.path.join('page', 'page4', 'thing', '1', str(self.kind), str(self.num), 'data.json')  # 武器信息文件路径
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.strength = data['strength']
        self.backshake = data['backshake']
        self.sell_price = data['sell_price']
        self.buy_price = data['buy_price']
        for image in data["image"]:  # 加载图片
            path = ''
            for directory in image[0]:
                path = os.path.join(path, directory)
            weapon_image = pygame.image.load(path)
            self.images.append(pygame.transform.scale(weapon_image, (image[1][0] * width, image[1][1] * width)))
            self.images[-1] = pygame.transform.rotate(self.images[-1], image[2])
            self.rects.append([])
            self.rects[-1].append(self.images[-1].get_rect())
            self.rects[-1].append((image[3][0] * width, image[3][1] * width))  # 武器图像偏移量
            self.rects[-1][0].x = rect.x + self.rects[-1][1][0]
            self.rects[-1][0].y = rect.y + self.rects[-1][1][1]

    def update(self, rect, choose):  # 根据角色移动以及英雄帧数进行武器移动
        self.choose = choose
        self.image = self.images[self.choose]
        self.rects[self.choose][0].x = rect.x + self.rects[self.choose][1][0]
        self.rects[self.choose][0].y = rect.y + self.rects[self.choose][1][1]
        self.rect = self.rects[self.choose][0]

    def draw(self, screen):  # 根据武器种类以及英雄帧数绘制武器
        screen.blit(self.image, self.rect)


class Shield:  # 盾牌类
    # num:盾牌编号
    # width:使用者大小
    # rect:使用者位置
    # screen_height:屏幕高度
    def __init__(self, num, width, screen_height, rect):
        self.defence = 0  # 防御力
        self.num = num  # 编号
        self.choose = 0  # 帧数定位
        self.speed_sub = 0  # 使用盾牌需要减少的速度
        self.sell_price = 0  # 出售价格
        self.buy_price = 0  # 购买价格
        self.images = []
        self.rects = []
        self.load_data(rect, width, screen_height)
        self.image = None  # 当前选中要绘制的图像
        self.rect = None

    def load_data(self, rect, width, screen_height):  # 根据盾牌编号读取文档信息获取盾牌图像等信息
        path = os.path.join('page', 'page4', 'thing', '2', str(self.num), 'data.json')  # 武器信息文件路径
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.defence = data['defence']
        self.speed_sub = data['speed_sub'] * screen_height
        self.sell_price = data['sell_price']
        self.buy_price = data['buy_price']
        for image in data["image"]:  # 加载图片
            path = ''
            for directory in image[0]:
                path = os.path.join(path, directory)
            weapon_image = pygame.image.load(path)
            self.images.append(pygame.transform.scale(weapon_image, (image[1][0] * width, image[1][1] * width)))
            self.images[-1] = pygame.transform.rotate(self.images[-1], image[2])
            self.rects.append([])
            self.rects[-1].append(self.images[-1].get_rect())
            self.rects[-1].append((image[3][0] * width, image[3][1] * width))  # 盾牌图像偏移量
            self.rects[-1][0].x = rect.x + self.rects[-1][1][0]
            self.rects[-1][0].y = rect.y + self.rects[-1][1][1]
