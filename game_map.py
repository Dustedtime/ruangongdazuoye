import pygame
import os


class Map:
    def __init__(self, dictionary, setting):
        self.layout_data = dictionary['layout_data']
        self.height = dictionary['height']
        self.wall_width = dictionary['width'] * setting.screen_height
        self.floor_width = self.wall_width
        self.left = dictionary['left'][0] * setting.screen_width + dictionary['left'][1] * self.wall_width
        self.right = dictionary['right'][0] * setting.screen_width + dictionary['right'][1] * self.wall_width
        self.top = dictionary['top'][0] * setting.screen_height + dictionary['top'][1] * self.wall_width
        self.bottom = dictionary['bottom'][0] * setting.screen_height + dictionary['bottom'][1] * self.wall_width
        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.stairs = pygame.sprite.Group()
        self.init_layout(setting)

    def init_layout(self, setting):
        for i in range(len(self.layout_data)):
            for j in range(len(self.layout_data[i])):
                if self.layout_data[i][j] == 1:
                    wall = Wall((self.left + self.wall_width * j, self.top + self.wall_width * i),
                                (self.wall_width, self.wall_width))
                    self.walls.add(wall)
                if self.layout_data[i][j] == 0:
                    floor = Floor((self.left + self.floor_width * j, self.top + self.floor_width * i),
                                  (self.floor_width, self.floor_width))
                    self.floors.add(floor)

    def update(self, x, y):
        self.walls.update(x, y)
        # self.floors.update(x, y)

    def draw(self, screen):
        screen.fill('black')
        self.walls.draw(screen)
        # self.floors.draw(screen)


class Wall(pygame.sprite.Sprite):
    def __init__(self, location, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('image', 'page4', 'map', 'wall.bmp')), size)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = location

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y


class Floor(pygame.sprite.Sprite):
    def __init__(self, location, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('image', 'page4', 'map', 'floor.bmp')), size)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = location

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y
