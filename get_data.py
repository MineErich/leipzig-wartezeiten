#####################################################
#               WHAT IS THIS ?                      #
#####################################################
# This shall be the script which does not only
# request and save the raw data, but will also 
# extract the needed data and write it to:
# 1. daily json     (data of the day)
# 2. 30days.json    (data of the month)
# 3. alltime.json   (every data since start)
#####################################################



#####################################################
#                 INSTRUCTIONS                      #
#####################################################
# needed dir:
# dir on same level called "rawdata"

# required libraries: requests, datetime, logging, time
# install library: 
# WINDOWS: py -m pip install [library]
# UNIX: python3 -m pip install [library]
#####################################################

import requests
from datetime import datetime
import logging
from os import path as ospath

# get current dir
source_dir = ospath.dirname(ospath.realpath(__file__))

# default logfile: lwartezeiten.log
logfile = "lwartezeiten.log"

# logging conf
FORMAT = '%(asctime)s %(levelname)s [%(funcName)s] %(message)s'
logging.basicConfig(filename=logfile, encoding='utf-8', level=logging.INFO, format=FORMAT)

# request to api
def get_current_json():
    # get date
    # important: get date before working with data, so date does not get mixed up from operation to operation!
    date = datetime.now().strftime("%y%m%d_%H_%M")
    
    get_current_data = requests.get('https://dev.lehst.de/Projects/Wartezeiten/')
    if get_current_data.status_code == 200:
        # Daten extrahieren in buffer schreiben
            # json-obj aufmachen
            # for location in data:
            # HELP:
            # ich will hier nur differenz sammeln und dann in day;30days;alltime.json schreiben..
            # sonst muss ich immer das gesamte file einlesen und dumpen
            # btw. wollte ich alltime vllt auf jährlich begrenzen oder so. dunno
            #   schreib das ins json-obj
            #   schieb json-obj in day;30days;alltime.json
            # 
        # 1. D in tagesaktuelle json speichern
        # 2. D in 30days.json speichern
        # 3. D in alltime.json speichern
        # 4. D als orig in rawdata/ ablegen
        with open(ospath.join(source_dir, 'rawdata',date,)+'.json', 'wb') as payload2file:
            payload2file.write(get_current_data.content)
        logging.info("saved "+date+'.json')
    else:
        # statuscode != 200 (this is bad)
        logging.error("could not fetch current json")

# test: call get_current_json()
get_current_json()
