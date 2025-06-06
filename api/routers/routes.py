from fastapi import APIRouter, Depends, Request, status

from api.modules.routes import sync_routes
from api.types.routes import SyncResponse
from api.utils.auth import auth_user
from api.utils.query_validators import validate_before_after

router = APIRouter(
    prefix="/routes",
    tags=["routes"],
)


@router.post(
    "/sync",
    summary="Trigger a sync of activities from Strava",
    description="This endpoint triggers a synchronization of activities from Strava for the authenticated user. By default it will sync all activities after the last synced time. You can specify 'before' and 'after' parameters to filter activities within a specific date range. NOTE! There is a rate limit on the Strava API so for the initial sync it is recommended to use the 'before' and 'after' parameters to limit the number of activities fetched to be around 50 and wait 15 minutes between the attempts.",
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
async def post_sync_routes(
    req: Request,
    user=Depends(auth_user),
    params=Depends(validate_before_after),
) -> SyncResponse:
    return await sync_routes(req.app.state.db, user, **params)
