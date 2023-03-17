# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 15:40:38 2023

@author: Huge Mstr
"""

import pygame

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
