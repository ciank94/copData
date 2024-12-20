# ===========Section 0: imports=============
from copchlhandler import *    

# ==========Section 1: Parameters=============
filepath_input = './input_files'
filepath_output = './output_files'
datatype = 'chl' # choose from ['chl']
resolution = '.3k' # choose from ['4km', '.3k']
start_date = '2023-11-18' # yyyy-mm-dd
file_prefix = f"{datatype}_{resolution}_{start_date}" # example: chl_4km_2016-11-18

# ==========Section 2: Parse data=============
parsed_file = logData(file_prefix, filepath_input, filepath_output)
parsed_file.parse_dataset()
breakpoint()
checkData(parsed_file)

breakpoint()