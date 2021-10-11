# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
drill_mtc_prepared = dataiku.Dataset("drill_mtc_prepared")
drill = drill_mtc_prepared.get_dataframe()

pred_df = drill[drill["mtc"] != drill["mtc"]] #NaN not equal to itself lel, cols with NaN MTC will go to predict

drill.dropna(inplace=True)
tr_df =  drill

# Write recipe outputs
tr = dataiku.Dataset("training")
tr.write_with_schema(tr_df)
pred = dataiku.Dataset("predict_set")
pred.write_with_schema(pred_df)