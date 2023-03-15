# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 14:44:07 2023

@author: j91722
"""

import sys
import math
from matplotlib import pyplot
import pandas as pd
import pdb


def scatter_plot_1d(x,vals,title):
    color_keys = ['b','g','r','c','m','y','k','w']
    if isinstance(title, str) == False:
        title = str(title)
    if isinstance(title, str) == False:
        message = "'title' could not be made a string. Default title will be given."
        print(message)
        title = "Default"
    pyplot.title(title)
    for ind, val_vec in enumerate(vals):    
        pyplot.scatter(x, val_vec,s=1,c=color_keys[ind],label=str(ind))
    pyplot.colorbar()
    #pyplot.savefig(title + ".png")        
    pyplot.show()


number_of_minutes = 6000
nominal_humidity = 0.5
current_relative_humidity = 0

test_scalars = [-0.0009, -0.0013, -0.002, -0.0035, -0.01]

data_array = []
for scalar in test_scalars:
    k = scalar/(nominal_humidity + current_relative_humidity)
    
    temp_vector = []
    for time in range(number_of_minutes):
        temp_velocity = k * math.exp(k*time) # matches 40 degrees celcius and 20% relative humidity
        temp_vector.append(temp_velocity)
        del temp_velocity
    data_array.append(temp_vector)
    del temp_vector
    


scatter_plot_1d(range(number_of_minutes), data_array, "Moisture ratio")

