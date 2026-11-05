import unittest
import json
import sys
import os
from io import StringIO
from unittest.mock import patch
import unit.test_config as test_config
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from localize.commands import *


class FakeResponse:
    def __init__(self, status_code=200, message=''):
        self.status_code = status_code
        self.text = json.dumps({'meta': {'error': {'message': message}}})


class TestPush (unittest.TestCase):

    def setUp(self):
        self.requests_post = patch('localize.commands.requests.post', side_effect=self.fake_post)
        self.requests_post.start()

    def tearDown(self):
        self.requests_post.stop()

    @staticmethod
    def fake_post(url, headers, verify, data, files):
        language = data['language']
        format = data['format']
        if language == 'ta':
            return FakeResponse(400, 'Target language is not supported by the project')
        if language == 'wrong_name':
            return FakeResponse(400, 'language code you provided is not found')
        if format == 'STRINGS':
            return FakeResponse(400, 'ValidationError: "format" must be one of')
        return FakeResponse()

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

        capturedOutput = StringIO()
        with patch('sys.stdout', capturedOutput):
            push(config, '')
        expected = 'Successfully pushed 0 file(s) to Localize'
        self.assertIn(expected, capturedOutput.getvalue())
    
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
                
        capturedOutput = StringIO()
        with patch('sys.stdout', capturedOutput):
            push(config, '')
        expected = 'Successfully pushed 1 file(s) to Localize'
        self.assertIn(expected, capturedOutput.getvalue())

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
        
        capturedOutput = StringIO()
        with patch('sys.stdout', capturedOutput):
            push(config, 'my-phrase')
        expected = 'Skipping import of xyz. No target file path in the localize cli config.yml'
        self.assertIn(expected, capturedOutput.getvalue())

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

        capturedOutput = StringIO()
        with patch('sys.stdout', capturedOutput):
            push(config, 'my-glossary')
        expected = 'Successfully pushed 1 file(s) to Localize'
        self.assertIn(expected, capturedOutput.getvalue())

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

        capturedOutput = StringIO()
        with patch('sys.stdout', capturedOutput):
            push(config, 'my-phrase')
        expected = 'Successfully pushed 1 file(s) to Localize'
        self.assertIn(expected, capturedOutput.getvalue())

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

