#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 15:27:00 2021

@author: goharshoukat

Extreme Value Analysis
"""

import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import genextreme as gev
from scipy.stats import cumfreq
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm

direc = 'tests/results/'
df = pd.read_csv(direc + '07_23-12_57_PM.csv', index_col = False)
df['Date'] = pd.to_datetime(df['Date'])
df = df.rename(columns = {'swh (m)':'swh', 'mwd (Degree true)':'mwd'})
df['new_date']= df['Date'].dt.strftime('%Y-%m-%d')

# %% Generate histogram and GEV fit for the data
#Generate a density plot
threshold = 0.6 * np.max(df.swh)
z = df.swh[df.swh>threshold]
# calculate GEV fit
fit = gev.fit(z)

# GEV parameters from fit
c, loc, scale = fit
fit_mean= loc


# evenly spread x axis values for pdf plot
x1 = np.linspace(min(df.swh),max(df.swh),200)

# plot distribution
plt.figure(figsize=(30,30))
plt.plot(x1, gev.pdf(x1, *fit))
z.plot.hist(density = True)
plt.xlabel('Significant Wave Height (m)')
plt.ylabel('Probability Density')
plt.title('{} $^\circ$N, {} $^\circ$E \n Generalised Extreme Value : ({} - {})'.format(df['latitude (degrees_north)'][0], df['longitude (degrees_east)'][0],df['new_date'][0], df.iloc[-1]['new_date']))
plt.savefig('Plots/Density Plot.pdf')

# %% Generate a Probability Plot
def exceedence(df, content, plot = False):
    #takes in the raw data file as input
    #content : string : the signal for which exceedence is needed
    #plot : string : Boolean. if true, plot is also displayed
    #outputs the exceedence curve : array
    #outputs the array for which the exceedence is calculated : array

    maxima = df.max(axis = 0) #needed to define the upper limit of array
    minima = df.min(axis = 0)#defines lower limit for which exceedence is calculated
    thresh_array = np.linspace(minima[content], maxima[content], 10)
    exceedence = []
    for i in range(len(thresh_array)):
        d = df[content] < thresh_array[i] #checks which value is above or below the value in the array
        x = sum(d) / len(df) #first fins total number of values in the df which exceed the stated value in the array. then finds the probability of the true values. then subtracts  from 1 to find the exceedence
        exceedence.append(x) #push it into the array which is then returned
        
    if plot == True:
        #fig = plt.figure(figsize = (20,10))
        plt.semilogy(thresh_array, exceedence)
        plt.xlabel(r'X/$\bar{X}$')
        plt.ylabel('Exceedence Probability')
        plt.grid('both')
        plt.title(content)
    return thresh_array, exceedence

#exceedence curve variables
thresh_exced = pd.DataFrame(z)
x2, exced = exceedence(thresh_exced, 'swh')

#normal distribution variables
counts, start, dx, _ = cumfreq(z, numbins=100)
x = np.arange(counts.size) * dx + start


plt.plot(x, counts/len(z))
plt.scatter(x2, exced)
plt.xlabel('Significant Wave Height (m)')
plt.ylabel('Probability')








plt.plot(x2, exced)
plt.xlabel('Significant Wave Height (m)')
plt.ylabel('Probability')


# %% Residual Plot

stats.probplot(z, plot=sns.mpl.pyplot)
