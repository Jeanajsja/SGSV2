import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db_config import get_connection
from login_controller import crear_router
from login_service import LoginService
from repositories.postgres_login_repository import PostgresLoginRepository
from security.werkzeug_password_hasher import WerkzeugPasswordHasher
from seed_superadmin import asegurar_superadmin


def create_app(service=None):
    asegurar_superadmin(get_connection)
    if service is None:
        service = LoginService(PostgresLoginRepository(get_connection), WerkzeugPasswordHasher())

    app = FastAPI(title="ms-login")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "ms-login"}

    app.include_router(crear_router(service))
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 5001)), reload=True)
