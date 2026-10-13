# Flujo de versionamiento

## Ramas

- `main`: versión estable aprobada; contiene v2.3.1 tras el merge 412a0bc.
- `dev_v2`: desarrollo y correcciones futuras de la línea v2.
- `dev`: rama histórica de la primera versión; no es la rama de trabajo actual.

## Reglas operativas

1. Todo trabajo futuro se inicia desde `dev_v2` actualizado.
2. Cada cambio funcional o documental relevante debe incluir una descripcion clara y pruebas aplicables.
3. Se realiza un commit por unidad coherente; no se suben secretos ni datos operativos.
   Se incluyen artefactos autorizados: ZIP de distribución y arquitectura generada.
4. Tras revisión y autorización del usuario, se integra `dev_v2` hacia `main`.
5. Las ramas de característica futuras usarán el prefijo `codex/` y se fusionarán
   primero en `dev_v2`, salvo instrucción expresa diferente del usuario.

## Convencion de commits

Se recomienda Conventional Commits en espanol:

- `docs: documenta estructura inicial`
- `feat(inventory): agrega movimientos de stock`
- `test(components): cubre validacion de referencia`
- `fix(documents): valida extension PDF`
