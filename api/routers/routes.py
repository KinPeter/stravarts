from fastapi import APIRouter, Depends, Request, status

from api.types.routes import SyncResponse
from api.utils.auth import auth_user

router = APIRouter(
    prefix="/routes",
    tags=["routes"],
)


@router.post(
    "/sync",
    summary="Trigger a sync of activities from Strava",
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {"example": {"detail": "Invalid API key."}}
            },
        },
    },
)
async def post_sync_routes(req: Request, user=Depends(auth_user)) -> SyncResponse:
    db = req.app.state.db
    # FIXME: Implement the actual route synchronization logic here
    print(f"User: {user}, Database: {db}")

    return SyncResponse(
        routes_synced=0,
        total_routes=0,
    )
