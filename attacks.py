# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 15:01:16 2023

@author: Huge Mstr
"""

import pygame
from settings import *
from sprites import Sprite
import math
import random

class Attack(Sprite):
    def __init__(self, level, x, y):      
        super().__init__(level, x, y) 
        ####################################################################
        ########################## CONFIGURATION ###########################
        ####################################################################
        ## Define which game object it is a part ot
        self.level = level
        
        ## Define which layer this sprite should be drawn in 
        self._layer = PLAYER_LAYER
        
        ## Define which groups this sprite should be a part of 
        self.groups = self.level.all_sprites, self.level.attacks
        
        ## Initialize inherited pygame Sprite Class
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        ## Sprite Dimensions
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        ## Sprite Image
        self.image = self.level.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        #######################################################################
        ########################## STATUS #####################################
        #######################################################################
        # 2 total animations
        self.animation_loop = 0
        
        ## Current Location
        self.x = x
        self.y = y
        
        ## Current collision box
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        #######################################################################
        ########################## ANIMATIONS #####################################
        #######################################################################
        self.right_animations = [self.level.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.level.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.level.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.level.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.level.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.level.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.level.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.level.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.level.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.level.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.level.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.level.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.level.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.level.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.level.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.level.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.level.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.level.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.level.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.level.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

        
    def update(self):
        self.animate()
        self.collide()
        
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.level.non_player, True)
        
    def animate(self):
        direction = self.level.player.facing
        
        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
                
        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
                
        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
                
        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
