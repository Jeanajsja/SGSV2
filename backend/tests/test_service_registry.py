from shared.service_registry import get_service_url, resolve_target_base_url


def test_known_service_url_is_resolved_from_registry():
    assert get_service_url("login") == "http://login:5001/api"
    assert get_service_url("reservas") == "http://reservas:5006/api"


def test_unknown_path_falls_back_to_monolith():
    assert resolve_target_base_url("usuarios/1") == "http://usuarios:5005/api"
    assert resolve_target_base_url("app/otra-ruta") == "http://monolito:5000/api"
