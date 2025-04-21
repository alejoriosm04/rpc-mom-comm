## ST0263 Tópic. Espec. en Telemática - Proyecto 1

### Integrantes

- Alejandro Ríos Muñoz - ariosm@eafit.edu.co
- Lina Sofía Ballesteros Merchán - lsballestm@eafit.edu.co
- Jhonnatan Stiven Ocampo Díaz - jsocampod@eafit.edu.co

### Profesor

- Edwin Nelson Montoya Munera - emontoya@eafit.edu.co

### Índice

1. [Descripción del proyecto](#1-descripción-del-proyecto)
   - [1.1 Requerimientos funcionales y no funcionales](#11-que-aspectos-cumplió-o-desarrolló-de-la-actividad-propuesta-por-el-profesor-requerimientos-funcionales-y-no-funcionales)
   - [1.2 Aspectos no desarrollados](#12-que-aspectos-no-cumplió-o-desarrolló-de-la-actividad-propuesta-por-el-profesor-requerimientos-funcionales-y-no-funcionales)

2. [Información general](#2-información-general)
   - [2.1 Diseño de alto nivel](#21-diseño-de-alto-nivel)
   - [2.2 Arquitectura](#22-arquitectura)
   - [2.3 Patrones de diseño](#23-patrones-de-diseño)
   - [2.4 Buenas prácticas utilizadas](#24-buenas-prácticas-utilizadas)

3. [Ambiente de desarrollo y técnico](#3-descripción-del-ambiente-de-desarrollo-y-técnico)
   - [3.1 Lenguajes y tecnologías principales](#31-lenguajes-y-tecnologías-principales)
   - [3.2 Compilación y ejecución](#32-cómo-compilar-y-ejecutar-el-proyecto)
   - [3.3 Detalles del desarrollo](#33-detalles-del-desarrollo)
   - [3.4 Estructura del proyecto](#34-estructura-del-proyecto)
   - [3.5 Descripción de los componentes](#35-descripción-de-los-componentes)
   - [3.6 Resultados y pantallazos](#36-resultados-y-pantallazos)

4. [Ambiente de ejecución (Producción)](#4-descripción-del-ambiente-de-ejecución-producción)
   - [4.1 Despliegue](#41-despliegue)
   - [4.2 IP o nombre de dominio del servidor](#42-ip-o-nombre-de-dominio-del-servidor)
   - [4.3 Mini guía para el usuario final](#43-mini-guía-para-el-usuario-final)

5. [Referencias](#referencias)

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
| RF06   | Microservicio de Inventario con gestión de stock | El sistema deberá contar con un microservicio de inventario encargado de gestionar el stock de productos y actualizarlo en tiempo real en respuesta a solicitudes de órdenes y productos. |
| RF07   | Microservicio de Órdenes con verificación de inventario | El sistema deberá contar con un microservicio que permita registrar órdenes realizadas por usuarios y verificar en tiempo real el stock disponible mediante comunicación gRPC con el microservicio de inventario. Actualizando dinámicamente el stock en el microservicio de inventario. |

---

##### 🔧 Requerimientos No Funcionales

| Código | Título                                 | Descripción                                                                                                                                         |
|--------|----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| RNF01  | Alta disponibilidad                    | El sistema deberá estar disponible incluso si uno o más componentes fallan, gracias a mecanismos de failover y reintentos. La caída de un microservicio no debe afectar la disponibilidad general. |
| RNF02  | Escalabilidad horizontal               | El sistema deberá poder escalar horizontalmente, permitiendo múltiples instancias de microservicios para atender mayor carga. Los microservicios deben ejecutarse como contenedores y la infraestructura debe soportar balanceo de carga. |
| RNF03  | Seguridad de la comunicación y acceso  | El sistema deberá contar con mecanismos de autenticación y autorización, además de cifrado en las comunicaciones. Las API deben tener autenticación por token y el acceso debe estar controlado por roles. |
| RNF04  | Mantenibilidad del código y despliegue | El sistema deberá tener código modular, documentado y con capacidad de despliegue automatizado mediante Docker.                                     |
| RNF05  | Monitoreo, logging y testing continuo  | El sistema deberá proporcionar métricas, logs y alertas que permitan su monitoreo y diagnóstico continuo. Además, deberá incorporar pruebas automáticas (unitarias) como parte del flujo de desarrollo. |

#### 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Se cumplió con todos los requerimientos funcionales y no funcionales propuestos.

### 2. Información general

#### 2.1 Diseño de alto nivel 

![HLD](https://github.com/user-attachments/assets/33ec742f-d34f-42df-8f8a-ac37123c75bc)

El sistema está compuesto por una arquitectura de microservicios donde cada componente cumple un rol específico. A través de un API Gateway se canalizan todas las peticiones REST del cliente, las cuales son traducidas a llamadas gRPC para comunicarse con los microservicios internos. Además, se ha implementado un mecanismo de fallback utilizando RabbitMQ para manejar los fallos temporales de los microservicios.

**Componentes:**
- Cliente Web (Next.js): Interfaz de usuario construida con Next.js, donde los usuarios pueden interactuar con el sistema.
- API Gateway (FastAPI): Punto de entrada principal para todas las solicitudes del cliente web. Proporciona un mecanismo de fallback utilizando RabbitMQ, en caso de que un microservicio no esté disponible.
- Microservicio de Productos: Gestiona la información de los productos (nombre, descripción, precio, stock, etc.).
- Microservicio de Inventario: Maneja la verificación y actualización del stock de productos.
- Microservicio de Órdenes: Verifica la disponibilidad de inventario a través del Microservicio de Inventario.
- MongoDB (persistencia): Base de datos NoSQL utilizada para almacenar los datos de productos, inventarios y órdenes.
- RabbitMQ (MOM): Utilizado para la gestión de solicitudes encoladas cuando un microservicio no está disponible.

#### 2.2 Arquitectura

![Diagrama de arquitectura](https://github.com/user-attachments/assets/9afcbdde-2c7a-4b37-b908-683bfa4eb92a)

- Los microservicios se comunican entre sí por gRPC
- RabbitMQ se usa como mecanismo de recuperación ante fallos (failover)
- MongoDB es la base de datos por microservicio
- Docker Swarm permite escalar los servicios horizontalmente y manejar la red interna

#### 2.3 Patrones de diseño

- **Microservicios:** Cada servicio representa un dominio independiente.
- **API Gateway:** Punto único de entrada para clientes, con traducción REST → gRPC.
- **Proxy:** El Gateway actúa como proxy que abstrae a los clientes del backend real.
- **DTO (Protobuf):** Contratos compartidos de datos entre servicios, desacoplando internamente los modelos.
- **Request/Reply Pattern:** Comunicación síncrona entre servicios vía gRPC.
- **Pub/Sub con RabbitMQ:** Desacoplamiento y resiliencia ante fallos.
- **Failover Messaging:** Mensajes encolados se reintentan si los servicios fallan temporalmente.

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
| Frontend             | Next.js (React)    | 15.2.4                |
| API Gateway          | FastAPI (Python)   | 0.110.0               |
| gRPC                 | grpcio (Python)    | 1.62.0                |
| Microservicios       | Python             | 3.10                  |
| Comunicación gRPC    | Protocol Buffers   | 3.21.12               |
| Bases de datos       | MongoDB            | 3.3.2                 |
| Middleware (MOM)     | RabbitMQ           | 4.x (Management UI)   |
| Orquestación         | Docker Swarm       | Docker 24.0.5         |
| Contenedores         | Docker Engine      | 24.0.5                |
| Monitoreo            | Loki, Promtail, Grafana | 2.9.2, 2.9.2, latest |

#### 3.2 Cómo compilar y ejecutar el proyecto

Clonar el repositorio en el equipo local.

```bash
git clone https://github.com/alejoriosm04/rpc-mom-comm.git
```

El proyecto puede ejecutarse directamente con Docker Compose o Docker Swarm.

##### Requisitos previos

- Tener instalado Docker, Docker Compose y Docker Swarm.
- El proyecto se puede ejecutar localmente o en un servidor remoto, tanto en un entorno Linux como en Windows.

##### Configurar variables de entorno

Para configurar las variables de entorno, se debe crear un archivo `.env` en la raíz de cada proyecto (ecommerce-app, api-gateway, microservices) y copiar el contenido del archivo `.env.example` en él.

```bash
cp .env.example .env
cp .env.example .env.local # Únicamente para el proyecto ecommerce-app
```

Luego, reemplazar las variables comentadas con los valores actuales compartidos con el equipo.

```bash
nano .env
```

> Ctrl + X, Y, Enter para guardar y salir.

**Nota:** La variable de entorno `NEXT_PUBLIC_API_KEY` y `NEXT_PUBLIC_WS_URL` en el proyecto *ecommerce-app*, deben ser reemplazadas por:

- `localhost` si se ejecuta el proyecto localmente.

    ```bash
    NEXT_PUBLIC_API_URL=http://localhost:8000/api
    NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
    ```

- `<IP-ADDRESS>` si se ejecuta el proyecto en un servidor remoto.

    ```bash
    NEXT_PUBLIC_API_URL=http://<IP-ADDRESS>:8000/api
    NEXT_PUBLIC_WS_URL=ws://<IP-ADDRESS>:8000/ws
    ```

    Así mismo, deberá agregar el IP-ADDRESS a la lista de permitidos en el archivo `app.py` de la API Gateway.

    ```python
    allow_origins=["http://localhost:3000", "http://<IP-ADDRESS>:3000"]
    ```

    > ⚠️ **Nota:** En nuestro caso, el IP-ADDRESS es `34.238.228.250`.

##### Despliegue completo del sistema

Para desplegar el proyecto en un entorno local o remoto que no simule alta disponibilidad, se debe ejecutar el archivo `docker-compose.yml` que se encuentra en la raíz del proyecto. De esta forma, se levantan todos los servicios necesarios para que el proyecto funcione.

```bash
docker-compose up -d --build
```

Si desea simular una **alta disponibilidad**, se debe ejecutar el archivo `deploy.sh` que se encuentra en la raíz del proyecto. De esta forma, se levantan todos los servicios necesarios para que el proyecto funcione, pero con la diferencia de que se levantan $n$ instancias de cada servicio, simulando una arquitectura de microservicios con alta disponibilidad.

```bash
docker swarm init
./deploy.sh   # para desplegar el proyecto
docker service ls   # para verificar que se han creado los servicios
docker stack rm ecommerce-app   # para eliminar los servicios
```

---

#### 3.3 Detalles del desarrollo

##### Características testeadas

###### ✅ Real-time Orders (WebSocket)

- Los pedidos muestran un mensaje como `"Su pedido ha sido confirmado"` o `"En cola"` en tiempo real.
- Si el `order_service` está inactivo, la solicitud se encola y se notifica al cliente.
- Cuando el `order_service` vuelve, el pedido se procesa y el cliente es notificado a través de WebSocket.

###### ✅ Real-time Product Updates

- El sistema escucha `/push/products` a través de WebSocket.
- Cuando los productos se actualizan (cambios de stock), la UI los refleja automáticamente.

###### 🔐 Protección de Clave API

Todas las rutas protegidas requieren el siguiente encabezado:

```
x-api-key: <supersecretkey>
```

Esto se aplica a:

- `/api/products/`
- `/api/orders/`
- `/api/inventory/check`

###### 🧪 Prueba de Fallo

1. Detener un microservicio (por ejemplo, `order_service`).
2. Realizar una solicitud (por ejemplo, Añadir al carrito).
3. Verás un mensaje como: `Pedido en cola. Esperando confirmación...`
4. Iniciar `order_service` de nuevo:
   ```bash
   docker-compose up -d order_service
   ```
5. El cliente recibirá confirmación en tiempo real a través de WebSocket.

#### 3.4 Estructura del proyecto

```
.
├── analytics/
│   ├── grafana/
│   └── promtail/
├── api-gateway/                 # FastAPI Gateway (gRPC + WebSocket + queue fallback)
├── ecommerce-app/              # Next.js Client (REST consumer)
├── microservices/
│   ├── product_service/
│   ├── inventory_service/
│   └── order_service/
├── deploy.sh
├── docker-compose.yml
├── docker-stack.yml
└── README.md
```
#### 3.5 Descripción de los componentes

##### Cliente Web (ecommerce-app)

Implementado en Next.js, proporciona una interfaz moderna y reactiva.

- Visualización de productos.
- Gestión interactiva de las compras a realizar.
- Proceso decreación de órdenes.
- Visualización del estado de órdenes en tiempo real.
- Actualizaciones automáticas de stock mediante WebSockets.

Características técnicas:
- Consume APIs REST del Gateway.
- Mantiene conexión WebSocket para actualizaciones en tiempo real.
- Implementa autenticación mediante API key.
- Diseño responsivo para diferentes dispositivos.
- Se actualiza de manera dinámica ante la perdída o recuperación de un microservicio

##### API Gateway

Implementado en FastAPI, actúa como el punto central de entrada.

- Traducción de peticiones REST a llamadas gRPC.
- Manejo de autenticación y autorización.
- Implementación de mecanismo de fallback.
- Gestión de WebSockets para actualizaciones en tiempo real.

Características técnicas:
- Validación de API keys.
- Manejo de CORS.
- Implementación de circuit breaker para fallos.
- Enrutamiento inteligente de peticiones.

##### Microservicio de Productos

Implementado en Python, gestiona el catálogo de productos.

- Lectura y listado de productos
- Gestión de categorías
- Validación de fuentes URL para imágenes

Características técnicas:
- Almacenamiento en MongoDB.
- Exposición de servicios vía gRPC.
- Validación de esquemas de datos.
- Modelos de respuesta y de solicitud
- Sistema de reintentos para fallos.

##### Microservicio de Inventario

Implementado en Python, gestiona el stock de productos.

- Verificación de disponibilidad.
- Actualización de inventario.
- Manejo y movimientos del stock.

Características técnicas:
- Gestión de cambios de stock.
- Integración con el servicio de órdenes.
- Manejo de reservas de stock.
- Comunicación grpc con microservicios
- Sistema de reintentos para fallos.

##### Microservicio de Órdenes

Implementado en Python, procesa las órdenes de compra.

- Creación y gestión de órdenes.
- Verificación de disponibilidad de stock.
- Notificación de estados de órdenes.

Características técnicas:
  - Manejo de estados de órdenes.
  - Integración con servicios de inventario.
  - Sistema de reintentos para fallos.

##### MongoDB

Base de datos NoSQL principal del sistema.

- Almacenamiento persistente de datos.
- Replicación para alta disponibilidad.
- Indexación para búsquedas eficientes.
- Transacciones ACID.
- Esquemas flexibles.
- Agregaciones complejas.
- Replicación de datos.
- Backup automático.

##### RabbitMQ

Sistema de mensajería para fallback y comunicación asíncrona.

- Colas de mensajes para fallback.
- Publicación/suscripción para eventos.
- Persistencia de mensajes.
- Reintentos automáticos.

Características técnicas:
- Exchange de mensajes.
- Colas durables.
- Confirmaciones de entrega.
- Dead letter queues.
- Cada microservicio tiene su respectiva cola para la cual realiza su procedimiento de recuperación en caso de que se "caiga" el respectivo servicio. Para el caso de order, por ejemplo, si se realizan múltiples ordenes con el microservicio apagado, estás seran encoladas y procesadas cuando el servicio esté disponible nuevamente (y notificadas por medio de logs desde el backend y por medio de pop-ups en el frontend)

##### Sistema de Monitoreo

Implementado con Loki, Promtail y Grafana.

- Recolección centralizada de logs.
- Visualización de métricas en tiempo real.
- Alertas automáticas.
- Dashboards personalizados.

Características técnicas:
- Agregación de logs.
- Análisis de patrones.
- Visualización de métricas.
- Configuración de alertas.

#### 3.6 Resultados y pantallazos

![image](https://github.com/user-attachments/assets/a7525902-a612-4022-b353-2b3caaf4b372)
![image](https://github.com/user-attachments/assets/461e7b2d-bf76-48f4-bc41-3db5cf5ac1bf)
![image](https://github.com/user-attachments/assets/178f3b92-ecd5-47dd-a508-5b4dfc4c12e8)
![image](https://github.com/user-attachments/assets/ab28516b-a72d-4ede-bbbd-2bf17d4409a3)
![image](https://github.com/user-attachments/assets/a369957b-4131-4300-a978-c49bfce372e5)
![image](https://github.com/user-attachments/assets/4122fd45-1162-453e-a9c9-96e06d4ccda7)
![image](https://github.com/user-attachments/assets/cebbb9c4-da87-4ebc-8b9e-f3df39a4fc6e)

### 4. Descripción del ambiente de ejecución (Producción)

#### 4.1 Despliegue

Para más información sobre el despliegue en producción en una instancia EC2 de AWS, ver el archivo [DEPLOYMENT.md](https://github.com/alejoriosm04/rpc-mom-comm/blob/main/docs/DEPLOYMENT.md). Aquí se describe paso a paso el despliegue del proyecto en una instancia EC2 de AWS.

#### 4.2 IP o nombre de dominio del servidor

- Acceso frontend: `http://<TU_IP_PUBLICA>:3000`
- Acceso API Gateway: `http://<TU_IP_PUBLICA>:8000/docs`
- Acceso RabbitMQ: `http://<TU_IP_PUBLICA>:15672`
- Accesso Logs Grafana: `http://<TU_IP_PUBLICA>:3001`


#### 4.3 Mini guía para el usuario final 

Aquí se describe cómo interactuar con el proyecto en el frontend:

1. Ingresar a la IP indicada, allí encontrará la página inicial o Home
![image](https://github.com/user-attachments/assets/c9d2f17e-f73d-459b-98c4-d32f30e81d64)

2. Ingresar a la sección "Products", allí encontrará los productos disponibles dentro del E-Commerce 
![image](https://github.com/user-attachments/assets/279f5a01-c343-45bc-b5e1-cc4fc79936e4)

3. Cuando ingresa a esta sección, seleccione la cantidad de producto que desea (por defecto 1), luego debe clickear la opción "Add to Cart" para simular la compra de un producto y visualizar en tiempo real cómo el stock disminuye.
   
![image](https://github.com/user-attachments/assets/a5297364-9763-41dd-8c12-af6a171996f9)

5. Si quiere probar el mecanismo de failover, conéctese a la instancia y apague el servicio de productos, verá que si intenta refrescar la página no aparecerá ningún producto. Después de unos segundos, inicie la instancia de nuevo y automáticamente, sin refrescar la página, usted verá como el E-commerce le muestra los productos nuevamente. Realice el mismo procedimiento para el servicio de orden y verá cómo el sistema intenta procesar la orden, pero dado que no está disponible, le notifica a usted, active el microservicio nuevamente y verá cómo en tiempo real la página le muestra un anuncio diciendo que su orden fue procesada.

   ![image](https://github.com/user-attachments/assets/154ddb65-eccf-45ea-b18d-751543dca33e)
   ![image](https://github.com/user-attachments/assets/1053253f-c319-4d4c-86cb-c3cc01e96451)
   
### Referencias

A continuación se listan las referencias utilizadas para el desarrollo del proyecto, incluyendo documentación oficial, tutoriales, videos, artículos y fragmentos de código reutilizados:

- 🔗 [mega-grpc – flop-code](https://github.com/flop-code/mega-grpc): Arquitectura completa con gRPC, múltiples microservicios y herramientas de monitoreo.
- 🔗 [fastapi-grpc-sample – odh1995](https://github.com/odh1995/fastapi-grpc-sample): Ejemplo de integración entre FastAPI y gRPC usando proto.
- 🔗 [api-gateway-grpc-microservice – hemicharly](https://github.com/hemicharly/api-gateway-grpc-microservice): Implementación de microservicios con API Gateway usando gRPC.
- 📹 [Video explicativo sobre gRPC y microservicios (YouTube)](https://www.youtube.com/watch?v=p23J6NTDhEk): Introducción clara sobre cómo funciona gRPC con ejemplos visuales.
- 📘 [FastAPI Websockets (Documentación oficial)](https://fastapi.tiangolo.com/advanced/websockets/): Guía avanzada para implementar WebSockets con FastAPI.
- 🛠️ [Cursor AI](https://www.cursor.com/): Plataforma de desarrollo asistido con IA, ideal para trabajo colaborativo y debugging.
- 🤖 [ChatGPT](https://chatgpt.com/): Asistente conversacional utilizado para ideación, redacción y soporte técnico en este proyecto.
- 📊 Diapositivas de clase - *Tópicos Especiales en Telemática ST0263*: Material académico de referencia utilizado durante el desarrollo del proyecto.
