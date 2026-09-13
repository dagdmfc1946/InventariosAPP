# InventariosAPP
Acá se encontrará documentado el desarrollo por fases conforme se vaya avanzando con el proyecto, la idea es ir acutalizando la documentación cada vez que se haga un cambio en una fase en específico y/o se agreguen cambios.

## Estado actual
F1 completada: entorno virtual Python 3.12, dependencias mínimas y configuración segura preparados y verificados.
F2 completada: base del proyecto Django configurada, apps modulares creadas y validadas con configuración inicial.
F3 completada: modelos del dominio de inventario definidos, migraciones generadas y comprobadas.
F4 iniciada: administración con Django Admin configurada para los modelos principales del MVP.

### Registro de cambios

- **F1 — Preparación del entorno — Completada (2026-09-13)**
   - Se creó `requirements.txt` con Django 5.2.6 y `python-decouple` 3.8.
   - Se preparó el entorno virtual local `.venv` con Python 3.12; no se versiona.
   - Se confirmó `.env.example` sin secretos reales y `.gitignore` para excluir `.env`, bases de datos, archivos cargados, respaldos y entornos virtuales.
   - Se verificó la instalación de dependencias y la comprobación de Django.
   - El proyecto Django se reserva para F2.

- **F2 — Base del proyecto Django — Completada (2026-09-13)**
   - Se creó el proyecto Django base con `django-admin startproject config .`.
   - Se añadieron las apps modulares: `core`, `components`, `suppliers`, `inventory`, `documents` y `dashboard`.
   - Se configuraron `INSTALLED_APPS`, rutas de templates, media y archivos estáticos y la gestión segura de entorno con `python-decouple`.
   - Se definió la decisión de ubicación inicial en modo **1-1**: cada componente tendrá una sola ubicación física en el MVP, manteniendo la estructura simple y controlable.
   - Se verificó la base del proyecto con `python manage.py check`.

- **F3 — Modelo de datos y migraciones — Completada (2026-09-13)**
   - Se implementaron los modelos de `Category`, `Component`, `Specification`, `Supplier`, `SupplierOffer`, `Location`, `Stock`, `StockMovement` y `Datasheet`.
   - La relación de ubicación se mantiene en modo **1-1** para el MVP, con una ubicación por componente.
   - Se generaron y aplicaron migraciones con validación real mediante `makemigrations` y `migrate`.

- **F4 — Administración con Django Admin — En desarrollo (2026-09-13)**
   - Se registraron los modelos principales en el administrador con listados, filtros, búsquedas e inlines.
   - Se habilitaron `SpecificationInline` y `SupplierOfferInline` para facilitar la edición de relaciones.
   - Se validará la administración con el arranque del servidor de Django y la comprobación del panel de administración.

---

1. **F0 — Validación de decisiones técnicas**  
   Cerrar las decisiones pendientes antes de crear código.

---

2. **F1 — Preparación del entorno**  
   Python, `venv`, Django, dependencias mínimas, `.env.example`, `.gitignore`, estructura de documentación y verificación de ejecución local.

---

3. **F2 — Base del proyecto Django**  
   Crear proyecto, apps modulares, configuración de rutas, estáticos, media y parámetros de seguridad básicos.

---

4. **F3 — Modelo de datos y migraciones**  
   Implementar categorías, componentes, especificaciones, proveedores/ofertas, stock, movimientos, ubicaciones y datasheets. Crear migraciones y pruebas de integridad.

---

5. **F4 — Administración con Django Admin**  
   Configurar CRUD administrativo, filtros, búsquedas e inlines para gestionar datos sin desarrollar formularios personalizados innecesarios.

---

6. **F5 — Gestión de datasheets**  
   Carga y validación de PDF, límite de tamaño, almacenamiento en `media/`, consulta segura y verificación de archivos faltantes.

---

7. **F6 — Stock y trazabilidad**  
   Implementar entradas, salidas y ajustes; impedir cantidades inválidas y mantener historial de movimientos.

---

8. **F7 — Buscador personalizado**  
   Vista de consulta rápida con filtros, paginación y ordenamiento.

---

9. **F8 — Dashboard**  
   Indicadores: bajo stock, componentes sin datasheet, sin precios y registros recientes.

---

10. **F9 — Backup, exportación y operación local**  
    Scripts para respaldar SQLite y `media/`; documentación de restauración y arranque.

---

11. **F10 — Pruebas y control de calidad**  
    Pruebas unitarias, integración, validación manual y revisión de seguridad básica.

---

12. **F11 — Estabilización y documentación final**  
    Corrección de incidencias, guía de instalación/uso y versión candidata.

---

13. **F12 — Empaquetado Windows**  
    Generar y probar el ejecutable `.exe` cuando el flujo local sea estable.

---
