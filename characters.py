# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 10:12:30 2023

@author: Huge Mstr
"""

import pygame
import math
import random
from settings import *
from sprites import *
from attacks import *
from debug import debug
# import numpy as np

## Purely Parent Class. No loading animations
class Character(Sprite):
    def __init__(self, level, x, y):
        ####################################################################
        ########################## CONFIGURATION ###########################
        ####################################################################        
        ## Inherit from Sprite class
        super().__init__(level, x, y)     
        ## Define which groups this sprite should be a part of
        self.groups.append(self.level.characters)
        self.x_overlap_offset = 0
        self.y_overlap_offset = -30
        
        #######################################################################
        ########################## STATUS #####################################
        #######################################################################
        ## Current Orientation
        self.facing = 'down'
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.keylist = []
        
        
    def collide_blocks(self, direction):
        if direction == 'x':
            for sprite in self.level.collision_blocks:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right
                    self.direction.x = 0                        
                    return True
        if direction == 'y':
            for sprite in self.level.collision_blocks:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    self.direction.y = 0                        
                    return True
                    
    def animate(self):
        if self.facing == "down":
            if self.direction.y == 0:
                self.image = self.down_animations[0]
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed_base*self.speed
                if self.animation_loop >= len(self.down_animations):
                    self.animation_loop = 1
                    
        if self.facing == "up":
            if self.direction.y == 0:
                self.image = self.up_animations[0]
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed_base*self.speed
                if self.animation_loop >= len(self.up_animations):
                    self.animation_loop = 1
        
        if self.facing == "left":
            if self.direction.x == 0:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed_base*self.speed
                if self.animation_loop >= len(self.left_animations):
                    self.animation_loop = 1
                    
        if self.facing == "right":
            if self.direction.x == 0:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed_base*self.speed
                if self.animation_loop >= len(self.right_animations):
                    self.animation_loop = 1
                    
    def attack(self):
        if self.facing == 'up':
            Attack(self, self.rect.x, self.rect.y - TILE_SIZE)
            self.direction.x = 0
            self.direction.y = 0
        if self.facing == 'down':
            Attack(self, self.rect.x, self.rect.y + TILE_SIZE)
            self.direction.x = 0
            self.direction.y = 0
        if self.facing == 'left':
            Attack(self, self.rect.x - TILE_SIZE, self.rect.y)
            self.direction.x = 0
            self.direction.y = 0
        if self.facing == 'right':
            Attack(self, self.rect.x + TILE_SIZE, self.rect.y)
            self.direction.x = 0
            self.direction.y = 0
        
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            
        x_movement = self.direction.x * speed
        y_movement = self.direction.y * speed
        
        self.hitbox.x += x_movement
        self.collide_blocks('x')
        self.hitbox.y += y_movement
        self.collide_blocks('y')
            
        self.rect.centerx = self.hitbox.centerx
        self.rect.centery = self.hitbox.centery

class Player(Character):
    def __init__(self, level, x, y):
        #######################################################################
        ########################## LOGISTICS ##################################
        ####################################################################### 
        ## Inherit from Character class
        super().__init__(level, x, y)
        ## The player should have his own layer
        self._layer = PLAYER_LAYER        
        ## Add to the player group
        self.groups.append(self.level.player_group)
        ## Lowest level group so initialize groups 
        pygame.sprite.Sprite.__init__(self, tuple(self.groups))
        
        #######################################################################
        ########################## STATS ######################################
        #######################################################################
        self.speed = PLAYER_SPEED
        
        #######################################################################
        ########################## ANIMATIONS #################################
        #######################################################################
        self.spritesheet = self.level.character_spritesheet
        ## Where in the spritesheet is the top left corner of the first sprite?
        pixel_x_start = 3
        pixel_y_start = 2
        self.load_animations_directional(pixel_x_start, pixel_y_start)
  
    def update(self):
        #######################################################################
        ####################### CHECK FOR COLLISIONS ##########################
        #######################################################################         
        self.inputs()
        self.move(self.speed)
        self.animate()
           
        self.collide_enemies_character('x')
        self.collide_enemies_character('y')

    def collide_enemies_character(self, direction):  
        ## Check for any collisions with the enemies group
        hits = pygame.sprite.spritecollide(self, self.level.enemies, False)
        ## Do we need to break into x and y? #TODO
        if direction == 'x':
            if hits:
                ## Right now if we collide with an enemy, we die immediately, someday, we will want to add health #TODO
                self.kill()
                self.level.game.playing = False
        if direction == 'y':
            if hits:
                ## Right now if we collide with an enemy, we die immediately, someday, we will want to add health #TODO
                self.kill()
                self.level.game.playing = False
                    
    def inputs(self):
        #######################################################################
        ####################### SINGLE BUTTON PRESSES #########################
        #######################################################################
        for event in self.level.game.event_list:
            if event.type == pygame.KEYDOWN:
                ## Basic attack
                if event.key == pygame.K_SPACE:
                    self.attack()
                        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.direction.x = 0
                    self.keylist.remove('left')
                if event.key == pygame.K_RIGHT:
                    self.direction.x = 0
                    self.keylist.remove('right')
                if event.key == pygame.K_UP:
                    self.direction.y = 0
                    self.keylist.remove('up')
                if event.key == pygame.K_DOWN:
                    self.direction.y = 0
                    self.keylist.remove('down')
                    
        if not self.attacking:
            #######################################################################
            ####################### BUTTONS THAT ARE HELD #########################
            ####################################################################### 
            keys = pygame.key.get_pressed()
            ## Movement
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                if 'left' not in self.keylist:
                    self.keylist.append('left')
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                if 'right' not in self.keylist:
                    self.keylist.append('right')
            if keys[pygame.K_UP]:
                self.direction.y = -1
                if 'up' not in self.keylist:
                    self.keylist.append('up')
            if keys[pygame.K_DOWN]:
                self.direction.y = 1
                if 'down' not in self.keylist:
                    self.keylist.append('down')
                
        if len(self.keylist) > 0:
            self.facing = self.keylist[-1]
            
            
## Purely Parent Class. No loading animations
class Non_Player(Character):
    def __init__(self, level, x, y): 

        #######################################################################
        ########################## LOGISTICS ##################################
        ####################################################################### 
        ## Inherit from Character class
        super().__init__(level, x, y)        
        ## Define which layer this sprite should be drawn in. All non-players should be drawn on the same layer.(I think?)
        self._layer = NON_PLAYER_LAYER
        ## Add to non-player group
        self.groups.append(self.level.non_player)
        
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
        self.move(self.speed)
        self.animate()
        
        #######################################################################
        ####################### CHECK FOR COLLISIONS ##########################
        ####################################################################### 
        ## If the NPC is running into a block, end command early
        if self.collide_blocks('x'):
            self.command_length = 0
            
        ## If the NPC is running into a block, end command early
        if self.collide_blocks('y'):
            self.command_length = 0
            
        
    def npc_brain(self):
        ## Command Initializations
        available_commands = ['wait', 'attack', 'up', 'down', 'left', 'right']
        command_length_min = 60
        command_length_max = 120
        
        if self.attacking:
            self.command_length = 0
        else:
            if self.command_loop < self.command_length:
                self.command_loop += 1
            ## If current command has ended, pick a new command
            else:
                self.command_current = self.command_current[:-1]
                self.command_current.append(random.choice(available_commands))
                self.command_length = random.randint(command_length_min, command_length_max)
                self.command_loop = 0
                
            ### Execute commands                
            if 'attack' in self.command_current:
                self.attack()
                self.command_current.remove('attack')
                
            if 'left' in self.command_current:
                self.direction.x = -1
            elif 'right' in self.command_current:
                self.direction.x = 1
            else:
                self.direction.x = 0
                
            if 'up' in self.command_current:
                self.direction.y = -1
            elif 'down' in self.command_current:
                self.direction.y = 1
            else:
                self.direction.y = 0   
            
            if len(self.command_current) > 0:
                if self.command_current[-1] is 'up' or 'down' or 'left' or 'right':
                    self.facing = self.command_current[-1]
        
class Villager(Non_Player):
    def __init__(self, level, x, y):        
        #######################################################################
        ########################## LOGISTICS ##################################
        ####################################################################### 
        ## Inherit from Character class
        super().__init__(level, x, y)        
        ## Add to villager group 
        self.groups.append(self.level.villagers)
        ## Lowest level group so initialize groups 
        pygame.sprite.Sprite.__init__(self, tuple(self.groups))
        
        #######################################################################
        ########################## STATS ######################################
        #######################################################################        
        self.speed = VILLAGER_SPEED

        #######################################################################
        ########################## ANIMATIONS #################################
        #######################################################################
        self.spritesheet = self.level.character_spritesheet
        pixel_x_start = 3
        pixel_y_start = 2        
        self.load_animations_directional(pixel_x_start, pixel_y_start)