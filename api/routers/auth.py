from fastapi import APIRouter, Request, status

from api.modules.auth import register_user
from api.types.auth import RegistrationRequest, RegistrationResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/register",
    summary="Register a new user to get an API key",
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {
            "description": "Email already registered",
            "content": {
                "application/json": {"example": {"detail": "Email already registered"}}
            },
        },
    },
)
async def post_register_user(
    body: RegistrationRequest, req: Request
) -> RegistrationResponse:
    return await register_user(req.app.state.db, body)
