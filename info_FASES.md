# InventariosAPP — Plan de nueva versión

Fecha de análisis: 12/10/2026. Estado: **Fases 1, 2 y 3 publicadas; mejoras adicionales locales en revisión**.
El usuario autorizó iniciar Fase 3 y unificar el encabezado de sesión en todas las vistas.
Fase 3 publicada en v2.1.1. Perfil/contraseña/exportación PDF v2.2.0 pendientes de aprobación; Fase 4 no iniciada.
Versión visible local: `v2.2.0`, fecha `12/10/2026`.
Plan ampliado a **cuatro fases** por solicitud del usuario: los pendientes de usuarios,
PDF y ubicaciones se incorporan antes de ampliar la operación diaria y distribuir.
Actualización del 12/10/2026: el usuario autorizó crear y subir `dev_v2` con esta
documentación antes de iniciar Fase 1. Destino confirmado: su PC Windows, uso local,
con empaquetado PyInstaller al finalizar. Posteriormente autorizó iniciar Fase 1.
Este archivo corresponde a `info_Fases.md` solicitado: en Windows ambas grafías
resuelven al mismo archivo. Se conserva el nombre registrado en Git y el historial
original al final para no perder trazabilidad.

## Objetivo y límites

Reducir el trabajo necesario para registrar componentes y mantener su inventario,
partiendo del aplicativo funcional existente. No se reconstruirá desde cero.
La aprobación de este plan autorizará crear `dev_v2` desde el estado actual e iniciar
únicamente Fase 1. Fases 2, 3 y 4 quedan propuestas para revisión posterior.
Ningún push, integración en `dev`/`main` ni publicación se hará sin aprobación explícita.

Supuestos: uso principal local en Windows, un administrador, Django con plantillas,
SQLite y una ubicación por componente, compartible entre varios componentes en Fase 2.
Se propone mantener herramientas gratuitas,
sin SPA ni servicios externos obligatorios. Uso en red o varios usuarios simultáneos
requiere revisar despliegue, permisos y concurrencia antes de habilitarlo.

## Diagnóstico basado en el código

- Base: rama `dev`, commit `842afd1`; Django 5.2.6 y python-decouple 3.8.
- Hay categorías, componentes, especificaciones, ofertas, ubicaciones, stock,
  movimientos y PDF. Django Admin permite mantenerlos; buscador y dashboard son propios.
- `ComponentAdmin` integra especificaciones, pero stock, ubicación y PDF se gestionan
  por separado. No existe todavía una pantalla propia para crear componentes.
- Las plantillas de búsqueda y dashboard son HTML básico, sin una navegación común.
- La búsqueda consulta referencia, nombre, valor, part number y categoría; no tiene
  paginación real aunque README la menciona.
- `StockMovement.save()` aplica el movimiento cada vez que se guarda, también si ya
  existía. La creación y actualización del saldo no están en una transacción explícita.
  Editar/eliminar movimientos o editar directamente el saldo puede desalinear historial.
  La suite no cubre esas operaciones ni concurrencia.
- Buscador y dashboard no exigen autenticación en sus vistas. Los PDF se sirven por
  rutas de desarrollo cuando DEBUG está activo. Esto debe revisarse para uso en red.
- La validación de datasheets comprueba extensión y tamaño, pero no su contenido.
- El respaldo copia archivos: falta verificar consistencia con la base en uso y una
  restauración que no deje archivos antiguos mezclados con los restaurados.
- Configuración actual: Europe/Madrid, DEBUG por defecto activo y sin STATIC_ROOT.
- No se encontró fuente de versión `__version__` ni `FECHA_VERSION` en apps/config.
- Verificación del 12/10/2026: 18 pruebas pasan; `manage.py check` sin incidencias.
  No se inspeccionaron los datos personales de la base ni se validó visualmente el navegador.

## Uso de las skills compartidas

El enlace corresponde a una colección. Se consultó y aplicó
[planning-and-task-breakdown](https://github.com/addyosmani/agent-skills/blob/main/skills/planning-and-task-breakdown/SKILL.md)
para ordenar tareas con aceptación y verificación. La
[guía de adopción](https://github.com/addyosmani/agent-skills/blob/main/docs/adoption-guide.md)
orienta la incorporación gradual en proyectos existentes. Sus documentos son guía
técnica; tus instrucciones sobre rama, archivos y aprobación tienen prioridad.
Se consultó también spec-driven-development como referencia; sus convenciones de
archivos y etapas no sustituyen el plan solicitado, ampliado ahora a cuatro fases.

No se instaló globalmente el paquete ni se ejecutaron sus scripts. Durante el desarrollo
se leerán las skills aplicables de implementación incremental, pruebas, UI, seguridad,
revisión y versionado antes de usarlas. Se registrará la revisión consultada para
reproducir el proceso. Índice técnico: `tasks/plan.md`; tareas: `tasks/todo.md`.

## Fase 1 — Integridad y primer flujo de alta rápida

**Resultado:** crear un componente y su stock desde una pantalla propia, con un único guardado.

1. Crear `dev_v2` después de aprobación, partiendo del estado actual de `dev`;
   registrar commit de origen y conservar archivos locales preexistentes.
   Preparar una copia de trabajo de SQLite y media: una rama Git no aísla esos datos.
   Las pruebas y migraciones se harán sobre esa copia, preservando la base operativa.
2. Incorporar una fuente única en `config/version.py`, mostrar versión en la interfaz
   y asociar cambios y fecha a CHANGELOG. Ajustar zona horaria a America/Bogota.
3. Cubrir con pruebas y corregir movimientos: guardado atómico, saldo no negativo,
   límites coherentes y protección contra doble aplicación. Movimientos históricos
   serán inmutables; errores se compensarán con otro movimiento motivado. Bloquear
   edición directa de cantidad en Admin una vez registrado el saldo.
   Diseñar la actualización condicional compatible con SQLite; no asumir que
   select_for_update proporciona bloqueo de filas en SQLite.
4. Implementar alta mínima autenticada: categoría existente, referencia, nombre,
   valor/part number opcionales, cantidad inicial y límites de stock.
   Crear componente y stock en una transacción, con entrada inicial cuando sea > 0.
   Stock cero no genera movimiento de cantidad cero. Mantener protección de duplicados
   por categoría/referencia y mostrar errores junto a los campos.
5. Añadir plantilla compartida, navegación, mensajes en español, botón Nuevo componente
   y opciones Guardar / Guardar y agregar otro. Conservar Django Admin como herramienta
   de mantenimiento. Definir autorización con permisos Django en las nuevas vistas.
6. Ampliación solicitada al revisar: igualar diseño de Administración con catálogo/resumen;
   traducir aplicaciones, modelos, campos y permisos sin traducir valores ingresados.
   Crear cuentas normales con contraseña mediante Administración, sin habilitar opciones
   de promoción administrativa. Superusuarios nuevos sólo mediante `createsuperuser`.
   Aclarar login de usuarios y validar carga/edición de PDF con guardar y continuar.

**Aceptación:** alta con un solo envío; stock disponible inmediatamente; datos inválidos
no dejan registros parciales; re-guardar un movimiento no duplica saldo; salidas
insuficientes se rechazan; los flujos antiguos siguen funcionando. Actualizar manual
y registro de proceso con evidencia real. Revisión contigo al cerrar Fase 1.

## Fase 2 — Ubicaciones compartidas, permisos y ficha completa

**Dependencia:** Fase 1 validada.

**Resultado:** completar y consultar un componente sin recorrer varios modelos de Admin.

1. Separar ubicación de componente: cada componente podrá seleccionar una ubicación,
   y varios componentes podrán usar la misma. Migración aditiva en copia, conservar
   cada asignación existente y su identificación; no fusionar registros por texto sin
   revisión. Editar una ubicación existente permitirá asignar componentes adicionales.
   Probar migración con ubicaciones vacías/asignadas y confirmar que saldos/PDF no cambian.
2. Definir perfiles lector/operador por grupos y permisos, administración reservada;
   auditar cuentas inactivas/contraseñas inutilizables sin divulgar ni resetear credenciales.
   Proteger búsqueda/resumen según perfil y probar sesión, 403 y cuentas existentes.
   Añadido por el usuario al aprobar esta fase: pantalla «Mi perfil» autenticada que
   edita nombre, apellidos y correo sólo de la cuenta de la sesión. No cambia usuario,
   contraseña, estado ni permisos; probar CSRF, datos inválidos y manipulación de IDs.
3. Ficha con edición de datos y selección/creación de ubicación; especificaciones en filas
   agregables/eliminables, con validación de atributo duplicado.
4. Alta contextual de categoría sin perder lo escrito.
5. Adjuntar PDF desde la ficha con límite de 20 MB, validación adicional de contenido,
   acceso autorizado y manejo de archivos fallidos sin huérfanos. Reprobar guardar y
   continuar con carga/reemplazo y conservar archivo existente sin volver a adjuntarlo.
   Si reaparece el fallo intermitente informado, registrar excepción y pasos concretos.

**Aceptación:** varios componentes comparten una ubicación y las asignaciones anteriores
se conservan; usuario normal activo entra al aplicativo con sus permisos; ficha permite
completar especificaciones/categoría/PDF sin perder campos ante errores. Cuentas
superusuario no se crean desde la interfaz. Revisar con el usuario antes de Fase 3.

## Fase 3 — Operación diaria dinámica

**Dependencia:** Fase 2 validada.

1. Acciones Entrada, Salida y Ajuste desde la ficha; ajuste se presenta como diferencia
   con signo, con vista previa del saldo y motivo obligatorio. Mostrar historial.
2. Duplicación de datos técnicos con nueva referencia, sin copiar saldos/historial/PDF.
   Ofertas y proveedores como sección opcional, reutilizando reglas existentes.
3. Catálogo con filtros separados por categoría, disponibilidad y bajo stock, paginación
   de 25 registros y enlaces a ficha. Dashboard con indicadores que llevan al filtro
   correspondiente. Interfaz adaptable a móvil y teclado, con estados vacíos claros.

**Aceptación:** completar ficha, cargar PDF y registrar movimiento desde el flujo propio;
mantener filtros al paginar; conservar saldos de componentes existentes; validar campos
y permisos en servidor aunque falle JavaScript. Medir pasos del flujo anterior y nuevo
con el mismo caso; documentar resultados sin inventar tiempos. Prueba manual contigo.

## Fase 4 — Estabilización y distribución local

**Dependencia:** Fase 3 validada. Destino elegido: PC Windows local.

1. Ejecutar regresión funcional y revisión de permisos, CSRF, PDF y configuración.
   Revisar actualizaciones de seguridad de dependencias con fuentes oficiales y probar
   cualquier actualización. Medir consultas antes de optimizar.
2. Respaldos consistentes de SQLite y media, restauración verificable sobre carpeta
   aislada, documentación de recuperación y política de actualización sin perder datos.
3. Ruta propuesta para Windows: Waitress, arranque local sencillo, datos persistentes
   fuera del programa y servicio de estáticos/PDF diseñado para DEBUG=False. Preparar
   paquete con PyInstaller al finalizar; validar en Windows sin Python instalado.
4. Limitar la escucha a 127.0.0.1, permitir operación sin Internet y probar arranque,
   cierre y actualización local. El despliegue Linux/Gunicorn queda fuera del alcance:
   el usuario confirmó que la consulta se refería a otro proyecto.
5. Cerrar manual, CHANGELOG, dev_Process y notas de versión con resultados y limitaciones.
   Entregar candidato para tu revisión antes de subir cualquier cambio.

**Aceptación:** instalación/arranque reproducibles en el destino elegido, estáticos/PDF
disponibles con DEBUG=False, restauración probada y actualización conserva información.
La publicación requiere tu aprobación separada; no la implica aprobar una fase.

## Versionado vigente

Por solicitud del usuario, desde el cierre aprobado de Fase 2 se usa `v2.x.x`,
sin sufijos de desarrollo. La versión actual visible es **v2.2.0** local, con exportación PDF y nombre de acceso editable.
Se mantiene SemVer: MENOR para funcionalidades compatibles y PARCHE para correcciones.
Ejemplos siguientes: `v2.3.0` para nuevas funciones y `v2.2.1` para una corrección.
Fuente de la regla: [SemVer](https://semver.org/lang/es/).

La fuente única es `config/version.py`; almacena el número sin prefijo para mantener
el formato SemVer. El contexto compartido agrega `v` al mostrarlo en la interfaz:

```python
"""Versión del software (SemVer 2.0.0: MAYOR.MENOR.PARCHE). Fuente única; ver CHANGELOG.md."""
__version__ = "2.2.0"
FECHA_VERSION = "12/10/2026"
```

Los identificadores anteriores `2.0.0-dev.1` y `2.0.0-dev.2` se conservan únicamente
como referencias históricas en el registro y CHANGELOG. El cambio de número no implica
que la distribución final esté terminada: Waitress/PyInstaller permanecen en Fase 4.
Cada fase no implica necesariamente un incremento; se decide según los cambios entregados.

## Verificación y riesgos

Comandos desde la raíz, usando la base de trabajo aislada cuando se configure:

```powershell
.\.venv\Scripts\python.exe manage.py test --noinput
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Las nuevas pruebas cubrirán transacciones, permisos, duplicados, límites, edición de
movimientos, envío repetido y regresión de Admin. Pruebas de navegador para alta,
errores, ficha y filtros. `check --deploy` se evaluará con configuración de distribución,
distinguiendo requisitos de HTTPS para servidor de ejecución exclusiva en localhost.

Riesgos: Git no conserva SQLite/media; usar backup y copia aislada. Transacciones de
base no revierten archivos; diseñar limpieza de cargas fallidas. Concurrencia SQLite
limitada; probar escrituras simultáneas antes de prometer uso multiusuario. No resetear
base, no reescribir migraciones aplicadas ni recalcular saldos históricos sin análisis.
Componentes previos sin stock necesitan diagnóstico antes de una migración de datos.
Historial anterior no permite deducir todo saldo inicial: no fabricar movimientos.

Fuera del alcance inicial: múltiples almacenes, lector de códigos, compras/contabilidad,
importación masiva y sincronización cloud. Se pueden planear después de validar este flujo.

## Evidencia de Fase 1 — 12/10/2026

Ampliación del cierre: Administración comparte diseño/navegación, etiquetas españolas
y altas de usuarios normales; acceso propio aclarado y validación de PDF faltante
corregida. **61 pruebas pasan**. Caso intermitente informado sin causa confirmada.
Ubicaciones compartidas se priorizan en Fase 2 con migración preservando asignaciones.
Las cifras y comprobaciones de abajo corresponden al primer cierre, antes de ampliar.

- Rama `dev_v2`; documentación de servidores publicada en commit `a1a1ba0`.
- Datos de trabajo aislados en `.local/dev_v2` mediante snapshot SQLite y copia de media.
  Configuración predeterminada v2 apunta a esta copia, no a los datos originales.
- Alta en `/components/new/`, inicio de sesión propio y navegación común con versión.
  Categoría, referencia, nombre y stock en un único guardado; cantidades cero admitidas.
- Movimiento inicial positivo registrado en historial; guardado transaccional de alta.
- Movimientos atómicos y con actualización condicional; historial inmutable; saldo
  existente protegido en Admin. FK PROTECT preserva componentes con historial.
- Migración `inventory.0002_alter_stockmovement_stock` aplicada sólo a copias de trabajo.
- Regresión completa: 50 pruebas correctas, check sin incidencias, sin migraciones pendientes
  por generar. Prueba concurrente comprueba que dos salidas no consumen el mismo saldo;
  no supone ausencia de bloqueos de SQLite ni habilita uso multiusuario.
- Navegador con datos ficticios: login, error de máximo, guardar/agregar otro y catálogo
  con saldo correcto. Formulario a 320 píxeles sin desbordamiento horizontal y foco de teclado.
- No se agregaron dependencias ni se sustituyó runserver. Waitress/PyInstaller quedan para Fase 3.
- Pendiente: tu revisión funcional de Fase 1; push de estos cambios requiere autorización.
  Fase 2 mantiene ubicación/especificaciones/PDF en flujo propio como tareas futuras.

---

## Evidencia de Fase 2 — 12/10/2026

- Aprobación de inicio recibida del usuario, incluyendo Mi perfil.
- Respaldo previo de la copia en .local/checkpoints/fase1_before_fase2.
- Migración de ubicaciones conserva identificadores/asignaciones. Comprobación en
  copia real: 2 asignaciones y 10 saldos previos conservados; integridad SQLite ok.
- Ficha editable, especificaciones hasta 50 filas y categoría/ubicación contextual.
- Pantallas propias de ubicaciones y perfil; perfiles Lector/Operador sin acceso staff.
- Catálogo/resumen requieren sesión y permisos; PDF protegidos también por media.
- 83 pruebas correctas, check sin incidencias y migraciones coherentes. Navegador:
  guardar perfil con sesión conservada, filas JS, ubicación contextual, ficha con
  saldo10 y ubicación compartida entre dos componentes; perfil a375px sin desbordar.
- SQLite operativo original intacto. Fase 2 local en dev_v2, pendiente de revisión
  y autorización para publicar. No se inició Fase 3.

# Historial de la versión anterior (conservado)
Acá se encontrará documentado el desarrollo por fases conforme se vaya avanzando con el proyecto, la idea es ir acutalizando la documentación cada vez que se haga un cambio en una fase en específico y/o se agreguen cambios.

## Evidencia de Fase 3 — 12/10/2026

- Usuario autorizó implementación y publicación tras aclarar el alta y equilibrar la cabecera.
- Sesión común en vistas propias y Admin, cambio de contraseña para usuarios normales;
  encabezados de Componentes centrados en catálogo y Administración.
- Movimientos con motivo, vista previa y token firmado ligado a usuario/componente,
  identificador único persistente, rechazo de saldo obsoleto y transacción SQLite IMMEDIATE.
- Migración inventory.0005 aditiva en copia, respaldo previo fase2_before_fase3;
  conserva movimientos existentes con request_id nulo. Historial completo paginado.
- Duplicación técnica con referencia nueva y stock cero; sin ubicación, movimientos,
  PDF u ofertas. Proveedores/ofertas y creación contextual conservando campos.
- Catálogo filtrado/paginado y resumen enlazado. Evidencia de pruebas y navegador
  en dev_Process.md; Control F3 concluido. Fase 4 requiere aprobación separada.

## Estado actual
F1 completada: entorno virtual Python 3.12, dependencias mínimas y configuración segura preparados y verificados.
F2 completada: base del proyecto Django configurada, apps modulares creadas y validadas con configuración inicial.
F3 completada: modelos del dominio de inventario definidos, migraciones generadas y comprobadas.
F4 completada: administración con Django Admin configurada para los modelos principales del MVP.
F5 completada: validación y almacenamiento seguro de datasheets PDF verificados con pruebas reales.
F6 completada: reglas de movimientos de stock, cantidades mínimas/máximas y trazabilidad comprobadas con pruebas reales.
F7 completada: buscador funcional de componentes por referencia, nombre y stock validado con pruebas de Django.
F8 completada: panel de indicadores con bajo stock, datasheets faltantes y precios sin oferta validado con pruebas reales.
F9 completada: backup y restauración de SQLite y `media/` implementados y validados con una prueba funcional de recuperación local.
F10 completada: suite de pruebas ampliada a 17 casos, regresión completa y revisión básica de seguridad ejecutadas.
F11 completada: guía de instalación, arranque, alta de componentes, pruebas y operación local validada.
F11 actualización: base local reiniciada para la prueba de validación; visualización de datasheets y enlace “VER EL SITIO” corregidos.

### Registro de cambios

- **F1 — Preparación del entorno — Completada (2026-09-13)**
   - Se creó `requirements.txt` con Django 5.2.6 y `python-decouple` 3.8.
   - Se preparó el entorno virtual local `.venv` con Python 3.12; no se versiona.
   - Se confirmó `.env.example` sin secretos reales y `.gitignore` para excluir `.env`, bases de datos, archivos cargados, respaldos y entornos virtuales.
   - Se verificó la instalación de dependencias y la comprobación de Django.
   - El proyecto Django se reserva para F2.

- **F2 — Base del proyecto Django — Completada (2026-09-13)**
   - Se creó el proyecto Django base con `django-admin startproject config .`.
   - Se añadieron las apps modulares: `core`, `components`, `suppliers`, `inventory`, `documents` y `dashboard`.
   - Se configuraron `INSTALLED_APPS`, rutas de templates, media y archivos estáticos y la gestión segura de entorno con `python-decouple`.
   - Se definió la decisión de ubicación inicial en modo **1-1**: cada componente tendrá una sola ubicación física en el MVP, manteniendo la estructura simple y controlable.
   - Se verificó la base del proyecto con `python manage.py check`.

- **F3 — Modelo de datos y migraciones — Completada (2026-09-13)**
   - Se implementaron los modelos de `Category`, `Component`, `Specification`, `Supplier`, `SupplierOffer`, `Location`, `Stock`, `StockMovement` y `Datasheet`.
   - La relación de ubicación se mantiene en modo **1-1** para el MVP, con una ubicación por componente.
   - Se generaron y aplicaron migraciones con validación real mediante `makemigrations` y `migrate`.

- **F4 — Administración con Django Admin — Completada (2026-09-13)**
   - Se registraron los modelos principales en el administrador con listados, filtros, búsquedas e inlines.
   - Se habilitaron `SpecificationInline` y `SupplierOfferInline` para facilitar la edición de relaciones.
   - Se validó el arranque del servidor y la administración del panel con un superusuario real.

- **F5 — Gestión de datasheets — Completada (2026-09-13)**
   - Se definió la validación del modelo `Datasheet`: extensión PDF y límite máximo de 20 MB.
   - Se reforzó la política de almacenamiento local en `media/datasheets` sin incluir archivos cargados en Git.
   - Se validó con pruebas reales de aceptación para PDF válido, PDF inválido y archivo > 20 MB.

- **F6 — Stock y trazabilidad — Completada (2026-09-13)**
   - Se definió la lógica de movimientos para entradas, salidas y ajustes de stock.
   - Se aplicaron reglas de cantidad máxima, cantidad mínima y validación de stock suficiente antes de registrar salidas.
   - Se validó con pruebas reales de entrada, salida y ajuste de inventario.

- **F7 — Buscador personalizado — Completada (2026-09-13)**
   - Se implementó la búsqueda por referencia, nombre, valor y categoría en una vista de componentes.
   - Se añadió ordenación por nombre o stock (ascendente/descendente) y se validó con pruebas del flujo real del buscador.
   - Se documentó y publicó la funcionalidad en el repositorio.

- **F8 — Dashboard — Completada (2026-09-13)**
   - Se definieron indicadores para stock bajo, componentes sin datasheet y componentes sin oferta de precio.
   - Se añadió la vista de dashboard con listado de movimientos recientes y se validó el cálculo de KPI con pruebas reales.
   - Se publicó la funcionalidad en la rama `dev`.

- **F9 — Backup, exportación y operación local — Completada (2026-09-13)**
   - Se implementó `backups/backup_local.py` para copiar `db.sqlite3` y el directorio `media/`.
   - Se implementó la restauración de la base de datos y los archivos locales desde una copia.
   - Se mantuvieron las copias generadas fuera de Git y se validó el ciclo backup/restauración con una prueba automatizada.

- **F10 — Pruebas y control de calidad — Completada (2026-09-13)**
   - Se amplió la cobertura con validaciones de componentes, especificaciones, proveedores, ofertas y exclusión de componentes inactivos del buscador.
   - Se detectó y corrigió la aceptación de cantidades mínimas iguales a cero en `SupplierOffer`; también se bloquean precios negativos.
   - Se ejecutó la suite completa: 17 pruebas, todas correctas, y `manage.py check` sin errores.
   - `manage.py check --deploy` dejó seis advertencias esperables para el modo local: HTTPS/HSTS, cookies seguras, `DEBUG=True` y clave local de desarrollo. Deben resolverse antes de un despliegue público.

- **F11 — Estabilización y documentación final — Completada (2026-09-13)**
   - Se actualizó `README.md` con instalación, configuración local, migraciones, creación del superusuario y arranque.
   - Se documentó el flujo de prueba para crear una categoría, registrar un componente, añadir especificaciones y consultar stock.
   - Se añadieron las rutas principales de uso: administración, buscador y dashboard.
   - Se validó con 17 pruebas, `manage.py check` sin errores y resolución real de las tres rutas documentadas.
   - Se reinició `db.sqlite3` y se reaplicaron las migraciones para comenzar la prueba de validación con un superusuario y datos nuevos.
   - Se documentó la activación/desactivación del entorno virtual, el cierre seguro del servidor y el reinicio controlado de la base local.
   - Se añadió la apertura de datasheets PDF en pestaña nueva desde el administrador y la raíz `/` ahora redirige al buscador para que funcione “VER EL SITIO”.

---

1. **F0 — Validación de decisiones técnicas**  
   Cerrar las decisiones pendientes antes de crear código.

---

2. **F1 — Preparación del entorno**  
   Python, `venv`, Django, dependencias mínimas, `.env.example`, `.gitignore`, estructura de documentación y verificación de ejecución local.

---

3. **F2 — Base del proyecto Django**  
   Crear proyecto, apps modulares, configuración de rutas, estáticos, media y parámetros de seguridad básicos.

---

4. **F3 — Modelo de datos y migraciones**  
   Implementar categorías, componentes, especificaciones, proveedores/ofertas, stock, movimientos, ubicaciones y datasheets. Crear migraciones y pruebas de integridad.

---

5. **F4 — Administración con Django Admin**  
   Configurar CRUD administrativo, filtros, búsquedas e inlines para gestionar datos sin desarrollar formularios personalizados innecesarios.

---

6. **F5 — Gestión de datasheets**  
   Carga y validación de PDF, límite de tamaño, almacenamiento en `media/`, consulta segura y verificación de archivos faltantes.

---

7. **F6 — Stock y trazabilidad**  
   Implementar entradas, salidas y ajustes; impedir cantidades inválidas y mantener historial de movimientos.

---

8. **F7 — Buscador personalizado**  
   Vista de consulta rápida con filtros, paginación y ordenamiento.

---

9. **F8 — Dashboard**  
   Indicadores: bajo stock, componentes sin datasheet, sin precios y registros recientes.

---

10. **F9 — Backup, exportación y operación local**  
    Scripts para respaldar SQLite y `media/`; documentación de restauración y arranque.

---

11. **F10 — Pruebas y control de calidad**  
    Pruebas unitarias, integración, validación manual y revisión de seguridad básica.

---

12. **F11 — Estabilización y documentación final**  
    Corrección de incidencias, guía de instalación/uso y versión candidata.

---

13. **F12 — Empaquetado Windows**  
    Generar y probar el ejecutable `.exe` cuando el flujo local sea estable.

---


## Mejoras adicionales previas a Fase 4 — 12/10/2026

Perfil con nombre de usuario editable, contraseña sin detalles técnicos en Administración
y tabla PDF del catálogo con filtros/todas las páginas implementados localmente en v2.2.0.
115 pruebas correctas y revisión visual de usuarios/PDF. El usuario revisará y aprobará
estos cambios antes de publicar y autorizar Fase 4; no se modifica el máximo de cuatro fases.
