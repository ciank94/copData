# copChlHandler
A package for handling chlorophyll data from Copernicus Marine Service:
-  handles reading and downloading chlorophyll data from Copernicus Marine Service
-  handles checks for chlorophyll data
-  contains plotting functions for visualizing datasets

**Note:**
*`copChlHandler` was developed by Cian Kelly (ciank94) in 2025 to handle a few personal projects. There are probably bugs, and this package is not intended for production use. It is still in development, but may be useful for other researchers.*

## catalogue
To find relevant chlorophyll observation data, search https://documentation.marine.copernicus.eu/PUM/CMEMS-OC-PUM.pdf with string: 
`**cmems_obs-oc_glo_bgc-plankton**`. At time of writing, 17 relevant datasets were found.

## installation:
-  clone the repository:
```bash
git clone https://github.com/ciank94/copData.git
```
-  navigate to the root directory (`path/to/copData/`)
-  install with pip in non-editable mode:
```bash
python -m pip install .
```
-  install with pip in editable mode:
```bash
python -m pip install -e .
```
-  install with poetry (wsl):
```bash
poetry install
```

**Note:**
*`copernicusmarine` is a python package for accessing Copernicus Marine Service data. Check `copData/pyproject.toml` for version information if there are any issues with dependencies and raise them on github.*

## setup
1. To use `copChlHandler` modules in `copData/`, you need to log into the Copernicus Marine Service using the following command:
```python
import copernicusmarine as cop
cop.login()
```
and this will store credentials in a .copernicusmarine-credentials file which may be found in the following paths (check directory for linux/ windows):
```python
configure_path = f'/home/{username}/.copernicusmarine/.copernicusmarine-credentials' # wsl/linux
configure_path = f'C:/Users/{username}/.copernicusmarine/.copernicusmarine-credentials' # windows
```

2. Create a folder for storing input (netcdf files) and output (log files) named `input_files` and `output_files`:
```bash
mkdir copData/input_files
mkdir copData/output_files
```	




