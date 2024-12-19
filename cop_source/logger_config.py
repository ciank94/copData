"""
Logger Configuration Module

This module implements a lazy-loading logging system that creates log files only when
a module actually logs something, not when the logger is initialized. This is particularly
useful in a package where multiple modules might be imported but not all are used.

Key Features:
- One log file per module
- Log files are created only when a module actually logs something
- Timestamps in log files reflect when the module was first used
- Console output for all logs
- Prevents duplicate log files when modules are imported but not used

Example Usage:
    from logger_config import setup_logger
    
    # Create a logger for your module
    logger = setup_logger('your_module_name')
    
    # Use the logger - file will be created only when this is called
    logger.info("This is a log message")
"""

import logging
import os
import datetime

# Dictionary to track file handlers to ensure only one handler per module
# Key: module name, Value: file handler instance
_file_handlers = {}

def setup_logger(name):
    """Setup a logger with lazy file handler initialization.
    
    This function creates a logger with two handlers:
    1. Console Handler: Created immediately for console output
    2. File Handler: Created lazily when the logger is first used
    
    The lazy initialization is achieved using a filter that creates
    the file handler on the first log message. This prevents creating
    log files for modules that are imported but never used.
    
    Args:
        name (str): Name of the logger (e.g., 'reader' or 'post_process')
        
    Returns:
        logging.Logger: Configured logger instance
    
    File Naming:
        Log files are named using the pattern: YYYY-MM-DD_HH-MM-SS_[name].log
        The timestamp reflects when the module was first used, not when it was imported.
    """
    # Configure logging format with detailed information
    log_format = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Create or get existing logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Return existing logger if it already has handlers
    # This prevents adding duplicate handlers if setup_logger is called multiple times
    if logger.handlers:
        return logger
    
    # Create formatter for consistent log formatting
    formatter = logging.Formatter(log_format, date_format)
    
    # Setup console handler immediately
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Get absolute paths for log file location
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    output_dir = os.path.join(project_root, 'output_files')
    os.makedirs(output_dir, exist_ok=True)
    
    def add_file_handler(record):
        """Filter that creates a file handler on first use.
        
        This filter is called for every log message. On the first message
        for a module, it creates a file handler. Subsequent calls simply
        return True to allow the message through.
        
        Args:
            record: Log record being processed
            
        Returns:
            bool: Always returns True to allow the message through
        """
        if name not in _file_handlers:
            # Generate timestamp when the logger is first used
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            log_file = os.path.join(output_dir, f'{timestamp}_{name}.log')
            
            try:
                # Create and configure file handler
                file_handler = logging.FileHandler(log_file, mode='w')
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
                _file_handlers[name] = file_handler
            except Exception as e:
                # Log error to console if file creation fails
                logger.error(f"Failed to create log file at {log_file}: {str(e)}")
        return True
    
    # Add the filter that will create the file handler on first use
    logger.addFilter(add_file_handler)
    
    return logger
