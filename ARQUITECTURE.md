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
- El UnitOfWork no impone políticas de commit (El UnitOfWork garantiza el boundary transaccional).
- La responsabilidad de cerrar una transacción pertenece al Application Service (El Application Service decide cuándo persistir).

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

# 11 Sesion Persistence
 - Toda sesión autenticada persistente debe tener representación en base de datos.
 - No se admiten JWT “stateless puros” para usuarios autenticados.

# 12 ## Unit of Work & Transaction Management Policy

### 12.1. Objetivo

El sistema adopta el patrón **Unit of Work (UoW)** como límite transaccional explícito para todas las operaciones que modifican estado persistente.

Los objetivos de esta política son:

- Garantizar **consistencia transaccional**
- Evitar **errores silenciosos** en operaciones de escritura
- Separar de forma estricta **lógica de negocio** de **infraestructura**
- Hacer explícitas las decisiones de `commit` y `rollback`
- Proveer un modelo transaccional homogéneo entre aplicaciones

---

### 12.2. Propiedad y responsabilidad

- La **UnitOfWork es provista exclusivamente por el framework** (`pegasus-framework`)
- La aplicación **no define implementaciones concretas de UoW**
- La aplicación **consume la UoW a través de los services**

Esto garantiza:

- Centralización de la política transaccional
- Independencia de la aplicación respecto al ORM o backend de persistencia
- Consistencia de comportamiento entre distintos proyectos basados en el framework

---

### 12.3. Política transaccional obligatoria

El sistema adopta una política de **commit explícito y obligatorio**.

Las reglas son las siguientes:

1. Toda operación que abre una UnitOfWork **debe ejecutar `commit()` explícitamente** si la operación es exitosa.
2. Si ocurre una excepción dentro del bloque `with`, la UnitOfWork:
   - ejecuta `rollback()` automáticamente.
3. **Salir de una UnitOfWork sin excepción y sin haber llamado a `commit()` es un error de programación.**

Formalmente:

> **Un bloque `with UnitOfWork()` que finaliza sin excepción y sin una llamada explícita a `commit()` representa un estado inválido del sistema.**

Este estado **no debe resolverse de forma silenciosa** y debe manifestarse como un error explícito.

---

### 12.4. Ciclo de vida de la Unit of Work

El ciclo de vida válido de una UnitOfWork es el siguiente:

1. Entrada al contexto (`__enter__`)
2. Ejecución de lógica de negocio
3. Una y solo una de las siguientes opciones:
   - `commit()` → confirma la transacción
   - excepción → rollback automático
4. Cierre y liberación de recursos (`__exit__`)

Cualquier desviación de este flujo se considera un error de uso.

---

### 12.5. Rol de los Services

- Los **services de la aplicación controlan explícitamente** el alcance transaccional.
- Los services:
  - deciden cuándo abrir una UnitOfWork
  - deciden cuándo ejecutar `commit()`
- Los services **no manejan directamente sesiones ni conexiones** de base de datos.

Ejemplo conceptual:

```python
with self._uow() as uow:
    repo = uow.repo(MovieRepository)
    entity = repo.create(data)
    uow.commit()
```
--- 


### 12.6 Rol del framework

El framework es responsable de:  

 - Proveer la abstracción UnitOfWork
 - Proveer implementaciones concretas (por ejemplo, SQLAlchemy)
 - Imponer invariantes transaccionales
 - Garantizar rollback automático ante excepciones
 - Garantizar la liberación de recursos al finalizar la UoW
El framework no ejecuta commits implícitos ni oculta el límite transaccional.

---

### 12.7 Prohibiciones explícitas

Quedan explícitamente prohibidos los siguientes comportamientos:

 - Commits implícitos al salir del bloque with
 - Autocommit automático en ausencia de errores
 - Uso directo de sesiones, conexiones o transacciones desde la aplicación
 - Silenciar el caso “sin commit y sin excepción”
 - Estas prohibiciones son parte del contrato arquitectónico del sistema.

--- 
### 12.8 Principio rector

```text
La transacción es una decisión de negocio expresada de forma explícita, nunca un efecto colateral de la infraestructura.
```
Este principio rige todas las decisiones relacionadas con persistencia y consistencia de datos dentro del sistema.


---

# 13. Error Management Policy

## 13.1. Visión general
La semántica del error vive en la excepción.
La forma HTTP del error vive en el handler.
El contrato HTTP es único y consistente.

## 13.2. Principio rector
```text
Los errores son un aspecto de negocio, no de infraestructura.
```
El principio rige todas las decisiones relacionadas con el manejo de errores dentro del sistema.

# 14. Anti-patrones prohibidos

- Framework con migraciones
- Framework con `__tablename__`

# 15. JWT Implementation

Pegasus Framework utiliza PyJWT como librería de referencia para JWT.
El paquete `jwt` (pip) no es compatible y no debe utilizarse.

# 16. Protección de Endpoints y Autenticación

## 16.1 Principio fundamental

Autenticación, identidad y autorización son responsabilidades distintas y no deben confundirse.

Un endpoint debe exigir **únicamente el nivel de protección que realmente necesita**.

## 16.2 Niveles de protección

El sistema reconoce tres niveles explícitos de protección de endpoints:

### Nivel A — Autenticación técnica

Garantiza que el request:
- contiene credenciales
- presenta un token válido
- el token no está expirado ni es inválido

Características:
- No carga entidades de dominio
- No accede a base de datos
- No construye `User`

Ejemplos de uso:
- `/auth/logout`
- `/auth/refresh`
- Endpoints que sólo requieren que el request no sea anónimo

---

### Nivel B — Contexto de identidad

Además de la autenticación técnica:
- identifica al usuario
- carga el agregado `User`
- establece contexto de dominio

Características:
- Accede a base de datos
- Construye entidades de dominio
- Tiene costo computacional mayor

Ejemplos de uso:
- `/users/me`
- Casos de uso que dependen del usuario autenticado

---

### Nivel C — Autorización de negocio

Evalúa reglas del dominio sobre el usuario autenticado:
- roles
- ownership
- permisos

Este nivel **siempre requiere** Nivel B.

---

## 16.3 Regla arquitectónica obligatoria

> **Un endpoint no debe depender de `get_current_user` si no necesita el agregado `User`.**

La autenticación técnica y la carga de identidad deben mantenerse separadas.

Sobrecargar un endpoint con identidad cuando no es requerida se considera un error de diseño.

---

## 16.4 Dependencias recomendadas

- Autenticación técnica:
  - `get_bearer_token`
  - `require_authentication`

- Identidad:
  - `get_current_user`

Cada endpoint debe declarar explícitamente cuál necesita.
