import os

import pygame
from game_equipment import Bullet


class Creature(pygame.sprite.Sprite):  # 生物类
    def __init__(self, dictionary, screen_width, screen_height):  # 字典dictionary里面存有要实例化的对象的属性
        pygame.sprite.Sprite.__init__(self)
        self.health = dictionary['health']  # 当前生命值
        self.strength = dictionary['strength']  # 攻击力
        self.defence = dictionary['defence']  # 防御力
        self.speed = dictionary['speed'] * screen_height  # 速度
        self.money = dictionary['money']  # 金币值，若为角色，则代表身上金币数量，若为怪物则代表击杀怪物获得的金币数量
        self.exp = dictionary['exp']  # 经验值，解释同金币
        self.movex = dictionary['movex']  # 横坐标上接着要移动的距离
        self.movey = dictionary['movey']  # 纵坐标上接着要移动的距离
        self.size = (screen_height * dictionary['size'], screen_height * dictionary['size'])  # 图像大小
        self.frame = dictionary['frame']  # 图像帧坐标
        self.direction = dictionary['direction']  # 角色朝向，0-8分别代表八个方向
        self.attack_time = dictionary['attack_time']  # 上次攻击的时间戳，结合后摇判断对象当前是否能攻击
        self.images = dictionary['images']  # 对象的图像
        self.load_image()
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (screen_width * dictionary['rect'][0], screen_height * dictionary['rect'][1])

    def load_image(self):
        num = len(self.images)
        for i in range(num):
            path = ''
            for directory in self.images[i]:
                path = os.path.join(path, directory)
            self.images[i] = pygame.transform.scale(pygame.image.load(path), self.size)

    def attacked(self, bullet):  # 被攻击，需要用到子弹对象
        self.health -= (bullet.strength - self.defence + abs(bullet.strength - self.defence)) // 2  # 计算被攻击者受到攻击后剩余生命值
        if self.health <= 0:  # 死亡
            pass

    def attack(self, kind, screen_height, pos):  # 根据使用的武器和攻击者属性返回实例化子弹对象
        bullet = Bullet(self.rect, pos, 1, kind, screen_height)
        return bullet
        # if pygame.time.get_ticks() - self.attack_time >= weapon.backshake:  # 判断是否仍处于后摇阶段
        #   self.attack_time = pygame.time.get_ticks()  # 更新最新攻击时间
        #  return Bullet(self.position, self.direction, self.strength, weapon.kind)
