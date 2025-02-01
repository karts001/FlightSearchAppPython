from pydantic import BaseModel


class AmadeusAuthResponseDTO(BaseModel):
    auth_response: str
    username: str
    application_name: str
    client_id: str
    token_type: str
    access_token: str
    expires_in: int
    state: str
    scope: str
