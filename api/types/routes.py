from enum import Enum
from api.types.common import PkBaseModel


class ActivityType(str, Enum):
    WALK = "Walk"
    RUN = "Run"
    RIDE = "Ride"


class SyncResponse(PkBaseModel):
    routes_synced: int
    total_routes: int


class Heatmap(PkBaseModel):
    points: dict = {}


class RoutesResponse(PkBaseModel):
    heatmap: Heatmap | None = None
    after: str | None = None
    before: str | None = None
    types: list[ActivityType]
    activity_count: int
