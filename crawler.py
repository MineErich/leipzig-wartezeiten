#####################################################
#               WHAT IS THIS ?                      #
#####################################################
# This is the basic crawler that will request the
# data from the api and save the json-files to your
# local storage.
# usefull for just collecting data, that will be used
# later (also good, when purpose is unknown)
#
# recommended: create a cronjob to run this file
# every hour or so.
#####################################################


#####################################################
#                 INSTRUCTIONS                      #
#####################################################
# needed dir:
# dir on same level called "rawdata"

# required libraries: requests, datetime, logging, os
# install library: 
# WINDOWS: py -m pip install [library]
# UNIX: python3 -m pip install [library]
#####################################################

import requests
from datetime import datetime
import logging
from os import path as ospath
from os import makedirs as osmakedirs

# default logfile: crawler.log
logfile = "crawler.log"

# logging conf
FORMAT = '%(asctime)s %(levelname)s [%(funcName)s] %(message)s'
logging.basicConfig(filename=logfile, encoding='utf-8', level=logging.WARN, format=FORMAT)


# get current dir
source_dir = ospath.dirname(ospath.realpath(__file__))

# check for needed dirs
# if not present create them
needed_dirs = ["daily","monthly","rawdata"]
for dir in needed_dirs:
    if not ospath.isdir(ospath.join(source_dir,dir)):
        osmakedirs(ospath.join(source_dir,dir))
        logging.info(dir+" was not present. created it!")

# request to api
def get_current_json():
    # get date
    # important: get date before working with data, so date does not get mixed up from operation to operation!
    date = datetime.now().strftime("%y%m%d_%H_%M")
    
    get_current_data = requests.get('https://dev.lehst.de/Projects/Wartezeiten/')
    if get_current_data.status_code == 200:
        with open(ospath.join(source_dir, 'rawdata',date,)+'.json', 'wb') as payload2file:
            payload2file.write(get_current_data.content)
        logging.info("saved "+date+'.json')
    else:
        # statuscode != 200 (this is bad)
        logging.error("could not fetch current json")

# test: call get_current_json()
get_current_json()
