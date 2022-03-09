#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 12:36:40 2022

@author: goharshoukat

Variables available for download:
    1. '100m_u_component_of_wind', 
    2. '100m_v_component_of_wind', 
    3. '10m_u_component_of_neutral_wind',
    4. '10m_u_component_of_wind', 
    5. '10m_v_component_of_neutral_wind', 
    6, '10m_v_component_of_wind',
    7. '10m_wind_gust_since_previous_post_processing', 
    8. 'instantaneous_10m_wind_gust', 
    9. 'mean_wave_direction',
    10. 'mean_wave_period', 
    11. 'significant_height_of_combined_wind_waves_and_swell',

Note: All variables are not covered here. The list is non-exhaustive. 
      Complete list can be viewed on the CDS website. 
      
      Also please do not enter more than 2-3 variables at a time. The size
      of each download file is limited and larger area coverage would require
      less data being fetched per request. Therefore, it is necessary that
      each data file contains a maximum of 2-3 variables only. 



Years covered under the dataset:
    1979 - Present (40+)
    
Months included:
    Jan - Dec (12)
    
Hours of day included:
    00:00 - 23:00

Global Coverage:
    
                        North
                         90

West            - 180          180                   East

                        - 90
                        South



Warning:
    Please ensure that the coordinates lie within this range only. 
"""


import cdsapi
import numpy as np
from os import path
import os


def download_cdspy(variables: list, year_start : float, year_end : float, 
                   North: float, West: float,
                   South: float, East: float,
                   folder_name: str):
    #variables  : list : list of string variables to download 
    #year_start : float : year to start downloading from
    #year_end   : float : year to end download
    #North      : float : define the coordinates of the area
    #West       : float : define the coordinates of the area
    #East       : float : define the coordinates of the area
    #South      : float : define the coordinates of the area
    #folder_name : str : define folder name to be created or store data in
    
    #Variables available for download:
    #    1. '100m_u_component_of_wind', 
    #    2. '100m_v_component_of_wind', 
    #    3. '10m_u_component_of_neutral_wind',
    #    4. '10m_u_component_of_wind', 
    #    5. '10m_v_component_of_neutral_wind', 
    #    6, '10m_v_component_of_wind',
    #    7. '10m_wind_gust_since_previous_post_processing', 
    #    8. 'instantaneous_10m_wind_gust', 
    #    9. 'mean_wave_direction',
    #    10. 'mean_wave_period', 
    #    11. 'significant_height_of_combined_wind_waves_and_swell',
    #    12. 'peak_wave_period',
    #    13. 'significant_height_of_wind_waves'

    #Note: All variables are not covered here. The list is non-exhaustive. 
    #      Complete list can be viewed on the CDS website. 



    #Years covered under the dataset:
    #    1979 - Present (40+)
        
    #Months included:
    #    Jan - Dec (12)
    #    
    #Hours of day included:
    #    00:00 - 23:00

    #Global Coverage:
        
     #                       North
     #                       90

     #West            - 180       180                   East

     #                       - 90
     #                       South



    #Warning:

    #    Please ensure that the coordinates lie within this range only. 

    #create folder if directory doesnt exist
    if not path.isdir(folder_name):
        os.mkdir(folder_name)
    
    #if len(variables) > 3:
        
    #    print("Please ensure only a maximum of 2 variables are added per \
    #          request. The size overflow will cause the download to fail. ")
    #    raise ValueError
    c = cdsapi.Client(timeout=600,quiet=False,debug=True)
    
    for year in range(year_start,year_end+1):
        print(year)
        c.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': variables,
                'month': [
                    '01', 
                ],
                'day': [
                    '01', 
                ],
                'time': [
                    '00:00', 
                ],
                'area': [
                    North, West, South, East
                ],
                'year': str(year),
            },
            folder_name + '/' + str(year) + '.nc')
        

"""
   
            
variable = ['10m_u_component_of_wind', '10m_v_component_of_wind', 'mean_wave_period', 'significant_height_of_wind_waves']
year_start = 2021
year_end = 2022
download_cdspy(variable, year_start, year_end, 90, 178, 88, 180, 'new_data_format') 
variable = ['10m_u_component_of_wind', '10m_v_component_of_wind', 'mean_wave_period', 'significant_height_of_wind_waves']
year_start = 2021
year_end = 2022
download_cdspy(variable, year_start, year_end, 90, 178, 88, 180, 'new_data_format')
# %%
variable = ['10m_u_component_of_wind', '10m_v_component_of_wind']
c = cdsapi.Client(timeout=600,quiet=False,debug=True)

for year in range(1979,1981):
    print(year)
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': variable,
            'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
            ],
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
            'area': [
                90, 178, 88,
                180,
            ],
            'year': str(year),
        },
        'data_test/' + str(year) + '.nc')
    
    """