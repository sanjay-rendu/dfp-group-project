import os

# NOTE: Replace this with local geckodriver location - https://github.com/mozilla/geckodriver/releases
# NOTE: Mozilla Firefox browser is a requirement and should be installed for selenium to work!
webdriver_path =  str(os.path.dirname(os.path.abspath(__file__))) + "/cmu/geckodriver"

# NOTE: This the number of latest pages of Craigslist that will be scrapped. Increase the number for more data.
craig_num_of_pages = 2

# NOTE: GOOGLE API COSTS MONEY!
# NOTE: Ideally this key should be saved as environment variable and kept secret
# Published on instructor's request to avoid env variables. Do not make this public!!!
# INTENTIONALLY LEFT BLANK
API_key = ''