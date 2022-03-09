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
from datetime import datetime  #libraries required to convert the time column of netcdf4
import pandas as pd
from pathlib import Path
from haversine import haversine
import glob
class ERA5():
    def __init__(self, directory):
        #inputs
        #directory : string : provide path of the directory housing the data files
        self.directory = directory
        self.files =np.sort(glob.glob(self.directory+'*.nc')) #gets rid of the hidden file. this will differ for windows
        #exVract information about the size of the array from the first file in the list
        self.f = Dataset(self.files[0], 'r')
        
    def load_variable(self, variable_list):
        #code functioins for one variable at a time. 
        #input
        #variable_list : numpy.ndarray : user defines the variables to study
        #output
        #a dictionary
        #time : str : contains the array of the time for all time
        #latitude : float : array of latitude
        #longitude : float : array of longitude
        #variable : float : array of the extracted data
        #lenght : int : length of each file for time to late split
        #keys : list : list of the variables available within the  data files for the user to chose from
        self.variable_list = variable_list
        self.lon = np.array(self.f.variables['longitude'][:])
        self.lat = np.array(self.f.variables['latitude'][:])
        time = self.f.variables['time'] 
        dtime = num2date(time[:], time.units) #hours since 1900-1-1 00:00:00"
        sizeofarray = np.array(len(time))
        #keys= list(f.variables.keys())
        
        #for the code to work, information from the first file needs to be extracted
        #from all other files, append the reults. 
        #lon and lat remain the same. variable data and time information chagnes
        self.cache = {}
        
        #extract variable unit information
        unit_list = variable_list
        unit_list = np.append(unit_list, ['latitude', 'longitude', 'time'])
        unit = pd.DataFrame(columns = unit_list, index = [0])
        unit.iloc[0]['latitude'] = self.f.variables['latitude'].units #after thought. also need to extract units for latitude and longitude. however, we can not alter the variable_list, otherwise it will break the code. 
        unit.iloc[0]['longitude'] = self.f.variables['longitude'].units
        unit.iloc[0]['time'] = time.units


        #creates a dictionary with all the variables
        for variable in variable_list:
            self.variable = variable
            unit.iloc[0][variable] = self.f.variables[variable].units

            
            
            #unit.append(self.f.variables[variable].units)
            
            
        #for the code to work, information from the first file needs to be extracted
        #from all other files, append the reults. 
        #lon and lat remain the same. variable data and time information chagnes
        
            arr = np.array(self.f.variables[variable])
            arr[arr == -32767] = None   #important step as netcdf variables created with fill_value of -32767
            arr = np.around(arr, decimals=2)
            self.cache[variable] = arr
            
            #
            if len(self.files) > 1:
                for file in self.files[1:]:
                    f2 = Dataset(file, 'r')
                    var = np.array(f2.variables[variable])
                    var[var == -32767] = None   #important step as netcdf variables created with fill_value of -32767
                    var = np.around(var, decimals=2)
                    self.cache[variable] = np.concatenate([self.cache[variable], var], axis = 0) 

    
    
    #    time and length arrays are fixed here
        if len(self.files) > 1:
                
            for file in self.files[1:]:
                dset = Dataset(file, 'r')
                time2 = dset.variables['time']
                dtime2 = num2date(time2[:], time2.units) #hours since 1900-1-1 00:00:00"
                dtime = np.concatenate([dtime, dtime2], axis = 0)
                l = len(dtime2)
                sizeofarray = np.append(sizeofarray, l)
            
        self.cache['time'] = dtime
        self.cache['longitude'] = self.lon
        self.cache['latitude'] = self.lat
        self.cache['length of file'] = sizeofarray
        self.cache['Units'] = unit
        return self.cache
    
    def extract_coordinate_data(self, variable, lat_idx = False, lon_idx = False):
        #self.cache with all the coordinates data will be used for this function
        #input
        #variables : numpy.ndarray of string : variable for which the data has to be extracted
        #lat_idx / lon_idx : float : under normal circumstances, these will be self transmitted to the function
        #the index of the latitude and longitude need to be transmitted
        #the actual longitude and latitude need not be mentioned
        #neighouring_cells_request_active : boolean : this will be true only when we are exploring neighouring cells
        #the neighouring_cells_request_active : remain false when multiple variables are being querried
        #important to include this here because this function will be called in the function explore_more_points. 
        #however, this function also has a call to this very function. 
        #to prevent from getting stuck in an infinite loop, this argument is added. 
        #output
        #dataframe of the variable data along with the time and lan and lat information
        #availability at this point
        
        if lat_idx == False and lon_idx == False:
            lat_idx = self.nearest_point_dict['latitude index']
            lon_idx = self.nearest_point_dict['longitude index']
        
        
        array_ = self.cache[variable][:, lat_idx, lon_idx]
        date = self.cache['time'][:]
        df = pd.DataFrame({'Date' :  date, 'latitude' : self.lat[lat_idx], 'longitude' : self.lon[lon_idx], variable : array_})
        
        availability = self.check_availability(df, variable)
        
        '''
        if neighouring_cells_request_active == False:#this false will ensure that only the first time the function is called, this optin will be provided to the user. Once the funtion is called from within the function explore_more_points, this will not get activated and prevent the infinite loop 
            if (availability != 100):
                user_input_nearest_point = input('This point has low availability. Do you wish to explore surrounding grid points?\n')
                if user_input_nearest_point == 'yes' or user_input_nearest_point == 'y' or user_input_nearest_point == 'Yes' or user_input_nearest_point == 'Y':
                    self.explore_more_points()
        '''
        return df, availability
    
    def check_availability(self, df, variable):
        #function to evaluate percentage of the times the data point has 
        #availability of data
        #function can only be used if file_type == 'Joint'
        #this function sums up the number of data points that are empty in the series and returns a percentage
        #input
        #df : Pandas DataFrame : checks the availibility of the data for the specifc dataframe and variable
        availability = 100 - df[variable].isnull().sum()/len(df) * 100 #calculate the percentage of data availabiliity
        print('{} has an availability of {} % at your specified/nearest coordinates\n'.format(variable,availability))
        return availability
    
    def nearest_point(self, lat_user, lon_user, radius = 1):
        #function to calculate the nearest data points
        #lon_user : float64 : coordinate passed onto the function by the user for which closest neighour is required
        #lat_user : float64 : coordinate passed onto the function by the user for which closest neighour is required
        #radius : int : specifiy the number of neighouring cells to explore. can only be defined interms of the neighouring cells. not distance
        #Outputs
        #Dictionary data type with the indexes and the corresponding values 
        #of longitude and latitude from the original file
        self.lat_user = lat_user
        self.lon_user = lon_user
        #checks if the specific user location matches grid points or not. 
        if not (lon_user in self.lon and lat_user in self.lat):
            idx_lon = np.abs(self.lon - lon_user).argmin()
            idx_lat = np.abs(self.lat - lat_user).argmin()
            print(f'The specified coordinates do not match any of the grid points available in the dataset. The nearest datapoint available is Latitude: {self.lat[idx_lat]}, Longitude: {self.lon[idx_lon]}')
        else:
            idx_lon = np.where(self.lon == lon_user)
            idx_lat = np.where(self.lat == lat_user)
        
        if type(idx_lon) == tuple:
            idx_lon = idx_lon[0][0]
            idx_lat = idx_lat[0][0]
            
        self.nearest_point_dict = {'latitude index': idx_lat, 'longitude index': idx_lon, \
                       'latitude' : self.lat[idx_lat], 'longitude' : self.lon[idx_lon]}
        
        #calculate the nearest distance
        if not (lon_user in self.lon and lat_user in self.lat):
           dist = self.calculate_dist(lat_user, lon_user, self.nearest_point_dict['latitude'], self.nearest_point_dict['longitude'])
           print('The distance between your specified coordinate and the nearest grid point is {:.2f} Km\n'.format(dist))
        
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
    
    
    def write_coordinate_data(self, df, variable, output_direc):
        #function to write the extracted data ponts to a csv
        #input
        #df : DataFrame : extracted coordinate data for one or all variables
        #varilable : np.ndarray : array of all variables
        #output_direc : string : location to save the output files
        #output_direc should end with a slash at the end
        #if the folder doens exist, it will create folder
        
        #extract units before writing it in the data file
        #for the purpose of plots, latitude and longitude will also be added to the list of variables. all variables witll have their units attached. 
        variable = np.append(variable, ['latitude', 'longitude'])
      
        
        for var in variable:
            df = df.rename(columns = {var : (var + ' ({})'.format(self.cache['Units'].iloc[0][var]))})        
 
        
        if not os.path.isdir(output_direc):
            os.mkdir(output_direc)
        
        date = datetime.now().strftime("%m_%d-%I_%M_%p")
        file_name = output_direc + date
        df.to_csv(file_name + '.csv', index = False)
            
        
        
    def next_nearest_point(self, row_idx, col_idx):
        #if user inputs coordinates and availability for the data point comes out low
        #the next_nearest_point_availibility function will calculate 3 other nearest points
      
        #input
        #variable : string : variable from the list of variables available within the data file
        #row_idx : int : row index for the center point for which nearest neighour needs to be searched
        #col_idx : int : index for the center point for which nearest neighour needs to be searched
        
        #output
        #returns a list
        #index of the nearest neighours
        #first element is row index, second element is column index
        
        #i iterates over row
        #j iterates over column
        
                
        #array : 2D float64/int : data array to find the nearest neighours from
        #slice the raw data file to include only one time stamp. 
        #this step only needs access to neighouring 
        array = self.cache[self.variable][0,:,:]
        
        
        #radius : int : it will iteratively increase until a distance limit is crossed
        #radius : int : specifies the radius in units of number of neighouring cells to check. 
        
        radius = 1

        
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
                indices.append([i, j]) 
                
        #this also includes the original cell. delete the original cell index
        #if [row_idx, col_idx] in indices:
         #   indices.pop(indices.index([self.nearest_point_dict['latitude index'], self.nearest_point_dict['longitude index']]))
       
         
        return indices
    
    
    def explore_more_points(self, variable):
        #input
        #variable : array of string : for which the calculation is being carried out
        #output
        #provides user option to explore data from surrounding neighouring grid points
        #explore data availability at each new data point
        #provides distance from each data point
        #additionally it allows switching coordinates and recalls the extract_coordinate_data to match the new selection
            
        indices = self.next_nearest_point(self.nearest_point_dict['latitude index'], self.nearest_point_dict['longitude index'])
                
        for ind in indices:
            for var in variable:
                if self.lat[self.nearest_point_dict['latitude index']] == self.lat[ind[0]] and self.lon[self.nearest_point_dict['longitude index']] == self.lon[ind[1]]:
                        pass
                else:
                    dist = self.calculate_dist(self.lat_user, self.lon_user, self.lat[ind[0]], self.lon[ind[1]])
                    print ('Distance between your specified point and the neighouring data point Lat: {}, Lon: {} is {:.2f} km'.format(self.lat[ind[0]], self.lon[ind[1]], dist))
                    df, _ = self.extract_coordinate_data(var, ind[0], ind[1])



    def df_generator(self, variable, research_more_points = False):
        #function to generate a combined dataframe of all the variables within the 
        #variables supplied by the user. It will also check the availability and 
        #call the necessary functions 
    
        #input
        #variable : array of string : contains all the variables for which 
        #research_more_points : dictionary of nearest point
        
        #output
        #combined_df : pandas.DataFrame : cotaining Date, lat/lon, variables
        #availability : np.array : array of the availibitly fo all variables
        availability = []
        self.combined_df= pd.DataFrame()
        for var in variable:
            df, avail= self.extract_coordinate_data(var)
            self.combined_df['Date'] = df['Date']
            self.combined_df['latitude'] = df['latitude']
            self.combined_df['longitude'] = df['longitude']
            self.combined_df[var] = df[var]
            availability = np.append(availability, avail)
        
        """
        #allow us to identify which variable has low availability
        avail_check = availability != 100
        
        if True in avail_check:
            print('The following variables have a low availability at the nearest/specified coordinate {}\n'.format(variable[avail_check]))
            user_input_nearest_point = input('This point has low availability. Do you wish to explore surrounding grid points?')
            if user_input_nearest_point == 'yes' or user_input_nearest_point == 'y' or user_input_nearest_point == 'Yes' or user_input_nearest_point == 'Y':
                self.explore_more_points(variable)
        """   
        return self.combined_df