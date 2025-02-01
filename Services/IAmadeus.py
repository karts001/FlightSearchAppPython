from abc import ABC, abstractmethod
from typing import List

class IAmadeus(ABC):

    @abstractmethod
    def authenticate_api() -> str:
        pass

    @abstractmethod
    def get_flights() -> List[dict]:
        pass



