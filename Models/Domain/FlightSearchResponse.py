from datetime import datetime

from typing import List, Optional
from pydantic import Field, BaseModel, field_validator


class IncludedCheckedBags(BaseModel):
    weight: int
    weight_unit: str = Field(default="kg")
    quantity: Optional[int] = None

    @field_validator("weight")
    def positive_weight_only(cls, value):
        if value <= 0:
            raise ValueError("Positive weights only")
        return value

class FareDetailsBySegment(BaseModel):
    include_checked_bags: Optional[IncludedCheckedBags] = Field(default=None)

class TravelerPricingSummary(BaseModel):
    traveler_id: int
    fare_details_by_segment: List[FareDetailsBySegment]

class Price(BaseModel):
    currency: str
    total: str
    grand_total: float

class PricingOptions(BaseModel):
    included_checked_bags_only: bool

class FlightInfo(BaseModel):
    iata_code: str
    terminal: Optional[str] = None
    departure_at: datetime

class Segment(BaseModel):
    departure_info: FlightInfo
    arrival_info: FlightInfo
    carrier_code: Optional[str] = None
    segment_duration: str
    number_of_stops: int

class Itinerary(BaseModel):
    duration: str
    segments: List[Segment]

class FlightOffer(BaseModel):
    id: int
    number_of_bookable_seats: int
    source: str
    itineraries: List[Itinerary]
    price: Price
    pricing_options: PricingOptions
    travel_pricings: List[TravelerPricingSummary]
    validation_airline_codes: List[str]
    score: Optional[float] = None

class FlightSearchResponse(BaseModel):
    flights: List[FlightOffer]