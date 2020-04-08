import numpy as np
import pandas as pd


def data_rating(data, price_lb, price_ub):
    data = data[price_lb < data["price"]]
    data = data[data["price"] < price_ub]
    # rating for distance_CMU:
    dist_CMU_walking_range = data["distance_to_CMU"].max() - data["distance_to_CMU"].min()
    data["rating_CMU_walking"] = 1 - ((data["distance_to_CMU"] - data["distance_to_CMU"].min()) / dist_CMU_walking_range)
    dist_CMU_bus_time_range = data["duration_CMU"].max() - data["duration_CMU"].min()
    data["rating_CMU_bus_time"] = 1 - ((data["duration_CMU"] - data["duration_CMU"].min()) / dist_CMU_bus_time_range)
    dist_CMU_downtown_range = data["duration_downtown"].max() - data["duration_downtown"].min()
    data["rating_CMU_downtown"] = 1 - (
                (data["duration_downtown"] - data["duration_downtown"].min()) / dist_CMU_downtown_range)

    data_restaurant_rating = []
    data_restaurant_distance = []
    for i in data["nearest_restaurants"]:
        i = eval(str(i))
        sum1 = 0
        sum2 = 0
        for j in i:
            sum1 += float(j[2])
            sum2 += float(j[1])
        mean1 = sum1 / 5
        mean2 = sum2 / 5
        data_restaurant_rating.append(mean1)
        data_restaurant_distance.append(mean2)
    data["restaurant_rating"] = pd.Series(data_restaurant_rating)
    data["restaurant_distance"] = pd.Series(data_restaurant_distance)
    data["restaurant_distance_rating"] = 1 - ((data.restaurant_distance - data.restaurant_distance.min()) / (data.restaurant_distance.max() - data.restaurant_distance.min()))
    data["total_rating"] = round(2.5 * data["rating_CMU_walking"] + 4 * data["rating_CMU_bus_time"] +
                                 1 * data["rating_CMU_downtown"] + 1 * (data["restaurant_rating"] / 5) +
                                 1.5 * data["restaurant_distance_rating"], 1)
    data = data[['neighborhood', 'post title', 'number bedrooms', 'sqft', 'price', 'distance_to_CMU', 'duration_CMU',
             'bus_distance_CMU', 'distance_to_downtown', 'duration_downtown', 'bus_distance_downtown',
             'nearest_shuttle_stop', 'nearest_restaurants', 'restaurant_distance', 'total_rating']]

    data = data.sort_values(by="total_rating", ascending=False)
    data = data.reset_index()
    return data

