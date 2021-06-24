#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 15:45:32 2021

@author: goharshoukat

ERA5. This code defines ERA5 as a class which for specific coordinates,
creates time series data in different format. 
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
    def __init__(self, directory):
        #inputs
        #directory : string : provide path of the directory housing the data files
        self.directory = directory
        
    
    def bounded_region(self, lon1, lat1, lon2, lat2):
        #This function is used to provide information about a bounded region
        #Needs to be run only once. This does not load the data. 
        #it only finds the bounded region
        #a rectangular shape is must. it can not work on arbitraty quadratic shapes
        #lon1 : floating point : 0 < lon < 359.5 longitudnal value of the first vertex
        #lon2 : floating point : longitudnal value of the second vertex
        #Ensure lon1 < lon2
        #lat1 : floating point : -90 < lat < 90 latitudnal value of the first vertex
        #lat2 : floating point : latitudnal value of the second vertex
        #Ensure lat1 < lat2
        #convert these points to the nearest points from the grid
        #output : dict object : contains the indices and the corresponding values
        self.files = os.listdir(self.directory)
        self.files = np.sort(self.files)[1:] #there is an additional file by the name ./dstore which needs to be removed. 
        #out_dir = 'ERA5 Formatted Files/'
        
        #this function loads the first file to extract the longitude and latitude information
        f = Dataset(self.directory + self.files[0], 'r') #common mistake is to not provide full path of the dataset

        #unpack all the variables
        self.lon = f.variables['longitude'][:]
        self.lat = f.variables['latitude'][:]
        
        self.vertex1 = self.nearest_point(self.lon, self.lat, lon1, lat1)
        self.vertex2 = self.nearest_point(self.lon, self.lat, lon2, lat2)
        
    def nearest_point(self, lon_file, lat_file, lon_user, lat_user):
        #function to calculate the nearest data points
        #lon_file : Array of float64 : Array passed on from the netcdf file
        #lat_file : Array of float64 : Array passed on from the netcdf file
        #lon_user : float64 : coordinate passed onto the function by the user for which closest neighour is required
        #lat_user : float64 : coordinate passed onto the function by the user for which closest neighour is required
        
        #Output
        #Dictionary data type with the indexes and the corresponding values 
        #of longitude and latitude from the original file
        idx_lon = np.abs(lon_file - lon_user).argmin()
        idx_lat = np.abs(lat_file - lon_user).argmin()
        output_dict = {'longitude index': idx_lon, 'latitude index': idx_lat, \
                       'longitude' : lon_file[idx_lon], 'latitude' : lat_file[idx_lat]}
        return output_dict
    
    def check_availability(self):
        #function to evaluate percentage of the times the data point has 
        #availability of data
        pass
    
    def load_coordinate_data(self, lon_user, lat_user, variable, output_directory, file_type = 'Joint'):
        #Function to extract information about a single point
        
        #input
        #lon_user : float64 : longitudnal value for which information is required
        #lat_user : float64 : latitudnal value for which information is required
        #variable : string : specify exactly the property to study. by default, 
        #all variables can be obtained but for now, we will limit the functionality to include only one variable specified by the user
        #output_directory : string : Provide directory to save the data file
        #file_type : string : 
        #if exact grid points for which data is available not entered, function 
        #finds the nearest data point. 
        nearest_grid_point = self.near_point(self.lon, self.lat, lon_user, lat_user)
        
        if not lon_user in self.lon and lat_user in self.lat:
            print ('The entered longitudnal coordinate does not have an associated value, value from the closest data point will be used.')
            print('The nearest point to your query is: Longitude: ' + str(nearest_grid_point['longitude']) + ', Latitude - ' + str(nearest_grid_point['latitude']))
        
        #if else structure to support code in the for loop for joint data frame output
        if file_type == 'Joint':
            joint_df = pd.DataFrame()
            
        for file in self.files:
            f = Dataset(self.directory + file, 'r')
            #unpack all variables of interest
            time = f.variables['time']
            dtime = num2date(time[:], time.units) #hours since 1900-1-1 00:00:00"
            #unpack variable of interest into var
            var = f.variables[variable][:]
            #slice the var to extract the data for the data point only
            var_point = var[:, nearest_grid_point['lat index'], nearest_grid_point['lon index']]
            
            #create dataframe with the var information along with the lon/lat and date
            df = pd.DataFrame({'Date' : np.array(dtime[:]), 'Longitude' : nearest_grid_point['longitude'], \
                               'Latitude' : nearest_grid_point['latitude'],\
                                   variable : var_point})
                
            #write the output to csv files
            if file_type == 'Separate':
                df.to_csv(output_directory + file[:-3] + variable + '.csv')
            
                #concat the dataframe to produce one file
            else:
                joint_df = pd.concat([joint_df, df], ignore_index=True)
                
        if file_type == 'Joint':
            joint_df.to_csv(output_directory + 'Joint ' + variable + '.csv')
                
   
    
   
    def load_bounded_region(self, output_directory, file_type = 'Joint'):

        #this function will load the data files and extract the values for the bounded region
        #inputs
        #output_directory : string : path where the bounded region files will be saved
        #file_type : string : 'Joint' or 'Separate : Joint creates one single data file, Separate creates one output per input file
        #create folder to write time series
        if not os.path.isdir(output_directory):
            os.mkdir(output_directory)

        #if else structure to support code in the for loop for joint data frame output
        if file_type == 'Joint':
            joint_df_swh = pd.DataFrame()
            joint_df_mwp = pd.DataFrame()
            joint_df_mwd = pd.DataFrame()
            
        for file in self.files:
            f = Dataset(self.directory + self.file, 'r') #common mistake is to not provide full path of the dataset
            #unpac variables of intereset
            time = f.variables['time']
            dtime = num2date(time[:], time.units) #hours since 1900-1-1 00:00:00"
            swh = f.variables['swh'][:]; swh_units = f.variables['swh'].units
            mwd = np.deg2rad(f.variables['mwd'][:]); mwd_units = f.variables['mwd'].units #units now are radians for mwd after conversion to raidans
            mwp = f.variables['mwp'][:]; mwp_units = f.variables['mwp'].units
            
            #extract the bounded region
            #+1 is incldued in the slicing because the end point is not included. 
            #by adding 1 to the end point, the last coordinate data is also included
            lon_reg = self.lon[self.vertex1['lon index']: self.vertex2['lon index']+1]
            lat_reg = self.lat[self.vertex1['lat index']: self.vertex2['lat index']+1]
            swh_reg = swh[:, self.vertex1['lat index'] : self.vertex2['lat index'] + 1, self.vertex1['lon index'] : self.vertex2['lon index']+1]
            mwd_reg = mwd[:, self.vertex1['lat index'] : self.vertex2['lat index'] + 1, self.vertex1['lon index'] : self.vertex2['lon index']+1]
            mwp_reg = mwp[:, self.vertex1['lat index'] : self.vertex2['lat index'] + 1, self.vertex1['lon index'] : self.vertex2['lon index']+1]
            
            #collapse the 3D arrays into 2D arrays
            #the rows represent the variation in time
            #the progression in columns represents the flattened array of lat and long
            #transpose the arrays to fit into the dataframe in the next frame
            #convert to dataframe after transposing so that the two dataframes can be merged
            swh_updated = pd.DataFrame(np.reshape(swh_reg, (-1,np.shape(swh_reg)[1] * np.shape(swh_reg)[2])).T)
            mwd_updated = pd.DataFrame(np.reshape(mwd_reg, (-1,np.shape(mwd_reg)[1] * np.shape(mwd_reg)[2])).T)
            mwp_updated = pd.DataFrame(np.reshape(mwp_reg, (-1,np.shape(mwp_reg)[1] * np.shape(mwp_reg)[2])).T)
            
            #first column will be longitude
            #second column will be latitude
            LON, LAT = np.meshgrid(lon_reg, lat_reg)
            LON = LON.flatten(); LAT = LAT.flatten()
            columns = np.array(['longitude', 'latitude'])
            
            
            #create an array with the multiple columns representing the time steps
            #flatten the array with column major
            swh_arr = np.array(swh_updated).flatten('F')
            mwd_arr = np.array(mwd_updated).flatten('F')
            mwp_arr = np.array(mwp_updated).flatten('F')
        
            #declare a dataframe with the long and lat repeated for the entire length
                #of the dtime.
            df_swh = pd.DataFrame(columns = columns)
            df_swh = pd.DataFrame({'Date' : None, 'longitude' : np.tile(LON, len(dtime)), \
                                   'latitude' : np.tile(LAT, len(dtime))})
            
           
            df_mwp = pd.DataFrame(columns = columns)
            df_mwp = pd.DataFrame({'Date' : None, 'longitude' : np.tile(LON, len(dtime)), \
                                   'latitude' : np.tile(LAT, len(dtime))})
           
            df_mwd = pd.DataFrame(columns = columns)
            df_mwd = pd.DataFrame({'Date' : None, 'longitude' : np.tile(LON, len(dtime)), \
                                   'latitude' : np.tile(LAT, len(dtime))})
           
                #declare a dtime dataframe with repeated values for the length of the long and lat
            #dt = (pd.DataFrame({'Date' : dtime[:]}))

            #following code is to reproduce
            x = np.array(dtime[:])
            x = np.repeat(x, len(lon_reg)*len(lat_reg))
            df_swh['Date'] = x; df_mwd['Date'] = x; df_mwp['Date'] = x; 
            df_swh['swh'] = swh_arr
            df_mwd['mwd'] = mwd_arr
            df_mwp['mwp'] = mwp_arr
                
            
            if file_type == 'Separate':
                df_swh.to_csv(output_directory + file[:-3] +'_swh.csv')
                df_mwp.to_csv(output_directory + file[:-3] +'_mwp.csv')
                df_mwd.to_csv(output_directory + file[:-3] +'_mwd.csv')

            elif file_type == 'Joint':
                joint_df_swh = pd.concat([joint_df_swh, df_swh], ignore_index=True)
                joint_df_mwp = pd.concat([joint_df_mwp, df_mwp], ignore_index=True)
                joint_df_mwd = pd.concat([joint_df_mwd, df_mwd], ignore_index=True)
                
        if file_type == 'Joint':
            joint_df_swh.to_csv(output_directory + 'Joint_swh.csv')
            joint_df_mwd.to_csv(output_directory + 'Joint_mwd.csv')
            joint_df_mwp.to_csv(output_directory + 'Joint_mwp.csv')
            
    
'''        
        

class ERA5():
    def __init__(self, directory, output = 'Joint', N = False, Single_file_name = False, lon1 = False, lon2 = False, lat1 = False, lat2 = False):
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
        #signle file name : string : if the user choses to study just one file, N = 1 and the file name needs to be provided.
        self.directory = directory
        self.output = output
        self.lon1 = lon1
        self.lon2 = lon2
        self.lat1 = lat1
        self.lat2 = lat2
        self.N = N
        self.Single_file_name = Single_file_name


    def load(self):
        files = os.listdir(self.directory)
        files = np.sort(files)[1:]
        out_dir = 'ERA5 Formatted Files/'

        #create folder to write time series
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

                del swh_arr, mwd_arr, mwp_arr #delete variables to avoid memory overload



                if self.output == 'Separate':
                    self.df.to_csv(out_dir + file[:-3] +'.csv')

                elif self.output == 'Joint':
                    joint_df = pd.concat([joint_df, self.df], ignore_index=True)

                else:
                    pass

        if self.output == 'Joint':
            joint_df.to_csv(out_dir + 'Joint.csv')

        elif self.N == 1:
            pass

        else:
            print('Error: Please provide either directory for all files or type N = 1 followed by file name in the direcctory')

'''