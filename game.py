import pygame
from game_setting import Setting
from game_page import Page


def run_game():  # 游戏主函数
    pygame.init()
    screen = pygame.display.set_mode((1500, 800))  # 尝试创建窗口，以获取电脑屏幕分辨率
    setting = Setting(screen)  # 设置类实例化
    setting.init_size(screen)  # 根据电脑屏幕分辨率，更新屏幕大小
    setting.music_init()  # 初始化游戏音量
    del screen
    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))  # 创建窗口
    page = Page(setting, screen)  # 页面类实例化
    pygame.display.set_caption("地宫类闯关游戏")
    clock = pygame.time.Clock()
    while True:  # 游戏主循环
        clock.tick(60)
        page.update_page()  # 更新页面
        page.check_event()  # 检测事件
        pygame.display.update()  # 屏幕刷新


run_game()
