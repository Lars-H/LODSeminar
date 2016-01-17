import random

# Receives an input value in a base unit and outputs
# a list of division factors which are partly dependent 
# on the size of the input and partly random.
def getFactorsAndRanges(norm_value, logString='FACTOR - '):
	

	try:
		norm_value_parsed = float(norm_value)

		very_small_range = 0.01
		small_range = 0.02
		medium_range = 0.05
		large_range = 0.1
		very_large_range = 0.2

		very_small_factors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		small_factors = [15, 20, 25, 30, 35, 40, 45, 50]
		medium_factors = [60, 70, 80, 90, 100]
		large_factors = [150, 200, 250, 300, 350, 400, 450, 500]
		very_large_factors = [600, 700, 800, 900, 1000]

		random.shuffle(very_small_factors)
		random.shuffle(small_factors)
		random.shuffle(medium_factors)
		random.shuffle(large_factors)
		random.shuffle(very_large_factors)

		factors_and_ranges = []

		factor = very_small_factors.pop()
		factors_and_ranges.append((factor, very_small_range*factor))

		factor = very_small_factors.pop()
		factors_and_ranges.append((factor, very_small_range))

		factor = small_factors.pop()
		factors_and_ranges.append((factor, small_range))

		factor = small_factors.pop()
		factors_and_ranges.append((factor, small_range))

		factor = medium_factors.pop()
		factors_and_ranges.append((factor, medium_range))

		factor = medium_factors.pop()
		factors_and_ranges.append((factor, medium_range))

		factor = large_factors.pop()
		factors_and_ranges.append((factor, large_range))

		factor = large_factors.pop()
		factors_and_ranges.append((factor, large_range))

		factor = very_large_factors.pop()
		factors_and_ranges.append((factor, very_large_range))

		factor = very_large_factors.pop()
		factors_and_ranges.append((factor, very_large_range))

		random.shuffle(factors_and_ranges)

		#print(factors_and_ranges)

		return factors_and_ranges
			
	except Exception:
		raise RuntimeError("Factor calculation failed!")

#getFactorsAndRanges(1000)