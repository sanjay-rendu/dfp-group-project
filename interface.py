import argparse
import pandas as pd
import re
import math
from rating import data_rating


def interface_start(info, top):
    # info = pd.read_csv("combined.csv")  # will change the name to the real csv file

    # rating it the scores for ranking
    # info = info.sort_values(by=['rating']) # with change to the real column name

    while True:
        #     # asking for expected price interval
        #     bound_bad = True
        #     while bound_bad:
        #         try:
        #             price_lb = int(input("please enter lower bound of expected price: \n"))
        #             price_ub = int(input("please enter upper bound of expected price: \n"))
        #         except:
        #             print("bad input, try again!")
        #         else:
        #             if 0 < price_lb < price_ub:
        #                 bound_bad = False

        input_bad = True
        valid_input = ["y", "exit"]
        view_choice = ""
        while input_bad:

            view_choice = input("Show the top " + str(top) + " properties we recommend? (y to continue, exit to quit)\n")
            if view_choice not in valid_input:
                print("bad input! enter again")
            else:
                input_bad = False

        if view_choice == "exit":
            break
        elif view_choice == "y":

            house_item = "{}. {}  \n" \
                         "Neighborhood: {}\n" \
                         "Size: {} sqft\n" \
                         "Number of bedrooms: {}\n" \
                         "Price: {}$/month"

            for i in range(1, top+1):
                num_bed = info.loc[i]["number bedrooms"]
                if math.isnan(num_bed):
                    num_bed = "Unknown"
                else:
                    num_bed = int(num_bed)
                print("\n", house_item.format(i, info.loc[i]["post title"], info.loc[i]["neighborhood"].strip()[1:-1],
                                              info.loc[i]["sqft"], num_bed, info.loc[i]["price"]), "\n")

        elif view_choice == "n":
            # will call the fetch function
            break

        house_bad = True
        house_choice = ""
        while house_bad:

            house_choice = input("\nSelect a property for more information : (type 'exit' to quit)\n")

            if house_choice == "exit":
                break
            else:
                try:
                    house_choice = int(house_choice)
                    if house_choice not in range(1, top + 1):
                        print("bad input! enter again")
                except Exception as e:
                    print("Bad input! Enter again")

                else:
                    house_bad = False

        if house_choice == "exit":
            break

        else:
            t_str = "Transport Information"
            print("\n", t_str.center(50, "-"), "\n")
            trans_item = "Distance to nearest bus stop: {} meters\n" \
                         "Distance to CMU: {} meters\n" \
                         "Distance to downtown: {} meters\n" \
                         "Distance to nearest shuttle stop: {} meters"
            shuttle = info.loc[i]['nearest_shuttle_stop'].split(",")[-1]

            print(trans_item.format(info.loc[i]['bus_distance_CMU'], info.loc[i]['distance_to_CMU'],
                                    info.loc[i]['distance_to_downtown'], shuttle))

            r_str = "Restaurant"
            print("\n", r_str.center(50, "-"), "\n")
            print("5 restaurants near by")
            res_item = "Restaurant name: {}\n" \
                       "Rating: {}"
            restaruant = info.loc[i]['nearest_restaurants']

            restaruant = eval(str(restaruant))
            for res in restaruant:

                print(res_item.format(res[0], res[2]))

            input_chk = True
            while input_chk:
                action = input("\nPress 'b' to go back to properties listing or type 'exit' to quit\n")
                if action in ["b","exit"]:
                    input_chk = False
                else:
                    print("bad input! enter again")

            if action == "b":
                continue
            elif action == "exit":
                break



    # print(parser.parse_args())
