import time
from fastapi import HTTPException, status

# In-memory store (OK for free tier)
_RATE_LIMIT_STORE = {}

def rate_limit(key: str, limit: int = 5, window: int = 60):
    """
    Generic rate limiter

    key: unique identifier (ip, user, endpoint)
    limit: max requests
    window: time window in seconds
    """

    now = time.time()

    # Initialize bucket
    if key not in _RATE_LIMIT_STORE:
        _RATE_LIMIT_STORE[key] = []

    # Remove expired timestamps
    _RATE_LIMIT_STORE[key] = [
        t for t in _RATE_LIMIT_STORE[key]
        if now - t < window
    ]

    # Check limit
    if len(_RATE_LIMIT_STORE[key]) >= limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later."
        )

    # Record request
    _RATE_LIMIT_STORE[key].append(now)


def rate_limit_admin(key: str):
    """
    Stricter admin limiter
    """
    rate_limit(key, limit=20, window=60)
