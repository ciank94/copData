import logging
from turtle import down
from .logConfig import logConfig
import copernicusmarine as cop
import os
import sys


class checkRequest:
    def __init__(self, dataID, output_path):
        """Initialize the copDataID class.

        :param dataID: The data identifier.
        :type dataID: str
        """
        name = os.path.basename(__file__)
        self.log_file_name = name +'_exit.log' # initialize log file assuming it exists
        self.log_file_path = os.path.join(output_path, self.log_file_name)
        self.logger = logConfig(output_path, self.log_file_name).logger
        self.logger.info(f"================={self.__class__.__name__}=====================")
        self.logger.info(f"Initializing {self.__class__.__name__}")
        self.logger.info(f"DataID: {dataID}")    
        self.dataID = dataID
        self.spilt_name()
        self.check_catalog()
        return

    def spilt_name(self):
        split_name = self.dataID.replace('_', '-').split('-')
        if "P1D" in split_name:
            self.frequency = "daily"
        elif "P1M" in split_name:
            self.frequency= "monthly"
        
        if "l3" in split_name:
            self.level = "3"
        elif "l4" in split_name:
            self.level = "4"

        if "nrt" in split_name:
            self.period = "near-real-time"
        elif "my" in split_name:
            self.period = "multi-year"

        if "olci" in split_name:
            self.sensor = "olci"
        elif "multi" in split_name:
            self.sensor = "multi"

        if "multi-climatology" in split_name:
            self.climatology = True
        else:
            self.climatology = False
        
        if "gapfree" in split_name:
            self.gapfree = True
        else:
            self.gapfree = False

        if "4km" in split_name:
            self.resolution = "4km"
            res_print = "4km"
        elif "300m" in split_name:
            self.resolution = ".3k"
            res_print = "300m"
        
        self.file_prefix = f"chl_{self.resolution}"
        self.logger.info(f"Frequency: {self.frequency}")
        self.logger.info(f"Level: {self.level}")
        self.logger.info(f"Period: {self.period}")
        self.logger.info(f"Resolution: {res_print}")
        self.logger.info(f"File prefix: {self.file_prefix}")
        self.logger.info(f"Climatology: {self.climatology}")
        self.logger.info(f"Gapfree: {self.gapfree}")
        self.logger.info(f"Sensor: {self.sensor}")
        return

    def check_catalog(self):
        cmems_obs_glo_bgc_plankton_files = self.get_catalog()
        if self.dataID in cmems_obs_glo_bgc_plankton_files:
            self.logger.info(f"dataID matches item in list of cmems_obs_glo_bgc_plankton_files")
        else:
            self.logger.warning(f"list of cmems_obs_glo_bgc_plankton_files: {cmems_obs_glo_bgc_plankton_files}")
            raise ValueError(
                f"dataID does not match list of cmems_obs_glo_bgc_plankton_files, "
                "may be added to list and checked if needed"
            )

    def get_catalog(self):
        return [# Level 3 datasets
            "cmems_obs-oc_glo_bgc-plankton_my_l3-olci-4km_P1D",
            "cmems_obs-oc_glo_bgc-plankton_nrt_l3-olci-300m_P1D",
            "cmems_obs-oc_glo_bgc-plankton_my_l4-multi-climatology-4km_P1D"]
    

class requestConfig:
    def __init__(self, parse_file):
        self.parse_file = parse_file
        self.logger = parse_file.logger
        self.logger.info(f"================={self.__class__.__name__}=====================")
        self.logger.info(f"Initializing {self.__class__.__name__}")
        self.parse_file = parse_file # instance of cmems data class
        if not hasattr(self.parse_file, 'file_prefix') or self.parse_file.file_prefix is None:
            raise AttributeError(f"File prefix is not set")
        return

    def configure_path(self, config_path, input_path):
        # check output path
        if not os.path.exists(input_path):
            raise ValueError(f"Output path does not exist: {input_path}")
        self.output_path = input_path
        self.logger.info(f"Output path: {input_path}")
        self.credentials_file=config_path + ".copernicusmarine-credentials"
        # check credentials file
        if not os.path.exists(self.credentials_file):
            raise ValueError(f"Credentials file does not exist: {self.credentials_file}")
        self.logger.info(f"Credentials file: {self.credentials_file}")
        return

    def configure_time(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.logger.info(f"Start date: {self.start_date}")
        self.logger.info(f"End date: {self.end_date}")
        return

    def configure_variable(self, variables):
        # Retrieve the dataset using the data ID
        self.variables = variables
        self.append_vars()
        self.logger.info(f"Variables: {self.variables}")
        self.config_prefix = self.parse_file.file_prefix + "_" + self.start_date[:10] 
        download_filename = self.config_prefix + ".nc"
        self.output_file = os.path.join(self.output_path, download_filename)
        self.check_file_exists()
        return

    def append_vars(self):
        if (self.parse_file.resolution == "4km" and
            self.parse_file.sensor == "olci" and
            not self.parse_file.gapfree):
            self.variables.append("CHL_gradient")
        if self.parse_file.climatology:
            self.variables.append("CHL_mean")
            self.variables.append("CHL_max")
            self.variables.append("CHL_min")
            self.variables.append("CHL_standard_deviation")
            self.variables.remove("CHL")
        return

    def check_file_exists(self):
        if os.path.exists(self.output_file):
            self.logger.info(f"File already exists: {self.output_file}")
            self.logger.info(f"Exiting as file: {self.output_file} already exists")
            sys.exit()
        else:
            self.logger.info(f"File does not exist: {self.output_file}")
            self.logger.info(f"File will be downloaded: {self.output_file}")
        return

    def configure_domain(self, lon_bounds, lat_bounds):
        self.lon_bounds = lon_bounds
        self.lat_bounds = lat_bounds
        self.logger.info(f"Longitude bounds: {self.lon_bounds}")
        self.logger.info(f"Latitude bounds: {self.lat_bounds}")
        return

class requestData:
    def __init__(self, config):
        self.config = config
        self.logger = config.logger
        self.logger.info(f"================={self.__class__.__name__}=====================")
        self.logger.info(f"Initializing {self.__class__.__name__}")
        self.request_data()
        self.change_log_file_name()
        return

    def request_data(self):
         cop.subset(
            dataset_id=self.config.parse_file.dataID,
            variables=self.config.variables,
            start_datetime=self.config.start_date,
            end_datetime=self.config.end_date,
            minimum_longitude=self.config.lon_bounds[0],
            maximum_longitude=self.config.lon_bounds[1],
            minimum_latitude=self.config.lat_bounds[0],
            maximum_latitude=self.config.lat_bounds[1],
            #minimum_depth=self.min_depth,
            #maximum_depth=self.max_depth,
            output_filename=self.config.output_file,
            credentials_file=self.config.credentials_file,
            force_download=True,
        )
    
    def change_log_file_name(self):
        self.logger.info(f"Successfully downloaded file, shutting down logger and" 
        f"renaming log file")
        logging.shutdown()
        split_name = self.config.parse_file.log_file_name.split('_')
        new_name = split_name[0] + '_' + self.config.config_prefix + '.log'
        original_path = self.config.parse_file.log_file_path
        new_path = os.path.join(os.path.dirname(original_path), new_name)
        # Check if the destination file already exists
        if os.path.exists(new_path):
            os.remove(new_path)  # Remove the existing file
        os.rename(original_path, new_path)
        
        return