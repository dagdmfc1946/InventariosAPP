# InventariosAPP

Aplicacion local para Windows destinada a administrar inventario personal o profesional de componentes electronicos. Permitira registrar, consultar y mantener componentes, sus especificaciones tecnicas, proveedores, precios, stock, ubicaciones fisicas y datasheets.

## Estado actual

El repositorio contiene la estructura documental inicial. Aun no se ha creado el proyecto Django, entorno virtual, base de datos, migraciones ni codigo funcional. El inicio de la fase F1 requiere autorizacion explicita.

## Alcance del MVP

- Gestion administrativa de componentes, categorias, proveedores y ofertas.
- Especificaciones tecnicas configurables por componente.
- Stock, movimientos de inventario y alertas de bajo stock.
- Ubicacion fisica y adjuntos PDF de datasheets.
- Busqueda con filtros, paginacion y dashboard de indicadores.
- Ejecucion local en `127.0.0.1`; sin servicios externos obligatorios.

## Politica tecnologica

Todo el desarrollo utilizara exclusivamente herramientas, librerias y servicios gratuitos u open source. No se incorporaran dependencias de pago, licencias propietarias obligatorias, APIs comerciales ni infraestructura cloud necesaria para operar el MVP.

La aplicacion se construira como un monolito modular con Django y SQLite. La interfaz principal de mantenimiento sera Django Admin personalizado; la busqueda y el dashboard tendran vistas propias.

## Estructura inicial

```text
InventariosAPP/
|-- apps/                 # Apps Django por dominio (se crean en F2)
|-- config/               # Configuracion raiz de Django (F2)
|-- docs/                 # Documentacion tecnica y de proceso
|-- media/datasheets/     # PDFs cargados en ejecucion; no se versionan
|-- static/css/           # Recursos CSS propios o vendorizados
|-- static/js/            # Recursos JavaScript propios o vendorizados
|-- templates/            # Plantillas globales Django
|-- tests/                # Pruebas automatizadas
|-- backups/              # Copias locales; no se versionan
|-- .env.example          # Plantilla de variables de entorno (F1)
|-- .gitignore
`-- README.md
```

Consulte los documentos de [arquitectura](docs/ARQUITECTURA.md), [plan de desarrollo](docs/PLAN_DESARROLLO.md), [dependencias](docs/DEPENDENCIAS.md) y [flujo Git](docs/FLUJO_GIT.md).

## Flujo de trabajo

El desarrollo se realiza en `dev`. Cada fase se documenta, prueba y confirma mediante un commit antes de integrarse de forma controlada en `main`. No se almacenan secretos, entornos virtuales, bases de datos locales, respaldos ni archivos cargados por usuarios.

## Inicio futuro

Cuando se autorice F1 se preparara Python, el entorno virtual, las dependencias minimas y la configuracion segura del proyecto.
