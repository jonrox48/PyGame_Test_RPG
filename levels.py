# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 19:45:24 2023

@author: Huge Mstr
"""

import sys
import pygame
from gui import *
from sprites import Spritesheet
from settings import *
from characters import *
from enemies import *
from non_collision_blocks import *
from collision_blocks import *
from attacks import *

class Level():
    def __init__(self, game):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        ## All
        self.game = game
        self.all_sprites = YSortCameraGroup()
        ## High level groups
        self.characters = pygame.sprite.LayeredUpdates()
        self.player_group = pygame.sprite.LayeredUpdates()
        self.non_player = pygame.sprite.LayeredUpdates()        
        ## Friendlies
        self.villagers = pygame.sprite.LayeredUpdates()
        ## Enemies
        self.enemies = pygame.sprite.LayeredUpdates()
        self.zombies = pygame.sprite.LayeredUpdates()
        ## Terrain Indestructable
        self.collision_blocks = pygame.sprite.LayeredUpdates()
        self.non_collision_blocks = pygame.sprite.LayeredUpdates() 
        ## Terrain Destructable
        ## Attacks
        self.attacks = pygame.sprite.LayeredUpdates()
        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.non_player_spritesheet = Spritesheet('img/enemy.png')
        self.attack_spritesheet = Spritesheet('img/attack.png')
        
        self.createTilemap()
        
    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Grass(self, j, i)
                if column == "B":
                    Rock(self, j, i)
                elif column == "E":
                    pass
                    Zombie(self, j, i)
                elif column == "N":
                    pass
                    Villager(self, j, i)
                elif column == "P":
                    pass
                    self.player = Player(self, j, i)

    def run(self):
        self.update()
        self.draw()
 

        
    def update(self):
        self.game.event_list = pygame.event.get()
        for ind, event in enumerate(self.game.event_list):
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.all_sprites.update()
        
    def draw(self):
        # self.display_surface.fill(BLACK)
        self.all_sprites.custom_draw(self.player)
        # self.clock.tick(FPS)
        pygame.display.update()
        
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        