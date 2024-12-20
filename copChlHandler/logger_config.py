import logging
from math import log
import os

class LoggerConfig:
    def __init__(self, output_path, output_file):
        self.output_path = output_path
        self.output_file = output_file
        self.log_format = '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        self.date_format = '%Y-%m-%d %H:%M:%S'

        # Create logger
        self.logger = logging.getLogger(__name__) # gets the name of the current module
        self.file_handler()
        return
    
    def file_handler(self):
        logging.basicConfig(level=logging.INFO,
                        format=self.log_format,
                        datefmt=self.date_format,
        handlers=[logging.FileHandler(os.path.join(self.output_path, self.output_file), mode='w'),
                            logging.StreamHandler()])
        self.logger.setLevel(logging.INFO)
        return