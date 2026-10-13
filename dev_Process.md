# Registro de desarrollo — InventariosAPP v2

Estado actual: **Fases 1, 2 y 3 publicadas; mejoras adicionales v2.2.0 aprobadas para publicar**.
Versión visible: `v2.2.0` (12/10/2026), publicación autorizada. Fase 4 no iniciada.
Las entradas siguientes conservan los estados históricos de cada avance.

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

## 12/10/2026 — Fase 2 autorizada, incluida edición de perfil

- El usuario autorizó iniciar Fase 2 y añadió una ventana para editar datos básicos
  del perfil de la sesión. Se mantiene dev_v2; no autoriza publicar esta fase.
- T7c: /accounts/profile/ con nombre/apellidos/correo, enlazado en aplicación y Admin.
  Instancia siempre request.user, sin ID de cuenta suministrado por cliente. Guardado
  restringido a esos tres campos. Pruebas verifican sesión conservada, correo inválido,
  CSRF, usuario anónimo e inyección de ID/username/privilegios sin efecto.
- Respaldo previo mediante prepare_development_copy de .local/dev_v2 a
  .local/checkpoints/fase1_before_fase2, SQLite consistente y media copiado.
- T7a: Component.location ahora FK opcional PROTECT; Location admite components.
  components.0003 añade columna; inventory.0004 copia asignaciones antes de quitar
  OneToOne antiguo. Conserva IDs y ubicaciones vacías, sin deduplicar por nombre.
  Migración reversible sólo mientras ninguna ubicación sea compartida; caso contrario
  exige respaldo y rechaza conversión con pérdida. Prueba de migración real con estado
  histórico verifica vínculo y saldo17. Copia real: 2 asignaciones y 10 saldos preservados.
- Pantalla /locations/ y editor permiten asignar varios componentes a ubicación creada;
  selección traslada desde otra y deselección libera. Formulario Admin adaptado también;
  cambios de asignación exigen permiso change_component. Ubicación ocupada no se elimina.
- T7b: grupos predefinidos Lector/Operador y comando configure_inventory_roles, sin
  asignación a cuentas existentes. Alta de usuarios elige perfil explícitamente, ambos
  sin staff/superusuario. Búsqueda/resumen exigen sesión/consulta; permiso individual
  add_component de Fase 1 mantiene consulta para operadores anteriores. PDF exige view_datasheet.
  Cuentas activas/grupos/contraseña utilizable se revisan en edición administrativa;
  no se resetean claves ni se publican datos de cuentas.
- T7/T8: ficha enlazada desde catálogo, datos/ubicación y formset de especificaciones
  en transacción. Duplicados no dejan guardado parcial; no toca Stock ni historial.
  IDs del formset restringidos al componente actual. Máximo50 filas, JS opcional y
  botón servido para agregar sin JS. Borrados exigen permiso delete_specification.
- T9: categoría y ubicación contextuales conservan datos y filas; se crean con botón
  específico, componente/asignación se confirman al guardar después. Errores abren el
  panel correspondiente. Pruebas rojas iniciales por rutas inexistentes antes de implementar.
- T11: formulario PDF en ficha, extensión/tamaño/cabecera, protección de descarga y
  media sin servir rutas arbitrarias. Registro ausente/archivo faltante devuelve404;
  FileResponse privado/no-store. Servicio limpia archivo escrito si falla INSERT.
  La validación es básica de formato, sin análisis completo del contenido.
  PDF registrado pero faltante muestra una pantalla propia en español con retorno
  a la ficha (HTTP404), evitando mostrar la página técnica de Django en ese caso.
  Fallos de base durante carga, incluido bloqueo SQLite, devuelven mensaje y limpian
  la carga fallida; prueba con IntegrityError y OperationalError. No se atribuye a esa
  causa el error intermitente anterior, que no tuvo mensaje de excepción disponible.
- Revisión de navegador: perfil guardado con sesión vigente, especificaciones JS,
  creación contextual de Caja de sensores sin perder campos, guardado con saldo10,
  alta de segundo componente y asignación de ambos a ubicación existente. Base ficticia
  .local/ui_review exclusivamente. Perfil375px sin desbordar. Capturas fase2_perfil,
  fase2_ficha y fase2_ubicaciones en .local/evidence fuera de Git.
  Perfil y ficha editable a375px sin desbordamiento; consola sin advertencias/errores.
  Servidor propio de pruebas detenido, sin detener el servidor del usuario en8001.
- Detectado banner de errores al recibir formset válido (lista de diccionarios vacíos
  evaluada como true); corregido por total_error_count y cubierto con regresión.
- 83 pruebas correctas. Prueba de PDF adaptada para cerrar respuestas streaming,
  evitando bloqueo de temporales en Windows; no afecta servicio de archivos de Django.
  Fixture de PDF del dashboard aislado también en MEDIA_ROOT temporal, para que las
  ejecuciones siguientes no escriban archivos de prueba en la copia de desarrollo.
  check/makemigrations --check --dry-run correctos. Hash original coincide con Fase 1:
  B247D32672C3D77C9DF9F377C833061D79AAFF9A7010112AB9776096616F12E2.
- Versión 2.0.0-dev.2, fecha12/10/2026. Documentación/tareas actualizadas. Fase 2
  implementada localmente, Control F2 espera revisión del usuario. Sin push ni merge;
  Fase 3 no iniciada. Datos originales y archivos preexistentes ajenos conservados.

## 12/10/2026 — Aprobación de Fase 2 y simplificación de versión

- El usuario aprobó subir Fase 2. Implementación en commit `5c9a6f4`.
- Se adopta versión visible `v2.0.0`, sin sufijo dev; fuente numérica `2.0.0` en
  config/version.py y prefijo v desde el contexto compartido. Fecha 12/10/2026.
- Manual, plan, tareas y CHANGELOG actualizados; historia anterior conservada.
- Se confirma uso de la colección Agent Skills: planificación, implementación
  incremental, TDD, UI, seguridad, revisión y versionado, con lecturas y revisión
  de origen documentadas arriba. No hubo instalación global ni ejecución de sus scripts.
- Publicación autorizada únicamente a dev_v2, sin integrar dev/main. Fase 3 no iniciada;
  su aprobación queda pendiente de la revisión del usuario.
- Verificación del cambio de versión: 18 pruebas de administración/alta rápida correctas; check y git diff --check sin incidencias. Se mantiene la evidencia de 83 pruebas de Fase 2.

## 12/10/2026 — Inicio autorizado de Fase 3: interfaz compartida

- Usuario autorizó Fase 3; publicación pendiente de revisión y aprobación separada.
- Bloque de sesión común según imagen: avatar, sesión activa, Mi perfil, cambiar contraseña y salir con POST/CSRF, tanto en vistas propias como Admin.
- Cambio de contraseña para usuarios normales conserva sesión usando vistas nativas Django. Encabezados de Componentes centrados en catálogo y Admin.
- v2.0.1 para este ajuste; 10 pruebas de sesión/Admin correctas y check sin incidencias.
- Consultadas incremental-implementation y frontend-ui-engineering de Agent Skills en la revisión previamente registrada. Referencia visual: imagen proporcionada por el usuario; misma paleta existente, controles adaptables y teclado.

## 12/10/2026 — Fase 3, T14: catálogo filtrado y resumen

- Filtros combinables por categoría, disponibilidad y pendientes; orden estable y paginación de 25. Enlaces conservan búsqueda/filtros.
- Resumen enlaza indicadores a los mismos filtros y movimientos a la ficha.
- Ocho pruebas de catálogo/resumen correctas. Categorías inválidas o fuera de rango se ignoran.
- Versión v2.1.0 por funcionalidades compatibles nuevas. Implementación local, sin push.

## 12/10/2026 — Fase 3, T13: movimientos desde ficha

- Entrada/salida/ajuste con motivo obligatorio, vista previa en servidor y verificación del saldo antes de confirmar.
- Token firmado por sesión/componente con identificador único persistente evita aplicar nuevamente un envío repetido; historial permanece inmutable.
- Migración aditiva inventory.0005 aplicada sólo a la copia de desarrollo, tras snapshot .local/checkpoints/fase2_before_fase3. Movimientos previos conservan identificador nulo.
- 26 pruebas de flujo/integridad correctas; ajuste de validación de vista previa y repetición verificado con seis pruebas del flujo. Salidas insuficientes, límites, permisos, CSRF y rollback cubiertos.
- Sin push ni cambios en base operativa original.

## 12/10/2026 — Fase 3, T10: duplicación técnica

- Copia categoría, valor, número de parte y especificaciones con referencia nueva. Stock cero, sin ubicación, historial, PDF ni ofertas.
- Guardado atómico y permisos para alta/especificaciones. Tres pruebas correctas: copia selectiva, rollback y rechazo sin permisos.
- Se corrigió la prueba del saldo original para consultar la base en vez de una relación cacheada; el saldo original se conserva.

## 12/10/2026 — Fase 3, T12/T15: ofertas, revisión y cierre local

- Proveedores: consulta/búsqueda/alta/edición propias. Ofertas desde la ficha con
  componente fijado por servidor y rechazo de precio negativo, compra mínima cero,
  URL inválida, duplicados y edición desde otro componente.
- Proveedor contextual conserva importe, moneda y parte; guarda independientemente
  del guardado posterior de oferta. Grupos Operador ampliados mediante comando en
  la copia local, sin cambiar membresías ni privilegios administrativos.
- Contexto de ficha compartido con errores de PDF para conservar historial y ofertas;
  historial completo en páginas de 25, permisos de consulta comprobados.
- Consultadas security-and-hardening y code-review-and-quality de Agent Skills en
  revisión 1be8e34187e34647bb83adc3a1323b26ae6f6abe. Límites de confianza: POST,
  IDs, token, permisos y URLs; validación de servidor, CSRF, autoescape y transacciones.
  La skill de revisión pide otro modelo: revisor independiente, sólo lectura de código,
  sin consultar datos reales ni publicar. Identificó required en proveedor contextual
  bloqueando Guardar oferta en navegador; corregido con use_required_attribute=False
  sólo para presentación, validación de nombre obligatoria conservada en servidor.
  Revisión final sin bloqueantes; desempate por pk y permiso condicional de Duplicar
  también corregidos. No se afirma una auditoría completa de distribución (Fase 4).
- Mutación controlada: invertir el rechazo de saldo obsoleto hizo fallar su prueba;
  archivo restaurado antes de regresión final. La prueba detecta pérdida de ese control.
- Regresión final: 108 pruebas correctas; check sin incidencias y migraciones coherentes.
  Incluye token vencido/otra sesión, ID de operación inmutable, salida grande reenviada,
  creación de stock ausente, paginación de historial y proveedor contextual opcional.
- Navegador en .local/ui_review_fase3 con datos ficticios: salida3 desde saldo10,
  vista previa7 sin guardar y confirmación con saldo7/historial; oferta con proveedor
  existente y contextual conserva importe8000/parte; copia técnica con saldo0,
  especificaciones y sin ubicación/ofertas/historial. Filtros categoría/disponibilidad
  muestran un resultado correcto. Logout devuelve login; Tab desde Mi perfil llega
  a Cambiar contraseña. Encabezados centrados verificados también en Admin.
- Ficha comprobada a320/768/1024/1440px sin desbordamiento del documento; catálogo
  a375px conserva botones de sesión. Consola del catálogo sin errores/advertencias.
  Capturas fase3_catalogo.png y fase3_catalogo_movil.png en .local/evidence, fuera de Git.
- Comparación estructural del mismo caso (categoría existente, componente nuevo,
  stock cero y entrada10 con historial): formularios separados de Admin requieren
  tres guardados (componente, stock, movimiento); alta rápida requiere un guardado
  que crea los tres registros. No se midieron tiempos. Para operación posterior,
  Fase 2 requería Administración; Fase 3 abre el movimiento desde su propia ficha,
  selecciona el componente en servidor y permite vista previa sin JavaScript.
- Comparación de snapshot previo con copia de desarrollo: 10 saldos y 10 movimientos
  anteriores conservados; integridad SQLite ok. SHA-256 de db.sqlite3 operativo:
  B247D32672C3D77C9DF9F377C833061D79AAFF9A7010112AB9776096616F12E2, sin cambios.
- Manual, CHANGELOG, README, plan y tareas actualizados para v2.1.0. Control F3 queda
  pendiente de revisión/aprobación del usuario; ningún push, merge ni inicio de Fase 4.


## 12/10/2026 — Usabilidad y cierre autorizado de Fase 3, v2.1.1

- El usuario solicita aclarar las opciones del alta, corregir la asimetría superior,
  subir los cambios y esperar su aprobación para iniciar Fase 4.
- Se mantiene categoría/referencia/nombre porque identifican el componente. La ubicación
  sigue opcional. «Valor» pasa a «Valor técnico»: describe resistencia, capacitancia o
  tensión; no dinero. El número de parte se identifica como código del fabricante.
  Se conservan ambos campos opcionales para compatibilidad y búsqueda; sin eliminar datos
  ni agregar campos redundantes. Atributos adicionales van en especificaciones; precios,
  en ofertas existentes. Datos técnicos y límites quedan desplegables con ayudas.
- Cabecera compartida: marca y sesión alineadas; navegación en una fila completa debajo.
  En móvil se apilan de forma explícita. Estilos incluidos también en Administración.
- Migración components.0004 de metadatos aplicada exclusivamente a .local/dev_v2 y
  .local/ui_review_fase3. La revisión automática rechazó el primer comando porque no
  expresaba el destino antes de migrar; no se ejecutó. La versión corregida fija ambos
  destinos explícitamente y fue aprobada. No queda bloqueo.
- SHA256 de db.sqlite3 original sigue siendo
  B247D32672C3D77C9DF9F377C833061D79AAFF9A7010112AB9776096616F12E2.
- Regresión: 108 pruebas correctas (92.669 s); check sin incidencias y makemigrations
  --check --dry-run sin cambios. Alta visual ficticia RES-PRUEBA conserva 10 kΩ y 2 unidades.
  Catálogo sin desbordamiento horizontal a 320, 768 y 1024 px; Administración revisada
  en escritorio y 320 px. Evidencia local: .local/evidence/fase3_usabilidad_catalogo.png
  y fase3_usabilidad_formulario.png (capturas ficticias, no versionadas).
- Manual, CHANGELOG, plan, tareas y README sincronizados con v2.1.1. Se conserva el
  historial de avances. Publicación normal de toda Fase 3 en dev_v2 autorizada;
  sin merge a dev/main. Fase 4 requiere una nueva aprobación del usuario.


## 12/10/2026 — Perfil, contraseña y exportación PDF, v2.2.0 local

- Fase 3 fue publicada y comprobada en remoto/local: 4dd6142. El usuario solicita
  estas mejoras antes de aprobar Fase 4; su implementación no autoriza publicar ni empezar F4.
- ProfileForm incorpora UsernameField para normalización y validación de caracteres,
  rechazo de nombres existentes sin distinguir mayúsculas; instancia fijada a request.user.
  Se guardan únicamente username/nombre/apellidos/email, con manejo de conflicto único.
  No cambia ID, contraseña ni privilegios. Ante error se restaura el usuario de la cabecera.
- Widget propio de contraseña muestra estado y enlace habitual de Django; no incluye
  valor/hash en contexto ni resumen criptográfico. Mantiene el campo disabled de UserChangeForm.
- Consulta filtrada extraída a función común para catálogo y descarga PDF. Exportación
  GET autenticada con permisos, todas las páginas activas, sin caché y sin archivos intermedios
  de usuarios. ReportLab 4.5.1 incorporado al entorno virtual y requisitos; sin instalaciones globales.
- Aplicada skill PDF para generación y verificación visual. Fuentes Vera integradas,
  texto escapado, columnas proporcionadas, filas divisibles y cabeceras repetidas.
  Referencia técnica: https://docs.reportlab.com/reportlab/userguide/ch7_tables/.
- Correcciones durante verificación: plantilla del widget ubicada en templates de la app
  para que el renderizador de formularios la encuentre; corregida codificación UTF-8 de
  etiquetas, y prueba de enlace ajustada al destino relativo habitual de Django.
- Regresión completa: 115 pruebas correctas en 114.092 s; check sin incidencias,
  makemigrations --check --dry-run sin cambios y pip check sin incompatibilidades.
  Casos nuevos: sesión/login después de renombrar, nombres inválidos/duplicados, inyección
  de privilegios/contraseña, estado sin clave y PDF con permisos/filtros/todas las páginas/vacío.
- QA aislada: .local/ui_review_fase3, sin modificaciones de datos reales. Navegador comprueba
  perfil y estado de contraseña; descarga componentes-2026-10-12.pdf. Informe sintético
  de 90 filas y nombres largos, 8 páginas: extracción confirma extremos, acentos, µ/Ω y
  cabeceras repetidas; páginas 1 y 8 renderizadas e inspeccionadas. Evidencia en .local/evidence.
- Base original mantiene SHA256 B247D32672C3D77C9DF9F377C833061D79AAFF9A7010112AB9776096616F12E2.
- Actualizados manual, CHANGELOG y estados del plan. v2.2.0 refleja nuevas funciones compatibles.
  Cambios locales en dev_v2 para revisión; sin push ni inicio de Fase 4.


## 12/10/2026 — Informe ejecutivo y publicación autorizada de v2.2.0

- El usuario pide el informe ejecutivo de las 115 pruebas y subir los cambios.
- Se revisa el resultado completo: 115 aprobadas, cero fallos/errores/omisiones,
  114.092 segundos. La suite descubierta confirma el recuento por módulo (115).
- INFORME_EJECUTIVO_PRUEBAS.md agrupa el alcance en siete áreas y distingue éxito
  de ejecución de cobertura de código; separa comprobaciones visuales y límites de Fase 4.
- No se repite una suite ya aprobada: desde e548970 solo cambia documentación,
  sin modificaciones funcionales. El informe referencia ese commit de implementación.
- Documentos de estado actualizados a publicación aprobada. Se conserva el historial.
- Publicación normal autorizada en dev_v2; no incluye merge a dev/main ni inicio de Fase 4.


## 12/10/2026 — Fase 4 autorizada: v2.3.0 candidata

- El usuario autoriza el trabajo pendiente y pide .exe con base nueva vacía, terminal
  e instrucciones para seguir desarrollando/reconstruir. No autoriza un nuevo push.
- Lanzador único (`launcher.py`): Waitress solo 127.0.0.1, init, comandos Django,
  backup/restore, carpeta configurable y bloqueo entre servidor/mantenimiento.
  Fuente con runserver para desarrollo; distribución con DEBUG=False y WhiteNoise.
- Base/media/clave fuera del ejecutable, por defecto LocalAppData/InventariosAPP/data.
  Primera instalación vacía, administrador con createsuperuser, sin clave predeterminada.
  init/actualizaciones preservan registros; snapshot previo si hay migraciones pendientes.
- backup_local usa API SQLite de snapshot, integridad, manifiesto SHA256 y publicación
  de carpeta temporal validada. Restore reemplaza base/media/clave y conserva previous;
  ante fallo de instalación devuelve el destino original. No mezclan media sobrante.
- Se descubrió que el hook estándar PyInstaller de Django podía incluir db.sqlite3
  del proyecto. Se reemplaza con hook de recursos explícitos y controles tanto en spec
  como en archivo generado. Ninguna base ni media del usuario entra en el paquete.
- build_exe.py genera estáticos, exe con consola, metadatos SHA/versiones y avisos
  de licencia. requirements-build separado. Django actualizado a 5.2.18 dentro de LTS
  tras revisar las actualizaciones oficiales de seguridad; ninguna migración de app nueva.
- Primer pase con Django 5.2.6: 125 pruebas correctas en 133.421 s. Pase final con
  Django 5.2.18: 125 correctas en 121.355 s; pip check y migraciones coherentes.
  Diez casos nuevos: seis recuperación y cuatro runtime. Sin tests con datos personales.
- QA del código final: navegador con Waitress, vistas/perfil/admin, estáticos hash,
  PDF/datasheet/permisos y movimiento con vista previa/reenvío. Saldo ficticio 10→7.
  Backup mientras está abierto rechazado. Restore real recupera 7 desde estado ficticio
  99 conservado en previous, sin mezclar archivos; actualización previa obtiene backup.
- Primer exe experimental sin Python en PATH hizo init vacío/creación de cuenta ficticia.
  El .exe final Django 5.2.18 se construye correctamente (31.713.511 bytes), pero Windows
  lo bloquea por Smart App Control (firma NotSigned, eventos CodeIntegrity 3033/3077/3118).
  No se cambia la seguridad del PC ni se declara validación completa del binario final.
- Datos operativos originales intactos, hash original verificado. Carpeta dev_v2 preservada.
- Documentación y estados actualizados; guía detallada de terminal, build, actualización,
  recuperación y bloqueo de firma. INFORME_VALIDACION_FASE4.md distingue suite, código
  final, artefacto y límites. T19/control F4 pendientes; sin push ni release final.

- Consultado si existe certificado de firma de un proveedor reconocido; el usuario
  responde que no dispone de certificado. No se adquiere ni se cambia Smart App Control.
  Se entrega candidato con guía y alternativa de ejecución desde fuente; firma y QA
  final del binario continúan pendientes. No se publica una release final.


## 12/10/2026 — UI UX Pro Max antes de reconstruir onedir (v2.3.1)

- Usuario autoriza limpiar artefactos PyInstaller anteriores y pide primero mejorar
  absolutamente toda la UI con nextlevelbuilder/ui-ux-pro-max-skill.
- Skill descargada por skill-installer en .local/tools/skills, aislada del sistema global.
  Leídos SKILL.md y referencias quick-reference/pro-rules; ejecutado generador por ruta
  absoluta y búsquedas de error-summary/foco. El stack real es Django/HTML/CSS propio;
  no se fuerzan React/Tailwind ni recomendaciones de marketing/tipografía fuera de contexto.
- Sistema verificado/adaptado documentado en design-system/inventariosapp/MASTER.md.
  Paleta verde/gris, fuente Segoe UI local y SVG propios; nada requiere Internet en la app.
- Theme común más CSS de aplicación/header/session/admin; navegación compartida y activa,
  orden DOM alineado con orden visual, tarjetas de resumen, tabla de movimientos,
  ubicaciones, catálogo/exportación, formularios y estados 403/404/500/PDF coherentes.
- ui.js añade descripción accesible, estado inválido, resumen de errores enfocable con
  enlaces, regiones de tabla para teclado y controles de mostrar/ocultar contraseña.
  No intercepta ni desactiva botones de guardado: mantiene submitters y datos de formularios.
- QA con datos ficticios en .local/ui_review_fase4. Suite: 125 correctas en 98.047 s.
  PDF: tres casos repetidos tras paleta, correctos en 0.747 s. Renderizado de 23 vistas,
  404/500, PDF y roles Lector/Operador verificados. Formularios inválidos: tres enlaces,
  tres campos inválidos y foco en resumen. Toggle probado sin cambiar credenciales.
- Navegador: catálogo/resumen/ubicaciones/proveedores/alta/ficha/edición/duplicación/
  movimientos/ofertas/perfil/contraseña/Admin, incluidos usuarios y selectores nativos.
  Pantallas 375/768/1024/1440 px: sin scroll horizontal del documento; tablas tienen
  scroll propio. Corregido overflow inicial Admin y selector elegido de bajo contraste.
  Texto principal/secundario/acción/error: 12.87/5.94/6.72/6.23; borde de control 3.15.
- Limpieza acotada, con rutas absolutas comprobadas y sin enlaces: dist/v2.3.0, ZIP
  previo, .local/pyinstaller_build, copia .exe de fase4_execution, collected_static y
  build_profile. No se elimina db.sqlite3/media/dev_v2 ni los respaldos/evidencias QA.
- Spec y builder pasan a onedir: EXE + COLLECT, verificación del contenido de toda la
  carpeta, collectstatic limpio, licencias, SHA256SUMS.txt y ZIP. PyInstaller 6.22.0 se
  mantiene; cambio de formato no constituye garantía ni excepción de Smart App Control.
- SHA256 original conserva B247D32672C3D77C9DF9F377C833061D79AAFF9A7010112AB9776096616F12E2.
  Candidato local en dev_v2; sin push ni cambio de protecciones.

- Primer onedir: Windows permite --version e init vacío/restauración sin firma, con
  PATH sin Python. Copia extraída fuera del proyecto y con espacios. Smoke detecta
  recurso common-passwords.txt.gz omitido por el hook explícito de Django al consultar
  cambio de contraseña. Se incluye el recurso oficial y se reconstruye; no se desactiva
  CommonPasswordValidator. Se añade esa comprobación al smoke del paquete final.

- La recompilación del recurso fue bloqueada por Windows. Comparación estricta con el
  lanzador aceptado: mismo archivo Python embebido y mismos scripts; seis bytes de fechas
  PE/debug y checksum distintos. Base_library.zip contiene módulos idénticos, distinto
  contenedor. El resto de recursos coincide; falta solo la lista pública Django.
- Se conserva copia exacta del lanzador aceptado (SHA 7d0e9b3c4e9ce64328d05065ba9636f4daf3b7da11b8f4c589db7c6b457848a4)
  con recursos corregidos. No se editan bytes de exe ni políticas/certificados Windows.
  Helper --reuse-launcher exige binario idéntico salvo metadatos PE y rechaza otro byte
  de diferencia (comprobado en memoria), impidiendo reutilizar otra versión/código.
- Smoke final congelado: 23 vistas, siete estáticos hash, PDF/datasheet/permisos/roles,
  estado de contraseña y rechazo de contraseña común. Movimiento 120→117; preview sin
  escritura y reenvío idempotente. Cuenta ficticia creada por terminal; sin datos del usuario.
- Ejecución en carpeta externa al proyecto con espacios y PATH sin Python. HTTP real
  desde exe con Waitress/DEBUG=False muestra nuevo catálogo y resumen; capturas onedir_v231.
  Backup mientras está abierto rechazado, cierre Ctrl+C y copia/restore/init correctos,
  conserva 117 en otro destino. Instalación vacía conserva cero registros en diez tablas.
- Datos originales intactos. Destino es este PC; no se declara prueba en otro Windows limpio.
  Documentación refleja hechos, límite de confianza por archivo y proceso de reconstrucción.
  T16–T20 verificados localmente; candidato para revisión, sin push.

### Publicación autorizada de v2.3.1 — 12/10/2026

- El usuario confirma que el ejecutable abre en su PC y autoriza subir todos los
  cambios pendientes a dev_v2, incluyendo únicamente el ZIP de la distribución.
- Se incluye dist/v2.3.1/InventariosAPP-v2.3.1-Windows-x64.zip mediante una excepción
  específica de .gitignore. La carpeta expandida, entornos, datos y artefactos de
  prueba permanecen fuera del control de versiones.
- SHA256 del ZIP: A740F96B023E23AF44DBF9FD455DE877702CA80F3AC9B207C9B1E907449F5171.
- Se conserva el historial de desarrollo de Fase 4 y la documentación de v2.3.1.

### Automatización de preparación y arranque del código — 12/10/2026

- Se añaden preparar_proyecto.bat e iniciar_desarrollo.bat a petición del usuario.
  Usan su propia carpeta como directorio de trabajo, admiten rutas con espacios y
  mantienen los errores visibles con pausa. La preparación reutiliza el entorno
  Python 3.12 y no solicita otra cuenta si ya existe un administrador activo.
- Se crea la carpeta DATA_DIR configurada antes de migrate y se preparan los roles.
  Se conservan las bases y cuentas existentes. Guía y README actualizados.
- Cambio de herramientas de desarrollo; versión del aplicativo y ZIP sin cambios.
- A petición del usuario, iniciar_desarrollo.bat indica /admin/ como página de
  entrada, con autenticación administrativa. No invalida sesiones ya abiertas.
- Verificación en copia aislada con ruta con espacios e invocación desde otra carpeta:
  dependencias satisfechas, migraciones/perfiles y administrador existente conservado.
  Arranque Django 5.2.18 sin errores de sistema en puerto de prueba 8017; proceso de
  prueba detenido. No se modifica el inventario real. --sin-pausa disponible en terminal.
- El usuario autoriza documentar y publicar estas herramientas en dev_v2.
  Se actualizan guía, README, manual y CHANGELOG; se mantiene v2.3.1 y el ZIP
  publicado, pues no cambia el código de ejecución del aplicativo empaquetado.

### Arquitectura y cierre aprobado — 12/10/2026

- El usuario considera estable dev_v2 y autoriza merge a main: realizado sin
  conflictos en 412a0bc; contenido idéntico a dev_v2 y Django check sin problemas.
- Solicita skill tt-a1i/archify y publicación de arquitectura/ en ambas ramas.
  Skill descargada en .local/tools/skills/archify; paquete 3.0.1, sin dependencias
  nuevas de ejecución. Se inspeccionan fuentes fijadas a e55a3f3.
- HTML español generado desde candidate.json: finalize pasa validate/deliver/check/
  browser-check sin diagnósticos. visual-check pasa cuatro capturas; se inspeccionan
  1440x900 claro y 2048x1320 oscuro. Se conservan recibos, capturas y licencias.
- Documentados módulos, modelo relacional, transacciones, permisos, PDF, persistencia,
  respaldo/restauración y límites. Se marca arquitectura previa como histórica.
- Datos del .exe confirmados por runtime_local: %LOCALAPPDATA%/InventariosAPP/data;
  db.sqlite3, media y .runtime-key fuera del programa. Manual y guía actualizados.
- El usuario inicia ejecución/pruebas con el .exe; futuro desarrollo en dev_v2.
  Cierre documentado en CIERRE_Y_PRUEBAS.md. Se mantiene versión y ZIP v2.3.1.
