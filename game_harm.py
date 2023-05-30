import json
import os


class Harm:
    def __init__(self):
        self.hero_rect = None
        self.monster_rect = None
        self.speed = 0

    def init_data(self):
        with open(os.path.join('page', 'page4', 'harm.json'), 'r') as f:
            dictionary = json.load(f)
        self.speed = dictionary['speed']
