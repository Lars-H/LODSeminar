from wrapper.dbpediaWrapper import DBPediaWrapper
import simplejson as json
from StringIO import StringIO
from helper.properties import Mapping
import random
from helper.conversion import Conversions
from helper.units import MassUnits, DistanceUnits, MonetaryUnits
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS ,  URIRef
import pprint
import sys
from helper.factor import Factor
from helper.range import Range

# Is called from the server with a value, a unit, and an output format.
# Parses the input, normalizes it, decides which wrapper to query and
# communicates with that wrapper. Than outputs the response back to the server.
# Nico Haubner, 20151212
class RequestHandler: 	

	# This method does all the work.
	def getResponse(self, inValue, inUnit, outFormat):

		# Values passed from the UI.
		orig_value = float(inValue)
		orig_unit = inUnit
		out_format = outFormat

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

		if quantity is None: sys.exit('ERROR: Unit could not be mapped to property.')

		# Input is normalized to base units.
		norm_value = Conversions().convert(orig_value, orig_unit, quantity)

		# The normalized input value is divided by a partly randomized factor.
		factor = Factor().getFactor(norm_value)
		query_value = norm_value/factor

		# A range inside which results can lie around the query value is determined.
		range = Range().getRange(query_value)

		# For debugging. TODO remove.
		print(norm_value, factor, query_value, query_value-range/2, query_value+range/2)

		# Right now, only the DBpedia wrapper is queried.
		# TODO add process to rank wrappers and call them.
		try:
			dbpWrapper = DBPediaWrapper()
		except Error:
			sys.exit('ERROR: Creating a DBpediaWrapper failed.')

		# Get results from the DBpediaWrapper. It needs grams as input (*1000)
		rdfResult = dbpWrapper.getResults(quantity, query_value*1000, range*1000)

		# Add some triples for final output.
		if rdfResult is not None:

			result = BNode('result1')
		
		
			rdfResult.add( (result, RDF.value , Literal(orig_value) ))
			rdfResult.add( (result, URIRef("http://www.w3.org/ns/org#hasUnit") , URIRef("http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#Kilogram") ))
			rdfResult.add( (result, URIRef("http://dbpedia.org/ontology/ratio"), Literal(factor) ))
		
			rdfResult.serialize(destination='output.txt', format='turtle')
		
			# TODO do some fancy things to output
			# TODO dependent on outformat
			for stmt in rdfResult:
				pprint.pprint(stmt)
		
		# Return graph to the calling program.
		return rdfResult