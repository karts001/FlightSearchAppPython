from datetime import datetime

from typing import List, Optional
from pydantic import Field, BaseModel, field_validator


class IncludedCheckedBagsDTO(BaseModel):
    weight: int
    weight_unit: str = Field(alias="weightUnit", default="kg")
    quantity: Optional[int] = None

    @field_validator("weight")
    def positive_weight_only(cls, value):
        if value <= 0:
            raise ValueError("Positive weights only")
        return value

class FareDetailsBySegmentDTO(BaseModel):
    include_checked_bags: IncludedCheckedBagsDTO = Field(alias="includeCheckedBags")

class TravelerPricingSummaryDTO(BaseModel):
    traveler_id: int = Field(alias="travelerId")
    fare_details_by_segment: List[FareDetailsBySegmentDTO] = Field(alias="fareDetailsBySegment")

class PriceDTO(BaseModel):
    currency: str
    total: str
    grand_total: float = Field(alias="grandTotal")

class PricingOptions(BaseModel):
    included_checked_bags_only: bool = Field(alias="includedCheckedBagsOnly")

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
    price: PriceDTO
    pricing_options: PricingOptions
    travel_pricings: List[TravelerPricingSummaryDTO]
    validation_airline_codes: List[str]
    score: float

class FlightSearchResponse(BaseModel):
    flights: List[FlightOffer] = Field(alias="data")