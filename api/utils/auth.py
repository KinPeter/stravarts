from fastapi import HTTPException, Header, Request, status

from api.types.common import AsyncDatabase


async def auth_user(
    request: Request,
    api_key: str = Header(..., alias="X-Api-Key"),
    strava_token: str = Header(..., alias="X-Strava-Token"),
):
    db: AsyncDatabase = request.app.state.db

    if not api_key or not strava_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication data. `X-Api-Key` and `X-Strava-Token` are required in the headers.",
        )

    # FIXME: Replace with actual user authentication logic
    user = await db.get_collection("users").find_one({"email": "alice@example.com"})
    return user
