import unittest
import sys
import os
from io import StringIO
import unit.test_config as test_config
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from localize.commands import *


class TestPush (unittest.TestCase):

    def test_push_missing_token (self):
        push_path = os.getcwd() + '/unit/test_files/fr.json'
        config = {
            'api': {
                'project': test_config.project,
                test_config.environment: True,
            },
            'format': 'JSON',
            'push': {
                'sources': [
                    { 'file' : push_path },
                ]
            },
            'type': 'phrase',
        }

        with self.assertRaises(KeyError):
            push(config, '')

    def test_push_missing_project (self):
        push_path = os.getcwd() + '/unit/test_files/fr.json'
        config = {
            'api': {
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'push': {
                'sources': [
                    { 'file' : push_path },
                ]
            },
            'type': 'phrase',
        }

        with self.assertRaises(KeyError):
            push(config, '')

    def test_push_missing_file (self):
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'push': {
                'sources': [
                ]
            },
            'type': 'phrase',
        }

        with self.assertRaises(SystemExit) as SystemExitMessage:
            push(config, '')
        expected = 'Successfully pushed 0 file(s) to Localize'
        self.assertTrue(expected in SystemExitMessage.exception.args[0])
    
    def test_push_with_correct_data (self):
        push_path = os.getcwd() + '/unit/test_files/fr.json'
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'push': {
                'sources': [
                    { 
                        'file' : push_path,
                    },
                ]
            },
            'type': 'phrase',
        }
                
        with self.assertRaises(SystemExit) as SystemExitMessage:
            push(config, '')
            expected = 'Successfully pushed 1 file(s) to Localize'
            self.assertTrue(expected in SystemExitMessage.exception.args[0])

    def test_push_non_existent_file (self):
        pull_path = os.getcwd() + '/unit/test_files/xyz.csv'
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'push': {
                'sources': [
                    { 'fr' : pull_path },
                ],
                'my-phrase' : {
                    'type': 'phrase',
                    'sources': [
                        { 'file' : pull_path, 'format': 'CSV' },
                    ],
                }

            },
            'type': 'glossary',
        }
        
        with self.assertRaises(SystemExit) as SystemExitMessage:
            push(config, 'my-phrase')
            expected = 'Skipping import of xyz. No target file path in the localize cli config.yml'
            self.assertTrue(expected in SystemExitMessage.exception.args[0])

    def test_push_with_custom_profile_test1 (self):
        push_path = os.getcwd() + '/unit/test_files/fr.json'
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'push': {
                'sources': [
                    { 'file' : push_path },
                ],
                'my-glossary' : {
                    'sources': [
                        { 'file' : push_path },
                    ],
                    'type': 'glossary',
                }

            },
            'type': 'glossary',
        }

        with self.assertRaises(SystemExit) as SystemExitMessage:
            push(config, 'my-glossary')
            expected = 'Successfully pushed 1 file(s) to Localize'
            self.assertTrue(expected in SystemExitMessage.exception.args[0])

    def test_push_with_custom_profile_test2 (self):
        pull_path = os.getcwd() + '/unit/test_files/fr.csv'
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'push': {
                'sources': [
                    { 'fr' : pull_path },
                ],
                'my-phrase' : {
                    'type': 'phrase',
                    'sources': [
                        { 'file' : pull_path, 'format': 'CSV' },
                    ],
                }

            },
            'type': 'glossary',
        }

        with self.assertRaises(SystemExit) as SystemExitMessage:
            push(config, 'my-phrase')
            expected = 'Successfully pushed 1 file(s) to Localize'
            self.assertTrue(expected in SystemExitMessage.exception.args[0])

    def test_push_incorrect_language_code (self):
        pull_path = os.getcwd() + '/unit/test_files/ta.csv'
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'push': {
                'sources': [
                    { 'fr' : pull_path },
                ],
                'my-phrase' : {
                    'type': 'phrase',
                    'sources': [
                        { 'file' : pull_path, 'format': 'CSV' },
                    ],
                }

            },
            'type': 'glossary',
        }

        capturedOutput = StringIO()
        sys.stdout = capturedOutput                 
        push(config, 'my-phrase')
        sys.stdout = sys.__stdout__
        actual = capturedOutput.getvalue()
        expected = 'Target language is not supported by the project for file'
        self.assertTrue(expected in actual)

    def test_push_language_validation (self):
        pull_path = os.getcwd() + '/unit/test_files/wrong_name.csv'
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'push': {
                'sources': [
                    { 'fr' : pull_path },
                ],
                'my-phrase' : {
                    'type': 'phrase',
                    'sources': [
                        { 'file' : pull_path, 'format': 'CSV' },
                    ],
                }

            },
            'type': 'glossary',
        }

        capturedOutput = StringIO()
        sys.stdout = capturedOutput                 
        push(config, 'my-phrase')
        sys.stdout = sys.__stdout__
        actual = capturedOutput.getvalue()
        expected = 'language code you provided is not found for file'
        self.assertTrue(expected in actual)

    def test_push_unsupported_format (self):
        pull_path = os.getcwd() + '/unit/test_files/fr.strings'
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'push': {
                'sources': [
                    { 'fr' : pull_path },
                ],
                'my-phrase' : {
                    'type': 'phrase',
                    'sources': [
                        { 'file' : pull_path, 'format': 'strings' },
                    ],
                }

            },
            'type': 'glossary',
        }

        capturedOutput = StringIO()
        sys.stdout = capturedOutput                 
        push(config, 'my-phrase')
        sys.stdout = sys.__stdout__
        actual = capturedOutput.getvalue()
        expected = 'ValidationError: "format" must be one of'
        self.assertTrue(expected in actual)

