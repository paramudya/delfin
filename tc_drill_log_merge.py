# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
well_58_32_processed_pason_log = dataiku.Dataset("Well_58_32_processed_pason_log")
thermal_conductivity_data = dataiku.Dataset("58_32_thermal_conductivity_data")

drill = well_58_32_processed_pason_log.get_dataframe()
mtc = thermal_conductivity_data.get_dataframe()


# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

drill_depth=drill['Depth(m)'].sort_values()
lower,upper = mtc.iloc[:,0],mtc.iloc[:,1]

count,j  = 0,0
for i in range(len(drill_depth)):
    while drill_depth[i]>upper[j] and j<len(upper)-1:
        j+=1
    if drill_depth[i]<lower[j]:
        continue
    drill.at[i,'mtc']=mtc.iloc[j][2]
    
# Filter
#pason=pason[(pason['Flow In (gal/min)']>=500)&(pason['Flow In (gal/min)']<=1000)&(pason['Pump Press (psi)']>=1000)]

# Write recipe outputs
drill_mtc = dataiku.Dataset("drill_mtc")
drill_mtc.write_with_schema(drill)
