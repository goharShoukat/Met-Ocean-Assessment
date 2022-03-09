# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

################################################################################
#************************* INFORMATION *****************************************
################################################################################

File name: WeatherWindows_v1.0

Version: 1.0

Date of release: 23.08.2021.

Created by:
    Name: Bepo Schira
    Email: bschira@gdgeo.com
    Date: 23.08.2021.
    
Checked by:
    Name: Helena Kustura
    Email: hkustura@gdgeo.com
    Date:

Approved by:
    Name:
    Email:
    Date:
        
Purpose:
    This script is used to estimate the Non-Exceedance and Persistence below
    (associated with workability) and Exceedance and Non-Persistance below (associated)
    with weather downtime (WDT) based on hindcast hourly data (the more years
    of hindcast data is available, the more accurate will the estimates be). It is
    advised to have at least 30 years of hourly hindcast data available.
    The script automatically writes the P-values in excel and the following
    charts can be plotted (if the user activates the option):
        1. PlottingYears - Plots Non-Exceedance and Persistence below for every year
        and yearly P-values for Non-Exceedance, Exceedance, Persistence below and Non-Persistence below
        2. PlottingAllMonthsAllYears - Plots Non-Exceedance and Persistence below for every month
        through all years, i.e. Non-Exceedance for January when Januaries for all years are considered
        3. PlottingAllMonthsEveryYear - Plots Non-Exceedance and Persistence below (+ reference periods)
        for every month and all years, e.g. January values for every year available
        4. PlottingMonthlyPvals - Plots P-values for Non-Exceedance and Persistence below
        (+ reference periods) for every month and all years, e.g. January values for every year available
    The following excel files are automatically created with P-values:
        1. 01_P-values for each year and TR_percentages - gives YEARLY P-values of Non-Exceedance,
        Exceedance, Persistence below and Non-Persistence below based on the statistics
        of all years
        2. 02_Every month all years_percentages - gives MONTHLY percentages of
        Non-Exceedance, Exceedance, Persistence below and Non-Persistence below
        for every month by considering the monthly values of all years, e.g.
        the data for all available Januaries is used to get the percentage
        for January (not P-values)
        3. 03_Monthly P-values_percentages - gives the MONTHLY P-values of
        Non-Exceedance, Exceedance, Persistence below and Non-Persistence below
        for every month by considering the monthly value of each year, i.e.
        for each month the ECDF curve is plotted based on the values of every
        year (more than 30 years necessary) from which the user-defined P-values 
        are found
    Warning! The data has to be provided in the .txt file in the specified order.
   
Changes since last release:
    1.


Notes: 
    The term "treshold" is used to describe the limiting value of a
metoecan parameter defined by operational limit. Of interest can be
the percentage of time the weather is below (installation phase) or 
above the treshold values (e.g. in wind farm operational phase).

    The term "workability" is here used for percentage of time that the 
weather parameters are below limit, which is related to the wave 
scatter diagram method described in [2] and usually used as a first 
estimation of WDT and for continuous operations. This would be the result 
of jointed criteria evaluation at each time step. 

    All the plots and data is by default "overlapping", unless stated otherwise.

    The following terminology needs to be distinguished [1]:

- EXCEEDENCE is the % of time above a given threshold irrespective of 
window duration. It represents the weather downtime in offshore operations, 
which implies a negative conotation. However, in case of estimating the 
performance of a wind turbine, this would have a positive conotation as in this
case the more time the wind is above a certain treshold, the more electricity
will be generated (noting that the turbine will not work above a certain wind
speed, the cut-out speed)

- NON-EXCEEDENCE is the % of time below a given threshold irrespective of 
window duration. In offshore construction this has usually a positive conotation
and represents the workability of the vessel, i.e. the percentage of time that
the weather is favourable for construction works

The sum of exceedence and non-exceedence always equals 100%.

- WEATHER WINDOW - a period of exceedence or non-exceedence that persists 
for at least a given time duration (this termed also reference period)

- PERSISTENCE is the % of all time that a threshold limit is exceeded 
(or less commonly not-exceeded) for at least a minimum (window) duration, 
i.e. the weather windows.

- NON-PERSISTENCE is the % of all time outside of the weather windows.

The sum of persistence and non- persistence always equals 100%, but the 
sum of persistence-below and persistence-above a threshold for a given 
weather window duration may not necessarily equal 100%. See also [8]

Based on above definitions, the non-exceedence and persistence below (a threshold) 
are related to workability, while the exceedance and non-persistence below are 
related with weather downtime.

The script uses the overlapping values for weather downtime, but the windows
are hourly based, not daily (as used sometimes).

It is assumed that the time step in the hindcast data is 1hr, the script
should work with other values but is not tested and is in general recommended
to use 1hr (see e.g. [1]). If data for some metocean parameters are given
in another time step (e.g. current speed every 10min, 30min etc.) it should
be transferred into 1hr time step, or the same time step for all the data.

When the reference period (minimum time that all the metocean parameters
of interest have to be above/below certain limits) is used for weather 
window statistics, only the time when the weather is above/below a specified
limit for at least the duration of the reference period is counted.
Sometimes, if there is an interruption in the sequence even for one time step
these conditions are violated. For example, let assume a reference period
of 4hrs and a weather time series where Hs is below the limit of 1.5m for 
12hrs continuously, then interrupted by 1hr where Hs is above 1.5m and then#
continuosly below 1.5m for 3hrs. Here, the script would give only one weather
window of 12hrs, but in practice the above 1.5m for 1hr can be very close
to the limit (say 1.6m) that the operations would continue, which would
imply a 16hr window, rather than 12hr. In [9] the authors assumed that the 
work continued when the exceedance time was less than 20 minutes. 


List of abbreviations:
    WDT - Weather downtime
    ECDF - Empirical cummulative distribution function
    Hs - Significant wave height
    NEYS - Non-Exceedance Years Sorted
    PBYS - Persistence below years sorted

################################################################################

References
[1] Lambkin, D., Wade, I. and Stephens, R. (2019): Estimating Operational
Weather Downtime: A Comparison of Analytical Methods, Proceedings of the ASME 2019 38th International
Conference on Ocean, Offshore and Arctic Engineering, June 9-14, 2019, Glasgow, Scotland, UK
OMAE2019-95367

[2] van der Wal, R. J. and de Boer, G. (2004): Downtime Analysis Techniques
for Complex Offshore and Dredging Operations, 23rd International Conference on Offshore Mechanics 
and Arctic Engineering, 23rd International Conference on Offshore Mechanics and Arctic Engineering

[3] Rip, J. (2015): Probabilistic downtime analysis for complex marine projects: A state-of-the-art model based on Markov theory to generate
binary workability sequences for sequential operations, MSc thesis, TU Delft

[4] Leontaris, G. (2015): Design of a probabilistic decision support tool for the
cable installation of an Offshore Wind Farm, MSc thesis, TU Delft

[5] Kikuchi, Y. and Ishihara, T. (2016): Assessment of weather downtime for the construction of
offshore wind farm by using wind and wave simulations, Journal of Physics: Conference Series 753 (2016) 092016,
doi:10.1088/1742-6596/753/9/092016

[6] Springett, C. N. (1977): A Method For Predicting Weather Downtime For Semisubmersibles,
Journal Of Petroleum Technology

[7] Clades, A. K. (2018): Developing a Method To Assess the Workability of a Heavy Lifting Operation, 
MSc thesis, TU Delft

[8] Graham, C. (1982): THE PARAMETERISATION AND PREDICTION OF WAVE HEIGHT
AND WIND SPEED PERSISTENCE STATISTICS FOR OIL INDUSTRY OPERATIONAL 
PLANNING PURPOSES, Coastal Engineering, 6 (1982) 303--329

[9] Kikuchi, Y. and Ishihara, T. (2016): Assessment of weather downtime 
for the construction of offshore wind farm by using wind and wave 
simulations, J. Phys.: Conf. Ser. 753 092016

"""

def WeatherWindows(WindSpeedLimit, WaveHeightLimit, CurrentSpeedLimit, PeakPeriodLimit, ReferencePeriods, Pvalues, Plot, UseFullYears, dataPath, outputPath):
    
    ################################################################################
    #******************* IMPORT PYTHON MODULES *************************************
    ################################################################################
    
    import numpy as np              # numpy as a math package 
    import time                     # time module to get the calculation time
    import matplotlib.pyplot as plt # plotting module 
    import pandas as pd
    import xlsxwriter
    import os
    import shutil
    #from scipy import stats
    #ReferencePeriods : list of int : User defined, >1
    #Pvalues : list of floats : 0 < x < 100
    #Plot : Bool : 
    #usefullyears : Bool : 1 for whole years
    ################################################################################
    #*********************** USER INPUT ********************************************
    ################################################################################
    
    start0 = time.time()
    # data given as: 0 Year/1 Month/2 Day/3 Hour/4 Wind Speed (m/s)
    # 5 Significant Wave Height (m)/6 Wave Period (sec)/7 Current speed (m/s)
    # hindcast data based on 1hr samples
    
    # Load hindcast data from .txt file
    data = np.loadtxt(dataPath, delimiter=',')
    
    # # Operational weather limits
    # WindSpeedLimit = 15        # m/s
    # WaveHeightLimit = 1.5      # m
    # CurrentSpeedLimit = 10     # m/s
    # PeakPeriodLimit = 100.0    # s, to exclude the limit put say 100
    # ReferencePeriods = [16]    # hrs, integers without "1" as it is available by default
    
    UseFullYears = UseFullYears             # "0" for using the whole data (even if in the last year
    # the data is incomplete), "1" to use only the years with data for every month (it will
    # exclude the data of last year if it is incomplete)
    
    # INPUT FOR PLOTTING
    PlottingYears = Plot           # Plots Non-Exceedance and Persistence below for every year
    #  and yearly P-values for Non-Exceedance, Exceedance, Persistence below and Non-Persistence below
    
    PlottingAllMonthsAllYears = Plot  # Plots Non-Exceedance and Persistence below for every month
    # through all years, i.e. Non-Exceedance for January when Januaries for all years are considered
    
    PlottingAllMonthsEveryYear = Plot  # Plots Non-Exceedance and Persistence below (+ reference periods)
    # for every month and all years, e.g. January values for every year available
    
    PlottingMonthlyPvals = Plot    # Plots P-values for Non-Exceedance and Persistence below 
    # (+ reference periods) for every month and all years, e.g. January values for every year available
    
    # Pvalues = [0,10,20,50,80,90,100]  # Will give the results of ECDF at defined P-values
    
    # Name of the months for plotting
    NameMonths = ['January','February','March','April','May','June','July','August','September','October','November','December']
    
    ################################################################################
    #*********************** PRE-CALCULATION ***************************************
    ################################################################################
    
    NumberOfLimits = 4          # number of metoecan parameters set as limit
    TSEval = NumberOfLimits + 1 # number of evaluations (individual limits plus jointed)
    
    # Evaluation matrix to check if each individual limit/criteria and jointed
    # criteria has been satisfied or not.  % of time below a given threshold 
    # irrespective of window duration
    NonExceedance = np.zeros([data.shape[0],TSEval]) # +4 for wind speed, Hs, current and Tp
    
    # List of years, indices of years and number of rows for each year (note that
    # there will be a difference every leap year and if simulation was not
    # done for all months in a year)
    Years, IndicesYears, CountsYears = np.unique(data[:,0], return_inverse=True, return_counts=True)
    NumberOfYears = len(Years)
    
    # Array of months, indices of months and number of rows (data) for each
    # month in the given hindcast period, e.g. 38 years
    Months, IndicesMonths, CountsMonths = np.unique(data[:,1], return_inverse=True, return_counts=True)
    NumberOfMonths = len(Months)
    TimeStep = data[1,3]-data[0,3]
    # print(f'Time step in hindcast time series is: {TimeStep} hrs')
    
    ################################################################################
    #*********************** OUTPUT DIRECTORIES ************************************
    ################################################################################
    
    # Get the location of current directory
    current_directory = outputPath #os.getcwd()
    
    # Define Output directory
    output_directory = os.path.join(current_directory, r'Output_WW')
    
    # Define subfolders
    figures_directory = os.path.join(current_directory, r'Output_WW', r'Figures')
    tables_directory = os.path.join(current_directory, r'Output_WW', r'Tables')
    
    # If Output directory exists, delete it and all its content
    if os.path.exists(output_directory) and os.path.isdir(output_directory):
        shutil.rmtree(output_directory, ignore_errors=True)
    
    
    # If Output directory does not exist, create it and subfolders
    if not os.path.exists(output_directory):
       os.makedirs(figures_directory)
       os.makedirs(tables_directory)
    
    
    ################################################################################
    #*********************** EVALUATION OF CRITERIA ********************************
    ################################################################################
    
    # Non-exceedance, i.e. % of time below a given threshold irrespective of 
    # window duration 
    for i in range (0,data.shape[0]):
        # Check the wind speed criteria
        if data[i,4] <= WindSpeedLimit:
            NonExceedance[i,0] = 1
        else:
            NonExceedance[i,0] = 0
        # Check the significant wave height criteria
        if data[i,5] <= WaveHeightLimit:
            NonExceedance[i,1] = 1
        else:
            NonExceedance[i,1] = 0
        # Check the peak period criteria
        if data[i,6] <= PeakPeriodLimit:
            NonExceedance[i,2] = 1
        else:
            NonExceedance[i,2] = 0
        # Check the sea current speed criteria
        if data[i,7] <= CurrentSpeedLimit:
            NonExceedance[i,3] = 1
        else:
            NonExceedance[i,3] = 0
        # Joint evaluation of all parameters: 1 if all are ok, 0 if not   
        SumEva = NonExceedance[i,0] + NonExceedance[i,1] + NonExceedance[i,2] + NonExceedance[i,3]
        if SumEva == 4: # 4 as number of parameters being evaluated
            NonExceedance[i,4] = 1
        else:
            NonExceedance[i,4] = 0
    
    # Weather window statistics for different reference periods
    # Persistence as the % of all time that a threshold limit is not exceeded
    # for at least a minimum (window) duration
    PersistenceBelow = np.zeros([data.shape[0],len(ReferencePeriods)])
    PersistenceBelowNO = np.zeros([data.shape[0],len(ReferencePeriods)])   # non-overlapping
    
    # Indices of where there is a change of "0" and "1" in the joint evaluation
    # of the NonExceedance matrix (last column)
    NonExceedanceChangeIndex = np.where(NonExceedance[:,-1][:-1] != NonExceedance[:,-1][1:])[0]
    # Adding first and last indice
    NonExceedanceChangeIndex = np.hstack((0,NonExceedanceChangeIndex,data.shape[0]))
    
    # Filtering periods by discarding those shorter than the weather window 
    # duration (reference periods) being assessed.
    for i in range(0,len(ReferencePeriods)):
        for j in range(0,len(NonExceedanceChangeIndex)-1):
            # A1 is used to start the counting from n+1 row, where n is the
            # last number of row considered in the previous loop, e.g. sums
            # are considered for index 0-22, 23-50, instead of 0-22, 22-50 which
            # would be wrong as the last row would be overwritten in the next loop
            if j==0:
                A1 = 0
            else:
                A1 = 1
            SumNE = np.sum(NonExceedance[NonExceedanceChangeIndex[j]+A1:NonExceedanceChangeIndex[j+1]+1,-1])
            # Relative index (local) for non-overlapping periods
            NOI = int(SumNE-np.floor(SumNE/ReferencePeriods[i])*ReferencePeriods[i])
            # Check if the duration is at least as the duration of reference period
            if SumNE >= ReferencePeriods[i]: 
                PersistenceBelow[NonExceedanceChangeIndex[j]+A1:NonExceedanceChangeIndex[j+1]+1,i] = 1
                PersistenceBelowNO[NonExceedanceChangeIndex[j]+A1:NonExceedanceChangeIndex[j+1]+1-NOI,i] = 1
            else:
                PersistenceBelow[NonExceedanceChangeIndex[j]+A1:NonExceedanceChangeIndex[j+1]+1,i] = 0
            # Check the code
            # if j < 10:
            #     print(i,j,NonExceedanceChangeIndex[j]+A1,NonExceedanceChangeIndex[j+1]+1)
    
    #np.savetxt('Persistence.txt', Persistence, delimiter=',', fmt='%1.5f')
    #timeit 'SomeOperation' # measuring the time necessary to carry on a computation
    
    ################################################################################
    #*********************** YEARLY STATISTICS *************************************
    ################################################################################
    
    # Check where the rows in first column change year
    YearsChangeIndex = np.where(data[:,0][:-1] != data[:,0][1:])[0]
    # Add first and last index to the array
    YearsChangeIndex = np.hstack((0,YearsChangeIndex,data.shape[0]))
    
    if UseFullYears == 1:
        NOY = NumberOfYears
        # Empty matrix for NonExceedance results
        NonExceedanceYears = np.zeros(NOY)
        # Empty matrix for workability results in each year
        PersistenceBelowYears = np.zeros([NOY,len(ReferencePeriods)])
        YearsP = Years
    else:
        NOY = NumberOfYears-1
        # Empty matrix for NonExceedance results
        NonExceedanceYears = np.zeros(NOY)
        # NumberOfYears-1 to remove last uncompleted year (not all months 
        # available)
        # Empty matrix for workability results in each year
        PersistenceBelowYears = np.zeros([NOY,len(ReferencePeriods)])
        YearsP = Years[:-1]
    
    ExceedancePlot = NonExceedanceYears+1
    
    PersistenceBelowOnes = PersistenceBelowYears+1
    
    for i in range(0,NOY):
        # Data length in each year
        if i == 0:
            YearSize = (YearsChangeIndex[i+1]-YearsChangeIndex[i])+1 
        else:
            YearSize = (YearsChangeIndex[i+1]-YearsChangeIndex[i])
        # Sum of all workable times in each year
        NonExceedanceSum = np.sum(NonExceedance[YearsChangeIndex[i]:YearsChangeIndex[i+1]+1,-1],axis=0) 
        # Non-Exceedance for each year
        NonExceedanceYears[i] = NonExceedanceSum/YearSize
        for j in range(0,len(ReferencePeriods)):
            # Sum of all workable times in each year
            PersistenceBelowSum = np.sum(PersistenceBelow[YearsChangeIndex[i]:YearsChangeIndex[i+1]+1,j],axis=0)
            # Persistence (below) - proportion of time that meets the required 
            # criteria (above/below the limit(s) for at least the weather window
            PersistenceBelowYears[i,j] = PersistenceBelowSum/YearSize
            #print(YearSize,WorkabilitySum)
                
    
    #**************** ECDF Non-Exceedance of each year ****************************
    
    # Sorting the values for each year into rank order (smallest to largest) 
    # and assigning a probability of non-exceedence
    NonExceedanceYearsSorted = np.zeros([len(NonExceedanceYears),2])
    NonExceedanceYearsSorted[:,0] = np.sort(NonExceedanceYears, axis=0)
    NonExceedanceYearsSorted[:,-1] = np.arange(1,NOY+1,1)/NOY
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    PvalsNEYS = np.linspace(0, 1, 101) # step of 0.01 in order to get the PXX (e.g. P50) values
    xinterpNEYS = np.interp(PvalsNEYS, NonExceedanceYearsSorted[:,-1], NonExceedanceYearsSorted[:,0])
    xinterpNEYSP = np.zeros(len(Pvalues))
    
    # Printing the P-values
    # P0 = minimum %, P100 = maximum %
    for i in range(0,len(Pvalues)):
        xinterpNEYSP[i] = 100*xinterpNEYS[Pvalues[i]] 
        # as PvalsNEYS is divided in 100 (step 0.01 or 1%) the P50 will be the 50eth number in the array
        #print(f'P{Pvalues[i]} value for Non-Exceedance (all years) is: {round(100*xinterpNEYS[Pvalues[i]],2)}%')
    
    
    # np.savetxt('NonExceedanceYearsSorted.txt', NonExceedanceYearsSorted, delimiter=',', fmt='%1.5f')
    # np.savetxt('ExceedanceYearsSorted.txt', ExceedanceYearsSorted, delimiter=',', fmt='%1.5f')
    # np.savetxt('xinterpNEYS.txt', xinterpNEYS, delimiter=',', fmt='%1.5f')
    
    #**************** ECDF Exceedance of each year ********************************
    
    # Sorting the values for each year into rank order (smallest to largest) 
    # and assigning a probability of non-exceedence
    ExceedanceYearsSorted = np.zeros([len(NonExceedanceYears),2])
    ExceedanceYearsSorted[:,0] = np.sort(1.0-NonExceedanceYears, axis=0)
    ExceedanceYearsSorted[:,-1] = np.arange(1,NOY+1,1)/NOY
    
    """
    Below would be the full step way to calculate the P-values for Exceedance.
    However, due to limited data points and interpolation, there would be a slight
    difference betweent he Exceedance (E) and Non-Exceedance (NE) P-values. The E 
    and NE P-values should sum up to 100% for PX and P(100-X) for E and NE values
    respectively. Small difference can be present and the sum might become slightly
    off 100% (observations showed < 1% difference). Therefore, it was decided to 
    drop off the interpolation and calculate interpolated values from NE values.
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    PvalsEYS = np.linspace(0, 1, 101)
    xinterpEYS = np.interp(PvalsEYS, ExceedanceYearsSorted[:,-1], ExceedanceYearsSorted[:,0])
    xinterpEYSP = np.zeros(len(Pvalues))
    """
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    PvalsEYS = np.linspace(0, 1, 101)
    xinterpEYS = np.sort(1.0-xinterpNEYS)
    xinterpEYSP = np.zeros(len(Pvalues))
    
    # Printing the P-values
    # P0 = minimum %, P100 = maximum %
    for i in range(0,len(Pvalues)):
        xinterpEYSP[i] = 100*xinterpEYS[Pvalues[i]]
    
    
    #**************** ECDF Persistence of each year *******************************
    
    # Sorting the values for each year into rank order (smallest to largest) 
    # and assigning a probability of non-exceedence
    PersistenceBelowYearsSorted = np.zeros([PersistenceBelowYears.shape[0],PersistenceBelowYears.shape[1]+1])
    PersistenceBelowYearsSorted[:,:-1] = np.sort(PersistenceBelowYears, axis=0)
    PersistenceBelowYearsSorted[:,-1] = np.arange(1,NOY+1,1)/NOY
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    xinterpPBYS = np.zeros([len(PvalsNEYS),len(ReferencePeriods)])
    xinterpPBYSP = np.zeros([len(Pvalues),len(ReferencePeriods)])
    for i in range(0,len(ReferencePeriods)):
        xinterpPBYS[:,i] = np.interp(PvalsNEYS, PersistenceBelowYearsSorted[:,-1], PersistenceBelowYearsSorted[:,i])
        # Printing the P-values
        # P0 = minimum %, P100 = maximum %
        for j in range(0,len(Pvalues)):
            xinterpPBYSP[j,i] = 100*xinterpPBYS[Pvalues[j],i]
            #print(f'P{Pvalues[j]} value for Persistence (below) and reference period {ReferencePeriods[i]}hrs is: {round(100*xinterpPBYS[Pvalues[j],i],2)}%')
    
    #**************** ECDF Non-Persistence of each year (WDT) ***************************
    
    # Sorting the values for each year into rank order (smallest to largest) 
    # and assigning a probability of non-exceedence
    NonPersistenceBelowYearsSorted = np.zeros([PersistenceBelowYears.shape[0],PersistenceBelowYears.shape[1]+1])
    NonPersistenceBelowYearsSorted[:,:-1] = np.sort(1.0-PersistenceBelowYears, axis=0)
    NonPersistenceBelowYearsSorted[:,-1] = np.arange(1,NOY+1,1)/NOY
    
    """
    # Interpolating ECDF curve (input is P-value from vertical axis)
    xinterpNPBYS = np.zeros([len(PvalsNEYS),len(ReferencePeriods)])
    xinterpNPBYSP = np.zeros([len(Pvalues),len(ReferencePeriods)])
    for i in range(0,len(ReferencePeriods)):
        xinterpNPBYS[:,i] = np.interp(PvalsNEYS, NonPersistenceBelowYearsSorted[:,-1], NonPersistenceBelowYearsSorted[:,i])
        # Printing the P-values
        # P0 = minimum %, P100 = maximum %
        for j in range(0,len(Pvalues)):
            xinterpNPBYSP[j,i] = 100*xinterpNPBYS[Pvalues[j],i]
    
    """
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    xinterpNPBYS = np.zeros([len(PvalsNEYS),len(ReferencePeriods)])
    xinterpNPBYSP = np.zeros([len(Pvalues),len(ReferencePeriods)])
    for i in range(0,len(ReferencePeriods)):
        xinterpNPBYS[:,i] = np.sort(1.0-xinterpPBYS[:,i])
        # Printing the P-values
        # P0 = minimum %, P100 = maximum %
        for j in range(0,len(Pvalues)):
            xinterpNPBYSP[j,i] = 100*xinterpNPBYS[Pvalues[j],i]
    
    #********* Saving standard P-values in excel **********************************
    
    # Names of the rows of the table
    NameRowsPvals = ["P" + str(int(Pvalues[i])) for i in range(0,len(Pvalues))]
    
    # Names of the columns of the table
    NameColumns1 = ["Non-Exceedance","Exceedance (WDT)"] + ["Persistence_TR_" + str(ReferencePeriods[i-2])
                   for i in range(2,len(ReferencePeriods)+2)] + ["Non-Persistence_TR(WDT)_" + str(ReferencePeriods[i-2])
                   for i in range(2,len(ReferencePeriods)+2)]
    
    # Stacking P-value data for all months
    YearsPvals = np.column_stack((np.round(xinterpNEYSP,2),np.round(xinterpEYSP,2),np.round(xinterpPBYSP,2),np.round(xinterpNPBYSP,2)))
    
    df_PvalsYear = pd.DataFrame(YearsPvals, NameRowsPvals, NameColumns1)
    
    # Create excel writer object
    file_table01 = '01_P-values for each year and TR_percentages.xlsx'
    writer01 = pd.ExcelWriter(os.path.join(tables_directory, file_table01))
    
    # Write dataframe to excel
    df_PvalsYear.to_excel(writer01)
    
    # Save the excel
    writer01.save()
    # print('DataFrame for yearly P-value is written successfully to Excel File.')
    
    
    if PlottingYears == 1:
        #**************** Plotting Non-Exceedance of each year ************************
        
        colors = np.random.rand(3,len(ReferencePeriods))
        width = 0.75
        
        fig01 = plt.figure(figsize=(8, 8))
        ax01 = fig01.add_subplot(211)
        ax01.set_title('Non-Exceedance plot for all years')
        ax01.bar(YearsP, 100*ExceedancePlot, width, color="orangered", label='Exceedance')
        ax01.bar(YearsP, 100*NonExceedanceYears, width, color="blue", label='Non-Exceedance')
        ax01.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
        ax01.set_ylabel('Time %')
        ax01.set_xlabel('Years')
        ax01.yaxis.grid(color='grey', linestyle='--', linewidth=0.5)
        fig_name01 = '01_Non-Exceedance plot for all years.jpg'
        fig_path01 = os.path.join(figures_directory, fig_name01)
        plt.savefig(fig_path01, dpi=100, bbox_inches='tight')
        
        #********* Plotting the ECDF Non-Exceedance of each year **********************
        
        # P20 Non-Exceedance + Exceedance = 100 etc.
        fig02 = plt.figure(figsize=(8, 8))
        ax02 = fig02.add_subplot(211)
        ax02.set_title("Non-Exceedance ECDF plot for all years")
        ax02.plot(100*NonExceedanceYearsSorted[:,0],NonExceedanceYearsSorted[:,-1],color=colors[:,0])
        ax02.fill_between(100*NonExceedanceYearsSorted[:,0],NonExceedanceYearsSorted[:,-1], color=colors[:,0], alpha=0.5)
        ax02.grid(color='grey', linestyle='--', linewidth=0.5)
        ax02.set_ylabel('P-value')
        ax02.set_xlabel('Time %')
        fig_name02 = '02_Non-Exceedance ECDF plot for all years.jpg'
        fig_path02 = os.path.join(figures_directory, fig_name02)
        plt.savefig(fig_path02, dpi=100, bbox_inches='tight')
        
        #********* Plotting the ECDF Exceedance of each year **************************
        
        fig03 = plt.figure(figsize=(8, 8))
        ax03 = fig03.add_subplot(211)
        ax03.set_title("Exceedance ECDF plot for all years")
        ax03.plot(100*ExceedanceYearsSorted[:,0],ExceedanceYearsSorted[:,-1],color=0.5*colors[:,0])
        ax03.fill_between(100*ExceedanceYearsSorted[:,0],ExceedanceYearsSorted[:,-1], color=0.5*colors[:,0], alpha=0.5)
        ax03.grid(color='grey', linestyle='--', linewidth=0.5)
        ax03.set_ylabel('P-value')
        ax03.set_xlabel('Time %')
        fig_name03 = '03_Exceedance ECDF plot for all years.jpg'
        fig_path03 = os.path.join(figures_directory, fig_name03)
        plt.savefig(fig_path03, dpi=100, bbox_inches='tight')
        
        #********* Plotting the Persistence (below treshold limit) of each year (overlapping) *******
        
        # subscript "a" - overlapping, "b" - non-overlapping
        
        for i in range(0,len(ReferencePeriods)):
            fig04a = plt.figure(figsize=(8, 8))
            ax04a = fig04a.add_subplot(211)
            ax04a.set_title(f'Persistence (below) plot for reference period: {ReferencePeriods[i]} hrs (Overlapping)')
            ax04a.bar(YearsP, 100*PersistenceBelowOnes[:,i], width, color="orangered", label='Non-Persistence below')
            ax04a.bar(YearsP, 100*PersistenceBelowYears[:,i], width, color="blue", label='Persistence below')
            ax04a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
            ax04a.set_ylabel('Time %')
            ax04a.set_xlabel('Years')
            ax04a.yaxis.grid(color='grey', linestyle='--', linewidth=0.5)
            fig_name04a = f'04_{i+1}_Persistence_below_years_TR_{ReferencePeriods[i]}hrs_overlapping.jpg'
            fig_path04a = os.path.join(figures_directory, fig_name04a)
            plt.savefig(fig_path04a, dpi=100, bbox_inches='tight')
            
        #********* Plotting the ECDF of Persistence (below treshold limit) of each year (overlapping) *******
        
        fig05a = plt.figure(figsize=(8, 8))
        ax05a = fig05a.add_subplot(211)
        
        for i in range(0,len(ReferencePeriods)):
            ax05a.set_title('P-values Persistence (below) for each year (overlapping)')
            ax05a.plot(100*PersistenceBelowYearsSorted[:,i],PersistenceBelowYearsSorted[:,-1],color=colors[:,i], label=f'TR {ReferencePeriods[i]} hrs')
            ax05a.fill_between(100*PersistenceBelowYearsSorted[:,i],PersistenceBelowYearsSorted[:,-1], color=colors[:,i], alpha=0.5)
        ax05a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
        ax05a.grid(color='grey', linestyle='--', linewidth=0.5)
        ax05a.set_ylabel('P-value')
        ax05a.set_xlabel('Time %')
        fig_name05a = f'05_P-values PersistenceBelow for each year_TR_{ReferencePeriods[i]}hrs_overlapping.jpg'
        fig_path05a = os.path.join(figures_directory, fig_name05a)
        plt.savefig(fig_path05a, dpi=100, bbox_inches='tight')
        
        #********* Plotting the ECDF of Non-Persistence (below treshold limit) of each year (overlapping) *******
        
        # P20 PersistenceBelow + P80 Non-PersistenceBelow = 100 etc.
        fig06a = plt.figure(figsize=(8, 8))
        ax06a = fig06a.add_subplot(211)
        
        for i in range(0,len(ReferencePeriods)):
            ax06a.set_title('P-values Non-Persistence (below) for each year (overlapping)')
            ax06a.plot(100*NonPersistenceBelowYearsSorted[:,i],NonPersistenceBelowYearsSorted[:,-1],color=colors[:,i], label=f'TR {ReferencePeriods[i]} hrs')
            ax06a.fill_between(100*NonPersistenceBelowYearsSorted[:,i],NonPersistenceBelowYearsSorted[:,-1], color=colors[:,i], alpha=0.5)
        ax06a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
        ax06a.grid(color='grey', linestyle='--', linewidth=0.5)
        ax06a.set_ylabel('P-value')
        ax06a.set_xlabel('Time %')
        fig_name06a = f'06_P-values Non-PersistenceBelow for each year_TR_{ReferencePeriods[i]}hrs_overlapping.jpg'
        fig_path06a = os.path.join(figures_directory, fig_name06a)
        plt.savefig(fig_path06a, dpi=100, bbox_inches='tight')
    
    """
    Notes:
    Additionally, the following can be added in this step:
        1. Bar plot for Persistence above a treshold limit for each year
        2. P-value plot for Persistence above a treshold limit for each year
        3. Delay/Waiting Time statistics by finding the mean duration of the 
        individual non-working intervals for each month
        4. Counting the number of occurances of weather window >= reference period
        
    It is worth remembering from [1] that:
    Quote
        The sum of persistence and non- persistence always equals 100%, but the 
    sum of persistence-below and persistence-above a threshold for a given 
    weather window duration may not necessarily equal 100%. The persistence of 
    favourable and unfavourable conditions must therefore be separately 
    assessed and is similarly context dependent in definition.
    Unqote
    
    The exceedance (1-non-exceedance) and the non-persistence below (1-persistence
    below) reflects the WDT.
    
    """
    
    ################################################################################
    #******************** MONTHLY STATISTICS (ALL YEARS) ***************************
    ################################################################################
    
    # Create a matrix with Non-Exceedance and Persistence results to be able
    # to split the monthly data. 
    # Note that this method will split the weather window at the boundary of
    # each month (start-end) so that part of the weather window will remain in
    # preceeding/succeeding month. Otherwise, the weather window is lost. If
    # it is desired to do separate evaluation for each month, with boundary
    # windows potentially lost, it can be done by evaluating Persistence for
    # each month separately as per above.
    DES = np.hstack((data,NonExceedance,PersistenceBelow)) # Complete table "data" sorted by month
    DES = DES[DES[:, 3].argsort()] # sort by hour 
    DES = DES[DES[:, 2].argsort(kind='mergesort')] # sort by day
    DES = DES[DES[:, 0].argsort(kind='mergesort')] # sort by year
    DES = DES[DES[:, 1].argsort(kind='mergesort')] # sort by month 
    
    # Non-overlapping data (starts from first workable hour, so the workability might not transfer to the next month)
    DESNO = np.hstack((data,NonExceedance,PersistenceBelowNO)) 
    DESNO = DESNO[DESNO[:, 3].argsort()] # sort by hour 
    DESNO = DESNO[DESNO[:, 2].argsort(kind='mergesort')] # sort by day
    DESNO = DESNO[DESNO[:, 0].argsort(kind='mergesort')] # sort by year
    DESNO = DESNO[DESNO[:, 1].argsort(kind='mergesort')] # sort by month 
     
    #np.savetxt('DES.txt', DES, delimiter=',', fmt='%1.5f')
    
    # Where months change
    MonthsChangeIndex = np.where(DES[:,1][:-1] != DES[:,1][1:])[0]
    MonthsChangeIndex = np.hstack((0,MonthsChangeIndex,DES.shape[0]))
    
    # Where years change
    YearMonthsChangeIndex = np.where(DES[:,0][:-1] != DES[:,0][1:])[0]
    YearMonthsChangeIndex = np.hstack((0,YearMonthsChangeIndex,DES.shape[0]))
    
    # Empty matrix for Non-Exceedance for months all years
    NonExceedanceMonthsAll = np.zeros([len(MonthsChangeIndex)-1])
    ExceedanceMonthsAllPlot = NonExceedanceMonthsAll + 1
    
    # Empty matrix for Exceedance for months all years
    ExceedanceMonthsAll = np.zeros([len(MonthsChangeIndex)-1])
    
    # Empty matrix for Persistence (below) for months all years
    PersistenceBelowMonthsAll = np.zeros([len(MonthsChangeIndex)-1,len(ReferencePeriods)])
    PersistenceBelowMonthsAllOnes = PersistenceBelowMonthsAll + 1
    
    # Empty matrix for Non-Persistence (below) for months all years
    NonPersistenceBelowMonthsAll = np.zeros([len(MonthsChangeIndex)-1,len(ReferencePeriods)])
    
    col_DES = data.shape[1]+NonExceedance.shape[1]-1 # column index of DES for NonExceedance, -1 as python starts at 0
    
    # Rearranging the data
    for i in range(0,NumberOfMonths):
        # Data length in each month
        if i == 0:
            MonthAllSize = MonthsChangeIndex[i+1]-MonthsChangeIndex[i]+1
        else:
            MonthAllSize = MonthsChangeIndex[i+1]-MonthsChangeIndex[i]
        #print(MonthAllSize)
        # Sum of all workable times in each month, all years   
        NonExceedanceMonthsAllSum = np.sum(DES[MonthsChangeIndex[i]:MonthsChangeIndex[i+1]+1,col_DES],axis=0) # col_nemas_th column is NonExceedance evaluation
        # Non-Exceedance for each each month, all years
        NonExceedanceMonthsAll[i] = NonExceedanceMonthsAllSum/MonthAllSize
        ExceedanceMonthsAll[i] = 1-NonExceedanceMonthsAll[i]
        for j in range(0,len(ReferencePeriods)):
            PersistenceBelowMonthsAllSum = np.sum(DES[MonthsChangeIndex[i]:MonthsChangeIndex[i+1]+1,j+(col_DES+1)],axis=0) # column indices for persistance, only Persistence with TR
            PersistenceBelowMonthsAll[i,j] = PersistenceBelowMonthsAllSum/MonthAllSize
            NonPersistenceBelowMonthsAll[i,j] = 1-PersistenceBelowMonthsAll[i,j]
    
    
    if PlottingAllMonthsAllYears == 1:
        
        #**************** Plotting Non-Exceedance of each month, all years (overlapping) ************
        
        fig07a = plt.figure(figsize=(8, 8))
        ax07a = fig07a.add_subplot(211)
        ax07a.set_title("Non-Exceedance plot for each month, all years (overlapping)")
        ax07a.bar(Months, 100*ExceedanceMonthsAllPlot, width, color="orangered", label='Exceedance')
        ax07a.bar(Months, 100*NonExceedanceMonthsAll, width, color="blue", label='Non-Exceedance')
        ax07a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
        ax07a.set_ylabel('Time %')
        ax07a.set_xlabel('Months')
        ax07a.yaxis.grid(color='grey', linestyle='--', linewidth=0.5)
        fig_name07a = '07_Non-Exceedance plot for each month_all years_overlapping.jpg'
        fig_path07a = os.path.join(figures_directory, fig_name07a)
        plt.savefig(fig_path07a, dpi=100, bbox_inches='tight')
        
        #**************** Plotting Persistence of each month, all years (overlapping) ***************
        
        for i in range(0,len(ReferencePeriods)):
            fig08a = plt.figure(figsize=(8, 8))
            ax08a = fig08a.add_subplot(211)
            ax08a.set_title(f'Persistence (below) plot for reference period: {ReferencePeriods[i]} hrs (overlapping)')
            ax08a.bar(Months, 100*PersistenceBelowMonthsAllOnes[:,i], width, color="orangered", label='Non-Persistence below')
            ax08a.bar(Months, 100*PersistenceBelowMonthsAll[:,i], width, color="blue", label='Persistence below')
            ax08a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
            ax08a.set_ylabel('Time %')
            ax08a.set_xlabel('Months')
            ax08a.yaxis.grid(color='grey', linestyle='--', linewidth=0.5)
            fig_name08a = f'08_Persistence below plot for each month_all years_TR_{ReferencePeriods[i]}hrs_overlapping.jpg'
            fig_path08a = os.path.join(figures_directory, fig_name08a)
            plt.savefig(fig_path08a, dpi=100, bbox_inches='tight')
        
    
    #*************** Saving values in excel ***************************************
    
    # Names of the rows of the table
    NameRowsPvals2 = NameMonths
    
    # Names of the columns of the table
    NameColumns2 = ["Non-Exceedance","Exceedance (WDT)"] + ["Persistence_TR_" + str(ReferencePeriods[i-2])
                   for i in range(2,len(ReferencePeriods)+2)] + ["Non-Persistence_TR(WDT)_" + str(ReferencePeriods[i-2])
                   for i in range(2,len(ReferencePeriods)+2)]
    
    # Stacking P-value data for all months
    MonthsYears = np.column_stack((np.round(100*NonExceedanceMonthsAll,2),np.round(100*ExceedanceMonthsAll,2),
                                   np.round(100*PersistenceBelowMonthsAll,2),np.round(100*NonPersistenceBelowMonthsAll,2)))
    
    df_MonthsYears = pd.DataFrame(MonthsYears, NameRowsPvals2, NameColumns2)
    
    # Create excel writer object
    file_table02 = '02_Every month all years_percentages.xlsx'
    writer02 = pd.ExcelWriter(os.path.join(tables_directory, file_table02))
    
    # Write dataframe to excel
    df_MonthsYears.to_excel(writer02)
    
    # Save the excel
    writer02.save()
    # print('DataFrame for months all years is written successfully to Excel File.')
    
    
    """
    Notes:
    Additionally, the following can be added in this step:
        1. Bar plot of Persistence above for each month, all years
        5. Counting the number of occurances of weather window >= reference period
    
    """
    
    ################################################################################
    #******************** MONTHLY STATISTICS (PER YEAR) ****************************
    ################################################################################
    
    # Statistics per year for all months
    
    # Empty 3D matrix for Non-Exceedance and Persistence for months all years
    DataMonths = np.zeros([NumberOfMonths,NumberOfYears,len(ReferencePeriods)+1])    # overlapping, number of weather windows can be a , nww = 4.5
    DataMonthsNO = np.zeros([NumberOfMonths,NumberOfYears,len(ReferencePeriods)+1])  # non-overlapping, number of ww is integer, nw = 4
    DataMonthsOnes = DataMonths + 1
    
    # Number of rows for each month
    RowsMonths = [MonthsChangeIndex[i+1]-MonthsChangeIndex[i] for i in range(0,NumberOfMonths)]
    
    # Index where index of months is equal to the index of year
    CombinedIndex = [np.where(YearMonthsChangeIndex == MonthsChangeIndex[i])[0][0] for i in range(0,len(MonthsChangeIndex))]
    
    # Number of years the data is available for each month
    JotMonths = [CombinedIndex[i+1]-CombinedIndex[i] for i in range(0,NumberOfMonths)] # +1??
    
    """
    Note that the 3D matrix can be simplified and below code can be made more
    efficient and shorter if only those years are used for which data exist
    for all months. As this is not the case here (data for last year is available
    only for 5 months) it was necessary to create a matrix with the results
    for each month.
    """
    
    # for i in range(0,NumberOfMonths):
    #     for j in range(0,JotMonths[i]):
    #         if i == 0 and j==0:
    #             A1 = 0
    #         else:
    #             A1 = 1
    #         print(i,j,CombinedIndex[i],CombinedIndex[i]+j+1,YearMonthsChangeIndex[CombinedIndex[i]+j]+A1,YearMonthsChangeIndex[CombinedIndex[i]+j+1]+1)
    
    # Populating the 3D matrix with the results
    for i in range(0,NumberOfMonths):
        for j in range(0,JotMonths[i]):
            for k in range(0,len(ReferencePeriods)+1): # +1 to include Non-Exceedance
            # A1 is used to start the counting from n+1 row, where n is the
            # last number of row considered in the previous loop, e.g. sums
            # are considered for index 0-22, 23-50, instead of 0-22, 22-50 which
            # would be wrong as the last row would be overwritten in the next loop
                if i == 0 and j == 0:
                    A1 = 0
                else:
                    A1 = 1
                MonthYearSize = YearMonthsChangeIndex[CombinedIndex[i]+j+1] - YearMonthsChangeIndex[CombinedIndex[i]+j]
                #print(i,j,MonthYearSize)
                # last month size 745 when 744 is 31x24hrs, check!
                DataMonthsSum = np.sum(DES[YearMonthsChangeIndex[CombinedIndex[i]+j]:YearMonthsChangeIndex[CombinedIndex[i]+j+1]+1,k+col_DES],axis=0) # col_DES for 4 criterias
                # Non-overlapping
                DataMonthsSumNO = np.sum(DESNO[YearMonthsChangeIndex[CombinedIndex[i]+j]:YearMonthsChangeIndex[CombinedIndex[i]+j+1]+1,k+col_DES],axis=0) # col_DES for 4 criterias
                DataMonthsNO[i,j,k] = DataMonthsSumNO/MonthYearSize
                DataMonths[i,j,k] = DataMonthsSum/MonthYearSize
    
    StartYear = data[0,0]
    YearsPerMonth = [np.arange(StartYear,StartYear+JotMonths[i],1) for i in range(0,NumberOfMonths)]
    
    
    #******************************************************************************
    #* Plotting Non-Exceedance and Persistence below of each month, all years (overlapping) ****
    #******************************************************************************
    
    if PlottingAllMonthsEveryYear == 1:
        # Exceedance
        for i in range(0,NumberOfMonths):
            fig09 = plt.figure(figsize=(8, 8))
            ax09 = fig09.add_subplot(211)  
            ax09.set_title(f'Non-Exceedance plot for {NameMonths[i]}')
            ax09.bar(Years, 100*DataMonthsOnes[i,:,0], width, color="orangered", label='Exceedance')
            ax09.bar(Years, 100*DataMonths[i,:,0], width, color="blue", label='Non-Exceedance')
            ax09.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
            ax09.set_ylabel('Time %')
            ax09.set_xlabel('Years')
            ax09.yaxis.grid(color='grey', linestyle='--', linewidth=0.5)
            fig_name09 = f'09_{i}{0}_Non-Exceedance_{NameMonths[i]}.jpg'
            fig_path09 = os.path.join(figures_directory, fig_name09)
            plt.savefig(fig_path09, dpi=100, bbox_inches='tight')
    
        # Overlapping
        for i in range(0,NumberOfMonths):
            for j in range(1,len(ReferencePeriods)+1):
                fig09a = plt.figure(figsize=(8, 8))
                ax09a = fig09a.add_subplot(211)  
                ax09a.set_title(f'Persistence (below) plot for {NameMonths[i]}, reference period: {ReferencePeriods[j-1]} hrs (overlapping)') # (j-1) as j=0 is for Non-Exceedance
                ax09a.bar(Years, 100*DataMonthsOnes[i,:,j], width, color="orangered", label='Non-Persistence below')
                ax09a.bar(Years, 100*DataMonths[i,:,j], width, color="blue", label='Persistence below')
                ax09a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
                ax09a.set_ylabel('Time %')
                ax09a.set_xlabel('Years')
                ax09a.yaxis.grid(color='grey', linestyle='--', linewidth=0.5)
                fig_name09a = f'09a_{i}{j}_PersistenceBelow_{NameMonths[i]}_ref_period_{ReferencePeriods[j-1]}_hrs_overlapping.jpg'
                fig_path09a = os.path.join(figures_directory, fig_name09a)
                plt.savefig(fig_path09a, dpi=100, bbox_inches='tight') # (j-1) as j=0 is for Non-Exceedance
    
    
    #******************************************************************************
    # ECDF and P-values of Non-Exceedance and Persistence below of each month, 
    # all years
    #******************************************************************************
    
    # Split data for each month, all years in separate matrices, OVERLAPPING
    January = DataMonths[0,0:JotMonths[0],:]
    February = DataMonths[1,0:JotMonths[1],:]
    March = DataMonths[2,0:JotMonths[2],:]
    April = DataMonths[3,0:JotMonths[3],:]
    May = DataMonths[4,0:JotMonths[4],:]
    June = DataMonths[5,0:JotMonths[5],:]
    July = DataMonths[6,0:JotMonths[6],:]
    August = DataMonths[7,0:JotMonths[7],:]
    September = DataMonths[8,0:JotMonths[8],:]
    October = DataMonths[9,0:JotMonths[9],:]
    November = DataMonths[10,0:JotMonths[10],:]
    December = DataMonths[11,0:JotMonths[11],:]  
    
    # Split data for each month, all years in separate matrices, NON-OVERLAPPING
    JanuaryNO = DataMonthsNO[0,0:JotMonths[0],:]
    FebruaryNO = DataMonthsNO[1,0:JotMonths[1],:]
    MarchNO = DataMonthsNO[2,0:JotMonths[2],:]
    AprilNO = DataMonthsNO[3,0:JotMonths[3],:]
    MayNO = DataMonthsNO[4,0:JotMonths[4],:]
    JuneNO = DataMonthsNO[5,0:JotMonths[5],:]
    JulyNO = DataMonthsNO[6,0:JotMonths[6],:]
    AugustNO = DataMonthsNO[7,0:JotMonths[7],:]
    SeptemberNO = DataMonthsNO[8,0:JotMonths[8],:]
    OctoberNO = DataMonthsNO[9,0:JotMonths[9],:]
    NovemberNO = DataMonthsNO[10,0:JotMonths[10],:]
    DecemberNO = DataMonthsNO[11,0:JotMonths[11],:] 
    
    # Empty matrices for sorted data
    JanuaryS = np.zeros([JotMonths[0],len(ReferencePeriods)+2])
    FebruaryS = np.zeros([JotMonths[1],len(ReferencePeriods)+2])
    MarchS = np.zeros([JotMonths[2],len(ReferencePeriods)+2])
    AprilS = np.zeros([JotMonths[3],len(ReferencePeriods)+2])
    MayS = np.zeros([JotMonths[4],len(ReferencePeriods)+2])
    JuneS = np.zeros([JotMonths[5],len(ReferencePeriods)+2])
    JulyS = np.zeros([JotMonths[6],len(ReferencePeriods)+2])
    AugustS = np.zeros([JotMonths[7],len(ReferencePeriods)+2])
    SeptemberS = np.zeros([JotMonths[8],len(ReferencePeriods)+2])
    OctoberS = np.zeros([JotMonths[9],len(ReferencePeriods)+2])
    NovemberS = np.zeros([JotMonths[10],len(ReferencePeriods)+2])
    DecemberS = np.zeros([JotMonths[11],len(ReferencePeriods)+2])
    
    # Empty matrices for sorted data, Non-overlapping
    JanuaryNOS = np.zeros([JotMonths[0],len(ReferencePeriods)+2])
    FebruaryNOS = np.zeros([JotMonths[1],len(ReferencePeriods)+2])
    MarchNOS = np.zeros([JotMonths[2],len(ReferencePeriods)+2])
    AprilNOS = np.zeros([JotMonths[3],len(ReferencePeriods)+2])
    MayNOS = np.zeros([JotMonths[4],len(ReferencePeriods)+2])
    JuneNOS = np.zeros([JotMonths[5],len(ReferencePeriods)+2])
    JulyNOS = np.zeros([JotMonths[6],len(ReferencePeriods)+2])
    AugustNOS = np.zeros([JotMonths[7],len(ReferencePeriods)+2])
    SeptemberNOS = np.zeros([JotMonths[8],len(ReferencePeriods)+2])
    OctoberNOS = np.zeros([JotMonths[9],len(ReferencePeriods)+2])
    NovemberNOS = np.zeros([JotMonths[10],len(ReferencePeriods)+2])
    DecemberNOS = np.zeros([JotMonths[11],len(ReferencePeriods)+2])
    
    # Sorting the values for each year into rank order (smallest to largest) 
    
    # Sort data for January
    JanuaryS[:,:-1] = np.sort(January, axis=0)
    JanuaryS[:,-1] = np.arange(1,JotMonths[0]+1,1)/JotMonths[0]
    JanuaryNOS[:,:-1] = np.sort(JanuaryNO, axis=0)
    JanuaryNOS[:,-1] = np.arange(1,JotMonths[0]+1,1)/JotMonths[0]
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    xinterp1A = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp1ANO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    xinterp1B = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp1BNO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    interp1PA = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp1PANO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    interp1PB = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp1PBNO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    for i in range(0,len(ReferencePeriods)+1):
        xinterp1A[:,i] = np.interp(PvalsNEYS, JanuaryS[:,-1], JanuaryS[:,i])
        xinterp1B[:,i] = np.sort(1.0-xinterp1A[:,i])
        xinterp1ANO[:,i] = np.interp(PvalsNEYS, JanuaryNOS[:,-1], JanuaryNOS[:,i])
        xinterp1BNO[:,i] = np.sort(1.0-xinterp1ANO[:,i])
        # Printing the P-values
        # P0 = minimum %, P100 = maximum %
        for j in range(0,len(Pvalues)):
            interp1PA[j,i] = 100*xinterp1A[Pvalues[j],i]
            interp1PB[j,i] = 100*xinterp1B[Pvalues[j],i]
            interp1PANO[j,i] = 100*xinterp1ANO[Pvalues[j],i]
            interp1PBNO[j,i] = 100*xinterp1BNO[Pvalues[j],i]
    
    
    # Sort data for February
    FebruaryS[:,:-1] = np.sort(February, axis=0)
    FebruaryS[:,-1] = np.arange(1,JotMonths[1]+1,1)/JotMonths[1]
    FebruaryNOS[:,:-1] = np.sort(FebruaryNO, axis=0)
    FebruaryNOS[:,-1] = np.arange(1,JotMonths[1]+1,1)/JotMonths[1]
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    xinterp2A = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp2ANO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    xinterp2B = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp2BNO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    interp2PA = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp2PANO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    interp2PB = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp2PBNO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    for i in range(0,len(ReferencePeriods)+1):
        xinterp2A[:,i] = np.interp(PvalsNEYS, FebruaryS[:,-1], FebruaryS[:,i])
        xinterp2B[:,i] = np.sort(1.0-xinterp2A[:,i])
        xinterp2ANO[:,i] = np.interp(PvalsNEYS, FebruaryNOS[:,-1], FebruaryNOS[:,i])
        xinterp2BNO[:,i] = np.sort(1.0-xinterp2ANO[:,i])
        # Printing the P-values
        # P0 = minimum %, P100 = maximum %
        for j in range(0,len(Pvalues)):
            interp2PA[j,i] = 100*xinterp2A[Pvalues[j],i]
            interp2PB[j,i] = 100*xinterp2B[Pvalues[j],i]
            interp2PANO[j,i] = 100*xinterp2ANO[Pvalues[j],i]
            interp2PBNO[j,i] = 100*xinterp2BNO[Pvalues[j],i]
        
        
    # Sort data for March
    MarchS[:,:-1] = np.sort(March, axis=0)
    MarchS[:,-1] = np.arange(1,JotMonths[2]+1,1)/JotMonths[2]
    MarchNOS[:,:-1] = np.sort(MarchNO, axis=0)
    MarchNOS[:,-1] = np.arange(1,JotMonths[2]+1,1)/JotMonths[2]
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    xinterp3A = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp3ANO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    xinterp3B = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp3BNO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    interp3PA = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp3PANO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    interp3PB = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp3PBNO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    for i in range(0,len(ReferencePeriods)+1):
        xinterp3A[:,i] = np.interp(PvalsNEYS, MarchS[:,-1], MarchS[:,i])
        xinterp3B[:,i] = np.sort(1.0-xinterp3A[:,i])
        xinterp3ANO[:,i] = np.interp(PvalsNEYS, MarchNOS[:,-1], MarchNOS[:,i])
        xinterp3BNO[:,i] = np.sort(1.0-xinterp3ANO[:,i])
        # Printing the P-values
        # P0 = minimum %, P100 = maximum %
        for j in range(0,len(Pvalues)):
            interp3PA[j,i] = 100*xinterp3A[Pvalues[j],i]
            interp3PB[j,i] = 100*xinterp3B[Pvalues[j],i]
            interp3PANO[j,i] = 100*xinterp3ANO[Pvalues[j],i]
            interp3PBNO[j,i] = 100*xinterp3BNO[Pvalues[j],i]
    
    
    # Sort data for April
    AprilS[:,:-1] = np.sort(April, axis=0)
    AprilS[:,-1] = np.arange(1,JotMonths[3]+1,1)/JotMonths[3]
    AprilNOS[:,:-1] = np.sort(AprilNO, axis=0)
    AprilNOS[:,-1] = np.arange(1,JotMonths[3]+1,1)/JotMonths[3]
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    xinterp4A = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp4ANO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    xinterp4B = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp4BNO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    interp4PA = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp4PANO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    interp4PB = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp4PBNO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    for i in range(0,len(ReferencePeriods)+1):
        xinterp4A[:,i] = np.interp(PvalsNEYS, AprilS[:,-1], AprilS[:,i])
        xinterp4B[:,i] = np.sort(1.0-xinterp4A[:,i])
        xinterp4ANO[:,i] = np.interp(PvalsNEYS, AprilNOS[:,-1], AprilNOS[:,i])
        xinterp4BNO[:,i] = np.sort(1.0-xinterp4ANO[:,i])
        # Printing the P-values
        # P0 = minimum %, P100 = maximum %
        for j in range(0,len(Pvalues)):
            interp4PA[j,i] = 100*xinterp4A[Pvalues[j],i]
            interp4PB[j,i] = 100*xinterp4B[Pvalues[j],i]
            interp4PANO[j,i] = 100*xinterp4ANO[Pvalues[j],i]
            interp4PBNO[j,i] = 100*xinterp4BNO[Pvalues[j],i]
    
    
    # Sort data for May
    MayS[:,:-1] = np.sort(May, axis=0)
    MayS[:,-1] = np.arange(1,JotMonths[4]+1,1)/JotMonths[4]
    MayNOS[:,:-1] = np.sort(MayNO, axis=0)
    MayNOS[:,-1] = np.arange(1,JotMonths[4]+1,1)/JotMonths[4]
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    xinterp5A = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp5ANO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    xinterp5B = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp5BNO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    interp5PA = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp5PANO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    interp5PB = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp5PBNO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    for i in range(0,len(ReferencePeriods)+1):
        xinterp5A[:,i] = np.interp(PvalsNEYS, MayS[:,-1], MayS[:,i])
        xinterp5B[:,i] = np.sort(1.0-xinterp5A[:,i])
        xinterp5ANO[:,i] = np.interp(PvalsNEYS, MayNOS[:,-1], MayNOS[:,i])
        xinterp5BNO[:,i] = np.sort(1.0-xinterp5ANO[:,i])
        # Printing the P-values
        # P0 = minimum %, P100 = maximum %
        for j in range(0,len(Pvalues)):
            interp5PA[j,i] = 100*xinterp5A[Pvalues[j],i]
            interp5PB[j,i] = 100*xinterp5B[Pvalues[j],i]
            interp5PANO[j,i] = 100*xinterp5ANO[Pvalues[j],i]
            interp5PBNO[j,i] = 100*xinterp5BNO[Pvalues[j],i]
    
    
    # Sort data for June
    JuneS[:,:-1] = np.sort(June, axis=0)
    JuneS[:,-1] = np.arange(1,JotMonths[5]+1,1)/JotMonths[5] 
    JuneNOS[:,:-1] = np.sort(JuneNO, axis=0)
    JuneNOS[:,-1] = np.arange(1,JotMonths[5]+1,1)/JotMonths[5]     
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    xinterp6A = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp6ANO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    xinterp6B = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp6BNO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    interp6PA = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp6PANO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    interp6PB = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp6PBNO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    for i in range(0,len(ReferencePeriods)+1):
        xinterp6A[:,i] = np.interp(PvalsNEYS, JuneS[:,-1], JuneS[:,i])
        xinterp6B[:,i] = np.sort(1.0-xinterp6A[:,i])
        xinterp6ANO[:,i] = np.interp(PvalsNEYS, JuneNOS[:,-1], JuneNOS[:,i])
        xinterp6BNO[:,i] = np.sort(1.0-xinterp6ANO[:,i])
        # Printing the P-values
        # P0 = minimum %, P100 = maximum %
        for j in range(0,len(Pvalues)):
            interp6PA[j,i] = 100*xinterp6A[Pvalues[j],i]
            interp6PB[j,i] = 100*xinterp6B[Pvalues[j],i]
            interp6PANO[j,i] = 100*xinterp6ANO[Pvalues[j],i]
            interp6PBNO[j,i] = 100*xinterp6BNO[Pvalues[j],i]
     
    
    # Sort data for July
    JulyS[:,:-1] = np.sort(July, axis=0)
    JulyS[:,-1] = np.arange(1,JotMonths[6]+1,1)/JotMonths[6] 
    JulyNOS[:,:-1] = np.sort(JulyNO, axis=0)
    JulyNOS[:,-1] = np.arange(1,JotMonths[6]+1,1)/JotMonths[6] 
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    xinterp7A = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp7ANO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    xinterp7B = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp7BNO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    interp7PA = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp7PANO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    interp7PB = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp7PBNO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    for i in range(0,len(ReferencePeriods)+1):
        xinterp7A[:,i] = np.interp(PvalsNEYS, JulyS[:,-1], JulyS[:,i])
        xinterp7B[:,i] = np.sort(1.0-xinterp7A[:,i])
        xinterp7ANO[:,i] = np.interp(PvalsNEYS, JulyNOS[:,-1], JulyNOS[:,i])
        xinterp7BNO[:,i] = np.sort(1.0-xinterp7ANO[:,i])
        # Printing the P-values
        # P0 = minimum %, P100 = maximum %
        for j in range(0,len(Pvalues)):
            interp7PA[j,i] = 100*xinterp7A[Pvalues[j],i]
            interp7PB[j,i] = 100*xinterp7B[Pvalues[j],i]
            interp7PANO[j,i] = 100*xinterp7ANO[Pvalues[j],i]
            interp7PBNO[j,i] = 100*xinterp7BNO[Pvalues[j],i]
    
    
    # Sort data for August
    AugustS[:,:-1] = np.sort(August, axis=0)
    AugustS[:,-1] = np.arange(1,JotMonths[7]+1,1)/JotMonths[7] 
    AugustNOS[:,:-1] = np.sort(AugustNO, axis=0)
    AugustNOS[:,-1] = np.arange(1,JotMonths[7]+1,1)/JotMonths[7] 
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    xinterp8A = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp8ANO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    xinterp8B = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp8BNO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    interp8PA = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp8PANO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    interp8PB = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp8PBNO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    for i in range(0,len(ReferencePeriods)+1):
        xinterp8A[:,i] = np.interp(PvalsNEYS, AugustS[:,-1], AugustS[:,i])
        xinterp8B[:,i] = np.sort(1.0-xinterp8A[:,i])
        xinterp8ANO[:,i] = np.interp(PvalsNEYS, AugustNOS[:,-1], AugustNOS[:,i])
        xinterp8BNO[:,i] = np.sort(1.0-xinterp8ANO[:,i])
        # Printing the P-values
        # P0 = minimum %, P100 = maximum %
        for j in range(0,len(Pvalues)):
            interp8PA[j,i] = 100*xinterp8A[Pvalues[j],i]
            interp8PB[j,i] = 100*xinterp8B[Pvalues[j],i]
            interp8PANO[j,i] = 100*xinterp8ANO[Pvalues[j],i]
            interp8PBNO[j,i] = 100*xinterp8BNO[Pvalues[j],i]
    
    
    # Sort data for September
    SeptemberS[:,:-1] = np.sort(September, axis=0)
    SeptemberS[:,-1] = np.arange(1,JotMonths[8]+1,1)/JotMonths[8] 
    SeptemberNOS[:,:-1] = np.sort(SeptemberNO, axis=0)
    SeptemberNOS[:,-1] = np.arange(1,JotMonths[8]+1,1)/JotMonths[8] 
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    xinterp9A = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp9ANO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    xinterp9B = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp9BNO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    interp9PA = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp9PANO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    interp9PB = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp9PBNO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    for i in range(0,len(ReferencePeriods)+1):
        xinterp9A[:,i] = np.interp(PvalsNEYS, SeptemberS[:,-1], SeptemberS[:,i])
        xinterp9B[:,i] = np.sort(1.0-xinterp9A[:,i])
        xinterp9ANO[:,i] = np.interp(PvalsNEYS, SeptemberNOS[:,-1], SeptemberNOS[:,i])
        xinterp9BNO[:,i] = np.sort(1.0-xinterp9ANO[:,i])
        # Printing the P-values
        # P0 = minimum %, P100 = maximum %
        for j in range(0,len(Pvalues)):
            interp9PA[j,i] = 100*xinterp9A[Pvalues[j],i]
            interp9PB[j,i] = 100*xinterp9B[Pvalues[j],i]
            interp9PANO[j,i] = 100*xinterp9ANO[Pvalues[j],i]
            interp9PBNO[j,i] = 100*xinterp9BNO[Pvalues[j],i]
    
    
    # Sort data for October
    OctoberS[:,:-1] = np.sort(October, axis=0)
    OctoberS[:,-1] = np.arange(1,JotMonths[9]+1,1)/JotMonths[9] 
    OctoberNOS[:,:-1] = np.sort(OctoberNO, axis=0)
    OctoberNOS[:,-1] = np.arange(1,JotMonths[9]+1,1)/JotMonths[9] 
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    xinterp10A = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp10ANO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    xinterp10B = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp10BNO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    interp10PA = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp10PANO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    interp10PB = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp10PBNO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    for i in range(0,len(ReferencePeriods)+1):
        xinterp10A[:,i] = np.interp(PvalsNEYS, OctoberS[:,-1], OctoberS[:,i])
        xinterp10B[:,i] = np.sort(1.0-xinterp10A[:,i])
        xinterp10ANO[:,i] = np.interp(PvalsNEYS, OctoberNOS[:,-1], OctoberNOS[:,i])
        xinterp10BNO[:,i] = np.sort(1.0-xinterp10ANO[:,i])
        # Printing the P-values
        # P0 = minimum %, P100 = maximum %
        for j in range(0,len(Pvalues)):
            interp10PA[j,i] = 100*xinterp10A[Pvalues[j],i]
            interp10PB[j,i] = 100*xinterp10B[Pvalues[j],i]
            interp10PANO[j,i] = 100*xinterp10ANO[Pvalues[j],i]
            interp10PBNO[j,i] = 100*xinterp10BNO[Pvalues[j],i]
    
    
    # Sort data for November
    NovemberS[:,:-1] = np.sort(November, axis=0)
    NovemberS[:,-1] = np.arange(1,JotMonths[10]+1,1)/JotMonths[10] 
    NovemberNOS[:,:-1] = np.sort(NovemberNO, axis=0)
    NovemberNOS[:,-1] = np.arange(1,JotMonths[10]+1,1)/JotMonths[10] 
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    xinterp11A = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp11ANO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    xinterp11B = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp11BNO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    interp11PA = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp11PANO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    interp11PB = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp11PBNO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    for i in range(0,len(ReferencePeriods)+1):
        xinterp11A[:,i] = np.interp(PvalsNEYS, NovemberS[:,-1], NovemberS[:,i])
        xinterp11B[:,i] = np.sort(1.0-xinterp11A[:,i])
        xinterp11ANO[:,i] = np.interp(PvalsNEYS, NovemberNOS[:,-1], NovemberNOS[:,i])
        xinterp11BNO[:,i] = np.sort(1.0-xinterp11A[:,i])
        # Printing the P-values
        # P0 = minimum %, P100 = maximum %
        for j in range(0,len(Pvalues)):
            interp11PA[j,i] = 100*xinterp11A[Pvalues[j],i]
            interp11PB[j,i] = 100*xinterp11B[Pvalues[j],i]
            interp11PANO[j,i] = 100*xinterp11ANO[Pvalues[j],i]
            interp11PBNO[j,i] = 100*xinterp11BNO[Pvalues[j],i]
    
    
    # Sort data for December
    DecemberS[:,:-1] = np.sort(December, axis=0)
    DecemberS[:,-1] = np.arange(1,JotMonths[11]+1,1)/JotMonths[11] 
    DecemberNOS[:,:-1] = np.sort(DecemberNO, axis=0)
    DecemberNOS[:,-1] = np.arange(1,JotMonths[11]+1,1)/JotMonths[11] 
    
    # Interpolating ECDF curve (input is P-value from vertical axis)
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    xinterp12A = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp12ANO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    xinterp12B = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    xinterp12BNO = np.zeros([len(PvalsNEYS),len(ReferencePeriods)+1])
    # Column 0 Non-Exceedance, Column 1:-1 Persistence
    interp12PA = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp12PANO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    # Column 0 Exceedance, Column 1:-1 Non-Persistence
    interp12PB = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    interp12PBNO = np.zeros([len(Pvalues),len(ReferencePeriods)+1])
    for i in range(0,len(ReferencePeriods)+1):
        xinterp12A[:,i] = np.interp(PvalsNEYS, DecemberS[:,-1], DecemberS[:,i])
        xinterp12B[:,i] = np.sort(1.0-xinterp12A[:,i])
        xinterp12ANO[:,i] = np.interp(PvalsNEYS, DecemberNOS[:,-1], DecemberNOS[:,i])
        xinterp12BNO[:,i] = np.sort(1.0-xinterp12ANO[:,i])
        # Printing the P-values
        # P0 = minimum %, P100 = maximum %
        for j in range(0,len(Pvalues)):
            interp12PA[j,i] = 100*xinterp12A[Pvalues[j],i]
            interp12PB[j,i] = 100*xinterp12B[Pvalues[j],i]
            interp12PANO[j,i] = 100*xinterp12ANO[Pvalues[j],i]
            interp12PBNO[j,i] = 100*xinterp12BNO[Pvalues[j],i]
    
    
    #********* Saving standard P-values in excel, overlapping *********************
    
    # P-values for Non-Exceedance and Persistence Below for each month (all years)
    MonthsPvalsA = [[interp1PA,interp2PA,interp3PA,interp4PA,interp5PA,
                            interp6PA,interp7PA,interp8PA,interp9PA,interp10PA,
                            interp11PA,interp12PA]]
    
    # 3D matrix with results
    MonthsPvalsA = np.vstack(MonthsPvalsA)
    
    # P-values for Exceedance and Non-Persistence Below for each month (all years)
    MonthsPvalsB = [[interp1PB,interp2PB,interp3PB,interp4PB,interp5PB,
                            interp6PB,interp7PB,interp8PB,interp9PB,interp10PB,
                            interp11PB,interp12PB]]
    
    # 3D matrix with results
    MonthsPvalsB = np.vstack(MonthsPvalsB)
    
    # Name of columns in excel
    NameColumns = NameMonths
    
    # List of names of each table in excel (table of P-values and months)
    # The list is comprised first of tables related to workability (Non-Exceedance
    # and Persistence below) and then the ones related to WDT (Exceedance and 
    # Non-Persistence below)
    NameTables = ['Non-Exceedance'] + ['Persistence Below_TR_' + str(ReferencePeriods[i]) for i in range(0,len(ReferencePeriods))] + \
     ['Exceedance'] + ['Non-Persistence Below_TR_' + str(ReferencePeriods[i]) for i in range(0,len(ReferencePeriods))]
    
    # Create the excel workbook and name it
    file_table03 = '03_Monthly P-values_percentages_overlapping.xlsx'
    workbook01 = xlsxwriter.Workbook(os.path.join(tables_directory, file_table03))
    
    # Create the excel sheet where the data will be written
    worksheet1 = workbook01.add_worksheet('Pvals')
    
    # Define cell formatting
    format1 = workbook01.add_format({'bold': 1,'align': 'left'})
    format2 = workbook01.add_format({'bold': 1,'align': 'center'})
    format3 = workbook01.add_format({'num_format': '#,##0.00','align': 'center'})
    
    # Adjust the columns width.
    worksheet1.set_column('A:M', 10)
    
    # Number of tables
    LenColsRepeat = len(NameTables)
    
    # Write the table names and headers (months)
    for i in range(0,LenColsRepeat):
        for j in range(0,NumberOfMonths):
            worksheet1.write(i*(len(Pvalues)+3), 0, NameTables[i], format1)
            worksheet1.write(i*(len(Pvalues)+3)+1, j+1, NameColumns[j], format2)
    
    # Write the name of rows
    for i in range(0,LenColsRepeat):
        for j in range(0,len(Pvalues)):
            worksheet1.write(i*(len(Pvalues)+3)+2+j, 0, 'P' + str(Pvalues[j]), format2)
    
    # Define at which row will the data related to WDT start to be written (Exceedance,
    # Non-Persistence below)
    kstart = (MonthsPvalsA.shape[2]-1)*(len(Pvalues)+3)+2+(MonthsPvalsA.shape[1]-1)+2
    
    # Write the data in the tables for each P-value (rows) and month (columns)
    for i in range(0,MonthsPvalsA.shape[0]):
        for j in range(0,MonthsPvalsA.shape[1]):
            for k in range(0,MonthsPvalsA.shape[2]):
                worksheet1.write(k*(len(Pvalues)+3)+2+j, i+1, MonthsPvalsA[i,j,k], format3)
                worksheet1.write(kstart+k*(len(Pvalues)+3)+2+j, i+1, MonthsPvalsB[i,j,k], format3)
    
    for i in range(0,MonthsPvalsA.shape[2]):
        worksheet1.conditional_format('B' + str(i*(len(Pvalues)+3)+3) + ':M' + str(i*(len(Pvalues)+3)+2+len(Pvalues)), {'type': '3_color_scale',
                                                                                                                        'min_color': "#FF0000",
                                                                                                                        'mid_color': "#FFFF00",
                                                                                                                        'max_color': "#00FF00"})
        worksheet1.conditional_format('B' + str(kstart+i*(len(Pvalues)+3)+3) + ':M' + str(kstart+i*(len(Pvalues)+3)+2+len(Pvalues)), {'type': '3_color_scale',
                                                                                                                        'min_color': "#00FF00",
                                                                                                                        'mid_color': "#FFFF00",
                                                                                                                        'max_color': "#FF0000"})
    
    
    # Close and save the workbook
    workbook01.close()
    
    
    #********* Saving standard P-values in excel, non-overlapping *****************
    
    # P-values for Non-Exceedance and Persistence Below for each month (all years)
    MonthsPvalsANO = [[interp1PANO,interp2PANO,interp3PANO,interp4PANO,interp5PANO,
                            interp6PANO,interp7PANO,interp8PANO,interp9PANO,interp10PANO,
                            interp11PANO,interp12PANO]]
    
    # 3D matrix with results
    MonthsPvalsANO = np.vstack(MonthsPvalsANO)
    
    # P-values for Exceedance and Non-Persistence Below for each month (all years)
    MonthsPvalsBNO = [[interp1PBNO,interp2PBNO,interp3PBNO,interp4PBNO,interp5PBNO,
                            interp6PBNO,interp7PBNO,interp8PBNO,interp9PBNO,interp10PBNO,
                            interp11PBNO,interp12PBNO]]
    
    # 3D matrix with results
    MonthsPvalsBNO = np.vstack(MonthsPvalsBNO)
    
    # Name of columns in excel
    NameColumns = NameMonths
    
    # List of names of each table in excel (table of P-values and months)
    # The list is comprised first of tables related to workability (Non-Exceedance
    # and Persistence below) and then the ones related to WDT (Exceedance and 
    # Non-Persistence below)
    NameTables = ['Non-Exceedance'] + ['Persistence Below_TR_' + str(ReferencePeriods[i]) for i in range(0,len(ReferencePeriods))] + \
     ['Exceedance'] + ['Non-Persistence Below_TR_' + str(ReferencePeriods[i]) for i in range(0,len(ReferencePeriods))]
    
    # Create the excel workbook and name it
    file_table04 = '04_Monthly P-values_percentages_non-overlapping.xlsx'
    workbook02 = xlsxwriter.Workbook(os.path.join(tables_directory, file_table04))
    
    # Create the excel sheet where the data will be written
    worksheet1 = workbook02.add_worksheet('Pvals')
    
    # Define cell formatting
    format1 = workbook02.add_format({'bold': 1,'align': 'left'})
    format2 = workbook02.add_format({'bold': 1,'align': 'center'})
    format3 = workbook02.add_format({'num_format': '#,##0.00','align': 'center'})
    
    # Adjust the columns width.
    worksheet1.set_column('A:M', 10)
    
    # Number of tables
    LenColsRepeat = len(NameTables)
    
    # Write the table names and headers (months)
    for i in range(0,LenColsRepeat):
        for j in range(0,NumberOfMonths):
            worksheet1.write(i*(len(Pvalues)+3), 0, NameTables[i], format1)
            worksheet1.write(i*(len(Pvalues)+3)+1, j+1, NameColumns[j], format2)
    
    # Write the name of rows
    for i in range(0,LenColsRepeat):
        for j in range(0,len(Pvalues)):
            worksheet1.write(i*(len(Pvalues)+3)+2+j, 0, 'P' + str(Pvalues[j]), format2)
    
    # Define at which row will the data related to WDT start to be written (Exceedance,
    # Non-Persistence below)
    kstartNO = (MonthsPvalsANO.shape[2]-1)*(len(Pvalues)+3)+2+(MonthsPvalsANO.shape[1]-1)+2
    
    # Write the data in the tables for each P-value (rows) and month (columns), non-overlapping
    for i in range(0,MonthsPvalsANO.shape[0]):
        for j in range(0,MonthsPvalsANO.shape[1]):
            for k in range(0,MonthsPvalsANO.shape[2]):
                worksheet1.write(k*(len(Pvalues)+3)+2+j, i+1, MonthsPvalsANO[i,j,k], format3)
                worksheet1.write(kstartNO+k*(len(Pvalues)+3)+2+j, i+1, MonthsPvalsBNO[i,j,k], format3)
    
    for i in range(0,MonthsPvalsANO.shape[2]):
        worksheet1.conditional_format('B' + str(i*(len(Pvalues)+3)+3) + ':M' + str(i*(len(Pvalues)+3)+2+len(Pvalues)), {'type': '3_color_scale',
                                                                                                                        'min_color': "#FF0000",
                                                                                                                        'mid_color': "#FFFF00",
                                                                                                                        'max_color': "#00FF00"})
        worksheet1.conditional_format('B' + str(kstartNO+i*(len(Pvalues)+3)+3) + ':M' + str(kstartNO+i*(len(Pvalues)+3)+2+len(Pvalues)), {'type': '3_color_scale',
                                                                                                                        'min_color': "#00FF00",
                                                                                                                        'mid_color': "#FFFF00",
                                                                                                                        'max_color': "#FF0000"})
    
    # Close and save the workbook
    workbook02.close()
    
    
    #********* Plotting the ECDF Non-Exceedance January (all years) ***************
    
    # fig41 = plt.figure(figsize=(8, 8))
    # ax41 = fig41.add_subplot(211)
    # ax41.set_title(f'P-value Non-Exceedance plot for {NameMonths[0]}')
    # ax41.plot(100*JanuaryS[:,0],JanuaryS[:,-1],color=colors[:,0])
    # ax41.fill_between(100*JanuaryS[:,0],JanuaryS[:,-1], color=colors[:,0], alpha=0.5)
    # ax41.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
    # ax41.grid(color='grey', linestyle='--', linewidth=0.5)
    # ax41.set_ylabel('P-value')
    # ax41.set_xlabel('Time %')
    # plt.savefig(f'08_01_NonExceedance_{NameMonths[0]}.jpg', dpi=100)
    
    
    if PlottingMonthlyPvals == 1:
       
        #********* Plotting NE and Persistence (below) January (all years) ***************
        
        colors1 = np.random.rand(3,len(ReferencePeriods)+1)
        
        fig10a = plt.figure(figsize=(8, 8))
        ax10a = fig10a.add_subplot(211)
        for i in range(0,len(ReferencePeriods)+1):
            ax10a.set_title(f'P-value plot for {NameMonths[0]} (overlapping)')
            if i == 0:
                ax10a.plot(100*JanuaryS[:,i],JanuaryS[:,-1],color=colors1[:,i], label='Non-Exceedance')
            else:
                ax10a.plot(100*JanuaryS[:,i],JanuaryS[:,-1],color=colors1[:,i], label=f'Ref_period_{ReferencePeriods[i-1]} hrs (overlapping)')
            ax10a.fill_between(100*JanuaryS[:,i],JanuaryS[:,-1], color=colors1[:,i], alpha=0.5)
        ax10a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
        ax10a.grid(color='grey', linestyle='--', linewidth=0.5)
        ax10a.set_ylabel('P-value')
        ax10a.set_xlabel('Time %')
        fig_name10a = f'10a_P-value_{NameMonths[0]}_overlapping.jpg'
        fig_path10a = os.path.join(figures_directory, fig_name10a)
        plt.savefig(fig_path10a, dpi=100, bbox_inches='tight')
        
        #********* Plotting NE and Persistence (below) February (all years) ***************
       
        fig11a = plt.figure(figsize=(8, 8))
        ax11a = fig11a.add_subplot(211)
        
        for i in range(0,len(ReferencePeriods)+1):
            ax11a.set_title(f'P-value plot for {NameMonths[1]} (overlapping)')
            if i == 0:
                ax11a.plot(100*FebruaryS[:,i],FebruaryS[:,-1],color=colors1[:,i], label='Non-Exceedance')
            else:
                ax11a.plot(100*FebruaryS[:,i],FebruaryS[:,-1],color=colors1[:,i], label=f'Ref_period_{ReferencePeriods[i-1]} hrs (overlapping)')
            ax11a.fill_between(100*FebruaryS[:,i],FebruaryS[:,-1], color=colors1[:,i], alpha=0.5)
        ax11a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
        ax11a.grid(color='grey', linestyle='--', linewidth=0.5)
        ax11a.set_ylabel('P-value')
        ax11a.set_xlabel('Time %')
        fig_name11a = f'11a_P-value_{NameMonths[1]}_overlapping.jpg'
        fig_path11a = os.path.join(figures_directory, fig_name11a)
        plt.savefig(fig_path11a, dpi=100, bbox_inches='tight')
        
        #********* Plotting NE and Persistence (below) March (all years) ***************
        
        fig12a = plt.figure(figsize=(8, 8))
        ax12a = fig12a.add_subplot(211)
        
        for i in range(0,len(ReferencePeriods)+1):
            ax12a.set_title(f'P-value plot for {NameMonths[2]} (overlapping)')
            if i == 0:
                ax12a.plot(100*MarchS[:,i],MarchS[:,-1],color=colors1[:,i], label='Non-Exceedance')
            else:
                ax12a.plot(100*MarchS[:,i],MarchS[:,-1],color=colors1[:,i], label=f'Ref_period_{ReferencePeriods[i-1]} hrs (overlapping)')
            ax12a.fill_between(100*MarchS[:,i],MarchS[:,-1], color=colors1[:,i], alpha=0.5)
        ax12a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
        ax12a.grid(color='grey', linestyle='--', linewidth=0.5)
        ax12a.set_ylabel('P-value')
        ax12a.set_xlabel('Time %')
        fig_name12a = f'12a_P-value_{NameMonths[2]}_overlapping.jpg'
        fig_path12a = os.path.join(figures_directory, fig_name12a)
        plt.savefig(fig_path12a, dpi=100, bbox_inches='tight')
        
        #********* Plotting NE and Persistence (below) April (all years) ***************
        
        fig13a = plt.figure(figsize=(8, 8))
        ax13a = fig13a.add_subplot(211)
        
        for i in range(0,len(ReferencePeriods)+1):
            ax13a.set_title(f'P-value plot for {NameMonths[3]} (overlapping)')
            if i == 0:
                ax13a.plot(100*AprilS[:,i],AprilS[:,-1],color=colors1[:,i], label='Non-Exceedance')
            else:
                ax13a.plot(100*AprilS[:,i],AprilS[:,-1],color=colors1[:,i], label=f'Ref_period_{ReferencePeriods[i-1]} hrs (overlapping)')
            ax13a.fill_between(100*AprilS[:,i],AprilS[:,-1], color=colors1[:,i], alpha=0.5)
        ax13a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
        ax13a.grid(color='grey', linestyle='--', linewidth=0.5)
        ax13a.set_ylabel('P-value')
        ax13a.set_xlabel('Time %')
        fig_name13a = f'13a_P-value_{NameMonths[3]}_overlapping.jpg'
        fig_path13a = os.path.join(figures_directory, fig_name13a)  
        plt.savefig(fig_path13a, dpi=100, bbox_inches='tight')
        
        #********* Plotting NE and Persistence (below) May (all years) ***************
        
        fig14a = plt.figure(figsize=(8, 8))
        ax14a = fig14a.add_subplot(211)
        
        for i in range(0,len(ReferencePeriods)+1):
            ax14a.set_title(f'P-value plot for {NameMonths[4]} (overlapping)')
            if i == 0:
                ax14a.plot(100*MayS[:,i],MayS[:,-1],color=colors1[:,i], label='Non-Exceedance')
            else:
                ax14a.plot(100*MayS[:,i],MayS[:,-1],color=colors1[:,i], label=f'Ref_period_{ReferencePeriods[i-1]} hrs (overlapping)')
            ax14a.fill_between(100*MayS[:,i],MayS[:,-1], color=colors1[:,i], alpha=0.5)
        ax14a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
        ax14a.grid(color='grey', linestyle='--', linewidth=0.5)
        ax14a.set_ylabel('P-value')
        ax14a.set_xlabel('Time %')
        fig_name14a = f'14a_P-value_{NameMonths[4]}_overlapping.jpg'
        fig_path14a = os.path.join(figures_directory, fig_name14a)
        plt.savefig(fig_path14a, dpi=100, bbox_inches='tight')
        
        #********* Plotting NE and Persistence (below) June (all years) ***************
        
        fig15a = plt.figure(figsize=(8, 8))
        ax15a = fig15a.add_subplot(211)
        
        for i in range(0,len(ReferencePeriods)+1):
            ax15a.set_title(f'P-value plot for {NameMonths[5]} (overlapping)')
            if i == 0:
                ax15a.plot(100*JuneS[:,i],JuneS[:,-1],color=colors1[:,i], label='Non-Exceedance')
            else:
                ax15a.plot(100*JuneS[:,i],JuneS[:,-1],color=colors1[:,i], label=f'Ref_period_{ReferencePeriods[i-1]} hrs (overlapping)')
            ax15a.fill_between(100*JuneS[:,i],JuneS[:,-1], color=colors1[:,i], alpha=0.5)
        ax15a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
        ax15a.grid(color='grey', linestyle='--', linewidth=0.5)
        ax15a.set_ylabel('P-value')
        ax15a.set_xlabel('Time %')
        fig_name15a = f'15a_P-value_{NameMonths[5]}_overlapping.jpg'
        fig_path15a = os.path.join(figures_directory, fig_name15a)
        plt.savefig(fig_path15a, dpi=100, bbox_inches='tight')
        
        #********* Plotting NE and Persistence (below) July (all years) ***************
        
        fig16a = plt.figure(figsize=(8, 8))
        ax16a = fig16a.add_subplot(211)
        
        for i in range(0,len(ReferencePeriods)+1):
            ax16a.set_title(f'P-value plot for {NameMonths[6]} (overlapping)')
            if i == 0:
                ax16a.plot(100*JulyS[:,i],JulyS[:,-1],color=colors1[:,i], label='Non-Exceedance')
            else:
                ax16a.plot(100*JulyS[:,i],JulyS[:,-1],color=colors1[:,i], label=f'Ref_period_{ReferencePeriods[i-1]} hrs (overlapping)')
            ax16a.fill_between(100*JulyS[:,i],JulyS[:,-1], color=colors1[:,i], alpha=0.5)
        ax16a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
        ax16a.grid(color='grey', linestyle='--', linewidth=0.5)
        ax16a.set_ylabel('P-value')
        ax16a.set_xlabel('Time %')
        fig_name16a = f'16a_P-value_{NameMonths[6]}_overlapping.jpg'
        fig_path16a = os.path.join(figures_directory, fig_name16a)
        plt.savefig(fig_path16a, dpi=100, bbox_inches='tight')
        
        #********* Plotting NE and Persistence (below) August (all years) ***************
        
        fig17a = plt.figure(figsize=(8, 8))
        ax17a = fig17a.add_subplot(211)
        
        for i in range(0,len(ReferencePeriods)+1):
            ax17a.set_title(f'P-value plot for {NameMonths[7]} (overlapping)')
            if i == 0:
                ax17a.plot(100*AugustS[:,i],AugustS[:,-1],color=colors1[:,i], label='Non-Exceedance')
            else:
                ax17a.plot(100*AugustS[:,i],AugustS[:,-1],color=colors1[:,i], label=f'Ref_period_{ReferencePeriods[i-1]} hrs (overlapping)')
            ax17a.fill_between(100*AugustS[:,i],AugustS[:,-1], color=colors1[:,i], alpha=0.5)
        ax17a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
        ax17a.grid(color='grey', linestyle='--', linewidth=0.5)
        ax17a.set_ylabel('P-value')
        ax17a.set_xlabel('Time %')
        fig_name17a = f'17a_P-value_{NameMonths[7]}_overlapping.jpg'
        fig_path17a = os.path.join(figures_directory, fig_name17a)
        plt.savefig(fig_path17a, dpi=100, bbox_inches='tight')
        
        #********* Plotting NE and Persistence (below) September (all years) ***************
        
        fig18a = plt.figure(figsize=(8, 8))
        ax18a = fig18a.add_subplot(211)
        
        for i in range(0,len(ReferencePeriods)+1):
            ax18a.set_title(f'P-value plot for {NameMonths[8]} (overlapping)')
            if i == 0:
                ax18a.plot(100*SeptemberS[:,i],SeptemberS[:,-1],color=colors1[:,i], label='Non-Exceedance')
            else:
                ax18a.plot(100*SeptemberS[:,i],SeptemberS[:,-1],color=colors1[:,i], label=f'Ref_period_{ReferencePeriods[i-1]} hrs (overlapping)')
            ax18a.fill_between(100*SeptemberS[:,i],SeptemberS[:,-1], color=colors1[:,i], alpha=0.5)
        ax18a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
        ax18a.grid(color='grey', linestyle='--', linewidth=0.5)
        ax18a.set_ylabel('P-value')
        ax18a.set_xlabel('Time %')
        fig_name18a = f'18a_P-value_{NameMonths[8]}_overlapping.jpg'
        fig_path18a = os.path.join(figures_directory, fig_name18a)
        plt.savefig(fig_path18a, dpi=100, bbox_inches='tight')
        
        #********* Plotting NE and Persistence (below) October (all years) ***************
        
        fig19a = plt.figure(figsize=(8, 8))
        ax19a = fig19a.add_subplot(211)
        
        for i in range(0,len(ReferencePeriods)+1):
            ax19a.set_title(f'P-value plot for {NameMonths[9]} (overlapping)')
            if i == 0:
                ax19a.plot(100*OctoberS[:,i],OctoberS[:,-1],color=colors1[:,i], label='Non-Exceedance')
            else:
                ax19a.plot(100*OctoberS[:,i],OctoberS[:,-1],color=colors1[:,i], label=f'Ref_period_{ReferencePeriods[i-1]} hrs (overlapping)')
            ax19a.fill_between(100*OctoberS[:,i],OctoberS[:,-1], color=colors1[:,i], alpha=0.5)
        ax19a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
        ax19a.grid(color='grey', linestyle='--', linewidth=0.5)
        ax19a.set_ylabel('P-value')
        ax19a.set_xlabel('Time %')
        fig_name19a = f'19a_P-value_{NameMonths[9]}_overlapping.jpg'
        fig_path19a = os.path.join(figures_directory, fig_name19a)
        plt.savefig(fig_path19a, dpi=100, bbox_inches='tight')
        
        #********* Plotting NE and Persistence (below) November (all years) ***************
        
        fig20a = plt.figure(figsize=(8, 8))
        ax20a = fig20a.add_subplot(211)
        
        for i in range(0,len(ReferencePeriods)+1):
            ax20a.set_title(f'P-value plot for {NameMonths[10]} (overlapping)')
            if i == 0:
                ax20a.plot(100*NovemberS[:,i],NovemberS[:,-1],color=colors1[:,i], label='Non-Exceedance')
            else:
                ax20a.plot(100*NovemberS[:,i],NovemberS[:,-1],color=colors1[:,i], label=f'Ref_period_{ReferencePeriods[i-1]} hrs (overlapping)')
            ax20a.fill_between(100*NovemberS[:,i],NovemberS[:,-1], color=colors1[:,i], alpha=0.5)
        ax20a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
        ax20a.grid(color='grey', linestyle='--', linewidth=0.5)
        ax20a.set_ylabel('P-value')
        ax20a.set_xlabel('Time %')
        fig_name20a = f'20a_P-value_{NameMonths[10]}_overlapping.jpg'
        fig_path20a = os.path.join(figures_directory, fig_name20a)
        plt.savefig(fig_path20a, dpi=100, bbox_inches='tight')
        
        #********* Plotting NE and Persistence (below) December (all years) ***************
        
        fig21a = plt.figure(figsize=(8, 8))
        ax21a = fig21a.add_subplot(211)
        
        for i in range(0,len(ReferencePeriods)+1):
            ax21a.set_title(f'P-value plot for {NameMonths[11]} (overlapping)')
            if i == 0:
                ax21a.plot(100*DecemberS[:,i],DecemberS[:,-1],color=colors1[:,i], label='Non-Exceedance')
            else:
                ax21a.plot(100*DecemberS[:,i],DecemberS[:,-1],color=colors1[:,i], label=f'Ref_period_{ReferencePeriods[i-1]} hrs (overlapping)')
            ax21a.fill_between(100*DecemberS[:,i],DecemberS[:,-1], color=colors1[:,i], alpha=0.5)
        ax21a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)
        ax21a.grid(color='grey', linestyle='--', linewidth=0.5)
        ax21a.set_ylabel('P-value')
        ax21a.set_xlabel('Time %')
        fig_name21a = f'21a_P-value_{NameMonths[11]}_overlapping.jpg'
        fig_path21a = os.path.join(figures_directory, fig_name21a)
        plt.savefig(fig_path21a, dpi=100, bbox_inches='tight')
    
     
    """
    Notes:
    Additionally, the following can be added in this step:
        1. Bar plot for Persistence above a treshold limit for each month
        2. P-value plot for Persistence above a treshold limit for each month
        3. Delay/Waiting Time statistics by finding the mean duration of the 
        individual non-working intervals for each month
        4. Counting the number of occurances of weather window >= reference period
        in each month for all years
        5. Code simplification by using only years with complete datasets
    
    Finally, the ENTIRE CODE can be adjusted to use user-defined set of 
    metocean limits for each operation, create folders named by each combination
    of limits and save all figures in subfolders. Morevoer, the data for each
    combination can be stored in a multidimensional matrix and some comparisons
    can be made.
    
    """
    
    """
    
    # Plotting table to check the procedure
    
    end0 = time.time()
    seconds0 = end0 - start0
    print('Time to complete: ' + str(round(seconds0,2)) + 's')
    
    
    # Names of the rows of the table
    NameRowsPvals2 = NameMonths
    
    # Names of the columns of the table
    NameColumns2 = ['Year','Month','Day','Hour','Wind speed','Wave Height','Wave Period','Current Speed',
                    '< Wind limit?','<Wave limit?','<Period limit?','<Current limit?','<ALL limits?'] + \
        ['TR_overlapping_'+str(x) for x in ReferencePeriods] + ['TR_non-overlapping_'+str(x) for x in ReferencePeriods]
    
    # Data to save
    DataToSave = np.concatenate((data,NonExceedance,PersistenceBelow,PersistenceBelowNO),axis=1)
    
    df_DataToSave = pd.DataFrame(DataToSave, columns=NameColumns2)
    
    # Create excel writer object
    writer = pd.ExcelWriter('DataToSave.xlsx')
    
    # Write dataframe to excel
    df_DataToSave.to_excel(writer)
    
    # Save the excel
    writer.save()
    print('DataFrame for months all years is written successfully to Excel File.')
    
    """






