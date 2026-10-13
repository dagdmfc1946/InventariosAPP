# Arquitectura tecnica

## Enfoque

Monolito modular Django para ejecucion local en Windows:

```text
Navegador (Chrome/Edge) -> Django -> Django ORM -> SQLite
```

No se implementaran microservicios, SPA separada, WebSockets, API REST ni dependencia de servicios externos en el MVP.

## Modulos previstos

| Modulo | Responsabilidad |
|---|---|
| `core` | Utilidades y configuracion compartida. |
| `components` | Categorias, componentes y especificaciones tecnicas. |
| `suppliers` | Proveedores y ofertas de compra. |
| `inventory` | Stock, movimientos y ubicaciones. |
| `documents` | Datasheets PDF y sus validaciones. |
| `dashboard` | Indicadores y vistas de resumen. |

Los modulos se crearan como apps Django en F2, dentro de `apps/`.

## Modelo de datos previsto

- Categoria 1:N Componente.
- Componente 1:N Especificacion (modelo EAV: atributo, valor, unidad).
- Componente N:M Proveedor mediante OfertaProveedor; una oferta conserva precio, moneda, URL, cantidad minima y fecha de consulta.
- Componente 1:1 Stock; Stock 1:N MovimientoStock.
- Componente 1:N Datasheet.
- Ubicaciones: decision pendiente entre una ubicacion unica por componente o multiples ubicaciones con cantidades por ubicacion.

## Seguridad y operacion

- `SECRET_KEY` y valores locales en `.env`, fuera de Git.
- Proteccion CSRF, escape de plantillas y validacion de entradas con formularios Django.
- Datasheets: solo PDF, limite de tamano y nombre/ruta gestionados por la aplicacion.
- Backups reproducibles de SQLite y `media/`.
- Los modelos deben usar ORM y evitar SQL especifico de SQLite, para permitir una migracion futura a PostgreSQL si el uso se vuelve multiusuario.
