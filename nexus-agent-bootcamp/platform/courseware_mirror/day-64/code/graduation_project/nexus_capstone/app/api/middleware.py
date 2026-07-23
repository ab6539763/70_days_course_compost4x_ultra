"""Day 62 — 请求中间件：日志、限流、鉴权"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestLogMiddleware(BaseHTTPMiddleware):
    """记录每个请求的耗时与状态码"""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"[{request.method}] {request.url.path} -> {response.status_code} ({elapsed_ms:.1f}ms)")
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """简易令牌桶限流（教学演示）"""
    _counter: dict[str, int] = {}
    LIMIT = 100  # 每 IP 每分钟

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        self._counter[client_ip] = self._counter.get(client_ip, 0) + 1
        if self._counter[client_ip] > self.LIMIT:
            from starlette.responses import JSONResponse
            return JSONResponse({"detail": "请求过于频繁"}, status_code=429)
        return await call_next(request)
