from pydantic import *
from movebank.client import *
from movebank.schemas import Study

# TODO Move this work to test file & replace with CRUD api
def main():
    study = get_study(136953438)
    individuals = get_individuals_by_study(136953438)
    event = get_individual_events(136953438, 322208296, 'gps')
    print(study)
    print(individuals)
    print(event)

if __name__ == "__main__":
    main()