from fastapi import FastAPI

from app.Routers.Flights import flight_router


app = FastAPI()
app.include_router(flight_router)

@app.get("/")
async def root():
    return {"message": "Test landing page"}
