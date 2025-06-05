from api.types.common import PkBaseModel


class SyncResponse(PkBaseModel):
    routes_synced: int
    total_routes: int
