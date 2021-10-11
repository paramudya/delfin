# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
user_inputs = dataiku.Folder("wPJARnFr")
user_inputs_info = user_inputs.get_info()
paths = user_inputs.list_paths_in_partition()

with user_inputs.get_download_stream(paths[0].split('/')[-1]) as f:
    data = pd.read_csv(f)

# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

# make sure of columns integrity
list_cols_to_keep=['well_id','lon','lat','depth',
                  'temp','elev','surface_temp',
                  'h_basin_fill','h_granitoid',
                  'KH_basin_fill_at_depth','KH_granitoid_at_depth','depth_deeper_than_borehole']
data.drop(data.columns.difference(list_cols_to_keep),axis=1,inplace=True)
#data.elev=data.elev.astype('int64')

#filter
user_input_dataset_df = data[(data['depth']>=0)&(data['depth']<=5000)]

# Write recipe outputs
user_input_dataset = dataiku.Dataset("user_input_dataset")
user_input_dataset.write_with_schema(user_input_dataset_df)
