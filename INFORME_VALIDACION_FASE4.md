# Validación de Fase 4 — v2.3.1

Fecha local: 12/10/2026 (America/Bogota). Rama: dev_v2.
Estado: **candidato local verificado en este PC; revisión/publicación del usuario pendiente**.

## Resultado vigente

- 125 pruebas automatizadas correctas en 98.047 s; cero errores/fallos. Tres pruebas
  PDF repetidas después del ajuste de paleta, correctas en 0.747 s; no se suman como casos nuevos.
- UI UX Pro Max aplicada en todo el aplicativo y Administración. Sistema visual:
  design-system/inventariosapp/MASTER.md. Fuente local, SVG locales, navegación activa,
  contraste, controles legibles, tablas, formularios, perfil y estados de error coherentes.
- 23 vistas renderizadas, 404/500, PDF y roles comprobados desde fuente. Navegador
  revisa altas/edición/duplicación/movimientos/ofertas/perfil/contraseña/ubicaciones/
  proveedores/Admin/usuarios, además del catálogo y resumen. Tamaños 375/768/1024/1440 px.
  Sin overflow horizontal del documento; tablas pueden desplazarse dentro de su región.
- Resumen de errores enfocable con tres enlaces a campos inválidos, texto conservado
  y aria-describedby/aria-invalid. Mostrar/Ocultar probado sin cambiar credenciales.
- Contraste principal/secundario/acción/error: 12.87/5.94/6.72/6.23:1; borde de control 3.15:1.
  No se declara certificación WCAG completa ni ensayo con lector de pantalla.

## Ejecutable realmente probado

Paquete onedir: `dist/v2.3.1/InventariosAPP/`. Abrir InventariosAPP.exe manteniendo
_internal, manuales y licencias junto a él. ZIP completo generado en dist/v2.3.1.
EXE: **8.177.726 bytes**, SHA256 `7d0e9b3c4e9ce64328d05065ba9636f4daf3b7da11b8f4c589db7c6b457848a4`.
Python 3.12.10, Django 5.2.18, Waitress 3.0.2, WhiteNoise 6.12.0, ReportLab 4.5.1,
PyInstaller 6.22.0. Sin firma Authenticode ni cambios de políticas Windows.

Se extrae en una carpeta fuera del proyecto con espacios, se retira Python del PATH
y se eliminan PYTHONPATH/PYTHONHOME. El exe ejecuta init vacío, restore y createsuperuser
ficticio por terminal. El código y los recursos se cargan desde _internal del paquete.

Smoke dentro del proceso congelado verifica **23 vistas, siete recursos estáticos
con hash, PDF, datasheet protegido, roles Lector/Operador, contraseña sin algoritmos
y rechazo de contraseñas comunes**. Salida ficticia 3 desde 120: preview no escribe,
registro deja 117 y repetición mantiene 117. Cuenta y datos solo de prueba.

Waitress arrancado por el exe permite acceso real desde navegador a catálogo/resumen,
con el diseño final y DEBUG=False. Ctrl+C muestra cierre. Backup mientras está abierto
rechazado; detenido permite copia/restauración/init y conserva saldo 117 en otra carpeta.

Primera instalación: cero usuarios, categorías, componentes, especificaciones, stocks,
movimientos, ubicaciones, proveedores, ofertas y datasheets. Solo schema/permisos/perfiles.
El paquete no incluye ninguna base, cuenta, documento personal, .env ni clave local.

## Incidencia de empaquetado y reconstrucción

El primer lanzador onedir fue permitido por Windows. Smoke descubrió un recurso oficial
Django omitido: common-passwords.txt.gz. Se incorpora al hook explícito; el validador
se mantiene habilitado. Al recompilar, Windows bloqueó el archivo nuevo, aunque el código
no había cambiado. No se desactiva Smart App Control ni se crea una excepción.

Comparación completa: mismas entradas/contenidos del archivo Python embebido; seis
bytes distintos limitados a fechas PE/debug y checksum. Biblioteca base ZIP: todos los
módulos idénticos, cambia su contenedor. Recursos compartidos idénticos, salvo la adición
de la lista oficial. Se conserva **una copia exacta del lanzador original**, sin editar
sus bytes, y se completa el paquete con recursos correctos. Ese paquete supera el smoke
completo y la prueba HTTP real. BUILD_INFO.json registra ambas sumas y la reutilización.

build_exe.py permite --reuse-launcher únicamente si todo el binario coincide salvo
esas fechas/checksum; rechaza otros bytes de diferencia, comprobado con una alteración
en memoria. No permite usar un lanzador viejo cuando cambia código o versión.

El resultado de este archivo no garantiza aceptación de otra compilación por Windows.
La ejecución de otro PC limpio sin Python no se ensayó: el destino solicitado es este PC.
SHA256SUMS.txt verifica integridad del paquete y no equivale a una firma digital.

## Datos, trazabilidad y cierre

Base original intacta: SHA256
B247D32672C3D77C9DF9F377C833061D79AAFF9A7010112AB9776096616F12E2.
Datos QA separados en .local; bases/media de trabajo no se vacían ni se distribuyen.
Artefacto onefile previo retirado por autorización del usuario; logs históricos conservados.

Logs locales: ui_fase4_tests.log, ui_v231_pdf_tests.log, build_onedir_v231_final.log,
onedir_code_comparison.json. Evidencias PNG locales de UI/frozen en .local/evidence.
T16–T20 verificados para el destino local. Control F4 y push pendientes de revisión.
Guía vigente: DISTRIBUCION_Y_DESARROLLO.md.

---

Lo siguiente conserva el historial anterior; no describe el paquete vigente.

## Historial v2.3.0 — artefacto onefile retirado

Fecha: 12/10/2026. Rama: dev_v2. Estado: candidato local; distribución final pendiente.
Referencia anterior publicada: 8cef3d60cc414a86b883c341ab03d5a77827fd09 (v2.2.0).

## Resultado ejecutivo

**125 pruebas automatizadas aprobadas**, sin errores ni fallos, en **121.355 segundos**
con Django 5.2.18. Se mantienen las 115 de la versión anterior y se añaden seis de
recuperación y cuatro de configuración/bloqueo local. Este resultado no expresa
un porcentaje de cobertura ni sustituye las pruebas del ejecutable.

| Área nueva | Casos | Resultado |
|---|---:|---|
| Snapshot consistente de SQLite, medios y manifiesto; destino protegido | 1 | Correcto |
| Restauración completa y conservación del estado previo | 1 | Correcto |
| Copia corrupta rechazada antes de modificar destino | 1 | Correcto |
| Rutas de manifiesto fuera de respaldo rechazadas | 1 | Correcto |
| Fallo de instalación revierte a carpeta original | 1 | Correcto |
| Restauración sobre raíz del proyecto rechazada | 1 | Correcto |
| Clave persistente y DEBUG=False sin crear datos prematuramente | 1 | Correcto |
| Exclusión de segunda instancia y liberación de bloqueo | 1 | Correcto |
| Argumentos Django y rechazo de host externo | 1 | Correcto |
| Clave inválida no se sustituye silenciosamente | 1 | Correcto |

El resto del alcance se conserva en [informe de 115 pruebas](INFORME_EJECUTIVO_PRUEBAS.md).
Log local final: `.local/fase4_full_tests_django518.log`. La salida de argparse al
rechazar `--host 0.0.0.0` es esperada por una prueba; la suite termina con OK.

## Comprobaciones operativas del código final

- Lanzador con configuración local real y Waitress: acceso desde navegador a catálogo,
  sesión y estilos en 127.0.0.1:8002; versión visible v2.3.0. Detención con Ctrl+C
  muestra «Aplicación detenida» en terminal. Mantenimiento posterior obtiene el bloqueo.
- Cinco vistas autenticadas (catálogo, resumen, perfil, admin y ficha) responden 200.
  PDF de catálogo y datasheet válidos; acceso anónimo al documento redirige al login.
  Estático con nombre hash servido con DEBUG=False; usuario sin detalles criptográficos.
- Salida ficticia 3 desde saldo 10: vista previa no guarda, registro deja 7,
  reenvío conserva 7. No se modifica el inventario del usuario.
- Lanzador rechaza un respaldo mientras Waitress tiene abierta la misma carpeta.
- Respaldo validado con SQLite y tres archivos de datos/clave/PDF. Tras modificar
  únicamente la copia ficticia a 99 y añadir un archivo sobrante, restaurar recupera
  7 y elimina el sobrante del estado activo. La carpeta previous conserva 99 y el archivo.
- Actualización simulada en copia ficticia: migración pendiente provoca snapshot
  verificado antes de aplicar, mantiene el componente y saldo 7. Registro de migraciones
  se manipuló solo para esta prueba temporal, nunca en datos del usuario.
- Base aislada de primera instalación: cero usuarios, categorías, componentes,
  especificaciones, stocks, movimientos, ubicaciones, proveedores, ofertas y datasheets.
  Existen tablas, permisos y perfiles predefinidos; no credenciales predeterminadas.
- `pip check`: sin incompatibilidades. `makemigrations --check --dry-run`: sin cambios.
  `check --deploy`: cuatro advertencias W004/W008/W012/W016 por HTTP en loopback
  (HSTS, redirección HTTPS y cookies Secure). No se silencian ni se afirma aptitud para Internet.

## Artefacto y bloqueo observado

Archivo: `dist/v2.3.0/InventariosAPP.exe`, Windows x64, consola, **31.713.511 bytes**.
Django 5.2.18, Waitress 3.0.2, WhiteNoise 6.12.0, ReportLab 4.5.1, PyInstaller 6.22.0.
SHA256: `12a9ba355f02b25fb30ac66e76cfb83f1f5f1ec012a8b690d0e5d3af3bab02fd`.

Construcción correcta e inspección de 4.236 entradas: sin SQLite, .env, claves ni media
personal. Incluye manifest de estáticos, fuente Vera y plantilla propia de contraseña.
Licencias y manuales acompañan el programa. No se distribuye el entorno virtual.

**Windows Smart App Control bloquea la ejecución del artefacto final** en la carpeta
de salida y en una copia fuera del proyecto. Authenticode: NotSigned. Eventos
CodeIntegrity 3033/3077/3118 señalan requisitos de firma. No se desactivaron protecciones.
Orientación de firma: [documentación de Microsoft](https://learn.microsoft.com/windows/apps/develop/smart-app-control/overview).

Un primer binario, previo a actualizar Django, ejecutó --version, init y creación
administrativa ficticia fuera del proyecto y con PATH sin Python. El binario final
**no** supera aún esa validación: no se transfieren los resultados del binario anterior.
El usuario confirma que no dispone de certificado. No se realiza compra ni cambio de
seguridad. También queda pendiente otro PC Windows x64 sin Python instalado y la revisión
del usuario.

## Protección del inventario y decisión de cierre

SHA256 de db.sqlite3 original, sin cambios:
`B247D32672C3D77C9DF9F377C833061D79AAFF9A7010112AB9776096616F12E2`.
Datos ficticios separados en `.local/fase4_*`; no se vacía la copia de desarrollo.

T16, T17, T18 y T20 completadas localmente. T19 construida, pero falta validación final
por el bloqueo de firma. Control F4 queda pendiente; no se publica ni integra en dev/main.
[Guía de instalación, desarrollo y reconstrucción](DISTRIBUCION_Y_DESARROLLO.md).
