from graphutils import GraphBuilder
from helper.properties import Mapping
from helper.units import MassUnits, DistanceUnits, MonetaryUnits, WikidataUnits
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS ,  URIRef
from StringIO import StringIO
from wrapper.dbpedia.dbpediaWrapper import DBPediaWrapper
from wrapper.worldbank.wbWrapper import wbWrapper
import helper.conversion as conv
import helper.factor as factorProvider
import helper.range as rangeProvider
import helper.units as units
import pprint
import random
import simplejson as json
import sys
import availableWrappers




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

		# Start building the final RDF graph. The "request" and part of the "query"
		# section are produced now.
		try:
			requestGraph = self.buildRequestGraph(graphBuilder, orig_unit, orig_value)
		except Exception:
			raise RuntimeError("Building the request graph failed!")

		# For debugging:
		#print(requestGraph.serialize(format='turtle'))

		# Input is normalized to base unit.
		norm_value = conv.convert(orig_value, orig_unit, quantity, RequestHandler.logString)

		# The normalized input value is divided by a partly randomized factor.
		factor = factorProvider.getFactor(norm_value, RequestHandler.logString)
		query_value = norm_value/factor
		print(RequestHandler.logString + "We will query " + str(query_value)+".")

		# A range inside which results can lie around the query value is determined.
		range = rangeProvider.getRange(query_value, RequestHandler.logString)

		# TODO Methode, die dynamisch Faktor auswaehlt, Range berechnet, Wrappers durchgeht (und das iterativ)

		# Process of wrapper selection, TODO auslagern
		possibleWrappers = availableWrappers.getAvailableWrappers(quantity)
		random.shuffle(possibleWrappers)
		currentWrapper = possibleWrappers.pop(0)

		#try:
		rdfResult = self.getData(currentWrapper, query_value, base_unit, range)
		#except Exception:
		#	raise RuntimeError("Fetching data from the wrapper failed!")

		# Process results
		if rdfResult is not None:

			# For debugging:
			print(rdfResult.serialize(format='turtle'))

			# Merge request and result graphs and add the factor
			try:
				finalGraph = graphBuilder.mergeWithResultGraph(rdfResult)
				finalGraph = graphBuilder.addFactorToGraph(factor)
			except Exception:
				raise RuntimeError("Merging request and result graphs failed!")

			# Convert output graph to JSON-LD and save as file (for debugging).
			#finalGraph.serialize(destination='graph_tests/factorFinalGraph.txt', format='turtle')
			#finalGraph.serialize(destination='graph_tests/factorFinalGraph_JSONLD.txt', format='json-ld', indent=4)

			# TODO auslagern
			if outFormat == "json":
				
				print(graphBuilder.buildJSON(factor, inValue, inUnit))
				return graphBuilder.buildJSON(factor, inValue, inUnit)
			
			elif outFormat == "json-ld":

				# Return graph to the calling program.		
				print(finalGraph.serialize(format='json-ld', indent=4))
				return finalGraph.serialize(format='json-ld', indent=4)

			else:

				raise ValueError("Return format must be 'json' or 'json-ld'! This should have been asserted before...")

		else:
			print("No results returned.")
			return None





	# When "interface" is queried as API. TODO comment.
	def getResource(self, inWrapper, inValue, inUnit, inRange):
		
		# Process values passed from the user.
		
		# Wrapper
		wrapper = inWrapper
		if wrapper != "dbpedia" and wrapper != "worldbank":
			raise ValueError("Invalid datasource. Possible values are 'dbpedia' and 'worldbank'.")

		# Value
		query_value = float(inValue)

		# Range
		# TODO change to decimal!
		range = float(inRange)

		# Unit
		base_unit = inUnit
		quantity = self.decideContext(base_unit)
		base_unit = units.baseUnit(quantity)
		
		print(RequestHandler.logString + "User query: " + str(query_value) + " " + str(base_unit) + ", range " + str(range))
		print(RequestHandler.logString + "Quantity: " + str(quantity))

		# Instance of GraphBuilder which builds the RDF graph.
		graphBuilder = GraphBuilder()

		# Build request graph
		try:
			requestGraph = self.buildRequestGraph(graphBuilder, base_unit, query_value)
		except Exception:
			raise RuntimeError("Building the request graph failed!")

		# For debugging:
		#requestGraph.serialize(destination='graph_tests/interfaceRequestGraph.txt', format='turtle')

		# Get data from wrapper
		#try:
		rdfResult = self.getData(wrapper, float(query_value), base_unit, float(range))
		#except Exception:
		#	raise RuntimeError("Fetching data from the wrapper failed!")
	
		# Merge request and result (no factor here).
		if rdfResult is not None:

			# For debugging, uncomment:
			#rdfResult.serialize(destination='graph_tests/interfaceResultGraph.txt', format='turtle')

			# Test whether merging graphs works
			try:
				finalGraph = graphBuilder.mergeWithResultGraph(rdfResult)
			except Exception:
				raise RuntimeError("Merging request and result graphs failed!")

			# Convert output graph to JSON-LD and save as file (for debugging).
			#finalGraph.serialize(destination='graph_tests/interfaceFinalGraph_JSONLD.txt', format='json-ld', indent=4)
			#finalGraph.serialize(destination='graph_tests/interfaceFinalGraph.txt', format='turtle')

			# Return to API user.
			print(finalGraph.serialize(format='json-ld', indent=4))
			return finalGraph.serialize(format='json-ld', indent=4)

		# If no result available:
		else:
			print("No results returned.")
			return None






	# Communicates with wrapper. TODO comment.
	def getData(self, inWrapper, query_value, base_unit, range):
		
		# Wrapper variable
		wrapperInstance = None

		# Create wrapper instance
		if inWrapper == "dbpedia":
			try:
				wrapperInstance = DBPediaWrapper()
			except Exception:
				raise RuntimeError('Creating a DBpediaWrapper failed.')

		elif inWrapper == "worldbank":
			try:
				wrapperInstance = wbWrapper()
			except Exception:
				raise RuntimeError('Creating a WorldbankWrapper failed.')

		else:
			raise RuntimeError("inWrapper variable not set properly! Should have been asserted before...")

		if wrapperInstance is None:
		
			raise RuntimeError("No wrapper instance could be created for an unknown reason!")

		else:

			# Which quantity?
			quantity = self.decideContext(base_unit)

			# Get results from the wrapper.			
			print(RequestHandler.logString + "Query to " + inWrapper + " wrapper: " + \
					"(" + str(quantity) + ", " + str(query_value) + ", " + str(range) +")")
			rdfResult = wrapperInstance.getResults(quantity, query_value, range)

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
