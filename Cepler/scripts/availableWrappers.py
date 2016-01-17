from helper.properties import Mapping
import random

# Based on the queried quantity, a list of wrappers is returned.
def getAvailableWrappers(quantity):

	result = None

	if quantity == Mapping.COST:
		result = ['dbpedia', 'worldbank']
		random.shuffle(result)
		return result

	elif quantity == Mapping.DISTANCE:
		result = ['dbpedia']
		random.shuffle(result)
		return result

	elif quantity == Mapping.WEIGHT:
		result = ['dbpedia']
		random.shuffle(result)
		return result