# Dependencias y licenciamiento

## Dependencias de v2.3.0 (vigente)

| Paquete | Versión | Finalidad | Licencia |
|---|---|---|---|
| Django | 5.2.18 | Framework, ORM y actualización de seguridad de la serie 5.2 | BSD-3-Clause |
| python-decouple | 3.8 | Configuración desde entorno | MIT |
| ReportLab | 4.5.1 | Tabla PDF del catálogo | BSD |
| Waitress | 3.0.2 | Servidor WSGI Windows en loopback | ZPL-2.1 |
| WhiteNoise | 6.12.0 | Estáticos con DEBUG=False | MIT |
| PyInstaller (solo build) | 6.22.0 | Construir .exe con Python incluido | GPL-2.0-or-later con excepción del bootloader |

Runtime fijado en requirements.txt; construcción en requirements-build.txt. Dependencias
transitivas de estas bibliotecas se instalan en el entorno virtual; pip check validado.
Pillow ahora es dependencia de ReportLab, sin añadir funciones de imágenes al catálogo.
El paquete acompaña avisos de licencias de dependencias/Python; no incorpora Bootstrap
ni jQuery. Construcción y SHA256 quedan registrados en BUILD_INFO.json.

La firma Authenticode es un paso de distribución pendiente por el bloqueo de Windows.
No se contrató ningún certificado ni se modificó la política de dependencias gratuitas.

## Referencia histórica del MVP

## Politica obligatoria

Solo se permiten componentes open source o gratuitos. Antes de agregar una dependencia se debe documentar su proposito, version fijada, licencia y justificacion tecnica. Las dependencias se instalaran y fijaran en `requirements.txt` durante F1; ese archivo aun no existe para no declarar paquetes no utilizados.

## Propuesta inicial para el MVP

| Componente | Uso | Licencia | Estado |
|---|---|---|---|
| Python 3.12 | Runtime | PSF License | Instalado y verificado en F1 |
| Django 5.2.6 | Framework y ORM | BSD-3-Clause | Fijado e instalado en F1 |
| python-decouple 3.8 | Variables de entorno | MIT | Fijado e instalado en F1 |
| Bootstrap 5 local | Interfaz responsive | MIT | Evaluar en F2 |
| jQuery local | Interacciones AJAX puntuales | MIT | Evaluar en F7 |
| Pillow | Imagenes de componentes | HPND | Diferido; no es parte del MVP actual |

SQLite se distribuye con Python y se empleara como motor local gratuito. No requiere paquete Python adicional.

## Criterios de incorporacion

1. Debe resolver una necesidad concreta del alcance aprobado.
2. Debe ser compatible con uso comercial y sin costo de ejecucion.
3. Debe mantenerse activamente o tener una alternativa estable.
4. Debe evitarse si Django o Python ya resuelven la necesidad.
