from pydantic import *
from movebank.client import *
from movebank.schemas import Study

# TODO Move this work to test file & replace with CRUD api
def main():
    study = call_movebank_api((('entity_type', 'study'), ('study_id', 136953438)))
    print (study)

if __name__ == "__main__":
    main()