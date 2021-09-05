#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 13:48:15 2021

@author: goharshoukat

scatter plots demnostrating number of bins in each bin

uses gaussian kde to plot contours and kde plots
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from scipy.stats import gaussian_kde
import matplotlib as mpl
def contours(df, variable1, variable2, units, Coordinates, date_range, direc):
    #ideally plotted just for swh vs mwp
    #inputs
    #df : pd.DataFrame : the entire dataframe as it is passed through from the run_code script
    #variable1: str : variable name - x variable like swh
    #variable2: str : variable name - y variable like mwp
    #the titles are used in plotting
    #Coordinates : str : The coordinates for which this data is extracted
    #date_range : str : The date interval for which this data corresponds to
    #title : str : title of the plot e.g. mwp vs swh
    #units : pd.DataFrame : df contains units of respective variables
    #direc : str : output directory entered by user
    
    
    variable1 = 'swh'
    variable2 = 'mwp'
    var1 = df[variable1] #swh
    var2 = df[variable2] #mwp
    b = 0.1
    bins_x = np.arange(np.floor(np.min(var1)), np.ceil(np.max(var1)) + 0.05, 0.05)
    bins_y = np.arange(np.floor(np.min(var2)), np.ceil(np.max(var2)) + 0.05, 0.1)
    H = np.arange(np.min(var1), np.max(var2) + 1, 0.05)
    T01428 = np.sqrt(2 * np.pi / 9.81 * H * 7)
    T125 = np.sqrt(2 * np.pi / 9.81 * H * 12.5)
    T15 = np.sqrt(2 * np.pi / 9.81 * H * 15)
    T20 = np.sqrt(2 * np.pi / 9.81 * H * 20)
    T25 = np.sqrt(2 * np.pi / 9.81 * H * 25)
    T30 = np.sqrt(2 * np.pi / 9.81 *  H * 30)
    
    xy = np.vstack([var1,var2])
    z = gaussian_kde(xy)(xy)
    
    # Sort the points by density, so that the densest points are plotted last
    idx = z.argsort()
    x, y, z = var1[idx], var2[idx], z[idx]
    
    
    #dummy figure to extract number of points in each bin. this will not be saved or processed further. it will be closed immediataly after plotting. 
    #alpha = 0 could not work because that would leave the color of the map transparent as well. 
    plt.figure(figsize=(30,30))
    h = plt.hist2d(x, y, bins = (bins_x, bins_y), cmin = 0.00000001, cmap = 'inferno')
    plt.close()
    
    #h[3] provides the frequency in each bin to the actual plot
    fig = plt.figure(figsize=(30,30))
    plt.scatter(x, y, c=z, s=10)
    plt.xlabel('{}'.format(variable1 + ' (' + units.loc[0, variable1] + ')'))
    plt.ylabel('{}'.format(variable2 + ' (' + units.loc[0, variable2] + ')'))
    
   # plt.title('try')
    plt.show()
    cbar = plt.colorbar(h[3])
    cbar.set_label('Number of points in the 0.05 x 0.05 bin')
    plt.set_cmap('inferno')
    #plt.plot(H, T01428, label = '$\epsilon$ = 1/7')
    #plt.plot(H, T125, label = '$\epsilon$ = 1/12.5')
    plt.plot(H, T15, label = '$\epsilon$ = 1/15')
    plt.plot(H, T20, label = '$\epsilon$ = 1/20')
    plt.plot(H, T25, label = '$\epsilon$ = 1/25')
    plt.plot(H, T30, label = '$\epsilon$ = 1/30')
    plt.grid()
    plt.legend()
    mpl.rcParams.update(mpl.rcParamsDefault)
    plt.title('{}\n Scatter Plot & Kernel Density : {}'.format(Coordinates, date_range))
    #fig.tight_layout()
    plt.savefig(direc + '{} vs {} Scatter_Plots.pdf'.format(variable1, variable2))
    plt.close()
    
    levels = [0.1, 0.3, 0.5, 0.7, 0.9, 0.99, 0.999]
    fig2 = plt.figure()
    p = sns.kdeplot(var1, var2, label = 'Data', levels = levels)
    plt.xlabel('{}'.format(variable1 + ' (' + units.loc[0, variable1] + ')'))
    plt.ylabel('{}'.format(variable2 + ' (' + units.loc[0, variable2] + ')'))
    plt.title('{}\n{} vs {} Kernel Density Contour Plot : {}'.format(Coordinates, variable1, variable2, date_range))
    plt.grid()
    plt.plot(H, T15, '--', label = '$\epsilon$ = 1/15', linewidth=0.5)
    plt.plot(H, T20, '--', label = '$\epsilon$ = 1/20', linewidth=0.5)
    plt.plot(H, T25, '--', label = '$\epsilon$ = 1/25', linewidth=0.5)
    plt.plot(H, T30, '--', label = '$\epsilon$ = 1/30', linewidth=0.5)
    plt.legend()
    plt.text(8, 4, 'Level Curves Enclosing\n10\n30\n50\n70\n90\n99\n99.9', color='black', 
            fontsize=9)
    fig2.tight_layout()
    plt.savefig(direc + '{} vs {} kde_contour.pdf'.format(variable1, variable2))
    plt.close() 
    
 


'''


direc = 'results/'
df = pd.read_csv(direc + '09_06-12_20_AM.csv', index_col = False)
df['Date'] = pd.to_datetime(df['Date'])
df = df.rename(columns = {'swh (m)':'swh', 'mwp (s)':'mwp'})
df['new_date']= df['Date'].dt.strftime('%Y-%m-%d')

swh = df.swh
mwp = df.mwp
b = 0.1
bins_x = np.arange(np.floor(np.min(swh)), np.ceil(np.max(swh)) + 0.05, 0.05)
bins_y = np.arange(np.floor(np.min(mwp)), np.ceil(np.max(mwp)) + 0.05, 0.1)
H = np.arange(np.min(swh), np.max(swh) + 1, 0.05)
T01428 = np.sqrt(2 * np.pi / 9.81 * H * 7)
T125 = np.sqrt(2 * np.pi / 9.81 * H * 12.5)
T15 = np.sqrt(2 * np.pi / 9.81 * H * 15)
T20 = np.sqrt(2 * np.pi / 9.81 * H * 20)
T25 = np.sqrt(2 * np.pi / 9.81 * H * 25)
T30 = np.sqrt(2 * np.pi / 9.81 *  H * 30)

xy = np.vstack([swh,mwp])
z = gaussian_kde(xy)(xy)

# Sort the points by density, so that the densest points are plotted last
idx = z.argsort()
x, y, z = swh[idx], mwp[idx], z[idx]


#dummy figure to extract number of points in each bin. this will not be saved or processed further. it will be closed immediataly after plotting. 
#alpha = 0 could not work because that would leave the color of the map transparent as well. 
plt.figure(figsize=(30,30))
h = plt.hist2d(x, y, bins = (bins_x, bins_y), cmin = 0.00000001, cmap = 'inferno')
plt.close()


#h[3] provides the frequency in each bin to the actual plot

fig = plt.figure(figsize=(30,30))
plt.scatter(x, y, c=z, s=10)
plt.xlabel('swh (m)')
plt.ylabel('mwp (s)')
cbar = plt.colorbar(h[3])
cbar.set_label('Number of points in the 0.05 x 0.05 bin')
plt.set_cmap('inferno')
#plt.plot(H, T01428, label = '$\epsilon$ = 1/7')
#plt.plot(H, T125, label = '$\epsilon$ = 1/12.5')
plt.plot(H, T15, label = '$\epsilon$ = 1/15')
plt.plot(H, T20, label = '$\epsilon$ = 1/20')
plt.plot(H, T25, label = '$\epsilon$ = 1/25')
plt.plot(H, T30, label = '$\epsilon$ = 1/30')
plt.grid()
plt.legend()
plt.title('{} $^\circ$N, {} $^\circ$E \n Scatter Plot & Kernel Density : ({} - {})'.format(df['latitude (degrees_north)'][0], df['longitude (degrees_east)'][0],df['new_date'][0], df.iloc[-1]['new_date']))
plt.show()
plt.savefig('Plots/Scatter_Plots.pdf')


levels = [0.1, 0.3, 0.5, 0.7, 0.9, 0.99, 0.999]
plt.figure(figsize=(30,30))
p = sns.kdeplot(swh, mwp, label = 'Data', levels = levels)
plt.xlabel('Significant Wave Height (m)')
plt.ylabel('Mean Wave Period (s)')
plt.title('{} $^\circ$N, {} $^\circ$E \n SWH vs MWP Kernel Density Contout Plot : ({} - {})'.format(df['latitude (degrees_north)'][0], df['longitude (degrees_east)'][0],df['new_date'][0], df.iloc[-1]['new_date']))
plt.grid()
plt.plot(H, T15, '--', label = '$\epsilon$ = 1/15', linewidth=0.5)
plt.plot(H, T20, '--', label = '$\epsilon$ = 1/20', linewidth=0.5)
plt.plot(H, T25, '--', label = '$\epsilon$ = 1/25', linewidth=0.5)
plt.plot(H, T30, '--', label = '$\epsilon$ = 1/30', linewidth=0.5)
plt.legend()
plt.text(8, 4, 'Level Curves Enclosing\n10\n30\n50\n70\n90\n99\n99.9', color='black', 
        fontsize=9)
plt.savefig('Plots/kde_contour.pdf')


'''
