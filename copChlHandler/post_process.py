from numpy import shape
import xarray as xr
from copChlHandler import LoggerConfig
# test
class inspectDataStructure:
    def __init__(self, dataset_path, output_path):
        self.logger = LoggerConfig(output_path, "post_process.log").logger
        self.logger.info(f"================={self.__class__.__name__}=====================")
        self.logger.info(f"Initializing {self.__class__.__name__}")
        self.dataset_path = dataset_path
        return
        
    def parse_dataset(self):
        """Open and analyze the dataset using xarray"""
        self.logger.info(f"Opening dataset: {self.dataset_path}")
        try:
            ds = xr.open_dataset(self.dataset_path)

            
            # Log dataset attributes
            self.logger.info("================global attributes=====================")
            for attr_name, attr_value in ds.attrs.items():
                self.logger.info(f"  {attr_name}: {attr_value}")
            self.logger.info("================end global attributes=====================")
            
            # Log coordinate information
            self.logger.info("================coordinate information=====================")
            for coord_name, coord in ds.coords.items():
                self.logger.info(f"Coordinate: {coord_name}")
                self.logger.info(f"  Range: {coord.values.min()} to {coord.values.max()}")
            self.logger.info("================end coordinate information=====================")
            
            # Log dataset variables
            self.data = {}
            var_names = []
            self.logger.info("================dataset variables=====================")
            for var_name, var in ds.variables.items():
                var_names.append(var_name)
                self.data[var_name] = {
                    'data': var # varname is the key, var is the value
                }
                self.logger.info(f"================saving data for variable: {var_name}=====================")
                self.logger.info(f"  Data structure: {var}")
                self.logger.info(f"================end saving data for variable: {var_name}=====================")
            self.logger.info("================end dataset variables=====================")
            self.logger.info(f"================dataset variables=====================")
            self.logger.info(f"Number of variables: {len(var_names)}")
            self.data['var_names'] = var_names
            self.logger.info(f"Saving variable names in key 'var_names'")
            self.logger.info(f"Variable names: {var_names}")
            self.logger.info(f"================end dataset variables=====================")
            ds.close()
            
        except Exception as e:
            self.logger.error(f"Error analyzing dataset: {str(e)}")
            raise

        return 
    
class checkDataStructure:
    def __init__(self, parsed_file):
        self.logger = parsed_file.logger
        self.data = parsed_file.data
        self.logger.info(f"================={self.__class__.__name__}=====================")
        self.logger.info(f"Initializing {self.__class__.__name__}")
        self.check_time()
        self.check_latlon()
        self.check_chl()
        return

    def check_time(self):
        self.logger.info(f"Checking time dimension")
        if 'time' in self.data['var_names']:
            self.logger.info(f"Time dimension found")
            ts = self.data['time']
            self.time_steps = ts['data'].shape[0]
            self.logger.info(f"Number of time steps: {self.time_steps}")
            self.time_values = ts['data'].values
            for timestamp in self.time_values:
                self.logger.info(f"Timestamp: {timestamp}")
        else:
            self.logger.warning(f"Time dimension not found")
        return

    def check_latlon(self):
        self.logger.info(f"Checking latitude and longitude dimensions")
        if 'latitude' in self.data['var_names'] and 'longitude' in self.data['var_names']:
            self.logger.info(f"Latitude and longitude dimensions found")
            lat = self.data['latitude']
            lon = self.data['longitude']
            lat_dims = lat['data'].dims
            lon_dims = lon['data'].dims
            if lat_dims == ('latitude',) and lon_dims == ('longitude',):
                self.logger.info(f"Dimensions: {lat_dims} and {lon_dims}")
            else:
                raise ValueError(f"Dimensions do not match expected dimensions: ('latitude',) and ('longitude',)")
        else:
            self.logger.warning(f"Latitude and longitude dimensions not found")
        
        # store variables if okay:
        self.lat = lat['data'].data
        self.lon = lon['data'].data
        return

    def check_chl(self):
        self.logger.info(f"Checking CHL variable")
        if 'CHL' in self.data['var_names']:
            self.logger.info(f"CHL variable found")
            chl = self.data['CHL']
            chl_dims = chl['data'].dims 
            chl_memory = chl['data'].nbytes/(1024**2)
            self.logger.info(f"Size in MB: {chl_memory}")
            self.logger.info(f"datatype: {type(chl['data'])}")
            
            if chl_dims == ('time', 'latitude', 'longitude'):
                self.logger.info(f"Dimensions: {chl_dims}")
            else:
                raise ValueError(f"Dimensions do not match expected dimensions: ('time', 'latitude', 'longitude')")

        else:
            raise ValueError(f"CHL variable not found")
        
        # store variables if okay:
        self.chl = chl['data']
        return

class chlDataHandler:
    def __init__(self, parsed_file):
        self.logger = parsed_file.logger
        self.logger.info(f"================={self.__class__.__name__}=====================")
        self.logger.info(f"Initializing {self.__class__.__name__}")
        self.chl = parsed_file.chl
        self.lat = parsed_file.lat
        self.lon = parsed_file.lon
        self.time = parsed_file.time_values
        return

    def index_chlorophyll(self):
        self.logger.info(f"Indexing CHL data")
        self.chl_array = self.chl.values
        self.logger.info(f"Shape of CHL data: {self.chl_array.shape}")
        self.logger.info(f"Data type of CHL data: {type(self.chl_array)}")
        
   


