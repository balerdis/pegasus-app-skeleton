# Arquitectura – pegasus-app-skeleton

## 1. Visión general

Este skeleton implementa una **arquitectura modular en capas**, inspirada en **Clean Architecture** y **DDD**, diseñada explícitamente para operar con un **framework reusable externo** (`pegasus_framework`).

El sistema siempre se divide en dos artefactos:

- **pegasus_framework** → framework reutilizable
- **Aplicación concreta** → construida sobre este skeleton

Regla absoluta:

> **El framework no conoce a la aplicación.  
> La aplicación depende del framework.**

---

## 2. Capas del sistema

### 2.1 Endpoints (FastAPI – Application)

Responsabilidades:
- Exponer contratos HTTP
- Orquestar dependencias
- Traducir errores de dominio a HTTP

Restricciones:
- Sin lógica de negocio
- Sin acceso a base de datos
- Sin instanciación directa de servicios

---

### 2.2 Schemas HTTP (Pydantic – Application)

Responsabilidades:
- Validar input/output HTTP
- Definir contratos públicos

Regla clave:

> **Los schemas HTTP no son DTOs de negocio.**

---

### 2.3 Servicios de negocio

Pueden existir en dos lugares:

- **Framework** → negocio reusable
- **Aplicación** → negocio específico

Características:
- No conocen HTTP
- No conocen FastAPI
- Operan mediante Unit of Work

---

### 2.4 Unit of Work (Framework)

Responsabilidades:
- Controlar sesión de DB
- Garantizar atomicidad
- Centralizar commit / rollback

Reglas:
- Una UoW por caso de uso
- Nadie ejecuta `commit()` fuera de la UoW

---

### 2.5 Repositories (Framework)

Responsabilidades:
- Encapsular acceso a datos
- Aislar SQLAlchemy del dominio

Decisión explícita:
- No existe método `update()`
- SQLAlchemy maneja el identity map

---

## 3. Registry vs Override

### Registry

Define **qué es** el sistema.

- Global
- Estático
- Ejecutado en bootstrap
- No depende del request

Usos típicos:
- Modelos ORM principales
- Proveedores globales
- Contratos estructurales

---

### Override

Define **cómo se comporta** el sistema.

- Dinámico
- Request-scoped
- Usa `dependency_overrides`
- Extiende o decora servicios

Usos típicos:
- Servicios de negocio
- Integraciones externas
- Logging, métricas, feature flags

---

## 4. Bootstrap de la aplicación

Toda inicialización explícita ocurre en un único punto:

```python
def bootstrap_application(app: FastAPI) -> None:
    register_models()
    register_providers()
    app.dependency_overrides[...]
```

Prohibido:
- Imports con efectos secundarios
- Registro implícito
- Wiring distribuido

---

## 5. Base de datos y migraciones

Principio fundamental:

> **La base de datos pertenece a la aplicación, no al framework.**

Consecuencias:
- Alembic vive solo en la aplicación
- El framework no define tablas concretas
- El framework puede definir contratos abstractos

La aplicación:
- Define su `Base`
- Es dueña del `MetaData`
- Versiona su historia con Alembic

---

## 6. Anti-patrones prohibidos

- Framework con migraciones
- Framework con `__tablename__`
- Commit fuera de la UoW
- Endpoints con lógica de negocio
- Repositorios expuestos a la API

---

## 7. Beneficios del diseño

- Bajo acoplamiento
- Reutilización real
- Testeo aislado
- Evolución segura
- Onboarding consistente

---

## 8. Regla de oro

> **Todo lo reusable vive en el framework.  
> Todo lo que define el contrato con el mundo vive en la aplicación.**

---
# 9. Arquitectura de la capa de servicios

## 9.1. Visión general

La capa de servicios representa el **Application Layer** del sistema y es responsable de:

- Implementar los casos de uso del negocio.
- Orquestar entidades, repositorios y unidades de trabajo mediante abstracciones.
- Aplicar reglas de negocio y políticas de la aplicación.
- Producir y consumir DTOs como mecanismo de intercambio de datos entre capas internas.

### 9.1.1. DTOs y resultados agregados

Los resultados agregados de negocio (por ejemplo: reports, summaries, analytics):

- **Siempre se modelan como DTOs** en la capa de servicios.
- No conocen ni dependen de HTTP, FastAPI ni de schemas de la API.
- Pueden ser reutilizados por distintos adaptadores de entrada (API, CLI, jobs, etc.).

La capa API es responsable de:

- Recibir requests HTTP mediante schemas específicos de la API.
- Mapear los DTOs retornados por la capa de servicios a schemas HTTP de response.
- Definir y versionar los contratos públicos expuestos a los clientes.

El flujo lógico completo de una request es el siguiente:
```text
HTTP Schema  →  DTO  →  Entity / Use Case  →  DTO  →  HTTP Response Schema
```

# 10 User Domain Ownership Rule

Pegasus Framework define únicamente los contratos abstractos e invariantes relacionados con identidad y autenticación.

La aplicación:

 - define el modelo concreto de usuario
 - implementa la tabla y las relaciones
 - define los servicios y casos de uso de negocio

El framework nunca implementa lógica de negocio asociada al dominio User.
