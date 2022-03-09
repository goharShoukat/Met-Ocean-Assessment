#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 16:02:15 2022

@author: goharshoukat

Warning: Dummy data is fed for current and mwp as they are not needed
for the weather window analysis
"""

import pandas as pd
import numpy as np
import os
import glob
from download_cdspy import download_cdspy
from ERA5 import ERA5
import datetime
from netCDF4 import num2date
input_ = pd.read_excel('input.xlsx', sheet_name = 'Download', header=None)
input_ = input_.set_index(0)


if input_.loc['Download Data',1]:
    var = []
    for v in range(1, np.size(input_, axis = 1)+1):
        var.append(input_.loc['Variables', v])
        
    north = input_.loc['North',1]
    west = input_.loc['West',1]
    south = input_.loc['South',1]
    east = input_.loc['East',1]
    output = input_.loc['Download Data Folder', 1]
    start = (input_.loc['Start Year',1])
    end = (input_.loc['End Year',1])
    lat = input_.loc['Required Latitude', 1]
    long = input_.loc['Required Longitude', 1]
    
    if not os.path.isdir(output):
        os.mkdir(output)
        
    download_cdspy(var, start, end, north, west, south, east, output)

if input_.loc['Extract Data', 1]:
    output_data = input_.loc['Extracted Data Folder', 1]
    cds = ERA5(output + '/')
    variables = ['u10', 'v10', 'shww'] #adjust variable for total swh
    cache=cds.load_variable(variables)
    cds.nearest_point(lat, long)
    df = cds.df_generator(variables)
    df['vel'] = np.sqrt(df['u10'] ** 2 + df['v10']**2)
    date = pd.DatetimeIndex(pd.to_datetime(df['Date'].astype(str)))
    year = int(date.year)
    month = int(date.month)
    day = int(date.day)
    hour = int(date.hour)
    #shww needs to be changed
    dummy = np.ones(len(df))
    
    array = np.array((year, month, day, hour, df['vel'], df['shww'], dummy, dummy), dtype=object).T
    if not os.path.isdir(output_data):
        os.mkdir(output_data)
    #adjust datatypes for each output format to limit the file size
    np.savetxt(output_data + '/Wind_Wave.txt', array, delimiter=',', fmt = ['%.0f','%.0f','%.0f','%.0f','%.3f','%.3f','%.0f','%.0f'])
    


WA = pd.read_excel('input.xlsx',  = 'WA', header = None)