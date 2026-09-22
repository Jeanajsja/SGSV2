import os

MONOLITH_URL = os.getenv("MONOLITH_URL", "http://monolito:5000/api")
MICROSERVICES = {
    "login": os.getenv("LOGIN_URL", "http://login:5001/api"),
    "usuarios": os.getenv("USUARIOS_URL", "http://usuarios:5005/api"),
    "roles": os.getenv("ROLES_URL", "http://roles:5004/api"),
    "salones": os.getenv("SALONES_URL", "http://salones:5002/api"),
    "docentes": os.getenv("DOCENTES_URL", "http://docentes:5003/api"),
    "reservas": os.getenv("RESERVAS_URL", "http://reservas:5006/api"),
}


def get_service_url(domain: str) -> str:
    return MICROSERVICES.get(domain, MONOLITH_URL)


def resolve_target_base_url(path: str) -> str:
    domain = path.split("/")[0]
    if domain in MICROSERVICES:
        return MICROSERVICES[domain]
    return MONOLITH_URL
