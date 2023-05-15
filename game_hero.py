import json
import os

import pygame

from game_bag import Bag
from game_creature import Creature


class Hero(Creature):  # 角色类
    def __init__(self, dictionary, setting, screen_width, screen_height):
        Creature.__init__(self, dictionary, screen_width, screen_height)  # 调用父类初始化
        self.level = dictionary['level']  # 等级
        self.max_health = dictionary['max_health']  # 最大生命值
        self.max_exp = dictionary['max_exp']  # 当前等级升级需要最大经验值
        self.left_max = dictionary['left_max'] * screen_width  # 向左移动时触发地图移动的极限坐标，下面三个类似
        self.right_min = dictionary['right_min'] * screen_width
        self.top_max = dictionary['top_max'] * screen_height
        self.bottom_min = dictionary['bottom_min'] * screen_height
        self.status = Status(screen_width, screen_height, self)  # 角色状态栏
        self.bag = Bag(setting)  # 背包
        self.bullets = pygame.sprite.Group()

    def draw(self, screen):  # 更新角色图像
        screen.blit(self.image, self.rect)
        self.status.draw(screen)
        self.bag.draw(screen)

    def control(self):  # 控制角色移动
        key_list = pygame.key.get_pressed()
        self.movex = self.speed * (key_list[pygame.K_d] - key_list[pygame.K_a])
        self.movey = self.speed * (key_list[pygame.K_s] - key_list[pygame.K_w])

    def update(self, game_map, ani):  # 更新角色坐标
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        # 下面依次从各种情况判断角色与墙的碰撞情况，修正角色坐标，以避免卡墙
        if self.movey < 0:  # 角色拥有向下速度
            self.frame += 1  # 调节角色图像所在帧
            if self.frame >= 4 * ani:
                self.frame = 0
            self.image = self.images[self.frame // ani + 12]
            if self.movex == 0:  # 角色没有横向速度
                for wall in pygame.sprite.spritecollide(self, game_map.walls, False):  # 进行精灵碰撞检测，如有碰撞则修正坐标
                    self.rect.y = wall.rect.y + game_map.wall_width
            elif self.movex < 0:  # 角色拥有向左速度
                self.image = self.images[self.frame // ani + 4]
                walls = pygame.sprite.spritecollide(self, game_map.walls, False)  # 角色斜向移动时，碰撞情况有多种，须分开讨论
                if len(walls) == 1:  # 仅与一面墙发生碰撞
                    if self.rect.x - walls[0].rect.x < self.rect.y - walls[0].rect.y:
                        self.rect.y = walls[0].rect.y + game_map.wall_width
                    elif self.rect.x - walls[0].rect.x > self.rect.y - walls[0].rect.y:
                        self.rect.x = walls[0].rect.x + game_map.wall_width
                    else:
                        self.rect.y = walls[0].rect.y + game_map.wall_width
                        self.rect.x = walls[0].rect.x + game_map.wall_width
                elif len(walls) == 2:  # 与两面墙发生碰撞
                    if walls[0].rect.x == walls[1].rect.x:
                        self.rect.x = walls[0].rect.x + game_map.wall_width
                    else:
                        self.rect.y = walls[0].rect.y + game_map.wall_width
                elif len(walls) == 3:  # 与三面墙发生碰撞
                    self.rect.x = (walls[0].rect.x + walls[1].rect.x + walls[2].rect.x + game_map.wall_width * 2) // 3
                    self.rect.y = (walls[0].rect.y + walls[1].rect.y + walls[2].rect.y + game_map.wall_width * 2) // 3
            else:  # 角色拥有向右速度
                self.image = self.images[self.frame // ani + 8]
                walls = pygame.sprite.spritecollide(self, game_map.walls, False)
                if len(walls) == 1:  # 仅与一面墙发生碰撞
                    if self.rect.x - walls[0].rect.x < walls[0].rect.y - self.rect.y:
                        self.rect.x = walls[0].rect.x - game_map.wall_width
                    elif self.rect.x - walls[0].rect.x > walls[0].rect.y - self.rect.y:
                        self.rect.y = walls[0].rect.y + game_map.wall_width
                    else:
                        self.rect.y = walls[0].rect.y + game_map.wall_width
                        self.rect.x = walls[0].rect.x - game_map.wall_width
                elif len(walls) == 2:  # 与两面墙发生碰撞
                    if walls[0].rect.x == walls[1].rect.x:
                        self.rect.x = walls[0].rect.x - game_map.wall_width
                    else:
                        self.rect.y = walls[0].rect.y + game_map.wall_width
                elif len(walls) == 3:  # 与三面墙发生碰撞
                    self.rect.x = (walls[0].rect.x + walls[1].rect.x + walls[2].rect.x - game_map.wall_width * 2) // 3
                    self.rect.y = (walls[0].rect.y + walls[1].rect.y + walls[2].rect.y + game_map.wall_width * 2) // 3
        # 下面情况与上面类似，不再注释
        elif self.movey > 0:
            self.frame += 1
            if self.frame >= 4 * ani:
                self.frame = 0
            self.image = self.images[self.frame // ani]
            if self.movex == 0:
                for wall in pygame.sprite.spritecollide(self, game_map.walls, False):
                    self.rect.y = wall.rect.y - game_map.wall_width
            elif self.movex < 0:
                self.image = self.images[self.frame // ani + 4]
                walls = pygame.sprite.spritecollide(self, game_map.walls, False)
                if len(walls) == 1:
                    if self.rect.x - walls[0].rect.x < walls[0].rect.y - self.rect.y:
                        self.rect.y = walls[0].rect.y - game_map.wall_width
                    elif self.rect.x - walls[0].rect.x > walls[0].rect.y - self.rect.y:
                        self.rect.x = walls[0].rect.x + game_map.wall_width
                    else:
                        self.rect.y = walls[0].rect.y - game_map.wall_width
                        self.rect.x = walls[0].rect.x + game_map.wall_width
                elif len(walls) == 2:
                    if walls[0].rect.x == walls[1].rect.x:
                        self.rect.x = walls[0].rect.x + game_map.wall_width
                    else:
                        self.rect.y = walls[0].rect.y - game_map.wall_width
                elif len(walls) == 3:
                    self.rect.x = (walls[0].rect.x + walls[1].rect.x + walls[2].rect.x + game_map.wall_width * 2) // 3
                    self.rect.y = (walls[0].rect.y + walls[1].rect.y + walls[2].rect.y - game_map.wall_width * 2) // 3
            else:
                self.image = self.images[self.frame // ani + 8]
                walls = pygame.sprite.spritecollide(self, game_map.walls, False)
                if len(walls) == 1:
                    if self.rect.x - walls[0].rect.x < self.rect.y - walls[0].rect.y:
                        self.rect.x = walls[0].rect.x - game_map.wall_width
                    elif self.rect.x - walls[0].rect.x > self.rect.y - walls[0].rect.y:
                        self.rect.y = walls[0].rect.y - game_map.wall_width
                    else:
                        self.rect.y = walls[0].rect.y - game_map.wall_width
                        self.rect.x = walls[0].rect.x - game_map.wall_width
                elif len(walls) == 2:
                    if walls[0].rect.x == walls[1].rect.x:
                        self.rect.x = walls[0].rect.x - game_map.wall_width
                    else:
                        self.rect.y = walls[0].rect.y - game_map.wall_width
                elif len(walls) == 3:
                    self.rect.x = (walls[0].rect.x + walls[1].rect.x + walls[2].rect.x - game_map.wall_width * 2) // 3
                    self.rect.y = (walls[0].rect.y + walls[1].rect.y + walls[2].rect.y - game_map.wall_width * 2) // 3
        else:
            self.frame += 1
            if self.frame >= 4 * ani:
                self.frame = 0
            if self.movex < 0:
                self.image = self.images[self.frame // ani + 4]
                for wall in pygame.sprite.spritecollide(self, game_map.walls, False):
                    self.rect.x = wall.rect.x + game_map.wall_width
            elif self.movex > 0:
                self.image = self.images[self.frame // ani + 8]
                for wall in pygame.sprite.spritecollide(self, game_map.walls, False):
                    self.rect.x = wall.rect.x - game_map.wall_width
        x_change = 0
        y_change = 0
        if self.rect.x < self.left_max:  # 判断角色坐标是否超出触发地图移动的极限，下面三个同理
            x_change = self.left_max - self.rect.x  # 此时只需移动地图，角色不必移动，计算得出地图需要移动的距离
            self.rect.x = self.left_max  # 再次修正角色坐标
            if game_map.left + x_change > game_map.left_max:  # 检测若如此移动，地图是否移动到边界。若是，则修正至刚好移动到边界
                self.rect.x -= x_change + game_map.left - game_map.left_max  # 因再次发生修正，角色坐标也需再次修正
                x_change = game_map.left_max - game_map.left  # 记录地图最终需要移动的距离
        elif self.rect.x + self.size[0] > self.right_min:
            x_change = -(self.rect.x + self.size[0] - self.right_min)
            self.rect.x = self.right_min - self.size[0]
            if game_map.right + x_change < game_map.right_min:
                self.rect.x += game_map.right_min - game_map.right - x_change
                x_change = game_map.right_min - game_map.right
        if self.rect.y < self.top_max:
            y_change = self.top_max - self.rect.y
            self.rect.y = self.top_max
            if game_map.top + y_change > game_map.top_max:
                self.rect.y -= y_change + game_map.top - game_map.top_max
                y_change = game_map.top_max - game_map.top
        elif self.rect.y + self.size[0] > self.bottom_min:
            y_change = -(self.rect.y + self.size[0] - self.bottom_min)
            self.rect.y = self.bottom_min - self.size[0]
            if game_map.bottom + y_change < game_map.bottom_min:
                self.rect.y += game_map.bottom_min - game_map.bottom - y_change
                y_change = game_map.bottom_min - game_map.bottom
        return x_change, y_change  # 返回地图需要移动的距离

    def defense(self, status, kind):  # 防御，kind只有两种值：-1和1，-1表示取消防御，1表示开始防御
        pass

    def stairs(self, game_map):  # 上下楼梯
        pass

    def talk(self, npc):  # 与npc交谈
        pass

    def door(self, game_map):  # 开门
        pass


class Status:  # 人物状态栏类
    def __init__(self, screen_width, screen_height, hero):
        self.info = []  # 状态栏信息
        self.images = []  # 图像列表
        self.words = []  # 文字列表
        self.init_data(screen_width, screen_height, hero)  # 初始化

    def init_data(self, screen_width, screen_height, hero):  # 初始化数据
        self.info = ["等级:" + str(hero.level), "经验值:" + str(hero.exp) + "/" + str(hero.max_exp),
                     "生命值:" + str(hero.health) + "/" + str(hero.max_health), "金币:" + str(hero.money),
                     "攻击力:" + str(hero.strength), "防御力:" + str(hero.defence), "速度:" + str(hero.speed)]
        with open(os.path.join('page', 'page4', 'status.json'), 'r') as f:  # 读取图像数据并更新页面相关信息
            images = json.load(f)
            for image in images:
                path = ''
                for directory_image in image[0]:
                    path = os.path.join(path, directory_image)
                size = (screen_width * image[2][0], screen_height * image[2][1])
                picture = pygame.transform.scale(pygame.image.load(path), size)
                picture_left_top_pos = (screen_width * image[1][0], screen_height * image[1][1])
                picture_right_bottom_pos = (picture_left_top_pos[0] + size[0], picture_left_top_pos[1] + size[1])
                self.images.append([picture, picture_left_top_pos, picture_right_bottom_pos])
        with open(os.path.join('page', 'page4', 'status_words.json'), 'r') as f:  # 读取文本数据并更新页面相关信息
            words = json.load(f)
            for i in range(len(words)):
                font = pygame.font.SysFont('SimSun', int(words[i][0] * screen_height))
                word_temp = font.render(self.info[i], True, tuple(words[i][3]))
                word_pos = word_temp.get_rect()
                word_pos.topleft = (words[i][2][0] * screen_width, words[i][2][1] * screen_height)
                self.words.append([word_temp, word_pos])

    def draw(self, screen):
        for image in self.images:
            screen.blit(image[0], image[1])
        for word in self.words:
            screen.blit(word[0], word[1])
