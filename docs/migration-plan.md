# Plan de migración más limpia hacia microservicios

## Objetivo

Separar los dominios por bounded contexts, conservar la lógica de negocio centralizada en servicios pequeños, y dejar la capa de gateway como única entrada pública.

## Principios de la migración

1. Un servicio debe tener una única responsabilidad de negocio.
2. Cada dominio debe poseer su propia base de datos o esquema.
3. El gateway no debe conocer detalles internos de cada servicio.
4. Las llamadas entre servicios deben pasar por contratos explícitos.
5. La migración debe realizarse en fases con validación de cada dominio.

## Dominios propuestos

- `auth` / `login`
- `usuarios`
- `roles`
- `salones`
- `docentes`
- `reservas`

## Fase 1: congelar el contrato actual

- Definir rutas públicas por dominio.
- Mantener las mismas respuestas y códigos HTTP.
- Asegurar que el gateway siga redirigiendo a la URL correcta.
- Guardar pruebas por servicio para cada endpoint.

## Fase 2: separar ownership de base de datos

- `login` y `usuarios`: autenticación y perfiles.
- `roles`: gestión de permisos.
- `salones`: catálogo y disponibilidad.
- `docentes`: docentes y validación de correo.
- `reservas`: flujo de creación, actualización y cancelación.

Cada servicio debe ser dueño de su esquema y no depender directamente del repositorio de otro dominio.

## Fase 3: migrar la lógica de negocio

- Mover las reglas de negocio de `backend/services` a cada microservicio.
- Mantener interfaces en cada dominio: repositorios, validadores, hashers.
- Eliminar acceso cruzado entre tablas de otros servicios.
- Dejar una sola implementación canónica por dominio.

## Fase 4: aislar la comunicación

- Usar `shared/service_catalog.py` y `shared/service_registry.py` como fuente de verdad de URLs.
- Usar `shared/service_client.py` como wrapper para llamadas HTTP.
- No duplicar rutas ni hostnames en los servicios.

## Fase 5: despliegue y observabilidad

- Agregar health checks por servicio.
- Centralizar logs y trazas.
- Debe haber timeouts, errores y reintentos controlados.
- Gateway debe responder con errores 502/503 bien definidos.

## Guardrails de calidad

- No más imports del tipo `from models...` cruzando dominios.
- No más `POSTGRES` shared entre servicios.
- No más endpoint de varios dominios mezclados en un mismo servicio.
- Cada servicio debe tener:
  - `app.py`
  - `service.py`
  - `controller.py`
  - `repository.py`
  - `interface/`
  - `models/`

## Criterio para marcar una migración exitosa

Un dominio está migrado cuando:

- tiene su propio servicio ejecutable,
- usa su propio repositorio y conexión,
- expone contratos públicos documentados,
- deja de depender de la capa monolítica,
- pasa sus pruebas de dominio.

## Orden recomendado

1. `login`
2. `usuarios`
3. `roles`
4. `salones`
5. `docentes`
6. `reservas`

Esto mantiene el flujo de autenticación y permisos primero, luego el resto del negocio.
