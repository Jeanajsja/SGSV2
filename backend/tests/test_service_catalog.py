from shared.service_catalog import MONOLITH_BASE_URL, SERVICE_CATALOG


def test_catalog_has_expected_domains():
    assert set(SERVICE_CATALOG) == {"login", "usuarios", "roles", "salones", "docentes", "reservas"}
    assert MONOLITH_BASE_URL == "http://monolito:5000/api"


def test_catalog_provides_base_urls():
    assert SERVICE_CATALOG["login"].base_url == "http://login:5001/api"
    assert SERVICE_CATALOG["reservas"].base_url == "http://reservas:5006/api"
