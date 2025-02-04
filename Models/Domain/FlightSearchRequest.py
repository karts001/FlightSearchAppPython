from typing import Optional, List
from pydantic import Field, BaseModel


class DateTimeRange(BaseModel):
    date: str
    time: str


class OriginDestination(BaseModel):
    id: int
    origin_location_code: str = Field(alias="originLocationCode")
    destination_location_code: str = Field(alias="destinationLocationCode")
    departure_date_time_range: DateTimeRange = Field(alias="departureDateTimeRange")


class Traveler(BaseModel):
    id: int
    traveler_type: str = Field(alias="travelerType")

class CabinRestrictions(BaseModel):
    cabin: Optional[str] = None
    coverage: Optional[str] = None
    origin_destination_ids: int = Field(alias="originDestinationIds")


class CarrierRestrictions(BaseModel):
    exclude_carrier_codes: Optional[List[str]] = Field(alias="excludeCarrierCodes", default=None)


class FlightFilters(BaseModel):
    cabin_restrictions: CabinRestrictions = Field(alias="cabinRestrictions")
    carrier_restrictions: CarrierRestrictions = Field(alias="carrierRestrictions")


class SearchCriteria(BaseModel):
    max_flight_offers: int = Field(alias="maxFlightOffers", default=None)
    flight_filters: FlightFilters = Field(alias="flightFilters", default=None)


class FlightSearchRequest(BaseModel):
    currency_code: str = Field(alias="currencyCode", default="GBP")
    origin_destinations: List[OriginDestination] = Field(alias="originDestinations")
    travelers: List[Traveler]
    sources: List[str]
    search_criteria: SearchCriteria = Field(alias="searchCriteria", default=None)
