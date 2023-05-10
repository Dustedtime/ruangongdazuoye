import json
import os
import shutil
import sys

import pygame

from game_hero import Hero
from game_map import Map


class Page:  # 定义页面类
    def __init__(self, setting):
        self.hero = None
        self.monster = []
        self.npc = []
        self.merchant = []
        self.game_map = None
        self.box = None
        self.bullet = []
        self.page_kind = 0  # 页面类别
        self.archival = None  # 游戏所有存档
        self.current_archival = [-1, '']  # 游玩中的存档
        self.directory = None
        self.images = None  # 页面的基本图像
        self.images_after = None  # 页面根据需要后期要绘制的图像
        self.images_after_num = 0  # 后期要绘制的图像此刻绘制的数量
        self.words = None  # 页面的基本文本
        self.words_after = None  # 页面根据需要后期要绘制的文本
        self.words_after_num = 0  # 后期要绘制的文本此刻绘制的数量
        self.update_page_info(setting)

    def update_page_info(self, setting):  # 根据页面类别更新页面信息
        self.images = []  # 先把图像、文本等基本信息重置，然后重新从相应目录读取
        self.images_after = []
        self.images_after_num = 0
        self.words = []
        self.words_after = []
        if self.page_kind == 1:  # 存档名称读取
            self.archival = []
        directory_middle = self.current_archival[1]  # 读取的存档所在的目录，若还没有读取存档（没有进入游戏），则为空
        route_common = os.path.join('page', 'page' + str(self.page_kind))  # 所有存档共用的数据存放的目录
        route_special = os.path.join('page', directory_middle, 'page' + str(self.page_kind))  # 存档专用的数据存放的目录
        with open(os.path.join(route_common, 'images.json'), 'r') as f:  # 读取图像数据并更新页面相关信息
            images = json.load(f)
            for image in images:
                path = ''
                for directory_image in image[0]:
                    path = os.path.join(path, directory_image)
                size = (setting.screen_width * image[2][0], setting.screen_height * image[2][1])
                picture = pygame.transform.scale(pygame.image.load(path), size)
                picture_left_top_pos = (setting.screen_width * image[1][0], setting.screen_height * image[1][1])
                picture_right_bottom_pos = (picture_left_top_pos[0] + size[0], picture_left_top_pos[1] + size[1])
                self.images.append([picture, picture_left_top_pos, picture_right_bottom_pos])
        if os.path.exists(os.path.join(route_common, 'archival.json')):  # 先检测是否存在，然后读取存档数据并更新页面相关信息
            with open(os.path.join(route_common, 'archival.json'), 'r') as f:
                words = json.load(f)
                for word in words:
                    font = pygame.font.SysFont('SimSun', int(word[0] * setting.screen_height))
                    word_temp = font.render(word[1], True, tuple(word[3]))
                    word_pos = word_temp.get_rect()
                    word_pos.center = (word[2][0] * setting.screen_width, word[2][1] * setting.screen_height)
                    self.words.append([word_temp, word_pos])
                    self.archival.append(word[1])
        if os.path.exists(os.path.join(route_common, 'words.json')):  # 先检测是否存在，然后读取文本数据并更新页面相关信息
            with open(os.path.join(route_common, 'words.json'), 'r') as f:
                words = json.load(f)
                for word in words:
                    font = pygame.font.SysFont('SimSun', int(word[0] * setting.screen_height))
                    word_temp = font.render(word[1], True, tuple(word[3]))
                    word_pos = word_temp.get_rect()
                    word_pos.center = (word[2][0] * setting.screen_width, word[2][1] * setting.screen_height)
                    self.words.append([word_temp, word_pos])
        if os.path.exists(os.path.join(route_common, 'images_after.json')):  # 先检测是否存在，然后读取后期图像数据并更新页面相关信息
            with open(os.path.join(route_common, 'images_after.json'), 'r') as f:
                images_after = json.load(f)
                for image_after in images_after:
                    path = ''
                    for directory_image in image_after[0]:
                        path = os.path.join(path, directory_image)
                    size = (setting.screen_width * image_after[2][0], setting.screen_height * image_after[2][1])
                    picture = pygame.transform.scale(pygame.image.load(path), size)
                    picture_left_top_pos = (
                        setting.screen_width * image_after[1][0], setting.screen_height * image_after[1][1])
                    picture_right_bottom_pos = (picture_left_top_pos[0] + size[0], picture_left_top_pos[1] + size[1])
                    self.images_after.append([picture, picture_left_top_pos, picture_right_bottom_pos])
        if os.path.exists(os.path.join(route_common, 'words_after.json')):  # 先检测是否存在，然后读取后期文本数据并更新页面相关信息
            with open(os.path.join(route_common, 'words_after.json'), 'r') as f:
                words_after = json.load(f)
                for word_after in words_after:
                    font = pygame.font.SysFont('SimSun', int(word_after[0] * setting.screen_height))
                    word_after_temp = font.render(word_after[1], True, tuple(word_after[3]))
                    word_after_pos = word_after_temp.get_rect()
                    word_after_pos.center = (
                        word_after[2][0] * setting.screen_width, word_after[2][1] * setting.screen_height)
                    self.words_after.append([word_after_temp, word_after_pos])
        if os.path.exists(os.path.join(route_special, 'floor.json')):
            with open(os.path.join(route_special, 'floor.json'), 'r') as f:
                dictionary = json.load(f)
                dictionary_temp = dictionary.copy()
            for key in dictionary:
                with open(os.path.join(route_special, 'floor' + str(dictionary[key]), 'map_data.json'), 'r') as f:
                    dictionary_temp.update(json.load(f))
            self.game_map = Map(dictionary_temp, setting)
        pass  # 需完善角色、敌人等对象的更新

    def update_page_type(self, page_kind, setting):  # 更新页面编号
        self.page_kind = page_kind
        self.update_page_info(setting)  # 根据编号更新页面信息

    def update_page(self, screen, setting):  # 刷新页面
        for image in self.images:
            screen.blit(image[0], image[1])
        for word in self.words:
            screen.blit(word[0], word[1])
        if self.game_map:
            x_change, y_change = self.hero.update(self.game_map.walls, setting.ani, self.game_map.wall_width)
            if x_change or y_change:
                self.game_map.update(x_change, y_change)
            self.game_map.draw(screen)
            self.hero.draw(screen)
        pass  # 需完善角色、敌人等对象的更新

    def check_event(self, screen, setting):  # 监测事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标按下
                self.mouse_button_down_page(event, screen, setting)
            elif event.type == pygame.KEYDOWN:  # 键盘按键按下
                self.key_down_page(event, screen, setting)
            elif event.type == pygame.KEYUP:  # 键盘按键松开
                self.key_up_page(event, screen, setting)
            elif event.type == pygame.MOUSEMOTION:  # 鼠标移动
                self.mouse_motion_page(event, screen, setting)
            elif event.type == pygame.MOUSEBUTTONUP:  # 鼠标松开
                self.mouse_button_up_page(event, screen, setting)
            pass  # 需完善其他事件

    def mouse_button_down_page(self, event, screen, setting):  # 鼠标按下
        if self.page_kind == 0 and event.button == 1:
            self.mouse_button_down_page0(event, setting)
        elif self.page_kind == 1 and (event.button == 1 or event.button == 3):
            self.mouse_button_down_page1(event, setting)
        elif self.page_kind == 2 and event.button == 1:
            self.mouse_button_down_page2(event, setting)
        elif self.page_kind == 3 and event.button == 1:
            self.mouse_button_down_page3(event, setting)
        elif self.page_kind == 4 and event.button == 1:
            self.mouse_button_down_page4(event, setting)
        elif self.page_kind == 5 and event.button == 1:
            self.mouse_button_down_page5(event, setting)
        elif self.page_kind == 6 and event.button == 1:
            self.mouse_button_down_page6(event, setting)
        pass  # 需完善其他页面或操作

    def mouse_button_down_page0(self, event, setting):  # 页面编号为0时鼠标按下
        if self.images[1][1][0] <= event.pos[0] < self.images[1][2][0] and self.images[1][1][1] <= event.pos[1] < \
                self.images[1][2][1]:
            self.update_page_type(1, setting)
        elif self.images[2][1][0] <= event.pos[0] < self.images[2][2][0] and self.images[2][1][1] <= event.pos[1] < \
                self.images[2][2][1]:
            self.update_page_type(5, setting)
        elif self.images[3][1][0] <= event.pos[0] < self.images[3][2][0] and self.images[3][1][1] <= event.pos[1] < \
                self.images[3][2][1]:
            self.update_page_type(6, setting)
        elif self.images[4][1][0] <= event.pos[0] < self.images[4][2][0] and self.images[4][1][1] <= event.pos[1] < \
                self.images[4][2][1]:
            pygame.quit()
            sys.exit()

    def mouse_button_down_page1(self, event, setting):  # 页面编号为1时鼠标按下
        if self.images[5][1][0] <= event.pos[0] < self.images[5][2][0] and self.images[5][1][1] <= event.pos[1] < \
                self.images[5][2][1] and event.button == 1:
            self.update_page_type(0, setting)
        elif self.images[1][1][0] <= event.pos[0] < self.images[1][2][0] and self.images[1][1][1] <= event.pos[1] < \
                self.images[3][2][1]:
            num = (event.pos[1] - 90) // 200
            if event.button == 1:
                if self.archival[num] != "New Game":  # 选中存档不为空，读取存档并进入游戏页面
                    self.enter_game(self.archival[num], num, setting)
                else:  # 选中存档为空，进入创建存档页面
                    self.current_archival[0] = num
                    self.update_page_type(2, setting)
            elif event.button == 3:
                if self.archival[num] != "New Game":  # 选中存档不为空，进入删除存档界面
                    self.current_archival = [num, self.archival[num]]
                    with open(os.path.join('page', 'page3', 'words.json'), 'w') as f:  # 更新存有要删除的存档的名字的文件信息
                        json.dump([[0.1, self.current_archival[1], [0.5, 0.55], [0, 0, 0]]], f)
                    self.update_page_type(3, setting)

    def enter_game(self, archival, num, setting):  # 读取存档进入游戏
        self.current_archival = [num, archival]  # 更新当前游戏中的存档信息
        with open(os.path.join('page', self.archival[num], 'page4', 'player', 'player_data.json'), 'r') as f:
            dictionary = json.load(f)
        self.hero = Hero(dictionary, setting)
        self.update_page_type(4, setting)

    def mouse_button_down_page2(self, event, setting):  # 页面编号为2时鼠标按下
        if self.images[4][1][0] <= event.pos[0] < self.images[4][2][0] and self.images[4][1][1] <= event.pos[1] < \
                self.images[4][2][1]:  # 确定创建新存档
            self.create_archival(setting)
        elif self.images[5][1][0] <= event.pos[0] < self.images[5][2][0] and self.images[5][1][1] <= event.pos[1] < \
                self.images[5][2][1]:  # 取消创建新存档
            self.current_archival = [-1, '']
            self.update_page_type(1, setting)

    def create_archival(self, setting):  # 检测存档名字是否合格，若合格则创建存档目录，将相关数据复制到该目录，并修改存储着存档名字的文件
        if len(self.current_archival[1]) == 0:  # 输入名字为空
            if self.images_after_num == 0:
                self.images_after_num = 1
                self.images.append([self.images_after[0][0], self.images_after[0][1]])
        elif self.archival[(self.current_archival[0] + 1) % 3] == self.current_archival[1] or \
                self.archival[(self.current_archival[0] + 2) % 3] == self.current_archival[1]:  # 输入名字已存在
            if self.images_after_num == 0:
                self.images_after_num = 1
                self.images.append([self.images_after[2][0], self.images_after[2][1]])
        else:  # 修改数据，创建存档
            with open(os.path.join('page', 'page1', 'archival.json'), 'r') as f:  # 读取所有存档名字，存储为列表
                archival = json.load(f)
            archival[self.current_archival[0]][1] = self.current_archival[1]  # 修改列表相应位置名字
            with open(os.path.join('page', 'page1', 'archival.json'), "w") as f:  # 将修改后的存档名字列表重新写入文件
                json.dump(archival, f)
            target_path = os.path.join('page', self.current_archival[1])
            self.copy_dir(os.path.join('page', 'default'), target_path)  # 创建存档目录，并把一些必要数据复制过去
            self.current_archival[0] = -1  # 重置当前选中存档信息
            self.current_archival[1] = ''
            self.update_page_type(1, setting)  # 更新页面类别，回到选择存档界面

    def copy_dir(self, src_path, target_path):  # 递归地将整个目录的结构以及文件复制到创建的存档目录下
        os.mkdir(target_path)
        filelist = os.listdir(src_path)
        for file in filelist:
            path = os.path.join(src_path, file)
            path1 = os.path.join(target_path, file)
            if os.path.isdir(path):
                self.copy_dir(path, path1)
            else:
                shutil.copy(path, path1)

    def mouse_button_down_page3(self, event, setting):  # 页面编号为3时鼠标按下
        if self.images[4][1][0] <= event.pos[0] < self.images[4][2][0] and self.images[4][1][1] <= event.pos[1] < \
                self.images[4][2][1]:  # 确定删除存档
            self.delete_archival()
            self.update_page_type(1, setting)
        elif self.images[5][1][0] <= event.pos[0] < self.images[5][2][0] and self.images[5][1][1] <= event.pos[1] < \
                self.images[5][2][1]:  # 取消删除存档
            self.current_archival = [-1, '']
            self.update_page_type(1, setting)

    def delete_archival(self):  # 删除存档目录，修改存储存档名字的文件信息
        shutil.rmtree(os.path.join('page', self.current_archival[1]))
        with open(os.path.join('page', 'page1', 'archival.json'), 'r') as f:
            archival = json.load(f)
        archival[self.current_archival[0]][1] = "New Game"
        with open(os.path.join('page', 'page1', 'archival.json'), 'w') as f:
            json.dump(archival, f)
        self.current_archival = [-1, '']

    def mouse_button_down_page4(self, event, setting):
        if self.images[0][1][0] <= event.pos[0] < self.images[0][2][0] and self.images[0][1][1] <= event.pos[1] < \
                self.images[0][2][1]:  # 返回主菜单
            self.update_page_type(0, setting)

    def mouse_button_down_page5(self, event, setting):  # 页面编号为5时鼠标按下
        if self.images[2][1][0] <= event.pos[0] < self.images[2][2][0] and self.images[2][1][1] <= event.pos[1] < \
                self.images[2][2][1]:  # 退出游戏设置界面，返回游戏主菜单
            self.update_page_type(0, setting)
        elif self.images[8][1][0] <= event.pos[0] < self.images[8][2][0] and self.images[8][1][1] <= event.pos[1] < \
                self.images[8][2][1]:  # 改变游戏音乐开关状态
            setting.music = self.change_music_state(8, setting.music)
        elif self.images[9][1][0] <= event.pos[0] < self.images[9][2][0] and self.images[9][1][1] <= event.pos[1] < \
                self.images[9][2][1]:  # 改变游戏音效开关状态
            setting.sound_effect = self.change_music_state(9, setting.sound_effect)
        elif self.images[7][1][0] <= event.pos[0] < self.images[7][2][0] and self.images[7][1][1] <= event.pos[1] < \
                self.images[7][2][1]:
            self.change_volume_instant(event, setting)
            setting.volume_hold = 1  # 鼠标可拖动改变音量标志设为1
        elif self.images[6][1][0] <= event.pos[0] < self.images[6][2][0] and self.images[7][1][1] <= event.pos[1] < \
                self.images[7][2][1]:
            self.change_volume_instant(event, setting)  # 修改游戏音量

    def change_music_state(self, num, state):  # 改变游戏音乐或音效开关状态
        with open(os.path.join('page', 'page5', 'images.json'), 'r') as f:  # 读取音效图像信息
            data = json.load(f)
        if data[num][0][2] == "on.bmp":  # 修改状态
            data[num][0][2] = "off.bmp"
        else:
            data[num][0][2] = "on.bmp"
        path = ''
        for directory in data[num][0]:
            path = os.path.join(path, directory)
        self.images[num][0] = pygame.transform.scale(pygame.image.load(path), (
            self.images[num][2][0] - self.images[num][1][0], self.images[num][2][1] - self.images[num][1][1]))  # 更新图像
        with open(os.path.join('page', 'page5', 'images.json'), "w") as f:  # 将最终效果保存至文件
            json.dump(data, f)
        return not state

    def change_volume_instant(self, event, setting):  # 修改游戏音量
        with open(os.path.join('page', 'page5', 'images.json'), 'r') as f:  # 读取音效图像信息
            data = json.load(f)
        data[7][1][0] = (event.pos[0] - data[7][2][0] * setting.screen_width / 2) / setting.screen_width
        if data[7][1][0] + data[7][2][0] / 2 < data[6][1][0]:
            data[7][1][0] = data[6][1][0] - data[7][2][0] / 2
        elif data[7][1][0] + data[7][2][0] / 2 >= data[6][1][0] + data[6][2][0]:
            data[7][1][0] = data[6][1][0] + data[6][2][0] - data[7][2][0] / 2
        setting.volume[1] = (data[7][1][0] + data[7][2][0] / 2) * setting.screen_width  # 修改游戏音量
        self.images[7][1] = (data[7][1][0] * setting.screen_width, self.images[7][1][1])
        self.images[7][2] = (self.images[7][1][0] + data[7][2][0] * setting.screen_width, self.images[7][2][1])
        with open(os.path.join('page', 'page5', 'images.json'), "w") as f:  # 将最终效果保存至文件
            json.dump(data, f)

    def mouse_button_down_page6(self, event, setting):  # 页面编号为6时鼠标按下
        if self.images[5][1][0] <= event.pos[0] < self.images[5][2][0] and self.images[5][1][1] <= event.pos[1] < \
                self.images[5][2][1]:
            self.update_page_type(0, setting)  # 返回主菜单
        elif self.images[3][1][0] <= event.pos[0] < self.images[3][2][0] and self.images[3][1][1] <= event.pos[1] < \
                self.images[3][2][1]:
            self.change_help_tip(-1)  # 游戏帮助小提示换上一页
        elif self.images[4][1][0] <= event.pos[0] < self.images[4][2][0] and self.images[4][1][1] <= event.pos[1] < \
                self.images[4][2][1]:
            self.change_help_tip(1)  # 游戏帮助小提示换下一页

    def change_help_tip(self, move):  # 游戏帮助小提示切换页数
        self.images_after_num += move
        if self.images_after_num < 0:
            self.images_after_num = 0
        elif self.images_after_num > 9:
            self.images_after_num = 9
        self.images[2] = self.images_after[self.images_after_num]

    def mouse_motion_page(self, event, screen, setting):  # 鼠标移动
        if self.page_kind == 5:
            self.mouse_motion_page5(event, setting)
        pass  # 需完善其他页面

    def mouse_motion_page5(self, event, setting):  # 页面编号为5时鼠标移动
        if setting.volume_hold:
            self.change_volume_constant(event, setting)

    def change_volume_constant(self, event, setting):  # 鼠标拖动音量刻度改变音量大小
        width = self.images[7][2][0] - self.images[7][1][0]  # 音量刻度的宽度
        if self.images[6][1][0] <= event.pos[0] < self.images[6][2][0]:
            setting.volume[1] = event.pos[0]
            self.images[7][1] = (event.pos[0] - width / 2, self.images[7][1][1])
            self.images[7][2] = (event.pos[0] + width / 2, self.images[7][2][1])
        elif event.pos[0] < self.images[6][1][0]:  # 防止音量刻度越界
            setting.volume[1] = self.images[6][1][0]
            self.images[7][1] = (setting.volume[1] - width / 2, self.images[7][1][1])
            self.images[7][2] = (setting.volume[1] + width / 2, self.images[7][2][1])
        else:
            setting.volume[1] = self.images[6][2][0] - 1
            self.images[7][1] = (setting.volume[1] - width / 2, self.images[7][1][1])
            self.images[7][2] = (setting.volume[1] + width / 2, self.images[7][2][1])

    def mouse_button_up_page(self, event, screen, setting):  # 鼠标松开
        if self.page_kind == 5 and event.button == 1:
            self.mouse_button_up_page5(setting)
        pass  # 需完善其他页面或操作

    def mouse_button_up_page5(self, setting):  # 页面编号为5时鼠标松开
        if setting.volume_hold:
            setting.volume_hold = 0
            with open(os.path.join('page', 'page5', 'images.json'), 'r') as f:  # 读取音量图像信息
                data = json.load(f)
            data[7][1][0] = self.images[7][1][0] / setting.screen_width
            with open(os.path.join('page', 'page5', 'images.json'), "w") as f:  # 将最终效果保存至文件
                json.dump(data, f)

    def key_down_page(self, event, screen, setting):  # 键盘按下
        if self.page_kind == 2:
            self.key_down_page2(event, screen, setting)
        elif self.page_kind == 4:
            self.hero.control(event)
        pass  # 需完善其他页面

    def key_down_page2(self, event, screen, setting):  # 页面编号为2时键盘按下
        with open(os.path.join('page', 'page2', 'words.json'), "r") as f:  # 加载文字属性
            data = json.load(f)
        self.enter_archival_name(event, 0, data, setting)  # 从键盘读取新存档名字

    def enter_archival_name(self, event, num, data, setting):  # 从键盘读取新存档名字
        if self.images_after_num:  # 检测特殊提示图像是否已加入要显示的图像列表，若已经加入，则将其移除
            self.images_after_num = 0
            self.images.pop()
        if event.key == pygame.K_a:
            self.current_archival[1] += 'a'
        elif event.key == pygame.K_b:
            self.current_archival[1] += 'b'
        elif event.key == pygame.K_c:
            self.current_archival[1] += 'c'
        elif event.key == pygame.K_d:
            self.current_archival[1] += 'd'
        elif event.key == pygame.K_e:
            self.current_archival[1] += 'e'
        elif event.key == pygame.K_f:
            self.current_archival[1] += 'f'
        elif event.key == pygame.K_g:
            self.current_archival[1] += 'g'
        elif event.key == pygame.K_h:
            self.current_archival[1] += 'h'
        elif event.key == pygame.K_i:
            self.current_archival[1] += 'i'
        elif event.key == pygame.K_j:
            self.current_archival[1] += 'j'
        elif event.key == pygame.K_k:
            self.current_archival[1] += 'k'
        elif event.key == pygame.K_l:
            self.current_archival[1] += 'l'
        elif event.key == pygame.K_m:
            self.current_archival[1] += 'm'
        elif event.key == pygame.K_n:
            self.current_archival[1] += 'n'
        elif event.key == pygame.K_o:
            self.current_archival[1] += 'o'
        elif event.key == pygame.K_p:
            self.current_archival[1] += 'p'
        elif event.key == pygame.K_q:
            self.current_archival[1] += 'q'
        elif event.key == pygame.K_r:
            self.current_archival[1] += 'r'
        elif event.key == pygame.K_s:
            self.current_archival[1] += 's'
        elif event.key == pygame.K_t:
            self.current_archival[1] += 't'
        elif event.key == pygame.K_u:
            self.current_archival[1] += 'u'
        elif event.key == pygame.K_v:
            self.current_archival[1] += 'v'
        elif event.key == pygame.K_w:
            self.current_archival[1] += 'w'
        elif event.key == pygame.K_x:
            self.current_archival[1] += 'x'
        elif event.key == pygame.K_y:
            self.current_archival[1] += 'y'
        elif event.key == pygame.K_z:
            self.current_archival[1] += 'z'
        elif event.key == pygame.K_BACKSPACE and len(self.current_archival[1]) > 0:  # 按下退格键
            self.current_archival[1] = self.current_archival[1][:-1]
        if len(self.current_archival[1]) > 15:  # 检测输入是否已经超出15个字符，若超出，则将超出范围提示的图像加入要显示的图像列表中
            self.images_after_num = 1
            self.images.append([self.images_after[1][0], self.images_after[1][1]])
            self.current_archival[1] = self.current_archival[1][:-1]
        font = pygame.font.SysFont('SimSun', int(data[0][0] * setting.screen_height))
        self.words[num][0] = font.render(self.current_archival[1], True, tuple(data[0][3]))  # 更新页面的文字列表，实时绘制输入的存档名
        words_pos = self.words[num][0].get_rect()
        words_pos.center = (data[0][2][0] * setting.screen_width, data[0][2][1] * setting.screen_height)
        self.words[num][1] = words_pos

    def key_up_page(self, event, screen, setting):
        if self.page_kind == 4:
            self.key_up_page4(event)

    def key_up_page4(self, event):
        self.hero.control(event)
