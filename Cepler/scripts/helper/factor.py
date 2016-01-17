import random

# Receives an input value in a base unit and outputs
# a list of division factors which are partly dependent 
# on the size of the input and partly random. TODO remove old stuff
def getFactorsAndRanges(norm_value, logString='FACTOR - '):
	

	try:
		norm_value_parsed = float(norm_value)

		# possible values
		# If they shall be extended, add a list to the factors list and 
		# a corresponding range to the ranges list
		ranges = [0.01, 0.02, 0.05, 0.1, 0.2]
		factors = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
					[15, 20, 25, 30, 35, 40, 45, 50], 
					[60, 70, 80, 90, 100], 
					[150, 200, 250, 300, 350, 400, 450, 500], 
					[600, 700, 800, 900, 1000]]



		# Shuffle each factor list in order to pick random ones later.
		for x in factors:
			random.shuffle(x)


		# Take two factors out of each list and write them into the final list
		# with corresponding ranges.
		num_lists = len(factors)
		factors_and_ranges = []

		for i in range(num_lists):

			currentFactorList = factors.pop()
			currentRange = ranges.pop()

			factors_and_ranges.append((currentFactorList.pop(), currentRange))
			factors_and_ranges.append((currentFactorList.pop(), currentRange))


		# Shuffle the final list such that the factors are not ordered by size.
		random.shuffle(factors_and_ranges)

		#print(factors_and_ranges)

		return factors_and_ranges
			
	except Exception:
		raise RuntimeError("Factor calculation failed!")

#getFactorsAndRanges(1000)