# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 10:13:06 2023

@author: Huge Mstr
"""

import pygame
from config import *
import math
import random
from sprites import *
from characters import *


## Purely Parent Class. No loading animations
class Enemy(Non_Player):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        ## Initialize inherited pygame Sprite Class
        self.groups.append(self.game.enemies)
        


class Zombie(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        self.groups.append(self.game.zombies)
        pygame.sprite.Sprite.__init__(self, tuple(self.groups))
        ## Sprite Image
        self.spritesheet = self.game.non_player_spritesheet
        pixel_x_start = 3
        pixel_y_start = 2
        self.load_animations(pixel_x_start, pixel_y_start)