# Informe ejecutivo de pruebas — InventariosAPP v2.2.0

Fecha: 12/10/2026. Rama: `dev_v2`. Implementación: `e548970`.
Estado: publicación autorizada por el usuario; Fase 4 sin iniciar.

## Dictamen

La regresión automatizada aprueba **115 de 115 pruebas**, sin fallos, errores ni
omisiones. Los resultados respaldan la publicación de los cambios implementados
para revisión y uso en el entorno local de desarrollo. No equivalen a certificar
una distribución final con Waitress/PyInstaller ni a una auditoría integral de seguridad.

| Indicador | Resultado |
|---|---:|
| Pruebas ejecutadas y aprobadas | 115 |
| Fallos / errores / omitidas | 0 / 0 / 0 |
| Éxito de ejecución | 100 % |
| Duración de la ejecución completa | 114.092 segundos (1 min 54 s) |
| Comprobación de Django | Sin incidencias |
| Migraciones no generadas | Ninguna |
| Compatibilidad de dependencias (`pip check`) | Sin incompatibilidades |

El 100 % representa pruebas aprobadas; **no es un porcentaje de cobertura del código**.
No se ha medido cobertura de líneas o ramas para esta ejecución.

## Alcance y resultados por área

| Área | Pruebas | Resultado y relevancia para el negocio |
|---|---:|---|
| Componentes, alta, ficha y duplicación | 25 | Alta junto con existencias, cantidades inválidas, doble envío, guardar/agregar otro, edición de especificaciones, permisos y duplicación técnica. Reduce registros parciales y copias accidentales de datos operativos. |
| Inventario, movimientos y ubicaciones | 38 | Entradas/salidas/ajustes, límites y saldo cero, movimientos inmutables, reversión ante fallos, saldos obsoletos, tokens alterados/expirados, reenvíos, dos salidas competidoras y migración a ubicaciones compartidas. Respalda la consistencia entre saldo e historial. |
| Usuarios, perfil, roles y sesión | 20 | Creación de cuentas normales, contraseña utilizable, acceso restringido al Admin, ausencia de promoción de privilegios, edición exclusiva del perfil propio, duplicados y nombres inválidos, sesión tras renombrar y acceso con el nuevo nombre. La contraseña permanece protegida. |
| Catálogo, resumen y exportación PDF | 11 | Búsqueda, componentes activos, filtros combinados, orden, paginación, métricas y enlaces; PDF con todos los resultados filtrados, incluso fuera de la página visible, informe vacío y autorización de descarga. |
| Proveedores y ofertas | 8 | Validaciones de modelos, edición, precio/cantidad, duplicados, vínculos con el componente correcto y creación contextual conservando los datos de la oferta. |
| Datasheets y archivos protegidos | 10 | Formato/tamaño del PDF, archivos disfrazados, acceso autorizado, archivos inexistentes, limpieza tras fallo de base de datos y guardar/seguir editando sin volver a subir el documento. |
| Copias y aislamiento del desarrollo | 3 | Prueba del respaldo/restauración existente y separación de la copia de desarrollo; rechazo de sobrescritura y de la raíz del proyecto como destino. Alcance preliminar: no cierra los requisitos de recuperación de Fase 4. |
| **Total** | **115** | **Todas aprobadas.** |

Las siete pruebas incorporadas respecto de la suite anterior de 108 son:

- Dos de perfil: cambio de nombre con sesión/login conservados; rechazo de nombres
  duplicados, vacíos o inválidos.
- Dos de Administración: contraseña sin detalles criptográficos y sin modificación
  mediante un POST manipulado; presentación de cuenta sin contraseña.
- Tres de PDF: exportación completa con cabeceras HTTP privadas, selección/vacío y
  requisitos de autenticación/permisos.

Además, se actualizó una prueba existente para verificar que renombrar la cuenta propia
no permite editar otra cuenta ni ampliar privilegios.

## Verificación visual y de documentos, adicional a las 115 pruebas

Se utilizó una base ficticia independiente (`.local/ui_review_fase3`). Se comprobó
el perfil editable, el estado simplificado de contraseña y el botón de descarga del
catálogo. El PDF descargado desde el navegador contiene los tres componentes ficticios
esperados y sus valores, sin archivos o credenciales del usuario real.

Se generó también un informe sintético de **90 filas y ocho páginas**, con nombres
largos, acentos, `µ`, `Ω` y caracteres que requieren escape. La extracción confirmó
los registros extremos y los encabezados en todas las páginas; se renderizaron e
inspeccionaron visualmente las páginas primera y última para comprobar alineación,
legibilidad y ausencia de recortes. No son ocho pruebas automatizadas adicionales.

La base `db.sqlite3` original mantiene el SHA256 registrado antes del desarrollo:
`B247D32672C3D77C9DF9F377C833061D79AAFF9A7010112AB9776096616F12E2`.

## Límites y trabajo pendiente

- La suite comprueba escenarios definidos; no garantiza ausencia de defectos en casos
  no cubiertos. No se realizó una prueba de carga ni una certificación multiusuario.
- La concurrencia probada incluye dos salidas competidoras y el rechazo de saldo
  obsoleto; no establece capacidad de producción bajo carga sostenida.
- Las comprobaciones de seguridad se concentran en autenticación, permisos, CSRF,
  manipulación de campos, tokens y archivos. No sustituyen una auditoría de seguridad.
- El respaldo existente tiene una prueba funcional; la recuperación consistente con
  archivos y su procedimiento de reversión siguen siendo trabajo de Fase 4.
- Arranque definitivo con Waitress, DEBUG desactivado, distribución PyInstaller y
  funcionamiento en un PC sin Python aún no se implementaron ni validaron.

**Decisión:** publicar las mejoras de v2.2.0 en `dev_v2`, conforme a la autorización
recibida. Mantener Fase 4 pendiente de aprobación expresa; no integrar en `dev`/`main`.

## Trazabilidad y reproducción

Resultado real conservado localmente: `.local/revision_usuarios_pdf_tests.txt`.
Django 5.2.6, Python 3.12, SQLite y ReportLab 4.5.1 en el entorno virtual del proyecto.
La suite crea y destruye una base de pruebas; no utiliza la base operativa como destino.

```powershell
$env:TEMP = Join-Path (Get-Location) 'backups/verification_tmp'
$env:TMP = $env:TEMP
.\.venv\Scripts\python.exe manage.py test --noinput
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe -m pip check
```

Inventario de pruebas por módulo (recuento de la suite descubierta, total 115):

| Módulo | Cantidad |
|---|---:|
| components.test_component_detail | 8 |
| components.test_duplicate | 4 |
| components.test_quick_create | 10 |
| components.tests | 3 |
| inventory.test_integrity | 20 |
| inventory.test_movement_flow | 11 |
| inventory.test_shared_locations | 4 |
| inventory.tests | 3 |
| core.test_admin_interface | 10 |
| core.test_profile | 5 |
| core.test_roles | 3 |
| core.test_session | 2 |
| core.test_catalog_filters | 3 |
| core.test_catalog_pdf | 3 |
| core.tests: catálogo y navegación | 4 |
| dashboard.tests | 1 |
| suppliers.test_offer_flow | 5 |
| suppliers.tests | 3 |
| documents.test_admin_upload | 3 |
| documents.test_protected_files | 4 |
| documents.tests | 3 |
| core.test_development_copy | 2 |
| core.tests: respaldo/restauración existente | 1 |
