<div align="center">

# **Clarity en español**

### *Una skill para reescribir textos con claridad, precisión y voz propia*

[![Agent Skill](https://img.shields.io/badge/Agent_Skill-clarity-6BA539?style=flat-square)](SKILL.md)
[![Español](https://img.shields.io/badge/Idioma-Espa%C3%B1ol-E9B44C?style=flat-square)](#adaptación)
[![Agentes](https://img.shields.io/badge/Agentes-OpenCode%20%C2%B7%20Claude%20Code%20%C2%B7%20Codex-000000?style=flat-square)](#instalar)
[![Tests](https://img.shields.io/github/actions/workflow/status/cursospotiapp/clarity-es/validate.yml?branch=main&style=flat-square&label=Tests&logo=githubactions&logoColor=white)](https://github.com/cursospotiapp/clarity-es/actions/workflows/validate.yml)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-blue?style=flat-square)](LICENSE)

</div>

---

Reescribe textos y documentos en español con precisión, claridad y voz propia. Conserva
hechos, cifras, matices y estilo del autor; pregunta o señala las lagunas en vez de inventar.

Adaptación de [Clarity, de Addy Osmani](https://github.com/addyosmani/clarity). Contiene la
skill y herramientas de validación, sin interfaz web, servidor ni compilación.

## Instalar

Con Node.js y el instalador [skills](https://github.com/vercel-labs/skills):

```bash
npx skills add cursospotiapp/clarity-es
```

O con pnpm:

```bash
pnpm dlx skills add cursospotiapp/clarity-es
```

Elige agente y alcance en el instalador. Para instalar globalmente en los tres agentes:

```bash
npx skills add cursospotiapp/clarity-es --skill clarity -g -a opencode claude-code codex
```

El repositorio se llama `clarity-es`; **la skill se llama `clarity`**. Si ya tienes la original
en el mismo alcance, ambas usan ese nombre: elige cuál conservar o usa proyectos distintos.
Reinicia la sesión del agente si no detecta la nueva instalación.

Desde el clon local en Windows:

```powershell
npx skills add C:\Proyectos\clarity-es --skill clarity -a opencode claude-code codex
```

No necesitas publicar en npm: `skills` obtiene el contenido de GitHub. Python 3 solo se
necesita para diagnóstico y pruebas, no para reescribir.

## Usar

Pega un texto o indica una ruta accesible:

```text
Reescribe este texto con clarity: [tu texto]
Reescribe el documento informe.md con clarity, manteniendo cifras y enlaces.
Revisa este documento con clarity sin modificarlo.
Ayúdame a escribir con clarity sobre por qué fallan nuestras reuniones de diseño.
```

En Codex puedes invocarla como `$clarity`. Si el agente expone skills como comandos, puedes
usar `/clarity reescribir borrador.md`. La sintaxis de comandos depende del agente; la petición
natural no exige comandos adicionales. OpenCode puede cargarla con su herramienta de skills.

| Modo | Función | Alias originales |
|---|---|---|
| Entrevista | Recoge lenguaje, ejemplos y criterio antes de redactar | `interview`, `write`, `draft`, `new` |
| Reescritura | Mejora el borrador conservando significado y voz | `rewrite`, `edit`, `fix`, `humanize` |
| Revisión | Diagnostica sin editar archivos | `review`, `critique`, `check` |
| Diagnóstico | Localiza hábitos sin cambiar ni puntuar la prosa | `lint`, `stats` |

Para texto pegado, devuelve la reescritura. Al editar archivos de texto, conserva código,
frontmatter y destinos de enlaces. Para Word o PDF, el agente necesita herramientas de lectura
y escritura del formato: esta skill no incluye un conversor documental.

`commands/` contiene accesos opcionales para Claude Code con nombres originales y españoles.
Copia los que quieras a `~/.claude/commands/`. El instalador no los registra automáticamente
como comandos independientes; no hacen falta para pedir «reescríbelo con clarity».

## Un ejemplo

Un correo que mezcla dos actos —un informe y una petición con plazo— en una sola frase de
58 palabras, y que alterna voseo con tuteo. Los datos son ficticios.

> Hola: el informe trimestral ya está cerrado y los números de octubre subieron un 4,2 %
> frente a septiembre, aunque el dato de Andalucía todavía está pendiente de consolidar y
> podría moverse, y necesito que me confirmes antes del jueves a las 12:00 si validás la
> cifra de Andalucía o preferís que la marquemos como provisional en la presentación del
> comité.

Tras aplicar la skill en modo reescritura:

> Hola:
>
> El informe trimestral ya está cerrado: los números de octubre subieron un 4,2 % frente a
> septiembre. El dato de Andalucía sigue pendiente de consolidar y podría moverse.
>
> Necesito que me confirmes antes del jueves a las 12:00 si validas la cifra de Andalucía o
> si prefieres que la marquemos como provisional en la presentación del comité.

Qué cambia y qué no:

- Informe y petición van en párrafos distintos, con la petición al frente del suyo.
- «validás» y «preferís» pasan a «validas» y «prefieres». Sin petición de variante, es-ES.
- Sobreviven el 4,2 %, octubre, septiembre, Andalucía, el jueves a las 12:00 y el comité.
- «podría moverse» se queda: es la incertidumbre real del dato, no una muletilla.
- El saludo se conserva. Un correo sigue siendo un correo.

### Cuándo no cambia nada

Aquí se separa de pedirle a un modelo «resúmelo y ve al grano». Ante este fragmento de
artículo académico, la respuesta correcta es no editarlo:

> Los resultados sugieren una asociación entre la exposición prolongada y el descenso de
> rendimiento (r = 0,31; p = 0,04; n = 148). No obstante, el diseño transversal impide
> inferir causalidad, y la muestra procede de una única cohorte universitaria.

«Sugieren» es el verbo exacto para r = 0,31, y las tres limitaciones son las que el dato
exige. Cambiarlo por «demuestran» o recortar las cautelas daría un texto más rotundo y menos
cierto. En el corpus de prueba, cuatro de catorce textos pedían esa respuesta: articulado
jurídico, guía operativa, prosa literaria y este.

## Adaptación

- Instrucciones, guías, comandos, ejemplos y casos de evaluación en español.
- Usa español de España por defecto (tuteo, «vosotros» plural, tildes imperativas); conserva voseo u otra variante solo si se pide expresamente, con coherencia completa.
- Respeta sujeto omitido, pasivas útiles, gerundios precisos y conectores justificados.
- Analiza tildes, ñ, Unicode normalizado, comillas angulares, decimales y léxicos españoles.
- Mantiene cuatro modos, fidelidad factual, límites de autoría y claves JSON del original.

No promete resultados en detectores de IA ni resultados idénticos entre modelos. Las pruebas
del paquete no sustituyen la evaluación editorial con agentes reales.

## Diagnóstico opcional

Desde la carpeta de la skill, con archivos UTF-8:

```bash
python scripts/prose_stats.py samples/actualizacion.before.md --markdown
python scripts/prose_stats.py samples/actualizacion.before.md --markdown --json
```

`--markdown` evita depender de la codificación de las tuberías de PowerShell. Admite también
texto plano o `-` para entrada estándar. El informe está en español; las claves JSON siguen
en inglés. Los recuentos son heurísticos: abreviaturas no previstas, listas complejas y nombres
propios pueden dar errores. Los léxicos no cubren todas las flexiones ni dialectos. Una
coincidencia requiere contexto; no convierte un conector o término técnico en defecto.

## Validación

`SKILL.md` elige modo; `references/` contiene las cinco guías; `scripts/` aporta diagnósticos
y pruebas; `samples/` muestra ejemplos; `evals/` define casos y protocolo de comparación.

```bash
python scripts/validate_package.py
python -m unittest discover -s scripts -p "test_*.py"
```

Los casos de `evals/cases.json` requieren ejecución con agente y juicio según `evals/JUDGE.md`.
Validar su estructura no equivale a superar una evaluación editorial.
Las comprobaciones realizadas se documentan en [evals/VALIDATION.md](evals/VALIDATION.md).

## Procedencia y mantenimiento

Basado en `addyosmani/clarity`, commit `e27ceeff60368cf6966b4ea00a5b9b36418ee9a0`
(skill 0.2.1). Esta adaptación usa 0.5.0. Conserva licencia MIT y copyright original en
[LICENSE](LICENSE). No es una traducción oficial del autor.

Los ejemplos son nuevos y didácticos; no se atribuyen a Addy Osmani. Se eliminan web,
despliegue, documentos de diseño e imagen del detector. Los originales siguen en el historial.
Para revisar mejoras futuras sin reincorporar automáticamente la web:

```bash
git fetch upstream
git log --oneline HEAD..upstream/main
git diff e27ceeff60368cf6966b4ea00a5b9b36418ee9a0 upstream/main -- SKILL.md references scripts evals
```

Integra los cambios pertinentes, adapta sus reglas al español y valida.
