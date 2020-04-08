import googlemaps as gm
import pandas as pd
import os
from tqdm import tqdm
import sys
sys.path.append('../')
import config

# constant value
this_dir = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_maps_dataframe():
    # Jinxue's key:
    API_key = config.API_key
    CMU_address = '40.444122, -79.943261'
    downtown_address = "40.441059, -80.002441"
    app = pd.read_csv(this_dir + '/temp/Pittsburgh_pages_2.csv')

    apartment_list = list(app.location)
    # Define the object Client to retrieve directions data
    client_test = gm.Client(key=API_key)


    raw_data_CMU = []
    raw_data_downtown = []
    # request data from Google API

    for i in tqdm(range(len(apartment_list)), desc="google api"):
        a = apartment_list[i]
        a = a.replace(';', ',')
        directions_CMU = client_test.directions(origin=a,
                                                destination=CMU_address,
                                                mode="transit",
                                                transit_mode='bus')
        raw_data_CMU.append(directions_CMU)

        directions_downtown = client_test.directions(origin=a,
                                                     destination=downtown_address,
                                                     mode="transit",
                                                     transit_mode='bus')
        raw_data_downtown.append(directions_downtown)


    dir_columns = ['location', 'distance_to_CMU', 'duration_CMU',
                   'bus_distance_CMU', 'distance_to_downtown', 'duration_downtown', 'bus_distance_downtown']
    directions_dataframe = pd.DataFrame(columns=dir_columns)

    for index in tqdm(range(len(raw_data_CMU)), desc="creating table"):
        try:
            i = raw_data_CMU[index][0]
            j = raw_data_downtown[index][0]
        except:
            continue
        else:
            distance_to_CMU = float(i["legs"][0]["distance"]["value"])  # distance in meters
            duration_CMU = float(i["legs"][0]["duration"]["value"])  # duration time in seconds
            bus_distance_CMU = float(i["legs"][0]["steps"][0]["distance"]["value"])  # bus distance in meters
            distance_to_downtown = float(j["legs"][0]["distance"]["value"])  # distance in meters
            duration_downtown = float(j["legs"][0]["duration"]["value"])  # duration time in seconds
            bus_distance_downtown = float(j["legs"][0]["steps"][0]["distance"]["value"])  # bus distance in meters
            series_i = pd.Series([apartment_list[index], distance_to_CMU, duration_CMU, bus_distance_CMU,
                                  distance_to_downtown, duration_downtown, bus_distance_downtown],
                                 index=directions_dataframe.columns)
            directions_dataframe = directions_dataframe.append(series_i, ignore_index=True)
    return directions_dataframe


if __name__ == "__main__":
    print(get_maps_dataframe().head())
