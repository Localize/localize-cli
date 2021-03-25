import unittest
import StringIO
import sys
import os
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from localize.localize import *
from localize.commands import *
project = 'LaHtKc8QETpCK'
token = 'bfdb2a80531475f2111a5b64d695d214'
class TestUtils (unittest.TestCase):

	def test_no_command_line_config (self):
		sys.argv = [sys.argv[0], '--config']

		try:
			parse_args()
		except:
			assert True

	def test_wrong_command_line_config (self):
		sys.argv = [sys.argv[0], '--config=filedoesnnotexist.cfg']

		with self.assertRaises(SystemExit):
			args = parse_args()
			configuration = get_configuration(args)

	def test_get_url_production (self):
		config = {
			'api': {
				'project': 'somekey',
				'token': 'sometoken',
			}
		}
		actual = get_url(config)
		expected = ('https://api.localizejs.com/v2.0/projects/somekey/resources')
		self.assertEqual(actual, expected)

	def test_get_url_dev (self):
		config = {
			'api': {
				'project': 'somekey',
				'token': 'sometoken',
				'dev': 'dev',
			}
		}
		actual = get_url(config)
		expected = ('http://localhost:8086/v2.0/projects/somekey/resources')
		self.assertEqual(actual, expected)
	
	def test_push_with_correct_data (self):
		push_path = os.getcwd() + '/unit/test_files/fr.json'
		config = {
			'api': {
				'project': project,
				'token': token,
				'dev': 'dev',
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
		push_path = os.getcwd() + '/unit/test_files/fr.json'
		config = {
			'api': {
				'project': project,
				'token': token,
				'dev': 'dev',
			},
			'format': 'CSV',
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
				'project': project,
				'dev': 'dev',
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
				'token': token,
				'dev': 'dev',
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
				'project': project,
				'token': token,
				'dev': 'dev',
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