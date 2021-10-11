# Define here a function that returns the outcome of the check.
import pandas as pd
def process(last_values, dataset, partition_id):
    # last_values is a dict of the last values of the metrics,
    # with the values as a dataiku.metrics.MetricDataPoint.
    # dataset is a dataiku.Dataset object
    df=dataset.get_dataframe()
    if pd.Series(['depth_m','rop_1_m','wob_kg','pump_press_kpa',
                  'surface_torque_kpa','rotary_speed_rpm','flow_out_%','wh_pressure_kpa']).isin(df.columns).all():
        return 'OK', 'optional message' # or 'WARNING' or 'ERROR'
    return 'WARNING', 'You are missing required column(s). Please recheck your data columns.'
