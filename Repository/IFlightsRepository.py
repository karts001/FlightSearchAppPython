from abc import ABC, abstractmethod
from typing import List

class IFlightsRepository(ABC):
    @abstractmethod
    def get_token() -> str:
        pass

    @abstractmethod
    async def update_token(token: str):
        pass

    @abstractmethod
    async def create_new_collection():
        pass

    @abstractmethod
    async def update_collection(documents: List[dict], collection_name: str):
        pass

    @abstractmethod
    async def get_all_flights_deserialized():
        pass

    @abstractmethod
    async def get_collections():
        pass
