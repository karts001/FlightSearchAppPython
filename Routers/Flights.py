import os

from fastapi import APIRouter
from dotenv import load_dotenv
from typing import List

from app.Models.Domain.FlightSearchRequest import FlightSearchRequest
from app.Models.Domain.FlightSearchResponse import FlightOffer
from app.Repository.FlightsRepository import FlightRepository
from app.Services.Amadeus import Amadeus
from app.Services.TokenService import TokenService
from app.Utilities.Calculations import calculate_score
from app.Utilities.Conversions import Conversions

load_dotenv()

flights = APIRouter(prefix="/api/flight", tags=["flight"])

# set up mongodb connection
flight_repository = FlightRepository(
    os.environ.get("MONGODB_CONNECTION_STRING"),
    os.environ.get("DATABASE_NAME")
)

# set up services
token_service = TokenService(db=flight_repository)
_amadeus_service = Amadeus(token_service)
_converter = Conversions()

@flights.get("/collections")
async def get_collections():
    return await flight_repository.get_collections()

@flights.post("/collections")
async def create_new_collection():
    return await flight_repository.create_new_collection()

@flights.post("/search")
async def search(flight_search_request: FlightSearchRequest) -> List[FlightOffer]:
    flights = await _amadeus_service.get_flights(flight_search_request)
 
    return flights

@flights.post("/compare")
async def compare(flights: List[FlightOffer], collection_name: str = "") -> List[FlightOffer]:
    db_flights = await flight_repository.get_all_flights_deserialized(collection_name)

    if db_flights == None:
        db_flights = []

    # combine db flights and search flights
    combined_flights: List[FlightOffer] = db_flights + flights

    for flight in combined_flights:
        price = flight.price.grand_total
        duration = flight.itineraries[0].duration
        flight.score = calculate_score(price_weighting=0.5, converter=_converter, price=price, duration=duration)

    # return the top 5 results
    return sorted(combined_flights, key=lambda x: x.score, reverse=True)[:5]

@flights.post("/save")
async def save(flights: List[FlightOffer], collection_name: str = "") -> dict:
    flights = await flight_repository.update_collection(flights, collection_name)

    return flights
