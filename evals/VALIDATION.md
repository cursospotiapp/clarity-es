# Validación de la adaptación 0.3.0

Fecha: 7 de septiembre de 2026. Entorno local: Windows, Python 3.11, skills 1.5.23.

## Comprobaciones ejecutadas

- `quick_validate.py`: frontmatter válido.
- `python scripts/validate_package.py`: archivos, rutas heredadas, presupuesto de instrucciones
  y estructura de 16 casos correctos. No ejecuta los casos con un modelo.
- `python -m unittest discover -s scripts -p "test_*.py"`: 12 pruebas superadas.
- `npx skills add C:\Proyectos\clarity-es --list`: descubre una skill, `clarity`.
- Instalación local con `--skill clarity -a opencode claude-code codex --copy -y` en un
  directorio temporal: completada; referencias y scripts presentes.
- `pnpm dlx skills add C:\Proyectos\clarity-es --list`: descubre `clarity`.
- Tras publicar el fork, `npx skills add cursospotiapp/clarity-es --list` y la instalación
  desde GitHub con `--skill clarity -a opencode claude-code codex --copy -y` completadas
  en el mismo directorio temporal.
- Revisión independiente de instrucciones, referencias y scripts: sin defectos materiales.

## Prueba puntual de reescritura

Un agente independiente de esta sesión recibió únicamente la skill, sus referencias y el
encargo siguiente. Es una prueba puntual; no fija parámetros de muestreo ni compara modelos.

**Petición:** «Este texto reescribelo con clarity. Mantén el voseo y devuélveme solo el texto».

**Entrada:**

> Es importante destacar que nuestra prueba interna sugiere que el arranque podría ser
> aproximadamente un 12 % más rápido en Pixel 8. La muestra fue de 40 arranques en frío y no
> probamos dispositivos anteriores. Mina cree que el cambio de caché explica la mayor parte
> de la mejora. Si encontrás un error, avisame antes del jueves a las 14:00 y lo revisamos juntos.

**Salida observada:**

> Nuestra prueba interna sugiere que el arranque podría ser aproximadamente un 12 % más rápido
> en Pixel 8. La muestra fue de 40 arranques en frío; no probamos dispositivos anteriores.
> Mina cree que el cambio de caché explica la mayor parte de la mejora.
>
> Si encontrás un error, avisame antes del jueves a las 14:00 y lo revisamos juntos.

Conservó cifras, alcance, incertidumbre, atribución, voseo y plazo; entregó solo la reescritura.
Los datos de este ejercicio son ficticios.

## Alcance de la evidencia

Se verificó la instalación destinada a los tres agentes. No se ejecutó una evaluación
editorial completa dentro de OpenCode, Claude Code y Codex por separado. Los 16 casos y
el protocolo `JUDGE.md` permiten hacer esa comparación; no se afirma equivalencia empírica
del 100 % ni una mejora cuantificada frente al original.
