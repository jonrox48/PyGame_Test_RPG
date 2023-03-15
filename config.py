# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 09:53:57 2023

@author: j91722
"""
## Game variables
WIN_WIDTH = 640
WIN_HEIGHT = 480
TILE_SIZE = 32
FPS = 60


## Layer order
GROUND_LAYER = 1
BLOCK_LAYER = 2
ENEMY_LAYER =3
PLAYER_LAYER = 4

## Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

## Speeds
PLAYER_SPEED = 3
ENEMY_SPEED = 2


tilemap = [
    'BBBBBBBBBBBBBBBBBBBB',
    'B...E..............B',
    'B..................B',
    'B.....B............B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B........P.........B',
    'B..................B',
    'B.......BBB........B',
    'B..................B',
    'B..................B',
    'B...............E..B',
    'B..................B',
    'BBBBBBBBBBBBBBBBBBBB'
    ]