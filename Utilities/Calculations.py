from app.Models.Domain.FlightSearchResponse import FlightOffer
from app.Utilities import Conversions


class Calculations:
    def __init__(self, price_weighting: float, converter: Conversions):
        self.price_weighting = price_weighting
        self.duration_weighting = 1 - self.price_weighting
        self._converter = converter

    def calculate_score(self, flight_offer: FlightOffer) -> float:
        price = flight_offer.price.grand_total
        normalised_price = 1 / price
        normalised_duration = self._converter.convert_iso_time_to_minutes(flight_offer.itineraries[0].duration)

        return (normalised_price * self.price_weighting) + (normalised_duration * self.duration_weighting)