#!/usr/bin/env python

import unittest
import os
from unit.test_utils import TestUtils
from unit.test_push import TestPush
from unit.test_get_url import TestGetUrl
from unit.test_lang_format import TestLanguageFormat
from unit.test_pull import TestPull

def main ():
	os.chdir(os.path.dirname(__file__))
	# Run the test suites
	util1= unittest.TestLoader().loadTestsFromTestCase(TestUtils)
	util2= unittest.TestLoader().loadTestsFromTestCase(TestPush)
	util3= unittest.TestLoader().loadTestsFromTestCase(TestGetUrl)
	util4= unittest.TestLoader().loadTestsFromTestCase(TestPull)
	util5= unittest.TestLoader().loadTestsFromTestCase(TestLanguageFormat)
	suite = unittest.TestSuite([util1, util2, util3, util4, util5])
	result = unittest.TextTestRunner().run(suite)
	return result.wasSuccessful()
	
if __name__ == '__main__':
	raise SystemExit(not main())
