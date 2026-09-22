import unittest
from interfaces.password_hasher import IPasswordHasher
from login_service import LoginService
from repositories.memory_login_repository import MemoryLoginRepository


class FakeHasher(IPasswordHasher):
    def verificar(self, password: str, almacenado: str) -> bool:
        return almacenado == password or almacenado == f"hash:{password}"


class TestLoginService(unittest.TestCase):
    def setUp(self):
        self.repo = MemoryLoginRepository()
        self.repo.agregar(
            {
                "id_usuario": 1,
                "nombre": "Ana",
                "email": "ana@gmail.com",
                "password": "hash:123",
                "id_rol": 1,
            }
        )
        self.service = LoginService(self.repo, FakeHasher())

    def test_login_ok(self):
        res = self.service.login("ana@gmail.com", "123")
        self.assertEqual(res["status"], "ok")
        self.assertNotIn("password", res["user"])

    def test_login_malo(self):
        res = self.service.login("ana@gmail.com", "otra")
        self.assertEqual(res["status"], "error")


if __name__ == "__main__":
    unittest.main()
