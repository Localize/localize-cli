#!/usr/bin/env python

import unittest
import sys
from unit.test_utils import TestUtils
#from unit.test_upload import TestUpload

def main ():
	# Run the test suites
	utils= unittest.TestLoader().loadTestsFromTestCase(TestUtils)
	unittest.TestSuite([utils])
	unittest.main()
	
if __name__ == '__main__':
	main()