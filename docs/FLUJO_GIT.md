# Flujo de versionamiento

## Ramas

- `main`: version estable y validada.
- `dev`: integracion de desarrollo activo.

## Reglas operativas

1. Todo trabajo se inicia desde `dev` actualizado.
2. Cada cambio funcional o documental relevante debe incluir una descripcion clara y pruebas aplicables.
3. Se realiza un commit por unidad coherente de trabajo; no se suben secretos, archivos generados ni datos operativos.
4. Al cerrar una fase, se revisa y se integra de `dev` hacia `main` de forma controlada.
5. Si se crean ramas de caracteristica en el futuro, se usara el prefijo `codex/` y se fusionaran primero en `dev`.

## Convencion de commits

Se recomienda Conventional Commits en espanol:

- `docs: documenta estructura inicial`
- `feat(inventory): agrega movimientos de stock`
- `test(components): cubre validacion de referencia`
- `fix(documents): valida extension PDF`
