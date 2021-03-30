import unittest
import sys
import os
import StringIO
import argparse
import unit.test_config as test_config
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from localize.commands import *


class TestPush (unittest.TestCase):

    # def test_push_missing_token (self):
    #     push_path = os.getcwd() + '/unit/test_files/fr.json'
    #     config = {
    #         'api': {
    #             'project': test_config.project,
    #             test_config.environment: True,
    #         },
    #         'format': 'JSON',
    #         'push': {
    #             'sources': [
    #                 { 'file' : push_path },
    #             ]
    #         },
    #         'type': 'phrase',
    #     }

    #     with self.assertRaises(KeyError):
    #         push(config)

    # def test_push_missing_project (self):
    #     push_path = os.getcwd() + '/unit/test_files/fr.json'
    #     config = {
    #         'api': {
    #             'token': test_config.token,
    #             test_config.environment: True,
    #         },
    #         'format': 'JSON',
    #         'push': {
    #             'sources': [
    #                 { 'file' : push_path },
    #             ]
    #         },
    #         'type': 'phrase',
    #     }

    #     with self.assertRaises(KeyError):
    #         push(config)

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
            push(config)
        expected = 'Successfully pushed 0 file(s) to Localize'
        self.assertTrue(expected in SystemExitMessage.exception.args[0])
    
    # def test_push_with_correct_data (self):
    #     push_path = os.getcwd() + '/unit/test_files/fr.json'
    #     config = {
    #         'api': {
    #             'project': test_config.project,
    #             'token': test_config.token,
    #             test_config.environment: True,
    #         },
    #         'format': 'JSON',
    #         'push': {
    #             'sources': [
    #                 { 
    #                     'file' : push_path,
    #                 },
    #             ]
    #         },
    #         'type': 'phrase',
    #     }
                
    #     with self.assertRaises(SystemExit) as SystemExitMessage:
    #         push(config)
    #         print(SystemExitMessage.exception.args[0])
    #         expected = 'Successfully pushed 1 file(s) to Localize'
    #         self.assertTrue(expected in SystemExitMessage.exception.args[0])
        
    def test_push_with_incorrect_data (self):
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
                        'file' : os.getcwd() + '/unit/test_files/es.json',
                    },
                ]
            },
            'type': 'phrase',
        }
        
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput                 
        push(config)
        sys.stdout = sys.__stdout__
        actual = capturedOutput.getvalue()
        print(actual)
        expected = 'Your file incorrectly contains 1 phrase(s) with phraseKeys.'
        self.assertTrue(expected in actual)
