import xarray as xr
from .logger_config import setup_logger

# Setup module logger
logger = setup_logger('post_process')

class DataAnalysis:
    def __init__(self, dataset_path):
        logger.info(f"================={self.__class__.__name__}=====================")
        logger.info(f"Initializing {self.__class__.__name__}")
        self.dataset_path = dataset_path
        self.analyze_dataset()
        
    def analyze_dataset(self):
        """Open and analyze the dataset using xarray"""
        logger.info(f"Opening dataset: {self.dataset_path}")
        try:
            ds = xr.open_dataset(self.dataset_path)
            
            # Log dataset variables
            logger.info("Dataset Variables:")
            for var_name, var in ds.variables.items():
                logger.info(f"Variable: {var_name}")
                logger.info(f"  Dimensions: {var.dims}")
                logger.info(f"  Shape: {var.shape}")
                logger.info(f"  Attributes:")
                for attr_name, attr_value in var.attrs.items():
                    logger.info(f"    {attr_name}: {attr_value}")
            
            # Log dataset attributes
            logger.info("\nDataset Global Attributes:")
            for attr_name, attr_value in ds.attrs.items():
                logger.info(f"  {attr_name}: {attr_value}")
            
            # Log coordinate information
            logger.info("\nDataset Coordinates:")
            for coord_name, coord in ds.coords.items():
                logger.info(f"Coordinate: {coord_name}")
                logger.info(f"  Range: {coord.values.min()} to {coord.values.max()}")
            
            ds.close()
            
        except Exception as e:
            logger.error(f"Error analyzing dataset: {str(e)}")
            raise

        return
    
class PostProcess:
    def __init__(self, filename):
        self.filename = filename
        ds = xr.open_dataset(self.filename)
        logger.info(f"================={self.__class__.__name__}=====================")
        logger.info(f"Initializing {self.__class__.__name__}")
        logger.info("Dataset Variables:")
        self.data = {}
        for var_name, var in ds.variables.items():
            self.data[var_name] = {
                'shape': var.shape,
                'dims': var.dims,
                'attrs': var.attrs,
                'data': var
            }
            logger.info(f"Variable: {var_name}")
            logger.info(f"  Shape: {var.shape}")
            logger.info(f"  Dimensions: {var.dims}")
            logger.info(f"  Attributes: {var.attrs}")
        return