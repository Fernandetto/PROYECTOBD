# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a SQL Server database project for a restaurant management system. The database schema is designed to handle restaurant operations including orders, menu items, tables, waiters, and categories.

## Database Architecture

### Schema: `restaurante`

The database follows a normalized relational design with the following core entities:

1. **Categorias** - Menu item categories (Entradas, Platos Fuertes, Bebidas, etc.)
2. **Meseros** - Waiter information and contact details
3. **Mesas** - Table management with capacity and status (Libre/Ocupada/Reservada)
4. **MenuProductos** - Menu items linked to categories
5. **Ordenes** - Order headers tracking table, waiter, timestamps, and status
6. **DetallesOrden** - Order line items with quantity, price, and subtotal calculations

### Key Design Patterns

- **Identity columns** are used for all primary keys (IDENTITY(1,1))
- **Computed column**: `DetallesOrden.Subtotal` is calculated as `Cantidad * PrecioUnitario PERSISTED`
- **Cascade delete**: Only `DetallesOrden` cascades on `Ordenes` deletion; other FKs use NO ACTION
- **Status tracking**:
  - Mesas: 'Libre', 'Ocupada', 'Reservada'
  - Ordenes: Default 'Abierta', can be closed with FechaCierre
  - DetallesOrden: Default 'Pendiente'
- **Indexes**: Created on frequently queried foreign keys and composite columns (CategoriaId, MesaId+FechaCreacion, OrdenId)

### Relationships

- MenuProductos → Categorias (many-to-one)
- Ordenes → Mesas (many-to-one)
- Ordenes → Meseros (many-to-one)
- DetallesOrden → Ordenes (many-to-one, CASCADE delete)
- DetallesOrden → MenuProductos (many-to-one)

## Working with the Database

### Creating/Recreating the Schema

To initialize the database from scratch:

```bash
sqlcmd -S <server> -d <database> -i BD1.sql
```

Or using SQL Server Management Studio (SSMS), open `BD1.sql` and execute.

### Key Constraints

- `MenuProductos.Precio` must be >= 0
- `Mesas.Capacidad` must be > 0
- `DetallesOrden.Cantidad` must be > 0
- `DetallesOrden.PrecioUnitario` must be >= 0
- `MenuProductos.Nombre` is UNIQUE within Categorias
- `Mesas.Numero` is UNIQUE

### Sample Data

The schema includes seed data:
- 3 categories (Entradas, Platos Fuertes, Bebidas)
- 2 waiters (Carlos Pérez, María López)
- 3 tables with varying capacities
- 3 sample menu items

## Development Notes

- The database uses SQL Server syntax (T-SQL) with `GO` batch separators
- Default values use SQL Server functions: `GETDATE()`, `SYSUTCDATETIME()`
- Text fields use `NVARCHAR` for Unicode support
- Currency/price fields use `DECIMAL(10,2)` or `DECIMAL(12,2)` for precision
