import uuid
from fastapi import HTTPException, status
from api.types.auth import RegistrationRequest, RegistrationResponse
from api.types.common import AsyncDatabase
from api.utils.auth import generate_alphanumeric_key, hash_api_key
from api.utils.db import DbCollection
from api.utils.logger import get_logger


async def register_user(
    db: AsyncDatabase, data: RegistrationRequest
) -> RegistrationResponse:
    logger = get_logger()
    users_collection = db.get_collection(DbCollection.USERS)
    existing_user = await users_collection.find_one({"email": data.email})

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    logger.info(f"Registering new user: {data.username} <{data.email}>")

    user_id = str(uuid.uuid4())
    api_key = generate_alphanumeric_key()

    try:
        api_key_hash = hash_api_key(api_key)
    except Exception as e:
        logger.error(f"Error hashing API key for user {data.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error: Could not handle the API Key.",
        )

    await users_collection.insert_one(
        {
            "id": user_id,
            "username": data.username,
            "email": data.email,
            "api_key_hash": api_key_hash,
        }
    )

    logger.info(f"User registered successfully: {data.email} with API key {api_key}")

    return RegistrationResponse(
        id=user_id,
        api_key=api_key,
    )
