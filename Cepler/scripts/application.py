from graphutils import GraphBuilder
from helper.factor import Factor
from helper.properties import Mapping
from helper.range import Range
from helper.units import MassUnits, DistanceUnits, MonetaryUnits, WikidataUnits
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS ,  URIRef
from StringIO import StringIO
from wrapper.dbpedia.dbpediaWrapper import DBPediaWrapper
import helper.conversion as conv
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
	def getResponse(self, inValue, inUnit, outFormat):

		# Process values passed from the UI.
		
		# Value
		orig_value = float(inValue)

		# Format
		out_format = outFormat
		if out_format != "json" and out_format != "json-ld":
			raise ValueError("Invalid return format. Possible values are 'json' and 'json-ld'.")

		# Unit
		orig_unit = inUnit
		quantity = self.decideContext(orig_unit)
		base_unit = units.baseUnit(quantity)
		
		print(RequestHandler.logString + "User query: " + str(orig_value) + " " + str(orig_unit) + ", return " + out_format)
		print(RequestHandler.logString + "Quantity: " + str(quantity))
		print(RequestHandler.logString + "Base unit: " + str(base_unit))

		# Instance of GraphBuilder which builds the RDF graph.
		graphBuilder = GraphBuilder()

		# Input is normalized to base unit.
		print(RequestHandler.logString),
		norm_value = conv.convert(orig_value, orig_unit, quantity)

		# The normalized input value is divided by a partly randomized factor.
		factor = Factor().getFactor(norm_value)
		print(RequestHandler.logString + "Value is divided by factor: " + str(factor))
		query_value = norm_value/factor
		print(RequestHandler.logString + "Therefore we will query " + str(query_value)+".")

		# Start building the final RDF graph. The "request" and part of the "query"
		# section are produced now.
		try:
			requestGraph = self.buildRequestGraph(graphBuilder, orig_unit, orig_value)
		except Exception:
			raise RuntimeError("Building the request graph failed!")

		# For debugging:
		requestGraph.serialize(destination='graph_tests/factorRequestGraph.txt', format='turtle')

		# A range inside which results can lie around the query value is determined.
		range = Range().getRange(query_value)
		print(RequestHandler.logString + "Range is " + str(range) + ", meaning values between " + 
				str(query_value-range/2) + " and " +
				str(query_value+range/2) + " can be returned.")

		# Right now, only the DBpedia wrapper is queried.
		# TODO add process to rank wrappers and call them (as soon as more than one wrapper is available)
		try:
			rdfResult = self.getData("dbpedia", query_value, base_unit, range)
		except Exception:
			raise RuntimeError("Fetching data from the wrapper failed!")

		# Process results
		if rdfResult is not None:

			# For debugging:
			rdfResult.serialize(destination='graph_tests/factorResultGraph.txt', format='turtle')

			# Merge request and result graphs and add the factor
			try:
				finalGraph = graphBuilder.mergeWithResultGraph(rdfResult)
				finalGraph = graphBuilder.addFactorToGraph(factor)
			except Exception:
				raise RuntimeError("Merging request and result graphs failed!")

			# Convert output graph to JSON-LD and save as file (for debugging).
			finalGraph.serialize(destination='graph_tests/factorFinalGraph.txt', format='turtle')
			finalGraph.serialize(destination='graph_tests/factorFinalGraph_JSONLD.txt', format='json-ld', indent=4)

			# TODO process outFormat parameter here! TODO auslagern

			if outFormat == "json":
				
				# INPROGRESS: Build a JSON document
				print(graphBuilder.buildJSON(factor, inValue, inUnit))
				return graphBuilder.buildJSON(factor, inValue, inUnit)
			
			elif outFormat == "json-ld":

				# Return graph to the calling program.		
				print(finalGraph.serialize(format='json-ld', indent=4))
				return finalGraph.serialize(format='json-ld', indent=4)

			else:

				raise ValueError("Return format must be 'json' or 'json-ld'! This should have been asserted before...")

		else:
			return None

	# When "interface" is queried as API. TODO comment.
	def getResource(self, wrapper, query_value, base_unit, range):
		
		# Instance of GraphBuilder which builds the RDF graph.
		graphBuilder = GraphBuilder()

		# Build request graph
		try:
			requestGraph = self.buildRequestGraph(graphBuilder, base_unit, query_value)
		except Exception:
			raise RuntimeError("Building the request graph failed!")

		# For debugging:
		requestGraph.serialize(destination='graph_tests/interfaceRequestGraph.txt', format='turtle')

		# Get data from wrapper
		try:
			rdfResult = self.getData(wrapper, float(query_value), base_unit, float(range))
		except Exception:
			raise RuntimeError("Fetching data from the wrapper failed!")
	
		# Merge request and result (no factor here).
		if rdfResult is not None:

			# For debugging, uncomment:
			rdfResult.serialize(destination='graph_tests/interfaceResultGraph.txt', format='turtle')

			# Test whether merging graphs works
			try:
				finalGraph = graphBuilder.mergeWithResultGraph(rdfResult)
			except Exception:
				raise RuntimeError("Merging request and result graphs failed!")

			# Convert output graph to JSON-LD and save as file (for debugging).
			finalGraph.serialize(destination='graph_tests/interfaceFinalGraph_JSONLD.txt', format='json-ld', indent=4)
			finalGraph.serialize(destination='graph_tests/interfaceFinalGraph.txt', format='turtle')

			# Return to API user.
			print(finalGraph.serialize(format='json-ld', indent=4))
			return finalGraph.serialize(format='json-ld', indent=4)

		# If no result available:
		else:
			return None


	# Communicates with wrapper. TODO comment.
	def getData(self, wrapper, query_value, base_unit, range):
		try:
			dbpWrapper = DBPediaWrapper()
		except Exception:
			raise RuntimeError('Creating a DBpediaWrapper failed.')

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
			raise ValueError("Sorry, invalid unit. Check for typos.")
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
