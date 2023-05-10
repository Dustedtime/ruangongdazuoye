import json

import pygame

dictionary = {'height': 1}
with open('floor.json', 'w') as f:
    json.dump(dictionary, f)
pygame.transform.scale()