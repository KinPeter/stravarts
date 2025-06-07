import string
import secrets
import hashlib
import os
from fastapi import HTTPException, Header, Request, Security, status
from fastapi.security import APIKeyHeader

from api.types.auth import User
from api.types.common import AsyncDatabase
from api.utils.db import DbCollection
from api.utils.logger import get_logger

api_key_header = APIKeyHeader(name="X-Api-Key", scheme_name="API Key", auto_error=True)


async def auth_user(
    request: Request,
    api_key: str = Security(api_key_header),
    strava_token: str = Header(
        ..., alias="X-Strava-Token", description="Strava access token for the user"
    ),
) -> User:
    db: AsyncDatabase = request.app.state.db
    logger = get_logger()

    if not api_key or not strava_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication data. `X-Api-Key` and `X-Strava-Token` are required in the headers.",
        )

    try:
        api_key_hash = hash_api_key(api_key)
    except Exception as e:
        logger.error(f"Error hashing API key {api_key}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error: Could not handle the API Key.",
        )

    user = await db.get_collection(DbCollection.USERS).find_one(
        {"api_key_hash": api_key_hash}
    )
    if not user:
        logger.warning(f"Unauthorized access attempt with API key: {api_key}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )

    return User(
        **user,
        strava_token=strava_token,
    )


def generate_alphanumeric_key(length=32):
    alphabet = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return "".join(secrets.choice(alphabet) for _ in range(length))


def hash_api_key(api_key: str) -> str:
    """
    Hash the API key using SHA-256 with a secret salt.
    """

    salt = os.getenv("API_SECRET")
    if not salt:
        raise ValueError("API_SECRET environment variable is not set.")

    hash_obj = hashlib.sha256()
    hash_obj.update((api_key + salt).encode("utf-8"))
    return hash_obj.hexdigest()
