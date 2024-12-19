import copernicusmarine as cop
import logging
import os

# Configure logging format to include the class name
log_format = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'

# Create logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Remove any existing handlers
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(log_format, date_format))
logger.addHandler(console_handler)

# Create file handler
log_file = os.path.join('output_files', 'cmems_request.log')
file_handler = logging.FileHandler(log_file, mode='w')
file_handler.setFormatter(logging.Formatter(log_format, date_format))
logger.addHandler(file_handler)

class ChlObsData:
    def __init__(self, dataID):
        """Initialize the copDataID class.

        :param dataID: The data identifier.
        :type dataID: str
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"================={self.__class__.__name__}=====================")
        self.logger.info(f"Initializing {self.__class__.__name__}")
        self.logger.info(f"DataID: {dataID}")
        cmems_obs_glo_bgc_plankton_files = [
            # Level 3 datasets
            "cmems_obs-oc_glo_bgc-plankton_my_l3-olci-4km_P1D",
        ]
        if dataID in cmems_obs_glo_bgc_plankton_files:
            self.logger.info(f"dataID matches item in list of cmems_obs_glo_bgc_plankton_files")
        else:
            self.logger.warning(f"list of cmems_obs_glo_bgc_plankton_files: {cmems_obs_glo_bgc_plankton_files}")
            raise ValueError(
                f"dataID does not match list of cmems_obs_glo_bgc_plankton_files, "
                "please add to list if needed"
            )
        self.dataID = dataID
        split_name = dataID.replace('_', '-').split('-')
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
        
        if "4km" in split_name:
            self.resolution = "4km"
        elif "300m" in split_name:
            self.resolution = "300m"
        self.logger.info(f"Frequency: {self.frequency}")
        self.logger.info(f"Level: {self.level}")
        self.logger.info(f"Period: {self.period}")
        self.logger.info(f"Resolution: {self.resolution}")
        return


    def configure_path(self):
        credentials_file=config_path + ".copernicusmarine-credentials"