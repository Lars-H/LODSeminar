import random

# Receives an input value in a base unit and outputs
# a list of division factors which are partly dependent 
# on the size of the input and partly random. TODO remove old stuff
def getFactorsAndRanges(norm_value, logString='FACTOR - '):
	

	try:
		norm_value_parsed = float(norm_value)

		# possible values
		# If they shall be extended, add factors to the factors list
		
		factors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 
					150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 
					1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 6000, 7000, 8000, 9000, 10000]


		# Calculate highest possible factor
		max_factor = min(max(factors), max(10, norm_value))


		# Write the feasible factors into a separate list
		possible_factors = []
		
		for x in factors:
			if x <= max_factor:
				possible_factors.append(x)


		# Shuffle possible factors
		random.shuffle(possible_factors)


		# Take the ten first factors out of the shuffled list and return them
		factors_and_ranges = []
		value_range = 0.02

		for i in range(10):

			current_factor = possible_factors.pop()
			if current_factor > 50:
				value_range = 0.1
			else:
				value_range = 0.02
			factors_and_ranges.append((current_factor, value_range))

		#print(factors_and_ranges)

		return factors_and_ranges
			
	except Exception:
		raise RuntimeError("Factor calculation failed!")

#getFactorsAndRanges(3)