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
        self.status = dictionary['status']  # 状态，决定对话时显示哪些内容
        self.status_len = dictionary['status_len']  # 状态总数
        self.color = tuple(dictionary['color'])
        self.backshake = dictionary['backshake']
        self.talk_time = 0
        self.talk_enable = 0  # 是否处于可交谈状态
        self.talking = 0  # 是否与角色进行交谈中
        self.words = []
        self.font = None
        self.words_tip = dictionary['words_tip']
        self.load_word_init()

    def load_image(self):  # 初始化图像
        path = ''
        for directory in self.image:
            path = os.path.join(path, directory)
        self.image = pygame.transform.scale(pygame.image.load(path), self.size)

    def load_word_init(self):
        self.font = pygame.font.SysFont('SimSun', self.font_height)
        # 加载可谈话标志
        word = self.font.render(self.words_tip, True, self.color)
        rect = word.get_rect()
        rect.centerx = self.rect.centerx
        rect.y = self.rect.y - self.font_gap
        self.words_tip = [word, rect]

    def load_word(self):  # 初始化字体设置等
        # 加载谈话内容
        path = os.path.join('page', 'page4', 'npc', str(self.kind), str(self.status) + '.txt')
        with open(path, 'r', encoding='utf-8') as f:
            words = f.readlines()
        length = len(words)
        self.words = []
        for i in range(length):
            word = self.font.render(words[i], True, self.color)
            rect = word.get_rect()
            rect.centerx = self.rect.centerx
            rect.y = self.rect.y - (length - i) * self.font_gap
            self.words.append([word, rect])
        self.status = (self.status + 1) % self.status_len  # 更新下次谈话状态

    def update(self, x, y, hero):  # 更新npc位置及可能存在的谈话文本的位置，以及更新交谈状态
        self.rect.x += x
        self.rect.y += y
        self.words_tip[1].x += x
        self.words_tip[1].y += y
        if self.talking:
            for word in self.words:
                word[1].x += x
                word[1].y += y
        self.talk_enable_check(hero)

    def draw(self, screen):  # 绘制npc及可能存在的谈话
        screen.blit(self.image, self.rect)
        if self.talk_enable and not self.talking:
            screen.blit(self.words_tip[0], self.words_tip[1])
        if self.talking:
            for word in self.words:
                screen.blit(word[0], word[1])

    def talk_enable_check(self, hero):  # 判断能否进行交谈
        if pygame.sprite.collide_rect(self, hero):
            self.talk_enable = 1
        else:
            self.talk_enable = 0
            self.talking = 0

    def talk(self):  # 进行交谈
        self.talking = 1
        time_now = pygame.time.get_ticks()
        if self.talk_time + self.backshake <= time_now:  # 防止按键间隔时间过短，谈话内容切换过快
            self.load_word()
            self.talk_time = time_now
