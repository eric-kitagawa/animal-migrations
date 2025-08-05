from backend.obselete_services import get_studies, get_individuals_by_study, get_individual_events
from backend.obselete_model import *

def main():
    # Step 1: Fetch all studies
    print("Fetching studies...")
    try:
        studies = get_studies()
        print(f"Found {len(studies)} studies.")
        if studies:
            print("Sample study:")
            print(studies[0])  # Print the first study for inspection
    except Exception as e:
        print(f"Error fetching studies: {e}")

    # Step 2: Fetch individuals for a specific study ID
    if studies:
        study_id = 136953438
        # study_id = int(studies[0]["id"])  # Use the ID of the first study
        print(f"\nFetching individuals for study ID: {study_id}")
        try:
            individuals = get_individuals_by_study(study_id)
            print(f"Found {len(individuals)} individuals.")
            if individuals:
                print("Sample individual:")
                print(individuals[0])  # Print the first individual for inspection
        except Exception as e:
            print(f"Error fetching individuals: {e}")

    # Step 3: Fetch GPS locations for a specific individual ID
    if individuals:
        individual_id = individuals[0].id  # Use the ID of the first individual
        print(f"\nFetching events for individual ID: {individual_id}...")
        individual_events = get_individual_events(study_id, individual_id, sensor_type_id=653)
        print(individual_events)


if __name__ == "__main__":
    main()