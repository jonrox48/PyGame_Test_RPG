# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 15:32:15 2023

@author: Huge Mstr
"""

import pygame
from config import *
from sprites import *


class Non_Collision_Block(Sprite):
    def __init__(self, game, x, y):
        ####################################################################
        ########################## LOGISTICS ###############################
        ####################################################################
        ## Inherit from Sprite class
        super().__init__(game, x, y)        
        ## Define which layer this sprite should be drawn in 
        self._layer = GROUND_LAYER
        ## Define which groups this sprite should be a part of 
        self.groups.append(self.game.non_collision_blocks)

        
class Grass(Non_Collision_Block):        
    def __init__(self, game, x, y):
        ####################################################################
        ########################## LOGISTICS ###############################
        ####################################################################
        ## Inherit from Non_Collision_Block class
        super().__init__(game, x, y)        
        ## Initialize inherited pygame Sprite Class
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        #######################################################################
        ########################## SPRITE #####################################
        #######################################################################
        self.spritesheet = self.game.terrain_spritesheet
        self.load_sprite(0, 352)
