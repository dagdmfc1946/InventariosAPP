# Cierre del desarrollo y pruebas de uso

12/10/2026. El usuario considera estable InventariosAPP v2.3.1 y aprueba su
integración en main. Las cuatro fases de desarrollo quedan cerradas para el alcance
local acordado. Empieza la etapa de ejecución y pruebas de uso con el .exe; sus
hallazgos pueden motivar correcciones o nuevas funcionalidades en dev_v2.

## Estado entregado

- main: versión estable, documentación, scripts Windows y ZIP de distribución.
- dev_v2: mismo contenido funcional, destinada a futuros desarrollos.
- arquitectura/: diagrama interactivo Archify, modelo, flujos y validación.
- Código v2.3.1, fuente única config/version.py. El cierre documental no cambia
  versión ni reconstruye el ejecutable probado.
- 125 pruebas automatizadas previas correctas y validación de uso/recuperación
  del paquete en el PC objetivo. No se afirma validación en otro Windows limpio.

## Dónde están los datos

Base predeterminada: `%LOCALAPPDATA%\InventariosAPP\data\db.sqlite3`.
Para Diego: `C:\Users\Diego\AppData\Local\InventariosAPP\data\db.sqlite3`.
PDF: carpeta hermana `media\datasheets`. Secreto persistente: `.runtime-key`.
La consola informa la ruta efectiva; --data-dir puede escoger otra carpeta.

Reemplazar la carpeta del programa no reinicia la base. Mantén la carpeta de datos
completa y obtén respaldos con la aplicación detenida según
[DISTRIBUCION_Y_DESARROLLO.md](DISTRIBUCION_Y_DESARROLLO.md#respaldar-y-restaurar).
No subas bases, claves, respaldos ni documentos personales al repositorio.

## Guía para probar y reportar hallazgos

Revisa inicio/cierre, sesión, perfil, categorías, alta/edición/duplicación de
componentes, ubicaciones compartidas, entradas/salidas/ajustes, límites de stock,
proveedores/ofertas, PDF adjuntos y exportación filtrada. Prueba un respaldo y su
restauración en una carpeta separada para comprobar recuperación sin reemplazar
los datos que usas. Conserva un respaldo antes de una actualización futura.

Para cada hallazgo registra:

| Dato | Qué anotar |
|---|---|
| Versión y pantalla | Versión de consola y sección utilizada. |
| Pasos | Acciones exactas que llevan al comportamiento. |
| Esperado y observado | Qué debería ocurrir y qué ocurrió. |
| Evidencia | Captura/error de consola; evitar contraseñas y datos sensibles. |
| Repetición | Si ocurre siempre y si persistió al reiniciar. |
| Impacto | Consulta, bloqueo de operación o posible inconsistencia de datos. |

No se agregan pruebas de usuario como registros de la base distribuida ni se
promete un resultado de esa etapa antes de que el usuario la ejecute.
