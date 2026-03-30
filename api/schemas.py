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

class FacilitySummary(BaseModel):
    facility_id:        int
    avg_percent_outage: float
    max_percent_outage: float
    total_mw_lost:      float
    days_with_outage:   int
    avg_capacity_factor: float
    total_records:      int
    last_reported:      str
    is_active:          bool


class Seasonality(BaseModel):
    month:             int
    avg_percent_outage: float
    avg_mw_offline:    float
    total_mw_lost:     float
    record_count:      int


class UsTotal(BaseModel):
    period:            str
    total_capacity:    float
    total_mw_offline:  float
    active_facilities: int
    percent_offline:   float