# ===========Section 0: imports=============
from copchlhandler import *    
import os

# ==========Section 1: Parameters=============
# Get the project root directory
#project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#filepath_input = os.path.join(project_root, 'input_files')
#filepath_output = os.path.join(project_root, 'output_files')
filepath_input='input_files'
filepath_output = 'output_files'
fileid = 'chl_obs_daily_L3_multi-year_4km_2016-12-18_to_2016-12-19.nc'
filename = os.path.join(filepath_input, fileid) #filepath_input + fileid


# ==========Section 2: Prepare data=============
parsed_file = inspectDataStructure(filename, filepath_output)
parsed_file.parse_dataset()
checkDataStructure(parsed_file)

breakpoint()