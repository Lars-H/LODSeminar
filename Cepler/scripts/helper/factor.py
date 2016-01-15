import random

# Receives an input value in a base unit and outputs
# a list of division factors which are partly dependent 
# on the size of the input and partly random.
def getFactor(norm_value, logString):
	
	try:
		norm_value_parsed = float(norm_value)
		# TODO insert intelligence that depends on size of input
		# TODO Wahrscheinlichkeitsverteilung s. Lars (kleinere wahrscheinlicher)
		very_small_range = 0.01
		small_range = 0.02
		medium_range = 0.05
		large_range = 0.1
		very_large_range = 0.2

		very_small_factors = random.shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
		small_factors = random.shuffle([15, 20, 25, 30, 35, 40, 45, 50])
		medium_factors = random.shuffle([60, 70, 80, 90, 100])
		large_factors = random.shuffle([150, 200, 250, 300, 350, 400, 450, 500])
		very_large_factors = random.shuffle([600, 700, 800, 900, 1000])

		factor = very_small_factors.pop()
		#TODO Liste von Tupeln oder Dictionaries mit Keys und Tupeln
		print(logString + "Value is divided by factor: " + str(factor))
		return factor
		
	except Exception:
		raise RuntimeError("Factor calculation failed!")