import logging
from django.db import connection
from django.http import JsonResponse
from django.core.cache import cache

logger = logging.getLogger("apps")
def health_check(request):
    logger.info("Health check called")
    health = {
        "status": "ok",
        "database": "ok",
        "redis": "ok",
    }

    # Check PostgreSQL
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        health["database"] = "error"
        health["status"] = "error"

    # Check Redis
    try:
        cache.set("health_check", "ok", timeout=10)
        if cache.get("health_check") != "ok":
            raise Exception("Redis returned an unexpected value")
    except Exception:
        health["redis"] = "error"
        health["status"] = "error"

    status_code = 200 if health["status"] == "ok" else 503

    return JsonResponse(health, status=status_code)