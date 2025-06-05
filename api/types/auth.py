from api.types.common import PkBaseModel


class RegistrationRequest(PkBaseModel):
    username: str
    email: str


class RegistrationResponse(PkBaseModel):
    id: str
    api_key: str
