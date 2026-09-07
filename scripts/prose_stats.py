#!/usr/bin/env python3
"""Localiza hábitos de prosa española; no puntúa calidad ni detecta autoría.

python scripts/prose_stats.py borrador.md --markdown [--json]
python scripts/strip_markdown.py borrador.md | python scripts/prose_stats.py -

Heurísticas, no análisis gramatical: abreviaturas no previstas, nombres propios y
enumeraciones complejas pueden dar falsos positivos. Las claves JSON se conservan
en inglés para mantener compatibilidad con las herramientas del original.
"""
import argparse
import json
import re
import statistics
import sys
import unicodedata

from strip_markdown import strip


# Léxicos de búsqueda, no listas de prohibiciones. Revisar siempre el contexto.
HEDGES = set('quizá quizás acaso posiblemente probablemente generalmente normalmente '
             'habitualmente frecuentemente aproximadamente aparentemente presuntamente '
             'relativamente parcialmente podría podrían parece parecen sugiere sugieren '
             'suele suelen casi algo bastante incierto incierta'.split())
HEDGE_PHRASES = ['tal vez', 'puede que', 'es posible', 'en parte', 'en general',
                'más o menos', 'creo que', 'a mi juicio', 'a veces', 'por lo general',
                'hasta cierto punto', 'en la práctica', 'al menos', 'tiende a']
BOOSTERS = set('crucial cruciales esencial esenciales vital vitales clave claves '
               'significativo significativa significativamente robusto robusta poderoso '
               'poderosa notable notablemente crítico crítica profundo profunda '
               'fundamental fundamentales imprescindible importante sustancial '
               'transformador transformadora revolucionario revolucionaria invaluable'.split())
SIGNPOSTS = ['además', 'asimismo', 'también', 'por tanto', 'por consiguiente',
             'en consecuencia', 'sin embargo', 'no obstante', 'en cambio',
             'por el contrario', 'de hecho', 'mientras tanto', 'igualmente']
CLOSERS = ['en conclusión', 'en resumen', 'para resumir', 'en definitiva',
           'en pocas palabras', 'a fin de cuentas', 'al fin y al cabo', 'mirando al futuro']
OPENER_PHRASES = ['en el mundo actual', 'en la era digital', 'cuando se trata de',
                  'en esencia', 'cabe destacar', 'es importante señalar',
                  'es importante destacar', 'en un mundo donde', 'la realidad es',
                  'adentrémonos', 'sin más preámbulos', 'la verdad incómoda']
LEXIS = ['sinergias', 'paradigma', 'ecosistema', 'poner en valor', 'hoja de ruta',
         'en constante evolución', 'desempeña un papel crucial',
         'desempeña un papel fundamental', 'arrojar luz', 'piedra angular',
         'multifacético', 'multifacética', 'revolucionario', 'revolucionaria',
         'marca un antes y un después', 'potenciar', 'fomentar', 'utilizar']
CONTRASTIVE = [re.compile(p, re.I) for p in [
    r'\ben lugar de\b', r'\bno necesariamente\b', r'\ba diferencia de\b',
    r'\bno (?:solo|sólo|solamente|únicamente)\b[^.?!]{0,80}\bsino(?: también)?\b',
    r'\bno es\b[^.?!]{0,60}[,;:]\s*(?:sino(?: que)? )?es\b',
    r'\bno se trata de\b[^.?!]{0,80}\bsino\b',
]]
COPULA = re.compile(r'\b(?:sirve como|se erige en|representa un|representa una|'
                    r'marca un|se presenta como|constituye un|constituye una)\b', re.I)
FALSE_AGENCY = re.compile(
    r'\b(?:(?:la (?:decisión|cultura|conversación|industria|tecnología|arquitectura)|'
    r'el (?:mercado|proceso))\s+(?:decide|quiere|exige|habla|escucha|premia)|'
    r'los datos\s+(?:hablan|deciden|exigen|quieren))\b', re.I)
PARTICIPIAL = re.compile(
    r'^\s*(?:construyendo|partiendo|considerando|aprovechando|combinando|reflejando|'
    r'destacando|subrayando|usando|añadiendo|reconociendo|entendiendo|teniendo en cuenta)'
    r'\b[^,\n]{2,60},', re.I)
LETTER = r'[^\W\d_]'
WORD_RE = re.compile(LETTER + r"+(?:['’\-]" + LETTER + r'+)*')
TRIAD = re.compile(
    r'\b(' + LETTER + r'+(?:[ \t]+' + LETTER + r'+){0,2}),[ \t]+'
    r'(' + LETTER + r'+(?:[ \t]+' + LETTER + r'+){0,2}),?[ \t]+'
    r'(?:y|e|o|u)[ \t]+(' + LETTER + r'+(?:[ \t]+' + LETTER + r'+){0,2})\b', re.I)
CHATBOT = ['espero que te sirva', 'espero que esto te ayude', 'si necesitas algo más',
           'si tienes alguna pregunta', 'gran pregunta', 'tienes toda la razón',
           'como modelo de lenguaje', 'según mi última actualización']
DASH_RE = re.compile(r'—|–|(?<=\s)--(?=\s)|(?<=\s)-(?=\s)')
NUM_RE = re.compile(r'\b\d+(?:[.,]\d+)*\b')
QUOTE_RE = re.compile(r'"[^"\n]{4,}"|“[^”\n]{4,}”|«[^»\n]{4,}»')
COMMON_CAPS = set('El La Los Las Un Una Unos Unas Yo Tú Vos Usted Ustedes Nosotros '
                  'Nosotras Vosotros Vosotras Él Ella Ellos Ellas Esto Eso Pero Y O '
                  'Si Cuando Mientras Porque Aunque En Por Para Con Sin No Sí Qué '
                  'Quién Cómo Dónde Después Antes Entonces Ahora'.split())
BODY_MIN_WORDS = 8
ABBREVIATION = re.compile(r'\b(?:sr|sra|srta|dr|dra|prof|profa|ud|uds|pág|págs|'
                          r'art|arts|núm|aprox)\.$', re.I)


def sentences(text):
    """Segmentación heurística con decimales, títulos comunes y signos españoles."""
    text = unicodedata.normalize('NFC', text)
    result = []
    for paragraph in paragraphs(text):
        start = 0
        for match in re.finditer(r'[.!?]+[\"\'»”\)\]]*', paragraph):
            pos, end = match.span()
            if match.group() == '.':
                if pos and end < len(paragraph) and paragraph[pos-1].isdigit() and paragraph[end].isdigit():
                    continue
                if end < len(paragraph) and ABBREVIATION.search(paragraph[start:end]):
                    continue
            # No separar dominios ni iniciales pegadas a otra palabra.
            if end < len(paragraph) and not paragraph[end].isspace() and paragraph[end] not in '¿¡':
                continue
            chunk = paragraph[start:end].strip()
            if chunk:
                result.append(chunk)
            start = end
        if paragraph[start:].strip():
            result.append(paragraph[start:].strip())
    return result


def paragraphs(text):
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]


def cv(values):
    vals = [v for v in values if v > 0]
    return statistics.pstdev(vals) / statistics.mean(vals) if len(vals) >= 2 else 0.0


def phrase_pattern(phrase):
    return re.compile(r'(?<!\w)' + r'\s+'.join(map(re.escape, phrase.split())) + r'(?!\w)', re.I)


def phrase_hits(text, phrases):
    return sorted({p for p in phrases if phrase_pattern(p).search(text)})


def regex_hits(text, regexes):
    return [m.group().strip() for rx in regexes for m in rx.finditer(text)]


def count_anchors(text, sents):
    """Cifras, citas y posibles nombres propios; no demuestra respaldo factual."""
    anchors = len(NUM_RE.findall(text)) + len(QUOTE_RE.findall(text))
    for sentence in sents:
        for token in WORD_RE.findall(sentence)[1:]:
            if token in COMMON_CAPS or len(token) < 2:
                continue
            if token[0].isupper():
                anchors += 1
    return anchors


def analyze(text):
    text = unicodedata.normalize('NFC', text).lstrip('\ufeff')
    sents, paras = sentences(text), paragraphs(text)
    words = WORD_RE.findall(text)
    n_words = len(words) or 1
    sent_lens = [len(WORD_RE.findall(s)) for s in sents]
    body_lens = [n for n in sent_lens if n >= BODY_MIN_WORDS]
    short_lens = [n for n in sent_lens if n < BODY_MIN_WORDS]
    lowered = [w.lower() for w in words]
    n_hedge = sum(w in HEDGES for w in lowered)
    n_hedge += sum(len(phrase_pattern(p).findall(text)) for p in HEDGE_PHRASES)
    n_boost = sum(w in BOOSTERS for w in lowered)
    co_occur, signposts, participials = [], [], []
    for s in sents:
        low = {w.lower() for w in WORD_RE.findall(s)}
        if (low & HEDGES or phrase_hits(s, HEDGE_PHRASES)) and low & BOOSTERS:
            co_occur.append(s[:110])
        if any(phrase_pattern(p).match(s.lstrip('¿¡«“"')) for p in SIGNPOSTS):
            signposts.append(s[:90])
        if PARTICIPIAL.match(s):
            participials.append(s[:90])
    return {
        'size': {'words': len(words), 'sentences': len(sents), 'paragraphs': len(paras)},
        'cadence': {
            'body_sentence_cv': round(cv(body_lens), 3),
            'all_sentence_cv': round(cv(sent_lens), 3),
            'cadence_masking': round(len(short_lens) / len(sents), 3) if sents else 0.0,
            'paragraph_word_cv': round(cv([len(WORD_RE.findall(p)) for p in paras]), 3),
            'mean_body_sentence_words': round(statistics.mean(body_lens), 1) if body_lens else 0.0,
        },
        'density': {
            'hedge_booster_per_100': round((n_hedge + n_boost) / n_words * 100, 2),
            'hedge_per_100': round(n_hedge / n_words * 100, 2),
            'booster_per_100': round(n_boost / n_words * 100, 2),
            'anchors_per_100': round(count_anchors(text, sents) / n_words * 100, 2),
            'signpost_opener_share': round(len(signposts) / len(sents), 3) if sents else 0.0,
        },
        'high_signal_clusters': {
            'hedge_booster_same_sentence': co_occur,
            'participial_openers': participials,
            'contrastive_pivots': regex_hits(text, CONTRASTIVE),
        },
        'look_here': {
            'triads': [' / '.join(m) for m in TRIAD.findall(text)][:25],
            'copula_displacement': regex_hits(text, [COPULA]),
            'false_agency': regex_hits(text, [FALSE_AGENCY]),
            'signpost_openers': signposts[:25],
            'dash_count': len(DASH_RE.findall(text)),
            'multi_dash_sentences': [s[:110] for s in sents if len(DASH_RE.findall(s)) >= 2],
            'overloaded_sentences': [f'({n} palabras) {s[:96]}' for s, n in
                                     sorted(zip(sents, sent_lens), key=lambda pair: -pair[1]) if n > 40],
            'stock_openers': phrase_hits(text, OPENER_PHRASES),
            'stock_closers': phrase_hits(text, CLOSERS),
            'model_lexis': phrase_hits(text, LEXIS),
            'chatbot_residue': phrase_hits(text, CHATBOT),
        },
    }


LABELS = {
    'body_sentence_cv': 'Variación de longitud de frases de 8 palabras o más',
    'cadence_masking': 'Proporción de frases de menos de 8 palabras',
    'hedge_per_100': 'Matizadores por cada 100 palabras',
    'booster_per_100': 'Intensificadores por cada 100 palabras',
    'anchors_per_100': 'Posibles anclajes concretos por cada 100 palabras',
    'signpost_opener_share': 'Proporción de aperturas con conectores',
    'hedge_booster_same_sentence': 'Matizador e intensificador en una frase',
    'participial_openers': 'Aperturas con gerundio',
    'contrastive_pivots': 'Giros de contraste',
    'triads': 'Enumeraciones de tres elementos',
    'copula_displacement': 'Posibles rodeos de la cópula',
    'false_agency': 'Posibles actores abstractos',
    'signpost_openers': 'Aperturas con conectores',
    'dash_count': 'Rayas y guiones separados',
    'multi_dash_sentences': 'Frases con varias rayas',
    'overloaded_sentences': 'Frases de más de 40 palabras',
    'stock_openers': 'Aperturas convencionales',
    'stock_closers': 'Cierres convencionales',
    'model_lexis': 'Léxico que conviene leer en contexto',
    'chatbot_residue': 'Posibles restos de conversación con un asistente',
}


def report(stats):
    s = stats['size']
    lines = [f"{s['words']} palabras, {s['sentences']} frases, {s['paragraphs']} párrafos"]
    if s['words'] < 400:
        lines.append('Nota: con menos de 400 palabras, las medidas de ritmo y densidad son inestables.')
    lines += ['', 'MEDIDAS DESCRIPTIVAS; NO SON OBJETIVOS']
    for section, keys in [('cadence', ['body_sentence_cv', 'cadence_masking']),
                          ('density', ['hedge_per_100', 'booster_per_100', 'anchors_per_100', 'signpost_opener_share'])]:
        for key in keys:
            lines.append(f'  {LABELS[key]}: {stats[section][key]}')
    lines.append('Compara versiones de un mismo texto, no con una norma universal.')
    if stats['cadence']['cadence_masking'] > 0.15:
        lines.append('Más del 15 % de las frases tienen menos de 8 palabras; comprueba si son títulos o listas.')
    for section, heading in [('high_signal_clusters', 'COMBINACIONES: REVISAR EN CONTEXTO'),
                             ('look_here', 'DÓNDE MIRAR: HIPÓTESIS, NO DICTÁMENES')]:
        lines += ['', heading]
        for key, items in stats[section].items():
            if isinstance(items, int):
                lines.append(f'  {LABELS[key]}: {items}')
            elif items:
                lines.append(f'  {LABELS[key]} ({len(items)})')
                lines.extend(f'    {item}' for item in items[:8])
                if len(items) > 8:
                    lines.append(f'    ... y {len(items) - 8} más')
    lines += ['', 'Sin puntuación global: los recuentos localizan pasajes, no califican la prosa.',
              'No demuestran calidad, veracidad ni autoría. Lee el contexto para decidir.']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', help='Archivo UTF-8, o - para la entrada estándar')
    parser.add_argument('--json', action='store_true', help='Salida JSON con claves compatibles')
    parser.add_argument('--markdown', action='store_true', help='Extraer prosa Markdown antes de analizar')
    args = parser.parse_args()
    # UTF-8 también en tuberías y consolas Windows; no depender de la página de códigos.
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    try:
        if args.path == '-':
            text = sys.stdin.read().lstrip('\ufeff')
        else:
            with open(args.path, encoding='utf-8-sig') as fh:
                text = fh.read()
    except (OSError, UnicodeError) as exc:
        parser.exit(1, f'No se pudo leer el texto: {exc}\n')
    stats = analyze(strip(text) if args.markdown else text)
    print(json.dumps(stats, indent=2, ensure_ascii=False) if args.json else report(stats))


if __name__ == '__main__':
    main()
