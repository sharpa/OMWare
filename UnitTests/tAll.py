# Module: UnitTests.tAll.py
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/25/2015
# 
# The purpose of this module is to run all of POMM's unit tests
import unittest

def run_suites(suite):
	unittest.TextTestRunner(verbosity=1).run(suite)

def get_all_test_suites():
	suite=unittest.TestSuite()
	suite.addTests(get_smoke_test())
	suite.addTests(get_utils_test_suites())
	suite.addTests(get_operations_test_suites())
	suite.addTests(get_bioNanoAssembly_test_suites())
	suite.addTests(get_bioNanoComparison_test_suites())
	suite.addTests(get_files_test_suites())
	return suite
	
def get_smoke_test():
	import UnitTests.SmokeTest
	return unittest.TestLoader().loadTestsFromModule(UnitTests.SmokeTest)

def get_utils_test_suites():
	import UnitTests.tUtils
	return unittest.TestLoader().loadTestsFromModule(UnitTests.tUtils)

def get_operations_test_suites():
	import UnitTests.tOperations
	return unittest.TestLoader().loadTestsFromModule(UnitTests.tOperations)

def get_bioNanoAssembly_test_suites():
	import UnitTests.tBioNanoAssembly
	return unittest.TestLoader().loadTestsFromModule(UnitTests.tBioNanoAssembly)

def get_bioNanoComparison_test_suites():
	import UnitTests.tBioNanoComparison
	return unittest.TestLoader().loadTestsFromModule(UnitTests.tBioNanoComparison)

def get_files_test_suites():
	import UnitTests.tFiles
	return unittest.TestLoader().loadTestsFromModule(UnitTests.tFiles)

if __name__=="__main__":
	test_suites=get_all_test_suites()
	run_suites(test_suites)
