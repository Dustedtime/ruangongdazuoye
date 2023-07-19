import os

import pygame


class NPC(pygame.sprite.Sprite):
    def __init__(self, dictionary, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.kind = dictionary['kind']  # 种类
        self.image = dictionary['image']  # 图像
        self.size = (screen_height * dictionary['size'], screen_height * dictionary['size'])
        self.load_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (screen_width * dictionary['rect'][0], screen_height * dictionary['rect'][1])
        self.font_height = int(dictionary['font_height'] * screen_height)
        self.font_gap = dictionary['font_gap'] * screen_height  # 字体行间距
        self.status_start = dictionary['status_start']  # 起始状态
        self.status_end = dictionary['status_end']  # 终止状态
        self.status = self.status_start - 1  # 当前状态
        self.color = tuple(dictionary['color'])
        self.backshake = dictionary['backshake']
        self.talk_time = 0
        self.talk_enable = 0  # 是否处于可交谈状态
        self.talking = 0  # 是否与角色进行交谈中
        self.words = []
        self.font = None
        self.words_tip = dictionary['words_tip']
        self.load_word_init(dictionary)

    def load_image(self):  # 初始化图像
        path = ''
        for directory in self.image:
            path = os.path.join(path, directory)
        self.image = pygame.transform.scale(pygame.image.load(path), self.size)

    def load_word_init(self, dictionary):  # 初始化文本内容
        self.font = pygame.font.SysFont('SimSun', self.font_height)
        # 加载可谈话标志
        word = self.font.render(self.words_tip, True, self.color)
        rect = word.get_rect()
        rect.centerx = self.rect.centerx
        rect.y = self.rect.y - self.font_gap
        self.words_tip = [word, rect]
        # 加载谈话内容
        words = dictionary['words']
        for word in words:
            row = len(word)
            words_tmp = []
            for i in range(row):
                word_tmp = self.font.render(word[i], True, self.color)
                rect_tmp = word_tmp.get_rect()
                rect_tmp.centerx = self.rect.centerx
                rect_tmp.y = self.rect.y - (row - i) * self.font_gap
                words_tmp.append([word_tmp, rect_tmp])
            self.words.append(words_tmp)

    def change_word(self):  # 更新谈话内容
        # 更新下次谈话状态
        self.status += 1
        self.status = self.status_start + (self.status - self.status_start) % (self.status_end - self.status_start + 1)

    def update(self, x, y, hero):  # 更新npc位置及可能存在的谈话文本的位置，以及更新交谈状态
        self.rect.x += x
        self.rect.y += y
        self.words_tip[1].x += x
        self.words_tip[1].y += y
        if self.talking:
            for word in self.words[self.status]:
                word[1].x += x
                word[1].y += y
        self.talk_enable_check(hero)

    def draw(self, screen):  # 绘制npc及可能存在的谈话
        screen.blit(self.image, self.rect)
        if self.talk_enable and not self.talking:
            screen.blit(self.words_tip[0], self.words_tip[1])
        if self.talking:
            for word in self.words[self.status]:
                screen.blit(word[0], word[1])

    def talk_enable_check(self, hero):  # 判断能否进行交谈
        if pygame.sprite.collide_rect(self, hero):
            self.talk_enable = 1
        else:
            self.talk_enable = 0
            self.talking = 0
            self.status = self.status_start - 1  # 重置谈话状态

    def talk(self):  # 进行交谈
        self.talking = 1
        time_now = pygame.time.get_ticks()
        if self.talk_time + self.backshake <= time_now:  # 防止按键间隔时间过短，谈话内容切换过快
            self.change_word()
            self.talk_time = time_now
