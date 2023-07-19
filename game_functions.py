import json
import os
import shutil

import pygame

from game_box import Box
from game_harm import Harm
from game_hero import Hero
from game_maps import Map
from game_merchant import Merchant
from game_monster import Monster
from game_npc import NPC


class Function:
    def __init__(self):
        pass

    @staticmethod
    def load_page_image(route, screen_width, screen_height, images_page):  # 加载当前页面基本图像
        images_page.clear()
        with open(os.path.join(route, 'images.json'), 'r', encoding='utf-8') as f:  # 读取图像数据并更新页面相关信息
            images = json.load(f)
            for image in images:
                path = ''
                for directory_image in image[0]:
                    path = os.path.join(path, directory_image)
                size = (screen_width * image[2][0], screen_height * image[2][1])  # 图像尺寸
                picture = pygame.transform.scale(pygame.image.load(path), size)
                # 图像左上角坐标
                picture_left_top_pos = (screen_width * image[1][0], screen_height * image[1][1])
                # 图像右下角坐标
                picture_right_bottom_pos = (picture_left_top_pos[0] + size[0], picture_left_top_pos[1] + size[1])
                images_page.append([picture, picture_left_top_pos, picture_right_bottom_pos])

    @staticmethod
    def load_page_archival(route, screen_width, screen_height, words_page, archival, page_kind):  # 加载存档信息
        words_page.clear()
        if page_kind == 1:
            archival.clear()
            with open(os.path.join(route, 'archival.json'), 'r', encoding='utf-8') as f:
                words = json.load(f)
                for word in words:
                    font = pygame.font.SysFont('SimSun', int(word[0] * screen_height))  # 设置字体
                    word_temp = font.render(word[1], True, tuple(word[3]))
                    word_pos = word_temp.get_rect()
                    word_pos.center = (word[2][0] * screen_width, word[2][1] * screen_height)
                    words_page.append([word_temp, word_pos])
                    archival.append(word[1])

    @staticmethod
    def load_page_word(route, screen_width, screen_height, page_words):  # 加载页面显示的文本信息
        if os.path.exists(os.path.join(route, 'words.json')):
            with open(os.path.join(route, 'words.json'), 'r', encoding='utf-8') as f:
                words = json.load(f)
                for word in words:
                    font = pygame.font.SysFont('SimSun', int(word[0] * screen_height))  # 设置字体
                    word_temp = font.render(word[1], True, tuple(word[3]))
                    word_pos = word_temp.get_rect()
                    word_pos.center = (word[2][0] * screen_width, word[2][1] * screen_height)
                    page_words.append([word_temp, word_pos])

    @staticmethod
    def load_page_image_after(route, screen_width, screen_height, page_images_after):  # 加载页面后续要显示图像
        page_images_after.clear()
        if os.path.exists(os.path.join(route, 'images_after.json')):
            with open(os.path.join(route, 'images_after.json'), 'r', encoding='utf-8') as f:
                images_after = json.load(f)
                for image_after in images_after:
                    path = ''
                    for directory_image in image_after[0]:
                        path = os.path.join(path, directory_image)
                    size = (screen_width * image_after[2][0], screen_height * image_after[2][1])  # 图像尺寸
                    picture = pygame.transform.scale(pygame.image.load(path), size)
                    picture_left_top_pos = (screen_width * image_after[1][0], screen_height * image_after[1][1])
                    picture_right_bottom_pos = (picture_left_top_pos[0] + size[0], picture_left_top_pos[1] + size[1])
                    page_images_after.append([picture, picture_left_top_pos, picture_right_bottom_pos])

    @staticmethod
    def load_page_word_after(route, screen_width, screen_height, page_words_after):  # 加载页面后续要显示文本
        page_words_after.clear()
        if os.path.exists(os.path.join(route, 'words_after.json')):
            with open(os.path.join(route, 'words_after.json'), 'r', encoding='utf-8') as f:
                words_after = json.load(f)
                for word_after in words_after:
                    font = pygame.font.SysFont('SimSun', int(word_after[0] * screen_height))  # 设置字体
                    word_after_temp = font.render(word_after[1], True, tuple(word_after[3]))
                    word_after_pos = word_after_temp.get_rect()
                    word_after_pos.center = (
                        word_after[2][0] * screen_width, word_after[2][1] * screen_height)
                    page_words_after.append([word_after_temp, word_after_pos])

    @staticmethod
    # 怪物发出的子弹的碰撞检测
    # monster_bullets: 怪物发出的子弹的精灵组
    # walls: 游戏地图中墙壁精灵组
    # sword_attack: 玩家发出的剑气精灵组
    # hero: 英雄对象
    # harm: 显示伤害数值的类的实例化对象，用于把造成的伤害值显示在屏幕上
    # screen_width, screen_height: 屏幕宽度和高度
    def collide_monster_bullet(monster_bullets, walls, sword_attack, hero, harm, screen_width, screen_height):
        # 检测是否击中墙壁
        dictionary = pygame.sprite.groupcollide(monster_bullets, walls, False, False)
        for bullet in dictionary.keys():
            for wall in dictionary[bullet]:
                if pygame.sprite.collide_mask(bullet, wall):
                    bullet.kill()
                    break
        # 检测怪物子弹是否被英雄剑气抵挡
        dictionary = pygame.sprite.groupcollide(monster_bullets, sword_attack, False, False)
        for bullet in dictionary.keys():
            for sword_attack in dictionary[bullet]:
                if pygame.sprite.collide_mask(bullet, sword_attack):
                    bullet.kill()
                    break
        # 检测怪物子弹是否击中英雄
        for bullet in pygame.sprite.spritecollide(hero, monster_bullets, False):
            if pygame.sprite.collide_mask(bullet, hero):
                hero.attacked(bullet.strength, harm)  # 对英雄造成伤害
                bullet.kill()  # 移除该子弹
                hero.status.update(hero, screen_height, screen_width)  # 更新状态栏信息

    @staticmethod
    def collide_hero_attack(monsters, walls, harm, hero, screen_width, screen_height):  # 英雄发出的子弹和剑气的碰撞检测
        # 英雄子弹与墙的碰撞检测
        dictionary = pygame.sprite.groupcollide(hero.bullets, walls, False, False)
        for bullet in dictionary.keys():
            for wall in dictionary[bullet]:
                if pygame.sprite.collide_mask(bullet, wall):
                    bullet.kill()
        # 英雄子弹与怪物的碰撞检测
        dictionary = pygame.sprite.groupcollide(hero.bullets, monsters, False, False)
        for bullet in dictionary.keys():
            for monster in dictionary[bullet]:
                if pygame.sprite.collide_mask(bullet, monster):
                    if monster.attacked(bullet.strength, harm):  # 对怪物造成伤害
                        monster.dead(hero)  # 怪物死亡
                        hero.status.update(hero, screen_height, screen_width)  # 更新状态栏
                    bullet.kill()
        # 英雄剑气与怪物的碰撞检测
        dictionary = pygame.sprite.groupcollide(hero.sword_attack, monsters, False, False)
        for attack in dictionary.keys():
            for monster in dictionary[attack]:
                if pygame.sprite.collide_mask(attack, monster) and not monster.attacked_sword:
                    monster.attacked_sword = 1  # 怪物被剑气攻击过的标志置为1
                    if monster.attacked(attack.strength, harm):  # 对怪物造成伤害
                        monster.dead(hero)  # 怪物死亡
                        hero.status.update(hero, screen_height, screen_width)  # 更新状态栏

    @staticmethod
    def enter_archival_name(page, event, num, data):  # 从键盘读取新存档名字
        if page.images_after_num:  # 检测特殊提示图像是否已加入要显示的图像列表，若已经加入，则将其移除
            page.images_after_num = 0
            page.images.pop()
        current_archival = page.current_archival[1]
        if event.key == pygame.K_a:
            current_archival += 'a'
        elif event.key == pygame.K_b:
            current_archival += 'b'
        elif event.key == pygame.K_c:
            current_archival += 'c'
        elif event.key == pygame.K_d:
            current_archival += 'd'
        elif event.key == pygame.K_e:
            current_archival += 'e'
        elif event.key == pygame.K_f:
            current_archival += 'f'
        elif event.key == pygame.K_g:
            current_archival += 'g'
        elif event.key == pygame.K_h:
            current_archival += 'h'
        elif event.key == pygame.K_i:
            current_archival += 'i'
        elif event.key == pygame.K_j:
            current_archival += 'j'
        elif event.key == pygame.K_k:
            current_archival += 'k'
        elif event.key == pygame.K_l:
            current_archival += 'l'
        elif event.key == pygame.K_m:
            current_archival += 'm'
        elif event.key == pygame.K_n:
            current_archival += 'n'
        elif event.key == pygame.K_o:
            current_archival += 'o'
        elif event.key == pygame.K_p:
            current_archival += 'p'
        elif event.key == pygame.K_q:
            current_archival += 'q'
        elif event.key == pygame.K_r:
            current_archival += 'r'
        elif event.key == pygame.K_s:
            current_archival += 's'
        elif event.key == pygame.K_t:
            current_archival += 't'
        elif event.key == pygame.K_u:
            current_archival += 'u'
        elif event.key == pygame.K_v:
            current_archival += 'v'
        elif event.key == pygame.K_w:
            current_archival += 'w'
        elif event.key == pygame.K_x:
            current_archival += 'x'
        elif event.key == pygame.K_y:
            current_archival += 'y'
        elif event.key == pygame.K_z:
            current_archival += 'z'
        elif event.key == pygame.K_BACKSPACE and len(current_archival) > 0:  # 按下退格键
            current_archival = current_archival[:-1]
        if len(current_archival) > 15:  # 检测输入是否已经超出15个字符，若超出，则将超出范围提示的图像加入要显示的图像列表中
            page.images_after_num = 1
            page.images.append([page.images_after[1][0], page.images_after[1][1]])
            current_archival = current_archival[:-1]
        font = pygame.font.SysFont('SimSun', int(data[0][0] * page.setting.screen_height))
        page.words[num][0] = font.render(current_archival, True, tuple(data[0][3]))  # 更新页面的文字列表，实时绘制输入的存档名
        words_pos = page.words[num][0].get_rect()
        words_pos.center = (data[0][2][0] * page.setting.screen_width, data[0][2][1] * page.setting.screen_height)
        page.words[num][1] = words_pos
        page.current_archival[1] = current_archival

    def create_archival(self, page):  # 检测存档名字是否合格，若合格则创建存档目录，将相关数据复制到该目录，并修改存储着存档名字的文件
        if len(page.current_archival[1]) == 0:  # 输入名字为空
            if page.images_after_num == 0:
                page.images_after_num = 1
                page.images.append([page.images_after[0][0], page.images_after[0][1]])
        elif page.archival[(page.current_archival[0] + 1) % 3] == page.current_archival[1] or \
                page.archival[(page.current_archival[0] + 2) % 3] == page.current_archival[1]:  # 输入名字已存在
            if page.images_after_num == 0:
                page.images_after_num = 1
                page.images.append([page.images_after[2][0], page.images_after[2][1]])
        else:  # 修改数据，创建存档
            with open(os.path.join('page', 'page1', 'archival.json'), 'r', encoding='utf-8') as f:  # 读取所有存档名字，存储为列表
                archival = json.load(f)
            archival[page.current_archival[0]][1] = page.current_archival[1]  # 修改列表相应位置名字
            with open(os.path.join('page', 'page1', 'archival.json'), "w", encoding='utf-8') as f:  # 将修改后的存档名字列表重新写入文件
                json.dump(archival, f, ensure_ascii=False)
            target_path = os.path.join('page', page.current_archival[1])
            self.copy_dir(os.path.join('page', 'default'), target_path)  # 创建存档目录，并把一些必要数据复制过去
            page.current_archival[0] = -1  # 重置当前选中存档信息
            page.current_archival[1] = ''
            page.update_page_type(1)  # 更新页面类别，回到选择存档界面

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

    @staticmethod
    def delete_archival(current_archival):  # 删除存档目录，修改存储存档名字的文件信息
        shutil.rmtree(os.path.join('page', current_archival[1]))
        with open(os.path.join('page', 'page1', 'archival.json'), 'r', encoding='utf-8') as f:
            archival = json.load(f)
        archival[current_archival[0]][1] = "New Game"
        with open(os.path.join('page', 'page1', 'archival.json'), 'w', encoding='utf-8') as f:
            json.dump(archival, f, ensure_ascii=False)
        current_archival[0] = -1
        current_archival[1] = ''

    @staticmethod
    def enter_game(page, num, change):  # 初始化相关信息并进入游戏
        page.current_archival = [num, page.archival[num]]  # 更新当前游戏中的存档信息
        archival_path = os.path.join('page', page.current_archival[-1], 'page4')
        # 实例化地图
        with open(os.path.join(archival_path, 'floor_data.json'), 'r', encoding='utf-8') as f:
            dictionary = json.load(f)
            dictionary_temp = dictionary.copy()
        for key in dictionary:
            with open(os.path.join(archival_path, 'floor' + str(dictionary[key]), 'map_data.json'), 'r',
                      encoding='utf-8') as f:
                dictionary_temp.update(json.load(f))
        page.game_map = Map(dictionary_temp, page.setting.screen_width, page.setting.screen_height)
        # 实例化角色
        if not change:
            with open(os.path.join(archival_path, 'player', 'player_data.json'), 'r', encoding='utf-8') as f:
                dictionary = json.load(f)
            page.hero = Hero(dictionary, page.setting, page.setting.screen_width, page.setting.screen_height,
                             page.current_archival[1])
        if dictionary_temp['hero_rect_init_sign'] == 0 or dictionary_temp['hero_rect_init_sign'] == 1:
            page.hero.rect.y = dictionary_temp['hero_rect'][1][0] * page.setting.screen_height + \
                               dictionary_temp['hero_rect'][1][1] * page.game_map.wall_width
        else:
            page.hero.rect.bottom = dictionary_temp['hero_rect'][1][0] * page.setting.screen_height + \
                                    dictionary_temp['hero_rect'][1][1] * page.game_map.wall_width
        if dictionary_temp['hero_rect_init_sign'] == 0 or dictionary_temp['hero_rect_init_sign'] == 2:
            page.hero.rect.x = dictionary_temp['hero_rect'][0][0] * page.setting.screen_width + \
                               dictionary_temp['hero_rect'][0][1] * page.game_map.wall_width
        else:
            page.hero.rect.right = dictionary_temp['hero_rect'][0][0] * page.setting.screen_width + \
                                   dictionary_temp['hero_rect'][0][1] * page.game_map.wall_width
        # 实例化怪物
        data = []
        path = os.path.join(archival_path, 'floor' + str(page.game_map.height), 'monster_data.json')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        monster_num = len(data)
        i = 0
        while i < monster_num:
            if not data[i]['die']:
                # noinspection PyTypeChecker
                page.monster.add(Monster(data[i], page.setting.screen_width, page.setting.screen_height))
            i += 1
        # 实例化npc
        data = []
        path = os.path.join(archival_path, 'floor' + str(page.game_map.height), 'npc_data.json')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        for dictionary in data:
            page.npc.add(NPC(dictionary, page.setting.screen_width, page.setting.screen_height))
        # 实例化宝箱
        data = []
        path = os.path.join(archival_path, 'floor' + str(page.game_map.height), 'box_data.json')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        for dictionary in data:
            page.box.add(Box(page.hero.size[0], page.hero.rect, page.setting, dictionary))
        # 实例化商人
        data = []
        path = os.path.join(archival_path, 'floor' + str(page.game_map.height), 'merchant_data.json')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        for dictionary in data:
            page.merchant.add(Merchant(dictionary, page.setting, page.hero.size[0], page.hero.rect))
        # 实例化伤害显示
        page.harm = Harm(page.setting.screen_height)
        if not change:
            page.update_page_type(4)
        page.tip.create_tip("第" + str(page.game_map.height) + "层")

    @staticmethod
    def pause_game_attack(page):  # 游戏画面暂停时计算当前所有拥有攻击行为的对象后摇已冷却时间
        if page.pausing:
            return
        page.pausing = True
        time_now = pygame.time.get_ticks()
        page.hero.attack_time_pause = time_now - page.hero.attack_time
        for monster in page.monster:
            monster.attack_time_pause = time_now - monster.attack_time
            monster.move_time_pause = time_now - monster.move_time
        return

    @staticmethod
    def start_game_attack(page):  # 游戏画面从暂停恢复时重置当前所有拥有攻击行为的对象上次攻击时间
        page.pausing = False
        time_now = pygame.time.get_ticks()
        page.hero.attack_time = time_now - page.hero.attack_time_pause
        for monster in page.monster:
            monster.attack_time = time_now - monster.attack_time_pause
            monster.move_time = time_now - monster.move_time_pause
        return

    @staticmethod
    def box_merchant_check(boxes, merchants):  # 检测宝箱以及商人的状态，返回此刻交互中的宝箱或商人（无交互则返回None）
        box_check, merchant_check = None, None
        for box in boxes:
            if box.opening:
                box_check = box
                break
        for merchant in merchants:
            if merchant.trading:
                merchant_check = merchant
                break
        return box_check, merchant_check

    def change_floor(self, page, change):  # 更改当前地图层数
        self.save_progress(page, change)
        self.enter_game(page, page.current_archival[0], change)

    @staticmethod
    def open_door_enable_check(pos, hero, game_map):  # 判断角色与门之间的距离是否满足可开门的条件，根据判断结果返回相应坐标
        x_gap = abs(pos[0] - hero.rect.centerx)
        y_gap = abs(pos[1] - hero.rect.centery)
        if x_gap < hero.door_enable and y_gap < hero.door_enable:
            y = int((pos[1] - game_map.top) // game_map.wall_width)
            x = int((pos[0] - game_map.left) // game_map.wall_width)
            return x, y
        else:
            return -1, -1

    @staticmethod
    def end_die(page):  # 角色死亡，结束游戏
        # 删除游戏内实例化对象
        page.hero.bullets = pygame.sprite.Group()
        page.hero.sword_attack = pygame.sprite.Group()
        page.monster = pygame.sprite.Group()
        page.monster_bullets = pygame.sprite.Group()
        page.npc = pygame.sprite.Group()
        page.merchant = pygame.sprite.Group()
        page.box = pygame.sprite.Group()
        page.game_map = None

    @staticmethod
    def end_win(page):  # 胜利
        # 删除游戏内实例化对象
        page.hero.bullets = pygame.sprite.Group()
        page.hero.sword_attack = pygame.sprite.Group()
        page.monster = pygame.sprite.Group()
        page.monster_bullets = pygame.sprite.Group()
        page.npc = pygame.sprite.Group()
        page.merchant = pygame.sprite.Group()
        page.box = pygame.sprite.Group()
        page.game_map = None

    @staticmethod
    def save_progress(page, change):  # 保存游戏进度
        page.pausing = False
        screen_width, screen_height = page.setting.screen_width, page.setting.screen_height
        current_archival = page.current_archival[1]  # 获取当前存档名
        # 保存游戏地图相关信息
        data = {"height": page.game_map.height + change}
        with open(os.path.join('page', current_archival, 'page4', 'floor_data.json'), 'w',
                  encoding='utf-8') as f:  # 保存当前地图层数
            json.dump(data, f, ensure_ascii=False)
        path = os.path.join('page', current_archival, 'page4', 'floor' + str(page.game_map.height), 'map_data.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data["layout_data"] = page.game_map.layout_data
        data["left"] = [page.game_map.left / screen_width, 0]
        data["right"] = [page.game_map.right / screen_width, 0]
        data["top"] = [page.game_map.top / screen_height, 0]
        data["bottom"] = [page.game_map.bottom / screen_height, 0]
        data['hero_rect_init_sign'] = 0
        data['hero_rect'] = [[page.hero.rect.x / screen_width, 0], [page.hero.rect.y / screen_height, 0]]
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        # 保存英雄数据
        if not change:
            path = os.path.join('page', current_archival, 'page4', 'player', 'player_data.json')
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data['health'] = page.hero.health
            data['strength'] = page.hero.strength
            data['defence'] = page.hero.defence
            data['speed'] = page.hero.max_speed / screen_height
            data['money'] = page.hero.money
            data['exp'] = page.hero.exp
            data['max_health'] = page.hero.max_health
            data['level'] = page.hero.level
            data['max_exp'] = page.hero.max_exp
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
            # 保存背包信息
            path = os.path.join('page', current_archival, 'page4', 'bag', 'bag_data.json')
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data['equip_wear'] = page.hero.bag.equip_wear
            data['things_kind'] = page.hero.bag.things_kind
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
        # 保存宝箱信息
        if page.box:
            path = os.path.join('page', current_archival, 'page4', 'floor' + str(page.game_map.height), 'box_data.json')
            with open(path, 'r', encoding='utf-8') as f:
                data_list = json.load(f)
            box_num = len(data_list)
            i = 0
            for box in page.box:
                if i == box_num:
                    data_list.append(data_list[-1].copy())
                    box_num += 1
                data_list[i]['rect'] = [box.rect.x / screen_width, box.rect.y / screen_height]
                data_list[i]['things_kind'] = box.things_kind
                i += 1
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data_list, f, ensure_ascii=False)
        # 保存怪物信息
        path = os.path.join('page', current_archival, 'page4', 'floor' + str(page.game_map.height), 'monster_data.json')
        with open(path, 'r', encoding='utf-8') as f:
            data_list = json.load(f)
        monster_num = len(data_list)
        i = 0
        for monster in page.monster:
            while True:
                if data_list[i]["die"]:
                    i += 1
                elif data_list[i]["kind"] != monster.kind:
                    data_list[i]["die"] = 1
                    i += 1
                else:
                    break
            data_list[i]["health"] = monster.health
            data_list[i]["rect"] = [monster.rect.x / screen_width, monster.rect.y / screen_height]
            i += 1
        while i < monster_num:
            data_list[i]["die"] = 1
            i += 1
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False)
        # 保存npc信息
        if page.npc:
            path = os.path.join('page', current_archival, 'page4', 'floor' + str(page.game_map.height), 'npc_data.json')
            with open(path, 'r', encoding='utf-8') as f:
                data_list = json.load(f)
            i = 0
            for npc in page.npc:
                data_list[i]['rect'] = [npc.rect.x / screen_width, npc.rect.y / screen_height]
                data_list[i]['status_start'] = npc.status_start
                data_list[i]['status_end'] = npc.status_end
                i += 1
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data_list, f, ensure_ascii=False)
        # 保存商人信息
        if page.merchant:
            path = os.path.join('page', current_archival, 'page4', 'floor' + str(page.game_map.height),
                                'merchant_data.json')
            with open(path, 'r', encoding='utf-8') as f:
                data_list = json.load(f)
            i = 0
            for merchant in page.merchant:
                data_list[i]['rect'] = [merchant.rect.x / screen_width, merchant.rect.y / screen_height]
                data_list[i]['things_kind'] = merchant.store.things_kind
                i += 1
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data_list, f, ensure_ascii=False)
        # 删除游戏内实例化对象
        page.hero.bullets = pygame.sprite.Group()
        page.hero.sword_attack = pygame.sprite.Group()
        page.monster = pygame.sprite.Group()
        page.monster_bullets = pygame.sprite.Group()
        page.npc = pygame.sprite.Group()
        page.merchant = pygame.sprite.Group()
        page.box = pygame.sprite.Group()
        page.game_map = None
        if not change:
            page.current_archival = [-1, '']
            page.hero = None
            page.tip.create_tip("游戏进度已保存")

    @staticmethod
    def change_music_state(page, num, state):  # 改变游戏音乐或音效开关状态
        with open(os.path.join('page', 'page5', 'images.json'), 'r', encoding='utf-8') as f:  # 读取音效图像信息
            data = json.load(f)
        if data[num][0][2] == "on.bmp":  # 修改状态
            data[num][0][2] = "off.bmp"
        else:
            data[num][0][2] = "on.bmp"
        path = ''
        for directory in data[num][0]:
            path = os.path.join(path, directory)
        image = pygame.image.load(path)
        # 要转换的图像尺寸
        size = (page.images[num][2][0] - page.images[num][1][0], page.images[num][2][1] - page.images[num][1][1])
        page.images[num][0] = pygame.transform.scale(image, size)  # 更新图像
        with open(os.path.join('page', 'page5', 'images.json'), "w", encoding='utf-8') as f:  # 将最终效果保存至文件
            json.dump(data, f, ensure_ascii=False)
        return not state

    @staticmethod
    def change_volume_instant(page, event):  # 修改游戏音量
        screen_width = page.setting.screen_width
        with open(os.path.join('page', 'page5', 'images.json'), 'r', encoding='utf-8') as f:  # 读取音效图像信息
            data = json.load(f)
        data[7][1][0] = (event.pos[0] - data[7][2][0] * screen_width / 2) / screen_width
        if data[7][1][0] + data[7][2][0] / 2 < data[6][1][0]:
            data[7][1][0] = data[6][1][0] - data[7][2][0] / 2
        elif data[7][1][0] + data[7][2][0] / 2 >= data[6][1][0] + data[6][2][0]:
            data[7][1][0] = data[6][1][0] + data[6][2][0] - data[7][2][0] / 2
        page.setting.volume[1] = (data[7][1][0] + data[7][2][0] / 2) * screen_width  # 修改游戏音量
        page.images[7][1] = (data[7][1][0] * screen_width, page.images[7][1][1])
        page.images[7][2] = (page.images[7][1][0] + data[7][2][0] * screen_width, page.images[7][2][1])
        with open(os.path.join('page', 'page5', 'images.json'), "w", encoding='utf-8') as f:  # 将最终效果保存至文件
            json.dump(data, f, ensure_ascii=False)

    @staticmethod
    def change_volume_constant(page, event):  # 鼠标拖动音量刻度改变音量大小
        width = page.images[7][2][0] - page.images[7][1][0]  # 音量刻度的宽度
        if page.images[6][1][0] <= event.pos[0] < page.images[6][2][0]:
            page.setting.volume[1] = event.pos[0]
            page.images[7][1] = (event.pos[0] - width / 2, page.images[7][1][1])
            page.images[7][2] = (event.pos[0] + width / 2, page.images[7][2][1])
        elif event.pos[0] < page.images[6][1][0]:  # 防止音量刻度越界
            page.setting.volume[1] = page.images[6][1][0]
            page.images[7][1] = (page.setting.volume[1] - width / 2, page.images[7][1][1])
            page.images[7][2] = (page.setting.volume[1] + width / 2, page.images[7][2][1])
        else:
            page.setting.volume[1] = page.images[6][2][0] - 1
            page.images[7][1] = (page.setting.volume[1] - width / 2, page.images[7][1][1])
            page.images[7][2] = (page.setting.volume[1] + width / 2, page.images[7][2][1])

    @staticmethod
    def change_help_tip(pos, move, images, images_after):  # 游戏帮助小提示切换页数
        num = len(images_after)
        pos_temp = pos + move
        if pos_temp < 0:
            pos_temp = 0
        elif pos_temp >= num:
            pos_temp = num - 1
        images[2] = images_after[pos_temp]
        return pos_temp
