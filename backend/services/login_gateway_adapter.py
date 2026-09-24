class LoginGatewayAdapter:
    def __init__(self, http_client):
        self._client = http_client

    def login(self, email: str, password: str):
        response = self._client.post_json("/login", {"email": email, "password": password})
        return response.json()
