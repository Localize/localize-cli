import unittest
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

