# DOCUMENTACIÓN API REST - SISTEMA DE GESTIÓN DE RESTAURANTE

**Versión:** 1.0.0
**Base URL:** `https://restaurant-api-app.azurewebsites.net/api/v1`
**Documentación Interactiva:** `/docs`

---

## TABLA DE CONTENIDOS

1. [Información General](#información-general)
2. [Autenticación](#autenticación)
3. [Endpoints - Categorías](#endpoints---categorías)
4. [Endpoints - Meseros](#endpoints---meseros)
5. [Endpoints - Mesas](#endpoints---mesas)
6. [Endpoints - Productos del Menú](#endpoints---productos-del-menú)
7. [Endpoints - Órdenes](#endpoints---órdenes)
8. [Endpoints - Detalles de Orden](#endpoints---detalles-de-orden)
9. [Códigos de Estado HTTP](#códigos-de-estado-http)
10. [Ejemplos de Uso](#ejemplos-de-uso)

---

## INFORMACIÓN GENERAL

Esta API REST proporciona acceso completo a todas las funcionalidades del sistema de gestión de restaurante. Todos los endpoints devuelven respuestas en formato JSON.

### Headers Requeridos

```
Content-Type: application/json
Accept: application/json
```

### Formato de Respuestas de Error

```json
{
  "detail": "Descripción del error"
}
```

---

## AUTENTICACIÓN

**Versión Actual:** No requiere autenticación (configurar según necesidades de producción)

---

## ENDPOINTS - CATEGORÍAS

### 1. Listar Todas las Categorías

**URI:** `/api/v1/categorias`
**Método HTTP:** `GET`
**Descripción:** Obtiene una lista paginada de todas las categorías de productos.

**Query Parameters:**
| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| skip | integer | No | 0 | Número de registros a omitir |
| limit | integer | No | 100 | Número máximo de registros a devolver |

**Payload:** No requiere

**Response 200 (Success):**
```json
[
  {
    "CategoriaId": 1,
    "Nombre": "Entradas",
    "Descripcion": "Entradas frías y calientes"
  },
  {
    "CategoriaId": 2,
    "Nombre": "Platos Fuertes",
    "Descripcion": "Platos principales"
  }
]
```

---

### 2. Obtener una Categoría por ID

**URI:** `/api/v1/categorias/{categoria_id}`
**Método HTTP:** `GET`
**Descripción:** Obtiene los detalles de una categoría específica.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| categoria_id | integer | ID de la categoría |

**Payload:** No requiere

**Response 200 (Success):**
```json
{
  "CategoriaId": 1,
  "Nombre": "Entradas",
  "Descripcion": "Entradas frías y calientes"
}
```

**Response 404 (Not Found):**
```json
{
  "detail": "Categoría con ID 1 no encontrada"
}
```

---

### 3. Crear una Categoría

**URI:** `/api/v1/categorias`
**Método HTTP:** `POST`
**Descripción:** Crea una nueva categoría de productos.

**Payload:**
```json
{
  "Nombre": "Postres",
  "Descripcion": "Postres variados"
}
```

**Validaciones:**
- `Nombre`: Requerido, máximo 100 caracteres, único
- `Descripcion`: Opcional, máximo 250 caracteres

**Response 201 (Created):**
```json
{
  "CategoriaId": 4,
  "Nombre": "Postres",
  "Descripcion": "Postres variados"
}
```

**Response 400 (Bad Request):**
```json
{
  "detail": "Ya existe una categoría con ese nombre"
}
```

---

### 4. Actualizar una Categoría

**URI:** `/api/v1/categorias/{categoria_id}`
**Método HTTP:** `PUT`
**Descripción:** Actualiza los datos de una categoría existente.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| categoria_id | integer | ID de la categoría |

**Payload:**
```json
{
  "Nombre": "Postres Premium",
  "Descripcion": "Postres gourmet y especialidades"
}
```

**Validaciones:**
- Todos los campos son opcionales
- `Nombre`: Máximo 100 caracteres, único
- `Descripcion`: Máximo 250 caracteres

**Response 200 (Success):**
```json
{
  "CategoriaId": 4,
  "Nombre": "Postres Premium",
  "Descripcion": "Postres gourmet y especialidades"
}
```

**Response 404 (Not Found):**
```json
{
  "detail": "Categoría con ID 4 no encontrada"
}
```

---

### 5. Eliminar una Categoría

**URI:** `/api/v1/categorias/{categoria_id}`
**Método HTTP:** `DELETE`
**Descripción:** Elimina una categoría del sistema.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| categoria_id | integer | ID de la categoría |

**Payload:** No requiere

**Response 200 (Success):**
```json
{
  "message": "Categoría Postres eliminada exitosamente"
}
```

**Response 400 (Bad Request):**
```json
{
  "detail": "No se puede eliminar la categoría porque tiene productos asociados"
}
```

**Response 404 (Not Found):**
```json
{
  "detail": "Categoría con ID 4 no encontrada"
}
```

---

## ENDPOINTS - MESEROS

### 1. Listar Todos los Meseros

**URI:** `/api/v1/meseros`
**Método HTTP:** `GET`
**Descripción:** Obtiene una lista paginada de todos los meseros.

**Query Parameters:**
| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| skip | integer | No | 0 | Número de registros a omitir |
| limit | integer | No | 100 | Número máximo de registros a devolver |

**Payload:** No requiere

**Response 200 (Success):**
```json
[
  {
    "MeseroId": 1,
    "Nombre": "Carlos Pérez",
    "Telefono": "+50412345678",
    "Email": "carlos@restaurante.example",
    "FechaIngreso": "2024-01-15"
  },
  {
    "MeseroId": 2,
    "Nombre": "María López",
    "Telefono": "+50487654321",
    "Email": "maria@restaurante.example",
    "FechaIngreso": "2024-02-01"
  }
]
```

---

### 2. Obtener un Mesero por ID

**URI:** `/api/v1/meseros/{mesero_id}`
**Método HTTP:** `GET`
**Descripción:** Obtiene los detalles de un mesero específico.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| mesero_id | integer | ID del mesero |

**Payload:** No requiere

**Response 200 (Success):**
```json
{
  "MeseroId": 1,
  "Nombre": "Carlos Pérez",
  "Telefono": "+50412345678",
  "Email": "carlos@restaurante.example",
  "FechaIngreso": "2024-01-15"
}
```

---

### 3. Crear un Mesero

**URI:** `/api/v1/meseros`
**Método HTTP:** `POST`
**Descripción:** Registra un nuevo mesero en el sistema.

**Payload:**
```json
{
  "Nombre": "Juan García",
  "Telefono": "+50499887766",
  "Email": "juan@restaurante.example",
  "FechaIngreso": "2024-11-19"
}
```

**Validaciones:**
- `Nombre`: Requerido, máximo 150 caracteres
- `Telefono`: Opcional, máximo 20 caracteres
- `Email`: Opcional, máximo 150 caracteres
- `FechaIngreso`: Opcional (default: fecha actual)

**Response 201 (Created):**
```json
{
  "MeseroId": 3,
  "Nombre": "Juan García",
  "Telefono": "+50499887766",
  "Email": "juan@restaurante.example",
  "FechaIngreso": "2024-11-19"
}
```

---

### 4. Actualizar un Mesero

**URI:** `/api/v1/meseros/{mesero_id}`
**Método HTTP:** `PUT`
**Descripción:** Actualiza los datos de un mesero existente.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| mesero_id | integer | ID del mesero |

**Payload:**
```json
{
  "Telefono": "+50499887700",
  "Email": "juan.garcia@restaurante.example"
}
```

**Response 200 (Success):**
```json
{
  "MeseroId": 3,
  "Nombre": "Juan García",
  "Telefono": "+50499887700",
  "Email": "juan.garcia@restaurante.example",
  "FechaIngreso": "2024-11-19"
}
```

---

### 5. Eliminar un Mesero

**URI:** `/api/v1/meseros/{mesero_id}`
**Método HTTP:** `DELETE`
**Descripción:** Elimina un mesero del sistema.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| mesero_id | integer | ID del mesero |

**Payload:** No requiere

**Response 200 (Success):**
```json
{
  "message": "Mesero Juan García eliminado exitosamente"
}
```

**Response 400 (Bad Request):**
```json
{
  "detail": "No se puede eliminar el mesero porque tiene órdenes asociadas"
}
```

---

## ENDPOINTS - MESAS

### 1. Listar Todas las Mesas

**URI:** `/api/v1/mesas`
**Método HTTP:** `GET`
**Descripción:** Obtiene una lista paginada de todas las mesas, con opción de filtrar por estado.

**Query Parameters:**
| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| skip | integer | No | 0 | Número de registros a omitir |
| limit | integer | No | 100 | Número máximo de registros a devolver |
| estado | string | No | null | Filtrar por estado (Libre, Ocupada, Reservada) |

**Payload:** No requiere

**Response 200 (Success):**
```json
[
  {
    "MesaId": 1,
    "Numero": 1,
    "Capacidad": 4,
    "Estado": "Libre"
  },
  {
    "MesaId": 2,
    "Numero": 2,
    "Capacidad": 2,
    "Estado": "Ocupada"
  }
]
```

---

### 2. Obtener una Mesa por ID

**URI:** `/api/v1/mesas/{mesa_id}`
**Método HTTP:** `GET`
**Descripción:** Obtiene los detalles de una mesa específica.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| mesa_id | integer | ID de la mesa |

**Payload:** No requiere

**Response 200 (Success):**
```json
{
  "MesaId": 1,
  "Numero": 1,
  "Capacidad": 4,
  "Estado": "Libre"
}
```

---

### 3. Crear una Mesa

**URI:** `/api/v1/mesas`
**Método HTTP:** `POST`
**Descripción:** Registra una nueva mesa en el sistema.

**Payload:**
```json
{
  "Numero": 10,
  "Capacidad": 6,
  "Estado": "Libre"
}
```

**Validaciones:**
- `Numero`: Requerido, único
- `Capacidad`: Requerido, debe ser > 0
- `Estado`: Default "Libre", valores permitidos: Libre, Ocupada, Reservada

**Response 201 (Created):**
```json
{
  "MesaId": 10,
  "Numero": 10,
  "Capacidad": 6,
  "Estado": "Libre"
}
```

**Response 400 (Bad Request):**
```json
{
  "detail": "Ya existe una mesa con ese número"
}
```

---

### 4. Actualizar una Mesa

**URI:** `/api/v1/mesas/{mesa_id}`
**Método HTTP:** `PUT`
**Descripción:** Actualiza los datos de una mesa existente.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| mesa_id | integer | ID de la mesa |

**Payload:**
```json
{
  "Estado": "Ocupada"
}
```

**Response 200 (Success):**
```json
{
  "MesaId": 10,
  "Numero": 10,
  "Capacidad": 6,
  "Estado": "Ocupada"
}
```

---

### 5. Eliminar una Mesa

**URI:** `/api/v1/mesas/{mesa_id}`
**Método HTTP:** `DELETE`
**Descripción:** Elimina una mesa del sistema.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| mesa_id | integer | ID de la mesa |

**Payload:** No requiere

**Response 200 (Success):**
```json
{
  "message": "Mesa 10 eliminada exitosamente"
}
```

---

## ENDPOINTS - PRODUCTOS DEL MENÚ

### 1. Listar Todos los Productos

**URI:** `/api/v1/menu-productos`
**Método HTTP:** `GET`
**Descripción:** Obtiene una lista paginada de todos los productos del menú, con opciones de filtrado.

**Query Parameters:**
| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| skip | integer | No | 0 | Número de registros a omitir |
| limit | integer | No | 100 | Número máximo de registros a devolver |
| categoria_id | integer | No | null | Filtrar por categoría |
| activo | boolean | No | null | Filtrar por estado activo/inactivo |

**Payload:** No requiere

**Response 200 (Success):**
```json
[
  {
    "ProductoId": 1,
    "Nombre": "Sopa del Día",
    "Descripcion": "Sopa casera",
    "Precio": 55.00,
    "CategoriaId": 1,
    "Activo": true
  },
  {
    "ProductoId": 2,
    "Nombre": "Hamburguesa Clásica",
    "Descripcion": "Carne de res 200g",
    "Precio": 120.00,
    "CategoriaId": 2,
    "Activo": true
  }
]
```

---

### 2. Obtener un Producto por ID

**URI:** `/api/v1/menu-productos/{producto_id}`
**Método HTTP:** `GET`
**Descripción:** Obtiene los detalles de un producto específico.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| producto_id | integer | ID del producto |

**Payload:** No requiere

**Response 200 (Success):**
```json
{
  "ProductoId": 1,
  "Nombre": "Sopa del Día",
  "Descripcion": "Sopa casera",
  "Precio": 55.00,
  "CategoriaId": 1,
  "Activo": true
}
```

---

### 3. Crear un Producto

**URI:** `/api/v1/menu-productos`
**Método HTTP:** `POST`
**Descripción:** Registra un nuevo producto en el menú.

**Payload:**
```json
{
  "Nombre": "Pizza Margarita",
  "Descripcion": "Pizza con tomate, mozzarella y albahaca",
  "Precio": 150.00,
  "CategoriaId": 2,
  "Activo": true
}
```

**Validaciones:**
- `Nombre`: Requerido, máximo 200 caracteres
- `Descripcion`: Opcional, máximo 500 caracteres
- `Precio`: Requerido, debe ser >= 0, con 2 decimales
- `CategoriaId`: Requerido, debe existir
- `Activo`: Default true

**Response 201 (Created):**
```json
{
  "ProductoId": 4,
  "Nombre": "Pizza Margarita",
  "Descripcion": "Pizza con tomate, mozzarella y albahaca",
  "Precio": 150.00,
  "CategoriaId": 2,
  "Activo": true
}
```

**Response 400 (Bad Request):**
```json
{
  "detail": "Categoría con ID 99 no existe"
}
```

---

### 4. Actualizar un Producto

**URI:** `/api/v1/menu-productos/{producto_id}`
**Método HTTP:** `PUT`
**Descripción:** Actualiza los datos de un producto existente.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| producto_id | integer | ID del producto |

**Payload:**
```json
{
  "Precio": 165.00,
  "Descripcion": "Pizza gourmet con tomate, mozzarella búfala y albahaca fresca"
}
```

**Response 200 (Success):**
```json
{
  "ProductoId": 4,
  "Nombre": "Pizza Margarita",
  "Descripcion": "Pizza gourmet con tomate, mozzarella búfala y albahaca fresca",
  "Precio": 165.00,
  "CategoriaId": 2,
  "Activo": true
}
```

---

### 5. Eliminar un Producto

**URI:** `/api/v1/menu-productos/{producto_id}`
**Método HTTP:** `DELETE`
**Descripción:** Elimina un producto del menú.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| producto_id | integer | ID del producto |

**Payload:** No requiere

**Response 200 (Success):**
```json
{
  "message": "Producto Pizza Margarita eliminado exitosamente"
}
```

**Response 400 (Bad Request):**
```json
{
  "detail": "No se puede eliminar el producto porque está en detalles de órdenes"
}
```

---

## ENDPOINTS - ÓRDENES

### 1. Listar Todas las Órdenes

**URI:** `/api/v1/ordenes`
**Método HTTP:** `GET`
**Descripción:** Obtiene una lista paginada de todas las órdenes, con opciones de filtrado.

**Query Parameters:**
| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| skip | integer | No | 0 | Número de registros a omitir |
| limit | integer | No | 100 | Número máximo de registros a devolver |
| mesa_id | integer | No | null | Filtrar por mesa |
| estado | string | No | null | Filtrar por estado |

**Payload:** No requiere

**Response 200 (Success):**
```json
[
  {
    "OrdenId": 1,
    "MesaId": 1,
    "MeseroId": 1,
    "FechaCreacion": "2024-11-19T10:30:00",
    "FechaCierre": null,
    "Total": 230.00,
    "Estado": "Abierta",
    "Comentarios": null,
    "Detalles": [
      {
        "DetalleId": 1,
        "OrdenId": 1,
        "ProductoId": 1,
        "Cantidad": 2,
        "PrecioUnitario": 55.00,
        "Subtotal": 110.00,
        "Estado": "Pendiente"
      },
      {
        "DetalleId": 2,
        "OrdenId": 1,
        "ProductoId": 2,
        "Cantidad": 1,
        "PrecioUnitario": 120.00,
        "Subtotal": 120.00,
        "Estado": "Pendiente"
      }
    ]
  }
]
```

---

### 2. Obtener una Orden por ID

**URI:** `/api/v1/ordenes/{orden_id}`
**Método HTTP:** `GET`
**Descripción:** Obtiene los detalles completos de una orden específica, incluyendo todos sus detalles.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| orden_id | integer | ID de la orden |

**Payload:** No requiere

**Response 200 (Success):**
```json
{
  "OrdenId": 1,
  "MesaId": 1,
  "MeseroId": 1,
  "FechaCreacion": "2024-11-19T10:30:00",
  "FechaCierre": null,
  "Total": 230.00,
  "Estado": "Abierta",
  "Comentarios": null,
  "Detalles": [
    {
      "DetalleId": 1,
      "OrdenId": 1,
      "ProductoId": 1,
      "Cantidad": 2,
      "PrecioUnitario": 55.00,
      "Subtotal": 110.00,
      "Estado": "Pendiente"
    }
  ]
}
```

---

### 3. Crear una Orden

**URI:** `/api/v1/ordenes`
**Método HTTP:** `POST`
**Descripción:** Crea una nueva orden, opcionalmente con detalles. Calcula el total automáticamente.

**Payload (sin detalles):**
```json
{
  "MesaId": 1,
  "MeseroId": 1,
  "Estado": "Abierta",
  "Comentarios": "Cliente prefiere agua sin gas"
}
```

**Payload (con detalles):**
```json
{
  "MesaId": 1,
  "MeseroId": 1,
  "Estado": "Abierta",
  "Comentarios": "Mesa para 4 personas",
  "Detalles": [
    {
      "ProductoId": 1,
      "Cantidad": 2,
      "PrecioUnitario": 55.00,
      "Estado": "Pendiente"
    },
    {
      "ProductoId": 2,
      "Cantidad": 1,
      "PrecioUnitario": 120.00,
      "Estado": "Pendiente"
    }
  ]
}
```

**Validaciones:**
- `MesaId`: Requerido, debe existir
- `MeseroId`: Requerido, debe existir
- Solo productos activos pueden agregarse
- El total se calcula automáticamente

**Response 201 (Created):**
```json
{
  "OrdenId": 2,
  "MesaId": 1,
  "MeseroId": 1,
  "FechaCreacion": "2024-11-19T11:00:00",
  "FechaCierre": null,
  "Total": 230.00,
  "Estado": "Abierta",
  "Comentarios": "Mesa para 4 personas",
  "Detalles": [
    {
      "DetalleId": 3,
      "OrdenId": 2,
      "ProductoId": 1,
      "Cantidad": 2,
      "PrecioUnitario": 55.00,
      "Subtotal": 110.00,
      "Estado": "Pendiente"
    }
  ]
}
```

**Response 400 (Bad Request):**
```json
{
  "detail": "Producto Pizza Vegetariana no está activo"
}
```

---

### 4. Actualizar una Orden

**URI:** `/api/v1/ordenes/{orden_id}`
**Método HTTP:** `PUT`
**Descripción:** Actualiza los datos de una orden existente.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| orden_id | integer | ID de la orden |

**Payload:**
```json
{
  "Estado": "En proceso",
  "Comentarios": "Cliente solicitó que la comida sea para llevar"
}
```

**Response 200 (Success):**
```json
{
  "OrdenId": 2,
  "MesaId": 1,
  "MeseroId": 1,
  "FechaCreacion": "2024-11-19T11:00:00",
  "FechaCierre": null,
  "Total": 230.00,
  "Estado": "En proceso",
  "Comentarios": "Cliente solicitó que la comida sea para llevar",
  "Detalles": [...]
}
```

---

### 5. Cerrar una Orden

**URI:** `/api/v1/ordenes/{orden_id}/cerrar`
**Método HTTP:** `POST`
**Descripción:** Cierra una orden, calculando el total final desde los detalles y estableciendo la fecha de cierre.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| orden_id | integer | ID de la orden |

**Payload:**
```json
{
  "Comentarios": "Cliente satisfecho, dejó propina"
}
```

**Response 200 (Success):**
```json
{
  "OrdenId": 2,
  "MesaId": 1,
  "MeseroId": 1,
  "FechaCreacion": "2024-11-19T11:00:00",
  "FechaCierre": "2024-11-19T12:30:00",
  "Total": 230.00,
  "Estado": "Cerrada",
  "Comentarios": "Cliente satisfecho, dejó propina",
  "Detalles": [...]
}
```

**Response 400 (Bad Request):**
```json
{
  "detail": "La orden ya está cerrada"
}
```

---

### 6. Eliminar una Orden

**URI:** `/api/v1/ordenes/{orden_id}`
**Método HTTP:** `DELETE`
**Descripción:** Elimina una orden y todos sus detalles (cascade delete).

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| orden_id | integer | ID de la orden |

**Payload:** No requiere

**Response 200 (Success):**
```json
{
  "message": "Orden 2 eliminada exitosamente"
}
```

---

## ENDPOINTS - DETALLES DE ORDEN

### 1. Listar Detalles de una Orden

**URI:** `/api/v1/detalles-orden/orden/{orden_id}`
**Método HTTP:** `GET`
**Descripción:** Obtiene todos los detalles de una orden específica.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| orden_id | integer | ID de la orden |

**Payload:** No requiere

**Response 200 (Success):**
```json
[
  {
    "DetalleId": 1,
    "OrdenId": 1,
    "ProductoId": 1,
    "Cantidad": 2,
    "PrecioUnitario": 55.00,
    "Subtotal": 110.00,
    "Estado": "Servido"
  },
  {
    "DetalleId": 2,
    "OrdenId": 1,
    "ProductoId": 2,
    "Cantidad": 1,
    "PrecioUnitario": 120.00,
    "Subtotal": 120.00,
    "Estado": "En preparación"
  }
]
```

---

### 2. Obtener un Detalle por ID

**URI:** `/api/v1/detalles-orden/{detalle_id}`
**Método HTTP:** `GET`
**Descripción:** Obtiene un detalle de orden específico.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| detalle_id | integer | ID del detalle |

**Payload:** No requiere

**Response 200 (Success):**
```json
{
  "DetalleId": 1,
  "OrdenId": 1,
  "ProductoId": 1,
  "Cantidad": 2,
  "PrecioUnitario": 55.00,
  "Subtotal": 110.00,
  "Estado": "Servido"
}
```

---

### 3. Crear un Detalle de Orden

**URI:** `/api/v1/detalles-orden`
**Método HTTP:** `POST`
**Descripción:** Agrega un nuevo detalle a una orden existente. Calcula el subtotal y actualiza el total de la orden automáticamente.

**Payload:**
```json
{
  "OrdenId": 1,
  "ProductoId": 3,
  "Cantidad": 4,
  "PrecioUnitario": 25.00,
  "Estado": "Pendiente"
}
```

**Validaciones:**
- `OrdenId`: Requerido, debe existir
- `ProductoId`: Requerido, debe existir y estar activo
- `Cantidad`: Requerido, debe ser > 0
- `PrecioUnitario`: Requerido, debe ser >= 0
- Subtotal se calcula automáticamente
- Total de la orden se actualiza automáticamente

**Response 201 (Created):**
```json
{
  "DetalleId": 5,
  "OrdenId": 1,
  "ProductoId": 3,
  "Cantidad": 4,
  "PrecioUnitario": 25.00,
  "Subtotal": 100.00,
  "Estado": "Pendiente"
}
```

**Response 400 (Bad Request):**
```json
{
  "detail": "Producto Café Americano no está activo"
}
```

---

### 4. Actualizar un Detalle de Orden

**URI:** `/api/v1/detalles-orden/{detalle_id}`
**Método HTTP:** `PUT`
**Descripción:** Actualiza un detalle de orden existente. Recalcula el subtotal y actualiza el total de la orden automáticamente.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| detalle_id | integer | ID del detalle |

**Payload:**
```json
{
  "Cantidad": 5,
  "Estado": "En preparación"
}
```

**Response 200 (Success):**
```json
{
  "DetalleId": 5,
  "OrdenId": 1,
  "ProductoId": 3,
  "Cantidad": 5,
  "PrecioUnitario": 25.00,
  "Subtotal": 125.00,
  "Estado": "En preparación"
}
```

---

### 5. Eliminar un Detalle de Orden

**URI:** `/api/v1/detalles-orden/{detalle_id}`
**Método HTTP:** `DELETE`
**Descripción:** Elimina un detalle de orden. Actualiza el total de la orden automáticamente.

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| detalle_id | integer | ID del detalle |

**Payload:** No requiere

**Response 200 (Success):**
```json
{
  "message": "Detalle 5 eliminado exitosamente"
}
```

---

## CÓDIGOS DE ESTADO HTTP

| Código | Significado | Uso |
|--------|-------------|-----|
| 200 | OK | Solicitud exitosa (GET, PUT, DELETE) |
| 201 | Created | Recurso creado exitosamente (POST) |
| 400 | Bad Request | Error de validación o lógica de negocio |
| 404 | Not Found | Recurso no encontrado |
| 500 | Internal Server Error | Error interno del servidor |

---

## EJEMPLOS DE USO

### Ejemplo 1: Crear una orden completa

```bash
# 1. Crear la orden con detalles
curl -X POST "https://restaurant-api-app.azurewebsites.net/api/v1/ordenes" \
  -H "Content-Type: application/json" \
  -d '{
    "MesaId": 1,
    "MeseroId": 1,
    "Detalles": [
      {
        "ProductoId": 1,
        "Cantidad": 2,
        "PrecioUnitario": 55.00
      },
      {
        "ProductoId": 2,
        "Cantidad": 1,
        "PrecioUnitario": 120.00
      }
    ]
  }'

# 2. Agregar más detalles a la orden
curl -X POST "https://restaurant-api-app.azurewebsites.net/api/v1/detalles-orden" \
  -H "Content-Type: application/json" \
  -d '{
    "OrdenId": 1,
    "ProductoId": 3,
    "Cantidad": 4,
    "PrecioUnitario": 25.00
  }'

# 3. Cerrar la orden
curl -X POST "https://restaurant-api-app.azurewebsites.net/api/v1/ordenes/1/cerrar" \
  -H "Content-Type: application/json" \
  -d '{
    "Comentarios": "Cliente satisfecho"
  }'
```

### Ejemplo 2: Consultar mesas disponibles

```bash
# Obtener solo mesas libres
curl "https://restaurant-api-app.azurewebsites.net/api/v1/mesas?estado=Libre"
```

### Ejemplo 3: Gestionar productos del menú

```bash
# Crear categoría
curl -X POST "https://restaurant-api-app.azurewebsites.net/api/v1/categorias" \
  -H "Content-Type: application/json" \
  -d '{
    "Nombre": "Bebidas",
    "Descripcion": "Bebidas frías y calientes"
  }'

# Crear producto en la categoría
curl -X POST "https://restaurant-api-app.azurewebsites.net/api/v1/menu-productos" \
  -H "Content-Type: application/json" \
  -d '{
    "Nombre": "Café Americano",
    "Descripcion": "Café negro americano",
    "Precio": 25.00,
    "CategoriaId": 3,
    "Activo": true
  }'

# Listar productos de la categoría Bebidas
curl "https://restaurant-api-app.azurewebsites.net/api/v1/menu-productos?categoria_id=3&activo=true"
```

---

**Nota:** Este documento puede convertirse a formato Word utilizando herramientas como Pandoc:

```bash
pandoc API_DOCUMENTATION.md -o API_DOCUMENTATION.docx
```

O puede copiarse el contenido a Microsoft Word directamente, donde el formato Markdown será interpretado correctamente con la función "Pegar especial".
