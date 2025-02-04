from fastapi import FastAPI

from app.Routers.Flights import flights


app = FastAPI()
app.include_router(flights)

@app.get("/")
async def root():
    return {"message": "Test landing page"}
