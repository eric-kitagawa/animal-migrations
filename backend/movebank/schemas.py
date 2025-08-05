import pydantic as _pydantic

class Study(_pydantic.BaseModel):
    study_id: int = _pydantic.Field(alias="id")
    name: str
    taxon: str = _pydantic.Field(alias="taxon_ids")
    number_of_individuals: int

class Individual(_pydantic.BaseModel):
    individual_id: int
    study_id: int
    taxon: str
    number_of_events: int

class Event(_pydantic.BaseModel):
    event_id: int
    individual_id: int
    study_id: int
    timestamp: str
    # TODO add location data







# id: str
# name: str
# main_lat: str
# main_long: str
# ts_first_deploy: str
# ts_last_deploy: str
# sensor_type_ids: str
# taxon_ids: str
# number_of_individuals: str
# number_of_tags: str
# number_of_locations: str
