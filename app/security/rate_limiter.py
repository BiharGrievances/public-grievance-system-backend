import time
from fastapi import HTTPException, Request

# =====================================
# SIMPLE IN-MEMORY RATE LIMITER (FREE)
# =====================================
# ✔ No Redis
# ✔ No paid services
# ✔ Good for India MVP
# ⚠ Resets on server restart (acceptable)
# =====================================

REQUESTS_PUBLIC = {}
REQUESTS_ADMIN = {}

# Limits
PUBLIC_LIMIT = 5        # login attempts
ADMIN_LIMIT = 60        # admin API calls

TIME_WINDOW = 60        # seconds


def _clean_old_requests(store: dict, ip: str, now: float):
    store[ip] = [t for t in store[ip] if now - t < TIME_WINDOW]


# -------------------------------------
# PUBLIC RATE LIMIT (AUTH / LOGIN)
# -------------------------------------
def rate_limit(request: Request):
    client_ip = request.client.host
    now = time.time()

    if client_ip not in REQUESTS_PUBLIC:
        REQUESTS_PUBLIC[client_ip] = []

    _clean_old_requests(REQUESTS_PUBLIC, client_ip, now)

    if len(REQUESTS_PUBLIC[client_ip]) >= PUBLIC_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts. Please wait."
        )

    REQUESTS_PUBLIC[client_ip].append(now)


# -------------------------------------
# ADMIN RATE LIMIT (DASHBOARD / APIs)
# -------------------------------------
def rate_limit_admin(request: Request):
    client_ip = request.client.host
    now = time.time()

    if client_ip not in REQUESTS_ADMIN:
        REQUESTS_ADMIN[client_ip] = []

    _clean_old_requests(REQUESTS_ADMIN, client_ip, now)

    if len(REQUESTS_ADMIN[client_ip]) >= ADMIN_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many admin requests. Slow down."
        )

    REQUESTS_ADMIN[client_ip].append(now)
