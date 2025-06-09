from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request, status

from api.modules.routes import get_routes, sync_routes
from api.types.auth import User
from api.types.routes import ActivityType, RoutesResponse, SyncResponse
from api.utils.auth import auth_user
from api.utils.query_validators import validate_before_after

router = APIRouter(
    prefix="/routes",
    tags=["routes"],
)


@router.get(
    "",
    summary="Get routes map coordinates for the authenticated user",
    description="This endpoint retrieves the routes map coordinates for the authenticated user. You can filter the results by date range and activity type.",
    responses={
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {"example": {"detail": "Invalid API key."}}
            },
        },
    },
)
async def get_get_routes(
    req: Request,
    user: Annotated[User, Depends(auth_user)],
    after: Annotated[
        datetime | None,
        Query(
            description="Filter activities after this date - ISO 8601 format, e.g., '2023-10-01T00:00:00Z'",
        ),
    ] = None,
    before: Annotated[
        datetime | None,
        Query(
            description="Filter activities before this date - ISO 8601 format, e.g., '2023-10-01T00:00:00Z'",
        ),
    ] = None,
    types: Annotated[
        list[ActivityType] | None,
        Query(
            description="Filter activities by type ('Walk', 'Run', 'Ride'). If not provided, all types are included.",
        ),
    ] = None,
) -> RoutesResponse:
    return await get_routes(
        db=req.app.state.db, user=user, before=before, after=after, types=types
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
    user: Annotated[User, Depends(auth_user)],
    params: Annotated[dict[str, datetime | None], Depends(validate_before_after)],
) -> SyncResponse:
    return await sync_routes(req.app.state.db, user, **params)
