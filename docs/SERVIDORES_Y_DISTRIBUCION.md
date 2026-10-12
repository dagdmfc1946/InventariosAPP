# Django: servidores, distribución y protección del código

Fecha: 12/10/2026. Decisión para InventariosAPP: desarrollo con runserver,
versión final aprobada con Waitress y distribución Windows con PyInstaller.
La sección Raspberry Pi es una recomendación para otro proyecto; no cambia ese equipo.

## Qué hace Django y qué hace el servidor

Django ejecuta la lógica del aplicativo: rutas, formularios, validaciones, permisos,
consultas y respuestas. El servidor recibe solicitudes HTTP del navegador, llama
al aplicativo y devuelve sus respuestas. Django y el servidor colaboran a través
de WSGI en los ejemplos de este documento.

Cuando ejecutas `python manage.py runserver`, cargas el aplicativo y arrancas el
servidor de desarrollo incluido. Por eso parecen una sola cosa. Waitress y Gunicorn
sustituyen ese servidor; tu código Django sigue ejecutándose.
Fuente: [despliegue WSGI de Django](https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/).

Ejemplo al guardar un componente:

1. El navegador envía el formulario al servidor.
2. El servidor entrega la solicitud a Django.
3. Django comprueba los datos, guarda en SQLite y prepara una respuesta.
4. El servidor devuelve la respuesta al navegador.

```text
Navegador → servidor HTTP/WSGI → aplicativo Django → base de datos
                         ← respuesta preparada por Django ←
```

## Tabla comparativa

| Aspecto | runserver de Django | Waitress | Gunicorn |
|---|---|---|---|
| Propósito | Desarrollo y pruebas | Operación del aplicativo terminado | Operación del aplicativo terminado |
| Plataforma | Windows, Linux y macOS | Windows y Unix | Unix, como Linux |
| Viene con Django | Sí | No | No |
| Ejecuta tu código Django | Sí | Sí | Sí |
| Atiende solicitudes HTTP | Sí | Sí | Sí |
| Concurrencia habitual | Hilos; orientado a desarrollo | Hilos configurables | Procesos workers; otros modos según configuración |
| Recarga al editar código | Automática por defecto | Reiniciar el proceso | Reiniciar/recargar workers; recarga opcional en desarrollo |
| Requiere servidor externo | No | No | No; puede ser local en Linux |
| Genera ejecutables | No | No | No |
| Aplicación aquí | Desarrollo de ambos proyectos | InventariosAPP final en Windows | Proyecto final en Raspberry Pi/Linux |

Fuentes: [runserver](https://docs.djangoproject.com/en/5.2/ref/django-admin/#runserver),
[Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/) y
[Gunicorn](https://github.com/benoitc/gunicorn).

Un servidor local es un programa que escucha en tu propio equipo; no exige cloud,
Internet ni otro computador. Escuchar en `127.0.0.1` limita el acceso a ese equipo;
abrir acceso en red requiere una decisión y configuración adicionales.
Cambiar servidor tampoco cambia automáticamente DEBUG ni convierte el aplicativo
en seguro: permisos, configuración, estáticos y archivos subidos necesitan atención.

## InventariosAPP en Windows: flujo acordado

1. **Desarrollo:** continuar con `python manage.py runserver 127.0.0.1:8000`.
2. **Versión final aprobada:** usar Waitress con Django en localhost. Diseñar servicio
   de estáticos y PDF y verificar DEBUG=False; Waitress no lo resuelve por sí solo.
3. **Distribución:** empaquetar el lanzador, Django, Waitress, dependencias, plantillas
   y recursos mediante PyInstaller. El usuario abrirá `InventariosAPP.exe`; el lanzador
   arrancará el servidor local y abrirá el navegador.

SQLite, PDF y configuración deben vivir en una carpeta persistente del usuario, fuera
del ejecutable y de las carpetas temporales. Una actualización no debe reemplazarlos.
Habrá control de cierre y prevención de instancias conflictivas. No se generó todavía
un ejecutable ni se instaló Waitress: eso corresponde al cierre del desarrollo.

## Raspberry Pi/Linux: desarrollo y operación

Durante desarrollo se puede usar runserver. Para la entrega final propongo sustituir
su ejecución dentro del servicio actual por Gunicorn, manteniendo systemd como supervisor.
Son funciones diferentes: **systemd arranca/reinicia el proceso; Gunicorn atiende HTTP;
Django ejecuta la lógica**. Usar runserver como servicio no cambia su naturaleza de desarrollo.

Ejemplo orientativo desde el entorno virtual, ajustando el módulo WSGI al proyecto real:

```bash
gunicorn mi_proyecto.wsgi:application --bind 127.0.0.1:8000 --workers 1
```

Se plantea un worker como punto inicial en un equipo pequeño; medir carga, RAM y
operaciones reales antes de aumentar workers. Si hay tareas de hardware o procesos
periódicos, separarlos del arranque de Django para no ejecutarlos una vez por worker.
No se conoce todavía la arquitectura de tu otro aplicativo; requiere comprobarlo.

Para acceso desde otros equipos, incorporar un proxy como Nginx, atender estáticos
y aplicar HTTPS según el contexto. Si sólo se usa un navegador en la Raspberry,
mantener localhost y resolver igualmente los estáticos/PDF. Ejecutar con usuario
de servicio sin privilegios, rutas de datos separadas, logs y recuperación probada.
No hace falta añadir un proxy por hábito al escenario exclusivamente local.
Referencias: [despliegue Gunicorn](https://gunicorn.org/deploy/) y
[checklist Django](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/).

## PyInstaller en Linux y límites de protección

PyInstaller también crea distribuciones Linux: el resultado es un ejecutable Linux,
no un `.exe` de Windows. Construir y probar para el sistema y arquitectura destino
(ARM de la Raspberry, 32/64 bits y bibliotecas compatibles); no reutilizar un binario Windows.
Empezar con distribución en carpeta antes del modo de un solo archivo facilita diagnóstico.

Empaquetar evita entregar los `.py` del programa de forma directa, pero incluye
bytecode recuperable; **PyInstaller no garantiza confidencialidad del código**.
Las plantillas y recursos también pueden quedar accesibles. `onefile` no cambia esa garantía.
Fuente: [PyInstaller: funcionamiento y código fuente](https://pyinstaller.org/en/stable/operating-mode.html).

Si se empaqueta Django con Gunicorn, preparar un lanzador Python que cargue WSGI e
inicie Gunicorn. No basta ejecutar el comando CLI sobre un árbol de fuentes que ya no
se entrega. Verificar imports dinámicos, apps, migraciones, plantillas, señales,
parada de workers y actualización. systemd podría supervisar ese ejecutable final.
La integración requiere una prueba de concepto en la Raspberry objetivo; no se da
por compatible con el proyecto desconocido.

## Recomendación para proteger el otro proyecto

- Primero estabilizar la operación con Gunicorn/systemd y datos independientes del código.
- Si sólo buscas instalación fácil y evitar entregar fuentes visibles, evaluar PyInstaller.
- Si la lógica es propiedad intelectual sensible, compilar los módulos críticos con
  Cython y empaquetar después; PyInstaller documenta esa posibilidad. Evaluar Nuitka
  como alternativa de compilación tras probar compatibilidad con Django en ARM.
  [Cython en la guía PyInstaller](https://pyinstaller.org/en/stable/operating-mode.html#hiding-the-source-code),
  [manual de Nuitka](https://nuitka.net/user-documentation/user-manual.html).
- La compilación eleva el esfuerzo de análisis, pero no impide ingeniería inversa
  a quien controla el dispositivo. No guardar secretos de terceros o claves maestras
  dentro del binario. Los permisos Linux restringen usuarios normales; no al dueño con root.
- Si necesitas que una lógica nunca llegue al cliente, mantenerla en un servicio bajo
  tu control ofrece un límite distinto, pero requiere conectividad y cambia el producto.
  No es la solución elegida para InventariosAPP, que debe operar localmente.

Para decidir el otro proyecto faltan modelo de Raspberry, SO/arquitectura, dependencias,
uso de hardware, acceso local/red y nivel de protección requerido. Esa evaluación se
haría en su propio repositorio; aquí sólo se documentan opciones y sus límites.
