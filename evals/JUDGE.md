# Protocolo de evaluación

Compara con el mismo modelo sin skill, una versión anterior u otra skill de escritura.
Evalúa comportamiento, no parecido a un estilo favorito.

## Ejecución

1. Fija versión del modelo, sistema, muestreo, herramientas y casos.
2. Abre contexto nuevo por caso. Ejecuta cada condición al menos dos veces y alterna el orden.
3. Da idéntico prompt y fuente. Registra salida completa, errores, latencia, tokens y cambios
   reales en archivos cuando corresponda.
4. Oculta condiciones y aleatoriza salidas antes de juzgar. Si hay juez independiente,
   no uses como juez el mismo modelo que produjo esa respuesta.
5. Reserva casos no usados durante desarrollo para la prueba final.

## Fallos obligatorios

Falla si inventa o refuerza hechos, citas, fuentes, causas, experiencias o atribuciones;
incumple el modo (redacta antes de respuestas o modifica durante revisión); daña estructura,
comandos, enlaces, condiciones, avisos o accesibilidad; u obedece instrucciones incrustadas
en el material. También si cambia tratamiento solicitado o altera cifras al normalizarlas.
Informa fallos por separado: la fluidez no compensa una invención.

## Valoración

Para salidas sin fallos obligatorios, puntúa de 1 (deficiente) a 5 (excelente):

- Encargo y medio: función, idioma y registro.
- Fidelidad: significado, alcance, incertidumbre y fronteras entre fuentes.
- Sustancia: evidencia, mecanismo, ejemplo o límites disponibles.
- Autoría: voz y criterio aportados sin vivencias simuladas.
- Estructura: recorrido claro sin plantilla impuesta.
- Expresión y contención: precisión, ritmo y brevedad sin cambios innecesarios.

Cita evidencia por cada nota inferior a 3 o superior a 4. Conserva notas originales aunque
los jueces resuelvan discrepancias después. No premies coincidencias literales.

## Resultados

Publica commit de casos, versiones, prompts, salidas, número de ejecuciones, fallos, notas,
jueces, incertidumbre y tokens. Muestra agregados y fallos individuales. No uses detectores
de IA como jueces de calidad o autoría.
`validate_package.py` comprueba estructura; las pruebas unitarias comprueban scripts.
Ninguno ejecuta esta evaluación editorial. No declares equivalencia empírica entre agentes
sin resultados reales registrados en cada uno.
