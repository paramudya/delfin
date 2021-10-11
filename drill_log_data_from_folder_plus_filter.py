# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
user_inputs_mtc = dataiku.Folder("W0JbBBz3")
user_inputs_mtc_info = user_inputs_mtc.get_info()
paths = user_inputs_mtc.list_paths_in_partition()

with user_inputs_mtc.get_download_stream(paths[0].split('/')[-1]) as f:
    data = pd.read_csv(f)

# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

user_inputs_mtc_dataset_df = data[(data['depth_m']>=0)&(data['depth_m']<=5000)]
data = data[(data['temp_in_c']>=0)&(data['temp_in_c']<=400)]
data = data[(data['temp_out_c']>=0)&(data['temp_out_c']<=400)]

# Write recipe outputs
user_inputs_mtc_dataset = dataiku.Dataset("user_inputs_mtc_dataset")
user_inputs_mtc_dataset.write_with_schema(user_inputs_mtc_dataset_df)
