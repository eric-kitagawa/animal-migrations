from pydantic import *
from movebank.client import *
from movebank.schemas import Study

# TODO Turn this from a test file into a proper 
def main():
    study = callMovebankAPI((('entity_type', 'study'), ('study_id', 136953438)))
    print(study)
    # study = getStudy(study_id=136953438)
    # study = getStudy(study_id=136953438)
    # study_model = [Study.model_validate(row) for row in study]
    # print(study_model)
    # individuals = getIndividualsByStudy(study_id=136953438)
    # prettyPrint(individuals)

    # events = getIndividualEvents(study_id=136953438, individual_id=322208299, sensor_type_id="gps")
    # prettyPrint(events)

    # gpsevents = getIndividualEvents(study_id=9493874, individual_id=11522613, sensor_type_id=653) #GPS events
    # if len(gpsevents) > 0:
    #     prettyPrint(transformRawGPS(gpsevents))

    # # Print tri-axial acceleration in m/s^2: [(ts, deployment, accx, accy, accz), [ts,...],...]
    # accevents = getIndividualEvents(study_id=9493874, individual_id=11522613, sensor_type_id=2365683) #ACC events
    # if len(accevents) > 0:
    #     prettyPrint(transformRawACC(accevents))

if __name__ == "__main__":
    main()