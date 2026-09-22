import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from interfaces.email_validator import IEmailValidator
from interfaces.password_hasher import IPasswordHasher
from interfaces.password_verifier import IPasswordVerifier
from models.administrador import Administrador
from models.superadministrador import Superadministrador
from models.usuario import Usuario
from models.usuario_factory import usuario_desde_fila
from repositories.memory_docente_repository import MemoryDocenteRepository
from repositories.memory_reserva_repository import MemoryReservaRepository
from repositories.memory_rol_repository import MemoryRolRepository
from repositories.memory_salon_repository import MemorySalonRepository
from repositories.memory_usuario_repository import MemoryUsuarioRepository
from services.docente_service import DocenteService
from services.email_validator import validar_dominio_email
from services.login_service import LoginService
from services.reserva_service import ReservaService
from services.rol_service import RolService
from services.salon_service import SalonService
from services.usuario_service import UsuarioService


class FakeHasher(IPasswordHasher):
    def hash(self, password: str) -> str:
        return f"hash:{password}"


class FakeVerifier(IPasswordVerifier):
    def verificar(self, password: str, almacenado: str) -> bool:
        return almacenado == f"hash:{password}" or almacenado == password


class FakeEmailOk(IEmailValidator):
    def validar(self, email):
        return None


class FakeEmailFail(IEmailValidator):
    def validar(self, email):
        return {"status": "error", "message": "correo malo"}


class TestS_ResponsabilidadUnica(unittest.TestCase):
    def test_usuario_solo_registra(self):
        self.assertFalse(hasattr(UsuarioService, "login"))

    def test_login_solo_inicia_sesion(self):
        self.assertTrue(hasattr(LoginService, "login"))
        self.assertFalse(hasattr(LoginService, "crear_usuario"))


class TestO_AbiertoCerrado(unittest.TestCase):
    def test_otro_repo_sin_cambiar_el_servicio(self):
        service = SalonService(MemorySalonRepository())
        res = service.crear({"nombre": "Lab Redes", "capacidad": 30, "ubicacion": "Piso 3"})
        self.assertEqual(res["status"], "ok")
        self.assertEqual(len(service.listar()), 1)

    def test_capacidad_invalida(self):
        service = SalonService(MemorySalonRepository())
        res = service.crear({"nombre": "Lab", "capacidad": 0, "ubicacion": "Piso 1"})
        self.assertEqual(res["status"], "error")


class TestL_Sustitucion(unittest.TestCase):
    def test_superadmin_y_admin_se_usan_como_usuario(self):
        fila_super = {"id_usuario": 1, "nombre": "Luisa", "email": "a@ucatolica.edu.co", "id_rol": 1}
        fila_admin = {"id_usuario": 2, "nombre": "Juan", "email": "j@ucatolica.edu.co", "id_rol": 2}
        superadmin = usuario_desde_fila(fila_super)
        admin = usuario_desde_fila(fila_admin)
        self.assertIsInstance(superadmin, Superadministrador)
        self.assertIsInstance(admin, Administrador)
        self.assertIsInstance(superadmin, Usuario)
        self.assertIsInstance(admin, Usuario)
        self.assertEqual(superadmin.to_public_dict()["nombre"], "Luisa")
        self.assertEqual(admin.to_public_dict()["nombre"], "Juan")
        self.assertIn("Superadministrador", superadmin.etiqueta())
        self.assertIn("Administrador", admin.etiqueta())

    def test_memory_repo_reemplaza_postgres_en_login(self):
        repo = MemoryUsuarioRepository()
        repo.crear("Ana", "ana@gmail.com", "hash:123", 1)
        service = LoginService(repo, FakeVerifier())
        res = service.login("ana@gmail.com", "123")
        self.assertEqual(res["status"], "ok")
        self.assertNotIn("password", res["user"])


class TestI_Segregacion(unittest.TestCase):
    def test_registro_no_pide_verificar(self):
        service = UsuarioService(MemoryUsuarioRepository(), FakeHasher(), FakeEmailOk())
        res = service.crear_usuario({"nombre": "Ana", "email": "ana@gmail.com", "password": "123", "id_rol": 2})
        self.assertEqual(res["status"], "ok")

    def test_solo_el_ancla_crea_superadmin(self):
        service = UsuarioService(MemoryUsuarioRepository(), FakeHasher(), FakeEmailOk())
        denegado = service.crear_usuario(
            {"nombre": "Otra", "email": "otra@ucatolica.edu.co", "password": "123", "id_rol": 1}
        )
        self.assertEqual(denegado["status"], "error")
        ok = service.crear_usuario(
            {
                "nombre": "Otra",
                "email": "otra@ucatolica.edu.co",
                "password": "123",
                "id_rol": 1,
                "solicitante_email": "lfpaez30@ucatolica.edu.co",
            }
        )
        self.assertEqual(ok["status"], "ok")

    def test_superadmin_cambia_rol_y_elimina(self):
        repo = MemoryUsuarioRepository()
        repo.crear("Luisa", "lfpaez30@ucatolica.edu.co", "hash:123", 1)
        service = UsuarioService(repo, FakeHasher(), FakeEmailOk())
        service.crear_usuario({"nombre": "Ana", "email": "ana@gmail.com", "password": "123", "id_rol": 3})
        ana = repo.buscar_por_email("ana@gmail.com")
        denegado = service.cambiar_rol(ana["id_usuario"], 2, "ana@gmail.com")
        self.assertEqual(denegado["status"], "error")
        cambiado = service.cambiar_rol(ana["id_usuario"], 2, "lfpaez30@ucatolica.edu.co")
        self.assertEqual(cambiado["status"], "ok")
        self.assertEqual(repo.buscar_por_id(ana["id_usuario"])["id_rol"], 2)
        ancla = repo.buscar_por_email("lfpaez30@ucatolica.edu.co")
        self.assertEqual(service.eliminar_cuenta(ancla["id_usuario"], "lfpaez30@ucatolica.edu.co")["status"], "error")
        self.assertEqual(service.eliminar_cuenta(ana["id_usuario"], "lfpaez30@ucatolica.edu.co")["status"], "ok")
        self.assertIsNone(repo.buscar_por_id(ana["id_usuario"]))

    def test_login_no_pide_hash(self):
        repo = MemoryUsuarioRepository()
        repo.crear("Ana", "ana@gmail.com", "hash:123", 1)
        service = LoginService(repo, FakeVerifier())
        self.assertEqual(service.login("ana@gmail.com", "123")["status"], "ok")


class TestD_Inversion(unittest.TestCase):
    def test_inyecto_validador_y_hasher_falsos(self):
        service = UsuarioService(MemoryUsuarioRepository(), FakeHasher(), FakeEmailFail())
        res = service.crear_usuario({"nombre": "Ana", "email": "ana@gmal.com", "password": "123", "id_rol": 1})
        self.assertEqual(res["status"], "error")

    def test_docente_usa_el_validador_inyectado(self):
        service = DocenteService(MemoryDocenteRepository(), FakeHasher(), FakeEmailOk())
        res = service.crear({"nombre": "Maria", "correo": "maria@gmail.com"})
        self.assertEqual(res["status"], "ok")
        self.assertEqual(len(service.listar()), 1)

    def test_roles_y_reservas_con_memoria(self):
        roles = RolService(MemoryRolRepository())
        self.assertGreaterEqual(len(roles.listar()), 3)
        reservas = ReservaService(MemoryReservaRepository())
        creado = reservas.crear_reserva(
            {"fecha": "2026-09-18", "hora_inicio": "08:00", "hora_fin": "10:00", "id_salon": 1, "id_docente": 2}
        )
        self.assertEqual(creado["status"], "ok")
        self.assertEqual(reservas.listar()["status"], "ok")


class TestEmailValidator(unittest.TestCase):
    def test_typo_gmail(self):
        res = validar_dominio_email("ana@gmal.com")
        self.assertEqual(res["status"], "error")
        self.assertIn("gmail.com", res["message"])

    def test_dominio_valido(self):
        self.assertIsNone(validar_dominio_email("ana@gmail.com"))


if __name__ == "__main__":
    unittest.main()
