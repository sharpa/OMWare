# Module: Operations.BioNano.files
# Version: 0.1
# Author: Aaron Sharp
# Date: 03/25/2016
# 
# The purpose of this module is to define errors and exceptions
# that BioNano objects might call

class FileArrangementException(Exception):
	pass
class FileMismatchException(Exception):
	def __init__(self, containing_file, missing_file, mismatched_entity):
		message=str(missing_file)+" is missing entity " + str(mismatched_entity) + ", which is contained in "+str(containing_file)
		super(FileMismatchException, self).__init__(message)
		self.containing_file=containing_file
		self.missing_file=missing_file
		self.mismatched_entity=mismatched_entity

