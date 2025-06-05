from fastapi import APIRouter, Request, status

from api.modules.auth import register_user
from api.types.auth import RegistrationRequest, RegistrationResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def post_register_user(
    body: RegistrationRequest, req: Request
) -> RegistrationResponse:
    return await register_user(req.app.state.db, body)
