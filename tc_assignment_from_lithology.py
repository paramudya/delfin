import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
predicted_mtc = dataiku.Dataset("user_inputs_mtc_dataset_prepared_scored")
predicted_mtc_df = predicted_mtc.get_dataframe()
lit = dataiku.Dataset("well_lithology_from_earth_model")
lit_df = lit.get_dataframe()

lit_58_32=lit_df[lit_df['Well ID']=='58-32']

basin_lower=float(lit_58_32[lit_58_32['Lithology']=='Basin Fill']['from'].values)
basin_upper=float(lit_58_32[lit_58_32['Lithology']=='Basin Fill']['to'].values)

granitoid_lower=float(lit_58_32[lit_58_32['Lithology']=='Granitiod']['from'].values)
granitoid_upper=float(lit_58_32[lit_58_32['Lithology']=='Granitiod']['to'].values)

basin_range=(basin_lower,basin_upper)
granitoid_range=(granitoid_lower,granitoid_upper)

def assign_lit(depth,basin_range,granitoid_range):
    if depth >= basin_range[0] and depth < basin_range[1]:
        return 'Basin Fill'
    elif depth >= granitoid_range[0] and depth < granitoid_range[1]:
        return 'Granitoid'

predicted_mtc_df['lithology']=predicted_mtc_df.apply(lambda row: assign_lit(row['depth_m'],basin_range,granitoid_range), axis=1)

predicted_mtc_with_lithology_df = predicted_mtc_df # For this sample code, simply copy input to output


# Write recipe outputs
predicted_mtc_with_lithology = dataiku.Dataset("predicted_mtc_from_input_with_lithology")
predicted_mtc_with_lithology.write_with_schema(predicted_mtc_with_lithology_df)
