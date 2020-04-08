# README #

## Group 6 (C3) ##

* Jinxue Li (ljinxue)
* Nishan He (nishanh)
* Sanjay Renduchintala (vrenduch)
* Yu Xia (yxia2)

### Summary ###

This project aims to create a customized search platform for college students to find
local housing near the university. We are currently limiting our scope to CMU. 
This project was done as part of a programming course called Data Focused Python.

### Prerequisites ###

* Python 3.7
* Packages mentioned in `requirements.txt`
* Mozilla Firefox
* geckodriver (runs on macOS using default settings for another OS change `config.py`)
* Google API Key (a default key provided in `config.py` for instructor's evaluation)

### Data Sources ###

* Craigslist (Default: Scrapes 2 pages. Can be increased in `config.py`)
* Yelp API
* CMU Shuttle Maps (4 custom Google Maps)
* Google Maps API

Detailed description and sample data: [Spreadsheet](https://docs.google.com/spreadsheets/d/1its0lItWUqh1YIxLvIme16pkwIeaMej2T3CIWyztjdo/edit?usp=sharing)

### Source Code ###

Link to project repository: [BitBucket Repo](https://bitbucket.org/vrenduch/dfp-group-project/src/master/)

### Usage ###

Demo video is available here: [Youtube Video](http://www.youtube.com/watch?v=pikOi92-71Y)  
    
`python3 main.py` runs the application with default options. By default the application runs using cached data from the previous run. To run using the latest data use options `--latest` or `--refresh_all`. Additional optional arguments are listed below.

### Help menu ###

`main.py -h` presents a help as shown below: 

    usage: main.py [-h] [-l] [-y] [-s] [-a] [-p PRICE_FILTER [PRICE_FILTER ...]]
               [-t TOP]

    optional arguments:
      -h, --help            show this help message and exit
      -l, --latest          Fetches latest properties from Craigslist
      -y, --refresh_yelp    Refreshes restaurants database with latest info from
                            Yelp
      -s, --refresh_shuttle
                            Refreshes shuttles database with latest info from CMU
      -a, --refresh_all     Refreshes all databases and uses latest information
      -p PRICE_FILTER [PRICE_FILTER ...], --price_filter PRICE_FILTER [PRICE_FILTER ...]
                            Optional price range filter. Usage: -p <MIN> <MAX>
      -t TOP, --top TOP     Number of properties to be displayed
      

### Interactions ###

This is the interactive menu presented to the user to navigate the housing recommendations
 
#### Step 1: Input 'y' to see the property recommendations ####
    Show the top 6 properties we recommend? (y to continue, exit to quit)
    
Example output:
    
    1. One Bedroom Available 08/01  
    Neighborhood: Oakland
    Size: 415.0 sqft
    Number of bedrooms: 1
    Price: 845$/month 
    
    2. ★Available NOW--AC--Hardwood Floors--Closet Space--Heat Incld!★  
    Neighborhood: Squirrel Hill / Murry Ave @ Forward Ave
    Size: 770.0 sqft
    Number of bedrooms: 1
    Price: 1295$/month 

    
#### Step 2: Select the property number from the displayed list ####
    Select a property for more information : (type 'exit' to quit)
    
Example output:
    
    --------------Transport Information--------------- 
    
    Distance to nearest bus stop: 82.0 meters
    Distance to CMU: 3222.0 meters
    Distance to downtown: 6409.0 meters
    Distance to nearest shuttle stop:  2.0014903583595665) meters
    
     --------------------Restaurant-------------------- 
    
    5 restaurants near by
    Restaurant name: Selamis Turkish Kebab House
    Rating: 4.5
    Restaurant name: BFG Café
    Rating: 4.0
    Restaurant name: Nak Won Garden
    Rating: 3.5
    Restaurant name: Spork Pit
    Rating: 3.5
    Restaurant name: Friendship Perk and Brew
    Rating: 4.5

 
#### Step 3: Option to go back to property listings or exit ####
    Press 'b' to go back to properties listing or type 'exit' to quit
    
    