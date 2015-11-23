class VitalParameters:
	def __init__(self, k):
		self.k=k
	def __eq__(self, other):
		if other is None:
			return False
		if self.__class__!=other.__class__:
			return False
		return self.__dict__==other.__dict__
	def __ne__(self, other):
		return not self == other
