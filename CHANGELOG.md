# CHANGELOG

Se registran cambios reales; las funcionalidades previstas se describen en info_FASES.md.
Convención vigente: [SemVer 2.0.0](https://semver.org/lang/es/).
Fuente única ejecutable: `config/version.py`.
No se atribuye una versión retrospectiva a la aplicación actual.

## [v2.0.0] — 12/10/2026 — Cierre aprobado de Fase 2

- El usuario autorizó publicar todo el desarrollo de Fase 2 en `dev_v2`.
- Versión simplificada a `v2.x.x`: fuente SemVer `2.0.0`, interfaz `v2.0.0`.
  Se eliminan los sufijos de desarrollo de la versión actual; las entradas anteriores
  conservan los identificadores usados durante su implementación.
- Incluye los cambios de Fases 1 y 2 documentados abajo. Fase 3 pendiente de aprobación;
  la distribución final con Waitress/PyInstaller sigue prevista en Fase 4.

## [Sin publicar] — Referencia histórica de la planificación inicial

### Documentación — 12/10/2026

- Análisis del aplicativo actual y propuesta de tres fases para la línea v2.
- Registro de proceso, manual inicial y tareas verificables.
- Conservación del historial anterior en info_FASES.md.
- Explicación de distribución Windows y despliegue con Gunicorn.
- Confirmación de destino Windows local con PyInstaller al finalizar; despliegue
  en servidor fuera del alcance. Creación de dev_v2 autorizada para subir documentación.

### Validación de la base anterior, antes de implementar Fase 1

- 18 pruebas correctas y comprobación Django sin incidencias.
- Ningún cambio funcional, de dependencias, de esquema ni de datos operativos.

## [2.0.0-dev.2] — 12/10/2026 — Fase 2 local, pendiente de revisión

### Añadido

- Mi perfil en /accounts/profile/: edita nombre, apellidos y correo de la cuenta
  autenticada, conserva sesión y excluye usuario/contraseña/permisos del formulario.
- Ficha de componente desde catálogo; edición conjunta de datos/especificaciones con
  validación de duplicados y saldo intacto. Filas dinámicas con alternativa sin JavaScript.
- Categorías y ubicaciones creadas/seleccionadas desde alta o edición, conservando campos.
- Ubicaciones compartidas y pantalla para asignar varios componentes a una ya guardada.
  Administración permite también asignación múltiple; ubicación ocupada protegida de borrado.
- Perfiles Lector/Operador y selector en altas de usuarios. Comando configure_inventory_roles
  prepara esos grupos sin asignar usuarios existentes ni conceder acceso administrativo.
- Adjuntar/abrir PDF desde ficha; validación adicional de cabecera y limpieza de carga
  si falla la inserción. No analiza el documento completo ni modifica archivos antiguos.

### Seguridad y compatibilidad

- Catálogo/resumen exigen sesión y permiso de consulta (se conserva acceso de operadores
  con permiso individual de alta de Fase 1). PDF exige permiso de documento, incluida
  la ruta directa media; archivos no registrados y faltantes devuelven 404.
- Logout redirige a login, pues catálogo requiere sesión. Pantalla 403 en español.
- Migraciones components.0003/inventory.0004 trasladan asignaciones al FK de componente.
  Se conservan IDs, ubicaciones vacías y saldos. No fusiona por texto. Si ya existen
  ubicaciones compartidas, revertir el esquema antiguo exige recuperar el respaldo.
- Datos operativos originales intactos; respaldo previo de la copia de desarrollo.
  Sin dependencias nuevas. Sigue runserver; distribución permanece en Fase 4.

### Verificación

- 83 pruebas correctas, check y coherencia de migraciones correctos. Incluye migración
  de datos, perfil propio/CSRF, roles, IDs de especificaciones ajenas, transacciones,
  PDF protegido, contenido falso y limpieza tras fallo de base.
- Navegador con datos ficticios: perfil guardado, ficha con especificaciones, ubicación
  contextual y asignación de dos componentes a ubicación existente; perfil móvil375px.
- Pendiente revisión y aprobación antes de push. Fase 3 no iniciada.

## [2.0.0-dev.1] — 12/10/2026 — Fase 1 concluida en dev_v2

### Añadido

- Alta rápida autenticada de componente y stock en `/components/new/`.
- Entrada inicial con trazabilidad para cantidades positivas; stock cero sin movimiento.
- Inicio/cierre de sesión, navegación común y versión visible; diseño adaptable.
- Datos de desarrollo aislados mediante INVENTARIOS_DATA_DIR y preparación de copia.
- Documento de servidores y distribución Windows/Raspberry publicado separadamente.

### Corregido

- Re-guardar un movimiento no lo aplica otra vez. Edición/borrado de historial bloqueados.
- Movimiento y saldo atómicos; actualización condicional evita pérdida de cantidades
  y sobregiro por instancias desactualizadas. Límites mínimo/máximo coherentes.
- Cantidad de stock existente protegida de edición directa y componentes con historial
  protegidos por relación PROTECT. Para correcciones, registrar movimientos compensatorios.

### Configuración y compatibilidad

- Zona horaria America/Bogota; fuente de versión config/version.py.
- Migración aditiva `inventory.0002_alter_stockmovement_stock`; no recalcula cantidades
  ni fabrica historial inicial para registros antiguos. Aplicada sólo en copias locales.
- Ruta predeterminada de datos en esta rama: `.local/dev_v2`; no usa el SQLite original.
  Ver README para copia inicial o instalación vacía. La fecha visible usa Bogotá;
  timestamps almacenados no se reescriben.
- No cambia dependencias. Sigue runserver durante desarrollo; Waitress/PyInstaller futuros.

### Validación

- 50 pruebas pasan; check sin incidencias y makemigrations --check --dry-run sin cambios.
- Navegador: login, validación de cantidad, guardar/agregar otro y saldo en catálogo;
  formulario móvil de 320 px y navegación con teclado.
- Pendiente aprobación funcional del usuario y autorización para subir desarrollo.
  No representa una release final ni se creó tag.

### Ampliación del cierre de Fase 1 — 12/10/2026

- Administración con paleta, tipografía, navegación y pie de versión coherentes con
  catálogo/resumen. Conserva formularios y widgets nativos Django.
- Etiquetas españolas de aplicaciones, modelos, campos y permisos. Catálogo/resumen
  usan «existencias» y «ficha técnica». Datos ingresados no se traducen.
- Alta administrativa de usuarios normales con contraseña obligatoria; opciones de
  promoción a staff/superusuario retiradas. Gestión de usuarios sólo para superusuario;
  crear superusuarios se mantiene mediante createsuperuser desde terminal.
- Acceso administrativo aclara el enlace de login para usuarios del aplicativo.
- Validación de PDF faltante/inaccesible muestra error de campo y permite reemplazo.
  Guardar/continuar y re-guardar sin nuevo archivo tienen pruebas de regresión.
  La causa del error intermitente informado sigue sin confirmarse.
- Migraciones de etiquetas en components/documents/inventory/suppliers, sin renombrar
  campos técnicos ni traducir datos. Aplicadas exclusivamente a las copias de desarrollo.
- Plan ampliado a cuatro fases: ubicaciones compartidas/permisos/ficha en Fase 2,
  operación diaria en Fase 3 y distribución Windows en Fase 4.
- Suite ampliada: 61 pruebas correctas, check sin incidencias y migraciones coherentes.
  Revisión visual de administrador/listados/formulario de usuario, cabecera a 375 px;
  consola sin advertencias/errores y hash del SQLite operativo sin cambios.

### Cierre autorizado — 12/10/2026

- Encabezado de sesión con avatar, nombre de usuario y acciones separadas en botones:
  Cambiar contraseña y Salir. Adaptación móvil y cierre mediante POST/CSRF conservados.
- El usuario aprobó concluir Fase 1 y subir todo su desarrollo/documentación a dev_v2.
  La Fase 2 no se inicia hasta nueva revisión y aprobación; dev/main no se integran.
- 61 pruebas correctas; check y coherencia de migraciones correctos. Encabezado
  revisado en escritorio y a 375px, sin desbordamiento ni errores de consola.

## Referencia anterior sin etiqueta SemVer comprobada

Commit analizado: `842afd1`, rama `dev`. Incluye Admin, búsqueda, dashboard, modelos
de stock/movimientos, datasheets y respaldo local. El historial detallado existente se
conserva en info_FASES.md y Git. No se afirma que sea versión 2.1.7.

## Política de registro

Cada entrega incluirá número, fecha real y cambios añadidos/corregidos/modificados,
compatibilidad de datos, instrucciones de actualización y validaciones relevantes.
La versión visible sigue `v2.x.x`, sin sufijos; el número SemVer se importa desde
config/version.py y el prefijo v se agrega en la presentación. Correcciones incrementan
PARCHE y nuevas funciones compatibles incrementan MENOR. Los sufijos antiguos se
conservan como historia. Publicar una fase no completa la distribución de Fase 4.
