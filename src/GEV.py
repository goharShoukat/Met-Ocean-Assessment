#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 15:27:00 2021

@author: goharshoukat

Extreme Value Analysis
"""

import pandas as pd
import numpy as np

from scipy.stats import genextreme as gev
import matplotlib.pyplot as plt

direc = 'tests/results/'
df = pd.read_csv(direc + '07_23-12_57_PM.csv', index_col = False)
df['Date'] = pd.to_datetime(df['Date'])
df = df.rename(columns = {'swh (m)':'swh', 'mwd (Degree true)':'mwd'})
df['new_date']= df['Date'].dt.strftime('%Y-%m-%d')

threshold = 0.6 * np.max(df.swh)
z = df.swh[df.swh>threshold]
# calculate GEV fit
fit = gev.fit(z)

# GEV parameters from fit
c, loc, scale = fit
fit_mean= loc
min_extreme,max_extreme = gev.interval(0.99,c,loc,scale) 

# evenly spread x axis values for pdf plot
x = np.linspace(min(df.swh),max(df.swh),200)

# plot distribution
fig,ax = plt.subplots(1, 1)
plt.plot(x, gev.pdf(x, *fit))
plt.hist(z,30,alpha=0.3)
