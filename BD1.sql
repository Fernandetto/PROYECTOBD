---------------------------------------------------------
-- SCRIPT DE PRUEBA FINAL
---------------------------------------------------------
USE dev_Proyecto_OOP_FS;  -- Cambia esto por tu base de datos
GO

---------------------------------------------------------
-- INSERTAR VARIAS ORDENES DE PRUEBA
---------------------------------------------------------

-- Orden 1
INSERT INTO restaurante.Ordenes (MesaId, MeseroId) 
VALUES (1, 1);

DECLARE @Orden1Id INT = SCOPE_IDENTITY();

INSERT INTO restaurante.DetallesOrden (OrdenId, ProductoId, Cantidad, PrecioUnitario)
VALUES
(@Orden1Id, 1, 2, 55.00),   -- 2 Sopa del Día
(@Orden1Id, 2, 1, 120.00);  -- 1 Hamburguesa Clásica

-- Orden 2
INSERT INTO restaurante.Ordenes (MesaId, MeseroId)
VALUES (2, 2);

DECLARE @Orden2Id INT = SCOPE_IDENTITY();

INSERT INTO restaurante.DetallesOrden (OrdenId, ProductoId, Cantidad, PrecioUnitario)
VALUES
(@Orden2Id, 2, 2, 120.00),  -- 2 Hamburguesas Clásicas
(@Orden2Id, 3, 3, 25.00);   -- 3 Coca-Cola

-- Orden 3
INSERT INTO restaurante.Ordenes (MesaId, MeseroId)
VALUES (3, 1);

DECLARE @Orden3Id INT = SCOPE_IDENTITY();

INSERT INTO restaurante.DetallesOrden (OrdenId, ProductoId, Cantidad, PrecioUnitario)
VALUES
(@Orden3Id, 1, 1, 55.00),
(@Orden3Id, 3, 2, 25.00);

---------------------------------------------------------
-- CONSULTA DE DETALLES DE TODAS LAS ORDENES
---------------------------------------------------------
SELECT 
    o.OrdenId,
    m.Nombre AS Mesero,
    me.Numero AS Mesa,
    d.ProductoId,
    p.Nombre AS Producto,
    d.Cantidad,
    d.PrecioUnitario,
    d.Subtotal
FROM restaurante.Ordenes o
JOIN restaurante.Meseros m ON o.MeseroId = m.MeseroId
JOIN restaurante.Mesas me ON o.MesaId = me.MesaId
JOIN restaurante.DetallesOrden d ON o.OrdenId = d.OrdenId
JOIN restaurante.MenuProductos p ON d.ProductoId = p.ProductoId
ORDER BY o.OrdenId, d.DetalleId;
GO

---------------------------------------------------------
-- RESUMEN DE TOTAL POR ORDEN
---------------------------------------------------------
SELECT 
    o.OrdenId,
    m.Nombre AS Mesero,
    me.Numero AS Mesa,
    SUM(d.Subtotal) AS TotalOrden
FROM restaurante.Ordenes o
JOIN restaurante.Meseros m ON o.MeseroId = m.MeseroId
JOIN restaurante.Mesas me ON o.MesaId = me.MesaId
JOIN restaurante.DetallesOrden d ON o.OrdenId = d.OrdenId
GROUP BY o.OrdenId, m.Nombre, me.Numero
ORDER BY o.OrdenId;
GO
