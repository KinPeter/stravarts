from datetime import datetime
from fastapi import HTTPException, Query, status


def validate_before_after(
    after: datetime | None = Query(
        None,
        description="Filter activities after this date - ISO 8601 format, e.g., '2023-10-01T00:00:00Z'; Requires 'before' to be set.",
    ),
    before: datetime | None = Query(
        None,
        description="Filter activities before this date - ISO 8601 format, e.g., '2023-10-01T00:00:00Z'; Requires 'after' to be set.",
    ),
):
    """
    Validate that both 'before' and 'after' parameters are provided together,
    or neither. If one is provided without the other, raise an HTTP 422 error.
    """

    if (before is not None) != (after is not None):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Both 'before' and 'after' must be provided together, or neither.",
        )
    return {"before": before, "after": after}
