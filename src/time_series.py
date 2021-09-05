
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from matplotlib.ticker import MaxNLocator, MultipleLocator
import cartopy as ct



def time_series_plot(df, variable, Coordinates, unit, plot_direc):
    #inputs
    #df : pd.DataFrame : the entire dataframe as it is passed through from the run_code script
    #x_variable: str : x variable name for the heatmap. like mwp
    #y_variable: ndarray : input array like swh
    #the titles are used in plotting
    
    #Coordinates : str : The coordinates for which this data is extracted
    #date_range : str : The date interval for which this data corresponds to
    #units : pd.DataFrame : df of units with columns as variable names
    #plot_direc : str : output directory entered by user
    #output:
     
    
    df['new_date']= df['Date'].dt.strftime('%Y-%m-%d')
    availability = 100 - df[variable].isnull().sum()/len(df) * 100 
    left = min(df['Date'])
    right = max((df['Date']))
    
    
    fig, ax = plt.subplots(figsize=(60,60))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("\n%Y"))
    loc = MultipleLocator(base=1.0)
    ax.yaxis.set_major_locator(loc)
    plt.setp(ax.get_xticklabels())
    plt.gca().xaxis.set_tick_params(rotation = 90)
    
    ax.set(xlabel="Year",
           ylabel=variable + ' (' + unit + ')',
           title = '{}\n{} Time Series: ({} - {})'.format(Coordinates, variable, df['new_date'][0], df.iloc[-1]['new_date']) , xlim=[left , right])
    ax.tick_params(direction = 'in', length=6, width=1.2, grid_alpha=0.5, bottom = True, top = True, left = True, right =True)
    ax.plot(df['Date'], df[variable], linewidth=.3)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*0.95, box.height])
    ax.grid(b = True, which = 'both', linestyle= '--')
    
    
    #plt.text(0.5, 0.5, 'matplotlib', ha='right', va='top', transform=ax.transAxes)
    plt.text(0.87, 0.87, 'Average \n{:.2f}'.format(np.mean(df[variable])), fontsize=9, transform=plt.gcf().transFigure)
    plt.text(0.93, 0.87, 'Availibility \n{:.2f}'.format(availability), fontsize=9, transform=plt.gcf().transFigure)
    
    plt.text(0.87, 0.80, 'Minimum \n{:.2f}'.format(np.min(df[variable])), fontsize=9, transform=plt.gcf().transFigure)
    plt.text(0.93, 0.80, 'Maximum \n{:.2f}'.format(np.max(df[variable])), fontsize=9, transform=plt.gcf().transFigure)
    plt.text(0.87, 0.73, 'Std \n{:.2f}'.format(np.std(df[variable])), fontsize=9, transform=plt.gcf().transFigure)
    plt.savefig(plot_direc + '{} Time Series.pdf'.format(variable))

'''


direc = 'results/'
df = pd.read_csv(direc + '09_05-11_14_AM.csv', index_col = False)


#hold latitude and longitude units seperately and rename them for ease of handling
unit_latitude = list(df.columns[df.columns == 'latitude (degrees_north)'].str.split())[0][1]
unit_longitude = list(df.columns[df.columns == 'longitude (degrees_east)'].str.split())[0][1]
df = df.rename(columns = {'latitude (degrees_north)' : 'latitude', 'longitude (degrees_east)' : 'longitude'})

df['Date'] = pd.to_datetime(df['Date'])
#strip the time from the date column
df['new_date']= df['Date'].dt.strftime('%Y-%m-%d')
availability = 100 - df['swh (m)'].isnull().sum()/len(df) * 100 
left = min(df['Date'])
right = max((df['Date']))


fig, ax = plt.subplots(figsize=(60,60))
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("\n%Y"))
loc = MultipleLocator(base=1.0)
ax.yaxis.set_major_locator(loc)
plt.setp(ax.get_xticklabels())
plt.gca().xaxis.set_tick_params(rotation = 90)

ax.set(xlabel="Year",
       ylabel=df.columns[4],
       title = '{} $^\circ$N, {} $^\circ$E \n Time Series: ({} - {})'.format(df['latitude'][0], df['longitude'][0],df['new_date'][0], df.iloc[-1]['new_date']) , xlim=[left , right])
ax.tick_params(direction = 'in', length=6, width=1.2, grid_alpha=0.5, bottom = True, top = True, left = True, right =True)
ax.plot(df['Date'], df['swh (m)'], linewidth=.3)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width*0.95, box.height])
ax.grid(b = True, which = 'both', linestyle= '--')


#plt.text(0.5, 0.5, 'matplotlib', ha='right', va='top', transform=ax.transAxes)
plt.text(0.87, 0.87, 'Average \n{:.2f}'.format(np.mean(df['swh (m)'])), fontsize=9, transform=plt.gcf().transFigure)
plt.text(0.93, 0.87, 'Availibility \n{:.2f}'.format(availability), fontsize=9, transform=plt.gcf().transFigure)

plt.text(0.87, 0.80, 'Minimum \n{:.2f}'.format(np.min(df['swh (m)'])), fontsize=9, transform=plt.gcf().transFigure)
plt.text(0.93, 0.80, 'Maximum \n{:.2f}'.format(np.max(df['swh (m)'])), fontsize=9, transform=plt.gcf().transFigure)
plt.text(0.87, 0.73, 'Std \n{:.2f}'.format(np.std(df['swh (m)'])), fontsize=9, transform=plt.gcf().transFigure)
plt.savefig('Plots/Time Series.png', dpi = 300)


'''