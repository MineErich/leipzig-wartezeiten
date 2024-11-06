import requests
from datetime import datetime
import logging
from pathlib import Path
# from time import sleep

# needed dir:
# dir on same level called "rawdata"

# required libraries: requests, datetime, logging, time
# install library: 
# WINDOWS: py -m pip install [library]
# UNIX: python3 -m pip install [library]

# get current dir
source_path = Path(__file__).resolve()
source_dir = source_path.parent.absolute()
# print(source_dir)

# default logfile: lwartezeiten.log
logfile = "lwartezeiten.log"

# logging conf
FORMAT = '%(asctime)s %(levelname)s [%(funcName)s] %(message)s'
logging.basicConfig(filename=logfile, encoding='utf-8', level=logging.INFO, format=FORMAT)

# header for requests
header = {
    'Content-Type': 'application/xml'
}

# ruft farplan ab
def get_current_json():
    # get time
    date = datetime.now().strftime("%y%m%d")
    hour = datetime.now().strftime("%H")
    minute = datetime.now().strftime("%M")
    # last_hour = datetime.now().hour
    
    planned_payload = requests.request("GET", 'https://dev.lehst.de/Projects/Wartezeiten/', headers=header)
    if planned_payload.status_code == 200:
        with open(str(source_dir)+'/rawdata/'+date+'_'+hour+'_'+minute+'.json', 'wb') as payload2file:
            payload2file.write(planned_payload.content)
        logging.info("saved "+date+'_'+hour+'_'+minute+'.json')
    else:
        logging.error("could not save "+date+'_'+hour+'_'+minute+'.json')

# test: call get_current_json()
get_current_json()
