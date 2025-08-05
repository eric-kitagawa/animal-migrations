import requests
import os
import hashlib
import csv
import json
import io
from dotenv import load_dotenv
from typing import Dict

# Load environment variables
load_dotenv()

# Constants
MOVEBANK_API_URL = 'https://www.movebank.org/movebank/service/direct-read'
MOVEBANK_USERNAME = os.getenv("MOVEBANK_USERNAME")
MOVEBANK_PASSWORD = os.getenv("MOVEBANK_PASSWORD")


# TODO Explore direct JSON requests (doesn't appear to be fully supported?)
def callMovebankAPI(params):
    # Requests Movebank API with ((param1, value1), (param2, value2),).
    # Returns the API response as plain text.

    response = requests.get(MOVEBANK_API_URL, params=params, auth=(MOVEBANK_USERNAME, MOVEBANK_PASSWORD))
    print("Request " + response.url)
    if response.status_code == 200:  # successful request
        if 'License Terms:' in str(response.content):
            # only the license terms are returned, hash and append them in a subsequent request.
            # See also
            # https://github.com/movebank/movebank-api-doc/blob/master/movebank-api.md#read-and-accept-license-terms-using-curl
            print("Has license terms")
            hash = hashlib.md5(response.content).hexdigest()
            params = params + (('license-md5', hash),)
            # also attach previous cookie:
            response = requests.get(MOVEBANK_API_URL, params=params,
                                    cookies=response.cookies, auth=(MOVEBANK_USERNAME, MOVEBANK_PASSWORD))
            if response.status_code == 403:  # incorrect hash
                print("Incorrect hash")
                return ''
        return response.content.decode('utf-8')
    print(str(response.content))
    return ''


def getStudies():
    studies = callMovebankAPI((
        ('entity_type', 'study'), ('i_can_see_data', 'true'), 
        ('there_are_data_which_i_cannot_see', 'false'), 
    ))
    if len(studies) > 0:
        # parse raw text to dicts
        studies = csv_to_dict(studies)
        return studies
    return []

def getStudy(study_id):
    study = callMovebankAPI((('entity_type', 'study'), ('study_id', study_id)))
    result = csv_to_dict(study)

    if result:
        return result
    return []


def getIndividualsByStudy(study_id):
    individuals = callMovebankAPI((('entity_type', 'individual'), ('study_id', study_id)))
    result = csv_to_dict(individuals)
    print(result)
    # if len(individuals) > 0:
    #     return list(csv.DictReader(io.StringIO(individuals)))
    # return []


def getIndividualEvents(study_id, individual_id, sensor_type_id):
    # See below table for sensor_type_id's.

    params = (('entity_type', 'event'), ('study_id', study_id), ('individual_id', individual_id),
              ('sensor_type_ids', sensor_type_id), ('attributes', 'all'))
    events = callMovebankAPI(params)
    if len(events) > 0:
        return csv_to_dict(events)
    return []


def csv_to_dict(raw_csv: str) -> Dict[str, str]:
    if not raw_csv.strip():
        return []
    
    # Use csv.DictReader to parse the CSV string
    reader = csv.DictReader(io.StringIO(raw_csv))
    
    # Extract the first (and only) row as a dictionary
    result = [row for row in reader]

    return result


# Debugging
def prettyPrint(data):
    print(json.dumps(data, indent=2))

""""
SENSORS
===============================================================================
description,external_id,id,is_location_sensor,name
"","bird-ring",397,true,"Bird Ring"
"","gps",653,true,"GPS"
"","radio-transmitter",673,true,"Radio Transmitter"
"","argos-doppler-shift",82798,true,"Argos Doppler Shift"
"","natural-mark",2365682,true,"Natural Mark"
"","acceleration",2365683,false,"Acceleration"
"","solar-geolocator",3886361,true,"Solar Geolocator"
"","accessory-measurements",7842954,false,"Accessory Measurements"
"","solar-geolocator-raw",9301403,false,"Solar Geolocator Raw"
"","barometer",77740391,false,"Barometer"
"","magnetometer",77740402,false,"Magnetometer"
"","orientation",819073350,false,"Orientation"
"","solar-geolocator-twilight",914097241,false,"Solar Geolocator Twilight"
"""
