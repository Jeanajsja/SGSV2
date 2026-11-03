from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceSpec:
    name: str
    host: str
    port: int
    path_prefix: str = "/api"

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}{self.path_prefix}"


SERVICE_CATALOG = {
    "login": ServiceSpec(name="login", host="login", port=5001),
    "usuarios": ServiceSpec(name="usuarios", host="usuarios", port=5005),
    "roles": ServiceSpec(name="roles", host="roles", port=5004),
    "salones": ServiceSpec(name="salones", host="salones", port=5002),
    "docentes": ServiceSpec(name="docentes", host="docentes", port=5003),
    "reservas": ServiceSpec(name="reservas", host="reservas", port=5006),
}

SERVICE_DOMAINS = tuple(SERVICE_CATALOG.keys())
MONOLITH_BASE_URL = "http://monolito:5000/api"
