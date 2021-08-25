#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 15:43:17 2021

@author: goharshoukat

uses percentage thresholds instead of probabililty density functions to plot
the gaussian kde. 
"""

import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt



direc = 'tests/results/'
df = pd.read_csv(direc + '07_29-02_43_PM.csv', index_col = False)
df['Date'] = pd.to_datetime(df['Date'])
df = df.rename(columns = {'swh (m)':'swh', 'mwp (s)':'mwp'})
df['new_date']= df['Date'].dt.strftime('%Y-%m-%d')



swh = df.swh
mwp = df.mwp


k = gaussian_kde(np.vstack([swh, mwp]))
xi, yi = np.mgrid[swh.min():swh.max():0.025,mwp.min():mwp.max():0.025]
zi = k(np.vstack([xi.flatten(), yi.flatten()]))

zi = (zi-zi.min())/(zi.max() - zi.min())
zi = zi.reshape(xi.shape)

levels = [0.1, 0.3, 0.5, 0.7, 0.9, 0.99, 0.999]

plt.figure(figsize=(30,30))
CS = plt.contour(xi, yi, zi,levels = levels,
              colors=('k',),
              linewidths=(1,),
              )

plt.clabel(CS, fmt='%.3f', colors='b', fontsize=8)
plt.xlim(-0.5,swh.max()+.1)
