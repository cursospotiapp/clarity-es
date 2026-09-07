"""Pruebas de comportamiento del diagnóstico y del paquete en español."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unicodedata
import unittest

from prose_stats import analyze, phrase_hits, report, sentences
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


if __name__ == '__main__':
    unittest.main()
