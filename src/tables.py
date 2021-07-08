#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 12:42:17 2021

@author: goharshoukat

Script to produce tables as images. These tables are monthly and annual summmaries. 

"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from matplotlib.ticker import MaxNLocator, MultipleLocator
import cartopy as ct
from matplotlib.font_manager import FontProperties



direc = 'tests/results/'
df = pd.read_csv(direc + 'data_file.csv', index_col = False)
df['Date'] = pd.to_datetime(df['Date'])

# %% Monthly Summary 
month_mean = pd.DataFrame()
month_mean['swh'] = np.round(df.groupby([df['Date'].dt.month.rename('month')])['swh (m)'].quantile(0.5), 2)
month_mean['hmax'] = np.round(df.groupby([df['Date'].dt.month.rename('month')])['hmax (m)'].quantile(0.5), 2)
month_mean['mwp'] = np.round(df.groupby([df['Date'].dt.month.rename('month')])['mwp (s)'].quantile(0.5), 2)


month_min = pd.DataFrame()
month_min['swh'] = np.round(df.groupby([df['Date'].dt.month.rename('month')])['swh (m)'].quantile(0.05), 2)
month_min['hmax'] = np.round(df.groupby([df['Date'].dt.month.rename('month')])['hmax (m)'].quantile(0.05), 2)
month_min['mwp'] = np.round(df.groupby([df['Date'].dt.month.rename('month')])['mwp (s)'].quantile(0.05), 2)

month_max = pd.DataFrame()
month_max['swh'] = np.round(df.groupby([df['Date'].dt.month.rename('month')])['swh (m)'].quantile(0.95), 2)
month_max['hmax'] = np.round(df.groupby([df['Date'].dt.month.rename('month')])['hmax (m)'].quantile(0.95), 2)
month_max['mwp'] = np.round(df.groupby([df['Date'].dt.month.rename('month')])['mwp (s)'].quantile(0.95), 2)



months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month= np.array([months_list, month_mean['swh'], month_min['swh'], month_max['swh'], month_mean['hmax'], month_min['hmax'], month_max['hmax'], month_mean['mwp'], month_min['mwp'], month_max['mwp']]).T



fig = plt.figure(figsize = (60,60))
table = plt.table(cellText=month, colLabels=['Months', '50th %', '5th %', '95th %', '50th %', '5th %', '95th %', '50th %', '5th %', '95th %'],loc='center', 
                  cellLoc='center')
table.auto_set_font_size(False)
h = table.get_celld()[(0,0)].get_height()
w = table.get_celld()[(0,0)].get_width()

for (row, col), cell in table.get_celld().items():
  if (row == 0) or (col == 0):
    cell.set_text_props(fontproperties=FontProperties(weight='bold'))
# Create an additional Header
header = [table.add_cell(-1,pos, w, h, loc="center", facecolor="none") for pos in [1,2, 3]]
header[0].visible_edges = "TBL"
header[1].visible_edges = "TB"
header[2].visible_edges = "TBR"
header[1].get_text().set_text("$\\bf{Hs (m)}$")


header2 = [table.add_cell(-1,pos, w, h, loc="center", facecolor="none") for pos in [4,5, 6]]
header2[0].visible_edges = "TBL"
header2[1].visible_edges = "TB"
header2[2].visible_edges = "TBR"
header2[1].get_text().set_text("$\\bf{Hmax (m}$)")


header3 = [table.add_cell(-1,pos, w, h, loc="center", facecolor="none") for pos in [7,8, 9]]
header3[0].visible_edges = "TBL"
header3[1].visible_edges = "TB"
header3[2].visible_edges = "TBR"
header3[1].get_text().set_text("$\\bf{Tp (s)}$")
plt.axis('off')
plt.tight_layout()

plt.savefig('Plots/Monthly_Percentiles.png', dpi = 300)


# %% yearly summary



yearly_mean = pd.DataFrame()
yearly_mean['swh'] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])['swh (m)'].quantile(0.5), 2)[20:]
yearly_mean['hmax'] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])['hmax (m)'].quantile(0.5), 2)[20:]
yearly_mean['mwp'] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])['mwp (s)'].quantile(0.5), 2)[20:]


yearly_min = pd.DataFrame()
yearly_min['swh'] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])['swh (m)'].quantile(0.05), 2)[20:]
yearly_min['hmax'] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])['hmax (m)'].quantile(0.05), 2)[20:]
yearly_min['mwp'] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])['mwp (s)'].quantile(0.05), 2)[20:]

yearly_max = pd.DataFrame()
yearly_max['swh'] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])['swh (m)'].quantile(0.95), 2)[20:]
yearly_max['hmax'] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])['hmax (m)'].quantile(0.95), 2)[20:]
yearly_max['mwp'] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])['mwp (s)'].quantile(0.95), 2)[20:]


yearly_list = np.array(np.linspace(1999, 2019, 21),dtype=object).astype(int)

yearly= np.array([yearly_list, yearly_mean['swh'], yearly_min['swh'], yearly_max['swh'], yearly_mean['hmax'], yearly_min['hmax'], yearly_max['hmax'], yearly_mean['mwp'], yearly_min['mwp'], yearly_max['mwp']],dtype=object).T



fig = plt.figure(figsize = (60,60))
table = plt.table(cellText=yearly, colLabels=['Year', '50th %', '5th %', '95th %', '50th %', '5th %', '95th %', '50th %', '5th %', '95th %'],loc='center', 
                  cellLoc='center')
table.auto_set_font_size(False)
h = table.get_celld()[(0,0)].get_height()
w = table.get_celld()[(0,0)].get_width()

for (row, col), cell in table.get_celld().items():
  if (row == 0) or (col == 0):
    cell.set_text_props(fontproperties=FontProperties(weight='bold'))
# Create an additional Header
header = [table.add_cell(-1,pos, w, h, loc="center", facecolor="none") for pos in [1,2, 3]]
header[0].visible_edges = "TBL"
header[1].visible_edges = "TB"
header[2].visible_edges = "TBR"
header[1].get_text().set_text("$\\bf{Hs (m)}$")


header2 = [table.add_cell(-1,pos, w, h, loc="center", facecolor="none") for pos in [4,5, 6]]
header2[0].visible_edges = "TBL"
header2[1].visible_edges = "TB"
header2[2].visible_edges = "TBR"
header2[1].get_text().set_text("$\\bf{Hmax (m)}$")


header3 = [table.add_cell(-1,pos, w, h, loc="center", facecolor="none") for pos in [7,8, 9]]
header3[0].visible_edges = "TBL"
header3[1].visible_edges = "TB"
header3[2].visible_edges = "TBR"
header3[1].get_text().set_text("$\\bf{Tp (s)}$")

plt.axis('off')

plt.tight_layout()

plt.savefig('Plots/Yearly_Percentiles.png', dpi = 300)

# %%
