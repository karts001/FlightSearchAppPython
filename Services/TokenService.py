import motor

from app.Repository.IFlightsRepository import IFlightsRepository


class TokenService:
    def __init__(self, db: IFlightsRepository):
        self._db = db
    
    def get_token(self):
        return self._db.get_token()
    
    def update_token(self, token: str):
        return self._db.update_token(token)