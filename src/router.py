from workers import Response
from site_html import page
from utils import json_response, parse_json, required, get_client_ip, rate_limit

class Router:
    def __init__(self, env):
        self.env = env

    async def handle(self, request, ctx):
        url = request.url
        method = request.method

        if method == "OPTIONS":
            return json_response({"ok": True})

        if method == "GET":
            if url.endswith("/") or url.endswith("/index.html"):
                return page(self.env, "index")
            if url.endswith("/services") or url.endswith("/services.html"):
                return page(self.env, "services")
            if url.endswith("/about") or url.endswith("/about.html"):
                return page(self.env, "about")
            if url.endswith("/contact") or url.endswith("/contact.html"):
                return page(self.env, "contact")
            if url.endswith("/intake") or url.endswith("/intake.html"):
                return page(self.env, "intake")
            if url.endswith("/privacy") or url.endswith("/privacy.html"):
                return page(self.env, "privacy")
            if url.endswith("/terms") or url.endswith("/terms.html"):
                return page(self.env, "terms")

        if method == "POST":
            ip = get_client_ip(request) or "unknown"
            window = int(getattr(self.env, "RATE_LIMIT_WINDOW_SECONDS", "600"))
            max_req = int(getattr(self.env, "RATE_LIMIT_MAX_REQUESTS", "10"))
            ok, _ = await rate_limit(self.env, f"{ip}", window, max_req)
            if not ok:
                return json_response({"ok": False, "error": "Rate limit exceeded. Try later."}, 429)

            if url.endswith("/api/contact"):
                return await self.api_contact(request, ip)
            if url.endswith("/api/intake"):
                return await self.api_intake(request, ip)
            if url.endswith("/api/newsletter"):
                return await self.api_newsletter(request)

        return Response("Not found", status=404)

    async def _honeypot(self, data: dict) -> bool:
        return bool(data.get("website", "").strip())

    async def api_contact(self, request, ip):
        data = await parse_json(request)
        if await self._honeypot(data):
            return json_response({"ok": True, "message": "Thanks!"})
        ok, msg = required(data, "name", "email", "message")
        if not ok:
            return json_response({"ok": False, "error": msg}, 400)

        db = self.env.COACHING_DB
        stmt = db.prepare(
            "INSERT INTO leads (name, email, message, created_at, ip) "
            "VALUES (?1, ?2, ?3, datetime('now'), ?4)"
        ).bind(data["name"], data["email"], data["message"], ip)
        await stmt.run()

        return json_response({"ok": True, "message": "Thanks—I'll get back to you shortly."})


    async def api_intake(self, request, ip):
        data = await parse_json(request)
        if await self._honeypot(data):
            return json_response({"ok": True, "message": "Received."})
        ok, msg = required(data, "full_name", "email", "goal", "timeline")
        if not ok:
            return json_response({"ok": False, "error": msg}, 400)

        db = self.env.COACHING_DB
        stmt = db.prepare(
            "INSERT INTO intakes (full_name, email, goal, timeline, details, created_at, ip) "
            "VALUES (?1, ?2, ?3, ?4, ?5, datetime('now'), ?6)"
        ).bind(
            data["full_name"], data["email"], data["goal"], data["timeline"],
            data.get("details", ""), ip
        )
        await stmt.run()

        return json_response({"ok": True, "message": "Intake submitted. I’ll follow up with next steps."})

    async def api_newsletter(self, request):
        data = await parse_json(request)
        if await self._honeypot(data):
            return json_response({"ok": True, "message": "You're on the list!"})
        ok, msg = required(data, "email")
        if not ok:
            return json_response({"ok": False, "error": msg}, 400)

        kv = self.env.COACHING_KV
        await kv.put(f"newsletter:{data['email'].lower()}", "1")
        return json_response({"ok": True, "message": "You're on the list!"})
