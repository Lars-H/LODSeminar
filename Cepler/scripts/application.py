from wrapper.dbpedia.dbpediaWrapper import DBPediaWrapper
import simplejson as json
from StringIO import StringIO
from helper.properties import Mapping
import random
from helper.conversion import Conversions
import helper.units as units
from helper.units import MassUnits, DistanceUnits, MonetaryUnits, WikidataUnits
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS ,  URIRef
import pprint
import sys
from helper.factor import Factor
from helper.range import Range
from graphutils.graphutils import GraphBuilder

# Is called from the server with a value, a unit, and an output format.
# Parses the input, normalizes it, decides which wrapper to query and
# communicates with that wrapper. Than outputs the response back to the server.
# Nico Haubner, 20151212
class RequestHandler: 	

	# For logging:
	logString = "APPLICATION - "

	# This method does all the work.
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
		
		# Input is normalized to base units.
		print(RequestHandler.logString)
		norm_value = Conversions().convert(orig_value, orig_unit, quantity)

		# The normalized input value is divided by a partly randomized factor.
		factor = Factor().getFactor(norm_value)
		print(RequestHandler.logString + "Value is divided by factor: " + str(factor))
		query_value = norm_value/factor
		print(RequestHandler.logString + "Therefore we will query " + str(query_value)+".")

		# Start building the final RDF graph. The "request" and part of the "query"
		# section are produced now. TODO: don't write factor before final graph.
		requestGraph = self.buildRequestGraph(graphBuilder, orig_unit, orig_value, factor)

		# A range inside which results can lie around the query value is determined.
		range = Range().getRange(query_value)
		print(RequestHandler.logString + "Range is " + str(range) + ", meaning values between " + 
				str(query_value-range/2) + " and " +
				str(query_value+range/2) + " can be returned.")

		# Right now, only the DBpedia wrapper is queried.
		# TODO add process to rank wrappers and call them.
		rdfResult = self.getResource("dbpedia", query_value, base_unit, range)

		# Process results
		outStr = ""

		if rdfResult is not None:

			# For debugging, uncomment:
			#rdfResult.serialize(destination='output.txt', format='turtle')

			# Test whether merging graphs works
			finalGraph = graphBuilder.mergeWithResultGraph(rdfResult)

			# Build an output string from the final graph.
			outStr = graphBuilder.buildOutputString(orig_unit)

			# For debugging:

			#for stmt in finalGraph:
			#	pprint.pprint(stmt)
			finalGraph.serialize(destination='finalgraph.txt', format='turtle')

		else:
			outStr = "No results matched this time. Try again!"

		# Return graph to the calling program.		
		print(RequestHandler.logString + "This output string is passed to the UI:")
		print(RequestHandler.logString + outStr)
		return outStr


	# Communicates with wrapper. TODO comment.
	def getResource(self, wrapper, query_value, base_unit, range):
		try:
			dbpWrapper = DBPediaWrapper()
		except Error:
			sys.exit('ERROR: Creating a DBpediaWrapper failed.')

		# Get results from the DBpediaWrapper (kg).
		quantity = self.decideContext(base_unit)
		print(RequestHandler.logString + "Query to DBPediaWrapper: (" + str(quantity) + ", " + str(query_value) + ", " + str(range) +")")
		rdfResult = dbpWrapper.getResults(quantity, query_value, range)

		# For debugging:

		#for stmt in finalGraph:
		#	pprint.pprint(stmt)
		rdfResult.serialize(destination='resultgraph.txt', format='turtle')

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
	def buildRequestGraph(self, graphBuilder, orig_unit, orig_value, factor):
		# read wikidata unit
		orig_unit_wd = WikidataUnits.wdUnits.get(orig_unit)

		# build graph
		requestGraph = graphBuilder.buildRequestGraph(orig_value, orig_unit_wd, factor)
		# For debugging:
		#for stmt in requestGraph:
		#		pprint.pprint(stmt)
		requestGraph.serialize(destination='requestgraph.txt', format='turtle')
		return requestGraph
