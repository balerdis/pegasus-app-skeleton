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
Documentacion de la pegasus-app-skeleton organización de directorios y objetivo de cada uno:

pegasus-app-skeleton
├── app
│   ├── api
│   │   ├── dependencies       # Directorio donde van los providers que Intermedia service del framework a la capa API
│   │   ├── main.py            # file central de construccion de la app FastAPI
│   │   └── v1                 # Directorio para versionado de endpoints
│   │       ├── endpoints      # directorio endpoints
│   │       └── schemas                  # Directorio para DTOs entre la capa API HTTP y la capa DOMAIN SERVICE
│   ├── cli                              # Futura interfaz de cli de la app
│   ├── config                           # Directorio de Config centralizada de la app
│   ├── core                             # Directorio para logica central independiente de la interfaz hacia afuera
│   │   ├── database                     # Directorio para logica de base de datos
│   │   │   ├── alembic                  # Directorio para ORM Alembic
│   │   │   ├── alembic.ini              # File Alembic decide que modelos tomar en cuenta 
│   │   │   ├── models                   # Directorio para modelos que representan la base de datos
│   │   │   └── repositories             # Directorio para el patron repository de los modelos a la base de datos
│   │   └── services                     # Directorio para el patron domain service con sus DTOs que va de capa resultset a capa service
│   ├── data                             # Directorio futuro almacenaje de archivos adjuntos
│   ├── overrides                          # Directorio para hacer override de logica proveniente desde el Pegasus-framework
│   ├── scripts                            # Directorio para script varios y de prueba
│   └── wiring                             # Directorio para vinculo de logica residente en el framework y se quiere utilizar en la app
│       └── bootstrap.py                   # File central de disponibilizacion de codigo residente en el framework y permitir usarlo desde la app
├── ARQUITECTURE.md           # File de documentación de la arquitectura de la aplicacion
├── pyproject.toml            # File para package de la app e indicar su dependencia del framework
├── README.md                 # File de documentacion general de la aplicacion
├── requirements.in           # File de dependencias para utilizar con pip-compile de pip-tools
├── requirements.in.example   # File de dependencias que se puede subir al repositorio
└── requirements.txt          # File resultante de pip-compile que podemos utilizar para pip-sync e instalar rapidamente las dependencias de la app

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
