# Define here a function that returns the outcome of the check.
import pandas as pd
def process(last_values, dataset, partition_id):
    # last_values is a dict of the last values of the metrics,
    # with the values as a dataiku.metrics.MetricDataPoint.
    # dataset is a dataiku.Dataset object
    df=dataset.get_dataframe()
    if pd.Series(['lon','lat','depth','temp','elev','h_basin_fill','h_granitoid']).isin(df.columns).all():
        return 'OK', 'optional message' # or 'WARNING' or 'ERROR'
    return 'WARNING', 'You are missing required column(s). Please recheck your data columns.'
