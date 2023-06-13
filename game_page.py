import json
import os
import sys

import pygame

from game_functions import Function


class Page:  # 定义页面类
    def __init__(self, setting, screen):
        self.screen = screen
        self.setting = setting
        self.hero = None
        self.monster = pygame.sprite.Group()
        self.monster_bullets = pygame.sprite.Group()  # 怪物发出的子弹
        self.npc = pygame.sprite.Group()
        self.merchant = pygame.sprite.Group()
        self.game_map = None
        self.box = None
        self.harm = None
        self.page_kind = 0  # 页面类别
        self.archival = []  # 游戏所有存档
        self.current_archival = [-1, '']  # 游玩中的存档
        self.images = []  # 页面的基本图像
        self.images_after = []  # 页面根据需要后期要绘制的图像
        self.images_after_num = 0  # 后期要绘制的图像此刻绘制的数量
        self.words = []  # 页面的基本文本
        self.words_after = []  # 页面根据需要后期要绘制的文本
        self.words_after_num = 0  # 后期要绘制的文本此刻绘制的数量
        self.functions = Function()  # 执行过程中要用到的一些函数存放的类
        self.update_page_info()

    def update_page_info(self):  # 根据页面类别更新页面信息
        route_common = os.path.join('page', 'page' + str(self.page_kind))  # 所有存档共用的数据存放的目录
        screen_width, screen_height = self.setting.screen_width, self.setting.screen_height
        self.functions.load_page_image(route_common, screen_width, screen_height, self.images)  # 加载基本图像
        self.functions.load_page_archival(route_common, screen_width, screen_height, self.words, self.archival,
                                          self.page_kind)  # 加载存档信息
        self.functions.load_page_word(route_common, screen_width, screen_height, self.words)  # 加载页面显示的文字
        # 加载页面后续要显示图像
        self.functions.load_page_image_after(route_common, screen_width, screen_height, self.images_after)
        self.images_after_num = 0
        # 加载页面后续要显示文字
        self.functions.load_page_word_after(route_common, screen_width, screen_height, self.words_after)
        self.words_after_num = 0
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
            self.update_game_scene()  # 更新游戏数据
            self.draw_game_scene()  # 更新游戏画面

    def update_game_scene(self):  # 更新游戏画面
        if self.hero.bag.showing >= 0:
            return
        # 更新人物位置
        screen_width, screen_height = self.setting.screen_width, self.setting.screen_height
        x_change, y_change = self.hero.update(self.game_map, self.setting.ani, self.monster, self.monster_bullets,
                                              screen_height, screen_width, self.harm)
        # 更新地图位置
        if x_change or y_change:
            self.game_map.update(x_change, y_change)
        # 更新怪物位置
        self.monster.update(x_change, y_change, self.game_map, self.setting.ani, self.hero, screen_height,
                            self.monster_bullets, self.monster, self.harm)
        # 更新子弹位置
        self.monster_bullets.update(x_change, y_change)
        self.hero.bullets.update(x_change, y_change)
        self.hero.sword_attack.update(x_change, y_change)
        # 子弹的检测碰撞
        self.functions.collide_monster_bullet(self.monster_bullets, self.game_map.walls, self.hero.sword_attack,
                                              self.hero, self.harm, screen_width, screen_height)
        self.functions.collide_hero_attack(self.monster, self.game_map.walls, self.harm, self.hero,
                                           self.setting.screen_width, self.setting.screen_height)
        # 更新伤害数值的显示
        self.harm.update(x_change, y_change)
        # 更新npc可谈话状态
        for npc in self.npc:
            npc.update(x_change, y_change, self.hero)
        # 更新商人坐标与交易状态
        for merchant in self.merchant:
            merchant.update(x_change, y_change, self.hero)

    def draw_game_scene(self):  # 依次绘制屏幕的所有元素
        self.game_map.draw(self.screen)
        for npc in self.npc:
            npc.draw(self.screen)
        for merchant in self.merchant:
            merchant.draw(self.screen)
        self.monster_bullets.draw(self.screen)
        self.hero.bullets.draw(self.screen)
        self.monster.draw(self.screen)
        self.hero.sword_attack.draw(self.screen)
        self.hero.draw(self.screen)
        self.harm.draw(self.screen)
        for image in self.images:
            self.screen.blit(image[0], image[1])
        pass  # 还欠npc等要素的更新

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
                    self.functions.enter_game(self, num)
                    self.update_page_type(4)
                else:  # 选中存档为空，进入创建存档页面
                    self.current_archival[0] = num
                    self.update_page_type(2)
            elif event.button == 3:
                if self.archival[num] != "New Game":  # 选中存档不为空，进入删除存档界面
                    self.current_archival = [num, self.archival[num]]
                    with open(os.path.join('page', 'page3', 'words.json'), 'w') as f:  # 更新存有要删除的存档的名字的文件信息
                        json.dump([[0.1, self.current_archival[1], [0.5, 0.55], [0, 0, 0]]], f)
                    self.update_page_type(3)

    def mouse_button_down_page2(self, event):  # 页面编号为2时鼠标按下
        if self.images[4][1][0] <= event.pos[0] < self.images[4][2][0] and self.images[4][1][1] <= event.pos[1] < \
                self.images[4][2][1]:  # 确定创建新存档
            self.functions.create_archival(self)
        elif self.images[5][1][0] <= event.pos[0] < self.images[5][2][0] and self.images[5][1][1] <= event.pos[1] < \
                self.images[5][2][1]:  # 取消创建新存档
            self.current_archival = [-1, '']
            self.update_page_type(1)

    def mouse_button_down_page3(self, event):  # 页面编号为3时鼠标按下
        if self.images[4][1][0] <= event.pos[0] < self.images[4][2][0] and self.images[4][1][1] <= event.pos[1] < \
                self.images[4][2][1]:  # 确定删除存档
            self.functions.delete_archival(self.current_archival)
            self.update_page_type(1)
        elif self.images[5][1][0] <= event.pos[0] < self.images[5][2][0] and self.images[5][1][1] <= event.pos[1] < \
                self.images[5][2][1]:  # 取消删除存档
            self.current_archival = [-1, '']
            self.update_page_type(1)

    def mouse_button_down_page4(self, event):  # 页面编号为4时鼠标按下
        if self.hero.bag.showing < 0 and self.images[0][1][0] <= event.pos[0] < self.images[0][2][0] and \
                self.images[0][1][1] <= event.pos[1] < self.images[0][2][1]:  # 保存游戏进度并返回主菜单
            self.functions.save_progress(self)  # 保存游戏进度
            self.update_page_type(0)  # 返回主菜单
        elif self.hero.bag.showing < 0 and self.game_map.left_max <= event.pos[0] < self.game_map.right_min and \
                self.game_map.top_max <= event.pos[1] < self.game_map.bottom_min:  # 角色攻击
            self.hero.attack(self.setting.screen_height, event.pos)
            self.hero.bag.selecting = -1
        elif self.hero.bag.images[1][1][0] <= event.pos[0] < self.hero.bag.images[1][2][0] and \
                self.hero.bag.images[1][1][1] <= event.pos[1] < self.hero.bag.images[1][2][1]:  # 选中背包物品
            self.hero.bag.click_select(event.pos, self.setting.screen_width, self.setting.screen_height)
        elif self.hero.bag.showing >= 0 and self.hero.bag.show_words[-2][1].topleft[0] <= event.pos[0] < \
                self.hero.bag.show_words[-2][1].bottomright[0] and self.hero.bag.show_words[-2][1].topleft[1] <= \
                event.pos[1] < self.hero.bag.show_words[-2][1].bottomright[1]:
            self.hero.bag.showing_click_left(self.setting.screen_width, self.setting.screen_height)
            self.hero.load_equipment()  # 更新英雄持有的武器
        elif self.hero.bag.showing >= 0 and self.hero.bag.show_words[-1][1].topleft[0] <= event.pos[0] < \
                self.hero.bag.show_words[-1][1].bottomright[0] and self.hero.bag.show_words[-1][1].topleft[1] <= \
                event.pos[1] < self.hero.bag.show_words[-1][1].bottomright[1]:
            self.hero.bag.showing_return(self.monster, self.hero)

    def mouse_button_down_page5(self, event):  # 页面编号为5时鼠标按下
        if self.images[2][1][0] <= event.pos[0] < self.images[2][2][0] and self.images[2][1][1] <= event.pos[1] < \
                self.images[2][2][1]:  # 退出游戏设置界面，返回游戏主菜单
            self.update_page_type(0)
        elif self.images[8][1][0] <= event.pos[0] < self.images[8][2][0] and self.images[8][1][1] <= event.pos[1] < \
                self.images[8][2][1]:  # 改变游戏音乐开关状态
            self.setting.music = self.functions.change_music_state(self, 8, self.setting.music)
        elif self.images[9][1][0] <= event.pos[0] < self.images[9][2][0] and self.images[9][1][1] <= event.pos[1] < \
                self.images[9][2][1]:  # 改变游戏音效开关状态
            self.setting.sound_effect = self.functions.change_music_state(self, 9, self.setting.sound_effect)
        elif self.images[7][1][0] <= event.pos[0] < self.images[7][2][0] and self.images[7][1][1] <= event.pos[1] < \
                self.images[7][2][1]:
            self.functions.change_volume_instant(self, event)
            self.setting.volume_hold = 1  # 鼠标可拖动改变音量标志设为1
        elif self.images[6][1][0] <= event.pos[0] < self.images[6][2][0] and self.images[7][1][1] <= event.pos[1] < \
                self.images[7][2][1]:
            self.functions.change_volume_instant(self, event)  # 修改游戏音量

    def mouse_button_down_page6(self, event):  # 页面编号为6时鼠标按下
        if self.images[5][1][0] <= event.pos[0] < self.images[5][2][0] and self.images[5][1][1] <= event.pos[1] < \
                self.images[5][2][1]:
            self.update_page_type(0)  # 返回主菜单
        elif self.images[3][1][0] <= event.pos[0] < self.images[3][2][0] and self.images[3][1][1] <= event.pos[1] < \
                self.images[3][2][1]:
            self.images_after_num = self.functions.change_help_tip(self.images_after_num, -1, self.images,
                                                                   self.images_after)  # 游戏帮助小提示换上一页
        elif self.images[4][1][0] <= event.pos[0] < self.images[4][2][0] and self.images[4][1][1] <= event.pos[1] < \
                self.images[4][2][1]:
            self.images_after_num = self.functions.change_help_tip(self.images_after_num, 1, self.images,
                                                                   self.images_after)  # 游戏帮助小提示换上一页

    def mouse_motion_page(self, event):  # 鼠标移动
        if self.page_kind == 4:
            self.mouse_motion_page4(event.pos)
        elif self.page_kind == 5:
            self.mouse_motion_page5(event)
        pass  # 需完善其他页面

    def mouse_motion_page4(self, pos):  # 页面编号为4时鼠标移动
        if self.hero.bag.moving:
            self.hero.bag.move(pos)  # 移动背包物品位置

    def mouse_motion_page5(self, event):  # 页面编号为5时鼠标移动
        if self.setting.volume_hold:
            self.functions.change_volume_constant(self, event)

    def mouse_button_up_page(self, event):  # 鼠标松开
        if self.page_kind == 4:
            self.mouse_button_up_page4(event.pos)
        elif self.page_kind == 5 and event.button == 1:
            self.mouse_button_up_page5()
        pass  # 需完善其他页面或操作

    def mouse_button_up_page4(self, pos):  # 页面编号为5时鼠标松开
        if self.hero.bag.moving:
            self.hero.bag.move_end()  # 移动背包物品位置结束

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
        if self.hero.bag.showing >= 0:
            return
        if event.y > 0:
            self.hero.change_weapon(-1)
        elif event.y < 0:
            self.hero.change_weapon(1)

    def key_down_page(self, event):  # 键盘按下
        if self.page_kind == 2:
            self.key_down_page2(event)
        elif self.page_kind == 4:
            self.key_down_page4(event)
        pass  # 需完善其他页面

    def key_down_page2(self, event):  # 页面编号为2时键盘按下
        with open(os.path.join('page', 'page2', 'words.json'), "r") as f:  # 加载文字属性
            data = json.load(f)
        self.functions.enter_archival_name(self, event, 0, data)  # 从键盘读取新存档名字

    def key_down_page4(self, event):  # 页面编号为4时键盘按下
        self.hero.control()
        if event.key == pygame.K_SPACE:
            for npc in self.npc:
                if npc.talk_enable:  # 检测npc是否可以交谈
                    npc.talk()  # 与npc进行交谈
            for merchant in self.merchant:
                if merchant.trade_enable:  # 检测商人是否可以交易
                    merchant.trade()  # 与商人进行交易


    def key_up_page(self, event):  # 键盘按键松开
        if self.page_kind == 4:
            self.key_up_page4()

    def key_up_page4(self):  # 页面类型为4时键盘按键松开
        self.hero.control()
