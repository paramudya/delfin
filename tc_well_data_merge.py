# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
forge_general = dataiku.Dataset("forge_general_well_all_depth_all_wells")
forge_general_df = forge_general.get_dataframe()

predicted_mtc = dataiku.Dataset("predicted_mtc_with_lithology")
predicted_mtc_df = predicted_mtc.get_dataframe()

mtc_mean_lit=predicted_mtc_df.groupby('lithology')['prediction'].mean()

def KH(well_data,mtc_mean_lit):
    well_data['KH_basin_fill_at_depth']=well_data['h_basin_fill']*mtc_mean_lit['Basin Fill']
    well_data['KH_granitoid_at_depth']=well_data['h_granitoid']*mtc_mean_lit['Granitoid']
    well_data.drop(columns=['h_basin_fill','h_granitoid'],inplace=True)
    well_data.fillna(0,inplace=True) # penting buat ganti NaN jadi 0--karena ada H yg kosong karena emang 0
    return well_data

forge_general_prepared_df = KH(forge_general_df,mtc_mean_lit)
forge_general_prepared_df.drop(['H_basin_fill_at_depth','H_granitoid_at_depth'],
                               axis=1,
                               inplace=True)

# Write recipe outputs
forge_general_prepared = dataiku.Dataset("general_well")
forge_general_prepared.write_with_schema(forge_general_prepared_df)
