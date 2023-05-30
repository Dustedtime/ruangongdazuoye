import json
import os
import shutil
import sys

import pygame

from game_hero import Hero
from game_maps import Map
from game_monster import Monster


class Page:  # 定义页面类
    def __init__(self, setting, screen):
        self.screen = screen
        self.setting = setting
        self.hero = None
        self.monster = pygame.sprite.Group()
        self.monster_bullets = pygame.sprite.Group()  # 怪物发出的子弹
        self.npc = []
        self.merchant = []
        self.game_map = None
        self.box = None
        self.bullet = []
        self.page_kind = 0  # 页面类别
        self.archival = None  # 游戏所有存档
        self.current_archival = [-1, '']  # 游玩中的存档
        self.images = None  # 页面的基本图像
        self.images_after = None  # 页面根据需要后期要绘制的图像
        self.images_after_num = 0  # 后期要绘制的图像此刻绘制的数量
        self.words = None  # 页面的基本文本
        self.words_after = None  # 页面根据需要后期要绘制的文本
        self.words_after_num = 0  # 后期要绘制的文本此刻绘制的数量
        self.update_page_info()

    def update_page_info(self):  # 根据页面类别更新页面信息
        self.images = []  # 先把图像、文本等基本信息重置，然后重新从相应目录读取
        self.images_after = []
        self.images_after_num = 0
        self.words = []
        self.words_after = []
        if self.page_kind == 1:  # 存档名称读取
            self.archival = []
        route_common = os.path.join('page', 'page' + str(self.page_kind))  # 所有存档共用的数据存放的目录
        with open(os.path.join(route_common, 'images.json'), 'r') as f:  # 读取图像数据并更新页面相关信息
            images = json.load(f)
            for image in images:
                path = ''
                for directory_image in image[0]:
                    path = os.path.join(path, directory_image)
                size = (self.setting.screen_width * image[2][0], self.setting.screen_height * image[2][1])  # 图像尺寸
                picture = pygame.transform.scale(pygame.image.load(path), size)
                # 图像左上角坐标
                picture_left_top_pos = (
                    self.setting.screen_width * image[1][0], self.setting.screen_height * image[1][1])
                # 图像右下角坐标
                picture_right_bottom_pos = (picture_left_top_pos[0] + size[0], picture_left_top_pos[1] + size[1])
                self.images.append([picture, picture_left_top_pos, picture_right_bottom_pos])
        if os.path.exists(os.path.join(route_common, 'archival.json')):  # 先检测是否存在，然后读取存档数据并更新页面相关信息
            with open(os.path.join(route_common, 'archival.json'), 'r') as f:
                words = json.load(f)
                for word in words:
                    font = pygame.font.SysFont('SimSun', int(word[0] * self.setting.screen_height))
                    word_temp = font.render(word[1], True, tuple(word[3]))
                    word_pos = word_temp.get_rect()
                    word_pos.center = (word[2][0] * self.setting.screen_width, word[2][1] * self.setting.screen_height)
                    self.words.append([word_temp, word_pos])
                    self.archival.append(word[1])
        if os.path.exists(os.path.join(route_common, 'words.json')):  # 先检测是否存在，然后读取文本数据并更新页面相关信息
            with open(os.path.join(route_common, 'words.json'), 'r') as f:
                words = json.load(f)
                for word in words:
                    font = pygame.font.SysFont('SimSun', int(word[0] * self.setting.screen_height))
                    word_temp = font.render(word[1], True, tuple(word[3]))
                    word_pos = word_temp.get_rect()
                    word_pos.center = (word[2][0] * self.setting.screen_width, word[2][1] * self.setting.screen_height)
                    self.words.append([word_temp, word_pos])
        if os.path.exists(os.path.join(route_common, 'images_after.json')):  # 先检测是否存在，然后读取后期图像数据并更新页面相关信息
            with open(os.path.join(route_common, 'images_after.json'), 'r') as f:
                images_after = json.load(f)
                for image_after in images_after:
                    path = ''
                    for directory_image in image_after[0]:
                        path = os.path.join(path, directory_image)
                    size = (
                        self.setting.screen_width * image_after[2][0], self.setting.screen_height * image_after[2][1])
                    picture = pygame.transform.scale(pygame.image.load(path), size)
                    picture_left_top_pos = (
                        self.setting.screen_width * image_after[1][0], self.setting.screen_height * image_after[1][1])
                    picture_right_bottom_pos = (picture_left_top_pos[0] + size[0], picture_left_top_pos[1] + size[1])
                    self.images_after.append([picture, picture_left_top_pos, picture_right_bottom_pos])
        if os.path.exists(os.path.join(route_common, 'words_after.json')):  # 先检测是否存在，然后读取后期文本数据并更新页面相关信息
            with open(os.path.join(route_common, 'words_after.json'), 'r') as f:
                words_after = json.load(f)
                for word_after in words_after:
                    font = pygame.font.SysFont('SimSun', int(word_after[0] * self.setting.screen_height))
                    word_after_temp = font.render(word_after[1], True, tuple(word_after[3]))
                    word_after_pos = word_after_temp.get_rect()
                    word_after_pos.center = (
                        word_after[2][0] * self.setting.screen_width, word_after[2][1] * self.setting.screen_height)
                    self.words_after.append([word_after_temp, word_after_pos])
        pass  # 需完善角色、敌人等对象的更新

    def update_page_type(self, page_kind):  # 更新页面编号
        self.page_kind = page_kind
        self.update_page_info()  # 根据编号更新页面信息

    def update_page(self):  # 刷新页面
        for image in self.images:
            self.screen.blit(image[0], image[1])
        for word in self.words:
            self.screen.blit(word[0], word[1])
        if self.game_map:
            self.update_game_scene()  # 更新游戏画面

    def update_game_scene(self):  # 更新游戏画面
        # 更新人物位置
        x_change, y_change = self.hero.update(self.game_map, self.setting.ani, self.monster, self.monster_bullets,
                                              self.setting.screen_height, self.setting.screen_width)
        if x_change or y_change:
            self.game_map.update(x_change, y_change)  # 更新地图位置
        self.monster.update(x_change, y_change, self.game_map, self.setting.ani, self.hero, self.setting.screen_height,
                            self.monster_bullets, self.monster)
        self.monster_bullets.update(x_change, y_change)  # 更新怪物子弹位置
        self.collide_monster_bullet()
        self.game_map.draw(self.screen)  # 绘制地图
        self.monster.draw(self.screen)  # 绘制怪物
        self.hero.draw(self.screen)  # 绘制人物
        self.monster_bullets.draw(self.screen)  # 绘制怪物子弹
        for image in self.images:
            self.screen.blit(image[0], image[1])
        pass  # 还欠敌人等要素的更新

    def collide_monster_bullet(self):  # 怪物子弹与墙壁的碰撞检测
        # 检测是否击中墙壁
        dictionary = pygame.sprite.groupcollide(self.monster_bullets, self.game_map.walls, False, False)
        for bullet in dictionary.keys():
            for wall in dictionary[bullet]:
                if pygame.sprite.collide_mask(bullet, wall):
                    bullet.kill()
                    break

    def check_event(self):  # 监测事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标按下
                self.mouse_button_down_page(event)
            elif event.type == pygame.KEYDOWN:  # 键盘按键按下
                self.key_down_page(event)
            elif event.type == pygame.KEYUP:  # 键盘按键松开
                self.key_up_page(event)
            elif event.type == pygame.MOUSEMOTION:  # 鼠标移动
                self.mouse_motion_page(event)
            elif event.type == pygame.MOUSEBUTTONUP:  # 鼠标松开
                self.mouse_button_up_page(event)
            elif event.type == pygame.MOUSEWHEEL:  # 鼠标滚轮滚动
                self.mousewheel_page(event)
            pass  # 需完善其他事件

    def mouse_button_down_page(self, event):  # 鼠标按下
        if self.page_kind == 0 and event.button == 1:
            self.mouse_button_down_page0(event)
        elif self.page_kind == 1 and (event.button == 1 or event.button == 3):
            self.mouse_button_down_page1(event)
        elif self.page_kind == 2 and event.button == 1:
            self.mouse_button_down_page2(event)
        elif self.page_kind == 3 and event.button == 1:
            self.mouse_button_down_page3(event)
        elif self.page_kind == 4 and event.button == 1:
            self.mouse_button_down_page4(event)
        elif self.page_kind == 5 and event.button == 1:
            self.mouse_button_down_page5(event)
        elif self.page_kind == 6 and event.button == 1:
            self.mouse_button_down_page6(event)
        pass  # 需完善其他页面或操作

    def mouse_button_down_page0(self, event):  # 页面编号为0时鼠标按下
        if self.images[1][1][0] <= event.pos[0] < self.images[1][2][0] and self.images[1][1][1] <= event.pos[1] < \
                self.images[1][2][1]:
            self.update_page_type(1)
        elif self.images[2][1][0] <= event.pos[0] < self.images[2][2][0] and self.images[2][1][1] <= event.pos[1] < \
                self.images[2][2][1]:
            self.update_page_type(5)
        elif self.images[3][1][0] <= event.pos[0] < self.images[3][2][0] and self.images[3][1][1] <= event.pos[1] < \
                self.images[3][2][1]:
            self.update_page_type(6)
        elif self.images[4][1][0] <= event.pos[0] < self.images[4][2][0] and self.images[4][1][1] <= event.pos[1] < \
                self.images[4][2][1]:
            pygame.quit()
            sys.exit()

    def mouse_button_down_page1(self, event):  # 页面编号为1时鼠标按下
        if self.images[5][1][0] <= event.pos[0] < self.images[5][2][0] and self.images[5][1][1] <= event.pos[1] < \
                self.images[5][2][1] and event.button == 1:
            self.update_page_type(0)
        elif self.images[1][1][0] <= event.pos[0] < self.images[1][2][0] and self.images[1][1][1] <= event.pos[1] < \
                self.images[3][2][1]:
            num = (event.pos[1] - 90) // 200
            if event.button == 1:
                if self.archival[num] != "New Game":  # 选中存档不为空，读取存档并进入游戏页面
                    self.enter_game(num)
                else:  # 选中存档为空，进入创建存档页面
                    self.current_archival[0] = num
                    self.update_page_type(2)
            elif event.button == 3:
                if self.archival[num] != "New Game":  # 选中存档不为空，进入删除存档界面
                    self.current_archival = [num, self.archival[num]]
                    with open(os.path.join('page', 'page3', 'words.json'), 'w') as f:  # 更新存有要删除的存档的名字的文件信息
                        json.dump([[0.1, self.current_archival[1], [0.5, 0.55], [0, 0, 0]]], f)
                    self.update_page_type(3)

    def enter_game(self, num):  # 读取存档进入游戏
        self.current_archival = [num, self.archival[num]]  # 更新当前游戏中的存档信息
        # 实例化地图
        archival_path = os.path.join('page', self.current_archival[-1], 'page4')
        with open(os.path.join(archival_path, 'floor.json'), 'r') as f:
            dictionary = json.load(f)
            dictionary_temp = dictionary.copy()
        for key in dictionary:
            with open(os.path.join(archival_path, 'floor' + str(dictionary[key]), 'map_data.json'), 'r') as f:
                dictionary_temp.update(json.load(f))
        self.game_map = Map(dictionary_temp, self.setting.screen_width, self.setting.screen_height)
        # 实例化角色
        with open(os.path.join(archival_path, 'player', 'player_data.json'), 'r') as f:
            dictionary = json.load(f)
        self.hero = Hero(dictionary, self.setting, self.setting.screen_width, self.setting.screen_height,
                         self.current_archival[1])
        # 实例化怪物
        with open(os.path.join(archival_path, 'floor' + str(self.game_map.height), 'monster.json'), 'r') as f:
            data = json.load(f)
        monster_num = len(data)
        i = 0
        while i < monster_num:
            if not data[i]['die']:
                # noinspection PyTypeChecker
                self.monster.add(Monster(data[i], self.setting.screen_width, self.setting.screen_height))
            i += 1
        self.update_page_type(4)

    def mouse_button_down_page2(self, event):  # 页面编号为2时鼠标按下
        if self.images[4][1][0] <= event.pos[0] < self.images[4][2][0] and self.images[4][1][1] <= event.pos[1] < \
                self.images[4][2][1]:  # 确定创建新存档
            self.create_archival()
        elif self.images[5][1][0] <= event.pos[0] < self.images[5][2][0] and self.images[5][1][1] <= event.pos[1] < \
                self.images[5][2][1]:  # 取消创建新存档
            self.current_archival = [-1, '']
            self.update_page_type(1)

    def create_archival(self):  # 检测存档名字是否合格，若合格则创建存档目录，将相关数据复制到该目录，并修改存储着存档名字的文件
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
            self.update_page_type(1)  # 更新页面类别，回到选择存档界面

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

    def mouse_button_down_page3(self, event):  # 页面编号为3时鼠标按下
        if self.images[4][1][0] <= event.pos[0] < self.images[4][2][0] and self.images[4][1][1] <= event.pos[1] < \
                self.images[4][2][1]:  # 确定删除存档
            self.delete_archival()
            self.update_page_type(1)
        elif self.images[5][1][0] <= event.pos[0] < self.images[5][2][0] and self.images[5][1][1] <= event.pos[1] < \
                self.images[5][2][1]:  # 取消删除存档
            self.current_archival = [-1, '']
            self.update_page_type(1)

    def delete_archival(self):  # 删除存档目录，修改存储存档名字的文件信息
        shutil.rmtree(os.path.join('page', self.current_archival[1]))
        with open(os.path.join('page', 'page1', 'archival.json'), 'r') as f:
            archival = json.load(f)
        archival[self.current_archival[0]][1] = "New Game"
        with open(os.path.join('page', 'page1', 'archival.json'), 'w') as f:
            json.dump(archival, f)
        self.current_archival = [-1, '']

    def mouse_button_down_page4(self, event):
        if self.images[0][1][0] <= event.pos[0] < self.images[0][2][0] and self.images[0][1][1] <= event.pos[1] < \
                self.images[0][2][1]:  # 保存游戏进度并返回主菜单
            self.save_progress()  # 保存游戏进度
            self.update_page_type(0)  # 返回主菜单
        elif self.game_map.left_max <= event.pos[0] < self.game_map.right_min and self.game_map.top_max <= \
                event.pos[1] < self.game_map.bottom_min:  # 角色攻击
            self.hero.attack(self.setting.screen_height, event.pos)

    def save_progress(self):  # 保存游戏进度
        # 保存游戏地图相关信息
        data = {"height": self.game_map.height}
        with open(os.path.join('page', self.current_archival[1], 'page4', 'floor.json'), 'w') as f:  # 保存当前地图层数
            json.dump(data, f)
        path = os.path.join('page', self.current_archival[1], 'page4', 'floor' + str(self.game_map.height),
                            'map_data.json')
        with open(path, 'r') as f:
            data = json.load(f)
        data["left"] = [self.game_map.left / self.setting.screen_width, 0]
        data["right"] = [self.game_map.right / self.setting.screen_width, 0]
        data["top"] = [self.game_map.top / self.setting.screen_height, 0]
        data["bottom"] = [self.game_map.bottom / self.setting.screen_height, 0]
        with open(path, 'w') as f:
            json.dump(data, f)
        # 保存英雄数据
        path = os.path.join('page', self.current_archival[1], 'page4', 'player', 'player_data.json')
        with open(path, 'r') as f:
            data = json.load(f)
        data['health'] = self.hero.health
        data['strength'] = self.hero.strength
        data['defence'] = self.hero.defence
        data['speed'] = self.hero.speed / self.setting.screen_height
        data['money'] = self.hero.money
        data['exp'] = self.hero.exp
        data['rect'] = [self.hero.rect.x / self.setting.screen_width, self.hero.rect.y / self.setting.screen_height]
        data['max_health'] = self.hero.max_health
        data['level'] = self.hero.level
        data['max_exp'] = self.hero.max_exp
        with open(path, 'w') as f:
            json.dump(data, f)
        # 保存背包信息
        path = os.path.join('page', self.current_archival[1], 'page4', 'bag', 'bag_data.json')
        with open(path, 'r') as f:
            data = json.load(f)
        data['selecting'] = self.hero.bag.selecting
        data['things'] = self.hero.bag.things_kind
        with open(path, 'w') as f:
            json.dump(data, f)
        # 保存怪物信息
        path = os.path.join('page', self.current_archival[1], 'page4', 'floor' + str(self.game_map.height),
                            'monster.json')
        with open(path, 'r') as f:
            data_list = json.load(f)
        monster_num = len(data_list)
        i = 0
        for monster in self.monster:
            while True:
                if data_list[i]["die"]:
                    i += 1
                elif data_list[i]["kind"] != monster.kind:
                    data_list[i]["die"] = 1
                    i += 1
                else:
                    break
            data_list[i]["health"] = monster.health
            data_list[i]["rect"] = [monster.rect.x / self.setting.screen_width,
                                    monster.rect.y / self.setting.screen_height]
            i += 1
        while i < monster_num:
            data_list[i]["die"] = 1
            i += 1
        with open(path, 'w') as f:
            json.dump(data_list, f)
        self.hero = None
        self.monster = pygame.sprite.Group()
        self.monster_bullets = pygame.sprite.Group()
        self.npc = []
        self.merchant = []
        self.game_map = None
        self.box = None
        self.bullet = []
        self.current_archival = [-1, '']
        pass

    def mouse_button_down_page5(self, event):  # 页面编号为5时鼠标按下
        if self.images[2][1][0] <= event.pos[0] < self.images[2][2][0] and self.images[2][1][1] <= event.pos[1] < \
                self.images[2][2][1]:  # 退出游戏设置界面，返回游戏主菜单
            self.update_page_type(0)
        elif self.images[8][1][0] <= event.pos[0] < self.images[8][2][0] and self.images[8][1][1] <= event.pos[1] < \
                self.images[8][2][1]:  # 改变游戏音乐开关状态
            self.setting.music = self.change_music_state(8, self.setting.music)
        elif self.images[9][1][0] <= event.pos[0] < self.images[9][2][0] and self.images[9][1][1] <= event.pos[1] < \
                self.images[9][2][1]:  # 改变游戏音效开关状态
            self.setting.sound_effect = self.change_music_state(9, self.setting.sound_effect)
        elif self.images[7][1][0] <= event.pos[0] < self.images[7][2][0] and self.images[7][1][1] <= event.pos[1] < \
                self.images[7][2][1]:
            self.change_volume_instant(event)
            self.setting.volume_hold = 1  # 鼠标可拖动改变音量标志设为1
        elif self.images[6][1][0] <= event.pos[0] < self.images[6][2][0] and self.images[7][1][1] <= event.pos[1] < \
                self.images[7][2][1]:
            self.change_volume_instant(event)  # 修改游戏音量

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

    def change_volume_instant(self, event):  # 修改游戏音量
        with open(os.path.join('page', 'page5', 'images.json'), 'r') as f:  # 读取音效图像信息
            data = json.load(f)
        data[7][1][0] = (event.pos[0] - data[7][2][0] * self.setting.screen_width / 2) / self.setting.screen_width
        if data[7][1][0] + data[7][2][0] / 2 < data[6][1][0]:
            data[7][1][0] = data[6][1][0] - data[7][2][0] / 2
        elif data[7][1][0] + data[7][2][0] / 2 >= data[6][1][0] + data[6][2][0]:
            data[7][1][0] = data[6][1][0] + data[6][2][0] - data[7][2][0] / 2
        self.setting.volume[1] = (data[7][1][0] + data[7][2][0] / 2) * self.setting.screen_width  # 修改游戏音量
        self.images[7][1] = (data[7][1][0] * self.setting.screen_width, self.images[7][1][1])
        self.images[7][2] = (self.images[7][1][0] + data[7][2][0] * self.setting.screen_width, self.images[7][2][1])
        with open(os.path.join('page', 'page5', 'images.json'), "w") as f:  # 将最终效果保存至文件
            json.dump(data, f)

    def mouse_button_down_page6(self, event):  # 页面编号为6时鼠标按下
        if self.images[5][1][0] <= event.pos[0] < self.images[5][2][0] and self.images[5][1][1] <= event.pos[1] < \
                self.images[5][2][1]:
            self.update_page_type(0)  # 返回主菜单
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

    def mouse_motion_page(self, event):  # 鼠标移动
        if self.page_kind == 5:
            self.mouse_motion_page5(event)
        pass  # 需完善其他页面

    def mouse_motion_page5(self, event):  # 页面编号为5时鼠标移动
        if self.setting.volume_hold:
            self.change_volume_constant(event)

    def change_volume_constant(self, event):  # 鼠标拖动音量刻度改变音量大小
        width = self.images[7][2][0] - self.images[7][1][0]  # 音量刻度的宽度
        if self.images[6][1][0] <= event.pos[0] < self.images[6][2][0]:
            self.setting.volume[1] = event.pos[0]
            self.images[7][1] = (event.pos[0] - width / 2, self.images[7][1][1])
            self.images[7][2] = (event.pos[0] + width / 2, self.images[7][2][1])
        elif event.pos[0] < self.images[6][1][0]:  # 防止音量刻度越界
            self.setting.volume[1] = self.images[6][1][0]
            self.images[7][1] = (self.setting.volume[1] - width / 2, self.images[7][1][1])
            self.images[7][2] = (self.setting.volume[1] + width / 2, self.images[7][2][1])
        else:
            self.setting.volume[1] = self.images[6][2][0] - 1
            self.images[7][1] = (self.setting.volume[1] - width / 2, self.images[7][1][1])
            self.images[7][2] = (self.setting.volume[1] + width / 2, self.images[7][2][1])

    def mouse_button_up_page(self, event):  # 鼠标松开
        if self.page_kind == 5 and event.button == 1:
            self.mouse_button_up_page5()
        pass  # 需完善其他页面或操作

    def mouse_button_up_page5(self):  # 页面编号为5时鼠标松开
        if self.setting.volume_hold:
            self.setting.volume_hold = 0
            with open(os.path.join('page', 'page5', 'images.json'), 'r') as f:  # 读取音量图像信息
                data = json.load(f)
            data[7][1][0] = self.images[7][1][0] / self.setting.screen_width
            with open(os.path.join('page', 'page5', 'images.json'), "w") as f:  # 将最终效果保存至文件
                json.dump(data, f)

    def mousewheel_page(self, event):
        if self.page_kind == 4:
            self.mousewheel_page4(event)

    def mousewheel_page4(self, event):
        if event.y > 0:
            self.hero.change_weapon(-1)
        elif event.y < 0:
            self.hero.change_weapon(1)

    def key_down_page(self, event):  # 键盘按下
        if self.page_kind == 2:
            self.key_down_page2(event)
        elif self.page_kind == 4:
            self.hero.control()
        pass  # 需完善其他页面

    def key_down_page2(self, event):  # 页面编号为2时键盘按下
        with open(os.path.join('page', 'page2', 'words.json'), "r") as f:  # 加载文字属性
            data = json.load(f)
        self.enter_archival_name(event, 0, data)  # 从键盘读取新存档名字

    def enter_archival_name(self, event, num, data):  # 从键盘读取新存档名字
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
        font = pygame.font.SysFont('SimSun', int(data[0][0] * self.setting.screen_height))
        self.words[num][0] = font.render(self.current_archival[1], True, tuple(data[0][3]))  # 更新页面的文字列表，实时绘制输入的存档名
        words_pos = self.words[num][0].get_rect()
        words_pos.center = (data[0][2][0] * self.setting.screen_width, data[0][2][1] * self.setting.screen_height)
        self.words[num][1] = words_pos

    def key_up_page(self, event):  # 键盘按键松开
        if self.page_kind == 4:
            self.key_up_page4()

    def key_up_page4(self):  # 页面类型为4时键盘按键松开
        self.hero.control()
