# InventariosAPP

## Desarrollo v2 — rama dev_v2

Fases 1, 2 y 3 concluidas en `dev_v2`, con publicación autorizada por el usuario.
Versión visible `v2.1.1`. Fase 4 no iniciada; requiere aprobación separada.
Esta sección prevalece para la rama v2; la documentación inferior conserva la referencia
de instalación y comportamiento de la primera versión.

El nuevo flujo permite crear componente y stock en una sola pantalla; los movimientos
son atómicos e inmutables. La ficha incorpora entrada/salida/ajuste con vista previa,
historial paginado, duplicación técnica y ofertas con proveedor contextual. El catálogo
combina filtros y páginas de 25; el resumen enlaza pendientes. La sesión muestra las
mismas acciones en todas las vistas. Admin sigue disponible para mantenimiento.

### Datos de trabajo y arranque

En este equipo ya se creó la copia `.local/dev_v2`, con las cuentas y datos originales.
Los originales `db.sqlite3` y `media/` no se migraron ni se borraron. La ruta de trabajo
se configura con `INVENTARIOS_DATA_DIR` (por defecto `.local/dev_v2`).

Para preparar una copia **sólo si aún no existe**, detener escrituras/subidas en la
versión original mientras se obtiene el snapshot y media:

```powershell
.\.venv\Scripts\python.exe backups/prepare_dev.py
```

El script rechaza un destino existente: no reemplaza datos previos. En un clon sin base
original, preparar una instalación vacía con `New-Item -ItemType Directory -Path .local/dev_v2 -Force`
y luego migrate/createsuperuser. Con la copia existente no crear otro superusuario.

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py configure_inventory_roles
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Abrir `/components/new/` o `/search/`; usar las credenciales habituales de la copia.
El nuevo login está en `/accounts/login/`. Se requieren los permisos de agregar componente,
stock y movimiento; el superusuario los tiene. El logout se realiza con botón POST.
No copiar los nuevos archivos sobre dev/main para probar: cambiar de rama de manera controlada.
Fase 2 exige sesión/permisos también en búsqueda, resumen y PDF. Usuarios nuevos permiten
seleccionar Lector u Operador; las cuentas anteriores conservan permisos y grupos, y el
superusuario puede asignarles esos perfiles. configure_inventory_roles prepara/actualiza
los permisos de esos dos grupos sin asignar cuentas ni conceder acceso administrativo.
La nueva ficha se abre desde el catálogo; «Mi perfil» desde el enlace de la sesión.

Antes de migrar Fase 2 se creó el respaldo local `.local/checkpoints/fase1_before_fase2`
de la copia de desarrollo. Se conservan las asignaciones existentes de ubicaciones.
Una ubicación ocupada no se borra. No volver al esquema antiguo sobre datos que ya
comparten ubicaciones: usar el respaldo si se necesita recuperar Fase 1.
El código y la documentación de Fase 1 se mantienen juntos en `dev_v2`, tanto localmente
como en GitHub. La base, los PDF, secretos y entornos virtuales permanecen locales y
fuera de Git. La copia `.local/dev_v2` permite revisar v2 sin alterar los datos de `dev`.

### Verificación y documentos

```powershell
.\.venv\Scripts\python.exe manage.py test --noinput
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Consulta [manual de usuario](MANUAL_USUARIO.md), [CHANGELOG](CHANGELOG.md),
[registro del desarrollo](dev_Process.md) y [servidores y distribución](docs/SERVIDORES_Y_DISTRIBUCION.md).
Se mantiene runserver mientras desarrollamos. Tras aprobación final se usará Waitress
y después PyInstaller para distribución Windows local. No se añadió aún ninguna de esas dependencias.

---

## Referencia de la primera versión

Aplicacion local para Windows destinada a administrar inventario personal o profesional de componentes electronicos. Permitira registrar, consultar y mantener componentes, sus especificaciones tecnicas, proveedores, precios, stock, ubicaciones fisicas y datasheets.

## Estado actual

Las fases F1 a F10 estan completadas. La aplicacion dispone de administracion Django, buscador, dashboard, movimientos de stock, gestion de datasheets, backup local y pruebas automatizadas.

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

Consulte los documentos de [arquitectura](docs/ARQUITECTURA.md), [plan de desarrollo](docs/PLAN_DESARROLLO.md), [dependencias](docs/DEPENDENCIAS.md), [flujo Git](docs/FLUJO_GIT.md) y el registro de fases en [info_FASES.md](info_FASES.md).

## Flujo de trabajo

El desarrollo se realiza en `dev`. Cada fase se documenta, prueba y confirma mediante un commit antes de integrarse de forma controlada en `main`. No se almacenan secretos, entornos virtuales, bases de datos locales, respaldos ni archivos cargados por usuarios.

## Entorno local

Se requiere Python 3.12. Desde PowerShell, situado en la carpeta del proyecto:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
```

El archivo `.env` es local y no se versiona. Cambie `SECRET_KEY` por un valor privado antes de usar la aplicacion fuera de pruebas locales.

### Activar el entorno virtual

Debe activar el entorno virtual antes de ejecutar comandos Python del proyecto:

```powershell
.\.venv\Scripts\Activate.ps1
```

Cuando aparezca `(.venv)` al inicio de la consola, puede usar `python` y `manage.py` directamente. Tambien puede omitir la activacion y ejecutar siempre `\.venv\Scripts\python.exe`.

### Reiniciar la prueba local desde cero

Este procedimiento elimina la base local, incluyendo el superusuario, categorias, componentes, stock y registros de datasheets. Los PDFs fisicos de `media/datasheets/` no se eliminan:

```powershell
Remove-Item .\db.sqlite3 -Force
python manage.py migrate
python manage.py createsuperuser
```

Ejecute el ultimo comando y defina las credenciales del unico usuario administrador de esta version.

## Arranque

```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Abra estas direcciones en el navegador:

- Administracion: http://127.0.0.1:8000/admin/
- Buscador: http://127.0.0.1:8000/search/
- Dashboard: http://127.0.0.1:8000/dashboard/

El enlace **VER EL SITIO** del administrador abre el buscador. Desde el listado de datasheets, **Abrir PDF** abre el archivo en una pestaña nueva; el navegador puede mostrarlo integrado o descargarlo según su configuracion de PDF.

## Primera prueba: agregar un componente

1. Entre en `/admin/` con el superusuario creado.
2. En **Categories**, cree una categoria, por ejemplo `Sensores`.
3. En **Components**, seleccione **Add Component**.
4. Complete `Category`, `Reference`, `Name` y, si aplica, `Value` y `Part number`.
5. Guarde el componente. Desde su pantalla de cambio puede añadir especificaciones en la seccion **Specifications**.
6. Cree el registro de stock del componente desde **Stocks** y defina cantidad actual, minima y maxima.
7. Compruebe el componente en `/search/` y los indicadores en `/dashboard/`.

## Pruebas y backup

```powershell
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py check
```

El backup local se puede ejecutar desde una consola Python con `backup_project` y restaurar con `restore_backup`, funciones disponibles en [backups/backup_local.py](backups/backup_local.py). Las copias deben conservarse fuera de Git.

## Cierre seguro

Para detener el servidor, vuelve a la consola donde ejecutaste `runserver` y pulsa `Ctrl+C`. Espera a que Django confirme que el servidor se detuvo antes de cerrar PowerShell o Windows. Los registros guardados desde el administrador se escriben en SQLite al guardar el formulario; no cierres la ventana durante una subida de PDF o mientras aparece el mensaje de guardado.

Para salir del entorno virtual al terminar:

```powershell
deactivate
```

La prueba de validacion de la primera version debe realizarse desde el navegador, usando `/admin/`, `/search/` y `/dashboard/`. El empaquetado `.exe` queda reservado para F12, despues de validar los flujos de la aplicacion Django.
