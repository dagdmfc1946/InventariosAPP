# Dependencias y licenciamiento

## Politica obligatoria

Solo se permiten componentes open source o gratuitos. Antes de agregar una dependencia se debe documentar su proposito, version fijada, licencia y justificacion tecnica. Las dependencias se instalaran y fijaran en `requirements.txt` durante F1; ese archivo aun no existe para no declarar paquetes no utilizados.

## Propuesta inicial para el MVP

| Componente | Uso | Licencia | Estado |
|---|---|---|---|
| Python 3.12 o 3.11 | Runtime | PSF License | Requerido en F1 |
| Django | Framework y ORM | BSD-3-Clause | Requerido en F1 |
| python-decouple | Variables de entorno | MIT | Requerido en F1 |
| Bootstrap 5 local | Interfaz responsive | MIT | Evaluar en F2 |
| jQuery local | Interacciones AJAX puntuales | MIT | Evaluar en F7 |
| Pillow | Imagenes de componentes | HPND | Diferido; no es parte del MVP actual |

SQLite se distribuye con Python y se empleara como motor local gratuito. No requiere paquete Python adicional.

## Criterios de incorporacion

1. Debe resolver una necesidad concreta del alcance aprobado.
2. Debe ser compatible con uso comercial y sin costo de ejecucion.
3. Debe mantenerse activamente o tener una alternativa estable.
4. Debe evitarse si Django o Python ya resuelven la necesidad.
