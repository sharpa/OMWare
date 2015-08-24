# Module: UnitTests.tAll.py
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/25/2015
# 
# The purpose of this module is to run all of POMM's unit tests
import unittest

def run_suites(test_suites):
	for suite in test_suites:
		unittest.TextTestRunner(verbosity=2).run(suite)

def get_all_test_suites():
	test_suites=[]
	test_suites.extend(get_smoke_test())
	test_suites.extend(get_utils_test_suites())
	test_suites.extend(get_operations_test_suites())
	test_suites.extend(get_bioNanoAssembly_test_suites())
	test_suites.extend(get_bioNanoComparison_test_suites())
	test_suites.extend(get_files_test_suites())
	return test_suites
	
def get_smoke_test():
	import UnitTests.SmokeTest
	test_suites=[]
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.SmokeTest.SmokeTest))
	return test_suites

def get_utils_test_suites():
	import UnitTests.tUtils
	test_suites=[]
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tUtils.tCD))
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tUtils.tResources))
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tUtils.tMacbookProResources))
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tUtils.tFultonResources))
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tUtils.tFultonResourcesLight))
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tUtils.tWorkspace))
	return test_suites

def get_operations_test_suites():
	import UnitTests.tOperations
	test_suites=[]
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tOperations.tStep))
	return test_suites

def get_bioNanoAssembly_test_suites():
	import UnitTests.tBioNanoAssembly
	test_suites=[]
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tBioNanoAssembly.tInput))
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tBioNanoAssembly.tAssembly))
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tBioNanoAssembly.tGroupManifest))
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tBioNanoAssembly.tRefineA))
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tBioNanoAssembly.tRefineB0))
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tBioNanoAssembly.tMerge))
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tBioNanoAssembly.tSummarize))
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tBioNanoAssembly.tGenericAssembly))
	return test_suites

def get_bioNanoComparison_test_suites():
	import UnitTests.tBioNanoComparison
	test_suites=[]
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tBioNanoComparison.tInput))
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tBioNanoComparison.tReferenceAlignment))
	return test_suites

def get_files_test_suites():
	import UnitTests.tFiles
	test_suites=[]
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tFiles.tFile))
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tFiles.tCmapFile))
	test_suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitTests.tFiles.tCmapFile_iter))
	return test_suites

if __name__=="__main__":
	test_suites=get_all_test_suites()
	run_suites(test_suites)
