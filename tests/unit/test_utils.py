import unittest
import StringIO
import sys
import os
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from localize.localize import *
from localize.commands import *

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

	def test_push (self):
		print(os.getcwd())
		push_path = os.getcwd() + '/unit/test_files/fr.json'
		print(push_path)
		data = dict(
			api = dict(
				project = 'LaHtKc8QETpCK',
				token = 'bfdb2a80531475f2111a5b64d695d214',
				dev = 'dev',
			),
			type = 'phrase',
			format = 'json',
			push = dict(
				sources = [dict(file = push_path)]
			),
			pull = dict(
				targets = [dict(language_code = '/full/path/to/your/file_name.extension')]
			)
  		)
		capturedOutput = StringIO.StringIO()
		sys.stdout = capturedOutput                 
		push(data)
		sys.stdout = sys.__stdout__
		actual = capturedOutput.getvalue()
		expected = 'ValidationError: "type" is required for file'
		self.assertTrue(expected in actual)
