# copData
copernicus marine service data pull

## setup
To use copData, you need to log into the Copernicus Marine Service using the following command:
```python
import copernicusmarine as cop
cop.login()
```
and this will store credentials in a .copernicusmarine-credentials file:
```python
configure_path = f'/home/{username}/.copernicusmarine/.copernicusmarine-credentials'
```
or 
```python
configure_path = f'C:/Users/{username}/.copernicusmarine/.copernicusmarine-credentials'
```
where username is replaced with your username.

## catalogue
To find relevant chlorophyll data, it's probably easiest to search the string: 
`**cmems_obs-oc_glo_bgc-plankton**` in https://documentation.marine.copernicus.eu/PUM/CMEMS-OC-PUM.pdf

