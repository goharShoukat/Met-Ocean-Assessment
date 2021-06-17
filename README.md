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

The other libraries required come preinstalled with your Python installation. We recommend you use Anaconda's version of Spyder to use Python. The libraries mentioned above can then be installed using the commands below from spyder's terminal:
- $ pip install netcdf4
- $ pip install cartopy
- $ pip install pyqt5 

Please be warned that downloading and installing libraries from Spyder's terminal may break the dependencies of your pre-existing libraries that come with Anaconda. Please open an issue and let us know if this is the case. 

The tool can be used with both Windows and Mac OS. Any changes to this will be highlighted in the documentation. 

## Version 0:
This is the first release and a test bed. This version will house all the scripts for the assessments. Initially, the user will have to interact with the code by declaring an instance of the class and passing on arguments. The following inputs are required:

- Longitudnal boundaries
- Latitudnal boundaries
- Map type - Orthographic or Platecarre
- Path to save the time series data
- Path to save the Images
- Video output of the time series - True or False


 
