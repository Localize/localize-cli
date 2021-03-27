import unittest
import StringIO
import sys
import os
import argparse
import test_config
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from localize.commands import *

class TestPush (unittest.TestCase):

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
                    { 'file' : push_path },
                ]
            },
            'type': 'phrase',
        }

        with self.assertRaises(SystemExit):
            push(config)

    def test_push_with_wrong_format (self):
        push_path = os.getcwd() + '/unit/test_files/es.json'
        config = {
            'api': {
                'project': test_config.project,
                'token': test_config.token,
                test_config.environment: True,
            },
            'format': 'XML',
            'push': {
                'sources': [
                    { 'file' : push_path },
                ]
            },
            'type': 'phrase',
        }

        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput                 
        push(config)
        sys.stdout = sys.__stdout__
        actual = capturedOutput.getvalue()
        expected = 'File format mismatch for file'
        self.assertTrue(expected in actual)

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
            push(config)

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
            push(config)

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

        with self.assertRaises(SystemExit):
            push(config)