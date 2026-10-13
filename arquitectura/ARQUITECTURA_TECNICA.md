# Arquitectura técnica implementada

## Sistema y ejecución

InventariosAPP es un monolito modular Django con plantillas, ORM y SQLite. Las
pantallas se renderizan en el servidor; CSS/JavaScript locales mejoran la interacción.
No hay SPA, API REST pública, microservicios ni servicios externos obligatorios.

En desarrollo, manage.py utiliza config.settings y runserver. preparar_proyecto.bat
crea/reutiliza Python 3.12 y configura dependencias, migraciones y perfiles; el
administrador se crea por terminal si no existe uno activo. iniciar_desarrollo.bat
inicia runserver e indica /admin/ como entrada; no abre automáticamente el navegador.

En distribución, PyInstaller empaqueta un directorio con InventariosAPP.exe y
_internal. El launcher configura la instalación antes de django.setup(), aplica
migraciones, prepara roles e inicia Waitress en 127.0.0.1:8000 por defecto. Abre
/accounts/login/ en el navegador salvo --no-browser. Cambiar la página indicada
por el .bat de desarrollo no modifica el comportamiento del .exe publicado.
Waitress ejecuta WSGI con cuatro hilos; WhiteNoise entrega estáticos recolectados.
config.settings_local usa DEBUG=False y limita ALLOWED_HOSTS a localhost/127.0.0.1.

## Responsabilidades

| Unidad | Responsabilidad y relaciones |
|---|---|
| config | Settings, URLs, WSGI/ASGI y fuente única de versión. |
| apps/core | Catálogo filtrado, paginación, exportación ReportLab, perfil, controles de acceso y roles. |
| apps/components | Categorías, fichas, especificaciones, alta con stock, edición y duplicación. |
| apps/inventory | Ubicaciones compartidas, stock, movimientos y validación de saldo. |
| apps/suppliers | Proveedores y ofertas vinculadas a componentes. |
| apps/documents | Registro/carga/descarga de PDF con autorización y limpieza de carga fallida. |
| apps/dashboard | Consultas agregadas, alertas y movimientos recientes. |
| templates / static | UI compartida, estilos, iconos y mejoras progresivas; Admin conserva controles Django. |
| launcher.py / runtime_local.py | Arranque, mantenimiento, secreto persistente y bloqueo de carpeta de datos. |
| backups/backup_local.py | Snapshot SQLite, copia media/clave, manifiesto SHA256, validación y restauración. |
| build_exe.py / InventariosAPP.spec | Recolección de estáticos, empaquetado onedir, inspección y ZIP. |

Las apps conviven en un proceso Django y comparten una base. Los módulos son unidades
de responsabilidad; no constituyen aislamiento de procesos. El ORM traduce operaciones
a SQLite. El controlador de negocio solicita las escrituras; no las hace el navegador.

## Reglas de integridad

El alta completa usa transaction.atomic: componente, stock y movimiento inicial
se confirman juntos o se revierten. La duplicación copia la ficha técnica y sus
especificaciones, con stock nuevo a cero; no copia documentos ni historial.

Los movimientos registrados son inmutables mediante los métodos del modelo y su
QuerySet. StockMovement.save() actualiza saldo e inserta historial en una misma
transacción, con filtros que impiden saldo negativo y exceso de máximo. El servicio
rechaza un saldo obsoleto y reconoce un request_id ya usado: el reenvío no duplica
el movimiento. Estas reglas son del aplicativo; no impiden una edición manual de
SQLite por herramientas externas.

Los PDF se validan por extensión, tamaño máximo de 20 MB y firma inicial %PDF- en
cargas nuevas. La operación intenta eliminar un archivo recién escrito si falla la
transacción. SQLite y el sistema de archivos no son una transacción distribuida;
un fallo de disco o interrupción requiere revisar el estado/respaldos.

## Autenticación y acceso

Django gestiona usuarios, hashes de contraseña, sesiones, CSRF y permisos. Lector y
Operador son grupos normales; la gestión de usuarios está reservada al superusuario.
El catálogo/resumen/PDF requieren sesión y permisos. /admin/ exige acceso staff;
el flujo de cuentas del aplicativo no crea superusuarios. /media/ pasa por una vista
que resuelve un Datasheet registrado y verifica permisos: no expone la carpeta sin
autorización. Una sesión válida del navegador puede sobrevivir al reinicio del servidor.

## Almacenamiento del ejecutable

Predeterminado en Windows: **%LOCALAPPDATA%\InventariosAPP\data**. Para Diego:
**C:\Users\Diego\AppData\Local\InventariosAPP\data**.

| Ruta dentro de data | Contenido |
|---|---|
| db.sqlite3 | Usuarios, permisos, sesiones, componentes, stock, movimientos, proveedores y metadatos PDF. |
| media/datasheets/AAAA/MM/DD/ | Archivos PDF adjuntados. |
| .runtime-key | Secreto persistente de la instalación; conservarlo y no publicarlo. |
| backups/ | Respaldos generados cuando no se indica --output. |

La consola del .exe imprime la carpeta efectiva. --data-dir permite otra ruta, por
lo que el valor de consola prevalece. Cada cuenta Windows tiene su propio LOCALAPPDATA.
Mover/reemplazar el programa no borra la carpeta de datos. El ZIP no incluye datos
de trabajo; una instalación nueva comienza vacía. Desarrollo usa .local/dev_v2 por
defecto y no comparte automáticamente la base del .exe.

## Recuperación y límites

El launcher mantiene un bloqueo de archivo durante servidor/mantenimiento. backup
obtiene un snapshot con la API SQLite, copia media y .runtime-key, verifica integridad
y escribe hashes. restore verifica el manifiesto y conserva el destino previo en
data.previous-... antes de instalar el respaldo. Detener el servidor antes de ambas
operaciones. El bloqueo no controla escrituras de procesos externos con manage.py.

El destino aprobado es un PC Windows x64 y HTTP de loopback. Exposición a la red,
concurrencia amplia, HTTPS o migración a PostgreSQL requieren trabajo adicional.
El .exe sin firma se comprobó en el PC objetivo; otro Windows puede decidir distinto
mediante Smart App Control. PyInstaller no garantiza confidencialidad del código.

## Evidencia principal del código

Todas las referencias corresponden al commit fijado del diagrama.

- [Arranque y Waitress](https://github.com/dagdmfc1946/InventariosAPP/blob/e55a3f3d2276997673efe33616debfd81b979c7a/launcher.py).
- [Datos, clave y bloqueo](https://github.com/dagdmfc1946/InventariosAPP/blob/e55a3f3d2276997673efe33616debfd81b979c7a/runtime_local.py).
- [Modelo y escritura atómica de stock](https://github.com/dagdmfc1946/InventariosAPP/blob/e55a3f3d2276997673efe33616debfd81b979c7a/apps/inventory/models.py).
- [Servicio de movimiento e idempotencia](https://github.com/dagdmfc1946/InventariosAPP/blob/e55a3f3d2276997673efe33616debfd81b979c7a/apps/inventory/services.py).
- [PDF protegidos](https://github.com/dagdmfc1946/InventariosAPP/blob/e55a3f3d2276997673efe33616debfd81b979c7a/apps/documents/views.py).
- [Respaldo y restauración](https://github.com/dagdmfc1946/InventariosAPP/blob/e55a3f3d2276997673efe33616debfd81b979c7a/backups/backup_local.py).
