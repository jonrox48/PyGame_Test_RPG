# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 10:13:06 2023

@author: Huge Mstr
"""

import pygame
from config import *
from characters import *


## Purely Parent Class. No loading animations
class Enemy(Non_Player):
    def __init__(self, game, x, y):
        #######################################################################
        ########################## LOGISTICS ##################################
        ####################################################################### 
        ## Inherit from Non_Player class
        super().__init__(game, x, y)
        ## Add to enemies group
        self.groups.append(self.game.enemies)

class Zombie(Enemy):
    def __init__(self, game, x, y):
        #######################################################################
        ########################## LOGISTICS ##################################
        ####################################################################### 
        ## Inherit from Enemies class
        super().__init__(game, x, y)
        ## Add to zombie group
        self.groups.append(self.game.zombies)
        ## Lowest level group so initialize groups 
        pygame.sprite.Sprite.__init__(self, tuple(self.groups))
        
        #######################################################################
        ########################## STATS ######################################
        #######################################################################  
        self.speed = ZOMBIE_SPEED
        
        #######################################################################
        ########################## ANIMATIONS #################################
        #######################################################################
        self.spritesheet = self.game.non_player_spritesheet
        pixel_x_start = 3
        pixel_y_start = 2
        self.load_animations(pixel_x_start, pixel_y_start)
        