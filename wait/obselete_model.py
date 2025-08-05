from pydantic import BaseModel
from typing import Optional

class Study(BaseModel):
    study_id: str
    study_name: str
    main_location_lat: Optional[float]
    main_location_long: Optional[float]
    num_of_individuals: Optional[int]
    taxon_ids: Optional[str]
    sensor_type_ids: Optional[str]
    description: Optional[str]
    authors: Optional[str]
    doi: Optional[str]

class Individual(BaseModel):
    id: str
    taxon: str
    num_of_events: str

class Event(BaseModel):
    study_id: str
    ind_id: str
    event_id: str
    timestamp: str
    location_lat: str
    location_long: str