# Registro de desarrollo — InventariosAPP v2

Estado actual: **Fase 1 implementada localmente, pendiente de revisión del usuario**.
Versión: `2.0.0-dev.1` (12/10/2026). Fases 2/3 no iniciadas.

## 12/10/2026 — Análisis y propuesta

Estado: planificación terminada; aprobación pendiente. Desarrollo no iniciado.
Origen revisado: `dev`, commit `842afd1` (feat: prepara prueba inicial y visualizacion de datasheets).

- Se leyeron modelos, administración, vistas, rutas, plantillas, configuración,
  pruebas, respaldo y documentación existente.
- Se consultó la colección solicitada de addyosmani/agent-skills. Skill aplicada:
  planning-and-task-breakdown; guía adicional: adopción en proyectos existentes.
  No se instaló globalmente ni se ejecutaron scripts externos.
- Diagnóstico y propuesta de tres fases en `info_FASES.md`, preservando historial.
- Se crearon este registro, CHANGELOG y manual del comportamiento vigente.
  Índice y tareas técnicas en `tasks/`; funcionalidad futura está marcada como pendiente.
- Verificación: 18 pruebas pasan; `manage.py check` sin incidencias.
  El primer intento tuvo un error de permisos al crear temporales del test de backup;
  se repitió con TEMP/TMP en `backups/verification_tmp`, sin cambiar tests ni código.
  La suite usa base de pruebas; no se migró ni reinició la base operativa.
- No se comprobó visualmente la aplicación ni se inspeccionaron registros personales.
- No se creó `dev_v2`, no se hicieron commits, push, merge ni cambios funcionales.
- Archivos locales anteriores `.venv_backup/` e `info_project.txt` se conservaron.

## 12/10/2026 — Rama y documentación autorizadas

- El usuario autorizó crear `dev_v2` y subir los Markdown preparados.
- Se creó `dev_v2` desde `dev` en `842afd1`; no se inició Fase 1.
- Destino confirmado: uso local en su PC Windows; PyInstaller al finalizar.
  Waitress ejecutará Django localmente dentro de la distribución prevista.
  No se incluye despliegue en servidor; Gunicorn correspondía a otro proyecto.
- Este cambio sólo incluye los seis Markdown del plan y registro. No incluye
  `.venv_backup/`, `info_project.txt`, SQLite, media ni código del aplicativo.
- La autorización de este push documental no autoriza pushes de desarrollo posteriores.

## Próximo paso tras la explicación y confirmación de inicio

Trabajar en `dev_v2`, verificando diferencias respecto de este diagnóstico.
Copiar y aislar datos de operación antes de Fase 1.
Registrar fuente de skills con revisión concreta al comenzar implementación.

## Formato para cada avance

Agregar fecha, fase/tarea, estado, cambio y razón, archivos afectados, pruebas y
resultado, limitaciones, decisiones, versión y commit si existe. Actualizar los estados
en `tasks/todo.md`; no marcar como implementado algo sólo propuesto. Mantener historial.

| Fase | Estado | Evidencia de cierre |
|---|---|---|
| 1 | Implementada localmente; revisión del usuario pendiente | 50 pruebas y navegador |
| 2 | Propuesta | — |
| 3 | Propuesta; destino Windows local confirmado | — |

## 12/10/2026 — Documento de servidores publicado

- Se documentó la explicación y tabla comparativa en `docs/SERVIDORES_Y_DISTRIBUCION.md`.
- Windows: runserver durante desarrollo, Waitress tras aprobación final, PyInstaller para
  distribución. Raspberry: runserver para desarrollo, Gunicorn supervisado con systemd
  para operación; empaquetado Linux/ARM requiere pruebas específicas.
- Se explicó que PyInstaller no garantiza confidencialidad del código, junto a opciones
  Cython/Nuitka y límites de protección cuando el cliente controla el dispositivo.
- Commit `a1a1ba0` subido a origin/dev_v2, por autorización expresa del usuario.
  Ningún archivo funcional se incluyó en ese push.

## 12/10/2026 — Fase 1, T1–T2: datos aislados y versión

- `INVENTARIOS_DATA_DIR` resuelve rutas relativas/absolutas. Predeterminado `.local/dev_v2`.
  SQLite/media originales se preservan; no se versionan copias, credenciales ni capturas.
- `backups/prepare_dev.py` prepara snapshot SQLite en modo lectura y copia media;
  rechaza sobrescribir un destino existente. Dos pruebas verifican independencia y límites.
- Se corrigió cierre explícito de conexiones SQLite durante las pruebas de copia en Windows:
  el context manager de sqlite3 controla la transacción, pero no cierra la conexión.
- Fuente única `config/version.py`, contexto de plantilla y zona America/Bogota.
  Sin actualización de dependencias ni instalaciones globales.

## 12/10/2026 — Fase 1, T3–T4: integridad de inventario

- Se aplicaron `incremental-implementation`, `test-driven-development`,
  `git-workflow-and-versioning`; se consultaron UI, seguridad, revisión y Definition of Done.
  Fuente solicitada: addyosmani/agent-skills. Revisión main observada al cierre:
  `1be8e34187e34647bb83adc3a1323b26ae6f6abe`. Lecturas vía documentación remota,
  sin ejecutar scripts del repositorio externo.
- La skill de pruebas pide un subagente para reproducir bugs complejos. Un subagente
  escribió y amplió exclusivamente `apps/inventory/test_integrity.py`; el agente principal
  implementó y revisó el cambio. Sin delegación del push ni acceso a datos personales.
- Reproducción inicial: re-guardado 13→16; instancias cacheadas dejaban 14 en lugar de17;
  edición/borrado y límites sin protección. Las pruebas fallaron antes de corregir.
- Movimientos en atomic + actualización condicional F; protección compatible con SQLite,
  sin confiar en bloqueo de filas. SQLite IMMEDIATE y timeout10; pueden existir bloqueos
  si hay otros procesos. Prueba concurrente admite/reintenta bloqueos y verifica un solo
  consumo válido al competir dos salidas7 por saldo10.
- Historial inmutable en modelo/QuerySet/Admin. Cantidad existente sólo cambia con
  movimientos; límites se validan al guardar. PROTECT impide borrar stock/componente
  con historial; no fabricar saldo inicial para registros anteriores.
- Migración 0002 aplicada a la copia de desarrollo y base ficticia de revisión, no al original.
- Revisión detectó otra ruta de límites inválidos en Stock.save: prueba roja añadida y corregida.
- Mutación controlada del signo de salida produjo fallo saldo20 frente a0; se restauró
  el código correcto. Las pruebas comprueban comportamiento, no sólo ejecución.

## 12/10/2026 — Fase 1, T5–T6: alta rápida y navegación

- Formulario propio con categoría, referencia, nombre, campos opcionales y stock.
  Servicio transaccional crea componente/stock y entrada inicial positiva, con rollback
  ante error. No hay movimientos cero ni duplicación al repetir referencia/categoría.
- Rutas `/components/new/`, `/accounts/login/` y logout POST. Autorización exige permisos
  add_component, add_stock y add_stockmovement; superusuario existente puede operar.
  Reutiliza autenticación Django; no asigna roles automáticamente.
- Base compartida, CSS local, navegación, pie de versión y mensajes en español.
  Búsqueda/resumen integrados sin cambiar sus reglas; paginación sigue para Fase 2.
- 10 pruebas de alta/servicio incluyen cantidades, duplicados, rollback, permisos,
  usuario no staff autorizado, CSRF, login/logout y guardar/agregar otro. Pruebas rojas
  por rutas/servicio inexistentes antes de implementar.

## Verificación de cierre y próximos pasos

- 50 pruebas correctas; manage.py check sin incidencias; makemigrations --check --dry-run
  sin cambios. No hay linter configurado en el repositorio; diff --check correcto.
- Navegador con base ficticia separada `.local/ui_review`: login, error de máximo sin
  pérdida de campos, guardar/agregar otro y catálogo con cantidad10. Revisión de teclado
  y formulario 320px: sin desbordamiento. Capturas en `.local/evidence/` fuera de Git.
  Dashboard mostró entrada inicial10 y Admin abrió correctamente. Registro de consola
  del resumen sin errores/advertencias. Servidores de prueba detenidos al terminar.
- El servidor de prueba requirió ejecución fuera del sandbox por bloqueo de sockets
  locales; sólo escuchó en localhost y usó datos ficticios.
- Comprobaciones finales de hash del SQLite original coinciden. No se cambiaron
  datos/adjuntos originales, `.venv_backup/` ni info_project.txt.
- Documentación de Fase 1 actualizada junto al código. Commits funcionales locales
  separados; no push ni merge del desarrollo, pendiente de revisión y autorización.
  Commits: `121ba8c` (aislamiento/versión), `54c5a59` (integridad/migración/pruebas),
  `ec8c228` (alta rápida/navegación). El cierre documental se guarda en otro commit local.
- Para revisión usar la copia de desarrollo y las credenciales habituales; no usar
  la cuenta ficticia de prueba. Fase 2 no comienza sin revisar este resultado.
- Límites pendientes: buscador/resumen siguen sin autenticación como antes, sin paginación;
  protección adicional de archivos y distribución con DEBUG=False son tareas posteriores.
  Backups generales/restore anteriores aún requieren servidor detenido y comprobación
  en copia: el helper de aislamiento no sustituye la mejora de recuperación de Fase 3.

## 12/10/2026 — Ampliación de Fase 1 solicitada en revisión

- Petición del usuario: igualar Administración a catálogo/resumen, interfaz en español,
  revisar PDF/usuarios/ubicaciones y replanificar hasta cuatro fases. No autoriza push.
- Administración: plantilla base propia y CSS con misma paleta/tipografía/navegación,
  versión visible. Mantiene las vistas, widgets, permisos y CSRF del Admin de Django.
  Cabecera móvil corregida tras reproducir desbordamiento de 562px a viewport375px;
  comprobación posterior sin desbordamiento. Formularios/listados revisados en navegador.
- Aplicaciones/modelos/campos/permisos traducidos mediante metadatos y etiquetas de
  formulario. Datos ingresados permanecen intactos, incluso nombres en inglés.
  Dos plantillas nativas adaptadas para etiquetas accesibles sin traducción española
  en Django 5.2.6: listado de aplicaciones y búsqueda administrativa.
- Altas de usuarios mediante UserCreationForm: contraseña obligatoria/confirmada y
  validada, hash Django y cuenta normal activa. No hay campos staff/superusuario.
  Gestión de usuarios restringida a superusuario; no se pueden borrar superusuarios
  desde esta pantalla. createsuperuser sigue disponible desde terminal. No se cambiaron
  privilegios ni contraseñas de cuentas existentes.
- Diagnóstico de login: Admin exige staff/activo; los usuarios normales usan
  /accounts/login/. Enlace/ayuda añadidos a ambos accesos. Pruebas verifican login de
  usuario recién creado, rechazo de cuenta inactiva y denegación de acceso administrativo.
  Sin datos adicionales no puede afirmarse si el fallo anterior era ruta, estado o clave.
  Referencia: https://docs.djangoproject.com/en/5.2/topics/auth/customizing/
- PDF: carga + _continue y segundo guardado sin archivo nuevo funcionaron en pruebas.
  Reproducción adicional: archivo persistido faltante provoca FileNotFoundError al
  consultar tamaño en clean(). Corregido para mostrar error de campo ante OSError;
  volver a adjuntar PDF recupera el formulario. Usuario sólo recuerda pantalla de
  error seguida de recarga; no hay evidencia para atribuirle la misma causa.
- Pruebas rojas antes de corregir: tres fallos de interfaz/cuentas y una excepción PDF;
  once pruebas nuevas de integración, suite completa de 61 pruebas pasa. check correcto,
  makemigrations --check --dry-run sin cambios. No se añadieron dependencias.
- Migraciones españolas: components.0002, documents.0002, inventory.0003 y suppliers.0002.
  Son de etiquetas, sin cambio de relaciones ni valores; aplicadas sólo a .local/dev_v2
  y .local/ui_review. El SQLite operativo original se conserva.
- Ubicaciones: OneToOneField desde Location a Component confirma la restricción actual.
  El plan sitúa primero en Fase 2 ubicación reutilizable y migración que conserva
  asignaciones; no se cambió esta relación durante el cierre de Fase 1.
- Nuevo orden: F1 base/admin/cuentas; F2 ubicaciones/permisos/ficha/PDF; F3 operación
  diaria dinámica; F4 recuperación/estabilización/Waitress/PyInstaller local.
  info_FASES, tasks, CHANGELOG y manual actualizados. Fases 2–4 no iniciadas.
- Cambios locales en dev_v2, pendientes de revisión del usuario; no push ni merge.
- Captura de revisión con datos ficticios: .local/evidence/fase1_admin.jpg (fuera de Git).
  Consola de navegador sin advertencias/errores. Cabecera móvil queda por encima de
  sus controles sin solapamiento; ancho de documento no supera viewport375px.
  Hash operativo comprobado de nuevo: B247D32672C3D77C9DF9F377C833061D79AAFF9A7010112AB9776096616F12E2.
  Servidor propio de prueba detenido; no se detuvo el servidor del usuario en 8001.

## 12/10/2026 — Cierre y publicación autorizados de Fase 1

- El usuario aprobó el resultado, pidió mejorar las acciones de sesión de su captura
  y autorizó subir toda la Fase 1 al repositorio. Fase 2 requiere aprobación posterior.
- Encabezado: avatar con inicial, identificación de sesión y dos botones separados,
  sin barra separadora ni textos pegados. Salir conserva POST/CSRF; cambio de contraseña
  conserva ruta nativa Django. Ningún cambio a cuentas ni contraseñas.
- Revisión visual en base ficticia .local/ui_review: escritorio y viewport375px sin
  desbordamiento; botones de 40px de altura. Captura .local/evidence/fase1_sesion.jpg.
  Consola sin advertencias/errores. Servidor de pruebas propio detenido al terminar.
- Regresión completa: 61 pruebas correctas; check sin incidencias;
  makemigrations --check --dry-run sin cambios; diff --check correcto.
- Documentación y control F1 actualizados. Fuente única de versión sigue
  2.0.0-dev.1: entrega de desarrollo de Fase 1, sin tag ni release final.
- Se actualizó la referencia remota mediante fetch: origin/dev_v2 no tiene commits
  exclusivos y permite publicación normal de los commits locales. Publicación
  autorizada exclusivamente a origin/dev_v2, sin force ni integración a dev/main.
- Al completar el push se comprueba igualdad de HEAD y origin/dev_v2 y ausencia de
  cambios pendientes en archivos versionados. Código/documentación de Fase 1 quedan
  juntos en esa rama. Datos, secretos, entornos y archivos personales preexistentes
  permanecen locales: .venv_backup/ e info_project.txt no forman parte de Fase 1.
