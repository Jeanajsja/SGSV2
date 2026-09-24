import os

from flask import Flask, Response, request

from shared.service_client import ServiceClient
from shared.service_registry import MONOLITH_URL, resolve_target_base_url

app = Flask(__name__)

CORS_ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:8080,http://127.0.0.1:8080").split(",") if origin.strip()]


@app.after_request
def add_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    origin = request.headers.get("Origin")
    if origin in CORS_ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy(path):
    if request.method == 'OPTIONS':
        return Response(status=204)

    target_base_url = resolve_target_base_url(path)

    if not target_base_url:
        return {"error": "Servicio no encontrado"}, 404

    domain = path.split('/')[0]
    client = ServiceClient(domain, timeout=10) if domain in {"login", "usuarios", "roles", "salones", "docentes", "reservas"} else ServiceClient("monolith", timeout=10)
    try:
        resp = client.proxy_request(request, path=path)
        return Response(resp.content, resp.status_code, resp.headers.items())
    except Exception as exc:
        return {"error": f"No se pudo conectar al servicio en {target_base_url}: {exc}"}, 503


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)
