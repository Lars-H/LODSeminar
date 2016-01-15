from helper.properties import Mapping
import random

# Based on the queried quantity, a list of wrappers is returned.
def getAvailableWrappers(quantity):

	if quantity == Mapping.COST:
		return random.shuffle(['dbpedia', 'worldbank'])

	elif quantity == Mapping.DISTANCE:
		return random.shuffle(['dbpedia'])

	elif quantity == Mapping.WEIGHT:
		return random.shuffle(['dbpedia'])