#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 18:50:29 2021

@author: goharshoukat
"""


from windrose import WindroseAxes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from matplotlib.ticker import MaxNLocator, MultipleLocator
import cartopy as ct
from matplotlib.font_manager import FontProperties
import matplotlib.cm as cm


direc = 'tests/results/'
df = pd.read_csv(direc + '07_23-12_57_PM.csv', index_col = False)
df['Date'] = pd.to_datetime(df['Date'])
df = df.rename(columns = {'swh (m)':'swh', 'mwd (Degree true)':'mwd'})



bins = np.arange(1, 6, 1)
bins = np.append(bins, 6)
ax = WindroseAxes.from_ax()
#circle1 = plt.Circle((0, 0), 5,  transform=ax.transData._b, color='white', fill=True)
ax.bar(df.mwd, df.swh, bins = bins,normed = True, 
       opening=0.8,edgecolor='gray',lw=0.1, cmap = cm.CMRmap)

ax.set_thetagrids(range(0,360,45), [90, 45, 0, 315, 270, 225, 180, 135])
ax.set_theta_zero_location('W', offset=-180)
ax.set_xticklabels(['E', 'NE', 'N', 'NW',  'W', 'SW', 'S', 'SE'])
#ax.add_patch(circle1)
#ax.set_rorigin(-5)
plt.text(0., 0., "Calm", size=18, ha="center", va="center", bbox=dict(boxstyle="circle") )
ax.set_legend()
