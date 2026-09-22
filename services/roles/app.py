import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db_config import get_connection
from repositories.postgres_rol_repository import PostgresRolRepository
from rol_controller import crear_router
from rol_service import RolService


def create_app(service=None):
    if service is None:
        service = RolService(PostgresRolRepository(get_connection))
    app = FastAPI(title="ms-roles")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "ms-roles"}

    app.include_router(crear_router(service))
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 5004)), reload=True)
