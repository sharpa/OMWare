# Module: Operations.exceptions
# Version: 0.1
# Author: Aaron Sharp
# Date: 03/29/2016
# 
# The purpose of this module is to define exceptions
# that are not specific to BioNano objects

class IllegalArgumentException(Exception):
	def __init__(self, name, value):
		message="The argument "+str(name)+" was set to an illegal value: " + str(value)
		super(IllegalArgumentException, self).__init__(message)
		self.name=name
		self.value=value
