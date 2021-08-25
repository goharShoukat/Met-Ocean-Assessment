#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 22:16:41 2021

@author: goharshoukat

Script to plot the region covered by the data

"""


import os
import matplotlib.pyplot as plt
from netCDF4 import Dataset, num2date
import numpy as np
import cartopy.crs as ccrs
from datetime import datetime, timedelta  #libraries required to convert the time column of netcdf4
import pandas as pd
f = Dataset('adaptor.mars.internal-1624043819.2189372-14651-11-647c0d64-af34-434a-986b-20e5a2b94df9.nc')
#f = Dataset('adaptor.mars.internal-1624043819.2189372-14651-11-647c0d64-af34-434a-986b-20e5a2b94df9.nc', mode = 'r')
f.variables.keys() #function to check all the column headers

#unpack all the variables
lon = f.variables['longitude'][:]
lat = f.variables['latitude'][:]
time = f.variables['time']
swh = np.array(f.variables['swh'][:]); swh_units = f.variables['swh'].units




#flatten the dataframes for 
#https://earth-env-data-science.github.io/lectures/mapping_cartopy.html
#declare ax as an instance of the ccrs.platecarree class
#creates an empty canvas bounded within a figure. it is a flat figure
#central_lon, central_lat = -10, 53
#extent = [-4, 1, 40, 45]
ax = plt.axes(projection=ccrs.Orthographic())
#ax.set_extent(extent)
ax.coastlines(resolution = '10m') #creates land boundraies
ax.gridlines()
#plt.contourf(f.variables['longitude'][:], f.variables['latitude'][:],f.variables['swh'][0, :, :], transform=ccrs.PlateCarree())
plt.contourf(lon, lat, f.variables['swh'][0, :, :], transform=ccrs.Orthographic())

