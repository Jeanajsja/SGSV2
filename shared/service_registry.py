import os

from shared.service_catalog import MONOLITH_BASE_URL, SERVICE_CATALOG

MONOLITH_URL = os.getenv("MONOLITH_URL", MONOLITH_BASE_URL)
MICROSERVICES = {
    domain: os.getenv(f"{domain.upper()}_URL", spec.base_url)
    for domain, spec in SERVICE_CATALOG.items()
}


def get_service_url(domain: str) -> str:
    return MICROSERVICES.get(domain, MONOLITH_URL)


def resolve_target_base_url(path: str) -> str:
    domain = path.split("/")[0]
    if domain in MICROSERVICES:
        return MICROSERVICES[domain]
    return MONOLITH_URL
