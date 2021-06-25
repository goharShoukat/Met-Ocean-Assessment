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
from haversine import haversine

class ERA5():
    def __init__(self, directory):
        #inputs
        #directory : string : provide path of the directory housing the data files
        self.directory = directory
        
        
    def load_files(self, variable):
        #code functioins for one variable at a time. 
        #input
        #variable : string : user defines the variable to study
        files =np.sort(os.listdir(self.directory))[1:] #gets rid of the hidden file
        #exVract information about the size of the array from the first file in the list
        f = Dataset(self.directory + files[0], 'r')
        
        
        self.lon = np.array(f.variables['longitude'][:])
        self.lat = np.array(f.variables['latitude'][:])
        
        #for the code to work, information from the first file needs to be extracted
        #from all other files, append the reults. 
        #lon and lat remain the same. variable data and time information chagnes
        
        arr = np.array(f.variables[variable])
        time = f.variables['time'] 
        dtime = num2date(time[:], time.units) #hours since 1900-1-1 00:00:00"
        
        
        if len(files) > 1:
        #in the event a single file is passed, the code will still function    
            for file in files[1:]:#since first file info extracted, start with second onwards
                dset = Dataset(self.directory + file, 'r') 
                time2 = dset.variables['time']
                dtime2 = num2date(time2[:], time2.units) #hours since 1900-1-1 00:00:00"
                dtime = np.concatenate([dtime, dtime2], axis = 0) #append with dtime from first file
                
                var = np.array(dset.variables[variable]) #extract values for current file
                arr = np.concatenate([arr, var], axis = 0)#merge with the first file data
            
                
        arr[arr == -32767] = None #important step as netcdf variables created with fill_value of -32767
        arr = np.around(arr, decimals=2) #rounds off the values to a 
        self.cache = {'time' : dtime, 'latitude' : self.lat, 'longitude' : self.lon, variable : arr}
        return self.cache
       
     
    def nearest_point(self, lon_user, lat_user):
        #function to calculate the nearest data points
        #lon_file : Array of float64 : Array passed on from the netcdf file
        #lat_file : Array of float64 : Array passed on from the netcdf file
        #lon_user : float64 : coordinate passed onto the function by the user for which closest neighour is required
        #lat_user : float64 : coordinate passed onto the function by the user for which closest neighour is required
        
        #Outputs
        #Dictionary data type with the indexes and the corresponding values 
        #of longitude and latitude from the original file
        
        #checks if the specific user location matches grid points or not. 
        if not (lon_user in self.lon and lat_user in self.lat):
            idx_lon = np.abs(self.lon - lon_user).argmin()
            idx_lat = np.abs(self.lat - lon_user).argmin()
            print(f'The specified coordinates do not match any of the grid points available in the dataset. The nearest datapoint available is Latitude: {self.lat[idx_lat]}, Longitude: {self.lon[idx_lon]}')
        else:
            idx_lon = np.where(self.lon == lon_user)
            idx_lat = np.where(self.lat == lat_user)
        
        nearest_point_dict = {'latitude index': idx_lat, 'longitude index': idx_lon, \
                       'latitude' : self.lat[idx_lat], 'longitude' : self.lon[idx_lon]}
        
        #calculate the nearest distance
        if not (lon_user in self.lon and lat_user in self.lat):
           dist = self.calculate_dist(lat_user, lon_user, nearest_point_dict['latitude'], nearest_point_dict['longitude'])
           print('The distance between your specified coordinate and the nearest grid point is {:.2f} Km'.format(dist))
        
        return nearest_point_dict
        
    
    def calculate_dist(self, lat_user, lon_user, lat_nearest, lon_nearest):
        #input
        #lat_user : float64 : user specified latitude value
        #lon_user : float64 : user specified longitude value
        #lat_nearest : float64 : user specified latitude value
        #lon_nearest : float64 : user specified longitude value
        #output
        #distance between the two coordinates
        user_input = (lat_user, lon_user) #lat, lon
        nearest_point = (lat_nearest, lon_nearest)
        return haversine(user_input, nearest_point) #returns value in km
'''   
    def next_nearest_point(self, array, row_idx, col_idx, radius):
        #if user inputs coordinates and availability for the data point comes out low
        #the next_nearest_point_availibility function will calculate 3 other nearest points
      
        #input
        #array : 2D float64/int : data array to find the nearest neighours from
        #slice the raw data file to include only one time stamp. 
        #this step only needs access to neighouring 
        #row_idx : int : row index for the center point for which nearest neighour needs to be searched
        #col_idx : int : index for the center point for which nearest neighour needs to be searched
        #radius : int : not the radius of search. raidus within the array. specify if the search radius needs to be for instance 2 element or 3 element in all directions. 
       
        #output
        #returns a list
        #index of the nearest neighours
        #first element is row index, second element is column index
        
        #i iterates over row
        #j iterates over column
        
        above_i = row_idx + radius + 1 #defines the higher limt of row iterator
        if above_i > len(array) - 1: #takes into account the array length to avoid crossing index limits
            above_i = len(array)
        
        below_i = row_idx - radius #defines lower limit
        if below_i < 0: #takes into account the zero index
            below_i = 0
            
            
        above_j = col_idx + radius + 1 #defines the higher limit of column iterator
        if above_j > len(array) - 1: #takes the end index into account
            above_j = len(array)
        
        below_j = col_idx - radius #defines the lower limit of column iterator
        if below_j < 0: #takes zero index into account
            below_j = 0
            
        indices = list()
        for i in range(below_i, above_i):
            for j in range(below_j, above_j):
                indices.append(i, j) 
        
        
    
        
        return indices
    
    
'''    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
'''    
    
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
        
    
    def check_availability(self):
        #function to evaluate percentage of the times the data point has 
        #availability of data
        #function can only be used if file_type == 'Joint'
        #this function sums up the number of data points that are empty in the series and returns a percentage
        
        return self.joint_df[self.variable].isnull().sum()/len(self.joint_df) * 100 #calculate the percentage of data availabiliity
    
    
'''       
'''        
    def load_coordinate_data(self, lon_user, lat_user, variable, output_directory, file_type = 'Joint'):
        #Function to extract information about a single point
        self.variable = variable #reference variable to access in other functions of the class
        #input
        #lon_user : float64 : longitudnal value for which information is required
        #lat_user : float64 : latitudnal value for which information is required
        #variable : string : specify exactly the property to study. by default, 
        #all variables can be obtained but for now, we will limit the functionality to include only one variable specified by the user
        #output_directory : string : Provide directory to save the data file
        #file_type : string : 
        #if exact grid points for which data is available not entered, function 
        #finds the nearest data point. 
        self.nearest_grid_piont = self.near_point(self.lon, self.lat, lon_user, lat_user)
        dist = self.calculate_dist(lat_user, lon_user, self.nearest_grid_piont['latitude'], self.nearest_grid_piont['longitude'])
        
        if not lon_user in self.lon and lat_user in self.lat:
            print ('The entered longitudnal coordinate does not have an associated value, value from the closest data point will be used.')
            print('The nearest point to your query is: Longitude: ' + str(self.nearest_grid_piont['longitude']) + ', Latitude - ' + str(self.nearest_grid_piont['latitude']))
            print('Distance between entered point and the nearest available point is: ' + str(dist))
            
        #if else structure to support code in the for loop for joint data frame output
        if file_type == 'Joint':
            self.joint_df = pd.DataFrame()
            
        for file in self.files:
            f = Dataset(self.directory + file, 'r')
            #unpack all variables of interest
            time = f.variables['time']
            dtime = num2date(time[:], time.units) #hours since 1900-1-1 00:00:00"
            #unpack variable of interest into var
            self.var = f.variables[self.variable][:]
            #slice the var to extract the data for the data point only
            var_point = self.var[:, self.nearest_grid_piont['lat index'], self.nearest_grid_piont['lon index']]
            
            #create dataframe with the var information along with the lon/lat and date
            df = pd.DataFrame({'Date' : np.array(dtime[:]), 'Longitude' : self.nearest_grid_piont['longitude'], \
                               'Latitude' : self.nearest_grid_piont['latitude'],\
                                   self.variable : var_point})
                
            #write the output to csv files
            if file_type == 'Separate':
                df.to_csv(output_directory + file[:-3] + self.variable + '.csv')
            
                #concat the dataframe to produce one file
            else:
                self.joint_df = pd.concat([self.joint_df, df], ignore_index=True)
                
        if file_type == 'Joint':
            self.joint_df.to_csv(output_directory + 'Joint ' + self.variable + '.csv')
'''                
   
    
'''
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
            lon_reg = self.lon[self.vertex1['lon index'] : self.vertex2['lon index']+1]
            lat_reg = self.lat[self.vertex1['lat index'] : self.vertex2['lat index']+1]
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