from pydantic import EmailStr, Field
from api.types.common import PkBaseModel


class RegistrationRequest(PkBaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr


class RegistrationResponse(PkBaseModel):
    id: str
    api_key: str


class UserResource(PkBaseModel):
    id: str
    username: str
    email: str
    api_key_hash: str


class User(UserResource):
    strava_token: str
