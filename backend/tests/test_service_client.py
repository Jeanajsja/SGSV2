from shared.service_client import ServiceClient


def test_service_client_builds_expected_url():
    client = ServiceClient("login")
    assert client.base_url == "http://login:5001/api"
    assert client.build_url("usuarios/1") == "http://login:5001/api/usuarios/1"
