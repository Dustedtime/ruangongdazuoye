import pygame
from game_bullet import Bullet


class Creature:  # 生物类
    def __init__(self, dictionary):  # 字典dictionary里面存有要实例化的对象的属性
        self.health = dictionary['health']  # 当前生命值
        self.strength = dictionary['strength']  # 攻击力
        self.defence = dictionary['defence']  # 防御力
        self.speed = dictionary['speed']  # 速度
        self.money = dictionary['speed']  # 金币值，若为角色，则代表身上金币数量，若为怪物则代表击杀怪物获得的金币数量
        self.exp = dictionary['exp']  # 经验值，解释同金币
        self.position = dictionary['position']  # 位置
        self.direction = dictionary['direction']  # 角色朝向，0-8分别代表八个方向
        self.attack_time = dictionary['attack_time']  # 上次攻击的时间戳，结合后摇判断对象当前是否能攻击
        self.image = dictionary['image']  # 对象的图像

    def attacked(self, bullet):  # 被攻击，需要用到子弹对象
        self.health -= (bullet.strength - self.defence + abs(bullet.strength - self.defence)) // 2  # 计算被攻击者受到攻击后剩余生命值
        if self.health <= 0:  # 死亡
            pass

    def draw(self, screen):  # 将对象绘制在屏幕上
        screen.blit(self.image, self.position)

    def attack(self, weapon):  # 根据使用的武器和攻击者属性返回实例化子弹对象
        if pygame.time.get_ticks() - self.attack_time >= weapon.backshake:  # 判断是否仍处于后摇阶段
            self.attack_time = pygame.time.get_ticks()  # 更新最新攻击时间
            return Bullet(self.position, self.direction, self.strength, weapon.kind)

    def move(self, game_map):  # 移动
        pass

    def load_data(self):  # 加载数据
        pass
