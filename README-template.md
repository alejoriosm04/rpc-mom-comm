## ST0263 Tópic. Espec. en Telemática - Proyecto 1

### Integrantes

- Alejandro Ríos Muñoz - ariosm@eafit.edu.co
- Lina Sofía Ballesteros Merchán - lsballestm@eafit.edu.co
- Jhonnatan Stiven Ocampo Díaz - jsocampod@eafit.edu.co

### Profesor

- Edwin Nelson Montoya Munera - emontoya@eafit.edu.co

## RPC communication system with MOM failure system

### 1. Descripción del proyecto

Este proyecto implementa un sistema de comunicación distribuido que combina RPC (Remote Procedure Call) con un sistema de fallback basado en MOM (Message-Oriented Middleware). 

El sistema permite la comunicación entre servicios distribuidos, donde RPC se utiliza como el método principal de comunicación, y en caso de fallos en la comunicación RPC, el sistema automáticamente cambia a un sistema de mensajería basado en MOM para garantizar la continuidad del servicio. 

Esta arquitectura híbrida proporciona tanto la eficiencia de RPC como la robustez y tolerancia a fallos de los sistemas de mensajería.

#### 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

##### 🧩 Requerimientos Funcionales

| Código | Título                                           | Descripción                                                                                                                                                   |
|--------|--------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RF01   | Comunicación RPC eficiente entre microservicios  | El sistema deberá permitir la comunicación entre microservicios mediante gRPC para asegurar una transmisión eficiente, estructurada y de baja latencia. La comunicación debe soportar reconexión en caso de falla de red. |
| RF02   | API Gateway como punto único de entrada          | El sistema deberá contar con un API Gateway que actúe como punto único de acceso, convirtiendo las solicitudes REST entrantes en llamadas gRPC hacia los microservicios. |
| RF03   | Cliente REST con interfaz gráfica                | El sistema deberá proporcionar una interfaz web, que permita al usuario realizar solicitudes REST y recibir actualizaciones mediante WebSockets.              |
| RF04   | Mecanismo de failover con MOM (RabbitMQ)         | El sistema deberá utilizar un Message Oriented Middleware (MOM) como RabbitMQ para asegurar la entrega de mensajes entre microservicios en caso de caída. Mensajes no deben perderse durante fallos temporales y los microservicios deben reintentar procesar mensajes una vez estén activos. |
| RF05   | Microservicio de Productos con CRUD              | El sistema deberá contar con un microservicio capaz de realizar operaciones CRUD sobre productos, almacenando la información en MongoDB y exponiendo sus servicios vía gRPC. |
| RF06   | Microservicio de Inventario con gestión de stock | El sistema deberá contar con un microservicio de inventario encargado de gestionar el stock de productos y actualizarlo en tiempo real en respuesta a solicitudes de órdenes. |
| RF07   | Microservicio de Órdenes con verificación de inventario | El sistema deberá contar con un microservicio que permita registrar órdenes realizadas por usuarios y verificar en tiempo real el stock disponible mediante comunicación gRPC con el microservicio de inventario. |

---

##### 🔧 Requerimientos No Funcionales

| Código | Título                                 | Descripción                                                                                                                                         |
|--------|----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| RNF01  | Alta disponibilidad                    | El sistema deberá estar disponible incluso si uno o más componentes fallan, gracias a mecanismos de failover y reintentos. La caída de un microservicio no debe afectar la disponibilidad general. |
| RNF02  | Escalabilidad horizontal               | El sistema deberá poder escalar horizontalmente, permitiendo múltiples instancias de microservicios para atender mayor carga. Los microservicios deben ejecutarse como contenedores y la infraestructura debe soportar balanceo de carga. |
| RNF03  | Seguridad de la comunicación y acceso  | El sistema deberá contar con mecanismos de autenticación y autorización, además de cifrado en las comunicaciones. Las API deben tener autenticación por token y el acceso debe estar controlado por roles. |
| RNF04  | Mantenibilidad del código y despliegue | El sistema deberá tener código modular, documentado y con capacidad de despliegue automatizado mediante Docker.                                     |
| RNF05  | Monitoreo y logging                    | El sistema deberá proporcionar métricas, logs y alertas que permitan su monitoreo y diagnóstico continuo.                                           |

#### 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Esperemos que todos esten completos 🙌🙏

### 2. Información general

#### 2.1 Diseño de alto nivel ***

**Insertar Diagrama**

El sistema está compuesto por una arquitectura de microservicios donde cada componente cumple un rol específico. A través de un API Gateway se canalizan todas las peticiones REST del cliente, las cuales son traducidas a llamadas gRPC para comunicarse con los microservicios internos.

**Componentes:**
- Cliente Web (Next.js)
- API Gateway (FastAPI)
- Microservicio de Productos
- Microservicio de Inventario
- Microservicio de Órdenes
- MongoDB (persistencia)
- RabbitMQ (MOM)

#### 2.2 Arquitectura ***

**Insertar Diagrama**

- Los microservicios se comunican entre sí por gRPC
- RabbitMQ se usa como mecanismo de recuperación ante fallos (failover)
- MongoDB es la base de datos por microservicio
- Docker Swarm permite escalar los servicios horizontalmente y manejar la red interna

#### 2.3 Patrones de diseño

- **Microservicios:** separación de lógica por dominio
- **API Gateway:** punto único de entrada
- **Request/Reply asincrónico:** resiliencia con RabbitMQ
- **Protocol Buffers (DTO):** contratos definidos para la comunicación gRPC

#### 2.4 Buenas prácticas utilizadas

- Separación de responsabilidades por servicio
- Comunicación eficiente con gRPC
- Escalabilidad horizontal con Docker Swarm
- Seguridad básica con autenticación y cifrado en APIs
- Despliegue contenerizado y reproducible
- Uso de redes internas para aislar servicios
- Configuración con variables de entorno
- Observabilidad con logs y métricas

### 3. Descripción del ambiente de desarrollo y técnico

#### 3.1 Lenguajes y tecnologías principales

| Componente           | Tecnología         | Versión               |
|----------------------|--------------------|------------------------|
| Frontend             | Next.js (React)    | 14.1.0                |
| API Gateway          | FastAPI (Python)   | 0.104.1               |
| gRPC                 | grpcio (Python)    | 1.60.0                |
| Microservicios       | Python             | 3.10                  |
| Comunicación gRPC    | Protocol Buffers   | 3.21.12               |
| Bases de datos       | MongoDB            | 6.0                   |
| Middleware (MOM)     | RabbitMQ           | 3.12 (Management UI)  |
| Orquestación         | Docker Swarm       | Docker 24.0.5         |
| Contenedores         | Docker Engine      | 24.0.5                |

#### 3.2 Cómo compilar y ejecutar el proyecto

##### Requisitos previos

##### Despliegue completo del sistema

#### 3.3 Detalles del desarrollo

#### 3.4 Detalles técnicos y configuración

#### 3.5 Estructura del proyecto

#### 3.6 Resultados y pantallazos

### 4. Descripción del ambiente de ejecución (Producción)

#### 4.1 Despliegue

#### 4.2 IP o nombre de dominio del servidor

- RabbitMQ: `http://<TU_IP_PUBLICA>:15672`
- Acceso frontend: `http://<TU_IP_PUBLICA>:3000`

> ⚠️ Recuerda abrir los puertos en el grupo de seguridad o firewall si usas AWS, GCP o VPS.

#### 4.3 Mini guía para el usuario final



### Referencias

A continuación se listan las referencias utilizadas para el desarrollo del proyecto, incluyendo documentación oficial, tutoriales, videos, artículos y fragmentos de código reutilizados:
