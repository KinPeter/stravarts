from enum import Enum
from api.types.common import PkBaseModel


class ActivityType(str, Enum):
    WALK = "Walk"
    RUN = "Run"
    RIDE = "Ride"


class SyncResponse(PkBaseModel):
    routes_synced: int
    total_routes: int


Coords = tuple[float, float]  # (latitude, longitude)


class Routemap(PkBaseModel):
    count: int = 0
    points: set[Coords] = set()


class RoutesResponse(PkBaseModel):
    routemap: Routemap | None = None
    after: str | None = None
    before: str | None = None
    types: list[ActivityType]
    activity_count: int


class RouteResource:
    id: str
    strava_id: int
    user_id: str
    name: str
    start_date: str  # ISO 8601 format
    distance: float  # Distance in meters
    type: ActivityType
    route: list[list[float]]  # List of (latitude, longitude) tuples as arrays
