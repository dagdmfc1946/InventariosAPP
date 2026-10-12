# CHANGELOG

Se registran cambios reales; las funcionalidades previstas se describen en info_FASES.md.
Convención propuesta: [SemVer 2.0.0](https://semver.org/lang/es/).
Fuente única ejecutable: `config/version.py`.
No se atribuye una versión retrospectiva a la aplicación actual.

## [Sin publicar]

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

## [2.0.0-dev.1] — 12/10/2026 — Desarrollo local, pendiente de revisión

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

## Referencia anterior sin etiqueta SemVer comprobada

Commit analizado: `842afd1`, rama `dev`. Incluye Admin, búsqueda, dashboard, modelos
de stock/movimientos, datasheets y respaldo local. El historial detallado existente se
conserva en info_FASES.md y Git. No se afirma que sea versión 2.1.7.

## Política de registro

Cada entrega incluirá número, fecha real y cambios añadidos/corregidos/modificados,
compatibilidad de datos, instrucciones de actualización y validaciones relevantes.
El plan propone `2.0.0-dev.1` durante desarrollo y `2.0.0` al validar la entrega;
`2.0.0-dev.1` identifica el trabajo local y `2.0.0` todavía no es una release emitida.
