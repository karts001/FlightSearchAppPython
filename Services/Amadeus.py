import os
import json

from typing import List
import httpx

from app.Services.IAmadeus import IAmadeus
from app.Models.Domain.FlightSearchRequest import FlightSearchRequest
from app.Models.DTO.FlightSearchResponseDTO import FlightOfferDTO
from app.Models.Domain.FlightSearchResponse import FlightOffer, Itinerary, Price, PricingOptions, TravelerPricingSummary
from app.Services.TokenService import TokenService


class Amadeus(IAmadeus):
    def __init__(self, token_service: TokenService):
        self._base_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        self._authentication_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        self.token_service = token_service

    async def authenticate_api(self) -> str:

        # get api auth details from .env file
        client_id = os.environ.get("CLIENT_ID")
        client_secret = os.environ.get("CLIENT_SECRET")

        # api requires the header to be set to this
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self._authentication_url}", data=body, headers=headers)

        access_token = response.json().get("access_token")

        # update the token in the database
        await self.token_service.update_token(access_token)

    async def get_flights(self, request: FlightSearchRequest, is_retry=False) -> List[FlightOfferDTO]:
        token = await self.token_service.get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "X-HTTP-Method-Override": "POST"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self._base_url, json=request.model_dump(by_alias=True), headers=headers, timeout=30)
            if response.status_code == 200:
                # convert the json response into the FlightSearchResponseDTO object
                flight_offers = response.json().get("data", [])
                dtos = [FlightOfferDTO(**flight) for flight in flight_offers]

                return self.convert_flight_offer_dto_to_domain(dtos)

            elif response.status_code == 401 and not is_retry:
                # we aren't authenticated with the api so try authenticating and then do the http post request
                # but only do it once
                await self.authenticate_api()
                await self.get_flights(request, True)

            else:
                return response.json()
                
        except Exception as e:
            raise Exception(e)
        
    def convert_flight_offer_dto_to_domain(self, dtos: List[FlightOfferDTO]) -> List[FlightOffer]:
        return [
            FlightOffer(
                id=dto.id,
                number_of_bookable_seats=dto.number_of_bookable_seats,
                source=dto.source,
                itineraries=[Itinerary(**itinerary.model_dump()) for itinerary in dto.itineraries],
                price=Price(**dto.price.model_dump()),
                pricing_options=PricingOptions(**dto.pricing_options.model_dump()),
                travel_pricings=[TravelerPricingSummary(**tp.model_dump()) for tp in dto.travel_pricings],
                validation_airline_codes=dto.validation_airline_codes,
                score=None  # Set score explicitly
            )
            for dto in dtos
        ]
