import unittest
import sys
import os
from io import StringIO
import unit.test_config as test_config
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from localize.commands import *


class TestPull (unittest.TestCase):
    def test_pull_missing_pull_targets (self):
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'pull': {
            },
            'type': 'phrase',
        }
        with self.assertRaises(SystemExit) as SystemExitMessage:
            pull(config, '')
            expected = 'Could not find any targets to pull. Please make sure your configuration is formed correctly.'
            self.assertTrue(expected in SystemExitMessage.exception.args[0])

    def test_pull_missing_token (self):
        pull_path = os.getcwd() + '/unit/test_files/fr_pull.json'
        config = {
            'api': {
                'project': test_config.project,
                test_config.environment: True,
            },
            'format': 'JSON',
            'pull': {
                'targets': [
                    { 'fr' : pull_path },
                ]
            },
            'type': 'phrase',
        }

        with self.assertRaises(KeyError):
            pull(config, '')
    
    def test_pull_missing_project (self):
        pull_path = os.getcwd() + '/unit/test_files/fr_pull.json'
        config = {
            'api': {
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'push': {
                'targets': [
                    { 'fr' : pull_path },
                ]
            },
            'type': 'phrase',
        }

        with self.assertRaises(KeyError):
            pull(config, '')
    
    def test_pull_correct_data (self):
        pull_path = os.getcwd() + '/unit/test_files/fr_pull.json'
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'pull': {
                'targets': [
                    { 'fr' : pull_path },
                ]
            },
            'type': 'phrase',
        }

        with self.assertRaises(SystemExit) as SystemExitMessage:
            pull(config, '')
            expected = 'Successfully pulled 1 file(s) from Localize'
            self.assertTrue(expected in SystemExitMessage.exception.args[0])

    def test_pull_with_custom_profile_test1 (self):
        pull_path = os.getcwd() + '/unit/test_files/fr_pull.json'
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'pull': {
                'targets': [
                    { 'fr' : pull_path },
                ],
                'my-glossary' : {
                    'targets': [
                        { 'fr' : pull_path },
                    ],
                }

            },
            'type': 'glossary',
        }

        with self.assertRaises(SystemExit) as SystemExitMessage:
            pull(config, 'my-glossary')
            expected = 'Successfully pulled 1 file(s) from Localize'
            self.assertTrue(expected in SystemExitMessage.exception.args[0])

    def test_pull_with_custom_profile_test2 (self):
        pull_path = os.getcwd() + '/unit/test_files/fr_pull.csv'
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'pull': {
                'targets': [
                    { 'fr' : pull_path },
                ],
                'my-phrase' : {
                    'type': 'phrase',
                    'targets': [
                        { 'fr' : pull_path, 'format': 'CSV' },
                    ],
                }

            },
            'type': 'glossary',
        }

        with self.assertRaises(SystemExit) as SystemExitMessage:
            pull(config, 'my-phrase')
            expected = 'Successfully pulled 1 file(s) from Localize'
            self.assertTrue(expected in SystemExitMessage.exception.args[0])

    def test_custom_profile_missing_targets (self):
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'pull': {
                'my-phrase' : {
                    'type': 'phrase',
                }
            },
            'type': 'phrase',
        }
        with self.assertRaises(SystemExit) as SystemExitMessage:
            pull(config, '')
            expected = 'Could not find any targets to pull. Please make sure your configuration is formed correctly.'
            self.assertTrue(expected in SystemExitMessage.exception.args[0])

    def test_pull_incorrect_language_code (self):
        pull_path = os.getcwd() + '/unit/test_files/fr_pull.json'
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'pull': {
                'targets': [
                    { 'ta' : pull_path },
                ]
            },
            'type': 'phrase',
        }

        capturedOutput = StringIO()
        sys.stdout = capturedOutput                 
        pull(config, '')
        sys.stdout = sys.__stdout__
        actual = capturedOutput.getvalue()
        expected = 'Failed to pull ta. This language does not exist in your project'
        self.assertTrue(expected in actual)

    def test_pull_language_validation (self):
        pull_path = os.getcwd() + '/unit/test_files/fr_pull.json'
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'JSON',
            'pull': {
                'targets': [
                    { 'xyz' : pull_path },
                ]
            },
            'type': 'phrase',
        }

        capturedOutput = StringIO()
        sys.stdout = capturedOutput                 
        pull(config, '')
        sys.stdout = sys.__stdout__
        actual = capturedOutput.getvalue()
        expected = 'language code you provided is not found for file'
        self.assertTrue(expected in actual)
    
    def test_pull_unsupported_file_format (self):
        pull_path = os.getcwd() + '/unit/test_files/fr_pull.strings'
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'IOS_STRINGS',
            'pull': {
                'targets': [
                    { 'fr' : pull_path },
                ]
            },
            'type': 'phrase',
        }

        capturedOutput = StringIO()
        sys.stdout = capturedOutput                 
        pull(config, '')
        sys.stdout = sys.__stdout__
        actual = capturedOutput.getvalue()
        expected = 'The format doesn\'t support export for web project'
        self.assertTrue(expected in actual)