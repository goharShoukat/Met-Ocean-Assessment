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

directory = '/Users/goharshoukat/Documents/GitHub/Met-Ocean-Assessment/some_data/'
files = np.sort(os.listdir(directory)[1:])
x = ERA5(directory)
cache = x.load_files('swh')
lon = -8.25
lat = 51.5
nearest = x.nearest_point(lat, lon)
variable = 'swh'
df = x.extract_coordinate_data()
x.write_coordinate_data(directory + 'results/')
