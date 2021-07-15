# Met Ocean Assessment 
This tool is designed to automate the process of met ocean assessments for a site's energy resource assessment and to provide a starting point for a more detailed analyses. The user can clone the repository using the following command from the terminal: 
git clone https://github.com/goharShoukat/Met-Ocean-Assessment.git
The above command can work if git is installed. This is the recommended cloning methodology as the users can get very conveniently download any updates to the software. The other optino is to manually clone the repository through github itself. On the top right corner, there is an option to clone the repository. Any updates to the software will have to be downloaded manually as well which can be quite cumbersome. 

Occasionaly, use the command from your terminal after entering the folder where the repositor was cloned:
git pull.
This automatically updates the library and provides all new functionalities that the contributors have included. For the two commands stated above to work with the terminal, 'git' has to be installed in your system. If it isn't, then manually clone the repository from Github. This however means that every time you wish to sync the repository with the source code, a manual download will be required which can lead to loss of old data files.  

This tool is designed to run with Python 3.7 and above. The following additional  libraries are needed to successfully run this program:
- Netfcdf4
- Cartopy
- PyQt5
- datetime
- haversine
The other libraries required come preinstalled with your Python installation. We recommend you use Anaconda's version of Spyder to use Python. The libraries mentioned above can then be installed using the commands below from spyder's terminal:
- $ pip install netcdf4
- $ pip install cartopy
- $ pip install pyqt5 
- $ pip install haversine

Please be warned that downloading and installing libraries from Spyder's terminal may break the dependencies of your pre-existing libraries that come with Anaconda. Please open an issue and let us know if this is the case. 

The tool can be used with both Windows and Mac OS. Any changes to this will be highlighted in the documentation. 

## Version 0:
This is the first release and a test bed. This version will house all the scripts for the assessments. Initially, the user will have to interact with the code by declaring an instance of the class and passing on arguments. The following inputs are required:
- Directory housing the ERA5 datasets

The code provides multiple functionalities to the user:
- Evaluate data at a single coordinate.
- Extract information about a single variable or multiple variables. 
- Specify a coordinate of interest and the software will check if the point specified is present within the dataset. If not, it will automatically snap to the nearest grid point. 
- Provides information about the distance between the nearest grid point and the point specified by the user. 
- Provides information about individual availability of each variable the user has chosen.
- If the availability is low, the software provides option to look at grid points further apart and then alter the coordinate the user wants to extract information for. 
- Provides the user with the option to chose between all the variables contained within the data files.
- If a critical variable (hard coded and can be changed) is missing, the software throws a warning. These critical variables are the ones that will be useful in generating the plots which will follow this software. 

For the single point data extraction, the code flows in a sequential model, a sample of which is given in the foler 'tests' under the name run_code.py:
- First, the data files are loaded and unpacked into a 3D array
- Then the user specifies the coordinate of interest and the function nearest_point is called which compares the coordinate with the data base. 
- Finally, the 3D array and the nearest coordinates are passed on to the function extract_coordinate_data which provides the formatted files. 

Version 0 comes with a wrapper function that allows the code to run using a CLI. The file name run_code.py should be executed to allow for an interactive CLI based environment. The user can still use his/her own workflow by using the ERA5 class. For that, please go over the next more detailed section which covers each individual function. 

To launch the program, the user must have a datafolder which contains only the datafiles. After entering the folder src from the command prompt, execute the python script run_code.py
To save the data, provide a name of the directory where the results have to be saved. If the directory doesn't exist, a new one by the same name entered by the user will be created. The csv files will be written using the current date and time to avoid overwriting in case the user wishes to extract information for multiple coordinates in the same directory. 

## Functions 
Under this section, we will cover each function available within the ERA5 class, specify the inputs and outputs for them and the datatypes. 


This class takes in a number of arguments. All these make it extremely important that each argument passed down is referenced with the variable definition as defined in the class. 

class ERA5():
An ERA5 instance is a collection of dimensions, groups, variables and atttributes that together define the data contained within a netcdf4 file downloaded from the copernicus website between the range 1979 - 2019. 

- ERA5()
	__init__(self, directory)
		This is the initialization function. To declare an instance of the class ERA5, call the class from the library ERA5 and pass on the directory containing the datafiles. Please note that this function might need to be adjusted for Windows based handling. If any datafile is missing from the output, please notify the developers.
		This function only takes in one string input and has no output.  
- def load_variable(self, variable_list):
	This function is used to extract 3D arrays from the raw netcdf files. It reads in the entire input file but only extracts - as 3D arrays, information about variables which the user asks for. 
	The input for this function is a numpy array: numpy.ndarray, created from the user input. The input is casted astype numpy.ndarray from a list. It is then passed on as an argument to this function. 
	The output of this function is a data structure of type - dict. This dict contains the following data. Also mentioned here is the individual data type of each element within the dictionary:
        time : Masked array of strings : contains the array of the time
        latitude : numpy.ndarray of float : array of latitude
        longitude : numpy.ndarray of float : array of longitude
        variable : numpy.ndarray of float : array of the extracted data
        lenght :numpy.ndarray of  int : length of each file. needed to split the data in another function
	Units : pandas.DataFrame : dataframe of the units of the variables chosen by the user. Can be referenced by the variable itself. 

	Note: This function scans the entire datafile for the given variable and extracts information contained within it for all available coordinates. Further filtering is done by the next function. 

- def extract_coordinate_data(self, variable, lat_idx = False, lon_idx = False):
	This function takes the dictionary created by the previous function and extracts data for a given coordinate. The dictionary is not one of the input arguments. The dictionary is key to the entire structure of the code and is self referenced throughout the class. As such, all methods  of this class will be able to access it. 
	The following are the input parameters and the expected data type: 
	variables : numpy.ndarray of string : variable for which the data has to be extracted
        lat_idx / lon_idx : float : under normal circumstances, these will be self transmitted to the function
        the index of the latitude and longitude need to be transmitted
        the actual longitude and latitude need not be mentioned
        neighouring_cells_request_active : boolean : this will be true only when we are exploring neighouring cells
        the neighouring_cells_request_active : remain false when multiple variables are being querried
        important to include this here because this function will be called in the function explore_more_points. 
        however, this function also has a call to this very function. 
        to prevent from getting stuck in an infinite loop, this argument is added. 
        


output
        dataframe of the variable data along with the time and lan and lat information
        availability at this point
         




### Warnings:
It is also important to note that the data files should all be homogenous. That is, they should have the same spatial resolution and have the same latitudnal and longitudnal coverage. The code can not adjust to varying coverage across data files.  

The Netcdf4 files used as sample data for this code have variables written to the raw files with a fill_value = -32767. When unpacking these variables into an array, the empty cells are automatically filled with the stated fill value. However, this fill value may not always be used by the raw files or might have a different value altogether. This will have to be adjusted manually. 

The algorithm for Version 0 is written with the end product in mind. The user might at times have to locate the index of the latitude and longitude of the point of interest and pass the indices into the function. One function which might present a challenge when availability for the default location is low is the extract_coordinate_data(). While this function under normal circumstances does not need any arguments to be passed on at all, when the availibility for the data point is low, some sort of interaction might be needed. This however, is kept to a minimum. 
### Windows Users:
The code is hard coded to avoid an hidden or cached files which maybe included within the directory folder passed on as an argument to the program. There is a chance that the first data file might be missing in the output csv. Please flag this issue if you encounter it by opening up an issue. We will resolve it in the next iteration. 
