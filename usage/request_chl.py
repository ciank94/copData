from copchlhandler import *

#================test parameters================
dataID = 'cmems_obs-oc_glo_bgc-plankton_my_l4-multi-climatology-4km_P1D'
#configure_path = '/home/ciank/.copernicusmarine/' # wsl
configure_path = 'C:/Users/ciank/.copernicusmarine/' # windows
input_path = 'input_files'
output_path = 'output_files'
start_date = "2005-12-18T00:00:00"
end_date = "2005-12-19T00:00:00"
lon_bounds = [-70, -31]
lat_bounds = [-73, -50]

#================parse file================
parse_file = checkRequest(dataID, output_path) # based on class

#================configure================
config = requestConfig(parse_file)
config.configure_path(configure_path, input_path)
config.configure_time(start_date, end_date)
config.configure_domain(lon_bounds, lat_bounds)
config.configure_variable(variables=['CHL'])

#================request data================
requestData(config)


