import random

class Factor:
	# Receives an input value in a base unit and outputs
	# a division factor which is partly dependent on the
	# size of the input and partly random.
	def getFactor(self, norm_value):
		
		try:
			norm_value_parsed = float(norm_value)
			# TODO insert intelligence that depends on size of input
			# TODO Wahrscheinlichkeitsverteilung s. Lars (kleinere wahrscheinlicher)
			factor = random.randrange(1, 100, 2)
		except Exception:
			raise RuntimeError("Factor calculation failed!")
		
		return factor