import math
from typing import cast

from api.types.routes import Coords, Routemap
from api.utils.logger import get_logger


def generate_routemap(activities: list[dict], sampling_rate: int = 5) -> Routemap:
    """
    Generate a route map based on activity data.
    This function takes a list of activities, extracts route coordinates,
    and clusters them.

    ### Adjust this parameters to control clustering sensitivity and performance.
    - `sampling_rate`: How often to sample points from the route (e.g., every 5th point). Default is 5.
    """
    logger = get_logger()

    points: set[Coords] = set()
    activity_count = len(activities)

    for index, activity in enumerate(activities):
        route = activity["route"]
        if not route:
            continue

        logger.info(
            f"Processing activity {index+1}/{activity_count} {activity['strava_id']} with {len(route)} coordinates."
        )

        points_before = len(points)
        for entry in route[1::sampling_rate]:
            # Round coordinates to 4 decimal places for better clustering (approx. 11m precision)
            coords: Coords = (
                round(entry[0], 4),
                round(entry[1], 4),
            )
            points.add(coords)

        points_after = len(points)
        logger.info(
            f"Added {points_after - points_before} unique points from activity."
        )

    logger.info(f"Generated routemap with {len(points)} unique points.")

    return Routemap(points=points, count=len(points))


def approx_distance(coord1: tuple[float, float], coord2: tuple[float, float]) -> float:
    """
    Approximate distance in degrees between two (lat, lon) points using Euclidean distance.
    Good enough for small distances and much faster than haversine.
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5


def haversine(coord1: tuple[float, float], coord2: tuple[float, float]) -> float:
    """
    Calculate the great-circle distance between two points (lat, lon) in meters.
    """
    R = 6371000  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
