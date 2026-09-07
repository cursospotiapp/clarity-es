# Validación de la adaptación 0.5.0

Fecha: 7 de septiembre de 2026. Entorno local: Windows, Python 3.11, skills 1.5.23.
Cambio 0.3.0 → 0.4.0: español de España por defecto; otra variante solo si se pide expresamente.
Cambio 0.4.0 → 0.5.0: corrección de defectos del diagnóstico contra corpus reales y regla
del gerundio conforme a la norma académica.

## Contraste con corpus reales (0.5.0)

Se pasó `prose_stats.py` por dos corpus humanos y uno de modelo. Los humanos son textos
publicados ajenos al proyecto: unas 10 800 palabras del *Quijote* (dominio público, Project
Gutenberg) y unas 9 400 de un artículo extenso de Wikipedia en español. El de modelo es un
borrador sintético con las fórmulas habituales, escrito para esta prueba.

| Corpus | `body_sentence_cv` | Matiz./100 | Intens./100 | Anclajes/100 | Aperturas con conector | Gerundios | Actores abstractos |
|---|---|---|---|---|---|---|---|
| Quijote (humano) | 0,742 | 0,41 | 0,02 | 2,54 | 0,004 | 0 | 0 |
| Wikipedia (humano) | 0,810 | 0,28 | 0,13 | 13,66 | 0,075 | 0 | 0 |
| Borrador de modelo | 0,290 | 1,04 | 2,77 | 0,00 | 0,125 | 4 | 2 |

Los detectores de gerundio y de actor abstracto no dieron ningún falso positivo en las
20 000 palabras humanas. La separación entre filas es la esperada, pero sigue siendo
descriptiva: no hay puntuación global ni umbral de aprobado, por diseño del original.

## Defectos encontrados y corregidos en 0.5.0

1. **«clave» sustantivo contado como intensificador.** `samples/guia.after.md` —la versión
   mejorada de una guía para rotar una clave de API— puntuaba 10,81 intensificadores/100
   frente a 9,84 de la versión sin editar: la mejora empeoraba la medida. Ahora «clave» solo
   cuenta en uso adjetivo («papel clave», «es clave»); con determinante o preposición delante
   («la clave», «referencia de claves») es el sustantivo y no cuenta. La guía pasa de 3,28 a 0,00.
2. **Matizadores frecuentes ausentes.** «a menudo», «al parecer», «en gran medida»,
   «en ocasiones», «prácticamente», «en principio», «más bien» y «puede/pueden» no se
   detectaban, pese a que sus equivalentes ingleses sí están en el original.
3. **Falsos positivos de matizador.** «algo», «bastante» y «al menos» contaban siempre,
   incluidos los usos cuantificadores («al menos 3000 personas»). Retirados o acotados.
4. **Aperturas con gerundio incompletas.** De 13 formas se pasa a 41 más las construcciones
   absolutas. Antes se escapaban «analizando», «basándose», «sabiendo», «comenzando»,
   «volviendo», «centrándonos», «habiendo», «dado» y «dicho esto». Se excluyen «dado que»
   (causal corriente) y las preposiciones «ante» y «frente a», que no son participios.
5. **Actores abstractos sin concordancia.** El patrón cubría seis verbos y no concordaba en
   número. Ahora hay dos alternativas, singular y plural, con los verbos del original.
6. **Conectores y cierres incompletos.** Faltaban «en última instancia», «por último»,
   «así pues», «por ello», «de este modo», «es más», «por su parte» y «dicho esto».
7. **Rodeos de la cópula.** Añadidos «supone un/una», «ofrece un/una», «se convierte en» y
   «presume de», equivalentes de `offers a`, `becomes` y `boasts` del original.
8. **Léxico de modelo.** Incorporados marcadores documentados en español —«profundizar»,
   «panorama», «cautivar», «punto de inflexión», «poner de relieve», «un sinfín de»— y las
   coletillas de asistente «avísame si», «te gustaría que», «aquí tienes».
9. **Siglas con punto interior.** «Trabaja en la U.E. desde 2020» se partía en dos frases y
   falseaba el ritmo. Corregido.
10. **Saltos de línea que ocultaban patrones.** `TRIAD` y `PARTICIPIAL` exigían espacio o
    tabulador entre elementos, así que una enumeración ajustada a 90 columnas —es decir,
    casi cualquier Markdown— dejaba de detectarse. Ahora admiten un salto de línea suelto,
    pero no una línea en blanco: la enumeración no cruza párrafos.
11. **La regla central no era verificable.** La «Comprobación final» de `SKILL.md` exige
    coherencia dialectal y tildes imperativas correctas, y no había forma de comprobarlo.
    Nuevos `dialect_mix` y `unaccented_imperatives`. El segundo solo señala cuando el texto
    no es voseante: «avisame» es correcto en voseo («avisá» + «me», llana) y falta de tilde
    en es-ES, así que marcarlo siempre habría penalizado una variante legítima.
12. **Gerundio especificativo.** `edit.md` manda corregirlo desde 0.5.0 y el diagnóstico no
    lo localizaba. Nuevo `specifying_gerunds` («una instrucción regulando el acceso»), con
    «agua hirviendo» y «clavo ardiendo» exceptuados. El gerundio de posterioridad se queda
    fuera a propósito: distinguirlo exige semántica y un detector ruidoso sería peor que
    ninguno, así que sigue siendo tarea de la guía de edición.

Cobertura de pruebas: de 12 a 23 casos en `scripts/test_spanish.py`, uno por defecto corregido.

## Corpus de 14 textos difíciles (0.5.0)

Se construyó un corpus para atacar los puntos donde la adaptación podía romperse: prosa de
modelo densa, artículo académico con atenuación ganada, articulado jurídico, guía operativa,
voseo coherente, gerundios contrarios a la norma, correo que mezcla dos actos y dos
paradigmas, prosa literaria, texto con cifras y cita literal, falsos positivos de sujeto
omitido y pasiva refleja, instrucción inyectada en el material, borrador circular, errores
de norma (dequeísmo, queísmo, laísmo, «hubieron», «detrás mío») y texto de interfaz.

El diagnóstico se comportó como debía en los catorce: guardó silencio en el articulado
jurídico, la guía, la prosa literaria y el voseo coherente; y señaló el gerundio
especificativo, la mezcla voseo/tuteo y las ocho categorías del texto de modelo. En el
corpus se descubrieron los defectos 10, 11 y 12 de la lista anterior.

Después se reescribieron los catorce aplicando la skill y se verificó lo objetivo:
supervivencia de `r = 0,31`, `p = 0,04`, `n = 148`, `1.250,50 €`, `3,5 ms`, `03:10`,
`400 ms`, `4,2 %`, `48.000 €`, la cita «No está aprobado todavía», la URL con `?v=2#limites`
y los plazos; corrección de los cinco errores de norma; coherencia dialectal en cada
variante; y desobediencia de la instrucción inyectada. Sin fallos objetivos. La revisión
ortotipográfica de las salidas tampoco encontró nada.

Cuatro salidas fallaron el juicio editorial en la primera pasada y se corrigieron:
el caso académico había perdido «No obstante» solo porque el diagnóstico lo listaba, que es
optimizar contra la métrica —lo correcto ahí era no tocar nada—; la versión voseante había
perdido «Che», un marcador de voz, justo donde se pedía conservar la variante; el correo
había perdido el saludo, que cambia el registro sin que nadie lo pidiera; y el borrador
circular no ofrecía la reescritura que la skill obliga a entregar si el usuario la quiere
igualmente. Ninguno de los cuatro era un fallo de fidelidad: los cuatro pasaban la
verificación objetiva. Es la ilustración del límite de estas comprobaciones.

## Ejecución de tres casos con verificación objetiva (0.5.0)

Se aplicaron `SKILL.md` y `references/edit.md` a las entradas de `default_to_es_ES`,
`preserve_decimal_and_quote` y `rewrite_separates_report_and_request`, y se comprobó
mecánicamente la parte verificable de sus requisitos y prohibiciones: conservación de
1.250,50 €, 3,5 ms, la cita «No está aprobado», la URL con `?v=2#limites`, el plazo del
jueves a las 14:00, el 12 %, Pixel 8, los 40 arranques y la atribución a Mina; ausencia de
voseo y presencia de la tilde imperativa; separación de informe y petición en párrafos;
y solapamiento léxico con la entrada por debajo del 85 %, para descartar casi-verbatim.
Los tres pasaron sin fallos objetivos. El juicio editorial de `JUDGE.md` sigue requiriendo
lectura humana o de modelo: esto solo descarta la deriva factual y dialectal.

En el tercer caso, el diagnóstico se movió en la dirección coherente con la reescritura:
matizadores 5,08 → 2,13 por 100 palabras (doble cobertura resuelta a una), intensificadores
1,69 → 0,00, anclajes 10,17 → 12,77 y desaparición tanto de la apertura convencional como
de la coocurrencia matizador-intensificador en la misma frase.

## Comprobaciones ejecutadas

- `quick_validate.py`: frontmatter válido.
- `python scripts/validate_package.py`: archivos, rutas heredadas, presupuesto de instrucciones
  y estructura de 18 casos correctos. No ejecuta los casos con un modelo.
- `python -m unittest discover -s scripts -p "test_*.py"`: 23 pruebas superadas.
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
> un 12 % más rápido. No probamos dispositivos anteriores. Mina cree que el cambio de caché
> explica la mayor parte de la mejora.
>
> Si encuentras algún error, avísame antes del jueves a las 14:00 y lo revisamos juntos.

Por qué es mejor: quita la muletilla, reduce la triple atenuación a dos capas sin reforzar
(«sugiere… en torno a»), agrupa muestra y dispositivo junto a la prueba, explicita el límite,
separa la petición y normaliza a es-ES con tildes correctas. No añade dispositivos, fechas ni
personas y conserva dos términos del original que parecen inocuos y no lo son: «dispositivos»,
no «modelos», porque cambiarlo alteraría el alcance del límite declarado; y «Mina cree que»,
no «Mina atribuye», porque la salvaguarda 1 distingue creencia de asignación causal. Con
petición expresa de voseo, la misma reescritura conservaría «Si encontrás… avisame» de
forma coherente.

## Alcance de la evidencia

Se verificó la instalación destinada a los tres agentes. No se ejecutó una evaluación
editorial completa dentro de OpenCode, Claude Code y Codex por separado. Los 18 casos y
el protocolo `JUDGE.md` permiten hacer esa comparación; no se afirma equivalencia empírica
del 100 % ni una mejora cuantificada frente al original.
