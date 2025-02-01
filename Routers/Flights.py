import os

from fastapi import APIRouter
from dotenv import load_dotenv

from app.Models.Domain.FlightSearchRequest import FlightSearchRequest
from app.Repository.FlightsRepository import FlightRepository
from app.Services.Amadeus import Amadeus
from app.Services.TokenService import TokenService

load_dotenv()

flight_router = APIRouter(prefix="/api/flight", tags=["flight"])

flight_repository = FlightRepository(
    os.environ.get("MONGODB_CONNECTION_STRING"),
    os.environ.get("DATABASE_NAME")
)

token_service = TokenService(db=flight_repository)

_amadeus_service = Amadeus(token_service)

@flight_router.get("/collections")
async def getAllCollections():
    return await flight_repository.get_collections()


@flight_router.post("/search")
async def search(flight_search_request: dict):
    flights = await _amadeus_service.get_flights(flight_search_request)

    return flights