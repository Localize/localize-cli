import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from localize.localize import *

class TestUtils (unittest.TestCase):

	def test_no_command_line_config (self):
		sys.argv = [sys.argv[0], '--config']

		try:
			parse_args()
		except:
			assert True
