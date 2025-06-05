from fastapi import HTTPException
from api.types.auth import RegistrationRequest, RegistrationResponse
from api.types.common import AsyncDatabase


async def register_user(
    db: AsyncDatabase, data: RegistrationRequest
) -> RegistrationResponse:
    users_collection = db.get_collection("users")
    existing_user = await users_collection.find_one({"email": data.email})

    if existing_user:
        raise HTTPException(
            status_code=401,
            detail="Email already registered",
        )

    # FIXME: Add logic to hash the password and store it securely
    return RegistrationResponse(
        id=str(data.username),  # Assuming username is unique and used as ID
        api_key="generated_api_key",  # Replace with actual API key generation logic
    )
