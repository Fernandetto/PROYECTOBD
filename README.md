# Restaurant Management API

API REST completa para sistema de gestión de restaurante construida con FastAPI y Azure SQL Database.

## Descripción

Esta API proporciona endpoints CRUD completos para gestionar un restaurante, incluyendo:
- Categorías de menú
- Meseros
- Mesas
- Productos del menú
- Órdenes
- Detalles de órdenes

## Características

- ✅ **FastAPI** - Framework moderno y rápido para construir APIs
- ✅ **SQLAlchemy** - ORM para interacción con base de datos
- ✅ **Pydantic** - Validación de datos robusta
- ✅ **Azure SQL Database** - Base de datos en la nube
- ✅ **Docker** - Contenedorización con multi-stage build
- ✅ **Azure Container Registry** - Registro de imágenes Docker
- ✅ **Azure Web App** - Despliegue en la nube
- ✅ **CORS** - Configuración de CORS
- ✅ **Health Check** - Endpoint de verificación de salud
- ✅ **Documentación automática** - Swagger/OpenAPI
- ✅ **Logging** - Sistema de registro de eventos
- ✅ **Validaciones** - Validaciones de negocio (productos activos, cálculo de totales, etc.)

## Estructura del Proyecto

```
PROYECTOBD/
├── app/
│   ├── main.py              # Aplicación principal FastAPI
│   ├── database.py          # Configuración de base de datos
│   ├── models.py            # Modelos SQLAlchemy
│   ├── schemas.py           # Esquemas Pydantic
│   ├── crud.py              # Operaciones CRUD
│   ├── requirements.txt     # Dependencias Python
│   └── routes/              # Endpoints de la API
│       ├── categorias.py
│       ├── meseros.py
│       ├── mesas.py
│       ├── menu_productos.py
│       ├── ordenes.py
│       └── detalles_orden.py
├── deploy/                  # Scripts de despliegue
│   ├── azure-deploy.sh      # Script de despliegue (Bash)
│   ├── azure-deploy.ps1     # Script de despliegue (PowerShell)
│   └── azure-update.sh      # Script de actualización
├── BD1.sql                  # Esquema de base de datos
├── Dockerfile               # Multi-stage Docker build
├── docker-compose.yml       # Docker Compose para desarrollo
├── .env.example             # Ejemplo de variables de entorno
├── .gitignore              # Archivos ignorados por Git
└── README.md               # Este archivo
```

## Requisitos Previos

- Python 3.11+
- Docker y Docker Compose
- Azure CLI (para despliegue)
- Azure SQL Database (con esquema restaurante)
- ODBC Driver 17 for SQL Server

## Instalación y Desarrollo Local

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd PROYECTOBD
```

### 2. Configurar variables de entorno

Crear un archivo `.env` basado en `.env.example`:

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales de Azure SQL:

```env
DB_SERVER=your-server.database.windows.net
DB_NAME=your-database-name
DB_USER=your-username
DB_PASSWORD=your-password
DB_DRIVER=ODBC Driver 17 for SQL Server
PORT=8000
CORS_ORIGINS=*
DEBUG=true
RELOAD=true
SQL_ECHO=false
```

### 3. Opción A: Ejecutar con Python (desarrollo)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
cd app
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

La API estará disponible en `http://localhost:8000`

#### Categorías
- `GET /api/v1/categorias` - Listar todas las categorías
- `GET /api/v1/categorias/{id}` - Obtener una categoría
- `POST /api/v1/categorias` - Crear una categoría
- `PUT /api/v1/categorias/{id}` - Actualizar una categoría
- `DELETE /api/v1/categorias/{id}` - Eliminar una categoría

#### Meseros
- `GET /api/v1/meseros` - Listar todos los meseros
- `GET /api/v1/meseros/{id}` - Obtener un mesero
- `POST /api/v1/meseros` - Crear un mesero
- `PUT /api/v1/meseros/{id}` - Actualizar un mesero
- `DELETE /api/v1/meseros/{id}` - Eliminar un mesero

#### Mesas
- `GET /api/v1/mesas` - Listar todas las mesas (filtrar por estado)
- `GET /api/v1/mesas/{id}` - Obtener una mesa
- `POST /api/v1/mesas` - Crear una mesa
- `PUT /api/v1/mesas/{id}` - Actualizar una mesa
- `DELETE /api/v1/mesas/{id}` - Eliminar una mesa

#### Productos del Menú
- `GET /api/v1/menu-productos` - Listar productos (filtrar por categoría/activo)
- `GET /api/v1/menu-productos/{id}` - Obtener un producto
- `POST /api/v1/menu-productos` - Crear un producto
- `PUT /api/v1/menu-productos/{id}` - Actualizar un producto
- `DELETE /api/v1/menu-productos/{id}` - Eliminar un producto

#### Órdenes
- `GET /api/v1/ordenes` - Listar órdenes (filtrar por mesa/estado)
- `GET /api/v1/ordenes/{id}` - Obtener una orden con detalles
- `POST /api/v1/ordenes` - Crear una orden (con detalles opcionales)
- `PUT /api/v1/ordenes/{id}` - Actualizar una orden
- `POST /api/v1/ordenes/{id}/cerrar` - Cerrar una orden (calcula total)
- `DELETE /api/v1/ordenes/{id}` - Eliminar una orden

#### Detalles de Orden
- `GET /api/v1/detalles-orden/orden/{orden_id}` - Listar detalles de una orden
- `GET /api/v1/detalles-orden/{id}` - Obtener un detalle
- `POST /api/v1/detalles-orden` - Crear un detalle (actualiza total automáticamente)
- `PUT /api/v1/detalles-orden/{id}` - Actualizar un detalle
- `DELETE /api/v1/detalles-orden/{id}` - Eliminar un detalle
