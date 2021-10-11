# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from pykrige import OrdinaryKriging


# Read recipe inputs
user_input_dataset_prepared_scored = dataiku.Dataset("user_input_dataset_prepared_scored")
df = user_input_dataset_prepared_scored.get_dataframe()

# Clean inputs
df.dropna(inplace=True)
df.reset_index(inplace=True)

# Define mercator conversion func
def wgs84_to_web_mercator(df, lon="lon", lat="lat"):
    k = 6378137
    df["x"] = df[lon] * (k * np.pi/180.0)
    df["y"] = np.log(np.tan((90 + df[lat]) * np.pi/360.0)) * k
    return df

# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.
#bole ni diganti biar dari input:D
depths = list(df.depth.unique())

list_=[]
for depth in depths:
    
    df_depth=df[df.depth==depth]
    points=[]
    for d in range(len(df_depth)):
        lats=df_depth.lat.iloc[d]
        lons=df_depth.lon.iloc[d]
    #     print(d)
        points.append([lons,lats])
    values=df_depth.prediction
    points=np.array(points)
    lons,lats=points[:,0],points[:,1]

    grid_space = 0.0025
    grid_lon = np.arange(-113.03662, -112.789, grid_space)
    grid_lat = np.arange(38.410448, 38.573241, grid_space)

    OK = OrdinaryKriging(lons, lats, values, variogram_model='gaussian', verbose=True,
                         enable_plotting=False,nlags=100000)

    zgrid, ssgrid = OK.execute('grid', grid_lon, grid_lat)

    new = []
    for i in range(grid_lon.shape[0]):
        for j in range(grid_lat.shape[0]):
            new.append([grid_lon[i], grid_lat[j], zgrid.data[j][i]])

    df_new = pd.DataFrame(new, columns=['lon', 'lat', 'pred'])
    df_new["depth"] = depth
    df_new = wgs84_to_web_mercator(df_new)
    
    list_.append(df_new)
    
df_stacked=pd.concat(list_)

dashboard_interpolated_df = df_stacked # For this sample code, simply copy input to output


# Write recipe outputs
dashboard_interpolated = dataiku.Dataset("dashboard_interpolated")
dashboard_interpolated.write_with_schema(dashboard_interpolated_df)