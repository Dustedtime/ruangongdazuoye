import pygame

from game_creature import Creature


class Hero(Creature):  # 角色类
    def __init__(self, dictionary, setting):
        Creature.__init__(self, dictionary, setting)
        self.level = dictionary['level']  # 等级
        self.max_health = dictionary['max_health']  # 最大生命值
        self.left_max = dictionary['left_max'] * setting.screen_width
        self.right_max = dictionary['right_max'] * setting.screen_width
        self.top_max = dictionary['top_max'] * setting.screen_height
        self.bottom_max = dictionary['bottom_max'] * setting.screen_height
        # self.bag = dictionary['bag']  # 背包

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def control(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.movey -= self.speed
            elif event.key == pygame.K_s:
                self.movey += self.speed
            elif event.key == pygame.K_a:
                self.movex -= self.speed
            elif event.key == pygame.K_d:
                self.movex += self.speed

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.movey += self.speed
            elif event.key == pygame.K_s:
                self.movey -= self.speed
            elif event.key == pygame.K_a:
                self.movex += self.speed
            elif event.key == pygame.K_d:
                self.movex -= self.speed

    def update(self, group, ani, size):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        if self.movey < 0:
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = self.images[self.frame // ani + 12]
            if self.movex == 0:
                for wall in pygame.sprite.spritecollide(self, group, False):
                    self.rect.y = wall.rect.y + size
            elif self.movex < 0:
                self.image = self.images[self.frame // ani + 4]
                walls = pygame.sprite.spritecollide(self, group, False)
                if len(walls) == 1:
                    if self.rect.x - walls[0].rect.x < self.rect.y - walls[0].rect.y:
                        self.rect.y = walls[0].rect.y + size
                    elif self.rect.x - walls[0].rect.x > self.rect.y - walls[0].rect.y:
                        self.rect.x = walls[0].rect.x + size
                    else:
                        self.rect.y = walls[0].rect.y + size
                        self.rect.x = walls[0].rect.x + size
                elif len(walls) == 2:
                    if walls[0].rect.x == walls[1].rect.x:
                        self.rect.x = walls[0].rect.x + size
                    else:
                        self.rect.y = walls[0].rect.y + size
                elif len(walls) == 3:
                    self.rect.x = (walls[0].rect.x + walls[1].rect.x + walls[2].rect.x + size * 2) // 3
                    self.rect.y = (walls[0].rect.y + walls[1].rect.y + walls[2].rect.y + size * 2) // 3
            else:
                self.image = self.images[self.frame // ani + 8]
                walls = pygame.sprite.spritecollide(self, group, False)
                if len(walls) == 1:
                    if self.rect.x - walls[0].rect.x < walls[0].rect.y - self.rect.y:
                        self.rect.x = walls[0].rect.x - size
                    elif self.rect.x - walls[0].rect.x > walls[0].rect.y - self.rect.y:
                        self.rect.y = walls[0].rect.y + size
                    else:
                        self.rect.y = walls[0].rect.y + size
                        self.rect.x = walls[0].rect.x - size
                elif len(walls) == 2:
                    if walls[0].rect.x == walls[1].rect.x:
                        self.rect.x = walls[0].rect.x - size
                    else:
                        self.rect.y = walls[0].rect.y + size
                elif len(walls) == 3:
                    self.rect.x = (walls[0].rect.x + walls[1].rect.x + walls[2].rect.x - size * 2) // 3
                    self.rect.y = (walls[0].rect.y + walls[1].rect.y + walls[2].rect.y + size * 2) // 3
        elif self.movey > 0:
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = self.images[self.frame // ani]
            if self.movex == 0:
                for wall in pygame.sprite.spritecollide(self, group, False):
                    self.rect.y = wall.rect.y - size
            elif self.movex < 0:
                self.image = self.images[self.frame // ani + 4]
                walls = pygame.sprite.spritecollide(self, group, False)
                if len(walls) == 1:
                    if self.rect.x - walls[0].rect.x < walls[0].rect.y - self.rect.y:
                        self.rect.y = walls[0].rect.y - size
                    elif self.rect.x - walls[0].rect.x > walls[0].rect.y - self.rect.y:
                        self.rect.x = walls[0].rect.x + size
                    else:
                        self.rect.y = walls[0].rect.y - size
                        self.rect.x = walls[0].rect.x + size
                elif len(walls) == 2:
                    if walls[0].rect.x == walls[1].rect.x:
                        self.rect.x = walls[0].rect.x + size
                    else:
                        self.rect.y = walls[0].rect.y - size
                elif len(walls) == 3:
                    self.rect.x = (walls[0].rect.x + walls[1].rect.x + walls[2].rect.x + size * 2) // 3
                    self.rect.y = (walls[0].rect.y + walls[1].rect.y + walls[2].rect.y - size * 2) // 3
            else:
                self.image = self.images[self.frame // ani + 8]
                walls = pygame.sprite.spritecollide(self, group, False)
                if len(walls) == 1:
                    if self.rect.x - walls[0].rect.x < self.rect.y - walls[0].rect.y:
                        self.rect.x = walls[0].rect.x - size
                    elif self.rect.x - walls[0].rect.x > self.rect.y - walls[0].rect.y:
                        self.rect.y = walls[0].rect.y - size
                    else:
                        self.rect.y = walls[0].rect.y - size
                        self.rect.x = walls[0].rect.x - size
                elif len(walls) == 2:
                    if walls[0].rect.x == walls[1].rect.x:
                        self.rect.x = walls[0].rect.x - size
                    else:
                        self.rect.y = walls[0].rect.y - size
                elif len(walls) == 3:
                    self.rect.x = (walls[0].rect.x + walls[1].rect.x + walls[2].rect.x - size * 2) // 3
                    self.rect.y = (walls[0].rect.y + walls[1].rect.y + walls[2].rect.y - size * 2) // 3
        else:
            if self.movex < 0:
                self.frame += 1
                if self.frame > 3 * ani:
                    self.frame = 0
                self.image = self.images[self.frame // ani + 4]
                for wall in pygame.sprite.spritecollide(self, group, False):
                    self.rect.x = wall.rect.x + size
            elif self.movex > 0:
                self.frame += 1
                if self.frame > 3 * ani:
                    self.frame = 0
                self.image = self.images[self.frame // ani + 8]
                for wall in pygame.sprite.spritecollide(self, group, False):
                    self.rect.x = wall.rect.x - size
        x_change = 0
        y_change = 0
        if self.rect.x < self.left_max:
            x_change = self.left_max - self.rect.x
            self.rect.x = self.left_max
        elif self.rect.x + self.size[0] > self.right_max:
            x_change = -(self.rect.x + self.size[0] - self.right_max)
            self.rect.x = self.right_max - self.size[0]
        if self.rect.y < self.top_max:
            y_change = self.top_max - self.rect.y
            self.rect.y = self.top_max
        elif self.rect.y + self.size[0] > self.bottom_max:
            y_change = -(self.rect.y + self.size[0] - self.bottom_max)
            self.rect.y = self.bottom_max - self.size[0]
        return x_change, y_change

    def defense(self, status, kind):  # 防御，kind只有两种值：-1和1，-1表示取消防御，1表示开始防御
        pass

    def stairs(self, game_map):  # 上下楼梯
        pass

    def talk(self, npc):  # 与npc交谈
        pass

    def door(self, game_map):  # 开门
        pass
