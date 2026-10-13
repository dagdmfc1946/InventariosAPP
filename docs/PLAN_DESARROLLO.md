# Plan de desarrollo por fases

Cada fase termina con pruebas proporcionales, actualizacion documental y commit en `dev`. La integracion a `main` se realiza solo tras validacion funcional.

| Fase | Objetivo | Entregable principal |
|---|---|---|
| F0 | Confirmar decisiones tecnicas | Decisiones aprobadas y plan vigente |
| F1 | Preparar entorno | venv, Django, `.env.example`, dependencias y arranque local |
| F2 | Crear base Django | Proyecto, apps, configuracion, rutas y recursos base |
| F3 | Implementar datos | Modelos, migraciones y pruebas de integridad |
| F4 | Configurar administracion | Django Admin con CRUD, filtros e inlines |
| F5 | Gestionar datasheets | Carga, validacion y visualizacion segura de PDFs |
| F6 | Implementar inventario | Stock, movimientos y reglas de consistencia |
| F7 | Crear buscador | Filtros, paginacion y ordenamiento |
| F8 | Crear dashboard | Indicadores operativos |
| F9 | Operacion y respaldo | Backup, restauracion y exportacion documentados |
| F10 | Verificar calidad | Pruebas, checklist manual y seguridad basica |
| F11 | Estabilizar entrega | Correcciones y guias de uso/instalacion |
| F12 | Empaquetar Windows | Ejecutable probado para Windows |

## Decisiones que requieren aprobacion antes de F1

1. Confirmar SQLite como base de datos del MVP.
2. Confirmar especificaciones EAV simples.
3. Definir si un componente puede repartir su stock entre multiples ubicaciones.
4. Confirmar movimientos de stock desde el MVP.
5. Confirmar Bootstrap y jQuery locales para operacion sin internet.
6. Mantener fotos de componentes y Pillow fuera del MVP inicial.
