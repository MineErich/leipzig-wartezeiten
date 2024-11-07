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

# required libraries: requests, datetime, logging, 
#   os, json
# install library: 
# WINDOWS: py -m pip install [library]
# UNIX: python3 -m pip install [library]
#####################################################

import requests
from datetime import datetime
import logging
from os import path as ospath
import json

# get current dir
source_dir = ospath.dirname(ospath.realpath(__file__))

# default logfile: lwartezeiten.log
logfile = "lwartezeiten.log"

# logging conf
FORMAT = '%(asctime)s %(levelname)s [%(funcName)s] %(message)s'
logging.basicConfig(filename=logfile, encoding='utf-8', level=logging.INFO, format=FORMAT)

def overwrite_jsonfiles(input, data, who):
    try:
        with open(input, encoding="utf-8") as f:
            ujson = json.load(f)
            ujson.update(data)
    except FileNotFoundError:
        fp = open(input, 'x')
        fp.close()
        ujson = json.loads(json.dumps(data))
    with open(input, 'w', encoding="utf-8") as f:
        json.dump(ujson, f, ensure_ascii=False, indent=4)
        logging.info("saved to "+who)


# request to api
def get_current_json():
    # get date
    # important: get date before working with data, so date does not get mixed up from operation to operation!
    date = datetime.now().strftime("%y%m%d_%H_%M")
    
    get_current_data = requests.get('https://dev.lehst.de/Projects/Wartezeiten/')
    if get_current_data.status_code == 200:
        # tmp json object
        new_json = {date: {}}
        # Daten extrahieren in buffer schreiben
        current_d_json = json.loads(get_current_data.content)
        for location, values in current_d_json["locations"].items():
            # Datenstruktur mit Datum und Uhrzeit als Schlüssel und Werten als Objekt
            data_entry = {
                # date: {
                    location: {
                        "active_counter_count": values["active_counter_count"],
                        "walkin_waiting_count": values["walkin_waiting_count"],
                        "walkin_serving_count": values["walkin_serving_count"],
                        "walkin_average_waitingtime": values["walkin_average_waitingtime"],
                        "walkin_end_count": values["walkin_end_count"],
                        "predicted_waiting_time": values["predicted_waiting_time"]
                    } 
                # }
            }
            # Daten zur Liste hinzufügen
            # new_json.append(data_entry)
            new_json[date].update(data_entry)

        # 1. save new values to todays json
        today = datetime.now().strftime("%y%m%d")
        overwrite_jsonfiles(ospath.join(source_dir, 'daily',today,)+'.json', new_json, 'daily')

        # 2. save new values to this month json
        tomonth = datetime.now().strftime("%y%m")
        overwrite_jsonfiles(ospath.join(source_dir, 'monthly',tomonth,)+'.json', new_json, 'monthly')

        # 3. save new values to alltime.json
        overwrite_jsonfiles(ospath.join(source_dir, 'alltime.json'), new_json, 'alltime')

        # 4. save original json to rawdata/
        with open(ospath.join(source_dir, 'rawdata',date,)+'.json', 'wb') as payload2file:
            payload2file.write(get_current_data.content)
            logging.info("saved to rawdata")

    else:
        # statuscode != 200 (this is bad)
        logging.error("could not fetch current json")

# test: call get_current_json()
get_current_json()
