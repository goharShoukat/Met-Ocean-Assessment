#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 21:44:22 2021

@author: goharshoukat

script to generate velocity and direction column vectors from the wind data

"""
import pandas as pd
import numpy as np


def wind_calc(dataframe):
#function to calculate the bearing. takes in the resultant vector
#outputs the bearing
#inputs:
    #dataframe : pd.DataFrame : dataframe with the u10 and v10
#outputs:
    #ang : np.ndarray : bearing giving blowing from
    #magnitude : np.ndarray : mangintude vector
    
    vector = np.array(dataframe[{'u10', 'v10'}].values.tolist())
    #calculates the angle from the postive x axis counter clockwise. neg is clockwise
    bearing = np.mod(180 + 180/np.pi * np.arctan2(vector[:, 1], vector[:,0]), 360)
    magnitude = np.sqrt(dataframe['u10']**2 + dataframe['v10']**2)
    
    
    return bearing, magnitude

