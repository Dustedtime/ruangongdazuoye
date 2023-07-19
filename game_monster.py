import random

from game_creature import Creature

import pygame

from game_equipment import Bullet


class Monster(Creature):  # 定义怪物类
    def __init__(self, dictionary, screen_width, screen_height):
        Creature.__init__(self, dictionary, screen_width, screen_height)  # 调用父类初始化
        self.move_time = pygame.time.get_ticks()  # 怪物上次更新移动方向的时间
        self.move_time_gap = dictionary['move_time_gap']  # 怪物移动方向更新的时间
        self.move_time_pause = -1  # 暂停页面加载瞬间的时间差，用于从暂停页面恢复游戏正常页面时计算当前改变移动方向剩余冷却时间
        self.backshake = dictionary['backshake']  # 怪物攻击后摇
        self.chasing = 0  # 怪物是否追逐角色
        self.chasing_gap = dictionary['chasing_gap']  # 用于判断怪物与英雄之间是否隔墙的丈量步长，越小越准确
        self.flying = dictionary['flying']  # 怪物是否属于飞行类，用于判断怪物站定时是否需要继续刷新帧率，以维持飞行状态
        self.withdraw_speed = dictionary['withdraw_speed'] * screen_height  # 怪物撤退速度
        self.attacked_sword = dictionary['attacked_sword']  # 判断怪物是否被剑气击中过，用来防止怪物被一个剑气重复击中
        self.kind = dictionary['kind']  # 怪物种类，用于辅助保存怪物数据
        self.weapon_kind = dictionary['weapon_kind']  # 怪物武器种类
        self.weapon_num = dictionary['weapon_num']  # 怪物武器编号
        self.rect_temp = [self.rect.x, self.rect.y]  # 怪物移动过程中位置的更新，使用临时列表存储更为精确的坐标(rect会自动约)
        self.range_max = dictionary['follow_range_max']  # 记录怪物跟踪范围上限
        self.range_middle = dictionary['follow_range_middle']  # 记录怪物跟踪静止范围
        self.range_min = dictionary['follow_range_min']  # 记录怪物跟踪范围下限

    def draw(self, screen):  # 更新怪物图像
        screen.blit(self.image, self.rect)

    def update(self, x, y, game_map, ani, hero, screen_height, monster_bullets, monsters, harm):  # 更新怪物位置，参数x和y为地图偏移量
        self.move(hero.rect, game_map)
        self.collide_monster(monsters)  # 怪物之间的碰撞检测，防止怪物完全重叠
        # 使用临时列表更新更为准确的坐标
        self.rect_temp[0] += x + self.movex
        self.rect_temp[1] += y + self.movey
        self.rect.x = self.rect_temp[0]
        self.rect.y = self.rect_temp[1]

        # 计算怪物的朝向，刷新怪物图像帧数
        direction = 0
        if self.movex < 0:
            direction = 4
        elif self.movex > 0:
            direction = 8
        elif self.movey < 0:
            direction = 12
        if self.chasing:
            x_sub = self.rect.centerx - hero.rect.centerx
            y_sub = self.rect.centery - hero.rect.centery
            if x_sub <= 0:
                if abs(y_sub) <= abs(x_sub):
                    direction = 8
                elif y_sub < 0:
                    direction = 0
                else:
                    direction = 12
            else:
                if abs(y_sub) <= abs(x_sub):
                    direction = 4
                elif y_sub < 0:
                    direction = 0
                else:
                    direction = 12
        if self.movex or self.movey:  # 怪物移动，刷新帧数
            self.frame += 1
            if self.frame >= 4 * ani:
                self.frame = 0
            self.image = self.images[self.frame // ani + direction]

        # 记录坐标修正前的坐标
        x_temp = self.rect.x
        y_temp = self.rect.y
        walls = pygame.sprite.spritecollide(self, game_map.walls, False)
        if self.movey < 0:  # 怪物拥有向上速度
            if self.movex == 0:  # 怪物没有横向速度
                for wall in walls:  # 进行精灵碰撞检测，如有碰撞则修正坐标
                    if wall:
                        self.rect.y = wall.rect.bottom
                        break
            elif self.movex < 0:  # 怪物拥有向左速度
                # 怪物斜向移动时，碰撞情况有多种，须分开讨论
                if len(walls) == 1:  # 仅与一面墙发生碰撞
                    if walls[0].rect.bottom - self.rect.y < walls[0].rect.right - self.rect.x:
                        self.rect.y = walls[0].rect.bottom
                    elif walls[0].rect.bottom - self.rect.y > walls[0].rect.right - self.rect.x:
                        self.rect.x = walls[0].rect.right
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
            else:  # 怪物拥有向右速度
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
            if self.movex == 0:
                for wall in pygame.sprite.spritecollide(self, game_map.walls, False):
                    if wall:
                        self.rect.bottom = wall.rect.y
                        break
            elif self.movex < 0:
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
                for wall in pygame.sprite.spritecollide(self, game_map.walls, False):
                    if wall:
                        self.rect.x = wall.rect.right
                        break
            elif self.movex > 0:
                for wall in pygame.sprite.spritecollide(self, game_map.walls, False):
                    if wall:
                        self.rect.right = wall.rect.x
                        break
            else:
                if self.flying:  # 怪物属于飞行种类，悬停时仍然刷新帧率，形成飞行效果
                    self.frame += 1
                    if self.frame >= 4 * ani:
                        self.frame = 0
                    self.image = self.images[self.frame // ani + direction]

        # 更新临时坐标列表和怪物移动方向
        if self.rect.x != x_temp:
            self.rect_temp[0] += self.rect.x - x_temp
            self.movex = -self.movex
        if self.rect.y != y_temp:
            self.rect_temp[1] += self.rect.y - y_temp
            self.movey = -self.movey
        if self.chasing:  # 怪物攻击
            time_now = pygame.time.get_ticks()
            if time_now - self.attack_time >= self.backshake:
                self.attack_time = time_now
                monster_bullets.add(self.attack((hero.rect.centerx, hero.rect.centery), screen_height))

    def collide_monster(self, monsters):  # 怪物之间的碰撞检测，防止怪物完全叠在一起
        for monster in pygame.sprite.spritecollide(self, monsters, False):
            if monster != self:
                if pygame.sprite.collide_mask(self, monster):
                    if self.movex > 0:
                        if monster.rect.centerx > self.rect.centerx:
                            self.movex = 0
                    else:
                        if monster.rect.centerx < self.rect.centerx:
                            self.movex = 0
                    if self.movey > 0:
                        if monster.rect.centery > self.rect.centery:
                            self.movey = 0
                    else:
                        if monster.rect.centery < self.rect.centery:
                            self.movey = 0

    def move(self, hero_rect, game_map):  # 怪物移动
        # 怪物与角色的距离，判断是否进行跟随
        distance = (abs(self.rect.centerx - hero_rect.centerx)) ** 2 + (abs(self.rect.centery - hero_rect.centery)) ** 2
        if distance <= self.range_min:
            self.chasing = 3
        elif distance <= self.range_middle:
            self.chasing = 2
        elif distance <= self.range_max:
            self.chasing = 1
        else:
            self.chasing = 0
        if self.chasing:  # 怪物跟随角色
            chasing_enable = 1
            # 判断怪物和英雄之间是否隔墙
            x_gap = hero_rect.centerx - self.rect.centerx
            y_gap = hero_rect.centery - self.rect.centery
            x_monster = self.rect.centerx - game_map.left
            y_monster = self.rect.centery - game_map.top
            x_hero = hero_rect.centerx - game_map.left
            y_hero = hero_rect.centery - game_map.top
            width = game_map.wall_width
            if x_gap == 0 and y_gap == 0:
                self.follow(hero_rect)
                return
            elif abs(x_gap) >= abs(y_gap):
                if x_gap < 0:
                    x_div = -self.chasing_gap
                else:
                    x_div = self.chasing_gap
                y_div = y_gap * x_div / x_gap
            else:
                if y_gap < 0:
                    y_div = -self.chasing_gap
                else:
                    y_div = self.chasing_gap
                x_div = x_gap * y_div / y_gap
            while True:
                if x_div < 0 and y_div < 0 and (x_monster < x_hero or y_monster < y_hero):
                    break
                elif x_div < 0 <= y_div and (x_monster < x_hero or y_monster > y_hero):
                    break
                elif x_div >= 0 > y_div and (x_monster > x_hero or y_monster < y_hero):
                    break
                elif x_div >= 0 and y_div >= 0 and (x_monster > x_hero or y_monster > y_hero):
                    break
                # 隔墙，追踪标志置零
                if 0 < game_map.layout_data[int(y_monster // width)][int(x_monster // width)] < 3:
                    chasing_enable = 0
                    break
                x_monster += x_div
                y_monster += y_div
            if chasing_enable:
                self.follow(hero_rect)
                return
            else:
                self.chasing = 0
        time_now = pygame.time.get_ticks()
        if time_now - self.move_time < self.move_time_gap:
            return
        else:  # 未注意到角色，随机移动
            self.move_time = time_now
            self.movex = random.uniform(-self.max_speed, self.max_speed)
            self.movey = random.uniform(-self.max_speed, self.max_speed)

    def follow(self, hero_rect):  # 怪物发现角色后的移动
        hero_x, hero_y = hero_rect.centerx, hero_rect.centery
        monster_x, monster_y = self.rect.centerx, self.rect.centery
        x_gap = abs(hero_x - monster_x)
        y_gap = abs(hero_y - monster_y)
        if self.chasing == 1:  # 追逐
            if x_gap >= y_gap:
                speed_x = self.max_speed
                speed_y = speed_x * y_gap / x_gap
            else:
                speed_y = self.max_speed
                speed_x = speed_y * x_gap / y_gap
            if monster_x + speed_x <= hero_x:
                self.movex = speed_x
            elif monster_x - speed_x >= hero_x:
                self.movex = -speed_x
            else:
                self.movex = hero_x - monster_x
            if monster_y + speed_y <= hero_y:
                self.movey = speed_y
            elif monster_y - speed_y >= hero_y:
                self.movey = -speed_y
            else:
                self.movey = hero_y - monster_y
        elif self.chasing == 2:  # 站定攻击
            self.movex = 0
            self.movey = 0
        else:  # 与角色拉开距离（远战敌人警戒距离较大，近战警戒距离小）
            if monster_x <= hero_x:
                self.movex = -self.withdraw_speed
            else:
                self.movex = self.withdraw_speed
            if monster_y <= hero_y:
                self.movey = -self.withdraw_speed
            else:
                self.movey = self.withdraw_speed

    def attack(self, hero_pos, screen_height):  # 攻击
        if self.weapon_kind == 1:
            pass
        elif self.weapon_kind == 2:
            return Bullet(self.rect, hero_pos, self.strength, self.weapon_num, screen_height)

    def attacked(self, strength, harm):  # 怪物被击中
        if strength > self.defence:  # 攻击高于防御，对怪物造成伤害
            self.health -= strength - self.defence
            harm.add_harm(strength - self.defence, self.rect)  # 伤害数值显示
        else:
            harm.add_harm(0, self.rect)
        if self.health <= 0:  # 怪物死亡
            return 1
        else:
            return 0

    def dead(self, hero):
        hero.money += self.money
        hero.exp += self.exp
        self.kill()
