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
    def __init__(self, character, x, y):
        super().__init__(character.level, x, y)
        ####################################################################
        ########################## LOGISTICS ###############################
        ####################################################################
        ## Define which layer this sprite should be drawn in 
        self._layer = character._layer
        ## Define which groups this sprite should be a part of 
        self.groups.append(self.level.attacks)
        ## Initialize inherited pygame Sprite Class
        pygame.sprite.Sprite.__init__(self, tuple(self.groups))
        self.character = character
        self.character.attacking = True
        
        self.name = 'attack'
        self.character.keylist.append(self.name)
        
        #######################################################################
        ########################## STATUS #####################################
        #######################################################################
        ## Current Location (CURRENTLY THIS IS BEING PASSED BY THE CHARACTER OBJ, SO ITS ALREADY IN PIXELS, NO NEED TO MULTIPLY BY TILE_SIZE)
        self.facing = self.character.facing
        self.x = x
        self.y = y
        #######################################################################
        ########################## ANIMATIONS #####################################
        #######################################################################
        ## Sprite Image
        self.spritesheet = self.level.attack_spritesheet
        pixel_x_start = 0
        pixel_y_start = 0
        self.animation_num_of_frames = 5
        self.animation_loop = 0
        self.speed = 17
        self.load_animations_directional(pixel_x_start, pixel_y_start)

        
    def update(self):
        self.collide()        
        self.animate()
        
    def collide(self):
        if self.character in self.level.player_group.sprites():
            pygame.sprite.spritecollide(self, self.level.non_player, True)
        elif self.character in self.level.enemies.sprites():
            pygame.sprite.spritecollide(self, self.level.villagers, True)
        elif self.character in self.level.villagers.sprites():
            pygame.sprite.spritecollide(self, self.level.enemies, True)
        
    def animate(self):
        if self.facing == "down":
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += self.animation_speed_base*self.speed
            if self.animation_loop >= len(self.down_animations):
                self.character.attacking = False       
                self.character.keylist.remove(self.name)
                self.kill()

                    
        if self.facing == "up":
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += self.animation_speed_base*self.speed
            if self.animation_loop >= len(self.up_animations):
                self.character.attacking = False  
                self.character.keylist.remove(self.name)
                self.kill()

        
        if self.facing == "left":
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += self.animation_speed_base*self.speed
            if self.animation_loop >= len(self.left_animations):
                self.character.attacking = False          
                self.character.keylist.remove(self.name)
                self.kill()

                    
        if self.facing == "right":
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += self.animation_speed_base*self.speed
            if self.animation_loop >= len(self.right_animations):
                self.character.attacking = False    
                self.character.keylist.remove(self.name)
                self.kill()

