import pygame
import os


class Map:  # 游戏地图类
    def __init__(self, dictionary, screen_width, screen_height):
        self.layout_data = dictionary['layout_data']  # 地图布局
        self.height = dictionary['height']  # 当前闯关层数
        self.wall_width = dictionary['width'] * screen_height  # 墙的宽度
        self.floor_width = self.wall_width  # 地板宽度
        # self.left为目前整张地图横坐标上最小值，下面三个类似
        self.left = dictionary['left'][0] * screen_width + dictionary['left'][1] * self.wall_width
        self.right = dictionary['right'][0] * screen_width + dictionary['right'][1] * self.wall_width
        self.top = dictionary['top'][0] * screen_height + dictionary['top'][1] * self.wall_width
        self.bottom = dictionary['bottom'][0] * screen_height + dictionary['bottom'][1] * self.wall_width
        # self.left_max为整张地图横坐标上最小值在屏幕上可允许的最大值（地图在屏幕上最大程度右移时，其横坐标上最左端的值），下面三个类似
        self.left_max = dictionary['left_max'] * screen_width
        self.right_min = dictionary['right_min'] * screen_width
        self.top_max = dictionary['top_max'] * screen_height
        self.bottom_min = dictionary['bottom_min'] * screen_height
        self.walls = pygame.sprite.Group()  # 建立墙精灵组
        self.doors = pygame.sprite.Group()
        self.stairs = pygame.sprite.Group()
        self.init_layout()  # 根据地图布局初始化地图

    def init_layout(self):  # 初始化地图
        for i in range(len(self.layout_data)):
            for j in range(len(self.layout_data[i])):
                if self.layout_data[i][j] == 1:
                    wall = Wall((self.left + self.wall_width * j, self.top + self.wall_width * i),
                                (self.wall_width, self.wall_width))
                    # noinspection PyTypeChecker
                    self.walls.add(wall)

    def update(self, x, y):  # 更新场景中除角色外所有对象坐标
        self.walls.update(x, y)
        self.left += x
        self.right += x
        self.top += y
        self.bottom += y

    def draw(self, screen):  # 更新场景中除角色外所有对象图像
        screen.fill('black')
        self.walls.draw(screen)


class Wall(pygame.sprite.Sprite):  # 定义墙类
    def __init__(self, location, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('image', 'page4', 'map', 'wall.bmp')), size)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = location

    def update(self, x, y):  # 更新墙坐标
        self.rect.x += x
        self.rect.y += y
