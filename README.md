# copchlhandler
A package for handling chlorophyll data from Copernicus Marine Service:
-  handles reading and downloading chlorophyll data from Copernicus Marine Service
-  logs info about chlorophyll data structure
-  contains plotting functions for visualizing datasets

**Note:**
*`copchlhandler` was developed by Cian Kelly (ciank94) in 2025 to handle a few personal projects. There are probably bugs, and this package is not intended for production use. It is still in development, but may be useful for other users.*

## catalogue
To find relevant chlorophyll observation data, search https://documentation.marine.copernicus.eu/PUM/CMEMS-OC-PUM.pdf with string: 
`**cmems_obs-oc_glo_bgc-plankton**`. At time of writing, 17 relevant datasets were found.\n
check the following before requesting data:
-  check if prefix matches: cmems_obs-oc_glo_bgc-plankton
-  check frequency of data (daily or monthly)
-  check if satellite product is level 3 (l3) or level 4 (l4)
-  check if dataset is near-real-time (nrt) or multi-year (my) (if nrt year should be >= 2023-04-05 as of writing)
- check if resolution is 4km (4km) or 300m (300m)

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
*`copernicusmarine` is a python package for accessing Copernicus Marine Service data. Check `/pyproject.toml` for version information if there are any issues with dependencies and raise them on github.*

## setup
1. To use package, register account with Copernicus Marine Service at https://marine.copernicus.eu/ and login with the following command (once off):
```python
import copernicusmarine as cop
cop.login()
```
and this will store credentials in a .copernicusmarine-credentials file which may be found in the following paths (check directory for linux/ windows):
```python
configure_path = f'/home/{username}/.copernicusmarine/.copernicusmarine-credentials' # wsl/linux
configure_path = f'C:/Users/{username}/.copernicusmarine/.copernicusmarine-credentials' # windows
```
login is only required once.
2. Create a folder for storing input (netcdf files) and output (log files) named `input_files` and `output_files` in project root directory:
```bash
mkdir ./input_files
mkdir ./output_files
```	
- todo: naming of netcdf files
- The log files will be created in the `output_files` folder with the filename `{module_name}.log`

## usage
In `usage` folder, there are examples of how to use the package. There are three types of usage:
1. `request_{experiment_name}` usage which requests chlorophyll data from Copernicus Marine Service
2. `process_{experiment_name}` usage which checks coordinates, time, variables, and frequency of chlorophyll data and processes it if in expected format.
3. `plot_{experiment_name}` usage which plots chlorophyll data with coastlines and geographic features.



