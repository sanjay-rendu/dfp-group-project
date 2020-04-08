from requests import get
from bs4 import BeautifulSoup
from time import sleep
from random import randint  # avoid throttling by not sending too many requests one after the other
from warnings import warn
import numpy as np
import pandas as pd

city_url = {
    'Pittsburgh': 'https://pittsburgh.craigslist.org/search/hhh?availabilityMode=0&hasPic=1&bundleDuplicates=1'
}


def scrape_it(city, num_pages):
    """
    Scrapes Craigslist to get rental posts for a city

    :param city: City to search
    :param num_pages: Number of pages to scarpe

    :return: Dataframe with web postings
    """

    response = get(city_url[city])

    html_soup = BeautifulSoup(response.text, 'html.parser')
    posts = html_soup.find_all('li', class_='result-row')

    # find the total number of posts to find the limit of the pagination
    results_num = html_soup.find('div', class_='search-legend')
    results_total = int(results_num.find('span',
                                         class_='totalcount').text)
    # pulled the total count of posts as the upper
    # bound of the pages array

    results_total = min(results_total, 120*num_pages)  # limit to number of pages

    # each page has 119 posts so each new page is defined as follows: s=120, s=240, s=360, and so on. So we need to
    # step in size 120 in the np.arange function
    pages = np.arange(0, results_total + 1, 120)

    iterations = 0

    post_timing = []
    post_hoods = []
    post_title_texts = []
    bedroom_counts = []
    sqfts = []
    post_links = []
    post_prices = []
    post_locations = []

    for page in pages:

        # get request
        response = get("https://pittsburgh.craigslist.org/search/hhh"
                       + "s="  # the parameter for defining the page number
                       + str(page)  # the page number in the pages array from earlier
                       + "&hasPic=1"
                       + "&availabilityMode=0")

        sleep(randint(1, 3))

        # throw warning for status codes that are not 200
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(response, response.status_code))

        # define the html text
        page_html = BeautifulSoup(response.text, 'html.parser')

        # define the posts
        posts = html_soup.find_all('li', class_='result-row')

        # extract data item-wise
        for post in posts:

            if post.find('span', class_='result-hood') is not None:

                # posting date
                # grab the datetime element 0 for date and 1 for time
                post_datetime = post.find('time', class_='result-date')['datetime']
                post_timing.append(post_datetime)

                # neighborhoods
                post_hood = post.find('span', class_='result-hood').text
                post_hoods.append(post_hood)

                # title text
                post_title = post.find('a', class_='result-title hdrlnk')
                post_title_text = post_title.text
                post_title_texts.append(post_title_text)

                # post link
                post_link = post_title['href']
                post_links.append(post_link)

                # post location
                post_open = get(post_link)
                post_open_html = BeautifulSoup(post_open.text, 'html.parser')
                post_geo = post_open_html.find_all('meta')[-3]
                post_location = post_geo['content']
                post_locations.append(post_location)

                # removes the \n whitespace from each side, removes the currency symbol, and turns it into an int
                post_price = int(post.a.text.strip().replace("$", ""))
                post_prices.append(post_price)

                if post.find('span', class_='housing') is not None:

                    # if the first element is accidentally square footage
                    if 'ft2' in post.find('span', class_='housing').text.split()[0]:

                        # make bedroom nan
                        bedroom_count = np.nan
                        bedroom_counts.append(bedroom_count)

                        # make sqft the first element
                        sqft = int(post.find('span', class_='housing').text.split()[0][:-3])
                        sqfts.append(sqft)

                    # if the length of the housing details element is more than 2
                    elif len(post.find('span', class_='housing').text.split()) > 2:

                        # therefore element 0 will be bedroom count
                        bedroom_count = post.find('span', class_='housing').text.replace("br", "").split()[0]
                        bedroom_counts.append(bedroom_count)

                        # and sqft will be number 3, so set these here and append
                        sqft = int(post.find('span', class_='housing').text.split()[2][:-3])
                        sqfts.append(sqft)

                    # if there is num bedrooms but no sqft
                    elif len(post.find('span', class_='housing').text.split()) == 2:

                        # therefore element 0 will be bedroom count
                        bedroom_count = post.find('span', class_='housing').text.replace("br", "").split()[0]
                        bedroom_counts.append(bedroom_count)

                        # and sqft will be number 3, so set these here and append
                        sqft = np.nan
                        sqfts.append(sqft)

                    else:
                        bedroom_count = np.nan
                        bedroom_counts.append(bedroom_count)

                        sqft = np.nan
                        sqfts.append(sqft)

                # if none of those conditions catch, make bedroom nan, this won't be needed
                else:
                    bedroom_count = np.nan
                    bedroom_counts.append(bedroom_count)

                    sqft = np.nan
                    sqfts.append(sqft)

        iterations += 1
        print("Page " + str(iterations) + " scraped successfully!")

    eb_apts = pd.DataFrame({'posted': post_timing,
                            'neighborhood': post_hoods,
                            'location': post_locations,
                            'post title': post_title_texts,
                            'number bedrooms': bedroom_counts,
                            'sqft': sqfts,
                            'URL': post_links,
                            'price': post_prices})

    eb_apts["lat"] = eb_apts["location"].str[:9]
    eb_apts["long"] = eb_apts["location"].str[10:]
    eb_apts["lat"] = pd.to_numeric(eb_apts["lat"], errors='coerce')
    eb_apts["long"] = pd.to_numeric(eb_apts["long"], errors='coerce')
    eb_apts = eb_apts.dropna(subset = ["lat"])
    return eb_apts