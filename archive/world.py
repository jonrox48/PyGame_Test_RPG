# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 13:23:20 2023

@author: j91722
"""
import sys
import math
import pandas as pd
from tile import Parent_Tile
import numpy as np
import pdb
    
class World():
    def __init__(self):
        # Size
        self.size = 16 #tiles
        
        # Environment
        self.temperature = -999 #fahrenheit
        self.humidity = -999 #50%
        self.minutes_per_day = 1440
        self.minutes_per_year = 525600
        self.yearly_temperature_offset = 50 #Mean of 50 degrees F
        
        # Time
        self.year = 2022
        self.time = 174720 ###(8:00AM) May 1st, (day 121, minute 480)
        
        ## Initialize temperature and humidity
        self.calc_world_temperature()
        self.calc_world_humidity() 
        
        ## Track tiles and changes at the WORLD level
        ## Initialize tile grid
        self.tile_grid = []
        for x in range(self.size):
            temp_vector = []
            for y in range(self.size):
                temp_tile = Parent_Tile(x, y, self.temperature, self.humidity)
                temp_vector.append(temp_tile)
                del temp_tile
            self.tile_grid.append(temp_vector)
            del temp_vector
        del x
        del y
        
        ## Initialize the change tracker grids
        self.change_grid = {}
        self.tile_tracked_parameter_names = ["temperature", "humidity"]
        
        for parameter in self.tile_tracked_parameter_names:
            temp_grid = []
            for x in range(self.size):
                temp_vector = []
                for y in range(self.size):
                    temp_vector.append(0.0)
                temp_grid.append(temp_vector)
                del temp_vector
            self.change_grid[parameter] = temp_grid
            del temp_grid
            
        
    def calc_world_temperature(self):
        ## Yearly Constants
        yearly_period_offset = (2*math.pi)/3.6
        yearly_amplitude_scaling = 30
        
        ## Daily Constants
        daily_period_offset = (2*math.pi)/3.6
        daily_amplitude_scaling = 10     
        
        ## Calculations
        daily_vertical_offset = (yearly_amplitude_scaling * math.sin((2*math.pi) * ((self.time / self.minutes_per_year) + yearly_period_offset))) + self.yearly_temperature_offset
        time_of_day = self.time % self.minutes_per_day
        temperature = ((math.sin((math.pi * 2) * ((time_of_day / self.minutes_per_day) + daily_period_offset))) * daily_amplitude_scaling) + daily_vertical_offset
        self.temperature = temperature
        
    def calc_world_humidity(self):
        ## Yearly Constants
        yearly_period_offset = (2*math.pi)/-3.2
        yearly_vertical_offset = 45
        yearly_amplitude_scaling = 15
        
        ## Calculations
        humidity = (yearly_amplitude_scaling * math.sin((2*math.pi) * ((self.time / self.minutes_per_year) + yearly_period_offset))) + yearly_vertical_offset
        self.humidity = humidity



world = World()
pdb.set_trace()


