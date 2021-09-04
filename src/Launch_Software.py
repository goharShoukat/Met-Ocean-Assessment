#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 20:24:27 2021

@author: goharshoukat

This script combinees both the time series extraction and the plotting
libraries. 

It only function with default settings. 


"""

import numpy as np
import pandas as pd
from run_code import run_script
from freq_occurence import frequency_occurence
import os

print('Welcome! This is a Preliminary Wind & Wave Resource Assessment Tool designed inhouse by GDG\n\n\n')
print('Before proceeding, please chose from amongst the 3 different options available to you:\n\n')
print('1. Extract data for variables of choice at a specified location.\n')
print('2. Extract data for variables associated with waves at a specified choice and plot using default plotting settings. If you chose this option, please ensure that you include swh, mwp and hmax within your choice of variables.\n')
print('3. Extract data for variables associated with wind at a specified choice and plot using default plotting settings. If you chose this option, please ensure that you include u10 and v10 within your choice of variables.\n')

option = (input('Select your option\n'))

if int(option) == 1:
    _ = run_script()

elif int(option) == 2:
    df, variable, units = run_script()
    
    
    pass

elif int(option) == 3:
    pass

else:
    print('Acceptable inputs are: 1, 2 & 3. Please relaunch and try again. ')
