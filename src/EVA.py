#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 23:36:26 2021

@author: goharshoukat

script to perform extreme value analysis

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scikit.skextremes as ske

def EVA(df, variable, Coordinates, date_range, direc):
    #inputs
    #df : pd.DataFrame : the entire dataframe as it is passed through from the run_code script
    #variable: str : x variable name for the EVA. like swh
    #Coordinates : str : The coordinates for which this data is extracted
    #date_range : str : The date interval for which this data corresponds to
    #title : str : title of the plot e.g. mwp vs swh
    #direc : str : output directory entered by user
    sorted_ = np.sort(df[variable])
    #select top 30 events
    top_20 = sorted_[-20:]
        
    model = ske.models.classic.GEV(top_20, fit_method = 'mle', ci = 0.05,
                                  ci_method = 'delta')
    model.plot_summary()
    plt.show()
    plt.savefig(direc + variable + ' summary_EVA.pdf')
    plt.close()
    
    model.plot_return_values()
    plt.title('{}\n{} Return Values: {}'.format(Coordinates, variable, date_range))
    plt.show()
    plt.savefig(direc + variable + ' return_values.pdf')

    plt.close()
    
    model.plot_qq()
    plt.title('{}\n{} QQ Plot: {}'.format(Coordinates, variable, date_range))
    plt.show()
    plt.savefig(direc + variable + ' qq.pdf')
    plt.close()
    
    
    model.plot_pp()
    plt.title('{}\n{} PP Plot: {}'.format(Coordinates, variable, date_range))
    plt.show()
    plt.savefig(direc + variable + ' pp.pdf')
    plt.close()
    
    
    model.plot_density()
    plt.title('{}\n{} Density Plot: {}'.format(Coordinates, variable, date_range))
    plt.show()
    plt.savefig(direc + variable + ' plot_density.pdf')
    plt.close()
    

    '''

direc = 'results/'
df = pd.read_csv(direc + '09_06-12_12_PM.csv', index_col = False)
df['Date'] = pd.to_datetime(df["Date"])


sorted_ = np.sort(df['swh (m)'])#sort the array
#select the top 30 maximum events
top_30 = sorted_[-25:]

model = ske.models.classic.GEV(top_30, fit_method = 'mle', ci = 0.05,
                              ci_method = 'delta')


 model.plot_summary()


plt.show()


x = model.plot_return_values()
plt.title('try')
'''