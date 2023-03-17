# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 10:12:30 2023

@author: Huge Mstr
"""

import pygame
import math
import random
from config import *
from sprites import *
from attacks import *
# import numpy as np

## Purely Parent Class. No loading animations
class Character(Sprite):
    def __init__(self, game, x, y):
        ####################################################################
        ########################## CONFIGURATION ###########################
        ####################################################################        
        ## Inherit from Sprite class
        super().__init__(game, x, y)     
        ## Define which groups this sprite should be a part of
        self.groups.append(self.game.characters)
        
        #######################################################################
        ########################## STATUS #####################################
        #######################################################################
        ## Current Orientation
        self.facing = 'down'
        
        #######################################################################
        ########################## TEMP VARIABLES #############################
        #######################################################################
        self.x_change = 0
        self.y_change = 0
        
    def load_animations(self, x_start, y_start):
        ## Load animations
        self.down_animations = []
        self.up_animations = []
        self.right_animations = []
        self.left_animations = []
        
        for frame in range(self.animation_num_of_frames):
            self.down_animations.append( self.spritesheet.get_sprite(x_start + (self.width * frame), y_start,                     self.width, self.height))
            self.up_animations.append(   self.spritesheet.get_sprite(x_start + (self.width * frame), y_start +  self.height,      self.width, self.height))
            self.right_animations.append(self.spritesheet.get_sprite(x_start + (self.width * frame), y_start + (self.height * 2), self.width, self.height))
            self.left_animations.append( self.spritesheet.get_sprite(x_start + (self.width * frame), y_start + (self.height * 3), self.width, self.height))
        
        ## Load collision box
        self.rect = self.down_animations[0].get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.collision_blocks, False)
            if hits:
                if self.x_change > 0:
                    self.x_change = 0
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.x_change = 0
                    self.rect.x = hits[0].rect.right
                return True
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.collision_blocks, False)
            if hits:
                if self.y_change > 0:
                    self.y_change = 0
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.y_change = 0
                    self.rect.y = hits[0].rect.bottom
                return True
                    
    def animate(self):
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.down_animations[0]
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed_base*self.speed
                if self.animation_loop >= len(self.down_animations):
                    self.animation_loop = 1
                    
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.up_animations[0]
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed_base*self.speed
                if self.animation_loop >= len(self.up_animations):
                    self.animation_loop = 1
        
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed_base*self.speed
                if self.animation_loop >= len(self.left_animations):
                    self.animation_loop = 1
                    
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed_base*self.speed
                if self.animation_loop >= len(self.right_animations):
                    self.animation_loop = 1


class Player(Character):
    def __init__(self, game, x, y):
        #######################################################################
        ########################## LOGISTICS ##################################
        ####################################################################### 
        ## Inherit from Character class
        super().__init__(game, x, y)
        ## The player should have his own layer
        self._layer = PLAYER_LAYER        
        ## Add to the player group
        self.groups.append(self.game.player_group)
        ## Lowest level group so initialize groups 
        pygame.sprite.Sprite.__init__(self, tuple(self.groups))
        
        #######################################################################
        ########################## STATS ######################################
        #######################################################################
        self.speed = PLAYER_SPEED

        #######################################################################
        ########################## ANIMATIONS #################################
        #######################################################################
        self.spritesheet = self.game.character_spritesheet
        ## Where in the spritesheet is the top left corner of the first sprite?
        pixel_x_start = 3
        pixel_y_start = 2
        self.load_animations(pixel_x_start, pixel_y_start)
  
    def update(self):
        self.events()
        self.animate()
        
        #######################################################################
        ####################### CHECK FOR COLLISIONS ##########################
        ####################################################################### 
        self.rect.x += self.x_change
        self.collide_enemies_character('x')
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_enemies_character('y')
        self.collide_blocks('y')
        
        #######################################################################
        ####################### CAMERA FOLLOWING PLAYER #######################
        ####################################################################### 
        for sprite in self.game.all_sprites:
            sprite.rect.x -= self.x_change
            sprite.rect.y -= self.y_change
        
        #######################################################################
        ####################### RESET TEMP VARIABLES ##########################
        ####################################################################### 
        self.x_change = 0
        self.y_change = 0
    
    def collide_enemies_character(self, direction):  
        ## Check for any collisions with the enemies group
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        ## Do we need to break into x and y? #TODO
        if direction == 'x':
            if hits:
                ## Right now if we collide with an enemy, we die immediately, someday, we will want to add health #TODO
                self.kill()
                self.game.playing = False
        if direction == 'y':
            if hits:
                ## Right now if we collide with an enemy, we die immediately, someday, we will want to add health #TODO
                self.kill()
                self.game.playing = False
                    
    def events(self):
        #######################################################################
        ####################### BUTTONS THAT ARE HELD #########################
        ####################################################################### 
        keys = pygame.key.get_pressed()
        ## Movement
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
        
        #######################################################################
        ####################### SINGLE BUTTON PRESSES #########################
        ####################################################################### 
        for event in self.game.events_list:
            if event.type == pygame.KEYDOWN:
                ## Basic attack
                if event.key == pygame.K_SPACE:
                    if self.facing == 'up':
                        Attack(self.game, self.rect.x, self.rect.y - TILE_SIZE)
                    if self.facing == 'down':
                        Attack(self.game, self.rect.x, self.rect.y + TILE_SIZE)
                    if self.facing == 'left':
                        Attack(self.game, self.rect.x - TILE_SIZE, self.rect.y)
                    if self.facing == 'right':
                        Attack(self.game, self.rect.x + TILE_SIZE, self.rect.y)
            

## Purely Parent Class. No loading animations    
class Non_Player(Character):
    def __init__(self, game, x, y): 

        #######################################################################
        ########################## LOGISTICS ##################################
        ####################################################################### 
        ## Inherit from Character class
        super().__init__(game, x, y)        
        ## Define which layer this sprite should be drawn in. All non-players should be drawn on the same layer.(I think?)
        self._layer = NON_PLAYER_LAYER
        ## Add to non-player group
        self.groups.append(self.game.non_player)
        
        #######################################################################
        ########################## NPC "BRAIN" ################################
        #######################################################################
        self.command_current = []
        self.command_length = 0
        self.command_loop = 0
    
    def update(self):
        #######################################################################
        ####################### EXECUTE BRAIN #################################
        ####################################################################### 
        self.npc_brain()
        self.movement()
        self.animate()
        
        #######################################################################
        ####################### CHECK FOR COLLISIONS ##########################
        ####################################################################### 
        self.rect.x += self.x_change
        ## If the NPC is running into a block, end command early
        if self.collide_blocks('x'):
            self.command_length = 0
            
        self.rect.y += self.y_change
        ## If the NPC is running into a block, end command early
        if self.collide_blocks('y'):
            self.command_length = 0
            
        #######################################################################
        ####################### RESET TEMP VARIABLES ##########################
        ####################################################################### 
        self.x_change = 0
        self.y_change = 0
        
    def npc_brain(self):
        ## Command Initializations
        available_commands = ['wait', 'up', 'down', 'left', 'right']
        command_length_min = 60
        command_length_max = 120
        
        ## If current command is still being executed
        if self.command_loop < self.command_length:
            self.command_loop += 1
        ## If current command has ended, pick a new command
        else:
            self.command_current = random.choice(available_commands)
            self.command_length = random.randint(command_length_min, command_length_max)
            self.command_loop = 0
        
    def movement(self):
        ## Execute movement commands
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
        if self.command_current == 'wait':
            self.x_change = 0
            self.y_change = 0


class Villager(Non_Player):
    def __init__(self, game, x, y):        
        #######################################################################
        ########################## LOGISTICS ##################################
        ####################################################################### 
        ## Inherit from Character class
        super().__init__(game, x, y)        
        ## Add to villager group 
        self.groups.append(self.game.villagers)
        ## Lowest level group so initialize groups 
        pygame.sprite.Sprite.__init__(self, tuple(self.groups))
        
        #######################################################################
        ########################## STATS ######################################
        #######################################################################        
        self.speed = VILLAGER_SPEED

        #######################################################################
        ########################## ANIMATIONS #################################
        #######################################################################
        self.spritesheet = self.game.character_spritesheet
        pixel_x_start = 3
        pixel_y_start = 2        
        self.load_animations(pixel_x_start, pixel_y_start)