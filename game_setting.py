import json
import os


class Setting:  # 游戏设置类
    def __init__(self, screen):
        self.screen_width = 3000
        self.screen_height = 2000
        self.ani = 10
        self.ALPHA = (0, 255, 0)
        self.volume = []  # 游戏音量，第一个元素为音量最小值代表的横坐标，第二个元素为当前音量代表的横坐标，两者相除即得当前真正音量数值
        self.music = 1
        self.sound_effect = 1
        self.volume_hold = 0
        self.bag_space = 35
        self.store_space = 35
        self.init_size(screen)
        self.music_init()

    def init_size(self, screen):
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

    def music_init(self):
        with open(os.path.join('page', 'page5', 'images.json'), 'r') as f:
            data = json.load(f)
        self.volume = [data[6][1][0] * self.screen_width, (data[7][1][0] + data[7][2][0] / 2) * self.screen_width]
        if data[8][0][2] == 'off.bmp':
            self.music = 0
        if data[9][0][2] == 'off.bmp':
            self.sound_effect = 0
