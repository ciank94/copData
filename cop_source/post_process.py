import xarray as xr
import logging
import os

# Setup module logger
def logger_post_process(output_path):
    log_format = '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    # Create logger
    logger = logging.getLogger(__name__) # gets the name of the current module
    logging.basicConfig(level=logging.INFO,
                        format=log_format,
                        datefmt=date_format,
                        handlers=[
                            logging.FileHandler(os.path.join(output_path, 'post_process.log'), mode='w'),
                            logging.StreamHandler()
                        ])
    logger.setLevel(logging.INFO)
    return logger

class DataAnalysis:
    def __init__(self, dataset_path, output_path):
        self.logger = logger_post_process(output_path)
        self.logger.info(f"================={self.__class__.__name__}=====================")
        self.logger.info(f"Initializing {self.__class__.__name__}")
        self.dataset_path = dataset_path
        return
        
    def analyze_dataset(self):
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
            data = {}
            var_names = []
            self.logger.info("================dataset variables=====================")
            for var_name, var in ds.variables.items():
                var_names.append(var_name)
                data[var_name] = {
                    'shape': var.shape,
                    'dims': var.dims,
                    'attrs': var.attrs,
                    'data': var
                }
                self.logger.info(f"================saving data for variable: {var_name}=====================")
                self.logger.info(f"  Data structure: {var}")
                self.logger.info(f"================end saving data for variable: {var_name}=====================")
            self.logger.info("================end dataset variables=====================")
            self.logger.info(f"================dataset variables=====================")
            self.logger.info(f"Number of variables: {len(var_names)}")
            for var_name in var_names:
                self.logger.info(f"Variable: {var_name}")
            self.logger.info(f"================end dataset variables=====================")
            ds.close()
            
        except Exception as e:
            self.logger.error(f"Error analyzing dataset: {str(e)}")
            raise

        return data, var_names
    
class PostProcess:
    def __init__(self, df, filename):
        pass

