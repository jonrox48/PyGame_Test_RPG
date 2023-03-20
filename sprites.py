# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 09:54:28 2023

@author: j91722
"""

import pygame
from settings import *
# from levels import *
import math

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
        
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite
    
class Sprite(pygame.sprite.Sprite):
    def __init__(self, level, x, y):
        ####################################################################
        ########################## CONFIGURATION ###########################
        ####################################################################
        ## Define which game object it is a part ot
        self.level = level
        ## Define which groups this sprite should be a part of         
        self.groups = [self.level.all_sprites]
        
        ## Sprite Dimensions
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        #######################################################################
        ########################## STATUS #####################################
        #######################################################################
        # 2 total animations
        self.animation_loop = 1
        self.animation_num_of_frames = 3
        self.animation_speed_base = 0.03
        
        ## Current Location
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        
        
    def load_sprite(self, x_start, y_start):
        ## Load image
        self.image = self.spritesheet.get_sprite(x_start, y_start, self.width, self.height)
        
        ## Load collision box
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def load_animations(self, x_start, y_start):
        ## Load animations
        self.animations = []
        
        for frame in range(self.animation_num_of_frames):
            self.animations.append(self.spritesheet.get_sprite(x_start + (self.width * frame), y_start, self.width, self.height))
        
        ## Load collision box
        self.rect = self.animations[0].get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def load_animations_directional(self, x_start, y_start):
        ## Load animations
        self.down_animations = []
        self.up_animations = []
        self.right_animations = []
        self.left_animations = []
        
        ## Requires the order to be DOWN, UP, RIGHT, LEFT
        for frame in range(self.animation_num_of_frames):
            self.down_animations.append( self.spritesheet.get_sprite(x_start + (self.width * frame), y_start,                     self.width, self.height))
            self.up_animations.append(   self.spritesheet.get_sprite(x_start + (self.width * frame), y_start +  self.height,      self.width, self.height))
            self.right_animations.append(self.spritesheet.get_sprite(x_start + (self.width * frame), y_start + (self.height * 2), self.width, self.height))
            self.left_animations.append( self.spritesheet.get_sprite(x_start + (self.width * frame), y_start + (self.height * 3), self.width, self.height))
        
        ## Load collision box
        self.image = self.down_animations[0]
        self.rect = self.down_animations[0].get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

                    
    def animate(self):
        self.image = self.animations[math.floor(self.animation_loop)]
        self.animation_loop += self.animation_speed_base * self.speed
        if self.animation_loop >= len(self.animations):
            self.animation_loop = 1
            
