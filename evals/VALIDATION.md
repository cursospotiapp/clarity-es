# Validación de la adaptación 0.4.0

Fecha: 7 de septiembre de 2026. Entorno local: Windows, Python 3.11, skills 1.5.23.
Cambio 0.3.0 → 0.4.0: español de España por defecto; otra variante solo si se pide expresamente.

## Comprobaciones ejecutadas

- `quick_validate.py`: frontmatter válido.
- `python scripts/validate_package.py`: archivos, rutas heredadas, presupuesto de instrucciones
  y estructura de 18 casos correctos. No ejecuta los casos con un modelo.
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

**Salida observada (0.3.0):**

> Nuestra prueba interna sugiere que el arranque podría ser aproximadamente un 12 % más rápido
> en Pixel 8. La muestra fue de 40 arranques en frío; no probamos dispositivos anteriores.
> Mina cree que el cambio de caché explica la mayor parte de la mejora.
>
> Si encontrás un error, avisame antes del jueves a las 14:00 y lo revisamos juntos.

Conservó cifras, alcance, incertidumbre, atribución y plazo; entregó solo la reescritura.
Los datos de este ejercicio son ficticios.

### Reevaluación: por qué esa salida era insuficiente

1. **Intervención casi nula.** Solo quitó «Es importante destacar» y cambió una coma por
   punto y coma. Mantuvo la doble cobertura «sugiere… podría ser aproximadamente», dejó el
   respaldo (40 arranques) desordenado y no resolvió el problema principal. Según `JUDGE.md`
   vigente, un casi-verbatim es fallo por intervención insuficiente, aunque conserve los hechos.
2. **Dialecto.** La petición pedía voseo y la skill 0.3.0 decía «no fuerza español de un país»,
   así que conservar «encontrás/avisame» era obedecer. Matiz: «Si encontrás, avisame» no es
   agramatical en voseo rioplatense coherente; es incorrecto como español de España. Desde 0.4.0
   la regla es: es-ES por defecto («Si encuentras, avísame», con tilde), y el voseo solo se
   conserva si se pide expresamente, sin mezclar paradigmas.
3. **Actos mezclados.** Informe técnico y petición con plazo iban en el mismo bloque. Deben ir
   en párrafos distintos, con la petición al frente de su párrafo.

**Salida esperada con la política 0.4.0 (sin petición de voseo, solo el texto):**

> Nuestra prueba interna (40 arranques en frío en Pixel 8) sugiere un arranque en torno a
> un 12 % más rápido. No probamos modelos anteriores. Mina atribuye la mayor parte de la
> mejora al cambio de caché.
>
> Si encuentras algún error, avísame antes del jueves a las 14:00 y lo revisamos juntos.

Por qué es mejor: quita la muletilla, reduce la triple atenuación a una sin reforzar
(«sugiere… en torno a»), agrupa muestra y dispositivo junto a la prueba, explicita el límite,
mantiene la causa atribuida a Mina, separa la petición y normaliza a es-ES con tildes
correctas. No añade dispositivos, fechas ni personas. Con petición expresa de voseo, la misma
reescritura conservaría «Si encontrás… avisame» de forma coherente.

## Alcance de la evidencia

Se verificó la instalación destinada a los tres agentes. No se ejecutó una evaluación
editorial completa dentro de OpenCode, Claude Code y Codex por separado. Los 18 casos y
el protocolo `JUDGE.md` permiten hacer esa comparación; no se afirma equivalencia empírica
del 100 % ni una mejora cuantificada frente al original.
