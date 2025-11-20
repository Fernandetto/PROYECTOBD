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

### 4. Opción B: Ejecutar con Docker Compose

```bash
# Construir y ejecutar
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

## Endpoints de la API

Una vez que la aplicación esté ejecutándose, puedes acceder a:

- **Documentación Swagger**: `http://localhost:8000/docs`
- **Documentación ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

### Endpoints principales

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

## Despliegue en Azure

### Método 1: Script automatizado (Recomendado)

#### Para Linux/Mac:

```bash
cd deploy
chmod +x azure-deploy.sh
./azure-deploy.sh
```

#### Para Windows (PowerShell):

```powershell
cd deploy
.\azure-deploy.ps1
```

El script te pedirá las credenciales de la base de datos y realizará:
1. Crear Resource Group
2. Crear Azure Container Registry
3. Construir y subir imagen Docker
4. Crear App Service Plan
5. Crear Web App
6. Configurar variables de entorno
7. Habilitar despliegue continuo
8. Reiniciar la aplicación

### Método 2: Comandos manuales paso a paso

```bash
# Variables de configuración
RESOURCE_GROUP="restaurant-api-rg"
LOCATION="eastus"
ACR_NAME="restaurantapiacr"
APP_SERVICE_PLAN="restaurant-api-plan"
WEB_APP_NAME="restaurant-api-app"

# 1. Crear Resource Group
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION

# 2. Crear Azure Container Registry
az acr create \
    --resource-group $RESOURCE_GROUP \
    --name $ACR_NAME \
    --sku Basic \
    --admin-enabled true

# 3. Construir y subir imagen Docker
az acr build \
    --registry $ACR_NAME \
    --image restaurant-api:latest \
    --file Dockerfile \
    .

# 4. Crear App Service Plan
az appservice plan create \
    --name $APP_SERVICE_PLAN \
    --resource-group $RESOURCE_GROUP \
    --is-linux \
    --sku B1

# 5. Crear Web App
az webapp create \
    --resource-group $RESOURCE_GROUP \
    --plan $APP_SERVICE_PLAN \
    --name $WEB_APP_NAME \
    --deployment-container-image-name $ACR_NAME.azurecr.io/restaurant-api:latest

# 6. Configurar credenciales ACR
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)
az webapp config container set \
    --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --docker-custom-image-name $ACR_NAME.azurecr.io/restaurant-api:latest \
    --docker-registry-server-url https://$ACR_NAME.azurecr.io \
    --docker-registry-server-user $ACR_NAME \
    --docker-registry-server-password $ACR_PASSWORD

# 7. Configurar variables de entorno
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --settings \
        DB_SERVER="your-server.database.windows.net" \
        DB_NAME="your-database" \
        DB_USER="your-user" \
        DB_PASSWORD="your-password" \
        DB_DRIVER="ODBC Driver 17 for SQL Server" \
        WEBSITES_PORT="8000" \
        CORS_ORIGINS="*"

# 8. Reiniciar Web App
az webapp restart \
    --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP
```

### Actualizar la aplicación desplegada

Para actualizar una aplicación ya desplegada con cambios nuevos:

```bash
cd deploy
./azure-update.sh
```

Esto construirá una nueva imagen y reiniciará la Web App.

## Validaciones Implementadas

La API incluye las siguientes validaciones de negocio:

1. **Productos**:
   - El precio debe ser >= 0
   - Solo productos activos pueden agregarse a órdenes

2. **Mesas**:
   - La capacidad debe ser > 0
   - El estado debe ser: Libre, Ocupada, o Reservada

3. **Detalles de Orden**:
   - La cantidad debe ser > 0
   - El precio unitario debe ser >= 0
   - El subtotal se calcula automáticamente

4. **Órdenes**:
   - Al crear detalles, el total de la orden se actualiza automáticamente
   - Al cerrar una orden, se calcula el total final
   - Se valida que mesa y mesero existan

## Testing de la API

### Usando curl

```bash
# Health check
curl http://localhost:8000/health

# Crear una categoría
curl -X POST http://localhost:8000/api/v1/categorias \
  -H "Content-Type: application/json" \
  -d '{"Nombre": "Bebidas", "Descripcion": "Bebidas variadas"}'

# Listar categorías
curl http://localhost:8000/api/v1/categorias
```

### Usando Postman o Thunder Client

Importa la documentación OpenAPI desde `http://localhost:8000/openapi.json`

## Troubleshooting

### Error de conexión a la base de datos

- Verifica que las credenciales en `.env` sean correctas
- Asegúrate de que el servidor Azure SQL permita conexiones desde tu IP
- Verifica que el driver ODBC esté instalado correctamente

### Error al construir imagen Docker

- Asegúrate de que Docker esté ejecutándose
- Verifica que tienes suficiente espacio en disco
- Si estás en Windows, asegúrate de usar contenedores Linux

### La API no responde en Azure

- Verifica los logs: `az webapp log tail --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP`
- Verifica que las variables de entorno estén configuradas correctamente
- Revisa el health check endpoint

## Licencia

Este proyecto es parte de un proyecto académico/empresarial.

## Autor

Desarrollado para el sistema de gestión de restaurante.
