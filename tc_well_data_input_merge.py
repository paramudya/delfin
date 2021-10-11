# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
dashboard_shahdi_250_m = dataiku.Dataset("dashboard_shahdi_250_m")
dashboard_shahdi_250_m_df = dashboard_shahdi_250_m.get_dataframe()
dashboard_shahdi_100_m = dataiku.Dataset("dashboard_shahdi_100_m")
dashboard_shahdi_100_m_df = dashboard_shahdi_100_m.get_dataframe()
dashboard_shahdi_50_m = dataiku.Dataset("dashboard_shahdi_50_m")
dashboard_shahdi_50_m_df = dashboard_shahdi_50_m.get_dataframe()

predicted_mtc = dataiku.Dataset("predicted_mtc_with_lithology")
predicted_mtc_df = predicted_mtc.get_dataframe()

mtc_mean_lit=predicted_mtc_df.groupby('lithology')['prediction'].mean()

def KH(well_data,mtc_mean_lit):
    well_data['KH_basin_fill_at_depth']=well_data['h_basin_fill']*mtc_mean_lit['Basin Fill']
    well_data['KH_granitoid_at_depth']=well_data['h_granitoid']*mtc_mean_lit['Granitoid']
    well_data.drop(columns=['h_basin_fill','h_granitoid'],inplace=True)
    well_data.fillna(0,inplace=True) # penting buat ganti NaN jadi 0--karena ada H yg kosong karena emang 0
    return well_data

# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

dashboard_shahdi_100_m_prepared_df = KH(dashboard_shahdi_100_m_df,mtc_mean_lit) # Compute a Pandas dataframe to write into dashboard_shahdi_100_m_prepared
dashboard_shahdi_250_m_prepared_df = KH(dashboard_shahdi_250_m_df,mtc_mean_lit) # Compute a Pandas dataframe to write into dashboard_shahdi_250_m_prepared
dashboard_shahdi_50_m_prepared_df = KH(dashboard_shahdi_50_m_df,mtc_mean_lit) # Compute a Pandas dataframe to write into dashboard_shahdi_50_m_prepared

# Write recipe outputs
dashboard_shahdi_100_m_prepared = dataiku.Dataset("dashboard_shahdi_100_m_prepared")
dashboard_shahdi_100_m_prepared.write_with_schema(dashboard_shahdi_100_m_prepared_df)
dashboard_shahdi_250_m_prepared = dataiku.Dataset("dashboard_shahdi_250_m_prepared")
dashboard_shahdi_250_m_prepared.write_with_schema(dashboard_shahdi_250_m_prepared_df)
dashboard_shahdi_50_m_prepared = dataiku.Dataset("dashboard_shahdi_50_m_prepared")
dashboard_shahdi_50_m_prepared.write_with_schema(dashboard_shahdi_50_m_prepared_df)