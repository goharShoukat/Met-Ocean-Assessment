#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 12:36:40 2022

@author: goharshoukat
"""
import cdsapi
variable = ['10m_u_component_of_wind', '10m_v_component_of_wind']
c = cdsapi.Client(timeout=600,quiet=False,debug=True)

c.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
    {
        'product_type': 'monthly_averaged_reanalysis_by_hour_of_day',
        'variable': variable,
        'year': [

            '2021',
        ],
        'month': [
            '01', 
        ],
        'time': [
            '00:00', 
        ],
        'area': [
            10, 176, 8,
            178,
        ],
        'format': 'netcdf',
    },
    'download.nc')