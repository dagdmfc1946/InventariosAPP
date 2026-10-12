# Registro de desarrollo — InventariosAPP v2

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
| 1 | Pendiente de aprobación | — |
| 2 | Propuesta | — |
| 3 | Propuesta; destino Windows local confirmado | — |
