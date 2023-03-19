# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 15:37:08 2023

@author: Huge Mstr
"""
import pygame
from settings import *
from sprites import *

class Collision_Block(Sprite):
    def __init__(self, level, x, y):
        ####################################################################
        ########################## LOGISTICS ###############################
        ####################################################################
        ## Inherit from Sprite class
        super().__init__(level, x, y)        
        ## Define which layer this sprite should be drawn in 
        self._layer = BLOCK_LAYER
        ## Define which groups this sprite should be a part of 
        self.groups.append(self.level.collision_blocks)

        
class Rock(Collision_Block):
    def __init__(self, level, x, y):
        ####################################################################
        ########################## LOGISTICS ###############################
        ####################################################################
        ## Inherit from Collision_Block class
        super().__init__(level, x, y)        
        ## Initialize inherited pygame Sprite Class
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        #######################################################################
        ########################## SPRITE #####################################
        #######################################################################
        self.spritesheet = self.level.terrain_spritesheet
        self.load_sprite(960, 448)
