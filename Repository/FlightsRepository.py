from typing import List

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException

from app.Models.Domain.FlightSearchResponse import FlightOffer
from app.Repository.IFlightsRepository import IFlightsRepository


class FlightRepository(IFlightsRepository):
    """This class contains the functinoality related to the chosen database. This class will handle connection,
    reading, updating and writing to the database. 

    Args:
        IFlightsRepository (IFlightRepository): Abstract class to define the interface for the FlightRepository class

    """
    def __init__(self, connection_string: str, database_name: str):

        self.client = AsyncIOMotorClient(connection_string)
        self.database = self.client.get_database(database_name)
        self.amadeus_collection = self.database.get_collection("AmadeusToken")
                
    async def get_token(self):
        item =  await self.amadeus_collection.find_one()
        
        if item and "token" in item:
            return item["token"]
        raise Exception("There is something wrong in the AmadeusToken collection")
    
    async def update_token(self, new_token: str):
        try:
            result = await self.amadeus_collection.update_one({}, {"$set": {"token": new_token}})
            
            if result.matched_count == 0:
                raise Exception("No document found to update.")
        except Exception as e:
            raise Exception(f"Failed to updated token: {e}")
            
    async def update_collection(self, flights: List[FlightOffer], collection_name: str) -> dict:
        if len(flights) == 0:
            raise Exception("No documents to update the db with")
        
        documents = [flight.model_dump() for flight in flights]
        collection = self.database.get_collection(collection_name)
        try:
            await collection.delete_many({})
            insert_result = await collection.insert_many(documents)

            return {
                "message": "Database updated successfully",
                "inserted_count": len(insert_result.inserted_ids),
                "inserted_ids": [str(_id) for _id in insert_result.inserted_ids]
            }
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database update failed: {str(e)}")
        
    async def get_collections(self) -> List[str]:
        collectionNames = await self.database.list_collection_names()

        return collectionNames
    
    async def get_all_flights_deserialized(self, collection_name: str) -> List[FlightOffer]:
        collection = self.database.get_collection(collection_name)
        flights = await collection.find({}).to_list()

        if not flights:
            return []
        
        print(flights[0])

        return [FlightOffer(
            id=flight["_id"],
            number_of_bookable_seats=flight["number_of_bookable_seats"],
            source=flight["source"],
            itineraries=flight["itinenaries"],
            price=flight["price"],
            pricing_options=flight["pricing_options"],
            travel_pricings=flight["travel_pricings"],
            validation_airline_codes=flight["validation_airline_codes"]) 

            for flight in flights
        ]
        
    async def create_new_collection(self, collection_name: str) -> List[str]:
        """
            Create a new collection with the name as an input from the front end
        Args:
            collection_name (str): name of collection to create

        Returns:
            List[str]: return a list of the collection names in the database
        """
        await self.database.create_collection(collection_name)

        return self.database.list_collection_names()
                