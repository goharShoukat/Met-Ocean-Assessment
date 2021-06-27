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
from src.ERA5 import ERA5
from netCDF4 import Dataset, num2date

directory = input('Enter the directory of the data folder: ')
directory = '/Users/goharshoukat/Documents/GitHub/Met-Ocean-Assessment/some_data/'
files = np.sort(os.listdir(directory)[1:])
x = ERA5(directory)
cache= x.load_variable('swh')
#print('The range of Latitudnal values is: {} < Lat < {}'.format(x.lat[0], x.lat[-1]))
#print('The range of Longitudnal values is: {} < Lon < {}'.format(x.lon[0], x.lon[-1]))
#lat = float(input('Enter the Latitude: '))
#lon = float(input('Enter the Longitude: '))

lon = 8.25
lat = 51.5
nearest = x.nearest_point(lat, lon)
k = list(x.f.variables.keys())
print('List of variables stored within the data files is: {}'.format(k[:]))
variable = 'swh'
df = x.extract_coordinate_data(nearest['latitude index'], nearest['longitude index'])
#x.write_coordinate_data(directory + 'results/')




