#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 23:49:37 2021

@author: goharshoukat
"""
import os
import matplotlib.pyplot as plt
from netCDF4 import Dataset, num2date
import numpy as np
import cartopy.crs as ccrs
from datetime import datetime, timedelta #libraries required to convert the time column of netcdf4
import pandas as pd
#ERA 5 data sent by Mazhar
f = Dataset('tests/some_data/2015_1.nc')
#f = Dataset('adaptor.mars.internal-1624043819.2189372-14651-11-647c0d64-af34-434a-986b-20e5a2b94df9.nc', mode = 'r')
f.variables.keys() #function to check all the column headers

#unpack all the variables
lon = f.variables['longitude'][:]
lat = f.variables['latitude'][:]
time = f.variables['time']
u10 = np.array(f.variables['u10'][:]); swh_units = f.variables['swh'].units


#u10 = f.variables['u10'][:]; u10_units = f.variables['u10'].units
#v10 = f.variables['v10'][:]; v10_units = f.variables['v10'].units
mwd = np.deg2rad(f.variables['mwd'][:]); mwd_units = f.variables['mwd'].units #units now are radians for mwd after conversion to raidans
mwp = f.variables['mwp'][:]; mwp_units = f.variables['mwp'].units
dtime = num2date(time[:], time.units) #hours since 1900-1-1 00:00:00"


df_swh =  pd.DataFrame(u10[0,:,:])
df_swh= df_swh.set_index(lat[:])
df_swh.columns = lon[:]




#collapse the 3D arrays into 2D arrays
#the rows represent the variation in time
#the progression in columns represents the flattened array of lat and long
#transpose the arrays to fit into the dataframe in the next frame
#convert to dataframe after transposing so that the two dataframes can be merged
#u10_updated = pd.DataFrame(np.reshape(u10, (-1,np.shape(u10)[1] * np.shape(u10)[2])).T)
#v10_updated = pd.DataFrame(np.reshape(v10, (-1,np.shape(v10)[1] * np.shape(v10)[2])).T)
swh_updated = pd.DataFrame(np.reshape(swh, (-1,np.shape(swh)[1] * np.shape(swh)[2])).T)
mwd_updated = pd.DataFrame(np.reshape(mwd, (-1,np.shape(mwd)[1] * np.shape(mwd)[2])).T)
mwp_updated = pd.DataFrame(np.reshape(mwp, (-1,np.shape(mwp)[1] * np.shape(mwp)[2])).T)

#first column will be longitude
#second column will be latitude
#then there will be another 139 column for each hour
#total of 141 columns are required.
#total of 28 rows are needed for this data set. 7 longitude and 4 latitude values
LON, LAT = np.meshgrid(lon, lat)
LON = LON.flatten(); LAT = LAT.flatten()
columns = np.array(['longitude', 'latitude'])

#create an array with the multiple columns representing the time steps
#flatten the array with column major
swh_arr = np.array(swh_updated).flatten('F')
#u10_arr = np.array(u10_updated).flatten('F')
#v10_arr = np.array(v10_updated).flatten('F')
mwd_arr = np.array(mwd_updated).flatten('F')
mwp_arr = np.array(mwp_updated).flatten('F')


#declare a dataframe with the long and lat repeated for the entire length 
#of the dtime. 
df = pd.DataFrame(columns = columns)
df = pd.DataFrame({'Date' : None, 'longitude' : np.tile(LON, len(dtime)), \
                   'latitude' : np.tile(LAT, len(dtime))})
#declare a dtime dataframe with repeated values for the length of the long and lat
#dt = (pd.DataFrame({'Date' : dtime[:]}))

#following code is to reproduce 
x = np.array(dtime[:])
x = np.repeat(x, len(lon)*len(lat))
df['Date'] = x
df['swh'] = swh_arr
df['mwd'] = mwd_arr
df['mwp'] = mwp_arr
#df['u10'] = u10_arr
#df['v10'] = v10_arr

#flatten the dataframes for 
#https://earth-env-data-science.github.io/lectures/mapping_cartopy.html
#declare ax as an instance of the ccrs.platecarree class
#creates an empty canvas bounded within a figure. it is a flat figure
central_lon, central_lat = -10, 53
extent = [-4, 1, 40, 45]
ax = plt.axes(projection=ccrs.Orthographic())
ax.set_extent(extent)
ax.coastlines(resolution = '10m') #creates land boundraies
ax.gridlines()
#plt.contourf(f.variables['longitude'][:], f.variables['latitude'][:],f.variables['swh'][0, :, :], transform=ccrs.PlateCarree())
plt.contourf(lon, lat, f.variables['swh'][0, :, :], transform=ccrs.PlateCarree())

#remember to transform data to the correct projection before plotting

'''

path = 'Data/'
files = os.listdir(path)
files = np.sort(files)
f = (Dataset(path + files[78]))

#unpack all the variables
lon = f.variables['longitude'][:]
lat = f.variables['latitude'][:]
time = f.variables['time']
swh = f.variables['swh'][:]; swh_units = f.variables['swh'].units
u10 = f.variables['u10'][:]; u10_units = f.variables['u10'].units
v10 = f.variables['v10'][:]; v10_units = f.variables['v10'].units
mwd = np.deg2rad(f.variables['mwd'][:]); mwd_units = f.variables['mwd'].units #units now are radians for mwd after conversion to raidans
mwp = f.variables['mwp'][:]; mwp_units = f.variables['mwp'].units
dtime = num2date(time[:], time.units) #hours since 1900-1-1 00:00:00"

u10_updated = pd.DataFrame(np.reshape(u10, (-1,np.shape(u10)[1] * np.shape(u10)[2])).T)
v10_updated = pd.DataFrame(np.reshape(v10, (-1,np.shape(v10)[1] * np.shape(v10)[2])).T)
swh_updated = pd.DataFrame(np.reshape(swh, (-1,np.shape(swh)[1] * np.shape(swh)[2])).T)
mwd_updated = pd.DataFrame(np.reshape(mwd, (-1,np.shape(mwd)[1] * np.shape(mwd)[2])).T)
mwp_updated = pd.DataFrame(np.reshape(mwp, (-1,np.shape(mwp)[1] * np.shape(mwp)[2])).T)
df = pd.DataFrame()

ax = plt.axes(projection=ccrs.Orthographic())
#ax.set_extent(extent)
ax.coastlines(resolution = '10m') #creates land boundraies
ax.gridlines()
plt.contourf(lon, lat, u10[100,:,:], transform=ccrs.Orthographic())

'''