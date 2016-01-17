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

		# Ask results from the wrappers.
		finalGraph = self.getFinalGraph(quantity, norm_value, base_unit, graphBuilder, out_format, orig_unit, orig_value)

		# Pass to calling method.
		return finalGraph





	# When "interface" is queried as API. Only 1:1 comparisons with a range are possible.
	def getResource(self, inWrapper, inValue, inUnit, inRange):
		
		# Process values passed from the user.
		
		# Wrapper
		wrapper = inWrapper
		if wrapper != "dbpedia" and wrapper != "worldbank":
			raise ValueError("Invalid datasource. Possible values are 'dbpedia' and 'worldbank'.")

		# Value
		query_value = float(inValue)

		# Range
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
		rdfResult = self.getData(wrapper, float(query_value), base_unit, float(range))
	
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






	# Fetches data from the datasource specified in "wrapper".
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

			if rdfResult is None:
				# Logging
				print(RequestHandler.logString + "No results could be found at " + inWrapper + ".")

			else:
				# Logging
				print(RequestHandler.logString + "Result was returned from " + inWrapper + ".")
			return rdfResult






	# Decides from "orig_unit" which quantity is going to be queried.
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






	# The request part of the final RDF graph is built.
	def buildRequestGraph(self, graphBuilder, orig_unit, orig_value):
		# read wikidata unit
		orig_unit_wd = WikidataUnits.wdUnits.get(orig_unit)

		# build graph
		requestGraph = graphBuilder.buildRequestGraph(orig_value, orig_unit_wd)

		return requestGraph





	# Iterate over possible datasources, factors and ranges and build the final graph out of the first good result.
	def getFinalGraph(self, quantity, norm_value, base_unit, graphBuilder, out_format, orig_unit, orig_value):

		# Get shuffled list of all wrappers which can process this quantity and shuffled list of factors.
		possibleWrappers = availableWrappers.getAvailableWrappers(quantity)
		possibleFactorsAndRanges = factorProvider.getFactorsAndRanges(norm_value,RequestHandler.logString)

		# Try at most 10 random factors
		currentFactor = 0
		currentRange = 0
		x = 0
		rdfResult = None
		while possibleFactorsAndRanges and not rdfResult:

			# Logging
			x = x + 1
			print(RequestHandler.logString + "Factor attempt no. " + str(x))

			# Pop first entry out of the factors and ranges
			currentFactorAndRange = possibleFactorsAndRanges.pop()
			currentFactor = currentFactorAndRange[0]
			currentRangeDecimal = currentFactorAndRange[1]
			query_value = norm_value/currentFactor
			currentRange = currentRangeDecimal*query_value
			print(RequestHandler.logString + "Factor: " + str(currentFactor) + ", range: " + str(currentRangeDecimal))
			print(RequestHandler.logString + "We will query " + str(query_value)+" and " + str(currentRange) + " around.")

			# Make a copy of possibleWrappers
			wrapperQueue = possibleWrappers[:]
			print(RequestHandler.logString + "Wrapper order: " + str(wrapperQueue))

			# try all wrappers
			currentWrapper = None
			while wrapperQueue and not rdfResult:
				currentWrapper = wrapperQueue.pop()
				rdfResult = self.getData(currentWrapper, query_value, base_unit, currentRange)


		# If result was found, merge to request graph and return final graph. Else, return None
		if rdfResult: 
			# For debugging:
			#print(rdfResult.serialize(format='turtle'))

			# Merge request and result graphs and add the factor
			finalGraph = graphBuilder.mergeWithResultGraph(rdfResult)
			finalGraph = graphBuilder.addFactorToGraph(currentFactor)

			# For debugging:
			#print(finalGraph.serialize(format='turtle'))
			#print(finalGraph.serialize(format='json-ld', indent=4))

			# Process results
			if out_format == "json":
				
				# For debugging:
				#print(graphBuilder.buildJSON(factor, orig_value, orig_unit))
				
				# Return JSON array to the calling program.
				return graphBuilder.buildJSON(currentFactor, orig_value, orig_unit)
			
			elif out_format == "json-ld":

				# For debugging:	
				#print(finalGraph.serialize(format='json-ld', indent=4))
				
				# Return graph to the calling program.	
				return finalGraph.serialize(format='json-ld', indent=4)

			else:

				raise ValueError("Return format must be 'json' or 'json-ld'! This should have been asserted before...")

		else:
			print("No results returned.")
			return None