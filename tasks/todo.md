# Tareas v2 — Fase 1 implementada; revisión pendiente

Plan: ../info_FASES.md. Evidencia de ejecución: ../dev_Process.md.
Cada unidad se mantiene pequeña; si supera cinco archivos de implementación se divide
antes de ejecutarse. Documentación de avance acompaña cada unidad.
Evidencia T1–T6 en dev_Process.md. El control de F1 espera revisión del usuario.

## Fase 1

- [x] T1. Aislar desarrollo. Autorización recibida el 12/10/2026.
  Aceptación: dev_v2 parte del estado vigente; SQLite/media operativos preservados;
  copia independiente configurada para desarrollo. Verificar rama, commit de origen,
  restauración en copia y rutas efectivas. Archivos previstos: configuración de rutas
  de datos, prueba de rutas, plantilla de entorno (hasta 3).
- [x] T2. Fuente de versión. Depende de T1.
  Aceptación: constantes importables con SemVer/fecha real y zona America/Bogota.
  Verificar importación, visualización posterior y check. Archivos: config/version.py,
  settings.py, context processor y prueba (hasta 4).
- [x] T3. Evitar doble aplicación de movimientos. Depende de T1.
  Aceptación: movimiento/saldo atómicos; re-guardar no altera saldo; límites y actualizaciones
  condicionales evitan saldo negativo. Verificar pruebas de re-guardado, rollback,
  límites y concurrencia compatible con SQLite. Archivos: inventory/models.py,
  servicio de stock si procede, inventory/tests.py (hasta 3).
- [x] T4. Proteger historial en Admin. Depende de T3.
  Aceptación: no modificar/borrar movimientos aplicados ni editar cantidad directamente;
  correcciones por movimiento compensatorio. Verificar permisos y regresión Admin.
  Archivos: inventory/admin.py, inventory/tests.py (2).
- [x] T5. Crear componente con stock. Depende de T3.
  Aceptación: servicio valida duplicados/cantidades, crea saldo y entrada inicial coherente;
  error no deja registros parciales. Verificar tests de alta cero/positiva e inválida.
  Archivos: components/forms.py, servicio y tests (hasta 3).
- [x] T6. Exponer alta autenticada. Depende de T2, T4 y T5.
  Aceptación: pantalla con errores por campo, navegación y Guardar/agregar otro;
  permisos Django comprobados. Verificar POST/CSRF/permisos y navegador.
  Archivos: components/views.py, urls raíz, plantilla base, plantilla alta y tests (5).
  Se ejecutó en unidades: servicio/formulario; vista y rutas; plantillas compartidas/CSS;
  integración visual de búsqueda/resumen. Sin dependencia JavaScript ni frameworks adicionales.
- [ ] Control F1: suite y check pasan; alta visible en búsqueda/Admin; revisión del usuario.

## Fase 2

- [ ] T7. Ficha y edición de ubicación. Depende de cierre F1.
  Aceptación: ficha muestra saldo/datos y edita ubicación opcional sin cambiar cantidades.
  Verificar lectura, permisos y edición. Archivos: forms, views, urls, template, tests (5).
- [ ] T8. Especificaciones dinámicas. Depende de T7.
  Aceptación: filas opcionales, sin atributos duplicados ni pérdida al fallar validación.
  Verificar formsets en servidor y navegador. Archivos: forms, views, template, JS, tests (5).
- [ ] T9. Categoría contextual. Depende de T7.
  Aceptación: crear categoría conserva datos del alta y rechaza duplicados.
  Verificar con/sin JS. Archivos: forms, views, urls, template/JS, tests (5).
- [ ] T10. Duplicación técnica. Depende de T8.
  Aceptación: copia datos técnicos, exige nueva referencia y no copia saldo/historial/PDF.
  Verificar integración. Archivos: servicio, views, urls, template, tests (5).
- [ ] T11. PDF en ficha. Depende de T7.
  Aceptación: validar contenido/tamaño, controlar acceso y limpiar cargas fallidas.
  Verificar archivos válidos, inválidos y error de guardado. Archivos: documents/models.py,
  forms, views, template y tests (5).
- [ ] T12. Ofertas opcionales. Depende de T7.
  Aceptación: gestionar oferta y proveedor respetando validación existente.
  Verificar precio, moneda y duplicados. Archivos: forms, views, urls, template, tests (5).
- [ ] T13. Operar movimientos en ficha. Depende de T3 y T7.
  Aceptación: entrada/salida/ajuste con motivo y saldo esperado; permisos y doble envío
  controlados. Verificar integración y navegador. Archivos: forms, views, urls, template, tests (5).
- [ ] T14. Catálogo filtrado. Depende de T7.
  Aceptación: filtros independientes y páginas de 25 preservan parámetros.
  Verificar navegación y consulta. Archivos: core/views.py, template, tests (3).
- [ ] T15. Dashboard y acabado de interfaz. Depende de T13 y T14.
  Aceptación: indicadores enlazan filtros, teclado/móvil utilizables y permisos coherentes.
  Verificar navegador y regresión. Archivos: dashboard/views.py, templates, CSS y tests (5).
- [ ] Control F2: ejecutar flujo completo y comparar pasos; revisión del usuario.

## Fase 3

- [ ] T16. Respaldo consistente. Depende de cierre F2.
  Aceptación: copia íntegra verificada con base de trabajo y media; respaldo no interrumpe
  datos operativos. Verificar lectura de copia y archivos. Archivos: backup_local.py, tests (2).
- [ ] T17. Recuperación aislada. Depende de T16.
  Aceptación: validar copia y restaurar sin mezclar media antiguo; conservar vía de rollback.
  Verificar restauración en temporales propios. Archivos: backup_local.py, tests (2).
- [ ] T18. Configuración de distribución. Depende de destino elegido y T17.
  Aceptación: DEBUG=False, secretos externos, estáticos/PDF servidos y datos persistentes.
  Verificar configuración y check --deploy interpretado según escenario.
  Archivos: settings, entorno ejemplo, launcher, requisitos específicos y tests (5).
- [ ] T19. Preparar artefacto del destino elegido. Depende de T18.
  Aceptación: Windows con Waitress/PyInstaller probado sin Python, operación local
  sin Internet y escucha exclusiva en localhost; nunca publicar automáticamente.
  Verificar arranque, parada y actualización con datos de prueba. Archivos: launcher,
  spec de empaquetado o servicio, script de build y pruebas (hasta 4).
- [ ] T20. Cerrar documentación y revisión. Depende de T19.
  Aceptación: manual refleja lo implementado, CHANGELOG/version coinciden y limitaciones
  constan; dependencias revisadas. Verificar regresión y checklist de distribución.
  Archivos: MANUAL_USUARIO.md, CHANGELOG.md, README.md, dev_Process.md, info_FASES.md (5).
- [ ] Control F3: candidato revisable, aprobación explícita antes de push/merge/publicación.
