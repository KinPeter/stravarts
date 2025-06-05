from fastapi import APIRouter, Depends, Request, status

from api.types.routes import SyncResponse
from api.utils.auth import auth_user

router = APIRouter(
    prefix="/routes",
    tags=["routes"],
)


@router.post("/sync", status_code=status.HTTP_201_CREATED)
async def post_sync_routes(req: Request, user=Depends(auth_user)) -> SyncResponse:
    db = req.app.state.db
    # FIXME: Implement the actual route synchronization logic here
    print(f"User: {user}, Database: {db}")

    return SyncResponse(
        routes_synced=0,
        total_routes=0,
    )
