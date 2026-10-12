# CHANGELOG

Se registran cambios reales; las funcionalidades previstas se describen en info_FASES.md.
Convención propuesta: [SemVer 2.0.0](https://semver.org/lang/es/).
La futura fuente única ejecutable será `config/version.py`, después de aprobar Fase 1.
No se atribuye una versión retrospectiva a la aplicación actual.

## [Sin publicar]

### Documentación — 12/10/2026

- Análisis del aplicativo actual y propuesta de tres fases para la línea v2.
- Registro de proceso, manual inicial y tareas verificables.
- Conservación del historial anterior en info_FASES.md.
- Explicación de distribución Windows y despliegue con Gunicorn.
- Confirmación de destino Windows local con PyInstaller al finalizar; despliegue
  en servidor fuera del alcance. Creación de dev_v2 autorizada para subir documentación.

### Validación de la base actual

- 18 pruebas correctas y comprobación Django sin incidencias.
- Ningún cambio funcional, de dependencias, de esquema ni de datos operativos.

## Referencia anterior sin etiqueta SemVer comprobada

Commit analizado: `842afd1`, rama `dev`. Incluye Admin, búsqueda, dashboard, modelos
de stock/movimientos, datasheets y respaldo local. El historial detallado existente se
conserva en info_FASES.md y Git. No se afirma que sea versión 2.1.7.

## Política de registro

Cada entrega incluirá número, fecha real y cambios añadidos/corregidos/modificados,
compatibilidad de datos, instrucciones de actualización y validaciones relevantes.
El plan propone `2.0.0-dev.1` durante desarrollo y `2.0.0` al validar la entrega;
estos identificadores todavía no representan releases emitidas.
