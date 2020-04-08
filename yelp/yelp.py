import requests
import json
import pandas as pd
from pandas.io.json import json_normalize

def yelp_search(term, location):
    """
    Scrapes yelp to get businesses posts for a city

    :param term: Businesses to scrape
    :param location: Location to search

    :return: Dataframe with web postings
    """
    api_key='DM7PL6iLbdk7M9ojq7WF2YkINFBjgLsfF7GL39CHueqP8naYvg8ivk8zjywwFtNy_g4qQ2UV4VqRUo_enzhx2pXxu96vHcRD0bFVdVIH1inpXbl8pfhzI3dBhtM9XnYx'
    headers = {'Authorization': 'Bearer %s' % api_key}
    url= 'https://api.yelp.com/v3/businesses/search'
    found = True
    yelp_df = pd.DataFrame()
    i = 0
    while found == True:
        params = {'term':term, 'location': location, 'limit' : 50, 'offset' : i * 50}
        req = requests.get(url, params=params, headers = headers)
        search = req.json()
        yelp_search = pd.DataFrame.from_dict(pd.io.json.json_normalize(search['businesses']),orient='columns')
        yelp_df = yelp_df.append(yelp_search, ignore_index=True)
        i += 1
        print("page "+str(i)+" success!")
        params1 = {'term': 'restaurant', 'location': 'Pittsburgh', 'limit': 50, 'offset': i * 50}
        req1 = requests.get(url, params=params1, headers=headers)
        search1 = req1.json()
        found = 'businesses' in pd.io.json.json_normalize(search1)
    return yelp_df

def yelp_clean(yelp_df):
    yelp_cleaned = {"name": [],"display_phone": [], "rating":[],"price":[],"categories":[],"long":[],
                    "lat":[], "location.display_address":[]}
    yelp_cleaned_df = pd.DataFrame(data = yelp_cleaned)
    yelp_cleaned_df["name"] = yelp_df["name"]
    yelp_cleaned_df["display_phone"] = yelp_df["display_phone"]
    yelp_cleaned_df["rating"] = yelp_df["rating"]
    yelp_cleaned_df["price"] = yelp_df["price"]
    yelp_cleaned_df["long"] = yelp_df["coordinates.longitude"]
    yelp_cleaned_df["lat"] = yelp_df["coordinates.latitude"]
    yelp_cleaned_df["location.display_address"] = yelp_df["location.display_address"]
    yelp_cleaned_df["categories"] = yelp_df["categories"]
    return yelp_cleaned_df

if __name__ == "__main__":
    yelp_df = yelp_search("restaurant", "Pittsburgh")
    yelp_cleaned_df = yelp_clean()
