#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 15:45:32 2021

@author: goharshoukat
"""

import os
import matplotlib.pyplot as plt
from netCDF4 import Dataset, num2date
import numpy as np
import cartopy.crs as ccrs
from datetime import datetime, timedelta  #libraries required to convert the time column of netcdf4
import pandas as pd
from pathlib import Path

class ERA5():
    def __init__(self, directory, output = 'Joint', N = False, lon1 = False, lon2 = False, lat1 = False, lat2 = False):
        #inputs
        #directory : provide path of the directory housing the data files
        #output : string : user choses between joint and seperate
        #if seperate is chosen, each file's time series is saved seperately
        #if joint is chosen, the entire series from all the years is combined into one
        #N : integer : user defines if only one particular file has to be used or all of them. 
        #lon1 : floating point : longitudnal value of the first vertex 
        #lon2 : floating point : longitudnal value of the second vertex
        #lat1 : floating point : latitudnal value of the first vertex
        #lat2 : floating point : latitudnal value of the second vertx
    
        self.directory = directory
        self.output = output 
        self.lon1 = lon1
        self.lon2 = lon2
        self.lat1 = lat1
        self.lat2 = lat2
        self.N = N
        
        
    def load(self):
        files = os.listdir(self.directory)
        files = np.sort(files)[1:]
        out_dir = 'ERA5 Formatted Files/'
        if not os.path.isdir(out_dir):
            os.mkdir(out_dir)
        
        #if else structure to support code in the for loop for joint data frame output
        if self.output == 'Joint':
            joint_df = pd.DataFrame()

        #the following sequence is initiated if the user wants to study all the 
        #files in the directory
        
        if self.N == False:
            for file in files:
                #load each file one by one
                f = Dataset(self.directory + file, 'r') #common mistake is to not provide full path of the dataset
                            
                #unpack all the variables
                lon = f.variables['longitude'][:]
                lat = f.variables['latitude'][:]
                time = f.variables['time']
                swh = f.variables['swh'][:]; swh_units = f.variables['swh'].units
                #u10 = f.variables['u10'][:]; u10_units = f.variables['u10'].units
                #v10 = f.variables['v10'][:]; v10_units = f.variables['v10'].units
                mwd = np.deg2rad(f.variables['mwd'][:]); mwd_units = f.variables['mwd'].units #units now are radians for mwd after conversion to raidans
                mwp = f.variables['mwp'][:]; mwp_units = f.variables['mwp'].units
                dtime = num2date(time[:], time.units) #hours since 1900-1-1 00:00:00"
                
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
                
                del swh, mwd, mwp #delete variables not required furhter. this will save memory consumption
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
                
                del swh_updated, mwd_updated, mwp_updated    #varilables not required further. step to avoid RAM overload
                #declare a dataframe with the long and lat repeated for the entire length 
                #of the dtime. 
                self.df = pd.DataFrame(columns = columns)
                self.df = pd.DataFrame({'Date' : None, 'longitude' : np.tile(LON, len(dtime)), \
                                   'latitude' : np.tile(LAT, len(dtime))})
                #declare a dtime dataframe with repeated values for the length of the long and lat
                #dt = (pd.DataFrame({'Date' : dtime[:]}))
                
                #following code is to reproduce 
                x = np.array(dtime[:])
                x = np.repeat(x, len(lon)*len(lat))
                self.df['Date'] = x
                self.df['swh'] = swh_arr
                self.df['mwd'] = mwd_arr
                self.df['mwp'] = mwp_arr
                #df['u10'] = u10_arr
                #df['v10'] = v10_arr
                df = self.df
                del swh_arr, mwd_arr, mwp_arr #delete variables to avoid memory overload
               
                
                
                if self.output == 'Separate':
                    self.df.to_csv(out_dir + file[:-3] +'.csv')
                    
                elif self.output == 'Joint':
                    joint_df = pd.concat([joint_df, self.df], ignore_index=True)
                   
                else:
                    pass
            
        if self.output == 'Joint':
            joint_df.to_csv(out_dir + 'Joint.csv')
                

                    
            
        else:
            pass
        

                
                