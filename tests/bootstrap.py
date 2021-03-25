#!/usr/bin/env python

import unittest
import sys
from unit.test_utils import TestUtils
from unit.test_push import TestPush
from unit.test_get_url import TestGetUrl
#from unit.test_upload import TestUpload

def main ():
	# Run the test suites
	util1= unittest.TestLoader().loadTestsFromTestCase(TestUtils)
	util2= unittest.TestLoader().loadTestsFromTestCase(TestPush)
	util3= unittest.TestLoader().loadTestsFromTestCase(TestPush)
	unittest.TestSuite([util1, util2, util3])
	unittest.main()
	
if __name__ == '__main__':
	main()