import unittest
import sys
import os
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from localize.commands import *

class TestLanguageFormat (unittest.TestCase):
    def test_correct_language_format (self):
        actual = check_and_return_lang_format('/unit/fr.json', 'push')
        expected = 'fr'
        self.assertEqual(actual, expected)
    
    def test_incorrect_language_format (self):
        actual = check_and_return_lang_format('/unit/fr', 'push')
        expected = 'Wrong filename for'
        self.assertTrue(expected in actual)