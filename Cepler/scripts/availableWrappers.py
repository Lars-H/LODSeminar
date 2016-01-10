from helper.properties import Mapping

# Based on the queried quantity, a list of wrappers is returned.
def getAvailableWrappers(quantity):

	if quantity == Mapping.COST:
		return ['dbpedia', 'worldbank']

	elif quantity == Mapping.DISTANCE:
		return ['dbpedia']

	elif quantity == Mapping.WEIGHT:
		return ['dbpedia']