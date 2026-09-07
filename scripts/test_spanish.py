"""Pruebas de comportamiento del diagnóstico y del paquete en español."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unicodedata
import unittest

from prose_stats import (
    FALSE_AGENCY, PARTICIPIAL, adjectival_clave, analyze, phrase_hits, report, sentences,
)
from strip_markdown import strip


class SpanishDiagnostics(unittest.TestCase):
    def test_accents_are_whole_words(self):
        self.assertEqual(analyze('Ángela explicó lingüística y programación.')['size']['words'], 5)

    def test_decomposed_unicode_matches_composed(self):
        text = 'Quizá Ángela explicó lingüística. En conclusión, es útil.'
        self.assertEqual(analyze(text), analyze(unicodedata.normalize('NFD', text)))

    def test_decimals_and_spanish_abbreviations(self):
        text = 'La Dra. Núñez midió 3.5 ms y 2,4 MB. ¿Mejoró? ¡Sí!'
        self.assertEqual(sentences(text), ['La Dra. Núñez midió 3.5 ms y 2,4 MB.', '¿Mejoró?', '¡Sí!'])

    def test_paragraphs_and_closing_quotes(self):
        self.assertEqual(sentences('Dijo «ya terminó».\n\nOtra frase sin punto'),
                         ['Dijo «ya terminó».', 'Otra frase sin punto'])

    def test_phrase_matches_whole_words(self):
        self.assertEqual(phrase_hits('reutilizar ecosistemas', ['utilizar', 'ecosistema']), [])
        self.assertEqual(phrase_hits('Cabe\n destacar el resultado.', ['cabe destacar']), ['cabe destacar'])

    def test_spanish_habits_are_located(self):
        stats = analyze('Quizá sea crucial. Sin embargo, no solo reduce errores, sino también costes. En conclusión, espero que te sirva.')
        self.assertGreater(stats['density']['hedge_per_100'], 0)
        self.assertTrue(stats['high_signal_clusters']['hedge_booster_same_sentence'])
        self.assertTrue(stats['high_signal_clusters']['contrastive_pivots'])
        self.assertEqual(len(stats['look_here']['signpost_openers']), 1)
        self.assertIn('en conclusión', stats['look_here']['stock_closers'])
        self.assertIn('espero que te sirva', stats['look_here']['chatbot_residue'])

    def test_spanish_triads_without_oxford_comma(self):
        self.assertTrue(analyze('Revisa certificado, registro y conexión.')['look_here']['triads'])

    def test_spanish_anchors(self):
        # Núñez and a quoted string; initial Ángela is deliberately excluded.
        stats = analyze('Ángela llamó a Núñez y dijo «ya terminó».')
        self.assertGreater(stats['density']['anchors_per_100'], 20)

    def test_empty_text_and_no_quality_score(self):
        stats = analyze('')
        self.assertEqual(stats['size'], {'words': 0, 'sentences': 0, 'paragraphs': 0})
        self.assertNotIn('score', stats)
        self.assertIn('Sin puntuación global', report(stats))

    def test_markdown_keeps_prose_and_discards_code(self):
        result = strip('---\ntitle: hola\n---\n# Acción\n\n[Guía](https://example.com) **útil**.\n\n```py\nprint("secreto")\n```')
        self.assertIn('Guía útil.', result)
        self.assertNotIn('secreto', result)
        self.assertNotIn('https:', result)

    def test_cli_markdown_utf8_bom_and_path_with_spaces(self):
        script = Path(__file__).with_name('prose_stats.py')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'mi borrador.md'
            path.write_text('# Acción\n\nÁngela programó.\n\n```py\nx = 1\n```', encoding='utf-8-sig')
            result = subprocess.run([sys.executable, str(script), str(path), '--markdown', '--json'],
                                    capture_output=True, encoding='utf-8', check=True)
            self.assertEqual(json.loads(result.stdout)['size']['words'], 3)

    def test_cli_rejects_unknown_options(self):
        result = subprocess.run([sys.executable, str(Path(__file__).with_name('prose_stats.py')), '--unknown'],
                                capture_output=True)
        self.assertEqual(result.returncode, 2)

    def test_clave_noun_is_not_a_booster(self):
        # «clave» sustantivo (contraseña) no es intensificador; adjetivo sí lo es.
        for nominal in ['Rota la clave de API.', 'Guarda las claves.',
                        'la referencia de claves', 'Crea una clave nueva.',
                        'Accede con la clave.', 'Un fichero sin clave.']:
            self.assertEqual(adjectival_clave(nominal), [], nominal)
        for adjectival in ['Es clave revisarlo.', 'Un factor clave del retraso.',
                           'La pieza clave es el caché.', 'Son claves para el arranque.']:
            self.assertTrue(adjectival_clave(adjectival), adjectival)

    def test_rewritten_guide_does_not_score_worse(self):
        # Regresión: una guía sobre rotar claves no debe subir en intensificadores
        # al mejorarla. La versión editada quita «es importante… fundamentales».
        before = analyze('Es importante señalar que los siguientes pasos son fundamentales.\n\n'
                         'Crea la clave de sustitución. Revoca la clave anterior.')
        after = analyze('Crea la clave de sustitución. Revoca la clave anterior.')
        self.assertGreater(before['density']['booster_per_100'], 0)
        self.assertEqual(after['density']['booster_per_100'], 0.0)

    def test_common_words_are_not_counted_as_hedges(self):
        # «algo», «bastante» y «al menos» cuantifican; no son matizadores por sí solos.
        for text in ['Algo falló en el despliegue.', 'Bastante gente se quejó.',
                     'Al menos 3000 personas asistieron.']:
            self.assertEqual(analyze(text)['density']['hedge_per_100'], 0.0, text)

    def test_frequent_spanish_hedges_are_found(self):
        for text in ['A menudo falla en frío.', 'Al parecer viene de red.',
                     'En gran medida depende del caché.', 'El cambio puede afectar al arranque.',
                     'En ocasiones se cuelga.', 'Más bien parece un sesgo.']:
            self.assertGreater(analyze(text)['density']['hedge_per_100'], 0.0, text)

    def test_gerund_openers_and_causal_clauses(self):
        for opener in ['Analizando los resultados, vimos un sesgo.',
                       'Basándose en los datos, el equipo actuó.',
                       'Dado el volumen, ampliamos el plazo.',
                       'Dicho esto, conviene revisar.']:
            self.assertTrue(PARTICIPIAL.match(opener), opener)
        for plain in ['Dado que llovía, no salimos.', 'Ante la duda, pregunta.',
                      'Frente a la sede, hay obras.']:
            self.assertIsNone(PARTICIPIAL.match(plain), plain)

    def test_false_agency_agrees_in_number(self):
        for text in ['La tecnología decide quién entra.', 'El proceso impulsa la adopción.',
                     'Los resultados exigen otra lectura.', 'Las cifras hablan solas.']:
            self.assertTrue(FALSE_AGENCY.search(text), text)
        # Sujeto humano explícito: no es actor abstracto.
        self.assertIsNone(FALSE_AGENCY.search('El equipo decide quién entra.'))

    def test_acronyms_with_inner_periods_do_not_split(self):
        self.assertEqual(sentences('Trabaja en la U.E. desde 2020. Ahora no.'),
                         ['Trabaja en la U.E. desde 2020.', 'Ahora no.'])

    def test_line_wrapping_does_not_hide_patterns(self):
        # Un salto de línea de ajuste no debe romper la coincidencia; una línea en blanco sí.
        self.assertTrue(analyze('Los entornos: desarrollo,\npreproducción y producción.')
                        ['look_here']['triads'])
        self.assertFalse(analyze('uno, dos\n\ny tres.')['look_here']['triads'])
        self.assertTrue(PARTICIPIAL.match('Teniendo en cuenta el coste inicial\ndel proyecto, lo aplazamos.'))

    def test_dialect_mix_is_flagged_but_coherent_variants_are_not(self):
        mezcla = analyze('Si encontrás un error, avísame. Tienes tiempo.')['look_here']
        self.assertTrue(mezcla['dialect_mix'])
        for coherente in ['Si encontrás un error, avisame. Tenés tiempo.',
                          'Si encuentras un error, avísame. Tienes tiempo.']:
            self.assertEqual(analyze(coherente)['look_here']['dialect_mix'], [], coherente)

    def test_unaccented_imperative_only_outside_voseo(self):
        # «avisame» es correcto en voseo (avisá + me, llana) y falta de tilde en es-ES.
        voseante = analyze('Si encontrás un error, avisame. Tenés tiempo.')
        self.assertEqual(voseante['look_here']['unaccented_imperatives'], [])
        tuteante = analyze('Si encuentras un error, avisame antes del jueves.')
        self.assertIn('avisame', tuteante['look_here']['unaccented_imperatives'])

    def test_human_prose_stays_below_model_prose(self):
        # Control humano frente a prosa de modelo: la separación debe ser evidente.
        humano = ('Llegamos a las siete y el taller ya estaba abierto. Mina había dejado el '
                  'motor destapado y una nota con tres cifras: 40 arranques, 12 % y un jueves. '
                  'No entendí la última hasta que abrí el registro de caché.')
        modelo = ('En el mundo actual, la automatización desempeña un papel fundamental. Es '
                  'importante destacar que representa un cambio de paradigma crucial. En '
                  'conclusión, espero que esto te ayude.')
        h, m = analyze(humano)['density'], analyze(modelo)['density']
        self.assertGreater(m['booster_per_100'], h['booster_per_100'])
        self.assertGreater(h['anchors_per_100'], m['anchors_per_100'])


if __name__ == '__main__':
    unittest.main()
