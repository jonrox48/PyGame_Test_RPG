# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 09:54:28 2023

@author: j91722
"""

import pygame
from config import *
import math
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
        
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):        
        ####################################################################
        ########################## CONFIGURATION ###########################
        ####################################################################
        ## Define which game object it is a part ot
        self.game = game
        
        ## Define which layer this sprite should be drawn in 
        self._layer = PLAYER_LAYER
        
        ## Define which groups this sprite should be a part of 
        self.groups = self.game.all_sprites
        
        ## Initialize inherited pygame Sprite Class
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        ## Sprite Dimensions
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        ## Sprite Image
        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

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
        
        ## Current collision box
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y        
        
        ## Temp Variables
        self.x_change = 0
        self.y_change = 0
        
        
    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()
        
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        
        self.x_change = 0
        self.y_change = 0
        
    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
                    self.rect.x = hits[0].rect.right
                    
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
                    self.rect.y = hits[0].rect.bottom
    
    
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False
                    
    def movement(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
        
    def animate(self):
        ## Define location of animations for each direction in character spritesheet
        down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]
        
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                    
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                    
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                                   
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):        
        ####################################################################
        ########################## CONFIGURATION ###########################
        ####################################################################
        ## Define which game object it is a part ot
        self.game = game
        
        ## Define which layer this sprite should be drawn in 
        self._layer = ENEMY_LAYER
        
        ## Define which groups this sprite should be a part of 
        self.groups = self.game.all_sprites, self.game.enemies
        
        ## Initialize inherited pygame Sprite Class
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        ## Sprite Dimensions
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        ## Sprite Image
        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)

        #######################################################################
        ########################## STATUS #####################################
        #######################################################################
        ## Current Orientation
        self.facing = random.choice(['left', 'right'])
        # 2 total animations
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)
        
        ## Current Location
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        
        ## Current collision box
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y        
        
        ## Temp Variables
        self.x_change = 0
        self.y_change = 0
        
        
    def update(self):
        self.movement()
        self.animate()
        
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        
        self.x_change = 0
        self.y_change = 0
        
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
                    
    def movement(self):
        # keys = pygame.key.get_pressed()
        
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'
        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'
        if self.facing == 'up':
            self.y_change -= ENEMY_SPEED
        if self.facing == 'down':
            self.y_change += ENEMY_SPEED
        
    def animate(self):
        ## Define location of animations for each direction in character spritesheet
        down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height)]

        up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height)]

        left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]
        
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                    
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                    
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
            
class Collision_Block(pygame.sprite.Sprite):
    # def __init__(self, game, x, y):
    #     self.game = game
    #     self._layer = BLOCK_LAYER
    #     self.groups = self.game.all_sprites, self.game.blocks
    #     pygame
        
    def __init__(self, game, x, y):
        
        ####################################################################
        ########################## CONFIGURATION ###########################
        ####################################################################
        ## Define which game object it is a part ot
        self.game = game
        
        ## Define which layer this sprite should be drawn in 
        self._layer = BLOCK_LAYER
        
        ## Define which groups this sprite should be a part of 
        self.groups = self.game.all_sprites, self.game.blocks
        
        ## Initialize inherited pygame Sprite Class
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        ## Sprite Dimensions
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        ## Sprite Image
        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)

        #######################################################################
        ########################## STATUS ###########################
        #######################################################################
        ## Current Orientation
        self.facing = 'down'
        
        ## Current Location
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        
        ## Define collision box
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y        
        
class Ground(pygame.sprite.Sprite):
    # def __init__(self, game, x, y):
    #     self.game = game
    #     self._layer = BLOCK_LAYER
    #     self.groups = self.game.all_sprites, self.game.blocks
    #     pygame
        
    def __init__(self, game, x, y):
        
        ####################################################################
        ########################## CONFIGURATION ###########################
        ####################################################################
        ## Define which game object it is a part ot
        self.game = game
        
        ## Define which layer this sprite should be drawn in 
        self._layer = GROUND_LAYER
        
        ## Define which groups this sprite should be a part of 
        self.groups = self.game.all_sprites
        
        ## Initialize inherited pygame Sprite Class
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        ## Sprite Dimensions
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        ## Sprite Image
        self.image = self.game.terrain_spritesheet.get_sprite(0, 352, self.width, self.height)

        #######################################################################
        ########################## STATUS ###########################
        #######################################################################
        ## Current Orientation
        self.facing = 'down'
        
        ## Current Location
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        
        ## Define collision box
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y        
              
class Button:
    def __init__(self, x, y, width, height, fg_col, bg_col, content, fontsize):
        self.font = pygame.font.Font('fonts/ARIAL.TTF', fontsize)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg_col = fg_col
        self.bg_col = bg_col
        
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg_col)
        self.rect = self.image.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.text = self.font.render(self.content, True, self.fg_col)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)
        
    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
    
    
                