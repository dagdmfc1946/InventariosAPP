# Distribución local y desarrollo — InventariosAPP v2.3.0

Estado: candidato local para revisión. El binario final está generado, pero Smart App
Control bloquea su ejecución en este PC; la validación final del .exe queda pendiente.

Destino: Windows x64, uso exclusivo en este PC mediante navegador. El ejecutable usa
Waitress y contiene Python, Django y dependencias; el destinatario no debe instalar Python.
La consola permanece abierta para controlar el servidor. Cerrar el navegador no lo detiene.

## Primera instalación: base vacía

El paquete no contiene ninguna base, cuenta, componente, oferta, PDF personal ni `.env`.
En una carpeta de datos nueva, el primer arranque aplica las migraciones y crea únicamente
las tablas, permisos y perfiles Lector/Operador. No existe una contraseña predeterminada.

Desde PowerShell, dentro de la carpeta donde está el ejecutable:

```powershell
.\InventariosAPP.exe init
.\InventariosAPP.exe manage createsuperuser
.\InventariosAPP.exe
```

`createsuperuser` solicita tus datos y contraseña en la terminal. Luego abre el navegador
para iniciar sesión. Crear categorías, ubicaciones y componentes desde cero.

Datos predeterminados: `%LOCALAPPDATA%\InventariosAPP\data`.
Incluye `db.sqlite3`, `media` y `.runtime-key` (secreto aleatorio propio de esa instalación).
Conservar la carpeta completa: el `.exe` se puede mover/reemplazar sin perder estos datos.
No guardar el secreto ni los respaldos en el repositorio.

Para una instalación de prueba completamente vacía, elegir **una carpeta nueva**:

```powershell
.\InventariosAPP.exe --data-dir 'D:\InventariosAPP_Prueba\data' init
.\InventariosAPP.exe --data-dir 'D:\InventariosAPP_Prueba\data' manage createsuperuser
.\InventariosAPP.exe --data-dir 'D:\InventariosAPP_Prueba\data' serve --port 8003 --no-browser
```

Reutilizar una carpeta de datos conserva sus registros. `init`, el arranque y generar
un nuevo `.exe` **nunca vacían una base existente**. La condición de base vacía aplica a
instalaciones nuevas. Los datos originales del proyecto y `.local/dev_v2` se conservan.

## Ejecutar y detener desde terminal

```powershell
.\InventariosAPP.exe serve --port 8000 --no-browser
.\InventariosAPP.exe --help
.\InventariosAPP.exe --version
.\InventariosAPP.exe manage check
```

Abrir `http://127.0.0.1:8000/search/`. El servidor escucha solo en 127.0.0.1; no admite
una opción para exponerlo en la red. Si el puerto está ocupado, usar otro con `--port`.
Detener con **Ctrl+C** y esperar el mensaje de cierre antes de respaldar o actualizar.
Solo una instancia o proceso de mantenimiento puede utilizar la misma carpeta de datos.

## Respaldar y restaurar

Detener la aplicación y cualquier `runserver`/comando que escriba en esa carpeta.
El bloqueo del launcher impide respaldar/restaurar mientras su servidor la usa; no
controla un proceso ajeno iniciado directamente con manage.py. No ejecutar escrituras
externas durante estas operaciones.

```powershell
.\InventariosAPP.exe backup --output 'D:\RespaldosInventario\respaldo_2026-10-12'
.\InventariosAPP.exe restore 'D:\RespaldosInventario\respaldo_2026-10-12'
```

El destino de respaldo debe ser nuevo. Incluye snapshot SQLite, PDF, clave local y
manifiesto SHA256. La base se copia con la API SQLite y se verifica su integridad.
Los archivos se comprueban antes de restaurar. La restauración reemplaza completamente
la carpeta de datos, por lo que no mezcla PDF antiguos; conserva el estado anterior en
una carpeta hermana `data.previous-...`. No restaura sobre la raíz del código/disco.

Si se necesita volver atrás: con todos los procesos detenidos, conservar también el
estado restaurado, renombrándolo a una carpeta nueva; renombrar la carpeta `data.previous-...`
al nombre original `data`. Ambos estados permanecen disponibles. Si hay un error de
instalación de la restauración, el proceso intenta reponer automáticamente el directorio
original. No borrar las carpetas previas hasta confirmar funcionamiento y respaldos.

Estos respaldos son del nuevo formato verificado. Las copias antiguas sin `manifest.json`
no se restauran automáticamente: deben revisarse y convertirse en una carpeta aislada.

## Continuar el desarrollo desde el código fuente

El `.exe` es una distribución; conservar el repositorio fuente para modificar el programa.
En PowerShell dentro del proyecto:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8001
```

Desarrollo usa `config.settings`, DEBUG=True y `.local/dev_v2` por defecto. Revisar `.env`
y `INVENTARIOS_DATA_DIR` antes de ejecutar migraciones: no apuntar a datos de distribución.
Si no existe el entorno, crear `.venv` con Python 3.12 (`py -3.12 -m venv .venv`).

Después de cambiar modelos, ejecutar `manage.py makemigrations`, revisar las migraciones
y probarlas en una copia respaldada. Actualizar `config/version.py`, fecha y CHANGELOG.
No editar manualmente una base ni borrar migraciones publicadas para reiniciarla.

## Generar un nuevo ejecutable

1. Terminar el cambio, actualizar SemVer (por ejemplo 2.3.1 para corrección), fecha,
   CHANGELOG, manual e informe de validación con los resultados de esa versión. Guardar
   las migraciones necesarias en el repositorio.
2. Verificar y empaquetar con el entorno del proyecto:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
$env:TEMP = Join-Path (Get-Location) 'backups/verification_tmp'
$env:TMP = $env:TEMP
.\.venv\Scripts\python.exe manage.py test --noinput
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe build_exe.py
```

El script ejecuta collectstatic y usa `InventariosAPP.spec`. Resultado:
`dist/v<versión>/InventariosAPP.exe`, documentación, avisos en `licenses/` y
`BUILD_INFO.json` con SHA256/versiones de dependencias. Distribuir la carpeta completa.
Los recursos se incluyen explícitamente y se comprueba que no haya bases ni secretos.
Las dependencias de empaquetado están en requirements-build.txt; las de ejecución en
requirements.txt. Construir Windows desde Windows, sin copiar el entorno virtual al destino.

3. Probar el nuevo ejecutable en una **carpeta de datos nueva**, desde una ubicación fuera
   del proyecto, con Python y el entorno virtual fuera del PATH. Comprobar init, creación
   de usuario, acceso, estilos, altas/movimientos, PDF, respaldo/restauración y cierre.
4. Para actualizar una instalación utilizada: detener, respaldar y verificar el respaldo;
   reemplazar solo el ejecutable. Mantener la carpeta de datos. Al iniciar se aplican
   migraciones pendientes, con un respaldo previo automático si la base ya existe.
   No basta con recuperar solo el `.exe` anterior si cambió el esquema: usar su respaldo
   completo con el programa compatible para volver atrás.
5. Pedir aprobación antes de publicar en Git o distribuir una nueva versión.

Django actualizado a 5.2.18 dentro de la serie 5.2; las dependencias fijadas se revisan
al preparar nuevas versiones.

La construcción no reinicia ni incluye datos de trabajo; cada instalación nueva parte
vacía. Un proceso repetido de build mantiene los datos de instalaciones anteriores.
PyInstaller empaqueta el código pero no garantiza que resulte imposible recuperarlo.

## Configuración y referencias

Waitress sirve Django, WhiteNoise entrega los estáticos recolectados y Django mantiene
la autorización de PDF. DEBUG=False; secreto persistente aleatorio; no se sirven carpetas
media sin validación. El escenario HTTP en loopback explica las cuatro advertencias
HTTPS de check --deploy (HSTS, redirección y cookies Secure). No habilitar este diseño en
red o Internet sin revisar TLS, configuración, permisos y concurrencia.

Fuentes: [Waitress](https://docs.pylonsproject.org/projects/waitress/en/latest/arguments.html),
[WhiteNoise/Django](https://whitenoise.readthedocs.io/en/stable/django.html),
[PyInstaller/spec](https://pyinstaller.org/en/stable/spec-files.html).


## Firma de Windows y estado de validación

El ejecutable v2.3.0 final no tiene firma Authenticode. En este equipo, Windows bloqueó
su arranque con Smart App Control. Eventos CodeIntegrity 3033/3077/3118 confirman
el incumplimiento de los requisitos de firma; no es una excepción de Django.
Se conservaron las protecciones del equipo. No se considera una distribución final aprobada.

Microsoft documenta la firma con certificados de proveedores de confianza para estas
políticas: [Smart App Control](https://learn.microsoft.com/windows/apps/develop/smart-app-control/overview).
Una firma autofirmada no equivale a una firma de un proveedor reconocido.
Si se incorpora firma, firmar después de construir y recalcular SHA256 en BUILD_INFO.json;
probar nuevamente el binario firmado y sus dependencias antes de distribuirlo.
No se adquiere ningún certificado ni se cambia una política de seguridad automáticamente.

Un primer artefacto de prueba, previo a actualizar Django, pudo ejecutar versión,
inicialización vacía y creación de administrador ficticio fuera del proyecto con Python
fuera de PATH. Ese resultado no valida el artefacto final con Django 5.2.18.
Con el código final se verificaron 125 pruebas y los flujos mediante el lanzador Python:
Waitress, sesión, estáticos, PDF, movimientos, respaldo/restauración y actualización.
Falta validar el binario final y repetir en otro Windows x64 limpio sin Python instalado.

Mientras se resuelve la firma, se puede ejecutar la misma configuración local desde fuente:

```powershell
.\.venv\Scripts\python.exe launcher.py --data-dir 'D:\InventariosAPP_Prueba\data' init
.\.venv\Scripts\python.exe launcher.py --data-dir 'D:\InventariosAPP_Prueba\data' manage createsuperuser
.\.venv\Scripts\python.exe launcher.py --data-dir 'D:\InventariosAPP_Prueba\data' serve --port 8003 --no-browser
```

Para desarrollar, seguir usando `manage.py runserver` con los pasos anteriores.
