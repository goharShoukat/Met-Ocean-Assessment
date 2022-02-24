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
variable = ['10m_u_component_of_wind', '10m_v_component_of_wind', 'mean_wave_direction']
c = cdsapi.Client(timeout=600)

for year in range(1979,1982):
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