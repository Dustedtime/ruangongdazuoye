import pygame
from game_setting import Setting
from game_page import Page


def run_game():
    pygame.init()
    setting = Setting()
    page = Page()
    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))
    pygame.display.set_caption("地宫类闯关游戏")
    while True:
        page.update_page(screen)
        page.check_event()
        pygame.display.update()


run_game()
