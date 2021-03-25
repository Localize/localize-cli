import unittest
import StringIO
import sys
import os
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from localize.commands import *

class TestGetUrl (unittest.TestCase):

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