# schemas.py

from pydantic import BaseModel


class Facility(BaseModel):
    facility_id:   int
    facility_name: str


class FacilityOutage(BaseModel):
    period:         str
    facility_id:    int
    capacity:       float
    outage:         float
    percent_outage: float


class GeneratorOutage(BaseModel):
    period:         str
    facility_id:    int
    generator_id:   int
    capacity:       float
    outage:         float
    percent_outage: float


class DataResponse(BaseModel):
    total:  int
    page:   int
    limit:  int
    data:   list


class RefreshResponse(BaseModel):
    status:  str
    message: str