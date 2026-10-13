# InventariosAPP — Sistema visual v2.3.1

Origen: UI UX Pro Max solicitada por el usuario, descargada mediante skill-installer
en .local/tools/skills/ui-ux-pro-max. Fuente: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.
Skill: .claude/skills/ui-ux-pro-max/SKILL.md; referencias quick-reference y pro-rules.
Stack real: Django 5.2, plantillas HTML y CSS propio. No se asume Tailwind/React.
La colección no tiene guía específica para Django: se aplican reglas generales web.

## Consultas verificadas y adaptación

Se ejecuta search.py por ruta absoluta con “inventory management dashboard minimal”
(--design-system, variance 3, density 7) y una revisión “inventory management internal tool”
(density 8). Estilo verificado: Minimalism & Swiss Style; paleta industrial slate/stock green.
La propuesta de composición comercial Feature-Rich Showcase no es aplicable al inventario,
y la tipografía académica del segundo resultado tampoco. No se persiste ese resultado
como una solución completa: se adopta un layout de herramienta operativa, conservando la
identidad verde y Segoe UI local por criterio de producto y funcionamiento sin Internet.
Búsquedas UX específicas verificadas: “error summary validation” y “focus not obscured”.

## Decisiones vigentes

- Fondo #f3f6f8, panel blanco, texto #1e3445, texto secundario #536677.
- Acción principal #17675a con texto blanco; error #a72d35, foco #a95708.
- Tokens en static/css/theme.css compartidos por app y Administración.
- Escala de espacio 8/16/24/32 px; radios 8/14 px y sombra tenue.
- Marca y sesión en fila común; navegación debajo. Orden DOM coincide con orden visual.
- Navegación muestra sección activa, con texto e iconos SVG locales decorativos.
- Campos legibles, controles principales de 44 px, ayuda persistente y errores enlazados.
- Tablas con cabeceras centradas, números tabulares y scroll local en pantallas pequeñas.
- Resumen con tarjetas enlazadas y tabla de movimientos. Ubicaciones agrupadas en tarjetas.
- Formularios y páginas de acceso/perfil/contraseña/errores siguen el mismo sistema.
- Administración conserva los widgets, permisos, inlines y flujos nativos de Django.
- Mostrar/ocultar contraseña solo cambia su visibilidad por petición del usuario.
- JavaScript añade aria-describedby, aria-invalid y foco al resumen de campos erróneos.
- Nada depende de CDNs, Google Fonts ni paquetes JS. Sin animaciones decorativas.
- Transiciones breves de color; prefers-reduced-motion elimina movimiento/transiciones.

## Verificación

Revisar desktop, 1440, 1024, 768 y 375 px; sin desbordamiento horizontal del documento.
Excepción deliberada: tablas pueden desplazarse dentro de su contenedor propio.
Contraste normal >=4.5:1, controles/foco >=3:1, zoom y texto largo, teclado, roles/permisos,
formularios válidos/inválidos y páginas de Administración. Suite existente de 125 pruebas.
La validación visual no constituye certificación WCAG completa ni prueba con lector de pantalla.

## Alcance de distribución

El diseño se verifica antes de limpiar el artefacto PyInstaller anterior y construir onedir.
Mantener datos reales fuera del paquete y la primera instalación vacía. No cambiar políticas
Windows para abrir el ejecutable. La aceptación de Smart App Control se comprueba por
resultado y eventos, sin afirmar que onedir elimina el bloqueo.
