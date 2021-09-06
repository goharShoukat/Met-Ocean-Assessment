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


def tables_monthly_summary(df, variable1, variable2, variable3, units, 
                           Coordinates, date_range, direc):
    #input
    #df : pd.DataFrame : df with all the columns intact, read from the cache file generated. 
    #variable1 : str : one of the variables found in the df
    #variable2 : str : one of the variables found in the df
    #variable3 : str : one of the variables found in the df
    #units : pd.DataFrame : df of units with columns as variable names
    #Coordinates : str : The coordinates for which this data is extracted
    #date_range : str : The date interval for which this data corresponds to
    #direc : str : directory to save the tables
    df['Date'] = pd.to_datetime(df['Date'])
    month_mean = pd.DataFrame()
    month_mean[variable1] = np.round(df.groupby([df['Date'].dt.month.rename('month')])[variable1].quantile(0.5), 2)
    month_mean[variable2] = np.round(df.groupby([df['Date'].dt.month.rename('month')])[variable2].quantile(0.5), 2)
    month_mean[variable3] = np.round(df.groupby([df['Date'].dt.month.rename('month')])[variable3].quantile(0.5), 2)
    
    
    month_min = pd.DataFrame()
    month_min[variable1] = np.round(df.groupby([df['Date'].dt.month.rename('month')])[variable1].quantile(0.05), 2)
    month_min[variable2] = np.round(df.groupby([df['Date'].dt.month.rename('month')])[variable2].quantile(0.05), 2)
    month_min[variable3] = np.round(df.groupby([df['Date'].dt.month.rename('month')])[variable3].quantile(0.05), 2)
    
    month_max = pd.DataFrame()
    month_max[variable1] = np.round(df.groupby([df['Date'].dt.month.rename('month')])[variable1].quantile(0.95), 2)
    month_max[variable2] = np.round(df.groupby([df['Date'].dt.month.rename('month')])[variable2].quantile(0.95), 2)
    month_max[variable3] = np.round(df.groupby([df['Date'].dt.month.rename('month')])[variable3].quantile(0.95), 2)
    
    
    
    months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month= np.array([months_list, month_mean[variable1], month_min[variable1], month_max[variable1], month_mean[variable2], month_min[variable2], month_max[variable2], month_mean[variable3], month_min[variable3], month_max[variable3]]).T
    
    
        
    
    
    fig, ax = plt.subplots(1,1,figsize=(60,60))
    table = ax.table(cellText=month, colLabels=['Months', '50th %', '5th %', '95th %', '50th %', '5th %', '95th %', '50th %', '5th %', '95th %'],loc='center', 
                      cellLoc='center')
    
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
    header[1].get_text().set_text("$\\bf{}$".format(variable1 + ' (' + units.loc[0, variable1] + ')'))
    
    header2 = [table.add_cell(-1,pos, w, h, loc="center", facecolor="none") for pos in [4,5, 6]]
    header2[0].visible_edges = "TBL"
    header2[1].visible_edges = "TB"
    header2[2].visible_edges = "TBR"
    header2[1].get_text().set_text("$\\bf{}$".format(variable2 + ' (' + units.loc[0, variable2] + ')'))
    
    
    header3 = [table.add_cell(-1,pos, w, h, loc="center", facecolor="none") for pos in [7,8, 9]]
    header3[0].visible_edges = "TBL"
    header3[1].visible_edges = "TB"
    header3[2].visible_edges = "TBR"
    header3[1].get_text().set_text("$\\bf{}$".format(variable3 + ' (' + units.loc[0, variable3] + ')'))
    plt.axis('off')
    plt.rcParams['axes.titley'] = .80   # y is in axes-relative coordinates.
    ax.set_title('rcParam y')
    ax.set_title('{}\nMonthly Percentiles: {}'.format(Coordinates, date_range))
    plt.tight_layout()
    plt.savefig(direc + 'summary_table_waves.pdf')
    plt.close()

def tables_yearly_summary_first_20(df, variable1, variable2, variable3, units, 
                          Coordinates, date_range, direc, key = False):
            #input
    #df : pd.DataFrame : df with all the columns intact, read from the cache file generated. 
  
    #so two seperate figures for years will be made of 20 years each
    #variable1 : str : one of the variables found in the df
    #variable2 : str : one of the variables found in the df
    #variable3 : str : one of the variables found in the df
    #units : pd.DataFrame : df of units with columns as variable names
    #Coordinates : str : The coordinates for which this data is extracted
    #date_range : str : The date interval for which this data corresponds to
    #direc : str : directory to save the tables
    #key : str/int : normally False but if 1 or 2, sets up multiple 
    
    yearly_mean = pd.DataFrame()
    yearly_mean[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.5), 2)[21:]
    yearly_mean[variable2] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable2].quantile(0.5), 2)[21:]
    yearly_mean[variable3] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable3].quantile(0.5), 2)[21:]
    
    
    yearly_min = pd.DataFrame()
    yearly_min[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.05), 2)[21:]
    yearly_min[variable2] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable2].quantile(0.05), 2)[21:]
    yearly_min[variable3] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable3].quantile(0.05), 2)[21:]
    
    yearly_max = pd.DataFrame()
    yearly_max[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.95), 2)[21:]
    yearly_max[variable2] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable2].quantile(0.95), 2)[21:]
    yearly_max[variable3] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable3].quantile(0.95), 2)[21:]
    
    
    yearly_list = np.array(np.linspace(2000, 2019, 20),dtype=object).astype(int)

    yearly= np.array([yearly_list, yearly_mean[variable1], yearly_min[variable1], yearly_max[variable1], yearly_mean[variable2], yearly_min[variable2], yearly_max[variable2], yearly_mean[variable3], yearly_min[variable3], yearly_max[variable3]],dtype=object).T
    
    
    
    
        
    fig, ax = plt.subplots(1,1,figsize = (60,60))
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
    header[1].get_text().set_text("$\\bf{}$".format(variable1 + ' (' + units.loc[0, variable1] + ')'))
    
    
    header2 = [table.add_cell(-1,pos, w, h, loc="center", facecolor="none") for pos in [4,5, 6]]
    header2[0].visible_edges = "TBL"
    header2[1].visible_edges = "TB"
    header2[2].visible_edges = "TBR"
    header2[1].get_text().set_text("$\\bf{}$".format(variable2 + ' (' + units.loc[0, variable2] + ')'))
    
    
    header3 = [table.add_cell(-1,pos, w, h, loc="center", facecolor="none") for pos in [7,8, 9]]
    header3[0].visible_edges = "TBL"
    header3[1].visible_edges = "TB"
    header3[2].visible_edges = "TBR"
    header3[1].get_text().set_text("$\\bf{}$".format(variable3 + ' (' + units.loc[0, variable3] + ')'))
    plt.axis('off')
    plt.rcParams['axes.titley'] = .9   # y is in axes-relative coordinates.
    ax.set_title('rcParam y')
    ax.set_title('{}\nYearly Percentiles: {}'.format(Coordinates, date_range))
    plt.tight_layout()
    plt.savefig(direc + 'summary_table_waves_1.pdf')
    plt.close()
    
def tables_yearly_summary_last_20(df, variable1, variable2, variable3, units, 
                          Coordinates, date_range, direc):
            #input
    #df : pd.DataFrame : df with all the columns intact, read from the cache file generated. 
    #so two seperate figures for years will be made of 20 years each
    #variable1 : str : one of the variables found in the df
    #variable2 : str : one of the variables found in the df
    #variable3 : str : one of the variables found in the df
    #units : pd.DataFrame : df of units with columns as variable names
    #Coordinates : str : The coordinates for which this data is extracted
    #date_range : str : The date interval for which this data corresponds to
    #direc : str : directory to save the tables

    
    yearly_mean = pd.DataFrame()
    yearly_mean[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.5), 2)[:20]
    yearly_mean[variable2] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable2].quantile(0.5), 2)[:20]
    yearly_mean[variable3] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable3].quantile(0.5), 2)[:20]
    
    
    yearly_min = pd.DataFrame()
    yearly_min[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.05), 2)[:20]
    yearly_min[variable2] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable2].quantile(0.05), 2)[:20]
    yearly_min[variable3] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable3].quantile(0.05), 2)[:20]
    
    yearly_max = pd.DataFrame()
    yearly_max[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.95), 2)[:20]
    yearly_max[variable2] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable2].quantile(0.95), 2)[:20]
    yearly_max[variable3] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable3].quantile(0.95), 2)[:20]
    
    
    yearly_list = np.array(np.linspace(1979, 1999, 20),dtype=object).astype(int)
    
    yearly= np.array([yearly_list, yearly_mean[variable1], yearly_min[variable1], yearly_max[variable1], yearly_mean[variable2], yearly_min[variable2], yearly_max[variable2], yearly_mean[variable3], yearly_min[variable3], yearly_max[variable3]],dtype=object).T
    
    
    
    
        
    fig, ax = plt.subplots(1,1,figsize = (60,60))
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
    header[1].get_text().set_text("$\\bf{}$".format(variable1 + ' (' + units.loc[0, variable1] + ')'))
    
    
    header2 = [table.add_cell(-1,pos, w, h, loc="center", facecolor="none") for pos in [4,5, 6]]
    header2[0].visible_edges = "TBL"
    header2[1].visible_edges = "TB"
    header2[2].visible_edges = "TBR"
    header2[1].get_text().set_text("$\\bf{}$".format(variable2 + ' (' + units.loc[0, variable2] + ')' ))
    
    
    header3 = [table.add_cell(-1,pos, w, h, loc="center", facecolor="none") for pos in [7,8, 9]]
    header3[0].visible_edges = "TBL"
    header3[1].visible_edges = "TB"
    header3[2].visible_edges = "TBR"
    header3[1].get_text().set_text("$\\bf{}$".format(variable3 + ' (' + units.loc[0, variable3] + ')'))
    plt.axis('off')
    plt.rcParams['axes.titley'] = .9   # y is in axes-relative coordinates.
    ax.set_title('rcParam y')
    ax.set_title('{}\nYearly Percentiles: {}'.format(Coordinates, date_range))
    plt.tight_layout()
    plt.savefig(direc + 'summary_table_waves_2.pdf')
    plt.close()
    
def tables_yearly_summary_lessthan_20(df, variable1, variable2, variable3, units, 
                          Coordinates, date_range, direc):
            #input
    #df : pd.DataFrame : df with all the columns intact, read from the cache file generated. 
    #so two seperate figures for years will be made of 20 years each
    #variable1 : str : one of the variables found in the df
    #variable2 : str : one of the variables found in the df
    #variable3 : str : one of the variables found in the df
    #units : pd.DataFrame : df of units with columns as variable names
    #Coordinates : str : The coordinates for which this data is extracted
    #date_range : str : The date interval for which this data corresponds to
    #direc : str : directory to save the tables

    
    yearly_mean = pd.DataFrame()
    yearly_mean[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.5), 2)
    yearly_mean[variable2] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable2].quantile(0.5), 2)
    yearly_mean[variable3] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable3].quantile(0.5), 2)
    
    
    yearly_min = pd.DataFrame()
    yearly_min[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.05), 2)
    yearly_min[variable2] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable2].quantile(0.05), 2)
    yearly_min[variable3] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable3].quantile(0.05), 2)
    
    yearly_max = pd.DataFrame()
    yearly_max[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.95), 2)
    yearly_max[variable2] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable2].quantile(0.95), 2)
    yearly_max[variable3] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable3].quantile(0.95), 2)
    
    
    yearly_list = np.array(np.arange(df.loc[0, 'Date'].year, df.loc[len(df)-1, 'Date'].year + 1, 1),dtype=object).astype(int)
    
    yearly= np.array([yearly_list, yearly_mean[variable1], yearly_min[variable1], yearly_max[variable1], yearly_mean[variable2], yearly_min[variable2], yearly_max[variable2], yearly_mean[variable3], yearly_min[variable3], yearly_max[variable3]],dtype=object).T
    
    
    
    
        
    fig, ax = plt.subplots(1,1,figsize = (60,60))
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
    header[1].get_text().set_text("$\\bf{}$".format(variable1 + ' (' + units.loc[0, variable1] + ')'))
    
    
    header2 = [table.add_cell(-1,pos, w, h, loc="center", facecolor="none") for pos in [4,5, 6]]
    header2[0].visible_edges = "TBL"
    header2[1].visible_edges = "TB"
    header2[2].visible_edges = "TBR"
    header2[1].get_text().set_text("$\\bf{}$".format(variable2 + ' (' + units.loc[0, variable2] + ')' ))
    
    
    header3 = [table.add_cell(-1,pos, w, h, loc="center", facecolor="none") for pos in [7,8, 9]]
    header3[0].visible_edges = "TBL"
    header3[1].visible_edges = "TB"
    header3[2].visible_edges = "TBR"
    header3[1].get_text().set_text("$\\bf{}$".format(variable3 + ' (' + units.loc[0, variable3] + ')'))
    plt.axis('off')
    plt.rcParams['axes.titley'] = .9   # y is in axes-relative coordinates.
    ax.set_title('rcParam y')
    ax.set_title('{}\nYearly Percentiles: {}'.format(Coordinates, date_range))
    plt.tight_layout()
    plt.savefig(direc + 'summary_table_waves_2.pdf')
    plt.close()
    

    
    
def tables_wind_monthly(df, variable1, units, Coordinates, date_range, direc):
    #input
    #df : pd.DataFrame : df with all the columns intact, read from the cache file generated. 
    #variable1 : str : one of the variables found in the df
    #variable2 : str : one of the variables found in the df
    #variable3 : str : one of the variables found in the df
    #units : pd.DataFrame : df of units with columns as variable names
    #Coordinates : str : The coordinates for which this data is extracted
    #date_range : str : The date interval for which this data corresponds to
    #direc : str : directory to save the tables
    df['Date'] = pd.to_datetime(df['Date'])
    month_mean = pd.DataFrame()
    month_mean[variable1] = np.round(df.groupby([df['Date'].dt.month.rename('month')])[variable1].quantile(0.5), 2)
    
    month_min = pd.DataFrame()
    month_min[variable1] = np.round(df.groupby([df['Date'].dt.month.rename('month')])[variable1].quantile(0.05), 2)
    
    month_max = pd.DataFrame()
    month_max[variable1] = np.round(df.groupby([df['Date'].dt.month.rename('month')])[variable1].quantile(0.95), 2)
    
    
    
    months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    month = np.array([months_list, month_mean[variable1], month_min[variable1], month_max[variable1]]).T
    
    
        
    
    
    fig, ax = plt.subplots(1,1,figsize=(60,60))
    table = ax.table(cellText=month, colLabels=['Months', '50th %', '5th %', '95th %', '50th %', '5th %', '95th %', '50th %', '5th %', '95th %'],loc='center', 
                      cellLoc='center')
    
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
    header[1].get_text().set_text("$\\bf{}$".format(variable1 + ' (' + units.loc[0, variable1] + ')'))
    
    plt.axis('off')
    plt.rcParams['axes.titley'] = .80   # y is in axes-relative coordinates.
    ax.set_title('rcParam y')
    ax.set_title('{}\nMonthly Percentiles: {}'.format(Coordinates, date_range))
    plt.tight_layout()
    plt.savefig(direc + 'summary_table_wind_monthly.pdf')
    plt.close()

def tables_wind_yearly_first_20(df, variable1, units, Coordinates, date_range, direc):
                #input
    #df : pd.DataFrame : df with all the columns intact, read from the cache file generated. 
  
    #so two seperate figures for years will be made of 20 years each
    #variable1 : str : one of the variables found in the df
    #variable2 : str : one of the variables found in the df
    #variable3 : str : one of the variables found in the df
    #units : pd.DataFrame : df of units with columns as variable names
    #Coordinates : str : The coordinates for which this data is extracted
    #date_range : str : The date interval for which this data corresponds to
    #direc : str : directory to save the tables

    
    yearly_mean = pd.DataFrame()
    yearly_mean[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.5), 2)[21:]
    
    
    yearly_min = pd.DataFrame()
    yearly_min[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.05), 2)[21:]
    
    yearly_max = pd.DataFrame()
    yearly_max[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.95), 2)[21:]
   
    
    yearly_list = np.array(np.linspace(2000, 2019, 20),dtype=object).astype(int)

    yearly= np.array([yearly_list, yearly_mean[variable1], yearly_min[variable1], yearly_max[variable1]],dtype=object).T
    
    
    
    
        
    fig, ax = plt.subplots(1,1,figsize = (60,60))
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
    header[1].get_text().set_text("$\\bf{}$".format(variable1 + ' (' + units.loc[0, variable1] + ')'))
    
    
    plt.axis('off')
    plt.rcParams['axes.titley'] = .9   # y is in axes-relative coordinates.
    ax.set_title('rcParam y')
    ax.set_title('{}\nYearly Percentiles: {}'.format(Coordinates, date_range))
    plt.tight_layout()
    plt.savefig(direc + 'summary_table_wind_yearly1.pdf')
    plt.close()
    
def tables_wind_yearly_last_20(df, variable1, units, Coordinates, date_range, direc):

            #input
    #df : pd.DataFrame : df with all the columns intact, read from the cache file generated. 
    #so two seperate figures for years will be made of 20 years each
    #variable1 : str : one of the variables found in the df
    #variable2 : str : one of the variables found in the df
    #variable3 : str : one of the variables found in the df
    #units : pd.DataFrame : df of units with columns as variable names
    #Coordinates : str : The coordinates for which this data is extracted
    #date_range : str : The date interval for which this data corresponds to
    #direc : str : directory to save the tables

    
    yearly_mean = pd.DataFrame()
    yearly_mean[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.5), 2)[:20]
     
    
    yearly_min = pd.DataFrame()
    yearly_min[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.05), 2)[:20]
    
    yearly_max = pd.DataFrame()
    yearly_max[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.95), 2)[:20]
    
    
    yearly_list = np.array(np.linspace(1979, 1999, 20),dtype=object).astype(int)
    
    yearly= np.array([yearly_list, yearly_mean[variable1], yearly_min[variable1], yearly_max[variable1]], dtype=object).T
    
    
    
    
        
    fig, ax = plt.subplots(1,1,figsize = (60,60))
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
    header[1].get_text().set_text("$\\bf{}$".format(variable1 + ' (' + units.loc[0, variable1] + ')'))
    plt.axis('off')
    plt.rcParams['axes.titley'] = .9   # y is in axes-relative coordinates.
    ax.set_title('rcParam y')
    ax.set_title('{}\nYearly Percentiles: {}'.format(Coordinates, date_range))
    plt.tight_layout()
    plt.savefig(direc + 'summary_table_wind_yearly2.pdf')
    #plt.close()
     
def tables_wind_yearly_lessthan_20(df, variable1, units, Coordinates, date_range, direc):
                #input
    #df : pd.DataFrame : df with all the columns intact, read from the cache file generated. 
  
    #so two seperate figures for years will be made of 20 years each
    #variable1 : str : one of the variables found in the df
    #variable2 : str : one of the variables found in the df
    #variable3 : str : one of the variables found in the df
    #units : pd.DataFrame : df of units with columns as variable names
    #Coordinates : str : The coordinates for which this data is extracted
    #date_range : str : The date interval for which this data corresponds to
    #direc : str : directory to save the tables

    
    yearly_mean = pd.DataFrame()
    yearly_mean[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.5), 2)
    
    
    yearly_min = pd.DataFrame()
    yearly_min[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.05), 2)
    
    yearly_max = pd.DataFrame()
    yearly_max[variable1] = np.round(df.groupby([df['Date'].dt.year.rename('yearly')])[variable1].quantile(0.95), 2)
   
    
    yearly_list = np.array(np.arange(df.loc[0, 'Date'].year, df.loc[len(df)-1, 'Date'].year + 1, 1),dtype=object).astype(int)
    
    yearly= np.array([yearly_list, yearly_mean[variable1], yearly_min[variable1], yearly_max[variable1]],dtype=object).T
    
    
    
    
        
    fig, ax = plt.subplots(1,1,figsize = (60,60))
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
    header[1].get_text().set_text("$\\bf{}$".format(variable1 + ' (' + units.loc[0, variable1] + ')'))
    
    
    plt.axis('off')
    plt.rcParams['axes.titley'] = .9   # y is in axes-relative coordinates.
    ax.set_title('rcParam y')
    ax.set_title('{}\nYearly Percentiles: {}'.format(Coordinates, date_range))
    plt.tight_layout()
    plt.savefig(direc + 'summary_table_wind_yearly_.pdf')
    plt.close()
    
