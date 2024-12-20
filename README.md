# copchlhandler
A package for handling chlorophyll data from Copernicus Marine Service:
-  handles reading and downloading chlorophyll data from Copernicus Marine Service
-  logs info about chlorophyll data structure (dimensions, variables, resolution, etc.)
-  contains plotting functions for visualizing datasets

**Note:**
*`copchlhandler` was developed by Cian Kelly (ciank94) in 2025 to handle a few personal projects. There are probably bugs, and this package is not intended for production use. It is still in development.*

## catalogue
To find relevant chlorophyll observation data, search [Product User Manual](https://documentation.marine.copernicus.eu/PUM/CMEMS-OC-PUM.pdf) with string: 
`**cmems_obs-oc_glo_bgc-plankton**`. At time of writing, 17 relevant datasets were found. Check `usage/catalog.txt` for a list of datasets handled.
\n
Check the following before requesting data:
-  check if prefix matches: cmems_obs-oc_glo_bgc-plankton
-  check if frequency of data is daily (P1D) or monthly (P1M) 
-  check if satellite product is level 3 (l3) or level 4 (l4)
-  check if dataset is near-real-time (nrt) or multi-year (my) (if nrt year should be >= 2023-04-05 as of writing)
- check if dateset is multi-climatology: coordinates could be between [2008-01-01 00:00:00, 2008-12-31 00:00:00] for some datasets
- check if resolution is 4km or 300m
- check Part II: Description of the Product Specification in [Product User Manual](https://documentation.marine.copernicus.eu/PUM/CMEMS-OC-PUM.pdf) for more information

## installation:
-  clone the repository:
```bash
git clone https://github.com/ciank94/copData.git
```
-  navigate to the root directory (`path/to/copData/`)
-  Installation options:
  ```bash
  # Install with pip in non-editable mode
  python -m pip install .
  
  # Install with pip in editable mode
  python -m pip install -e .
  
  # Install with poetry (wsl)
  poetry install
  ```
-  **Note:**
*`copernicusmarine` is a python package for accessing Copernicus Marine Service data. Check `/pyproject.toml` for version information if there are any issues with dependencies and raise them on github. Also check the [Copernicus Marine Toolbox](https://help.marine.copernicus.eu/en/articles/7949409-copernicus-marine-toolbox-introduction) documentation.*
## setup
1. To use package, use or register account details with [Copernicus Marine Service](https://marine.copernicus.eu/) and login with the following command (once off):
```python
import copernicusmarine as cop
cop.login()
```
and this will store credentials in a .copernicusmarine-credentials file that is printed to the terminal. For example, the file could be in the following paths (check directory for linux/ windows):
```python
configure_path = f'/home/{username}/.copernicusmarine/.copernicusmarine-credentials' # wsl/linux
configure_path = f'C:/Users/{username}/.copernicusmarine/.copernicusmarine-credentials' # windows
```
**Note:** login is only required once.
2. Create a folder for storing input (netcdf files) and output (log files) named `input_files` and `output_files` in project root directory:
```bash
mkdir ./input_files
mkdir ./output_files
```	
- netcdf files will be downloaded to the `input_files` folder with the filename `{chl}_{resolution}_{date_start}.nc` where `{resolution}` is the resolution of the dataset (4km for 4km, .3k for 300m), and `{date_start}` is the start date of the dataset (yyyy-mm-dd). Note: netcdf files are not downloaded if they already exist in the `input_files` folder. Note: if trying to download a new file with the same start date but different end date the file will not be downloaded.
- log files produced from running scripts will be created in the `output_files` folder with the filename `copRequest.py_{chl}_{resolution}_{date_start}.log`. The logger uses the python `logging` module with a custom format. Note: if the netcdf file already exists or there is an error/ issue downloading the netcdf file, the log file name will be `copRequest.py_{exit}.log`.

## usage
In `usage` folder, there are examples of how to use the package. There are three types of usage:
1. `request_{experiment_name}` usage which requests chlorophyll data from Copernicus Marine Service
2. `process_{experiment_name}` usage which checks coordinates, time, variables, and frequency of chlorophyll data and processes it if in expected format.
3. `plot_{experiment_name}` usage which plots chlorophyll data with coastlines and geographic features.



