# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 10:12:30 2023

@author: Huge Mstr
"""

import pygame
from config import *
import math
import random
from sprites import *
import pdb
import numpy as np

class Character(pygame.sprite.Sprite):
    def __init__(self, game, x, y):        
        ####################################################################
        ########################## CONFIGURATION ###########################
        ####################################################################
        ## Define which game object it is a part ot
        self.game = game
        
        ## Define which groups this sprite should be a part of 
        self.groups = self.game.all_sprites
        
        ## Sprite Dimensions
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        # ## Sprite Image
        ## Define which layer this sprite should be drawn in 
        self._layer = []        
        self.spritesheet = []
        self.rect = []
        self.speed = []
        
        #######################################################################
        ########################## STATUS #####################################
        #######################################################################
        ## Current Orientation
        self.facing = 'down'
        # 2 total animations
        self.animation_loop = 1
        
        ## Current Location
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        
        ## Temp Variables
        self.x_change = 0
        self.y_change = 0
        
    
    def load_animations(self, x_start, y_start):
        ## Load animations
        self.down_animations = [self.spritesheet.get_sprite(x_start,                    y_start,                     self.width, self.height),
                                self.spritesheet.get_sprite(x_start +  self.width,      y_start,                     self.width, self.height),
                                self.spritesheet.get_sprite(x_start + (self.width * 2), y_start,                     self.width, self.height)]
        
        self.up_animations =   [self.spritesheet.get_sprite(x_start,                    y_start + self.height,       self.width, self.height),
                                self.spritesheet.get_sprite(x_start +  self.width,      y_start + self.height,       self.width, self.height),
                                self.spritesheet.get_sprite(x_start + (self.width * 2), y_start + self.height,       self.width, self.height)]
        
        self.right_animations =[self.spritesheet.get_sprite(x_start,                    y_start + (self.height * 2), self.width, self.height),
                                self.spritesheet.get_sprite(x_start +  self.width,      y_start + (self.height * 2), self.width, self.height),
                                self.spritesheet.get_sprite(x_start + (self.width * 2), y_start + (self.height * 2), self.width, self.height)]
        
        self.left_animations = [self.spritesheet.get_sprite(x_start,                    y_start + (self.height * 3), self.width, self.height),
                                self.spritesheet.get_sprite(x_start +  self.width,      y_start + (self.height * 3), self.width, self.height),
                                self.spritesheet.get_sprite(x_start + (self.width * 2), y_start + (self.height * 3), self.width, self.height)]
        
        ## Load collision box
        self.rect = self.down_animations[0].get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 
            
        
    # Update for all characters. Will be overwritten for player character
    def update(self):
        pass
        
    ## Movement function for all characters. Will be overwritten for player character
    def movement(self):
        pass
    
    ## This will be overwritten for the player character so all other sprites move, causing a camera effect
    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    
    def animate(self):
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.down_animations[0]
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.3/self.speed
                if self.animation_loop >= len(self.down_animations):
                    self.animation_loop = 1
                    
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.up_animations[0]
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.3/self.speed
                if self.animation_loop >= len(self.up_animations):
                    self.animation_loop = 1
        
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.3/self.speed
                if self.animation_loop >= len(self.left_animations):
                    self.animation_loop = 1
                    
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.3/self.speed
                if self.animation_loop >= len(self.right_animations):
                    self.animation_loop = 1


class Player(Character):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        ####################################################################
        ########################## CONFIGURATION ###########################
        ####################################################################
        ## Define which layer this sprite should be drawn in 
        self._layer = PLAYER_LAYER
        self.speed = PLAYER_SPEED
        
        self.groups = self.game.all_sprites, self.game.player_group
        
        ## Initialize inherited pygame Sprite Class
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        ## Sprite Image
        self.spritesheet = self.game.character_spritesheet
        pixel_x_start = 3
        pixel_y_start = 2
        
        #######################################################################
        ########################## ANIMATIONS #####################################
        #######################################################################
        self.load_animations(pixel_x_start, pixel_y_start)
  
    def update(self):
        self.movement()
        self.animate()
        
        self.rect.x += self.x_change        
        self.collide_non_player_character('x')        
        self.collide_blocks('x')
        self.rect.y += self.y_change        
        self.collide_non_player_character('y')        
        self.collide_blocks('y')
        
        for sprite in self.game.all_sprites:
            sprite.rect.x -= self.x_change
            sprite.rect.y -= self.y_change
            
        self.x_change = 0
        self.y_change = 0
    
    def collide_non_player_character(self, direction):        
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.non_player, False)
            if hits:
                self.kill()
                self.game.playing = False
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.non_player, False)
            if hits:
                self.kill()
                self.game.playing = False

            
    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.x_change = 0
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.x_change = 0
                    self.rect.x = hits[0].rect.right
                    
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.y_change = 0
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.y_change = 0
                    self.rect.y = hits[0].rect.bottom            
                    
    def movement(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.x_change -= self.speed
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += self.speed
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= self.speed
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += self.speed
            self.facing = 'down'
            

                    
class Non_Player(Character):
    def __init__(self, game, x, y): 
        super().__init__(game, x, y)
        ####################################################################
        ########################## CONFIGURATION ###########################
        ####################################################################
        
        ## Define which layer this sprite should be drawn in 
        self._layer = NON_PLAYER_LAYER
        self.speed = NON_PLAYER_SPEED
        
        ## Define which groups this sprite should be a part of 
        self.groups = self.game.all_sprites, self.game.non_player
        
        ## Initialize inherited pygame Sprite Class
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        ## Sprite Image
        self.spritesheet = self.game.non_player_spritesheet
        pixel_x_start = 3
        pixel_y_start = 2
        
        ## NPC "BRAIN"
        self.command_current = random.choice(['up', 'down', 'left', 'right'])
        self.command_length = random.randint(7,30)
        self.command_loop = 0

        #######################################################################
        ########################## ANIMATIONS #####################################
        #######################################################################
        self.load_animations(pixel_x_start, pixel_y_start)
        
        
    # Update for all non-player characters
    def update(self):
        if self.command_loop < self.command_length:
            self.command_loop += 1
        else:
            self.command_current = random.choice(['up', 'down', 'left', 'right'])
            self.command_length = random.randint(7,30)
            self.command_loop = 0        
            
        self.movement()
        self.animate()
        
        self.rect.x += self.x_change
        self.collide_blocks('x')
        # self.collide_player_character('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        # self.collide_player_character('y')
        
        self.x_change = 0
        self.y_change = 0
        
    ## Movement function for all characters. Will be overwritten for player character
    def movement(self):
        if self.command_current == 'left':
            self.x_change -= self.speed
            self.facing = 'left'
        if self.command_current == 'right':
            self.x_change += self.speed
            self.facing = 'right'
        if self.command_current == 'up':
            self.y_change -= self.speed
            self.facing = 'up'
        if self.command_current == 'down':
            self.y_change += self.speed
            self.facing = 'down'
            
    # def collide_player_character(self, direction):
    #     if direction == 'x':
    #         hits = pygame.sprite.spritecollide(self, self.game.player_group, False)
    #         if hits:
    #             if self.x_change > 0:
    #                 self.rect.x = hits[0].rect.left - self.rect.width
    #             if self.x_change < 0:
    #                 self.rect.x = hits[0].rect.right
    #     if direction == 'y':
    #         hits = pygame.sprite.spritecollide(self, self.game.player_group, False)
    #         if hits:
    #             if self.y_change > 0:
    #                 self.rect.y = hits[0].rect.top - self.rect.height
    #             if self.y_change < 0:
    #                 self.rect.y = hits[0].rect.bottom
