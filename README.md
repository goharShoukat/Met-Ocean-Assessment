# Met Ocean Assessment 
This tool is designed to automate the process of met ocean assessments for a site's energy resource assessment and to provide a starting point for a more detailed analyses. The user can clone the repository using the following command from the terminal: 

git clone https://github.com/goharShoukat/Met-Ocean-Assessment.git

Occasionaly, use the command from your terminal after entering the folder where the repositor was cloned:
git pull

This automatically updates the library and provides all new functionalities that the contributors have included. 

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
- The user can study a bounded region.
- Evaluate data at a single coordinate.

For a bounded region, the user will need to use the following two functions:
bounded_region() - this function takes the two opposite vertices. The bounded region can only be in the shape of rectange
load_bounded_region() - this function then extracts the information about the three variables - swh, mwp and mwd. For now this is hardcoded. 

The code also provides additional features to carry out data extraction for a signle data point throught the function:
- load_coordinate_data() - this function requires the user to input the longitude and latitude of the point of interest. If the coordinates do not snap to a grid point, the function calculates the nearest neighour and uses the data for that particular point. 
- It also informs the user of the distance between the specified point and the one being used. 

This class takes in a number of arguments. All these make it extremely important that each argument passed down is referenced with the variable definition as defined in the class. 

The structure of the code is kept basic for ease of editing. The three variables obtained from netcdf files - 'swh', 'mwd', 'mwp', are hard coded for now. It is important therefore that any input file must have these 3 variables. Future iterations will make the code more generalisable and will provide all class functionalities for any available key within the netcdf file.

It is also important to note that the data files should all be homogenous. That is, they should have the same spatial resolution and have the same latitudnal and longitudnal coverage. The code can not adjust to varying coverage across data files.  
### Windows Users:
The code is hard coded to avoid an hidden or cached files which maybe included within the directory folder passed on as an argument to the program. There is a chance that the first data file might be missing in the output csv. Please flag this issue if you encounter it by opening up an issue. We will resolve it in the next iteration. 
