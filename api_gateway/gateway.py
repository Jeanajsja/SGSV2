import os

import requests
from flask import Flask, Response, request

app = Flask(__name__)

MONOLITH_URL = os.getenv("MONOLITH_URL", "http://monolito:5000/api")
MICROSERVICES = {
    "login": os.getenv("LOGIN_URL", "http://login:5001/api"),
    "usuarios": os.getenv("USUARIOS_URL", "http://usuarios:5005/api"),
    "roles": os.getenv("ROLES_URL", "http://roles:5004/api"),
    "salones": os.getenv("SALONES_URL", "http://salones:5002/api"),
    "docentes": os.getenv("DOCENTES_URL", "http://docentes:5003/api"),
    "reservas": os.getenv("RESERVAS_URL", "http://reservas:5006/api"),
}
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

    domain = path.split('/')[0]
    if domain in ['login', 'usuarios', 'roles', 'salones', 'docentes', 'reservas']:
        target_base_url = MICROSERVICES.get(domain)
    else:
        target_base_url = MONOLITH_URL

    if not target_base_url:
        return {"error": "Servicio no encontrado"}, 404

    url = f"{target_base_url}/{path}"
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key.lower() not in {"host", "content-length"}},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=10,
        )
        return Response(resp.content, resp.status_code, resp.headers.items())
    except requests.exceptions.RequestException as exc:
        return {"error": f"No se pudo conectar al servicio en {url}: {exc}"}, 503


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)
