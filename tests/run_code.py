#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 18:40:57 2021

@author: goharshoukat
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from netCDF4 import Dataset, num2date
import time
import sys
sys.path.append('/Users/goharshoukat/Documents/GitHub/Met-Ocean-Assessment/src/')
from ERA5 import ERA5
def run_script():
    directory = input('Enter the directory of the data folder: \n')
    #directory = '/Users/goharshoukat/Documents/GitHub/Met-Ocean-Assessment/some_data/'
    #files = np.sort(os.listdir(directory)[1:])
    x = ERA5(directory)
    k = list(x.f.variables.keys())
    print('List of variables stored within the data files is: {} \n'.format(k[:]))
    time.sleep(1)
    variable = input('Which parameter would you like to analyse: \n')

    cache= x.load_variable(variable)
    print('The range of Latitudnal values is: {} < Lat < {} \n'.format(x.lat[-1], x.lat[0]))
    print('The range of Longitudnal values is: {} < Lon < {} \n'.format(x.lon[0], x.lon[-1]))
    lat = float(input('Enter the Latitude: \n'))
    lon = float(input('Enter the Longitude: \n'))
    #lon = 45
    #lat = 80
    nearest = x.nearest_point(lat, lon)

    df = x.extract_coordinate_data(nearest['latitude index'], nearest['longitude index'])
    if_save = input('Do you wish to save the data for this coordinate? \n')

    if if_save == 'yes':
        out_direc = input('Please provide directory to save the data \n')
        x.write_coordinate_data(out_direc)
        print('Successfully Saved')

while True:
    run_script()
