from graphutils.graphutils import GraphBuilder
from helper.conversion import Conversions
from helper.factor import Factor
from helper.properties import Mapping
from helper.range import Range
from helper.units import MassUnits, DistanceUnits, MonetaryUnits, WikidataUnits
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS ,  URIRef
from StringIO import StringIO
from wrapper.dbpedia.dbpediaWrapper import DBPediaWrapper
import helper.units as units
import pprint
import random
import simplejson as json
import sys

# Methods for factor or interface communication.
class RequestHandler: 	

	# For logging:
	logString = "APPLICATION - "

	# Is called from the server with a value, a unit, and an output format.
	# Parses the input, normalizes it, decides which wrapper to query and
	# communicates with that wrapper. Than outputs the response back to the server.
	def getResponse(self, inValue, inUnit):

		# Instance of GraphBuilder which builds the RDF graph.
		graphBuilder = GraphBuilder()

		# Values passed from the UI.
		orig_value = float(inValue)
		orig_unit = inUnit
		print(RequestHandler.logString + "User query: " + str(orig_value) + " " + str(orig_unit))

		# It is decided from orig_unit which quantity we want to query.
		quantity = self.decideContext(orig_unit)
		base_unit = units.baseUnit(quantity)
		print(RequestHandler.logString + "Base unit: " + str(base_unit))
		
		# Input is normalized to base unit.
		print(RequestHandler.logString),
		norm_value = Conversions().convert(orig_value, orig_unit, quantity)

		# The normalized input value is divided by a partly randomized factor.
		factor = Factor().getFactor(norm_value)
		print(RequestHandler.logString + "Value is divided by factor: " + str(factor))
		query_value = norm_value/factor
		print(RequestHandler.logString + "Therefore we will query " + str(query_value)+".")

		# Start building the final RDF graph. The "request" and part of the "query"
		# section are produced now.
		requestGraph = self.buildRequestGraph(graphBuilder, orig_unit, orig_value)

		# For debugging:
		requestGraph.serialize(destination='factorRequestGraph.txt', format='turtle')

		# A range inside which results can lie around the query value is determined.
		range = Range().getRange(query_value)
		print(RequestHandler.logString + "Range is " + str(range) + ", meaning values between " + 
				str(query_value-range/2) + " and " +
				str(query_value+range/2) + " can be returned.")

		# Right now, only the DBpedia wrapper is queried.
		# TODO add process to rank wrappers and call them (as soon as more than one wrapper is available)
		rdfResult = self.getData("dbpedia", query_value, base_unit, range)

		# Process results
		if rdfResult is not None:

			# For debugging:
			rdfResult.serialize(destination='factorResultGraph.txt', format='turtle')

			# Merge request and result graphs and add the factor
			finalGraph = graphBuilder.mergeWithResultGraph(rdfResult)
			finalGraph = graphBuilder.addFactorToGraph(factor)

			# Convert output graph to JSON-LD and save as file (for debugging).
			finalGraph.serialize(destination='factorFinalGraph_JSONLD.txt', format='json-ld', indent=4)

			# Return graph to the calling program.		
			return finalGraph.serialize(format='json-ld', indent=4)

		else:
			return None

	# When "interface" is queried as API. TODO comment.
	def getResource(self, wrapper, query_value, base_unit, range):
		
		# Instance of GraphBuilder which builds the RDF graph.
		graphBuilder = GraphBuilder()

		# Build request graph
		requestGraph = self.buildRequestGraph(graphBuilder, base_unit, query_value)

		# For debugging:
		requestGraph.serialize(destination='interfaceRequestGraph.txt', format='turtle')

		# Get data from wrapper
		rdfResult = self.getData(wrapper, float(query_value), base_unit, float(range))

		# Merge request and result (no factor here).
		if rdfResult is not None:

			# For debugging, uncomment:
			rdfResult.serialize(destination='interfaceResultGraph.txt', format='turtle')

			# Test whether merging graphs works
			finalGraph = graphBuilder.mergeWithResultGraph(rdfResult)

			# Convert output graph to JSON-LD and save as file (for debugging).
			finalGraph.serialize(destination='interfaceFinalGraph_JSONLD.txt', format='json-ld', indent=4)

			# Return to API user.
			return finalGraph.serialize(format='json-ld', indent=4)

		# If no result available:
		else:
			return None


	# Communicates with wrapper. TODO comment.
	def getData(self, wrapper, query_value, base_unit, range):
		try:
			dbpWrapper = DBPediaWrapper()
		except Error:
			sys.exit('ERROR: Creating a DBpediaWrapper failed.')

		# Get results from the DBpediaWrapper (kg).
		quantity = self.decideContext(base_unit)
		print(RequestHandler.logString + "Query to DBPediaWrapper: (" + str(quantity) + ", " + str(query_value) + ", " + str(range) +")")
		rdfResult = dbpWrapper.getResults(quantity, query_value, range)

		return rdfResult


	# TODO comment
	def decideContext(self, orig_unit):
		quantity = None
		for u in MassUnits:
			if orig_unit == u.value:
				quantity = Mapping.WEIGHT

		if quantity is None:
			for u in DistanceUnits:
				if orig_unit == u.value:
					quantity = Mapping.DISTANCE

		if quantity is None:
			for u in MonetaryUnits:
				if orig_unit == u.value:
					quantity = Mapping.COST

		if quantity is None: 
			sys.exit('ERROR: Unit could not be mapped to property.')
		else: 
			print(RequestHandler.logString + "The quantity we are looking for is " + str(quantity) + ".")
			return quantity


	# TODO comment
	def buildRequestGraph(self, graphBuilder, orig_unit, orig_value):
		# read wikidata unit
		orig_unit_wd = WikidataUnits.wdUnits.get(orig_unit)

		# build graph
		requestGraph = graphBuilder.buildRequestGraph(orig_value, orig_unit_wd)

		return requestGraph
