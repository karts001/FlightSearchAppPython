from abc import ABC, abstractmethod
from typing import List

from app.Models.Domain.FlightSearchResponse import FlightOffer

class IAmadeus(ABC):

    @abstractmethod
    def authenticate_api() -> str:
        pass

    @abstractmethod
    def get_flights() -> List[FlightOffer]:
        pass
