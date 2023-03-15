# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 15:56:57 2023

@author: j91722
"""

import numpy as np
import math

class Parent_Tile():
    def __init__(self, x, y, world_temperature, world_humidity):
        self.size = 32 #pixels
        self.nominal_humidity = 0.5
        self.x_coordinate = 0
        self.y_coordinate = 0
        ## sprite location
        self.sprite = []
        
        
        self.temperature = 70 #fahrenheit
        self.relative_humidity = 0.5 #50%
        self.ground_moisture = 1.0
        self.time_since_last_watering = 0.0
        
        ## ## placeholder to be replaced by specific tile
        self.temperature_drying_domain =  [] #Celsius
        self.temperature_drying_scalars = [] #Scalar
        
    def _iterate_tile(self, watered_bool):
        ## User Changes:
        if watered_bool:
            self.ground_moisture = 1.0
                
        #### ENVIRONMENT CAUSED CHANGES
        ## DRYING
        current_temperature_drying_scalars = np.interp(self.temperature, self.temperature_drying_domain, self.temperature_drying_scalars)
        
        if self.ground_moisture > 0.005:
            self.time_since_last_watering += 1 #increment time since watering
            ## Calculate Percent drying this time step
            k = current_temperature_drying_scalars/(self.nominal_humidity + self.relative_humidity) 
            moisture_change = k * math.exp(k*self.time_since_last_watering)
            self.ground_moisture = self.ground_moisture + moisture_change
        elif self.ground_moisture > 0:
            ground_moisture = 0.0
        elif ground_moisture == 0:
            pass
        
##########################################
############ CROP TILES ##################
##########################################

class Crop_Tile(Parent_Tile):
    def __init__(self):
        ## Growth amount (min 0.0, max 100.0)
        self.growth = 0.0
        self.baseline_growth_rate = 1.0 ## placeholder to be replaced by specific crop
        
        ## Growth Rate Data
        self.growth_rate_temperature_domain =  [4.44444, 10.0, 16.94444, 23.8889, 32.22] #Celsius
        self.growth_rate_temperature_scalars = [    0.0,  0.9,      1.0,     0.9,   0.0] #Scalar
        
        self.temperature_drying_domain =  [    0.0,    20.0,   40.0,    60.0,  80.0] #Celsius
        self.temperature_drying_scalars = [-0.0009, -0.0013, -0.002, -0.0035, -0.01] #Scalar
        
        
    def _iterate_crop(self, fertalized_bool):        
        # User Changes:
        
        # Environmental Changes
        current_growth_rate_temperature_scalar = np.interp(self.temperature, self.growth_rate_temperature_domain, self.growth_rate_temperature_scalars)
        
class Grass_Tile(Crop_Tile):
    def __init__(self):
        
        self.baseline_growth_rate = 1.0
        
        ## Growth Rate Data
        self.growth_rate_temperature_domain =  [4.44444, 10.0, 16.94444, 23.8889, 32.22] #Celsius
        self.growth_rate_temperature_scalars = [    0.0,  0.9,      1.0,     0.9,   0.0] #Scalar

        
        
        