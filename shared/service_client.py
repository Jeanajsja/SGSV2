import requests

from shared.service_registry import get_service_url


class ServiceClient:
    def __init__(self, domain: str, timeout: int = 10):
        self.domain = domain
        self.timeout = timeout
        self.base_url = get_service_url(domain)

    def build_url(self, path: str) -> str:
        normalized = path.lstrip("/")
        return f"{self.base_url.rstrip('/')}/{normalized}"

    def proxy_request(self, incoming_request, *, path: str):
        headers = {
            key: value
            for key, value in incoming_request.headers
            if key.lower() not in {"host", "content-length"}
        }
        return requests.request(
            method=incoming_request.method,
            url=self.build_url(path),
            headers=headers,
            data=incoming_request.get_data(),
            cookies=incoming_request.cookies,
            allow_redirects=False,
            timeout=self.timeout,
        )
