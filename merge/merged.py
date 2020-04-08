import geopandas as geopandas
import pandas as pd
from shapely.geometry import Point
import warnings
warnings.filterwarnings("ignore")

# Convert location to geo points
def geopoint(x):

    x['Coordinates'] = list(zip(x["lat"], x["long"]))
    x['Coordinates'] = x['Coordinates'].apply(Point)
    x_geo = geopandas.GeoDataFrame(x, geometry='Coordinates')
    x_geo.crs = {'init': 'epsg:4326'}  # tell python that the current coordinates are WGS84 coordinate system
    x_geo = x_geo.to_crs({'init': 'epsg:2272'})  # convert the coordinate system to NAD83 (a projected coordinate system)
    return x_geo


def nearest_5(row, df=None):
    X = row['Coordinates']
    dist_list = []
    rest_list = df['name'].tolist()
    rating_list = df['rating'].tolist()
    for j in range(0, len(df)):
        Y = df.iloc[j, -1]
        dist_list.append(X.distance(Y)*0.0003048)
    min_list = sorted(zip(rest_list,dist_list,rating_list), key = lambda t: t[1])[:5]
    return min_list


def nearest(row, df=None):
    X = row['Coordinates']
    dist_list = []
    for j in range(0, len(df)):
        Y = df.iloc[j, -1]
        dist_list.append(X.distance(Y)*0.0003048)
    n = dist_list.index(min(dist_list))
    nearest = (df.iloc[n,2],df.iloc[n,3], dist_list[n])
    return nearest


