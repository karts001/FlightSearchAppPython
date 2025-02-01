from datetime import datetime
from typing import List, Optional
from pydantic import Field, BaseModel


class IncludedCheckedBagsDTO(BaseModel):
    weight: int
    weight_unit: str = Field(alias="weightUnit", default="kg")
    quantity: Optional[int] = None


class FareDetailsBySegmentDTO(BaseModel):
    include_checked_bags: Optional[IncludedCheckedBagsDTO] = Field(alias="includeCheckedBags", default=None)


class TravelerPricingSummaryDTO(BaseModel):
    traveler_id: int = Field(alias="travelerId")
    fare_details_by_segment: List[FareDetailsBySegmentDTO] = Field(alias="fareDetailsBySegment")


class PriceDTO(BaseModel):
    currency: str
    total: str
    grand_total: float = Field(alias="grandTotal")


class PricingOptionsDTO(BaseModel):
    included_checked_bags_only: bool = Field(alias="includedCheckedBagsOnly")


class FlightInfoDTO(BaseModel):
    iata_code: str = Field(alias="iataCode")
    terminal: Optional[str] = None
    departure_at: datetime = Field(alias="at")


class SegmentDTO(BaseModel):
    departure_info: FlightInfoDTO = Field(alias="departure")
    arrival_info: FlightInfoDTO = Field(alias="arrival")
    carrier_code: Optional[str] = Field(alias="carrierCode", default=None)
    segment_duration: str = Field(alias="duration")
    number_of_stops: int = Field(alias="numberOfStops")


class ItineraryDTO(BaseModel):
    duration: str
    segments: List[SegmentDTO]


class FlightOfferDTO(BaseModel):
    id: int
    number_of_bookable_seats: int = Field(alias="numberOfBookableSeats")
    source: str
    itineraries: List[ItineraryDTO]
    price: PriceDTO
    pricing_options: PricingOptionsDTO = Field(alias="pricingOptions")
    travel_pricings: List[TravelerPricingSummaryDTO] = Field(alias="travelerPricings")
    validation_airline_codes: List[str] = Field(alias="validatingAirlineCodes")

class FlightSearchResponseDTO(BaseModel):
    meta: Optional[dict] = Field(default=None)
    data: List[FlightOfferDTO]