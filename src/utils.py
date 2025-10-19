import json
from workers import Response

def json_response(data: dict, status: int = 200, cors: bool = True) -> Response:
    headers = {"Content-Type": "application/json"}
    if cors:
        headers.update({
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
        })
    return Response(json.dumps(data), headers=headers, status=status)

async def parse_json(request) -> dict:
    if request.method == "OPTIONS":
        return {}
    try:
        payload = await request.json()
        if hasattr(payload, "to_py"):
            payload = payload.to_py()
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}

def required(fields: dict, *names: str) -> tuple[bool, str | None]:
    missing = [n for n in names if not (str(fields.get(n, "")).strip())]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    return True, None

def html_response(html: str, status: int = 200) -> Response:
    return Response(html, headers={"Content-Type": "text/html; charset=utf-8"}, status=status)

def get_client_ip(request) -> str:
    headers = request.headers
    for k in ("CF-Connecting-IP", "True-Client-IP", "X-Forwarded-For"):
        v = headers.get(k)
        if v:
            return v.split(",")[0].strip()
    return ""

async def rate_limit(env, key: str, window_seconds: int, max_requests: int):
    kv = env.COACHING_KV
    now_key = f"rl:{key}"
    val = await kv.get(now_key)
    count = int(val) if val else 0
    if count >= max_requests:
        return False, count
    count += 1
    if val is None:
        await kv.put(now_key, str(count), expiration_ttl=window_seconds)
    else:
        await kv.put(now_key, str(count))
    return True, count
