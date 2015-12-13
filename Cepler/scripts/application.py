from wrapper.dbpediaWrapper import DBPediaWrapper
import simplejson as json
from StringIO import StringIO
from helper.properties import Mapping
import random
from helper.conversion import Conversions
from helper.units import MassUnits, DistanceUnits, MonetaryUnits, WikidataUnits
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS ,  URIRef
import pprint
import sys
from helper.factor import Factor
from helper.range import Range
from graphutils.graphutils import GraphUtils

# Is called from the server with a value, a unit, and an output format.
# Parses the input, normalizes it, decides which wrapper to query and
# communicates with that wrapper. Than outputs the response back to the server.
# Nico Haubner, 20151212
class RequestHandler: 	

	# This method does all the work.
	def getResponse(self, inValue, inUnit, outFormat):

		# For logging:
		logString = "APPLICATION - "

		# Values passed from the UI.
		orig_value = float(inValue)
		orig_unit = inUnit
		out_format = outFormat
		print(logString + "User query: " + str(orig_value) + " " + str(orig_unit))

		# It is decided from orig_unit what we want to query.
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
			print(logString + "The quantity we are looking for is " + str(quantity) + ".")

		# Input is normalized to base units.
		print(logString),
		norm_value = Conversions().convert(orig_value, orig_unit, quantity)

		# The normalized input value is divided by a partly randomized factor.
		factor = Factor().getFactor(norm_value)
		print(logString + "Value is divided by factor: " + str(factor))
		query_value = norm_value/factor
		print(logString + "Therefore we will query " + str(query_value)+".")

		# Start building the final RDF graph. The "request" and part of the "query"
		# section are produced now. TODO: don't write factor before final graph.

		# read wikidata unit
		orig_unit_wd = WikidataUnits.wdUnits.get(orig_unit)

		# build graph
		graphutils = GraphUtils()
		requestGraph = graphutils.buildRequestGraph(orig_value, orig_unit_wd, factor)
		# For debugging:
		#for stmt in requestGraph:
		#		pprint.pprint(stmt)
		requestGraph.serialize(destination='requestgraph.txt', format='turtle')


		# A range inside which results can lie around the query value is determined.
		range = Range().getRange(query_value)
		print(logString + "Range is " + str(range) + ", meaning values between " + 
				str(query_value-range/2) + " and " +
				str(query_value+range/2) + " can be returned.")

		# Right now, only the DBpedia wrapper is queried.
		# TODO add process to rank wrappers and call them.
		try:
			dbpWrapper = DBPediaWrapper()
		except Error:
			sys.exit('ERROR: Creating a DBpediaWrapper failed.')

		# Get results from the DBpediaWrapper. It needs grams as input (*1000)
		# TODO unify the interface (not *1000)
		# 13122015: changed to kilogram or generally, base units
		print(logString + "Query to DBPediaWrapper: (" + str(quantity) + ", " + str(query_value) + ", " + str(range) +")")
		rdfResult = dbpWrapper.getResults(quantity, query_value, range)

		# Add some triples for final output.
		if rdfResult is not None:

		
			# For debugging, uncomment:
			#rdfResult.serialize(destination='output.txt', format='turtle')
		
			# TODO do some fancy things to output
			# TODO dependent on outformat
			#for stmt in rdfResult:
			#	pprint.pprint(stmt)

			# In progress: Process RDF graph that is coming back.
			#outStr = "You wanted a comparison for " + str(orig_value) + str(orig_unit) + "." + "\n"
			#outStr += "It equals about " + str(factor) + " "
			#
			#for rdfLabel in rdfResult.objects(BNode('result1'),RDFS.label): # should only ocurr once!
			#	outStr += rdfLabel
#
			#outStr += ". Nice!"

			# Test whether merging graphs works
			finalGraph = graphutils.mergeWithResultGraph(rdfResult)

			# For debugging:

			#for stmt in finalGraph:
			#	pprint.pprint(stmt)
			requestGraph.serialize(destination='finalgraph.txt', format='turtle')

			print(logString + "Results were written to files.")

		else: print(logString + "No result was returned!")

		# Return graph to the calling program.
		outStr = "Wait for it..."
		return outStr