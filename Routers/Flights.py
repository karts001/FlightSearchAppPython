import os

from fastapi import APIRouter
from dotenv import load_dotenv
from typing import List
from itertools import islice

from app.Models.Domain.FlightSearchRequest import FlightSearchRequest
from app.Models.Domain.FlightSearchResponse import FlightOffer
from app.Repository.FlightsRepository import FlightRepository
from app.Services.Amadeus import Amadeus
from app.Services.TokenService import TokenService

load_dotenv()

flights = APIRouter(prefix="/api/flight", tags=["flight"])

flight_repository = FlightRepository(
    os.environ.get("MONGODB_CONNECTION_STRING"),
    os.environ.get("DATABASE_NAME")
)

token_service = TokenService(db=flight_repository)

_amadeus_service = Amadeus(token_service)

@flights.get("/collections")
async def getAllCollections():
    return await flight_repository.get_collections()

@flights.post("/search")
async def search(flight_search_request: FlightSearchRequest) -> List[FlightOffer]:
    flights = await _amadeus_service.get_flights(flight_search_request)

    return flights

@flights.post("/compare")
async def compare(flights: List[FlightOffer], collection_name: str = "") -> List[FlightOffer]:
    db_flights = await flight_repository.get_all_flights_deserialized(collection_name)

    return _rank_flights(flights, db_flights)


def _rank_flights(search_flights: List[FlightOffer], db_flights: List[FlightOffer]) -> List[FlightOffer]:
    all_flights = search_flights + db_flights

    # sort the combined list by score attribute and return the top 5 flight offers
    return islice(all_flights.sort(key =lambda x: x.score, reverse=True), 5)
    