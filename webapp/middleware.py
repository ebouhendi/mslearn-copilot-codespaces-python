import time
from collections import deque
from threading import Lock

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware keyed by client IP.

    Not suitable for multi-process deployments or production use without a shared store.
    """

    def __init__(self, app, max_requests: int = 10, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests: dict[str, deque] = {}
        self.lock = Lock()

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        with self.lock:
            q = self.requests.get(client_ip)
            if q is None:
                q = deque()
                self.requests[client_ip] = q

            # prune timestamps outside the window
            while q and q[0] <= now - self.window:
                q.popleft()

            if len(q) >= self.max_requests:
                return JSONResponse(
                    status_code=429,
                    content={"error": "Rate limit exceeded. Try again later."},
                )

            q.append(now)

        response = await call_next(request)
        return response
