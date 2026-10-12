# Manual de usuario — InventariosAPP

Actualizado: 12/10/2026. Versión `2.0.0-dev.1`, Fase 1 concluida en `dev_v2`.
La Fase 2 espera nueva revisión y aprobación. La versión anterior sigue en `dev`.

## Datos separados para revisar v2

Esta rama usa por defecto `.local/dev_v2/db.sqlite3` y `.local/dev_v2/media`.
La copia de desarrollo ya fue preparada en este equipo. Conserva las cuentas que
tenías en la base original: usa tus credenciales habituales. No usar la cuenta de
prueba visual: sólo existe en otra base ficticia independiente.

INVENTARIOS_DATA_DIR permite elegir otra carpeta. Cambiar de rama no separa datos
automáticamente; no apuntar la versión en desarrollo a los datos operativos.
Si ya hay copia, no ejecutar de nuevo prepare_dev: rechaza sobrescribirla.

## Iniciar y cerrar

Desde PowerShell en la raíz del proyecto, con el entorno y base ya preparados:

```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Abrir [administración](http://127.0.0.1:8000/admin/),
[buscador](http://127.0.0.1:8000/search/) o
[dashboard](http://127.0.0.1:8000/dashboard/).
El administrador requiere las credenciales de superusuario. Para instalar desde cero
seguir la sección v2 del README; no reiniciar ni borrar la base existente para actualizar.
Para detener: Ctrl+C en la consola y esperar a que termine. No cerrar durante guardados
o carga de archivos. `runserver` se documenta aquí para desarrollo/prueba local.

## Usuarios normales e inicio de sesión

El superusuario puede entrar a **Administración → Usuarios → Añadir**, escribir un
nombre de usuario y confirmar la contraseña. Esta pantalla crea cuentas normales
activas, sin acceso administrativo. No ofrece crear ni promover a superusuario.
Para crear un superusuario nuevo se mantiene el comando de terminal:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Después de guardar un usuario normal, se pueden asignar permisos desde su edición.
Para el alta rápida necesita **Puede agregar** componente, existencias y movimiento.
Los grupos permiten compartir permisos; los perfiles simplificados lector/operador se
implementarán en Fase 2. La gestión de cuentas está reservada al superusuario.

Los usuarios normales deben entrar por `/accounts/login/`, o **Iniciar sesión** en
el catálogo. `/admin/login/` está reservado a cuentas con acceso administrativo:
no poder entrar ahí no demuestra que la contraseña sea incorrecta. La pantalla
administrativa incluye un enlace al acceso del aplicativo.

Si falla el acceso normal, comprobar usuario exacto, contraseña y que la cuenta esté
activa. Las cuentas sin contraseña utilizable requieren que el responsable les
establezca una desde la edición de usuario. No se cambian contraseñas existentes al
actualizar y no se almacenan contraseñas en texto plano.

## Alta rápida de componente y stock

1. Abrir `/search/` y pulsar **Nuevo componente**, o visitar `/components/new/`.
2. Iniciar sesión si se solicita. El superusuario existente puede usar la nueva pantalla.
3. Elegir categoría existente y completar referencia y nombre; valor y número de parte
   son opcionales. Una referencia no se puede repetir dentro de la categoría.
4. Indicar cantidad inicial, mínimo y máximo. No se admiten negativos; el mínimo y
   la cantidad inicial no pueden superar el máximo si éste es distinto de cero.
5. Pulsar **Guardar componente** para volver al catálogo, o **Guardar y agregar otro**
   para continuar con un formulario limpio. El componente y su stock se guardan juntos.
6. Si falla la validación, revisar los mensajes; no se crean registros parciales.
   Si hay cantidad inicial positiva, aparece una entrada en el historial. Con cero,
   se crea stock sin movimiento de cantidad cero.

Si no hay categorías, la pantalla explica cómo crear una desde Administración.
Los usuarios no administradores necesitan permisos para agregar componente, stock y
movimiento. Un usuario autenticado sin esos permisos recibe 403. No se conceden permisos
automáticamente. El alta, login y logout usan CSRF; no requieren JavaScript.

## Completar información mediante Administración

La ficha ampliada llegará en Fase 2. Mientras tanto se puede usar el flujo administrativo:
Para un alta alternativa desde Admin, seguir los pasos de abajo. Si usaste el alta
rápida, el componente y su stock ya existen: sólo completa sus datos opcionales.

1. Entrar al administrador y crear o elegir una categoría.
2. Abrir Componentes y Agregar. Completar categoría, referencia y nombre;
   valor y número de parte son opcionales. La referencia es única dentro de la categoría.
3. Completar especificaciones (atributo, valor y unidad opcional) en las filas del componente.
4. Guardar el componente.
5. Abrir Existencias y crear su stock: componente, cantidad, mínimo y máximo.
   Máximo cero equivale a no configurar límite máximo en las reglas de movimientos.
6. Si corresponde, crear una ubicación vinculada: estante, caja, cajón o descripción.
7. Agregar ficha técnica vinculada: archivo .pdf de hasta 20 MB. Abrir PDF desde su listado.
8. Registrar proveedor y oferta si se quiere conservar precio, moneda, cantidad mínima
   de compra y fecha de consulta. El valor predeterminado de moneda actual es EUR.
9. Buscar el componente y comprobar su saldo en el buscador y alertas del dashboard.

Administración comparte colores, tipografía y navegación con el catálogo y resumen.
Los nombres de aplicaciones, modelos, campos y permisos se muestran en español;
los nombres/referencias/atributos que escribas en inglés se conservan.

**Guardar y continuar editando** en Fichas técnicas conserva el PDF: no hace falta
seleccionarlo otra vez al editar otros datos. Si el archivo guardado no se puede leer,
se muestra un error en el campo **Archivo PDF**, en lugar de una pantalla de error.
Vuelve a adjuntar el archivo correcto. El fallo intermitente comunicado no pudo
identificarse con certeza sin su mensaje; carga, re-guardado y reemplazo están probados.

**Ubicaciones:** todavía hay una ubicación vinculada a un solo componente. Compartir
una ubicación guardada con varios componentes requiere cambiar el modelo; es la
primera tarea de Fase 2. No borrar ubicaciones para intentar resolver esa limitación.

## Stock y movimientos

- Entrada: cantidad positiva que se suma al saldo.
- Salida: cantidad positiva que se resta; no puede superar el saldo disponible.
- Ajuste: diferencia positiva o negativa que cambia el saldo, sin dejarlo negativo.
- Cantidad cero no está permitida como movimiento.

Registrar entradas, salidas y ajustes desde Administración. Los movimientos ya guardados
son de consulta: no se pueden editar/eliminar, y guardar el mismo objeto otra vez no
cambia el saldo. Para corregir un error, registrar un movimiento compensatorio y motivo.
La cantidad y el componente de un stock existente son de sólo lectura en Admin;
sí se pueden editar sus límites siempre que sean válidos. Un componente con historial
no se elimina; se puede marcar inactivo. El stock inicial introducido directamente por
el flujo antiguo de Admin no genera historial automáticamente; el alta rápida sí lo registra.

## Consulta

Buscar por referencia, nombre, valor, número de parte o texto de categoría y ordenar
por nombre o cantidad. Sólo aparecen componentes activos. La búsqueda actual no
tiene paginación. El dashboard muestra bajo stock, ausencia de datasheet, ausencia de
oferta y diez movimientos recientes. Las pantallas comparten navegación y pie de versión.

## Respaldo

Antes de respaldar o restaurar, detener el servidor y conservar una copia independiente.
Actualmente el respaldo se opera mediante funciones de Python, sin botón en interfaz:

```powershell
.\.venv\Scripts\python.exe manage.py shell -c 'from django.conf import settings; from backups.backup_local import backup_project; print(backup_project(settings.DATA_DIR))'
```

Conservar la carpeta resultante que contiene SQLite y media, fuera de Git y preferiblemente
fuera del equipo. La restauración actual combina media con el destino: primero debe
validarse en una copia aislada; no garantiza eliminar archivos sobrantes. Fase 4 mejorará
y documentará recuperación consistente. No usar los datos personales como fixtures.

## Distribuir o desplegar

Decisión del usuario (12/10/2026): operar exclusivamente en su PC Windows y preparar
PyInstaller al finalizar. Las referencias a servidor son explicativas, fuera del alcance.

Waitress se usa mientras la aplicación está abierta: recibe las solicitudes del
navegador y las entrega a Django. PyInstaller se usa al construir la distribución:
reúne el programa, Python y sus dependencias. En la distribución prevista el usuario
abre InventariosAPP.exe, el programa inicia Waitress en 127.0.0.1 y abre el navegador;
Waitress permite consultar y guardar mediante Django, y SQLite conserva los datos.
No requiere servidor externo ni Internet; base y archivos permanecen fuera del ejecutable.

Gunicorn es un servidor HTTP/WSGI que ejecuta Django; PyInstaller empaqueta Python
y dependencias como ejecutable. No son equivalentes ni pasos obligatorios consecutivos.
[Django documenta la integración con Gunicorn](https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/gunicorn/).

| Destino | Propuesta | Cómo accede el usuario |
|---|---|---|
| Windows personal | Django + Waitress; paquete .exe opcional | Navegador en localhost |
| Varios equipos | Servidor Linux + Gunicorn detrás de proxy HTTPS | Navegador a URL del servidor |

Para tu uso local se propone Waitress, que soporta Windows, y posteriormente un paquete
PyInstaller para distribuir sin instalar Python. El .exe iniciará el servidor
local y abrirá el navegador; la interfaz seguirá siendo web. Debe incluir plantillas y
estáticos, atender PDFs, cerrar correctamente y guardar SQLite/media/configuración
en una carpeta persistente del usuario, independiente de la instalación. Inicialmente
conviene probar distribución en carpeta antes de un único ejecutable.
Fuentes: [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/) y
[PyInstaller](https://pyinstaller.org/en/stable/operating-mode.html).

Gunicorn es una buena opción para el servidor Linux; su proyecto se describe como
servidor para UNIX. Para Windows nativo la propuesta de este proyecto es Waitress.
No hace falta convertir Gunicorn en .exe: el despliegue compartido ejecuta Django en
el servidor, y cada usuario abre su navegador. Fuente: [Gunicorn](https://github.com/benoitc/gunicorn).

Antes de distribuir se necesitan configuración DEBUG=False, clave propia por instalación,
permisos de acceso, servicio de estáticos y media, backups y actualización probada.
Para publicar en red se añaden dominio, HTTPS y arranque supervisado. SQLite se conserva
para el escenario local; varias escrituras simultáneas pueden requerir PostgreSQL.
La configuración actual todavía no implementa estos destinos. Referencia de preparación:
[checklist de Django](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/).

## Funcionalidad pendiente

Fase 1 está implementada y requiere tu revisión.
Fase 2: ubicaciones compartidas, perfiles de permisos, ficha, especificaciones y PDF.
Fase 3: ofertas, filtros, duplicación y acciones de inventario.
Fase 4: recuperación y distribución verificada. Este manual se actualizará con rutas
y capturas reales al implementar; no se presentan acciones futuras como disponibles.
