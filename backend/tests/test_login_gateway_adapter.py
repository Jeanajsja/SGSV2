from backend.services.login_gateway_adapter import LoginGatewayAdapter


class DummyResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload


class DummyClient:
    def __init__(self):
        self.calls = []

    def post_json(self, path, payload):
        self.calls.append((path, payload))
        return DummyResponse({"status": "ok", "user": {"nombre": "Ana"}}, 200)


def test_login_gateway_adapter_calls_external_auth_service():
    client = DummyClient()
    service = LoginGatewayAdapter(client)

    result = service.login("ana@gmail.com", "123")

    assert result["status"] == "ok"
    assert result["user"]["nombre"] == "Ana"
    assert client.calls == [("/login", {"email": "ana@gmail.com", "password": "123"})]
