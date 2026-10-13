# Validación y regeneración

Fecha local: 12/10/2026, America/Bogota. Herramienta: skill Archify, paquete 3.0.1.
Tipo: architecture. Perfil: showcase. Idioma: español, catálogo es.json de Archify.

Se inspeccionaron entradas, settings, URLs, modelos, servicios de escritura, vistas
de documentos y respaldo. Las referencias del diagrama se verifican contra bytes
Git del commit e55a3f3d2276997673efe33616debfd81b979c7a; no contra una base personal.
Los archivos no versionados .venv_backup e info_project.txt no son fuentes del diagrama.

Resultado del comando finalize: validate, deliver, check y browser-check **pass**,
sin diagnósticos. El recibo compacto contiene SHA256 del candidato y HTML. El gate
browser-check utiliza navegador real, no demuestra por sí solo una revisión visual.

Revisión adicional: visual-check pasó contención, legibilidad, controles, temas y
capturas a 1440×900 y 2048×1320 en claro/oscuro. Se inspeccionaron las imágenes
1440×900 claro y 2048×1320 oscuro: nodos, etiquetas y conexiones legibles, sin
solapamientos observados. No es una certificación completa de accesibilidad.
El recibo automático mantiene visualReview=pending porque no registra el juicio
humano/visual posterior; esta nota distingue ambos resultados.

SHA256 del HTML validado:
`d7151f977ba61a81a5bb08089ccd430ea816f4827210d8449dc3c9a99a0f6745`.

## Cómo regenerar

Instala/descarga la skill desde [tt-a1i/archify](https://github.com/tt-a1i/archify).
No se añadió la herramienta a requirements.txt: solo se necesita para regenerar
diagramas, no para ejecutar el aplicativo. La copia usada aquí reside en
.local/tools/skills/archify y queda fuera del repositorio.

Desde la raíz del proyecto, con Node.js disponible y esa copia de la skill:

```powershell
node .local/tools/skills/archify/bin/archify.mjs finalize architecture arquitectura/candidate.json arquitectura/inventariosapp.html --repo-root . --quality showcase --json
```

Si cambia el código, actualiza meta.repository.revision y las referencias reales,
revisa el esquema y conserva evidencia previa usando --out-dir con una carpeta nueva.
Sigue SKILL.md para reparaciones y comprobaciones del navegador. Los recibos contienen
rutas de la máquina generadora; son evidencia de esa ejecución, no instrucciones
de rutas para otro PC. El HTML y candidate.json son portables.

Estos cambios son documentación. No se reconstruyó el .exe ni se modificó el esquema;
se conservan los resultados previos de 125 pruebas y validación del ejecutable.
