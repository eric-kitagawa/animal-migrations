import requests
import hashlib
import os
import csv
import io
from typing import List
from dotenv import load_dotenv
from backend.obselete_model import Study, Individual, Event
from utils import _safe_float, _safe_int

# Load environment variables
load_dotenv()

# Constants
MOVEBANK_API_URL = "https://www.movebank.org/movebank/service/direct-read"
MOVEBANK_USERNAME = os.getenv("MOVEBANK_USERNAME")
MOVEBANK_PASSWORD = os.getenv("MOVEBANK_PASSWORD")

# Utility function to make API calls (keep as is)
def call_movebank_api(params):
    response = requests.get('https://www.movebank.org/movebank/service/direct-read', 
                          params=params, auth=(MOVEBANK_USERNAME, MOVEBANK_PASSWORD))
    print("Request " + response.url)
    if response.status_code == 200:
        if 'License Terms:' in str(response.content):
            print("Has license terms")
            hash = hashlib.md5(response.content).hexdigest()
            params = params + (('license-md5', hash),)
            response = requests.get('https://www.movebank.org/movebank/service/direct-read', 
                                  params=params, cookies=response.cookies, 
                                  auth=(MOVEBANK_USERNAME, MOVEBANK_PASSWORD))
            if response.status_code == 403:
                print("Incorrect hash")
                return ''
        return response.content.decode('utf-8')
    print(str(response.content))
    return ''

def get_studies() -> List[Study]:
    """
    Fetch all studies from the Movebank API and parse them into Study models.
    """
    params = (
        ("entity_type", "study"),
        ("i_can_see_data", "true"),
        ("there_are_data_which_i_cannot_see", "false"),
        ("i_have_download_access", "true"),
        ("sensor_type_ids", "653"), #Currently only naming gps for sake of simplicity
    )
    raw_data = call_movebank_api(params)
    
    if raw_data:
        studies_dicts = list(csv.DictReader(io.StringIO(raw_data), delimiter=","))
        print(studies_dicts)
        studies = []
        
        for study_dict in studies_dicts:
            # Handle type conversions and field mapping
            study_data = {
                'study_id': study_dict.get('id', ''),
                'study_name': study_dict.get('name', ''),
                'main_location_lat': _safe_float(study_dict.get('main_location_lat')),
                'main_location_long': _safe_float(study_dict.get('main_location_long')),
                'num_of_individuals': _safe_int(study_dict.get('number_of_individuals')),
                'taxon_ids': study_dict.get('taxon_ids'),
                'sensor_type_ids': study_dict.get('sensor_type_ids'),
                'description': study_dict.get('description'),
                'authors': study_dict.get('principal_investigator_name'),
                'doi': study_dict.get('doi')
            }
            studies.append(Study(**study_data))
        
        return studies
    return []

def get_individuals_by_study(study_id: int) -> List[Individual]:
    """
    Fetch individuals for a given study ID and return as Individual models.
    """
    params = (
        ("entity_type", "individual"),
        ("study_id", study_id),
    )
    raw_data = call_movebank_api(params)

    if raw_data:
        individuals_dicts = list(csv.DictReader(io.StringIO(raw_data), delimiter=","))
        individuals = []
        
        for individual_dict in individuals_dicts:
            individual_data = {
                'id': individual_dict.get('id', ''),
                'taxon': individual_dict.get('taxon_canonical_name', ''),
                'num_of_events': individual_dict.get('number_of_events', '0')
            }
            individuals.append(Individual(**individual_data))
        
        return individuals
    return []

def get_individual_events(study_id: int, individual_id: int, sensor_type_id: int = 653) -> List[Event]:
    """
    Fetch events for an individual and return as Event models.
    """
    params = (
        ('entity_type', 'event'), 
        ('study_id', study_id), 
        ('individual_id', individual_id),
        ('sensor_type_id', sensor_type_id), 
        ('attributes', 'all'),
    )
    raw_data = call_movebank_api(params)
    
    if raw_data:
        events_dicts = list(csv.DictReader(io.StringIO(raw_data), delimiter=','))
        events = []
        
        for event_dict in events_dicts:
            event_data = {
                'study_id': str(study_id),
                'ind_id': str(individual_id),
                'event_id': event_dict.get('event_id', ''),
                'timestamp': event_dict.get('timestamp', ''),
                'location_lat': event_dict.get('location_lat', ''),
                'location_long': event_dict.get('location_long', '')
            }
            events.append(Event(**event_data))
        
        return events
    return []