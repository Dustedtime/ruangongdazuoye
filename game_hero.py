import json
import os

import pygame

from game_bag import Bag
from game_creature import Creature
from game_equipment import Bullet, SwordAttack


class Hero(Creature):  # 角色类
    def __init__(self, dictionary, setting, screen_width, screen_height, archival):
        Creature.__init__(self, dictionary, screen_width, screen_height)  # 调用父类初始化
        self.level = dictionary['level']  # 等级
        self.max_health = dictionary['max_health']  # 最大生命值
        self.max_exp = dictionary['max_exp']  # 当前等级升级需要最大经验值
        self.speed = self.max_speed  # 角色当前速度
        self.choose = 0  # 武器帧数选择
        self.stair_status = 0  # 角色靠近楼梯标号（决定按下空格键是上楼梯、下楼梯还是无操作）
        self.door_enable = 1.5 * self.size[0]  # 角色最远开门距离
        self.defensing = 0  # 角色处于持盾防御状态的标志

        self.left_max = dictionary['left_max'] * screen_width  # 向左移动时触发地图移动的极限坐标，下面三个类似
        self.right_min = dictionary['right_min'] * screen_width
        self.top_max = dictionary['top_max'] * screen_height
        self.bottom_min = dictionary['bottom_min'] * screen_height

        self.status = Status(screen_width, screen_height, self)  # 角色状态栏
        self.bag = Bag(setting, archival, self.size[0], self.rect)  # 背包
        self.weapon = None  # 角色武器
        self.shield = None  # 角色盾牌
        self.jewel = None  # 角色宝石
        self.bullets = pygame.sprite.Group()
        self.sword_attack = pygame.sprite.Group()
        self.load_weapon()

    def load_weapon(self):  # 加载装备中的武器
        if self.bag.equip_wear[0] >= 0:
            self.weapon = self.bag.things[self.bag.equip_wear[0]]
            self.weapon.update(self.rect, self.choose)
        else:
            self.weapon = None

    def load_shield(self):  # 加载装备中的盾牌

        pass

    def load_jewel(self):  # 加载装备中的宝石
        pass

    def draw(self, screen):  # 更新角色图像
        screen.blit(self.image, self.rect)
        if self.weapon and not self.defensing:
            self.weapon.draw(screen)  # 绘制持有武器
        if self.shield and self.defensing:
            pass
        self.status.draw(screen)  # 绘制人物状态栏
        self.bag.draw(screen)  # 绘制背包栏

    def control(self):  # 控制角色移动
        key_list = pygame.key.get_pressed()
        self.movex = self.speed * (key_list[pygame.K_d] - key_list[pygame.K_a])
        self.movey = self.speed * (key_list[pygame.K_s] - key_list[pygame.K_w])

    def update(self, game_map, ani, monsters, monster_bullets, screen_height, screen_width, harm):  # 更新角色坐标
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        # 下面依次从各种情况判断角色与墙的碰撞情况，修正角色坐标，以避免卡墙
        if self.movey < 0:  # 角色拥有向上速度
            self.frame += 1  # 调节角色图像所在帧
            if self.frame >= 4 * ani:
                self.frame = 0
            self.image = self.images[self.frame // ani + 12]
            if self.movex == 0:  # 角色没有横向速度
                for wall in pygame.sprite.spritecollide(self, game_map.walls, False):  # 进行精灵碰撞检测，如有碰撞则修正坐标
                    self.rect.y = wall.rect.bottom
                    break
            elif self.movex < 0:  # 角色拥有向左速度
                self.image = self.images[self.frame // ani + 4]
                walls = pygame.sprite.spritecollide(self, game_map.walls, False)  # 角色斜向移动时，碰撞情况有多种，须分开讨论
                if len(walls) == 1:  # 仅与一面墙发生碰撞
                    if walls[0].rect.right - self.rect.x < walls[0].rect.bottom - self.rect.y:
                        self.rect.x = walls[0].rect.right
                    elif walls[0].rect.right - self.rect.x > walls[0].rect.bottom - self.rect.y:
                        self.rect.y = walls[0].rect.bottom
                    else:
                        self.rect.y = walls[0].rect.bottom
                        self.rect.x = walls[0].rect.right
                elif len(walls) > 1:  # 与不止一面墙发生碰撞
                    if min(wall.rect.x for wall in walls) == max(wall.rect.x for wall in walls):
                        self.rect.x = walls[0].rect.right
                    elif min(wall.rect.y for wall in walls) == max(wall.rect.y for wall in walls):
                        self.rect.y = walls[0].rect.bottom
                    else:
                        self.rect.x = min(wall.rect.right for wall in walls)
                        self.rect.y = min(wall.rect.bottom for wall in walls)
            else:  # 角色拥有向右速度
                self.image = self.images[self.frame // ani + 8]
                walls = pygame.sprite.spritecollide(self, game_map.walls, False)
                if len(walls) == 1:  # 仅与一面墙发生碰撞
                    if self.rect.right - walls[0].rect.x < walls[0].rect.bottom - self.rect.y:
                        self.rect.right = walls[0].rect.x
                    elif self.rect.right - walls[0].rect.x > walls[0].rect.bottom - self.rect.y:
                        self.rect.y = walls[0].rect.bottom
                    else:
                        self.rect.y = walls[0].rect.bottom
                        self.rect.right = walls[0].rect.x
                elif len(walls) > 1:  # 与不止一面墙发生碰撞
                    if min(wall.rect.x for wall in walls) == max(wall.rect.x for wall in walls):
                        self.rect.right = walls[0].rect.x
                    elif min(wall.rect.y for wall in walls) == max(wall.rect.y for wall in walls):
                        self.rect.y = walls[0].rect.bottom
                    else:
                        self.rect.right = max(wall.rect.x for wall in walls)
                        self.rect.y = min(wall.rect.bottom for wall in walls)
        # 下面情况与上面类似，不再注释
        elif self.movey > 0:
            self.frame += 1
            if self.frame >= 4 * ani:
                self.frame = 0
            self.image = self.images[self.frame // ani]
            if self.movex == 0:
                for wall in pygame.sprite.spritecollide(self, game_map.walls, False):
                    self.rect.bottom = wall.rect.y
                    break
            elif self.movex < 0:
                self.image = self.images[self.frame // ani + 4]
                walls = pygame.sprite.spritecollide(self, game_map.walls, False)
                if len(walls) == 1:
                    if self.rect.bottom - walls[0].rect.y < walls[0].rect.right - self.rect.x:
                        self.rect.bottom = walls[0].rect.y
                    elif self.rect.bottom - walls[0].rect.y > walls[0].rect.right - self.rect.x:
                        self.rect.x = walls[0].rect.right
                    else:
                        self.rect.bottom = walls[0].rect.y
                        self.rect.x = walls[0].rect.right
                elif len(walls) > 1:
                    if min(wall.rect.x for wall in walls) == max(wall.rect.x for wall in walls):
                        self.rect.x = walls[0].rect.right
                    elif min(wall.rect.y for wall in walls) == max(wall.rect.y for wall in walls):
                        self.rect.bottom = walls[0].rect.y
                    else:
                        self.rect.x = min(wall.rect.right for wall in walls)
                        self.rect.bottom = max(wall.rect.y for wall in walls)
            else:
                self.image = self.images[self.frame // ani + 8]
                walls = pygame.sprite.spritecollide(self, game_map.walls, False)
                if len(walls) == 1:
                    if self.rect.right - walls[0].rect.x < self.rect.bottom - walls[0].rect.y:
                        self.rect.right = walls[0].rect.x
                    elif self.rect.right - walls[0].rect.x > self.rect.bottom - walls[0].rect.y:
                        self.rect.bottom = walls[0].rect.y
                    else:
                        self.rect.bottom = walls[0].rect.y
                        self.rect.right = walls[0].rect.x
                elif len(walls) > 1:
                    if min(wall.rect.x for wall in walls) == max(wall.rect.x for wall in walls):
                        self.rect.right = walls[0].rect.x
                    elif min(wall.rect.y for wall in walls) == max(wall.rect.y for wall in walls):
                        self.rect.bottom = walls[0].rect.y
                    else:
                        self.rect.right = max(wall.rect.x for wall in walls)
                        self.rect.bottom = max(wall.rect.y for wall in walls)
        else:
            if self.movex < 0:
                self.frame += 1
                if self.frame >= 4 * ani:
                    self.frame = 0
                self.image = self.images[self.frame // ani + 4]
                for wall in pygame.sprite.spritecollide(self, game_map.walls, False):
                    self.rect.x = wall.rect.right
                    break
            elif self.movex > 0:
                self.frame += 1
                if self.frame >= 4 * ani:
                    self.frame = 0
                self.image = self.images[self.frame // ani + 8]
                for wall in pygame.sprite.spritecollide(self, game_map.walls, False):
                    self.rect.right = wall.rect.x
                    break

        # 角色与楼梯精灵类的碰撞检测
        stairs = pygame.sprite.spritecollide(self, game_map.stairs, False)
        if not stairs:
            self.stair_status = 0
        elif game_map.layout_data[int((stairs[0].rect.y - game_map.top) // game_map.wall_width)][int(
                (stairs[0].rect.x - game_map.left) // game_map.wall_width)] == 3:
            self.stair_status = -1
        else:
            self.stair_status = 1

        # 下面判断角色移动是否触发地图整体的移动
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

        # 下面更新角色拥有的一些对象的坐标等信息
        self.sword_attack_exist(monsters)  # 判断剑气是否到达存在时间
        choose = self.frame // ani
        if self.movex:
            if self.movex < 0:
                choose += 4
            else:
                choose += 8
        else:
            if self.movey < 0:
                choose += 12
            elif self.movey == 0:
                choose = self.choose
        self.choose = choose
        if self.weapon:
            self.weapon.update(self.rect, self.choose)  # 更新手持武器的坐标
        return x_change, y_change  # 返回地图需要移动的距离

    def attack(self, screen_height, pos):  # 角色攻击
        self.bag.selecting = -1
        if not self.weapon:
            return
        time_now = pygame.time.get_ticks()
        if self.attack_time + self.weapon.backshake <= time_now:  # 后摇时间已过，可以攻击
            self.attack_time = time_now  # 更新最近攻击时间
            if self.weapon.kind == 1:  # 近战
                # noinspection PyTypeChecker
                self.sword_attack.add(SwordAttack(self.rect, pos, self.strength + self.weapon.strength, screen_height))
            else:  # 远战
                # noinspection PyTypeChecker
                self.bullets.add(
                    Bullet(self.rect, pos, self.strength + self.weapon.strength, self.weapon.num, screen_height))

    def attacked(self, strength, harm):  # 英雄被击中
        if strength > self.defence:  # 攻击高于防御，对英雄造成伤害
            self.health -= strength - self.defence
            harm.add_harm(strength - self.defence, self.rect)  # 伤害数值显示
        else:
            harm.add_harm(0, self.rect)
        return 0

    def sword_attack_exist(self, monsters):  # 检测剑气存在时间是否已达上限
        if self.sword_attack:
            time_now = pygame.time.get_ticks()
            for attack in self.sword_attack:
                if time_now >= attack.end:
                    self.sword_attack.remove(attack)
                    for monster in monsters:
                        monster.attacked_sword = 0  # 更新怪物能否被剑气击中的标志

    def change_weapon(self, direction):  # 更换手持的武器
        if self.bag.equip_wear[0] < 0:
            return
        pos = self.bag.equip_wear[0]
        for i in range(self.bag.space):
            pos = (pos + direction + self.bag.space) % self.bag.space
            if self.bag.things_kind[pos]:
                if self.bag.things_kind[pos][0] == 1:
                    if self.bag.equip_wear[0] == pos:
                        return
                    self.bag.change_weapon_wear(pos)
                    self.load_weapon()
                    return
        self.bag.equip_wear[0] = -1
        self.load_weapon()

    def unlock(self, x, y, tip, game_map):  # 开门
        self.bag.selecting = -1
        for i in range(self.bag.space):
            if self.bag.things_kind[i] and self.bag.things_kind[i][0] == 4 and self.bag.things_kind[i][1] == 1:
                for j in range(x - 1, x + 2):
                    for k in range(y - 1, y + 2):
                        if 0 <= j < len(game_map.layout_data[0]) and 0 <= k < len(game_map.layout_data):
                            if game_map.layout_data[k][j] == 2:
                                game_map.layout_data[k][j] = 0
                game_map.init_layout()
                # 更新背包物品信息
                self.bag.things_kind[i][-1] -= 1
                self.bag.update(i)
                return
        tip.create_tip("缺少钥匙")

    def defense(self, status, kind):  # 防御，kind只有两种值：-1和1，-1表示取消防御，1表示开始防御
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
                     "攻击力:" + str(hero.strength), "防御力:" + str(hero.defence), "速度:" + str(hero.max_speed)]
        with open(os.path.join('page', 'page4', 'status.json'), 'r', encoding='utf-8') as f:  # 读取图像数据并更新页面相关信息
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
        with open(os.path.join('page', 'page4', 'status_words.json'), 'r', encoding='utf-8') as f:  # 读取文本数据并更新页面相关信息
            words = json.load(f)
            for i in range(len(words)):
                font = pygame.font.SysFont('SimSun', int(words[i][0] * screen_height))
                word_temp = font.render(self.info[i], True, tuple(words[i][3]))
                word_pos = word_temp.get_rect()
                word_pos.topleft = (words[i][2][0] * screen_width, words[i][2][1] * screen_height)
                self.words.append([word_temp, word_pos])

    def update(self, hero, screen_height, screen_width):  # 当角色数值发生变化时更新角色状态栏信息
        self.words = []
        self.info = ["等级:" + str(hero.level), "经验值:" + str(hero.exp) + "/" + str(hero.max_exp),
                     "生命值:" + str(hero.health) + "/" + str(hero.max_health), "金币:" + str(hero.money),
                     "攻击力:" + str(hero.strength), "防御力:" + str(hero.defence), "速度:" + str(hero.max_speed)]
        with open(os.path.join('page', 'page4', 'status_words.json'), 'r', encoding='utf-8') as f:  # 读取文本数据并更新页面相关信息
            words = json.load(f)
            for i in range(len(words)):
                font = pygame.font.SysFont('SimSun', int(words[i][0] * screen_height))
                word_temp = font.render(self.info[i], True, tuple(words[i][3]))
                word_pos = word_temp.get_rect()
                word_pos.topleft = (words[i][2][0] * screen_width, words[i][2][1] * screen_height)
                self.words.append([word_temp, word_pos])

    def draw(self, screen):  # 绘制状态栏
        for image in self.images:
            screen.blit(image[0], image[1])
        for word in self.words:
            screen.blit(word[0], word[1])
