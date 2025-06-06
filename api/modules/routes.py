import uuid
from datetime import datetime, timezone
from fastapi import HTTPException, status
from api.types.auth import User
from api.types.common import AsyncDatabase
from api.types.routes import SyncResponse
from api.utils.db import DbCollection
from api.utils.logger import get_logger
from api.utils.strava_api import StravaApi


async def sync_routes(
    db: AsyncDatabase, user: User, before: datetime | None, after: datetime | None
) -> SyncResponse:
    logger = get_logger()
    strava = StravaApi(user.strava_token)
    activities_collection = db.get_collection(DbCollection.ACTIVITIES)
    sync_meta_collection = db.get_collection(DbCollection.SYNC_METADATA)

    user_sync_data = await sync_meta_collection.find_one({"user_id": user.id})
    if not user_sync_data:
        logger.info(
            f"No sync metadata found for user {user.username}, creating new entry."
        )
        user_sync_data = {"user_id": user.id, "synced_ids": [], "last_synced": None}
        await sync_meta_collection.insert_one(user_sync_data)

    logger.info(f"Syncing routes for user: {user.username} ({user.id})")
    try:
        athlete = await strava.get_athlete()
        logger.info(
            f"Authenticated as athlete: {athlete['username']} ({athlete['id']})"
        )

        if before is not None and after is not None:
            before_ts = int(before.timestamp())
            after_ts = int(after.timestamp())
            logger.info(
                f"Fetching activities between {after} and {before} (timestamps: {after_ts}, {before_ts})"
            )
            activities = await strava.get_all_activities(
                after=after_ts, before=before_ts
            )
        elif user_sync_data["last_synced"] is not None:
            dt = datetime.fromisoformat(
                user_sync_data["last_synced"].replace("Z", "+00:00")
            )
            epoch_ts = int(dt.timestamp())
            activities = await strava.get_all_activities(after=epoch_ts)
        else:
            logger.info("No last synced time found, fetching all activities.")
            activities = await strava.get_all_activities()

        logger.info(f"Fetched {len(activities)} activities for athlete {athlete['id']}")

        if not activities:
            logger.info("No activities found to sync.")
            saved_count = await activities_collection.count_documents(
                {"user_id": user.id}
            )
            return SyncResponse(
                routes_synced=0,
                total_routes=saved_count,
            )

        already_synced = set(user_sync_data["synced_ids"])
        just_synced_count = 0

        for activity in activities:
            strava_id = activity["id"]

            if strava_id in already_synced:
                logger.info(f"Activity {strava_id} already synced, skipping.")
                continue

            if activity["type"] not in ["Walk", "Run", "Ride"]:
                logger.info(
                    f"Activity {strava_id} is of type {activity['type']}, skipping."
                )
                continue

            stream_response = await strava.get_activity_latlng_stream(
                activity_id=strava_id
            )

            if (
                not stream_response
                or "latlng" not in stream_response
                or not stream_response["latlng"]["data"]
            ):
                logger.info(
                    f"No lat/lng stream found for activity {strava_id}, skipping."
                )
                continue

            latlng_data = stream_response["latlng"]["data"]
            logger.info(
                f"Activity {strava_id} has lat/lng data with length: {len(latlng_data)}, syncing..."
            )

            activity_with_route = {
                "id": str(uuid.uuid4()),
                "strava_id": strava_id,
                "user_id": user.id,
                "name": activity.get("name", "Unnamed Activity"),
                "start_date": activity["start_date"],
                "distance": activity["distance"],
                "type": activity["type"],
                "route": latlng_data,
            }
            await activities_collection.insert_one(activity_with_route)

            user_sync_data["synced_ids"].append(strava_id)
            user_sync_data["last_synced"] = datetime.now(timezone.utc).isoformat()
            await sync_meta_collection.update_one(
                {"user_id": user.id},
                {"$set": user_sync_data},
            )
            just_synced_count += 1
            logger.info(f"Synced activity {strava_id} for user {user.username}")

        logger.info(
            f"Successfully synced {just_synced_count} activities for user {user.username}"
            if just_synced_count > 0
            else "No new activities were synced."
        )
        return SyncResponse(
            routes_synced=just_synced_count,
            total_routes=len(user_sync_data["synced_ids"]),
        )

    except Exception as e:
        logger.error(f"Error syncing routes for user {user.username}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: Could not sync routes from Strava. - {str(e)}",
        )
