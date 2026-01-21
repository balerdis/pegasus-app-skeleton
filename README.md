# pegasus-app-skeleton

## Propósito

`pegasus-app-skeleton` es un **esqueleto de aplicación backend en Python** diseñado para servir como punto de partida consistente y repetible para construir APIs basadas en **FastAPI**, apoyadas en el framework reutilizable **pegasus_framework**.

Este repositorio **no es una aplicación de negocio**, sino una **plantilla estructural** que define:

- cómo iniciar una nueva aplicación
- dónde vive cada responsabilidad
- cómo se integra correctamente con el framework
- cómo escalar sin degradar la arquitectura

---

## Qué es y qué no es

### Es

- Un punto de arranque oficial para nuevas aplicaciones
- Una referencia viva de arquitectura
- Un ejemplo canónico de integración framework ↔ aplicación
- Un contenedor de decisiones no negociables

### No es

- Un proyecto de negocio terminado (a modo de ejemplo se muestra 2 ABMS de entidades relacionadas y sistema de authenticacion JWT)
- Un monorepo de features
- Un framework alternativo
- Un lugar para lógica reusable transversal

---

## Stack tecnológico

- Python 3.11+
- FastAPI
- Pydantic
- SQLAlchemy ORM
- Alembic
- pegasus_framework

---

## Principio rector

> **La aplicación depende del framework.  
> El framework nunca depende de la aplicación.**

Toda la estructura del skeleton existe para hacer cumplir esta regla.

---

## Flujo de una request

```text
HTTP Request
↓
FastAPI Endpoint (Application)
↓
HTTP Schemas (Pydantic)
↓
Business Services (Framework / App)
↓
Unit of Work (Framework)
↓
Repositories (Framework)
↓
SQLAlchemy ORM
↓
Database
```

---

## Estructura del proyecto

```text
app/
├── api/
│   └── v1/
│       ├── endpoints/
│       └── schemas/
├── core/
│   ├── database/
│   │   ├── base.py
│   │   └── models/
│   ├── services/        # negocio propio de la app
│   └── unit_of_work/
├── wiring/
│   └── bootstrap.py
├── overrides/
├── main.py
└── settings.py
```

---

## Uso típico

1. Clonar este repositorio
2. Renombrar el proyecto
3. Definir el dominio propio (entidades, endpoints)
4. Integrar módulos del `pegasus_framework`
5. Implementar overrides y registries necesarios
6. Crear migraciones propias con Alembic

---

## Extensión del framework

La aplicación puede extender el framework mediante dos mecanismos explícitos:

- **Registry** → define *qué es* el sistema
- **Override** → define *cómo se comporta*

Ambos deben declararse de forma explícita durante el bootstrap.

---

## Documentación clave

- **ARCHITECTURE.md** → reglas, decisiones y contratos del sistema

Este archivo no debe eliminarse ni ignorarse: es parte del producto.

---

## Regla final

> Este skeleton no acelera el corto plazo.  
> Asegura la sostenibilidad del largo plazo.
