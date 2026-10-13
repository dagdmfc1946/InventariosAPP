# Manual de usuario — InventariosAPP

Actualizado: 12/10/2026. Versión `v2.3.1` publicada en `dev_v2`; interfaz y distribución onedir verificadas localmente.
Fases 1, 2 y 3 concluidas en `dev_v2`. La versión anterior sigue en `dev`.

## Datos separados para revisar v2

Esta rama usa por defecto `.local/dev_v2/db.sqlite3` y `.local/dev_v2/media`.
La copia de desarrollo ya fue preparada en este equipo. Conserva las cuentas que
tenías en la base original: usa tus credenciales habituales. No usar la cuenta de
prueba visual: sólo existe en otra base ficticia independiente.

INVENTARIOS_DATA_DIR permite elegir otra carpeta. Cambiar de rama no separa datos
automáticamente; no apuntar la versión en desarrollo a los datos operativos.
Si ya hay copia, no ejecutar de nuevo prepare_dev: rechaza sobrescribirla.

## Iniciar y cerrar

Para preparar el código después de clonar en otro PC Windows, instala Python 3.12
con el lanzador `py` y ejecuta **preparar_proyecto.bat** en la raíz del proyecto.
Admite doble clic o PowerShell (`.\preparar_proyecto.bat`); necesita Internet para
instalar dependencias y solicita crear el administrador si no existe uno activo.
Conserva los datos y usuarios al repetirlo.

Para iniciar, ejecuta **iniciar_desarrollo.bat** con doble clic o PowerShell
(`.\iniciar_desarrollo.bat`). Abre la dirección indicada en la consola:
`http://127.0.0.1:8000/admin/`. El archivo inicia el servidor; no abre el navegador
automáticamente. Administración exige una cuenta autorizada. Si el navegador
conserva una sesión válida, no pedirá la contraseña nuevamente; usa **Salir** al
terminar para cerrar esa sesión. Los usuarios Lector/Operador acceden por
`/accounts/login/`, como se explica en la siguiente sección.

Estos archivos se usan para desarrollo desde código. El ZIP del ejecutable incluye
sus dependencias y conserva sus datos en una carpeta independiente. Consulta la
[guía de instalación y desarrollo](DISTRIBUCION_Y_DESARROLLO.md) para ambos casos.

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

Al crear una cuenta se elige **Lector** (consultar inventario y PDF) u **Operador**
(además registrar componentes, completar fichas, crear categorías/ubicaciones y cargar PDF).
Ambos son usuarios normales. Las cuentas existentes no cambian de grupo automáticamente.
Desde su edición, el superusuario puede asignar **Inventario - Lector** o
**Inventario - Operador**, o mantener permisos individuales. El comando
`manage.py configure_inventory_roles` prepara/actualiza esos perfiles sin asignar cuentas.
La gestión de cuentas está reservada al superusuario.

Los usuarios normales deben entrar por `/accounts/login/`, o **Iniciar sesión** en
el catálogo. `/admin/login/` está reservado a cuentas con acceso administrativo:
no poder entrar ahí no demuestra que la contraseña sea incorrecta. La pantalla
administrativa incluye un enlace al acceso del aplicativo.

Si falla el acceso normal, comprobar usuario exacto, contraseña y que la cuenta esté
activa. Las cuentas sin contraseña utilizable requieren que el responsable les
establezca una desde la edición de usuario. No se cambian contraseñas existentes al
actualizar y no se almacenan contraseñas en texto plano.

El catálogo, resumen y PDF requieren sesión. Un usuario sin permisos recibe una
pantalla de acceso restringido: eso no equivale a contraseña incorrecta. Al salir,
se vuelve a la pantalla de inicio de sesión.

## Mi perfil

1. Pulsar **Mi perfil** en el encabezado, junto al nombre de la sesión, o abrir
   `/accounts/profile/`. También está disponible desde Administración.
2. Editar **Nombre de usuario** (nombre de acceso obligatorio y único), nombre, apellidos
   y correo electrónico (opcionales). El nombre de acceso admite letras, números y
   @/./+/-/_. No se acepta otro usuario existente, incluso con distinta capitalización.
3. Pulsar **Guardar mi perfil**. Un correo inválido muestra el error y conserva lo escrito.
4. La sesión permanece abierta. Esta pantalla sólo cambia tu propia cuenta;
   la contraseña y los permisos se conservan.

## Ficha completa del componente

1. En el catálogo, pulsar la referencia/nombre para abrir su ficha.
2. Los operadores pueden pulsar **Editar ficha** para cambiar datos básicos y ubicación.
3. **Crear una categoría aquí** o **Crear una ubicación aquí** crea y selecciona el
   registro conservando los campos escritos. La categoría/ubicación queda creada en
   ese momento; el componente y su asignación se confirman con **Guardar ficha**.
4. Agregar especificaciones con atributo, valor y unidad opcional. **Agregar especificación**
   añade una fila; sin JavaScript también funciona mediante el servidor. Marcar
   **Eliminar** retira una especificación al guardar. Los atributos no se pueden repetir.
5. Guardar ficha confirma datos y especificaciones juntos. Si hay errores, no guarda
   parcialmente. El saldo y los movimientos no se modifican desde esta edición.
6. En la ficha, **Adjuntar PDF** guarda una ficha técnica por separado. Acepta extensión
   PDF, tamaño hasta 20 MB y cabecera de PDF. Es una comprobación básica de formato;
   no analiza el contenido completo del documento. Cargas rechazadas no se guardan.
7. **Abrir PDF** exige sesión y permiso de consulta, incluso mediante la ruta de media.
   Si falta el archivo, se indica que no está disponible; adjuntar la copia correcta.

## Ubicaciones compartidas

Abrir **Ubicaciones** y crear o editar una. Indicar al menos estante, caja, cajón o
descripción. En **Componentes en esta ubicación**, seleccionar varios componentes
(en PC, mantener Ctrl). Guardar agrega los seleccionados a esa ubicación; los retirados
quedan sin ubicación, y los elegidos desde otra ubicación se trasladan a ésta.
Cada componente tiene como máximo una ubicación. Los saldos no cambian.

También funciona desde Administración → Ubicaciones. Una ubicación con componentes
asignados está protegida contra borrado: primero retirar o reasignar esos componentes.

## Nombre de acceso y contraseña

Desde **Mi perfil** puedes modificar tu nombre de usuario. Al guardar se mantiene
la sesión; la próxima vez inicia sesión con el nuevo nombre y tu contraseña habitual.
El cambio conserva permisos, componentes y movimientos porque la cuenta mantiene su ID.
Solo se modifica la cuenta de la sesión activa; no permite cambiar roles ni privilegios.

En **Administración → Usuarios → Modificar**, el campo Contraseña muestra
**Contraseña configurada** o **Sin contraseña para iniciar sesión**. No muestra
algoritmos, iteraciones ni fragmentos de la contraseña almacenada. El botón
**Cambiar contraseña** o **Establecer contraseña** abre el formulario habitual de Django.
No se puede consultar la contraseña actual ni editarla como texto en ese campo.

## Descargar componentes en una tabla PDF

1. Abrir **Componentes**. Si quieres una selección, aplicar búsqueda/filtros con **Buscar**.
2. Pulsar **Descargar tabla PDF** debajo de los filtros.
3. Guardar el archivo `componentes-AAAA-MM-DD.pdf` cuando lo solicite el navegador.

El PDF incluye todos los componentes activos que coinciden con los filtros **ya
aplicados**, aunque ocupen varias páginas en pantalla; ignora el número de página.
Sin filtros, incluye todo el catálogo activo. Mantiene el orden seleccionado y registra
fecha/hora, total y filtros. Las columnas son referencia interna, nombre, categoría,
valor técnico, parte del fabricante, ubicación y unidades. El informe refleja los datos
al descargarlo; si cambian las existencias, vuelve a descargar para actualizarlo.
Los encabezados se repiten en cada página. Si no hay resultados, informa del total cero.
Solo usuarios con acceso al catálogo pueden descargarlo; se genera localmente sin
subir datos a servicios externos ni incluir credenciales o contraseñas.

## Alta rápida de componente y stock

1. Abrir `/search/` y pulsar **Nuevo componente**, o visitar `/components/new/`.
2. Iniciar sesión si se solicita. El superusuario existente puede usar la nueva pantalla.
3. Elegir categoría y completar **Referencia interna** (tu código, por ejemplo RES-001)
   y **Nombre del componente**. La referencia no se puede repetir dentro de la categoría.
   La **Ubicación** es opcional y puede asignarse después.
4. Indicar la **Cantidad inicial**. En **Datos técnicos opcionales**, completar
   **Valor técnico** (por ejemplo 10 kΩ, 100 µF o 5 V; no es un precio) y **Número de
   parte del fabricante** (por ejemplo LM358N) si se conocen. Para otros atributos
   usar las especificaciones de la ficha; los precios corresponden a ofertas de proveedores.
   En **Avisos y límite de existencias**, configurar **Mínimo de aviso** y **Máximo
   permitido** si se necesitan. El mínimo avisa cuando el saldo es igual o inferior;
   con mínimo 0 avisa al agotarse. Máximo 0 permite guardar sin límite superior.
   No se admiten negativos; el mínimo y la cantidad inicial no pueden superar un
   máximo distinto de cero. Los desplegables conservan los valores y se abren al tener errores.
5. Pulsar **Guardar componente** para volver al catálogo, o **Guardar y agregar otro**
   para continuar con un formulario limpio. El componente y su stock se guardan juntos.
6. Si falla la validación, revisar los mensajes; no se crean registros parciales.
   Si hay cantidad inicial positiva, aparece una entrada en el historial. Con cero,
   se crea stock sin movimiento de cantidad cero.

Si no hay categorías, el usuario con permiso puede usar **Crear una categoría aquí**.
Los usuarios no administradores necesitan permisos para agregar componente, stock y
movimiento. Un usuario autenticado sin esos permisos recibe 403. No se conceden permisos
a las cuentas anteriores automáticamente; las nuevas reciben el perfil elegido en
su alta. El alta, login y logout usan CSRF; no requieren JavaScript.

## Completar información mediante Administración

La ficha propia permite completar estos datos; Administración ofrece un flujo alternativo:
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

**Ubicaciones:** el administrador permite seleccionar varios componentes para una
ubicación guardada, y la ficha permite seleccionar una ubicación existente.

## Stock y movimientos

- Entrada: cantidad positiva que se suma al saldo.
- Salida: cantidad positiva que se resta; no puede superar el saldo disponible.
- Ajuste: diferencia positiva o negativa que cambia el saldo, sin dejarlo negativo.
- Cantidad cero no está permitida como movimiento.

Desde la ficha abre **Entrada, salida o ajuste**. Selecciona tipo, cantidad y motivo
obligatorio. **Ver saldo previsto** muestra el resultado sin guardar; **Registrar
movimiento** lo confirma y vuelve a la ficha. Para ajuste escribe la diferencia con
signo: si hay 10 y el conteo real es 8, usa −2. El historial completo se consulta por
páginas de 25 en la ficha según permisos.

El formulario vence en una hora. Si otro movimiento cambió el saldo, recarga la ficha
y revisa la cantidad antes de confirmar. Reenviar el mismo formulario no vuelve a aplicar
el movimiento; abrir un formulario nuevo sí representa otra operación. Si aparece un
fallo de base, revisa el historial antes de reintentar. Si el componente no tiene stock,
el primer movimiento crea un registro desde cero (requiere permiso de agregar stock).

Administración conserva la alternativa de registrar movimientos. Los movimientos ya guardados
son de consulta: no se pueden editar/eliminar, y guardar el mismo objeto otra vez no
cambia el saldo. Para corregir un error, registrar un movimiento compensatorio y motivo.
La cantidad y el componente de un stock existente son de sólo lectura en Admin;
sí se pueden editar sus límites siempre que sean válidos. Un componente con historial
no se elimina; se puede marcar inactivo. El stock inicial introducido directamente por
el flujo antiguo de Admin no genera historial automáticamente; el alta rápida sí lo registra.

## Consulta

Buscar por referencia, nombre, valor, número de parte o texto de categoría y ordenar
por nombre o cantidad. Sólo aparecen componentes activos. Combina categoría,
disponibilidad (con/sin existencias) y pendientes (bajo stock, sin PDF o sin oferta).
Pulsa Buscar; Anterior/Siguiente conserva filtros en páginas de 25. Limpiar filtros
restablece la consulta. Existencias bajas incluye el saldo igual al mínimo; componentes
sin registro de stock se incluyen en Sin existencias.

Resumen enlaza cada indicador al catálogo filtrado y cada movimiento a su ficha.
Todas las vistas comparten avatar, Sesión activa, Mi perfil, Cambiar contraseña y Salir
cuando hay sesión; Cambiar contraseña aparece si la cuenta tiene contraseña usable.
Usa la contraseña actual y confirma la nueva; guardar conserva tu sesión.

## Duplicar datos técnicos

Desde una ficha pulsa **Duplicar**, escribe una referencia nueva y confirma **Crear
copia técnica**. Copia categoría, nombre (editable), valor, número de parte y especificaciones.
La copia queda activa, sin ubicación y con existencias cero; sus límites son cero,
lo que significa sin máximo. No copia movimientos, PDF ni ofertas. Revisa la ficha,
asigna ubicación y registra una entrada cuando corresponda. Para copiar especificaciones
necesitas permiso de agregarlas; el componente original conserva sus datos y saldo.

## Proveedores y ofertas

El menú **Proveedores** permite consultar, buscar, crear y editar según permisos.
En la ficha usa **Agregar oferta** para elegir proveedor, número de parte, precio,
moneda, cantidad mínima de compra y los datos opcionales de consulta. Precio admite
cero, nunca negativos; compra mínima debe ser al menos uno. Moneda se convierte a
mayúsculas sin convertir importes. No se mezclan ni comparan precios de monedas distintas.

Si falta un proveedor, despliega **Crear proveedor sin perder la oferta** y pulsa
**Crear y seleccionar proveedor**. Se conservan los datos escritos; luego guarda la
oferta. El proveedor se guarda independientemente y permanece si cancelas la oferta.
La misma combinación componente/proveedor/número de parte no puede repetirse.
Usa **Editar** en la fila de una oferta para actualizarla. Registrar una cotización
no realiza compras ni modifica existencias.

El grupo Operador incorpora permisos de alta/edición de proveedores y ofertas; Lector
sólo consulta. Al actualizar otra copia v2, ejecuta `configure_inventory_roles` después
de `migrate` (en este equipo ya se hizo). El comando actualiza los grupos predefinidos
sin asignar cuentas existentes a otro grupo ni habilitar Administración.

## Respaldo y recuperación

Detener la aplicación antes de respaldar/restaurar. Desde la carpeta del ejecutable:

```powershell
.\InventariosAPP.exe backup --output 'D:\RespaldosInventarios\copia_20261012'
.\InventariosAPP.exe restore 'D:\RespaldosInventarios\copia_20261012'
```

El destino de copia debe ser nuevo. La copia incluye SQLite, documentos, clave local
si existe y manifiesto de integridad. Conservarla fuera del repositorio y preferiblemente
fuera del equipo. La restauración verifica la copia antes de reemplazar los datos:
no mezcla documentos antiguos y conserva la carpeta previa en `.previous-*`.
La terminal indica su ruta. El lanzador rechaza operaciones si esa carpeta está en uso.
`runserver` no participa en este bloqueo: también debe detenerse antes del mantenimiento.

Si Windows bloquea el ejecutable, usar los mismos comandos desde fuente con
`.\.venv\Scripts\python.exe launcher.py`, siempre con `--data-dir` explícito.
Detalles y recuperación del estado anterior: [guía de distribución](DISTRIBUCION_Y_DESARROLLO.md).

## Primera instalación y uso local

El paquete v2.3.1 no incluye la base ni documentos del proyecto. Una instalación nueva
empieza sin cuentas, categorías ni componentes. Las tablas y los perfiles se preparan
al iniciar; crear el administrador desde terminal:

```powershell
.\InventariosAPP.exe init
.\InventariosAPP.exe manage createsuperuser
.\InventariosAPP.exe
```

Datos en `%LOCALAPPDATA%\InventariosAPP\data`. Conservar toda esa carpeta al actualizar;
reconstruir o sustituir el ejecutable no vacía registros existentes.
Extraer y conservar toda la carpeta del paquete, incluido `_internal`: no mover el .exe solo.
El .exe abre el navegador e inicia Waitress localmente; mantener su consola abierta.
Detener con Ctrl+C antes de cerrar, respaldar o cambiar de versión.
Para abrir tú mismo el navegador: `InventariosAPP.exe serve --no-browser`.

Desarrollo: Django `runserver`. Uso local final: Django con Waitress.
PyInstaller reúne Python, dependencias y recursos en el ejecutable; la interfaz sigue
siendo web en localhost. Gunicorn cumple el papel de servidor WSGI en el proyecto Linux,
según la [explicación de servidores y distribución](docs/SERVIDORES_Y_DISTRIBUCION.md).

## Continuar desarrollo y generar otra versión

Consultar [DISTRIBUCION_Y_DESARROLLO.md](DISTRIBUCION_Y_DESARROLLO.md) para preparar
el entorno, probar, actualizar `config/version.py`/CHANGELOG, generar migraciones cuando
corresponda y ejecutar `build_exe.py`. El resultado se deja en `dist/v<versión>/` con
manuales, licencias y BUILD_INFO.json. No incorporar bases de desarrollo al paquete.

## Mejoras visuales v2.3.1

El mismo diseño se aplica a catálogo, resumen, ficha, formularios, ubicaciones,
proveedores, perfil/contraseña y Administración. La navegación destaca la sección
actual. Los encabezados de las tablas están centrados y las tablas anchas se pueden
recorrer dentro de su propio contenedor en móvil, también con teclado.

Al guardar un formulario con errores, el resumen enlaza los campos que debes corregir
sin eliminar sus mensajes ni los datos escritos. Mostrar/Ocultar permite comprobar
lo escrito en una contraseña: al abrir la vista sigue oculta. No revela claves guardadas.
Los estados vacíos y páginas de error conservan el diseño y una forma de volver.

## Estado de revisión

125 pruebas correctas, tres pruebas PDF repetidas después del ajuste de paleta,
23 vistas renderizadas y revisión visual en escritorio/móvil con datos ficticios.
El onefile previo se retiró. El paquete onedir funciona en este PC desde su exe,
fuera del proyecto y sin Python en PATH; se comprobaron vistas, PDF, permisos y respaldos. El resultado
actual del ejecutable consta en INFORME_VALIDACION_FASE4.md. Otro Windows x64 limpio
sin Python y la revisión/publicación del usuario siguen siendo comprobaciones separadas.
