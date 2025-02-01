from typing import List

from motor.motor_asyncio import AsyncIOMotorClient

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
            
    async def update_collection(self, documents: List[dict], collection_name: str):
        if len(documents) == 0:
            raise Exception("No documents to update the db with")
        
        collection = self.database.get_collection(collection_name)
        await collection.delete_many({})
        await collection.update_many(documents)

    async def get_collections(self) -> List[str]:
        collectionNames = await self.database.list_collection_names()
        print(collectionNames)
        return collectionNames
    
    async def get_all_flights_deserialized():
        pass

    async def create_new_collection():
        pass
                