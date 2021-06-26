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
        #output
        #a dictionary
        #time : str : contains the array of the time for all time
        #latitude : float : array of latitude
        #longitude : float : array of longitude
        #variable : float : array of the extracted data
        #lenght : int : length of each file for time to late split
        self.variable = variable
        
        self.files =np.sort(os.listdir(self.directory))[1:] #gets rid of the hidden file
        #exVract information about the size of the array from the first file in the list
        f = Dataset(self.directory + self.files[0], 'r')
        unit = []
        unit.append(f.variables[variable].units)
        unit.append(f.variables['latitude'].units)
        unit.append(f.variables['longitude'].units)
        
        self.lon = np.array(f.variables['longitude'][:])
        self.lat = np.array(f.variables['latitude'][:])
        
        #for the code to work, information from the first file needs to be extracted
        #from all other files, append the reults. 
        #lon and lat remain the same. variable data and time information chagnes
        
        arr = np.array(f.variables[variable])
        time = f.variables['time'] 
        dtime = num2date(time[:], time.units) #hours since 1900-1-1 00:00:00"
        
        #this variable is introduced to keep track of the time length of each file
        #it will then be used to split the concatenated array in the cache
        sizeofarray = np.array(len(time))
        if len(self.files) > 1:
        #in the event a single file is passed, the code will still function    
            for file in self.files[1:]:#since first file info extracted, start with second onwards
                dset = Dataset(self.directory + file, 'r') 
                time2 = dset.variables['time']
                dtime2 = num2date(time2[:], time2.units) #hours since 1900-1-1 00:00:00"
                dtime = np.concatenate([dtime, dtime2], axis = 0) #append with dtime from first file
                
                var = np.array(dset.variables[variable]) #extract values for current file
                arr = np.concatenate([arr, var], axis = 0)#merge with the first file data
                
                l = len(dtime2)
                sizeofarray = np.append(sizeofarray, l)
                
        arr[arr == -32767] = None #important step as netcdf variables created with fill_value of -32767
        arr = np.around(arr, decimals=2) #rounds off the values to a 
        self.cache = {'time' : dtime, 'latitude' : self.lat, 'longitude' : self.lon, variable : arr, 'units' : unit, 'length of file' : sizeofarray}
        return self.cache
    
    def extract_coordinate_data(self):
        #self.cache with all the coordinates data will be used for this function
        lat_idx = self.nearest_point_dict['latitude index'][0][0]
        lon_idx = self.nearest_point_dict['longitude index'][0][0]
        
        array_ = self.cache[self.variable][:, lat_idx, lon_idx]
        date = self.cache['time'][:]
        self.df = pd.DataFrame({'Date' :  date, 'Latitude' : self.lat[lat_idx], 'Longitude' : self.lon[lon_idx], self.variable : array_})
        
        availability = self.check_availability(self.df)
        
        return self.df
    
    def check_availability(self, df):
        #function to evaluate percentage of the times the data point has 
        #availability of data
        #function can only be used if file_type == 'Joint'
        #this function sums up the number of data points that are empty in the series and returns a percentage
        #input
        #df : Pandas DataFrame : checks the availibility of the data for the specifc dataframe and variable
        availability = 100 - df[self.variable].isnull().sum()/len(df) * 100 #calculate the percentage of data availabiliity
        print('This variable has an availability of {} % at your specified/nearest coordinates'.format(availability))
    
    def nearest_point(self, lat_user, lon_user):
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
            idx_lat = np.abs(self.lat - lat_user).argmin()
            print(f'The specified coordinates do not match any of the grid points available in the dataset. The nearest datapoint available is Latitude: {self.lat[idx_lat]}, Longitude: {self.lon[idx_lon]}')
        else:
            idx_lon = np.where(self.lon == lon_user)
            idx_lat = np.where(self.lat == lat_user)
        
        self.nearest_point_dict = {'latitude index': idx_lat, 'longitude index': idx_lon, \
                       'latitude' : self.lat[idx_lat], 'longitude' : self.lon[idx_lon]}
        
        #calculate the nearest distance
        if not (lon_user in self.lon and lat_user in self.lat):
           dist = self.calculate_dist(lat_user, lon_user, self.nearest_point_dict['latitude'], self.nearest_point_dict['longitude'])
           print('The distance between your specified coordinate and the nearest grid point is {:.2f} Km'.format(dist))
        
        return self.nearest_point_dict
        
    
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
    
    
    def write_coordinate_data(self, output_direc, save = 'Joint'):
        #function to write the extracted data ponts to a csv
        #input
        #output_direc : string : location to save the output files
        #output_direc should end with a slash at the end
        #if the folder doens exist, it will create folder
        #save : string : Joint or Separate
        #Joint creates a single data file
        #Separate creates one file per input file. Default is joint
        
        if not os.path.isdir(output_direc):
            os.mkdir(output_direc)
        
        #before writing the file, add the unit to the dataframe
        self.df = self.df.rename(columns={self.variable : (self.variable + ' ({})'.format(self.cache['units'][0])),\
                                          'Latitude' : ('Latitude' + ' ({})'.format(self.cache['units'][1])),\
                                        'Longitude' : ('Longitude' + ' ({})'.format(self.cache['units'][2]))})
                                 
        if save == 'Joint':
            self.df.to_csv(output_direc + self.variable + '.csv')
        
        elif save == 'Separate':
            for i in range(len(self.cache['length of file'])):
                if i == 0:
                    df2 = self.df[self.variable][0:self.cache['length of file'][0]].reset_index(drop = True)
                else:
                    df2 = self.df[self.variable][self.cache['length of file'][i-1]:(self.cache['length of file'][i] + self.cache['length of file'][i-1])].reset_index(drop = True)
                
                df2.to_csv(output_direc + self.files[i][:-3] + '.csv')
        else:
            print('Please choose between Joint or Separate save type for file output')
        

    
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