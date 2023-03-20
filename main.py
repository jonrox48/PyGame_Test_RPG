# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 09:54:10 2023

@author: j91722
"""

import sys
import pygame
from gui import *
from sprites import *
from settings import *
from characters import *
from enemies import *
from non_collision_blocks import *
from collision_blocks import *
from attacks import *
from levels import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()     
        
        self.font = pygame.font.Font('fonts/ARIAL.TTF', 32)
        self.running = True
        self.playing = False
        
        self.event_list = []
        
        # self.level = Level(self)
        
        self.intro_background = pygame.image.load('img/introbackground.png')
        self.go_background = pygame.image.load('img/gameover.png')

####################################################################
########################## START NEW GAME ##########################
####################################################################
    def new(self):
       self.level = Level(self)
       
####################################################################
##################### DELETE CURRENT GAME ##########################
####################################################################\
    def delete(self):
        del self.level
        
####################################################################
########################## RUNNING THE GAME ########################
####################################################################
    def run(self):
        while self.playing:
            self.screen.fill(BLACK)                    
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
    

####################################################################
########################## DIFFERENT SCREENS #######################
####################################################################

    def intro_screen(self):
        intro = True
        
        title = self.font.render('Awesome Game', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)
        
        play_button = Button(10, 50, 100, 50, WHITE, BLACK, "Play", 32)
        
        while intro:
            self.event_list = pygame.event.get()
            for event in self.event_list:
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
                    # pygame.quit()
                    # sys.exit()
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                self.playing = True
                self.new()
                
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
            
            
    def game_over(self):
        text = self.font.render('Game Over', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        
        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Restart', 32)
        
        loop = True
        while loop:
            self.event_list = pygame.event.get()
            for event in self.event_list:
                if event.type == pygame.QUIT:
                    self.running = False
                    loop = False
                    
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.delete()
                loop = False
                
            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
            
                    
####################################################################
########################## BOILER PLATE ############################
####################################################################
if __name__ == '__main__':
    g = Game()
    while g.running:
        g.intro_screen()
        # g.new()
        while g.playing:
            g.run()
        g.game_over()
    pygame.quit()
    sys.exit()


