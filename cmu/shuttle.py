from selenium import webdriver
import pandas as pd
import os

import sys
sys.path.append('../')
import config


webdriver_path = config.webdriver_path


def get_shuttle_stops():
    """
    Scrapes Google Map created by CMU to get bus stops for CMU shuttle
    :return: bus stops for CMU shuttle
    """

    null = "null"
    false = "false"
    true = "true"

    driver = webdriver.Firefox(executable_path=webdriver_path)

    driver.get(
        'https://www.google.com/maps/d/u/0/viewer?mid=1nlvSKs1efNJN_XF3Pq8xN0zus9E&ll=40.45065582444209%2C-79'
        '.94149449999998&z=16')
    _pageData = driver.execute_script('return _pageData')

    data_list = eval(_pageData.strip())

    data = []
    for i in data_list[1][6][0][4]:
        try:
            data.append([i[4][0][1][0], i[4][0][1][1], i[5][0][0]])
        except:
            pass

    route_a = pd.DataFrame(data, columns=['lat', 'long', 'name'])
    route_a['route'] = 'A'
    print("Scrapped route A successfully!")

    driver.get(
        'https://www.google.com/maps/d/u/0/viewer?mid=1u6tib7ziB2WhnyB1H3FueOaxB1o&ll=40.45305942967349%2C-79.93174649999997&z=15')
    _pageData = driver.execute_script('return _pageData')
    data_list = eval(_pageData.strip())

    data = []
    for i in data_list[1][6][0][4]:
        try:
            data.append([i[4][0][1][0], i[4][0][1][1], i[5][0][0]])
        except:
            pass

    route_b = pd.DataFrame(data, columns=['lat', 'long', 'name'])
    route_b['route'] = 'B'
    print("Scrapped route B successfully!")

    driver.get(
        'https://www.google.com/maps/d/u/0/viewer?mid=1-2CGWycO35moaKwMf_EjnDr49fE&ll=40.45236950876952%2C-79.9370156&z=15')
    _pageData = driver.execute_script('return _pageData')
    data_list = eval(_pageData.strip())

    data = []
    for i in data_list[1][6][0][4]:
        try:
            data.append([i[4][0][1][0], i[4][0][1][1], i[5][0][0]])
        except:
            pass

    route_ab = pd.DataFrame(data, columns=['lat', 'long', 'name'])
    route_ab['route'] = 'AB'
    print("Scrapped route AB successfully!")


    driver.get(
        'https://www.google.com/maps/d/u/0/viewer?mid=1PktbKCIDcq6BWugIxaWTf1MtfdI&ll=40.43523578508325%2C-79.95123999999998&z=15')
    _pageData = driver.execute_script('return _pageData')
    data_list = eval(_pageData.strip())

    data = []
    for i in data_list[1][6][0][4]:
        try:
            data.append([i[4][0][1][0], i[4][0][1][1], i[5][0][0]])
        except:
            pass

    route_ptc = pd.DataFrame(data, columns=['lat', 'long', 'name'])
    route_ptc['route'] = 'PTC'
    print("Scrapped route PTC successfully!")


    driver.get(
        'https://www.google.com/maps/d/u/0/viewer?mid=1T4O7QCmmanIry70ks1tjhm58aUg&ll=40.44699122648596%2C-79.93365500000004&z=14')
    _pageData = driver.execute_script('return _pageData')
    data_list = eval(_pageData.strip())

    data = []
    for i in data_list[1][6][0][4]:
        try:
            data.append([i[4][0][1][0], i[4][0][1][1], i[5][0][0]])
        except:
            pass

    route_bs = pd.DataFrame(data, columns=['lat', 'long', 'name'])
    route_bs['route'] = 'BS'
    print("Scrapped Baker Street route successfully!")


    return route_a.append([route_b, route_ab, route_ptc, route_bs])


if __name__ == '__main__':
    print(get_shuttle_stops())
