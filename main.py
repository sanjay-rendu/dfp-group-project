import os
import argparse
from craigslist.scraper import scrape_it
from google.api import get_maps_dataframe
from cmu.shuttle import get_shuttle_stops
from yelp.yelp import yelp_search
from yelp.yelp import yelp_clean
from merge.merged import geopoint
from merge.merged import nearest_5
from merge.merged import nearest
from pathlib import Path
from rating import data_rating
from interface import interface_start
import pandas as pd
import config
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

this_dir = str(os.path.dirname(os.path.abspath(__file__)))

# create temp dir if it doesn't exist
Path(this_dir + "/temp").mkdir(parents=True, exist_ok=True)

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--latest", dest="latest", action='store_true', default=False
                            , help='Fetches latest properties from Craigslist')

parser.add_argument("-y", "--refresh_yelp", dest="yelp", action='store_true', default=False
                            , help='Refreshes restaurants database with latest info from Yelp')

parser.add_argument("-s", "--refresh_shuttle", dest="cmu", action='store_true', default=False
                            , help='Refreshes shuttles database with latest info from CMU')

parser.add_argument("-a", "--refresh_all", dest="all_db", action='store_true', default=False
                            , help='Refreshes all databases and uses latest information')

parser.add_argument("-p", "--price_filter", dest="price_filter", type=int, nargs='+', default=[0, 1000000]
                    , help='Optional price range filter. Usage: -p <MIN> <MAX>')

parser.add_argument("-t", "--top", dest= "top", type=int, nargs=1, default = [5],
                    help = "Number of properties to be displayed")

args = parser.parse_args()

if __name__ == "__main__":

    shuttle_file_loc = this_dir + '/temp/cmu_shuttle.csv'
    num_of_pages = config.craig_num_of_pages
    city = 'Pittsburgh'
    craig_file_loc = this_dir + '/temp/{}_pages_{}.csv'.format(city, num_of_pages)
    term = 'restaurant'
    location = 'Pittsburgh'
    yelp_file_loc = this_dir + '/temp/{}_in_{}.csv'.format(term, location)
    maps_file_loc = this_dir + '/temp/map_data.csv'
    merged_file_loc = this_dir + "/temp/apartment.csv"
    price_lb, price_ub = args.price_filter

    try:
        if int(price_ub) < int(price_lb):
            raise ValueError(" Retry with sensible price filters. Make sure <MIN> is greater than <MAX>")
    except:
        raise ValueError(" Retry with sensible price filters. Make sure <MIN> is greater than <MAX>")

    try:
        if args.yelp or args.all_db:
            # Get yelp data
            print("Scrapping Yelp...")
            yelp_df = yelp_search(term, location)
            yelp_cleaned_df = yelp_clean(yelp_df)
            yelp_cleaned_df.to_csv(yelp_file_loc, index=False)
    except Exception as e:
        print("Unable to refresh Yelp database.")
        print(e)

    try:
        if args.cmu or args.all_db:
            # Get CMU Shuttle data
            print("Scrapping CMU Shuttle Map...")
            shuttle_df = get_shuttle_stops()
            shuttle_df.to_csv(shuttle_file_loc, index=False)
    except Exception as e:
        print("Unable to refresh CMU shuttle database.")
        print(e)

    if args.latest or args.all_db:
        # Scrape craigslist for recent postings
        print("Scrapping Craigslist...")
        try:
            craig_df = scrape_it(city, 1)
            craig_df.to_csv(craig_file_loc, index=False)
        except Exception as e:
            print("Unable to get latest data from Craigslist.")
            print(e)

        # Get Google API data
        print("Fetching Google API data...")
        maps_df = get_maps_dataframe()
        maps_df.to_csv(maps_file_loc, index=False)

        if 'craig_df' not in locals():
            craig_df = pd.read_csv(craig_file_loc)

        if 'yelp_df' not in locals():
            yelp_df = pd.read_csv(yelp_file_loc)

        if 'shuttle_df' not in locals():
            shuttle_df = pd.read_csv(shuttle_file_loc)

        # Calculate geo-distances
        merged_df = pd.merge(craig_df, maps_df, how="left", on="location")
        #merged_df = craig_df.join(maps_df, on="location")
        apartments_geo = geopoint(merged_df)
        restaurants_geo = geopoint(yelp_cleaned_df)
        shuttles_geo = geopoint(shuttle_df)
        apartments_geo['nearest_shuttle_stop'] = apartments_geo.apply(nearest, df=shuttles_geo, axis=1)

        apartments_geo['nearest_restaurants'] = apartments_geo.apply(nearest_5, df=restaurants_geo, axis=1)

        apartments_geo = apartments_geo.dropna(axis=0, how="any")
        apartments_geo.drop_duplicates(subset=["post title", "neighborhood", "sqft", "price"], keep="first", inplace=True)
        apartments_geo.reset_index()
        apartments_geo.to_csv(merged_file_loc)

    if not(args.all_db):
        print("Using cached data to make housing recommendations.")

    if 'info' not in locals():
        final_merge_df = pd.read_csv(merged_file_loc)

    info = data_rating(final_merge_df, price_lb, price_ub)

    df1 = info.groupby(['number bedrooms', 'sqft'], as_index=False).agg({'price': 'mean'})

    df1.sqft = df1.sqft.astype(int)
    df1.price = df1.price.astype(int)
    df1 = df1.pivot(index='sqft', columns='number bedrooms').fillna(0)

    plt.rcParams["figure.figsize"] = (15, 10)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    X, Y = np.meshgrid(np.array([x[1] for x in df1.columns.values]), df1.index.values)
    Z = df1.values
    im = ax.plot_surface(X, Y, Z, cmap='viridis', )
    ax.set_title('price variation')
    plt.xlabel('sqft')
    plt.ylabel('number of bedrooms')
    plt.colorbar(im)
    plt.savefig('price_var_graph.png')


    info.to_csv(this_dir + "/temp/rated.csv")
    interface_start(info, args.top[0])