from pydantic import *
from movebank.client import *
from movebank.schemas import Study

# TODO Turn this from a test file into a proper 
def main():
    study = callMovebankAPI((('entity_type', 'study'), ('study_id', 136953438)))

if __name__ == "__main__":
    main()